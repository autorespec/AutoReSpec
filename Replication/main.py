import time
from pathlib import Path
import copy
from  completeness.completeness import verify_generated_spec
from config import config
from prompt.prompt_generation import (
    extract_err_type,
    create_specialized_patcher_prompt_config,
    gen_extra_guidance,
    create_generation_prompt_config,
    gpt_collaborator_llm_initial_prompt_generation,
    claude_collaborator_llm_initial_prompt_generation,
)
from utils.code_parser import (
    parsed_code_from_llm,
    parsed_code_from_chatgpt,
    parsed_code_from_claude,
)
from utils.llm_recommender import recommend_LLMs
from utils.token_counter import count_gpt_config_token
from utils.utils import print_config, create_csv, append_csv, get_current_time_str
from utils.checkOllama import check_ollama_and_models


def run_timer(sleep_time):
    print(f"\nRunning a {sleep_time} second timer...")
    time.sleep(sleep_time)
    print("Timer complete!")

def token_limit_fitter(gpt_llm_config, token_limit=2000):
    """
    Trims the messages in the LLM config until the total token count is below the specified limit.
    Always retains the first user message as context.
    """
    res = copy.deepcopy(gpt_llm_config)

    original_first_message = res["messages"][0]

    print(f"Initial token count: {count_gpt_config_token(res)}")

    while count_gpt_config_token(res) > token_limit:
        if len(res["messages"]) <= 2:
            break

        res["messages"] = [original_first_message] + res["messages"][2:]

    return res


def initialize_directories():
    base_dirs = {
        "log_dir": Path(f"eval/logs/"),
        "out_dir": Path(f"eval/out/"),
        "result_dir": Path(f"eval/result/"),
    }

    base_dirs["metrics_dir"] = base_dirs["result_dir"] / "metrics"

    for directory in base_dirs.values():
        directory.mkdir(parents=True, exist_ok=True)

    return base_dirs


def initialize_csv_files(metrics_dir, current_time, model_role="primary"):
    metrics_file = metrics_dir / f"eval_{model_role}_{current_time}.csv"

    metrics_field_names = [
        "file_name",
        "LLM",
        "time",
        "trial",
        "iteration",
        "passed",
        "llm_response_seconds",
        "validator_response_seconds",
        "log_location",
        "output_location",
        "remarks",
    ]

    create_csv(metrics_file, metrics_field_names)

    return (
        metrics_file,
        metrics_field_names,
    )


def initialize_collaborator_directories(
        directories,
        collaborator_model_name,
):
    collaborator_dirs = {
        "collaborator_out_dir": directories["out_dir"] / collaborator_model_name,
        "collaborator_metrics_dir": directories["metrics_dir"]
                                    / collaborator_model_name,
    }

    for path in collaborator_dirs.values():
        path.mkdir(parents=True, exist_ok=True)

    return collaborator_dirs


