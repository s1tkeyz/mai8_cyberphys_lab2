from fastapi import FastAPI

from app.src.constants import *
from app.src.models import *
from app.src.llm import check_sms


app = FastAPI()


@app.post("/predict", response_model=SpamFilterResponse)
async def call_ollama_llm(request: SpamFilterRequest):
    """Ручка вызова LLM для проверки SMS на спам"""
    response = check_sms(request.sms_text)
    return SpamFilterResponse(is_spam=response["is_spam"], reason=response["reason"])
