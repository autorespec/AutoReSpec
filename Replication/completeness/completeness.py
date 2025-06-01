import os
import shutil
import subprocess
import time
from pathlib import Path
import pandas as pd
import re


def extract_class_name_from_code(code: str) -> str:
    # Remove multiline and single-line comments
    code_no_comments = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    code_no_comments = re.sub(r"//.*", "", code_no_comments)

    # Search for the actual class declaration
    match = re.search(
        r"\bpublic\s+(?:final\s+|abstract\s+)?class\s+(\w+)", code_no_comments
    )
    if match:
        return match.group(1) + ".java"
    raise ValueError("Could not find a public class in the provided Java code.")


def execute_command(command_list, timeout=200):
    try:
        result = subprocess.run(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        if result.returncode != 0:
            return result.stderr.decode() or result.stdout.decode()
        return result.stdout.decode()
    except subprocess.TimeoutExpired:
        return "Timeout"


def mutation_analysis(testcase_path, out_dir):
    base_dir = Path(__file__).resolve().parent

    executable_path = base_dir / ".." / "major" / "bin" / "major"
    major_config_path = base_dir / ".." / "config" / "major.mml.bin"

    assert (
        executable_path.exists()
    ), "Major executable not found at: {}. Please download Major v.3.0.1 and put into the mutators/ folder".format(
        executable_path
    )

    assert (
        major_config_path.exists()
    ), "MML file not found at: {}. Please re-download our package.".format(
        major_config_path
    )

    os.makedirs(out_dir, exist_ok=True)
    shutil.copy(testcase_path, out_dir)

    absolute_path = os.path.join(
        os.path.abspath(out_dir), os.path.basename(testcase_path)
    )

    current_dir = os.getcwd()
    os.chdir(out_dir)

    command = [
        str(executable_path),
        "--mml",
        str(major_config_path),
        str(absolute_path),
        "--export",
        "export.mutants",
    ]
    output = execute_command(command)
    print(output)
    os.chdir(current_dir)


def verify_mutants(mutants_dir):
    base_dir = Path(__file__).resolve().parent
    n_errors = 0
    validated_mutants = 0
    openjml_path = base_dir / ".." / "openjml" / "openjml"
    for root, dirs, files in os.walk(mutants_dir):
        for file in files:
            # mutants += 1
            mutant_location = os.path.abspath(os.path.join(root, file))
            print("evaluating ", mutant_location)
            cmd = [
                openjml_path,
                "--esc",
                "--esc-max-warnings=1",
                "--arithmetic-failure=quiet",
                "--nonnull-by-default",
                "--timeout=180",
                "--quiet",
                "-nowarn",
                mutant_location,
            ]
            try:
                result = subprocess.run(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=200
                )
                res = result.stdout.decode("utf-8")
                validated_mutants += 1
                if res and "validity is unknown" not in res.lower():
                    n_errors += 1
                    print(res)

            except subprocess.TimeoutExpired:
                print(f"Timeout on {mutant_location}")
                continue

    print("validated_mutants:", validated_mutants, "n_errors:", n_errors)
    return validated_mutants, n_errors


def evaluate_all_verified_specs(
    verified_dir="verified_specs", output_csv="completeness_summary.csv"
):

    if Path(output_csv).exists():
        done = set(pd.read_csv(output_csv)["file"].tolist())
        print(f"Resuming... {len(done)} files already processed.")
    else:
        done = set()

    for root, _, files in os.walk(verified_dir):
        for file in files:
            if file.endswith(".java"):
                java_path = Path(root) / file

                if str(java_path) in done:
                    print(f"Skipping (already processed): {java_path}")
                    continue

                print(f"\n>>> Evaluating: {java_path}")
                start_time = time.time()

                # Set up clean workspace
                base_current_dir = Path("tmp/completeness/current")
                base_done_dir = Path("tmp/completeness/done")
                out_dir = base_current_dir / "mutants"
                for p in [base_current_dir, base_done_dir, out_dir]:
                    p.mkdir(parents=True, exist_ok=True)
                for item in base_current_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)

                base_name = file.split("-")[0] + ".java"
                target_path = base_current_dir / base_name
                shutil.copy(java_path, target_path)

                validated_mutants = 0
                n_errors = 0
                try:
                    mutation_analysis(target_path, out_dir)
                    validated_mutants, n_errors = verify_mutants(out_dir / "mutants")
                    completeness = (
                        (n_errors / validated_mutants) * 100
                        if validated_mutants
                        else 0.0
                    )
                    elapsed = time.time() - start_time
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                    completeness = 0.0
                    mutants = n_errors = 0
                    elapsed = time.time() - start_time

                result = {
                    "file": str(java_path),
                    "validated_mutants": validated_mutants,
                    "errors": n_errors,
                    "completeness": completeness,
                    "elapsed_time_sec": elapsed,
                }
                print(f"Completeness Result: {result}")

                # Move output for archival
                trial_dir = base_done_dir / file
                if trial_dir.exists():
                    shutil.rmtree(trial_dir)
                shutil.move(str(base_current_dir), str(trial_dir))


def verify_generated_spec(verified_spec: str, class_name: str):

    print(f"\n>>> Evaluating: {class_name}.java")
    start_time = time.time()

    # Set up clean workspace
    base_current_dir = Path("tmp/completeness/current")
    base_done_dir = Path("tmp/completeness/done")
    out_dir = base_current_dir / "mutants"
    for p in [base_current_dir, base_done_dir, out_dir]:
        p.mkdir(parents=True, exist_ok=True)

    for item in base_current_dir.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

    # Write the code to {class_name}.java
    target_path = base_current_dir / f"{class_name}.java"
    with open(target_path, "w") as f:
        f.write(verified_spec)

    validated_mutants = 0
    n_errors = 0
    try:
        mutation_analysis(target_path, out_dir)
        validated_mutants, n_errors = verify_mutants(out_dir / "mutants")
        completeness = (
            (n_errors / validated_mutants) * 100 if validated_mutants else 0.0
        )
        elapsed = time.time() - start_time
    except Exception as e:
        print(f"Error processing {class_name}: {e}")
        completeness = 0.0
        validated_mutants = n_errors = 0
        elapsed = time.time() - start_time

    result = {
        "file": str(target_path),
        "validated_mutants": validated_mutants,
        "errors": n_errors,
        "completeness": completeness,
        "elapsed_time_sec": elapsed,
    }
    print(f"Completeness Result: {result}")

    # Archive the verified Java file into 'done/' folder
    try:
        shutil.copy(target_path, base_done_dir / class_name)
    except Exception as e:
        print(f"Archival failed: {e}")
