import csv
import os
import re
import time

from config import config


def print_msg(message):
    print("{r}:{c}".format(r=message["role"], c=message["content"]))


def file2str(filename):
    res = ""
    with open(filename, "r") as f:
        for line in f.readlines():
            res = res + line
    return res


def config2str(config):
    res = ""
    for message in config["messages"]:
        res += "{role}: {content}\n".format(
            role=message["role"], content=message["content"]
        )
    return res


def print_config(config):
    print(config2str(config))


def parse_code_from_reply(content):
    extracted_str = content.split("```")[1]  # check it improves code parsing!
    extracted_str = (
        extracted_str
        if not extracted_str.startswith("java")
        else extracted_str[len("java") :]
    )
    return extracted_str.strip()


def parse_code_from_chatgpt_reply(content):
    content = "a" + content
    extracted_str = content.split("```")[1]
    extracted_str = (
        extracted_str
        if not extracted_str.startswith("java")
        else extracted_str[len("java") :]
    )
    return extracted_str.strip()


def parse_code_from_claude_reply(content):
    # Split by code block markers
    parts = content.split("```")

    # If there's an even number of parts, something is wrong
    if len(parts) < 3:
        raise ValueError("No complete code block found in the response")

    # Get the content of the first code block (should be at index 1)
    code_block = parts[1]

    # Remove language identifier if present
    if code_block.startswith("java"):
        code_block = code_block[len("java") :]
    elif any(
        code_block.startswith(lang) for lang in ["python", "javascript", "c++", "c#"]
    ):
        # Handle other common language identifiers
        code_block = code_block.split("\n", 1)[1] if "\n" in code_block else code_block

    return code_block.strip()


def check_file_read_access(file_path: str):
    if not os.access(file_path, os.R_OK):
        print("Cannot open input file {filename}".format(filename=file_path))
        exit(-1)


def save_file(content, file_dir, file_name):
    create_folder_if_not_exist(
        os.path.abspath(".") + "/{file_dir}".format(file_dir=file_dir)
    )
    tmp_filename = os.path.abspath(".") + "/{file_dir}/{file_name}.java".format(
        file_dir=file_dir, file_name=file_name
    )
    tmp_file = open(tmp_filename, "w")
    tmp_file.write(content)
    tmp_file.close()


def create_folder_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Folder '{path}' created.")
    else:
        print(f"Folder '{path}' already exists.")


def get_current_time_str():
    return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))


def create_csv(file_name, fieldnames):
    """Creates a CSV file with a fixed set of field names and write the headers"""
    with open(file_name, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def append_csv(file_name, fieldnames, file_dict):
    """Appends a row to the CSV file while maintaining a consistent column order."""
    with open(file_name, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(file_dict)
