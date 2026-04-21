import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"

class GenerateRequest(BaseModel):
    prompt: str
    stream: bool = False

class GenerateResponse(BaseModel):
    response: str

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    payload = {
        "model": "qwen2.5:0.5b",
        "prompt": request.prompt,
        "stream": request.stream
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return GenerateResponse(response=data.get("response", ""))
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")