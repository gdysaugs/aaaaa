FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    libsndfile1 \
    ffmpeg \
    espeak-ng \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    sox \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# 環境変数の設定
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV COQUI_TOS_AGREED=1

# PyTorchとCoqui TTSのインストール
RUN pip3 install --no-cache-dir torch==2.5.1 torchaudio==2.5.1
RUN pip3 install --no-cache-dir TTS
RUN pip3 install --no-cache-dir cutlet
RUN pip3 install --no-cache-dir fugashi[unidic-lite]
RUN pip3 install --no-cache-dir numpy scipy librosa soundfile
RUN pip3 install --no-cache-dir pydub numba onnxruntime sentencepiece protobuf

# FastAPIとUvicornインストール（APIサーバー用）
RUN pip3 install --no-cache-dir fastapi uvicorn python-multipart

# 音声ファイル保存用のディレクトリ
RUN mkdir -p /app/output
VOLUME ["/app/data"]

# ポート解放
EXPOSE 8002

# APIサーバーファイル
COPY ./coquitts/app.py /app/app.py

# サーバー起動コマンド
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"] 