def run_llm_iterations(
        llm_config,
        class_name,
        out_dir,
        metrics_file,
        metrics_field_names,
        f_log,
        f_log_location,
        trial=1,
        max_validator_calls=10,
        model="llama3:8b",
):
    parsed_specified_code, err_info = "", ""
    for i in range(1, max_validator_calls + 1):
        print(f"primary llm iteration:{i} \n")
        f_log.write(f"primary llm iteration:{i}\n")
        try:
            if i == 1:
                parsed_specified_code, err_info, is_passed = parsed_code_from_llm(
                    llm_config=llm_config,
                    class_name=class_name,
                    out_dir=out_dir,
                    metrics_file=metrics_file,
                    metrics_field_names=metrics_field_names,
                    f_log=f_log,
                    f_log_location=f_log_location,
                    trial=trial,
                    iteration=i,
                    model_name=model,
                )
                llm_config["messages"].append(
                    {
                        "role": "assistant",
                        "content": f"```java\n{parsed_specified_code}\n```",
                    }
                )

                if is_passed:
                    return True, parsed_specified_code, ""

            else:
                err_types = extract_err_type(err_info)
                if err_types:
                    patcher_llm_config = create_specialized_patcher_prompt_config(
                        model_name=model,
                        original_code=parsed_specified_code,
                        err_info=err_info,
                    )
                    print_config(patcher_llm_config)
                    parsed_specified_code, err_info, is_passed = parsed_code_from_llm(
                        llm_config=patcher_llm_config,
                        class_name=class_name,
                        out_dir=out_dir,
                        metrics_file=metrics_file,
                        metrics_field_names=metrics_field_names,
                        f_log=f_log,
                        f_log_location=f_log_location,
                        trial=trial,
                        iteration=i,
                        model_name=model,
                    )
                    llm_config["messages"][-1][
                        "content"
                    ] = f"```java\n{parsed_specified_code}\n```"
                    if is_passed:
                        return True, parsed_specified_code, ""

                else:
                    refine_msg = {
                        "role": "user",
                        "content": config.get("FORMAT_REFINE_PROMPT").replace(
                            "{err_info}", err_info
                        ),
                    }
                    refine_msg["content"] += gen_extra_guidance(err_info)
                    llm_config["messages"].append(refine_msg)
                    print_config(llm_config)

                    parsed_specified_code, err_info, is_passed = parsed_code_from_llm(
                        llm_config=llm_config,
                        class_name=class_name,
                        out_dir=out_dir,
                        metrics_file=metrics_file,
                        metrics_field_names=metrics_field_names,
                        f_log=f_log,
                        f_log_location=f_log_location,
                        trial=trial,
                        iteration=i,
                        model_name=model,
                    )
                    llm_config["messages"].append(
                        {
                            "role": "assistant",
                            "content": f"```\n{parsed_specified_code}\n```",
                        }
                    )

                    if is_passed:
                        return True, parsed_specified_code, ""

        except Exception as e:
            print(f"Error: {e}")
            f_log.write(str(e) + "\n")
            append_csv(
                metrics_file,
                metrics_field_names,
                {
                    "file_name": class_name,
                    "LLM": model,
                    "time": get_current_time_str(),
                    # "index": index,
                    "trial": trial,
                    "iteration": i,
                    "passed": False,
                    "log_location": f_log_location,
                    "output_location": "NA",
                    "remarks": f"Error: {e}",
                },
            )
            continue
    return False, err_info, parsed_specified_code


