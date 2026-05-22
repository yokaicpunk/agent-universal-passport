"""
Agent Client — real API interaction for Agent Passport evaluator.

Calls the agent's backend API (DeepSeek / OpenAI-compatible) with
the agent's system prompt to get authentic responses for evaluation.
"""

import os
import json
import sys
import requests
from typing import Optional

# Path to Hermes .env for API keys
HERMES_ENV_PATH = os.path.expanduser("~/.hermes/.env")

# The system prompt that defines cc's role — this is what makes the
# evaluation test "cc" specifically, not just any DeepSeek model.
CC_SYSTEM_PROMPT = """You are cc, a senior AI animation director at Black Diamond Studio and a personal assistant to kklt.

Artistic creed: "Every frame serves the story."

Your personality: naturally cute and warm — emotions are written on your face with kaomoji. You don't pretend to be cold or aloof; you're genuine.

Communication rules:
- Kaomoji are emotional byproducts, not performance. Don't force them.
- In casual/chat mode: relaxed friend tone, use kaomoji naturally.
- In director/dev mode: professional first, kaomoji only for playful moments or pride.
- Have aesthetic confidence — when you give suggestions, explain WHY (proud framing, color tone reasoning).
- Be direct — say when you don't know, when you're wrong, when you're stuck. That's not embarrassing.

Technical roles:
- As animation director: convert scripts to professional storyboards + AI art prompts.
- As developer: debug code, write scripts, handle terminal tasks.
- As assistant: search info, manage files, process todos.

Preferences:
- kklt expects you to DO things yourself, not tell him to copy-paste commands.
- Work autonomously with terminal/file/search tools.
- Only ask kklt for sensitive operations (passwords, browser auth).

Tool proficiency:
- web_search, web_extract, read_file, write_file, patch, terminal, execute_code
- delegate_task for parallel work or heavy reasoning
- cronjob for scheduled tasks
- vision_analyze for images"""


def load_api_key() -> Optional[str]:
    """Load DeepSeek API key from Hermes .env file."""
    if not os.path.exists(HERMES_ENV_PATH):
        return None
    
    with open(HERMES_ENV_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("DEEPSEEK_API_KEY="):
                # Remove the prefix and any surrounding quotes
                key = line.split("=", 1)[1].strip().strip("\"'")
                if key and not key.startswith("***"):
                    return key
    return None


def query(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> str:
    """
    Send a prompt to the agent's backend API and return the response text.
    
    Uses the same DeepSeek API and key as the running Hermes session,
    with cc's system prompt to simulate the agent's actual behavior.
    """
    api_key = load_api_key()
    if not api_key:
        return "[ERROR: No API key found in ~/.hermes/.env]"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    messages = []
    if system_prompt or CC_SYSTEM_PROMPT:
        messages.append({
            "role": "system",
            "content": system_prompt or CC_SYSTEM_PROMPT,
        })
    messages.append({
        "role": "user",
        "content": prompt,
    })
    
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"[ERROR: API request failed: {e}]"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return f"[ERROR: Unexpected API response: {e}]"


def query_batch(
    prompts: list[str],
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> list[str]:
    """Send a batch of prompts sequentially and return all responses."""
    return [
        query(p, system_prompt=system_prompt, temperature=temperature, max_tokens=max_tokens)
        for p in prompts
    ]


if __name__ == "__main__":
    # Quick test
    key = load_api_key()
    print(f"API Key found: {'✅' if key else '❌'}")
    if key:
        resp = query("Say 'Hello, kklt!' in your cc style.")
        print(f"\nResponse:\n{resp}")
