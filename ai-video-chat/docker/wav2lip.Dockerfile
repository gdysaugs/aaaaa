# Stage 1: Build
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /workspace

# 基本ツール
RUN apt-get update && \
    apt-get install -y \
        python3.8 python3.8-dev python3.8-venv \
        python3-pip ffmpeg git git-lfs ca-certificates cmake build-essential \
        libglib2.0-0 libsm6 libxext6 libxrender-dev \
        libgtk2.0-dev libstdc++6 libopenblas-dev libatlas-base-dev liblapack-dev libjpeg-dev \
        wget && \
    rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

# CUDA対応PyTorch
RUN pip3 install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu118

# FastAPIとUvicorn
RUN pip3 install fastapi uvicorn python-multipart

# 依存パッケージ
COPY ./wav2lip/requirements.txt /workspace/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Wav2Lip本体
RUN git lfs install
RUN git clone https://github.com/Rudrabha/Wav2Lip.git
WORKDIR /workspace/Wav2Lip
RUN git lfs fetch --all
RUN git lfs checkout

# モデル格納用ディレクトリ
RUN mkdir -p /workspace/models

# 作業ディレクトリ
WORKDIR /workspace

# データディレクトリ
RUN mkdir -p /workspace/Wav2Lip/temp
VOLUME ["/workspace/data"]

# ポート公開
EXPOSE 8004

# APIサーバーファイルをコピー
COPY ./wav2lip/app.py /workspace/app.py

# サーバー起動
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8004"] 