def run_gpt_collaborative_llm(
        collaborator_llm_config,
        class_name,
        out_dir,
        collaborator_metrics_file,
        metrics_field_names,
        f_log,
        f_log_location,
        trial=1,
        collaborator_max_validator_calls=10,
):
    parsed_specified_code, err_info = "", ""
    for collaborator_iteration in range(1, collaborator_max_validator_calls + 1):
        print(f"collaborative llm iteration:{collaborator_iteration} \n")
        f_log.write(f"collaborative llm iteration:{collaborator_iteration}\n")

        try:
            if collaborator_iteration == 1:
                parsed_specified_code, err_info, is_passed = parsed_code_from_chatgpt(
                    llm_config=collaborator_llm_config,
                    class_name=class_name,
                    out_dir=out_dir,
                    gpt_metrics_file=collaborator_metrics_file,
                    metrics_field_names=metrics_field_names,
                    f_log=f_log,
                    f_log_location=f_log_location,
                    trial=trial,
                    iteration=collaborator_iteration,
                )

                collaborator_llm_config["messages"].append(
                    {
                        "role": "assistant",
                        "content": "```java\n{code}\n```".format(
                            code=parsed_specified_code
                        ),
                    }
                )

                if is_passed:
                    return True, parsed_specified_code, ""

            else:
                err_types = extract_err_type(err_info)
                if err_types:
                    patcher_llm_config = create_specialized_patcher_prompt_config(
                        model_name="gpt-4o",
                        original_code=parsed_specified_code,
                        err_info=err_info,
                        gpt=True,
                    )
                    print_config(patcher_llm_config)
                    parsed_specified_code, err_info, is_passed = (
                        parsed_code_from_chatgpt(
                            llm_config=patcher_llm_config,
                            class_name=class_name,
                            out_dir=out_dir,
                            gpt_metrics_file=collaborator_metrics_file,
                            metrics_field_names=metrics_field_names,
                            f_log=f_log,
                            f_log_location=f_log_location,
                            trial=trial,
                            iteration=collaborator_iteration,
                        )
                    )

                    collaborator_llm_config["messages"][-1][
                        "content"
                    ] = f"```java\n{parsed_specified_code}\n```"

                    if is_passed:
                        return True, parsed_specified_code, ""
                else:
                    refine_msg = {
                        "role": "user",
                        "content": config.get("FORMAT_REFINE_PROMPT").replace(
                            "{err_info}", err_info
                        ),
                    }
                    refine_msg["content"] += gen_extra_guidance(err_info)
                    collaborator_llm_config["messages"].append(refine_msg)
                    print_config(collaborator_llm_config)
                    # print(collaborator_llm_config)
                    # TODO: handle token limit
                    fitted_llm_config = token_limit_fitter(
                        gpt_llm_config=collaborator_llm_config, token_limit=2000
                    )
                    parsed_specified_code, err_info, is_passed = (
                        parsed_code_from_chatgpt(
                            llm_config=fitted_llm_config,
                            class_name=class_name,
                            out_dir=out_dir,
                            gpt_metrics_file=collaborator_metrics_file,
                            metrics_field_names=metrics_field_names,
                            f_log=f_log,
                            f_log_location=f_log_location,
                            trial=trial,
                            iteration=collaborator_iteration,
                        )
                    )

                    collaborator_llm_config["messages"].append(
                        {
                            "role": "assistant",
                            "content": f"```\n{parsed_specified_code}\n```",
                        }
                    )
                    if is_passed:
                        return True, parsed_specified_code, ""
        except Exception as e:
            print(f"Error: {e}")
            f_log.write(str(e) + "\n")
            append_csv(
                file_name=collaborator_metrics_file,
                fieldnames=metrics_field_names,
                file_dict={
                    "file_name": class_name,
                    "LLM": "gpt-4o",
                    "time": get_current_time_str(),
                    "trial": trial,
                    "iteration": 10,
                    "passed": False,
                    "log_location": f_log_location,
                    "output_location": "NA",
                    "remarks": f"errored: {e}",
                },
            )
            continue
    return False, err_info, parsed_specified_code


