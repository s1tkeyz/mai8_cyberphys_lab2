#!/bin/bash

set -e

ollama serve &

until curl -s http://localhost:11434/ >/dev/null; do
    sleep 5
done

ollama pull qwen2.5:0.5b

exec uvicorn app.main:app --host 0.0.0.0 --port 8000