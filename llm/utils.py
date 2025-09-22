import requests
from django.conf import settings
from server.responses import error_response, success_response
from rest_framework import status


def call_deepseek_chat(prompt: str, temperature: float = 0.7, max_tokens: int = 200):
    if not prompt:
        return error_response(
            message="Prompt required",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    api_key = getattr(settings, "DEEPSEEK_API_KEY", None)
    base_url = getattr(settings, "DEEPSEEK_BASE_URL", None)
    model = getattr(settings, "DEEPSEEK_MODEL", None)

    if not api_key or not base_url or not model:
        return error_response(
            message="DeepSeek configuration missing",
            details="Missing DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, or DEEPSEEK_MODEL",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

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

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content")
        )

        if not content:
            return error_response(
                message="Invalid response from DeepSeek",
                details=data,
                status_code=status.HTTP_502_BAD_GATEWAY
            )

        return success_response(
            data={"response": content},
            message="DeepSeek response generated",
            status_code=status.HTTP_200_OK
        )

    except requests.exceptions.RequestException as e:
        return error_response(
            message="Failed to connect to DeepSeek",
            details=str(e),
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    except Exception as e:
        return error_response(
            message="Unexpected error while calling DeepSeek",
            details=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
