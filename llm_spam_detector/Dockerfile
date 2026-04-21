FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    zstd \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY app /app

COPY launch.sh /launch.sh
RUN chmod +x /launch.sh

EXPOSE 11434 8000

ENTRYPOINT ["/launch.sh"]