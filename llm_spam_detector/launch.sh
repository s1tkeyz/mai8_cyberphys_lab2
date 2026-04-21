set -e

ollama serve &

sleep 10

ollama pull qwen2.5:0.5b

uvicorn app.main:app --host 0.0.0.0 --port 8000