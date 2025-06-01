import tiktoken


def count_str_token(string: str) -> int:
    """Returns the number of tokens in a text string."""
    model = "gpt-4o"
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def count_gpt_config_token(gpt_llm_config) -> int:
    sum = 0
    for message in gpt_llm_config["messages"]:
        sum += count_str_token(message["content"])
    return sum
