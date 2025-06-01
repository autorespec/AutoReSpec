# AutoReSpec Replication Package

## Install Dependencies

1. The python version used for the project is ```Python 3.12```. Use ```pyenv``` to handle multiple python versions.

2. To install the required python packages, openjml, and major use the ```install.sh``` script using the following command.

   ```shell
   ./install.sh
   ```

   if there is ```permission denied``` error, change the file permission and run again.

   ```shell
   chmod +x ./install.sh
   ```

3. AutoReSpec ues ```Ollama``` to call primary LLMs. To install ```Ollama``` by following their [website](https://ollama.com/download)

4. To run the motivating example, the primary model is ```llama3:8b``` to download the model, run the following command.

   ```shell
   ollama pull llama3:8b
   ```

5. For collaboration, the motivating example, uses ```GPT 4o```. Add the private key to the config.yaml file.

## Running the scripts

1. After installation, to run AutoReSpec activate the virtual environment using the following command

   ```shell
   . ./.autorespec/bin/activate
   ```

   To deactivate the virtual environment use the following command

   ```shell
   deactivate
   ```

2. To turn the motivating example, use the following command

   ```shell
   python main.py
   ```

   It will run all the motivating example from the ```motivatineExample``` directory. The validated outputs will be saved in the
   ```eval/out``` directory and the logs will be generated in the ```eval/logs``` directory. To extend the app and use with other models, please use the ```config.yaml``` file and download necessary models from ```Ollama```.
