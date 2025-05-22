FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg git git-lfs curl libsm6 libxext6 libgl1 libglib2.0-0 libxrender1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./backend /app/

# データディレクトリ
VOLUME ["/app/data"]

# ポート公開
EXPOSE 8000

# サーバー起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 