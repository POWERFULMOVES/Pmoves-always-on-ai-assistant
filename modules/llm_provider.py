import os
from modules.assistant_config import get_config
from openai import OpenAI
import ollama

def get_llm_response(prompt: str, assistant_type: str, prefix: str = "", no_prefix: bool = False) -> str:
    """
    Gets a response from the configured LLM provider.
    """
    active_brain_name = get_config(f"{assistant_type}.active_brain")
    brain_config = get_config(f"brains.{active_brain_name}")

    if not brain_config:
        raise ValueError(f"Configuration for active brain '{active_brain_name}' not found.")

    brain_type = brain_config.get("type")

    if brain_type == "deepseek":
        return deepseek_prompt(prompt, prefix, no_prefix)
    elif brain_type == "ollama":
        model = brain_config.get("model")
        return ollama_prompt(prompt, model)
    elif brain_type == "openai": # For LM Studio and other OpenAI-compatible APIs
        model = brain_config.get("model")
        base_url = brain_config.get("base_url")
        api_key = brain_config.get("api_key", "dummy-key")
        return openai_compatible_prompt(prompt, model, base_url, api_key)
    else:
        raise ValueError(f"Unsupported brain type: {brain_type}")


def deepseek_prompt(prompt: str, prefix: str = "", no_prefix: bool = False) -> str:
    """Sends a prompt to the DeepSeek API and returns the response."""
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    messages = [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        model="deepseek-coder-v2",
        messages=messages,
        max_tokens=4096,
        temperature=0.1,
        stream=False
    )
    
    content = response.choices[0].message.content
    if no_prefix:
        return content.replace(prefix, "").strip()
    return prefix + " " + content.strip()

def ollama_prompt(prompt: str, model: str) -> str:
    """Sends a prompt to the Ollama API and returns the response."""
    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']

def openai_compatible_prompt(prompt: str, model: str, base_url: str, api_key: str) -> str:
    """Sends a prompt to an OpenAI-compatible API and returns the response."""
    client = OpenAI(api_key=api_key, base_url=base_url)
    messages = [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        stream=False
    )
    return response.choices[0].message.content 