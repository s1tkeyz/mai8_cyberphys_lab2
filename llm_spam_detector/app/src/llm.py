import json
import requests
from typing import Dict, Any

from app.src.models import *
from app.src.constants import *

def create_prompt(sms_text: str) -> str:
    """ Создание системного промпта """
    return (
        f"Классифицируй SMS-сообщение как 'спам'/'не спам'."
        f"Признаки спама: реклама, мошенничество, фишинг, запрос личных данных, подозрительные ссылки. "
        f"Определи, является ли следующее SMS-сообщение спамом: \"{sms_text}\". "
        f"Ответь исключительно в виде JSON с двумя полями: "
        f"'is_spam' (булево, true если спам, false если не спам) и 'reason' (краткое объяснение решения)"
    )

def call_llm(prompt: str) -> Dict[str, Any]:
    """ Обертка вызова модели Ollama """

    payload = {
        "model": OLLAMA_MODEL_NAME,
        "prompt": create_prompt(prompt),
        "stream": False,
        "format": "json"
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_RESPONSE_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }

def check_sms(sms_text: str) -> Dict[str, Any]:
    """ Проверка SMS на спам с помощью LLM """

    ollama_resp = call_llm(create_prompt(sms_text))

    if "error" in ollama_resp:
        return {"is_spam": None, "reason": f"Ошибка LLM: {ollama_resp['error']}"}

    try:
        result = json.loads(ollama_resp.get("response", "{}"))
        return {
            "is_spam": bool(result.get("is_spam", False)),
            "reason": str(result.get("reason", "Причина не указана"))
        }
    except json.JSONDecodeError:
        return {"is_spam": False, "reason": "Не удалось распарсить JSON-ответ модели"}
