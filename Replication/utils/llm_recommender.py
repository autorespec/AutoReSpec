import json
import os

import javalang
from javalang.tree import TernaryExpression, IfStatement


def classify_program_type(java_code: str, testcase_name: str = "") -> str:
    try:
        tree = javalang.parse.parse(java_code)
    except javalang.parser.JavaSyntaxError as e:
        return f"Parse Error: {e}"

    loops = []
    branches = []

    # Collect loops and branches (include ternaries as branches too)
    for path, node in tree:
        if isinstance(node, (javalang.tree.ForStatement, javalang.tree.WhileStatement, javalang.tree.DoStatement)):
            loops.append((path, node))
        elif isinstance(node, (javalang.tree.IfStatement, javalang.tree.SwitchStatement, TernaryExpression)):
            branches.append((path, node))

    if not loops and not branches:
        return "Sequential"

    if branches and not loops:
        return "Branched"

    for i, (path1, _) in enumerate(loops):
        for j, (path2, _) in enumerate(loops):
            if i != j and len(path2) > len(path1) and path2[:len(path1)] == path1:
                return "Nested Loop"

    for loop_path, _ in loops:
        branch_count = 0
        ternary_count = 0
        if_else_count = 0
        compound_condition_count = 0

        # Count if and if-else statements inside the loop
        for branch_path, branch_node in branches:
            if len(branch_path) > len(loop_path) and branch_path[:len(loop_path)] == loop_path:
                branch_count += 1
                if isinstance(branch_node, IfStatement) and getattr(branch_node, "else_statement", None):
                    branch_count += 1
                    if_else_count += 1

                condition = getattr(branch_node, "condition", None)
                if isinstance(condition, javalang.tree.BinaryOperation) and condition.operator in {"||", "&&"}:
                    branch_count += 1
                    compound_condition_count += 1
                    

        for path, node in tree:
            if isinstance(node, TernaryExpression):
                if len(path) > len(loop_path) and path[:len(loop_path)] == loop_path:
                    ternary_count += 1
                    branch_count += 1

        if branch_count >= 1:
            return "Multi-path Loop"



    return "Single-path Loop"


def analyze_java_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, "r") as f:
        code = f.read()

    program_type = classify_program_type(code)
    print(f"{os.path.basename(file_path)}: {program_type}")


def run_on_json(json_path: str, output_path: str = "classified_output.json"):
    with open(json_path, "r") as f:
        data = json.load(f)

    result = []
    for entry in data:
        name = entry["testcaseName"]
        code = entry["testcase"]
        program_type = classify_program_type(code)
        result.append({
            "testcaseName": name,
            "programType": program_type
        })

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Classification complete. Results saved to: {output_path}")




def recommend_LLMs(testcase):
    program_type = classify_program_type(testcase)
    if program_type == "Branched":
        return program_type, {
            "primaryLLM": {
                "model": "gemma3:27b",
                "shot_count": 2
            },
            "collaborativeLLM":{
            "model": "claude-3-7-sonnet-20250219",
            "shot_count": 4
        }}
    elif program_type == "Sequential":
        return program_type, {
            "primaryLLM": {
                "model": "gemma3:27b",
                "shot_count": 2
            },
            "collaborativeLLM":{
                "model": "gpt-4o",
                "shot_count": 2
            }}
    elif program_type == "Single-path Loop":
        return program_type, {
            "primaryLLM": {
                "model": "llama3:8b",
                "shot_count": 2
            },
            "collaborativeLLM":{
                "model": "gpt-4o",
                "shot_count": 4
            }}
    elif program_type == "Multi-path Loop":
        return program_type,{
            "primaryLLM": {
                "model": "llama3:8b",
                "shot_count": 2
            },
            "collaborativeLLM":{
                "model": "gpt-4o",
                "shot_count": 4
            }
        }
    elif program_type == "Nested Loop":
        return program_type, {
            "primaryLLM": {
                "model": "llama3:8b",
                "shot_count": 2
            },
            "collaborativeLLM":{
                "model": "claude-3-7-sonnet-20250219",
                "shot_count": 4
            }
        }
    return program_type,{
            "primaryLLM": {
                "model": "llama3:8b",
                "shot_count": 2
            },
            "collaborativeLLM":{
                "model": "gpt-4o",
                "shot_count": 4
            }
    }