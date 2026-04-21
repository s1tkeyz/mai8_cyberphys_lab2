import json
import requests
from typing import Dict, Any

from src.models import *
from src.constants import *

def create_prompt(sms_text: str) -> str:
    """ Создание системного промпта """
    return (
        f"Ты — аналитик сотовой связи. Твоя задача - определить, является ли следующее SMS-сообщение спамом. "
        f"Отвечай только в виде JSON с двумя полями: "
        f"is_spam - является ли сообщение спамом (true/false) и "
        f"reason - кратое объяснение решения. "
        f"Текст SMS: \"{sms_text}\""
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
