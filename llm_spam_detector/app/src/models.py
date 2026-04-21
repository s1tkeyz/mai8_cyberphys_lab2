from pydantic import BaseModel

class SpamFilterRequest(BaseModel):
    """Pydantic-модель запроса к сервису LLM"""
    sms_text: str

class SpamFilterResponse(BaseModel):
    """Pydantic-модель ответа сервиса LLM"""
    is_spam: bool
    reason: str
