import signal
import time

import anthropic
from ollama import chat, ChatResponse
from openai import RateLimitError, APIConnectionError, OpenAIError, OpenAI

from config import config

client = None
anthropic_client = None

def get_openai_client():
    global client
    if client is None:
        client = OpenAI(api_key=config.get("openai_api_key"))
    return client

def get_anthropic_client():
    global anthropic_client
    if anthropic_client is None:
        anthropic_client = anthropic.Anthropic(api_key=config.get("anthropic_api_key"))
    return anthropic_client



def create_llm_config(model_name, messages):
    llm_config = {
        "model": model_name,
        "stream": False,
        "options": {
            "temperature":0.4
        },
        "messages": messages,
    }
    return llm_config


def create_chatgpt_config(messages):
    # TODO: change from config.yaml
    chatgpt_config = {
        "model": "gpt-4o",
        "temperature": 0.4,
        "messages": messages
    }
    return chatgpt_config


def create_claude_config(messages):

    claude_config = {
        "model": "claude-3-7-sonnet-20250219",
        "system": config.get("system_message"),
        "temperature": 0.4,
        "messages": messages,
        "max_tokens": 4000
    }
    return claude_config


def create_collaborative_llm_config(messages):
    collaborator_llm_config = {
        "model": config.get("collaborator_model"),
        "stream": False,
        "options": config.get("collaborator_llm_options", {}),
        "messages": messages,
    }
    return collaborator_llm_config


def create_collaborative_gpt_llm_config(messages):
    # TODO: change from config.yaml
    collaborator_llm_config = {
        "model":"gpt-4o", # change later
        "temperature":0.4,
        "messages": messages,
    }
    # print(collaborator_llm_config)
    return collaborator_llm_config


def truncate_claude_messages_heuristic(messages, max_messages=3):
    filtered_messages = [msg for msg in messages if msg.get("role") != "system"]
    if len(filtered_messages) > max_messages:
        filtered_messages = filtered_messages[-max_messages:]
    return filtered_messages

def truncate_messages_heuristic(messages, max_messages=3):
    return messages[-max_messages:]

# need to handle tokens
def create_collaborative_claude_llm_config(messages):
    # TODO: change from config.yaml
    collaborator_claude_config = {
        "model": "claude-3-7-sonnet-20250219",
        "temperature":0.4,
        "system": config.get("collaborator_system_message"),
        "messages":truncate_claude_messages_heuristic(messages),
        "max_tokens": 8000
    }
    print("collaborator_claude_config", collaborator_claude_config)
    return collaborator_claude_config


def request_llm_engine(llm_config, max_retries: int = 5, delay: float = 2):
    llm_config["messages"] = truncate_messages_heuristic(llm_config["messages"])
    for attempt in range(max_retries):
        try:
            ret: ChatResponse = chat(**llm_config)
            return ret
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay * (2 ** attempt))
    print("Max retries reached. Failed to get a response.")
    return None # handle error here


def handler(signum, frame):
    raise Exception("end of time")


def request_chatgpt_engine(gpt_config, max_retries=5):
    ret = None
    attempts = 0  # Track retry attempts
    openai_client = get_openai_client()

    while ret is None and attempts < max_retries:
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(100)  # Set timeout for 100 seconds

            ret = openai_client.chat.completions.create(**gpt_config)
            signal.alarm(0)  # Cancel alarm if successful

        except RateLimitError as e:
            print(f"Rate limit exceeded. Retrying in {2 ** attempts} seconds...")
            print(e)
            signal.alarm(0)
            time.sleep(2 ** attempts)  # Exponential backoff (1s, 2s, 4s, 8s, 16s)
            attempts += 1

        except APIConnectionError as e:
            print(f"API connection error. Retrying in {2 ** attempts} seconds...")
            print(e)
            signal.alarm(0)
            time.sleep(2 ** attempts)  # Exponential backoff
            attempts += 1

        except OpenAIError as e:  # Catch any OpenAI-specific errors
            print(f"OpenAI API error: {e}. Retrying in {2 ** attempts} seconds...")
            signal.alarm(0)
            time.sleep(2 ** attempts)  # Exponential backoff
            attempts += 1

        except TimeoutError as e:
            print(f"Timeout error: {e}. Retrying in {2 ** attempts} seconds...")
            signal.alarm(0)
            time.sleep(2 ** attempts)  # Exponential backoff
            attempts += 1

        except Exception as e:
            print(f"Unknown error: {e}. Retrying in {2 ** attempts} seconds...")
            signal.alarm(0)
            time.sleep(2 ** attempts)  # Exponential backoff
            attempts += 1

    if ret is None:
        print("Max retries reached. Failed to get a response from OpenAI.")

    return ret


def request_claude_engine(claude_config, max_retries=5):
    ret = None
    attempts = 0  # Track retry attempts
    client = get_anthropic_client()
    claude_config["messages"] = truncate_claude_messages_heuristic(claude_config["messages"])
    while ret is None and attempts < max_retries:
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(100)  # Set timeout for 100 seconds
            ret = client.messages.create(**claude_config)
            signal.alarm(0)  # Cancel alarm if successful

        except anthropic.RateLimitError as e:
            print(f"Rate limit exceeded. Retrying in {2 ** attempts} seconds...")
            print(e)
            signal.alarm(0)
            time.sleep(2 ** attempts)  # Exponential backoff (1s, 2s, 4s, 8s, 16s)
            attempts += 1

        except anthropic.APIConnectionError as e:
            print(f"API connection error. Retrying in {2 ** attempts} seconds...")
            print(e)
            signal.alarm(0)
            time.sleep(2 ** attempts)  # Exponential backoff
            attempts += 1


        except anthropic.APIError as e:  # Catch any Anthropic-specific errors
            print(f"Anthropic API error: {e}. Retrying in {2 ** attempts} seconds...")
            signal.alarm(0)
            time.sleep(2 ** attempts)  # Exponential backoff
            attempts += 1


        except TimeoutError as e:
            print(f"Timeout error: {e}. Retrying in {2 ** attempts} seconds...")
            signal.alarm(0)
            time.sleep(2 ** attempts)  # Exponential backoff
            attempts += 1


        except Exception as e:
            print(f"Unknown error: {e}. Retrying in {2 ** attempts} seconds...")
            signal.alarm(0)
            time.sleep(2 ** attempts)  # Exponential backoff
            attempts += 1

    if ret is None:
        print("Max retries reached. Failed to get a response from OpenAI.")

    return ret
