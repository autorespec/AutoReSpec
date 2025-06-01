import json

from prompt.prompt_generation import provide_good_feedback_gpt, provide_good_feedback_claude
from utils.cost import measure_time
from utils.llm_wrapper import request_llm_engine, request_chatgpt_engine, request_claude_engine
from utils.logging import save_and_log_result
from utils.utils import parse_code_from_reply, append_csv, get_current_time_str, parse_code_from_chatgpt_reply, \
    parse_code_from_claude_reply
from validator.validate import validate_openjml


def parsed_code_from_llm(llm_config, class_name, out_dir, metrics_file,
                         metrics_field_names, f_log, f_log_location, trial, iteration, model_name):
    f_log.write(f"{'*' * 8} prompt {'*' * 8}\n")
    f_log.write(json.dumps(llm_config, indent=2) + "\n")

    print("\nparsing response from LLM ...")
    ret, llm_response_time_delta = measure_time(
        request_llm_engine, llm_config
    )

    f_log.write(f"{'*' * 8} parsed response {'*' * 8}\n")
    f_log.write(json.dumps(ret.dict(), indent=2) + "\n")
    print(f"LLM response execution time: {llm_response_time_delta:.6f} seconds")

    content = ret.message.content
    print(content)

    print("\nparsing code from LLM response ...")
    # TODO: handle no code response here!!
    if "```" not in content:
        raise ValueError("LLM response did not contain a code block!")

    parsed_specified_code = parse_code_from_reply(content)
    print(parsed_specified_code)

    # log the parsed code in the log file
    f_log.write(f"{'*' * 8} parsed code {'*' * 8}\n")
    f_log.write(parsed_specified_code + "\n")

    # validate code using openjml
    print("\nvalidating code with OpenJML ...")

    # measure time and handle validator timeout of 30 minutes
    err_info, validator_response_time_delta = measure_time(
        validate_openjml, parsed_specified_code, class_name
    )

    print(f"Validator execution time: {validator_response_time_delta:.6f} seconds")
    print(err_info)

    # log the validator errors
    f_log.write(f"{'*' * 8} validator error {'*' * 8}\n")
    f_log.write(err_info + "\n")

    is_passed = len(err_info) == 0

    if is_passed:
        output_location = save_and_log_result(class_name, parsed_specified_code, out_dir)
        append_csv(metrics_file, metrics_field_names, {
            "file_name": class_name,
            "LLM": model_name,
            "time": get_current_time_str(),
            # "index": index,
            "trial": trial,
            "iteration": iteration,
            "passed": is_passed,
            "log_location": f_log_location,
            "output_location": output_location,
            "llm_response_seconds": llm_response_time_delta,
            "validator_response_seconds": validator_response_time_delta,
        })
        print(f"Passed on iteration {iteration}, no error for file {output_location}!")
        # provide_good_feedback(llm_config, f_log)
        f_log.close()
    else:
        append_csv(metrics_file, metrics_field_names, {
            "file_name": class_name,
            "LLM": model_name,
            "time": get_current_time_str(),
            # "index": index,
            "trial": trial,
            "iteration": iteration,
            "passed": is_passed,
            "log_location": f_log_location,
            "output_location": 'NA',
            "llm_response_seconds": llm_response_time_delta,
            "validator_response_seconds": validator_response_time_delta,
        })
    return parsed_specified_code, err_info, is_passed


