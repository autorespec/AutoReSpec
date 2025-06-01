import subprocess
import sys
import shutil

def check_ollama_and_models(required_models=None):
    if shutil.which("ollama") is None:
        sys.exit("Ollama is not installed or not found in PATH. Please install it from https://ollama.com before proceeding.")

    print("Ollama is installed.")

    try:
        result = subprocess.run(["ollama", "list"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        available_models_output = result.stdout.decode().strip().split("\n")[1:]  # Skip header
        available_model_names = {line.split()[0] for line in available_models_output}

        if required_models:
            installed = [model for model in required_models if model in available_model_names]
            missing = [model for model in required_models if model not in available_model_names]

            if installed:
                print(f"Installed models: {', '.join(installed)}")
            if missing:
                print(f"Missing models: {', '.join(missing)}")

            if not installed:
                sys.exit(
                    f"None of the required models are installed: {', '.join(required_models)}.\n"
                    f"Please run `ollama pull <model>` to install at least one."
                )
        else:
            print("No specific models required to check.")
    except Exception as e:
        sys.exit(f"Failed to check Ollama models: {e}")
