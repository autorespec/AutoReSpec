# AutoReSpec Webserver

## Install Dependencies

1. The ```node``` version used for the project is ```v22.13.1```. Download node from [nodejs](https://nodejs.org/en/download)

2. To install the required openjml, and major use the ```install.sh``` script using the following command.

   ```shell
   ./install.sh
   ```

   if there is ```permission denied``` error, change the file permission and run again.

   ```shell
   chmod +x ./install.sh
   ```

3. To install required node packages, use the following command

   ```shell
   npm install
   ```

4. AutoReSpec ues ```Ollama``` to call primary LLMs. To install ```Ollama``` by following their [website](https://ollama.com/download)

5. To run closed-source models update the ```.env``` file with your private api keys

## Running the scripts

1. To run the webserver use the following command

   ```shell
   npm run dev
   ```

   The webserver will start running at ```localhost:3000```

2. To check the program type, request the webserver using the following ```curl``` command

   ```shell
   curl --location 'http://localhost:3000/api/autorespec/recommend' \
   --header 'Content-Type: application/json' \
   --data '{
   "testcase": "public class TokenTest02 {\n  public static boolean f(String sentence) {\n    String[] tokens = sentence.split(\" \");\n\n    int i = 0;\n    for (String token : tokens) {\n      if (i == 3)\n        if (!token.equals(\"genneration\"))\n          return false;\n      ++i;\n    }\n    return true;\n  }\n}"
   }'
   ```

   Sample response:

   ```shell
   {
      "programType":"Multi-path Loop",
      "primaryLLM":{
         "model":"llama3:8b",
         "shot_count":2
         },
         "collaborativeLLM":{
            "model":"gpt-4o",
            "shot_count":4
            }
      }
   ```

3. To generate specification, request the webserver using the following ```curl``` command

   ```shell
   curl --location 'http://localhost:3000/api/autorespec/generate-spec' \
   --header 'Content-Type: application/json' \
   --data '{
      "model": "llama3:8b",
      "shotCount": 2,
      "iteration": 5,
      "collaboratorModel": "gpt-4o",
      "collaborativeShotCount": 4,
      "collaboratorIteration": 5,
      "testcase": "public class TokenTest02 {\n  public static boolean f(String sentence) {\n    String[] tokens = sentence.split(\" \");\n\n    int i = 0;\n    for (String token : tokens) {\n      if (i == 3)\n        if (!token.equals(\"genneration\"))\n          return false;\n      ++i;\n    }\n    return true;\n  }\n}"
   }'
   ```

4. To measure completeness, request the webserver using the following ```curl``` command

   ```shell
   curl --location 'http://localhost:3000/api/autorespec/measure-completeness' \
   --header 'Content-Type: application/json' \
   --data-raw '{
      "testcase":  "public class Abs {\n\t\n\t//@ ensures \\result >= 0;\n\tpublic int Abs(int num) {\n\t\tif (num < 0)\n\t\t\treturn -num;\n\t\telse\n\t\t\treturn num;\n\t}\n\n}"
   }'
   ```

   Sample response:

   ```shell
   {
      "mutantCount": 5,
      "errorCount": 3,
      "completeness": "0.60",
      "mutantDir": "AutoReSpec/Webserver/completenessAnalysis/Abs-1748769508048/mutants"
   }
   ```