def parsed_code_from_chatgpt(llm_config, class_name, out_dir, gpt_metrics_file,
                             metrics_field_names, f_log, f_log_location, trial, iteration):
    f_log.write(f"{'*' * 8} prompt {'*' * 8}\n")
    f_log.write(json.dumps(llm_config, indent=2) + "\n")

    print("\nparsing response from LLM ...")
    # TODO: test here
    ret, llm_response_time_delta = measure_time(
        lambda: request_chatgpt_engine(llm_config)
    )

    f_log.write(f"{'*' * 8} parsed response {'*' * 8}\n")
    f_log.write(json.dumps(ret.dict(), indent=2) + "\n")
    print(f"LLM response execution time: {llm_response_time_delta:.6f} seconds")

    content = ret.choices[0].message.content
    # response.choices[0].message.content
    print(content)

    print("\nparsing code from LLM response ...")
    # TODO: handle no code response here!!
    if "```" not in content:
        raise ValueError("LLM response did not contain a code block!")

    parsed_specified_code = parse_code_from_chatgpt_reply(content)
    print(parsed_specified_code)

    # log the parsed code in the log file
    f_log.write(f"{'*' * 8} parsed code {'*' * 8}\n")
    f_log.write(parsed_specified_code + "\n")

    # validate code using openjml
    print("\nvalidating code with OpenJML ...")

    # measure time and handle validator timeout of 30 minutes
    err_info, validator_response_time_delta = measure_time(
        validate_openjml, parsed_specified_code, class_name
    )

    print(f"Validator execution time: {validator_response_time_delta:.6f} seconds")
    print(err_info)

    # log the validator errors
    f_log.write(f"{'*' * 8} validator error {'*' * 8}\n")
    f_log.write(err_info + "\n")

    is_passed = len(err_info) == 0

    if is_passed:
        output_location = save_and_log_result(class_name, parsed_specified_code, out_dir)
        append_csv(gpt_metrics_file, metrics_field_names, {
            "file_name": class_name,
            "LLM": "gpt-4o",
            "time": get_current_time_str(),
            # "index": index,
            "trial": trial,
            "iteration": iteration,
            "passed": is_passed,
            "log_location": f_log_location,
            "output_location": output_location,
            "llm_response_seconds": llm_response_time_delta,
            "validator_response_seconds": validator_response_time_delta,
        })
        print(f"Passed on iteration {iteration}, no error for file {output_location}!")
        provide_good_feedback_gpt(llm_config, f_log)
        f_log.close()
    # write the metrics file
    else:
        append_csv(gpt_metrics_file, metrics_field_names, {
            "file_name": class_name,
            "LLM": "gpt-4o",
            "time": get_current_time_str(),
            # "index": index,
            "trial": trial,
            "iteration": iteration,
            "passed": is_passed,
            "log_location": f_log_location,
            "output_location": 'NA',
            "llm_response_seconds": llm_response_time_delta,
            "validator_response_seconds": validator_response_time_delta,
        })
    return parsed_specified_code, err_info, is_passed


def parsed_code_from_claude(llm_config, class_name, out_dir, metrics_file,
                             metrics_field_names, f_log, f_log_location,
                            # index,
                            trial, iteration):
    f_log.write(f"{'*' * 8} prompt {'*' * 8}\n")
    f_log.write(json.dumps(llm_config, indent=2) + "\n")

    print("\nparsing response from Claude ...")
    # TODO: test here
    ret, llm_response_time_delta = measure_time(
        lambda: request_claude_engine(llm_config)
    )

    f_log.write(f"{'*' * 8} parsed response {'*' * 8}\n")
    f_log.write(json.dumps(ret.dict(), indent=2) + "\n")
    print(f"Claude response execution time: {llm_response_time_delta:.6f} seconds")

    content = ret.content[0].text
    # response.choices[0].message.content
    print(content)

    print("\nparsing code from LLM response ...")
    # TODO: handle no code response here!!
    if "```" not in content:
        raise ValueError("LLM response did not contain a code block!")

    parsed_specified_code = parse_code_from_claude_reply(content)
    print(parsed_specified_code)

    # log the parsed code in the log file
    f_log.write(f"{'*' * 8} parsed code {'*' * 8}\n")
    f_log.write(parsed_specified_code + "\n")

    # validate code using openjml
    print("\nvalidating code with OpenJML ...")

    # measure time and handle validator timeout of 30 minutes
    err_info, validator_response_time_delta = measure_time(
        validate_openjml, parsed_specified_code, class_name
    )

    print(f"Validator execution time: {validator_response_time_delta:.6f} seconds")
    print(err_info)

    # log the validator errors
    f_log.write(f"{'*' * 8} validator error {'*' * 8}\n")
    f_log.write(err_info + "\n")

    is_passed = len(err_info) == 0

    if is_passed:
        output_location = save_and_log_result(class_name, parsed_specified_code, out_dir)
        append_csv(metrics_file, metrics_field_names, {
            "file_name": class_name,
            "LLM": "claude-3.7",
            "time": get_current_time_str(),
            # "index": index,
            "trial": trial,
            "iteration": iteration,
            "passed": is_passed,
            "log_location": f_log_location,
            "output_location": output_location,
            "llm_response_seconds": llm_response_time_delta,
            "validator_response_seconds": validator_response_time_delta,
        })
        print(f"Passed on iteration {iteration}, no error for file {output_location}!")
        provide_good_feedback_claude(llm_config, f_log)
        f_log.close()
    # write the metrics file
    else:
        append_csv(metrics_file, metrics_field_names, {
            "file_name": class_name,
            "LLM": "claude-3.7",
            "time": get_current_time_str(),
            # "index": index,
            "trial": trial,
            "iteration": iteration,
            "passed": is_passed,
            "log_location": f_log_location,
            "output_location": 'NA',
            "llm_response_seconds": llm_response_time_delta,
            "validator_response_seconds": validator_response_time_delta,
        })
    return parsed_specified_code, err_info, is_passed
