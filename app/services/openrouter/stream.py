import os
import json
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

FREE_MODEL_CHAIN = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemma-3-27b-it:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
]


def stream_chat_completion(messages):
    print(f"--- STARTING STREAM ---")
    print(f"Key used: {OPENROUTER_API_KEY[:10]}...")  # Verify key is loaded

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://easycidr.cloud/",  # Hardcoded for testing
        "X-Title": "AIToolkit",
    }

    payload = {
        "model": FREE_MODEL_CHAIN[0],
        "messages": messages,
        "stream": True,
        "models": FREE_MODEL_CHAIN[1:],  # Fallback list [cite: 255]
    }

    try:
        # 1. Use a standard POST first to see if the connection is even possible
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30,
        )

        print(f"OpenRouter Status: {response.status_code}")
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            decoded_line = line.decode("utf-8")

            # If OpenRouter sends an error, it often comes as a raw JSON line
            if decoded_line.startswith("{"):
                error_data = json.loads(decoded_line)
                print(f"JSON error received: {error_data}")
                yield f"Error: {error_data.get('error', {}).get('message', 'Unknown')}"
                return

            if not decoded_line.startswith("data: "):
                continue

            data_str = decoded_line[6:]
            if data_str.strip() == "[DONE]":
                print("--- STREAM FINISHED ---")
                break

            try:
                data = json.loads(data_str)
                content = data["choices"][0]["delta"].get("content", "")
                if content:
                    print(f"Yielding: {content}")  # This MUST show in terminal
                    yield content
            except Exception as e:
                print(f"Parsing error: {e}")
                continue

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        yield f"Connection Error: {str(e)}"