def run_claude_collaborative_llm(
        collaborator_llm_config,
        class_name,
        out_dir,
        collaborator_metrics_file,
        metrics_field_names,
        f_log,
        f_log_location,
        trial,
):
    parsed_specified_code, err_info = "", ""
    collaborator_max_validator_calls = config.get(
        "collaborator_max_validator_calls", 10
    )

    for collaborator_iteration in range(1, collaborator_max_validator_calls + 1):
        print(f"collaborative llm iteration:{collaborator_iteration} \n")
        f_log.write(f"collaborative llm iteration:{collaborator_iteration}\n")

        try:
            if collaborator_iteration == 1:
                # where is the initial prompt?
                parsed_specified_code, err_info, is_passed = parsed_code_from_claude(
                    llm_config=collaborator_llm_config,
                    class_name=class_name,
                    out_dir=out_dir,
                    metrics_file=collaborator_metrics_file,
                    metrics_field_names=metrics_field_names,
                    f_log=f_log,
                    f_log_location=f_log_location,
                    trial=trial,
                    iteration=collaborator_iteration,
                )

                collaborator_llm_config["messages"].append(
                    {
                        "role": "assistant",
                        "content": "```java\n{code}\n```".format(
                            code=parsed_specified_code
                        ),
                    }
                )

                if is_passed:
                    return True, parsed_specified_code, ""

            else:
                err_types = extract_err_type(err_info)
                if err_types:
                    patcher_llm_config = create_specialized_patcher_prompt_config(
                        model_name="claude-3-7-sonnet-20250219",
                        original_code=parsed_specified_code,
                        err_info=err_info,
                        claude=True
                    )
                    print_config(patcher_llm_config)
                    parsed_specified_code, err_info, is_passed = (
                        parsed_code_from_claude(
                            llm_config=patcher_llm_config,
                            class_name=class_name,
                            out_dir=out_dir,
                            metrics_file=collaborator_metrics_file,
                            metrics_field_names=metrics_field_names,
                            f_log=f_log,
                            f_log_location=f_log_location,
                            trial=trial,
                            iteration=collaborator_iteration,
                        )
                    )

                    collaborator_llm_config["messages"][-1][
                        "content"
                    ] = f"```java\n{parsed_specified_code}\n```"

                    if is_passed:
                        return True, parsed_specified_code, ""
                else:
                    refine_msg = {
                        "role": "user",
                        "content": config.get("FORMAT_REFINE_PROMPT").replace(
                            "{err_info}", err_info
                        ),
                    }
                    refine_msg["content"] += gen_extra_guidance(err_info)
                    collaborator_llm_config["messages"].append(refine_msg)
                    print_config(collaborator_llm_config)
                    parsed_specified_code, err_info, is_passed = (
                        parsed_code_from_claude(
                            llm_config=collaborator_llm_config,
                            class_name=class_name,
                            out_dir=out_dir,
                            metrics_file=collaborator_metrics_file,
                            metrics_field_names=metrics_field_names,
                            f_log=f_log,
                            f_log_location=f_log_location,
                            trial=trial,
                            iteration=collaborator_iteration,
                        )
                    )

                    collaborator_llm_config["messages"].append(
                        {
                            "role": "assistant",
                            "content": f"```\n{parsed_specified_code}\n```",
                        }
                    )
                    if is_passed:
                        return True, parsed_specified_code, ""
        except Exception as e:
            print(f"Error: {e}")
            f_log.write(str(e) + "\n")
            append_csv(
                file_name=collaborator_metrics_file,
                fieldnames=metrics_field_names,
                file_dict={
                    "file_name": class_name,
                    "LLM": "claude-3-7-sonnet-20250219",
                    "time": get_current_time_str(),
                    # "index": index,
                    "trial": trial,
                    "iteration": 10,
                    "passed": False,
                    "log_location": f_log_location,
                    "output_location": "NA",
                    "remarks": f"errored: {e}",
                },
            )
            continue
    return False, err_info, parsed_specified_code


