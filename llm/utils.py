import requests
from django.conf import settings


def call_deepseek_chat(prompt: str, temperature: float = 0.7, max_tokens: int = 200):
    if not prompt:
        raise ValueError("Prompt required")

    api_key = getattr(settings, "DEEPSEEK_API_KEY", None)
    base_url = getattr(settings, "DEEPSEEK_BASE_URL", None)
    model = getattr(settings, "DEEPSEEK_MODEL", None)

    if not api_key or not base_url or not model:
        raise RuntimeError("DeepSeek configuration missing")

    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    content = (
        data.get("choices", [{}])[0]
        .get("message", {})
        .get("content")
    )

    if not content:
        raise RuntimeError("Invalid response from DeepSeek")

    return content  # just return raw text
