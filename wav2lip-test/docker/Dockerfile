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

# 依存パッケージ
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Wav2Lip本体
RUN git lfs install
RUN git clone https://github.com/Rudrabha/Wav2Lip.git
WORKDIR /workspace/Wav2Lip
RUN git lfs fetch --all
RUN git lfs checkout

# モデル格納用ディレクトリ
RUN mkdir -p /workspace/models

# s3fd.pth（face detectionモデル）DL
# RUN mkdir -p /workspace/Wav2Lip/face_detection/detection/sfd && \
#     wget -O /workspace/Wav2Lip/face_detection/detection/sfd/s3fd.pth https://huggingface.co/akhaliq/s3fd/resolve/main/s3fd.pth

# 作業ディレクトリ
WORKDIR /workspace

# エントリポイントは指定しない（手動実行用）

RUN mkdir -p /workspace/Wav2Lip/temp
