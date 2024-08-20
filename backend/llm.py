import os
from typing import Any, Dict, List, Callable
from openai import AzureOpenAI
import backend.config as cfg

def build_models():
    client = AzureOpenAI(
        api_key=cfg.AZURE_GPT_40_API_KEY,
        api_version=cfg.AZURE_GPT_40_API_VERSION,
        azure_endpoint=cfg.AZURE_GPT_40_API_END_POINT
    )
    return client

def get_completion(prompt, client_instance, model="gpt-4o", max_tokens=1000):
    messages = [{"role": "user", "content": prompt}]
    response = client_instance.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0,
    )
    return response

# Initialize the Azure OpenAI client
client_instance = build_models()

def add_cap_ref(
    prompt: str, prompt_suffix: str, cap_ref: str, cap_ref_content: str
) -> str:
    """
    Attaches a capitalized reference to the prompt.
    Example
        prompt = 'Refactor this code.'
        prompt_suffix = 'Make it more readable using this EXAMPLE.'
        cap_ref = 'EXAMPLE'
        cap_ref_content = 'def foo():\n    return True'
        returns 'Refactor this code. Make it more readable using this EXAMPLE.\n\nEXAMPLE\n\ndef foo():\n    return True'
    """
    new_prompt = f"""{prompt} {prompt_suffix}\n\n{cap_ref}\n\n{cap_ref_content}"""
    return new_prompt


def safe_get(data, dot_chained_keys):
    """
    {'a': {'b': [{'c': 1}]}}
    safe_get(data, 'a.b.0.c') -> 1
    """
    keys = dot_chained_keys.split(".")
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data
def response_parser(response: Dict[str, Any]):
    return safe_get(response, "choices.0.message.content")

def prompt(
    prompt: str,
    model: str = "gpt-4o",
    instructions: str = "You are a helpful assistant capable of generating both SQL and MongoDB queries.",
    max_tokens: int = 1000
) -> str:
    """
    Generate a response from a prompt using the Azure OpenAI API.
    """
    response = get_completion(prompt, client_instance, model=model, max_tokens=max_tokens)
    return response_parser(response.model_dump())

# def prompt(
#     prompt: str,
#     model: str = "gpt-4o",
#     instructions: str = "You are a helpful assistant.",
#     max_tokens: int = 1000
# ) -> str:
#     """
#     Generate a response from a prompt using the Azure OpenAI API.
#     """
#     response = get_completion(prompt, client_instance, model=model, max_tokens=max_tokens)
#     return response_parser(response.model_dump())