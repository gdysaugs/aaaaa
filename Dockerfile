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

# Coqui TTSのインストール
RUN pip3 install --no-cache-dir torch==2.5.1 torchaudio==2.5.1
RUN pip3 install --no-cache-dir TTS
RUN pip3 install --no-cache-dir cutlet
RUN pip3 install --no-cache-dir fugashi[unidic-lite]
RUN pip3 install --no-cache-dir numpy scipy librosa soundfile
RUN pip3 install --no-cache-dir pydub numba onnxruntime sentencepiece protobuf

# 音声ファイル保存用のディレクトリ
RUN mkdir -p /app/output

# エントリポイントスクリプト
COPY voice_clone.py /app/

# 環境変数の設定
ENV COQUI_TOS_AGREED=1

# 実行コマンド
ENTRYPOINT ["python3", "/app/voice_clone.py"] 