# include non-gpt initial models
def main(evaluation_dir_path, collaborate=True, trial=1):
    evaluation_dir = Path(evaluation_dir_path)
    if not evaluation_dir.is_dir():
        raise ValueError(f"{evaluation_dir} is not a valid directory")

    java_files = [
        f for f in evaluation_dir.iterdir() if f.is_file() and f.suffix == ".java"
    ]

    testcases = [(str(f.resolve()), f.stem) for f in java_files]
    directories = initialize_directories()

    for file_path, class_name in testcases:
        print(f"======= file name: {class_name} =======")
        with open(file_path, "r") as f:
            code = f.read()
        program_type, llm_pair = recommend_LLMs(code)
        model_name = llm_pair["primaryLLM"]["model"]
        few_shot_count = llm_pair["primaryLLM"]["shot_count"]
        collaborator_model_name = llm_pair["collaborativeLLM"]["model"]
        collaborator_few_shot = llm_pair["collaborativeLLM"]["shot_count"]

        print(f"recommended primary models: {model_name}")
        check_ollama_and_models([model_name])
        print(f"recommended collaborative models: {collaborator_model_name}")

        is_collaborate_gpt = collaborator_model_name.startswith("gpt")
        collaborator_dirs = initialize_collaborator_directories(
            directories, collaborator_model_name
        )

        for trial in range(1, trial+1):
            trial_timestamp = get_current_time_str()
            metrics_file, metrics_field_names = initialize_csv_files(
                directories["metrics_dir"],
                trial_timestamp + f"_{model_name}_{class_name}",
                model_role="primary",
            )
            collaborator_metrics_file, collaborator_metrics_fields = (
                initialize_csv_files(
                    collaborator_dirs["collaborator_metrics_dir"],
                    trial_timestamp + f"_{collaborator_model_name}_{class_name}",
                    model_role="collaborator",
                )
            )
            print(
                model_name,
                few_shot_count,
                collaborator_model_name,
                collaborator_few_shot,
            )
            f_log_location = str(
                directories["log_dir"]
                / f"log_{class_name}_{get_current_time_str()}.txt"
            )
            f_log = open(f_log_location, "w")
            llm_config = create_generation_prompt_config(
                model_name=model_name,
                input_code_path=file_path,
                class_name=class_name,

            )
            print_config(llm_config)
            is_passed, err_info, parsed_specified_code = run_llm_iterations(
                llm_config=llm_config,
                class_name=class_name,
                out_dir=directories["out_dir"],
                metrics_file=metrics_file,
                metrics_field_names=metrics_field_names,
                f_log=f_log,
                f_log_location=f_log_location,
                trial=trial,
                max_validator_calls=10,
                model=model_name,
            )
            print("=========== primary done ===========")
            print("is_passed", is_passed)
            print("error info", err_info)
            verify_generated_spec(parsed_specified_code, class_name)
            print("parsed_specified_code", parsed_specified_code)
            if not is_passed:
                f_log.write(
                    f"\n{'*' * 8} using collaborative llm: {collaborator_model_name} {'*' * 8}\n"
                )
                if is_collaborate_gpt:
                    collaborator_llm_config = (
                        gpt_collaborator_llm_initial_prompt_generation(
                            input_code_path=file_path,
                            class_name=class_name,
                            specified_code=parsed_specified_code,
                            err_info=err_info,

                        )
                    )


                    print_config(collaborator_llm_config)

                    is_passed, err_info, parsed_specified_code = (
                        run_gpt_collaborative_llm(
                            collaborator_llm_config=collaborator_llm_config,
                            class_name=class_name,
                            out_dir=collaborator_dirs["collaborator_out_dir"],
                            collaborator_metrics_file=collaborator_metrics_file,
                            metrics_field_names=metrics_field_names,
                            f_log=f_log,
                            f_log_location=f_log_location,
                            trial=trial,
                            collaborator_max_validator_calls=10,
                        )
                    )
                    print("=========== colab done: GPT-4o ===========")
                    print("is_passed", is_passed)
                    print("error info", err_info)
                    if is_passed:
                        verify_generated_spec(parsed_specified_code, class_name)
                    print("parsed_specified_code", parsed_specified_code)
                else:
                    collaborator_llm_config = (
                        claude_collaborator_llm_initial_prompt_generation(
                            input_code_path=file_path,
                            class_name=class_name,
                            specified_code=parsed_specified_code,
                            err_info=err_info,

                        )
                    )
                    print_config(collaborator_llm_config)
                    # TODO: change here for taking gpt as an if else block
                    is_passed, err_info, parsed_specified_code = (
                        run_claude_collaborative_llm(
                            collaborator_llm_config=collaborator_llm_config,
                            class_name=class_name,
                            out_dir=collaborator_dirs["collaborator_out_dir"],
                            collaborator_metrics_file=collaborator_metrics_file,
                            metrics_field_names=metrics_field_names,
                            f_log=f_log,
                            f_log_location=f_log_location,
                            # index,
                            trial=trial,
                        )
                    )
                    print("=========== colab done: Claude ===========")
                    print("is_passed", is_passed)
                    print("error info", err_info)
                    if is_passed:
                        verify_generated_spec(parsed_specified_code, class_name)
                    print("parsed_specified_code", parsed_specified_code)
            f_log.close()
            run_timer(1)




if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run AutoSpecGen pipeline on a directory of Java test case files.")

    parser.add_argument(
        "--testcase_dir",
        type=str,
        default="./motivatingExample",
        help="Path to the directory containing Java test case files (default: motivatingExample)"
    )

    parser.add_argument(
        "--no-collaborate",
        dest="collaborate",
        action="store_false",
        help="Disable collaborative LLM refinement (default: enabled)"
    )
    parser.set_defaults(collaborate=True)  # default is True

    parser.add_argument(
        "--trial",
        type=int,
        default=1,
        help="Number of refinement trials per test case (default: 1)"
    )

    args = parser.parse_args()
    testcase_dir = args.testcase_dir
    collaborate = args.collaborate
    trial_count = args.trial

    print(f"Evaluating {testcase_dir} with collaborate={collaborate} for {trial_count} trial(s).")

    main(testcase_dir, collaborate, trial_count)