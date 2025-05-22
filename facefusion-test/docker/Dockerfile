# =========================
# Stage 1: Build & Download Models
# =========================
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --allow-change-held-packages --no-install-recommends \
        python3 python3-pip python3-dev git git-lfs ca-certificates wget \
        libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 ffmpeg curl \
        libcudnn8 libcudnn8-dev && \
    rm -rf /var/lib/apt/lists/*

# CUDAライブラリのパスを明示
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# Pythonパッケージ
RUN pip3 install --upgrade pip
RUN pip3 install numpy==1.26.4
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install onnxruntime-gpu==1.16.3 && pip3 uninstall -y onnxruntime

# FaceFusion本体をクローン
WORKDIR /app
RUN git clone https://github.com/facefusion/facefusion.git
WORKDIR /app/facefusion

# 必要なPython依存をインストール
RUN sed -i '/onnxruntime/d' requirements.txt && pip3 install -r requirements.txt

# onnxruntime-gpuだけをインストール
RUN pip3 install onnxruntime-gpu==1.16.3

# Git LFSモデルを確実に取得
RUN git lfs install && \
    git lfs fetch --all && \
    git lfs checkout

# =========================
# Stage 2: Runtime
# =========================
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

RUN apt-get update && \
    apt-get install -y --allow-change-held-packages --no-install-recommends \
        python3 python3-pip python3-dev git git-lfs ca-certificates wget \
        libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 ffmpeg curl \
        libcudnn8 libcudnn8-dev \
        libnvinfer8 libnvinfer-dev \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /app/facefusion /app/facefusion

WORKDIR /app/facefusion

# ポート公開（WebUI用）
EXPOSE 7860 7861

RUN pip3 install --force-reinstall --no-deps --no-cache-dir numpy==1.26.4

CMD ["python3", "facefusion.py"]
