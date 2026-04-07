FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydantic \
    requests \
    openenv-core \
    streamlit \
    huggingface_hub \
    openai

EXPOSE 7860
EXPOSE 8501

CMD uvicorn server.app:app --host 0.0.0.0 --port 7860 & streamlit run app_ui.py --server.port 8501 --server.address 0.0.0.0