ARG CUDA_VERSION=11.8.0
ARG UBUNTU_VERSION=22.04
ARG PYTHON_VERSION=3.10

# Stage 1: Clone repository and download LFS files
FROM ubuntu:${UBUNTU_VERSION} AS git-clone-stage

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    git-lfs \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN git lfs install --system

WORKDIR /app
RUN git clone https://github.com/RVC-Boss/GPT-SoVITS.git .
# If the repository uses submodules, uncomment the following line
# RUN git submodule update --init --recursive

# Fetch LFS objects. If specific paths are problematic, fetch them individually.
RUN git lfs fetch --all
RUN git lfs checkout

# Stage 2: Build stage with CUDA
FROM nvidia/cuda:${CUDA_VERSION}-cudnn8-devel-ubuntu${UBUNTU_VERSION} AS build-stage

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo
ARG PYTHON_VERSION=3.10

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    curl \
    ffmpeg \
    libsndfile1 \
    git \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.10 /usr/bin/python

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

WORKDIR /app
COPY --from=git-clone-stage /app /app

# Install Python dependencies
# Some packages might need specific versions or pre-installation of other system libraries
# First, try installing common problematic packages or those requiring compilation
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install --no-cache-dir huggingface-hub
RUN pip install --no-cache-dir -r requirements.txt

# Download pre-trained models for v4 and other dependencies
WORKDIR /app
# Download chinese-roberta-wwm-ext-large (for bert_path)
RUN python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('hfl/chinese-roberta-wwm-ext-large', resume_download=True).save_pretrained('GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large')"

# Download chinese-hubert-base (for SSL model)
RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('TencentGameMate/chinese-hubert-base', resume_download=True).save_pretrained('GPT_SoVITS/pretrained_models/chinese-hubert-base')"

# Create directory for model downloads
RUN mkdir -p GPT_SoVITS/pretrained_models/gsv-v4-pretrained

# Download v4 pre-trained models from the official repo
WORKDIR /app/GPT_SoVITS/pretrained_models/gsv-v4-pretrained
# Download GPT-SoVITS v4 models
RUN curl -L -o s2v4.ckpt https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/s2v4.ckpt && \
    curl -L -o vocoder.pth https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/vocoder.pth

# Return to app directory
WORKDIR /app

# Set environment variables for CLI
ENV PYTHONPATH=/app:$PYTHONPATH
ENV GPT_PATH=/app/GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2v4.ckpt
ENV SOVITS_PATH=/app/GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2v4.ckpt
ENV BERT_PATH=/app/GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large
ENV SSL_MODEL_PATH=/app/GPT_SoVITS/pretrained_models/chinese-hubert-base

# Default command (can be overridden in docker-compose.yaml or docker run)
# For now, let's make it a simple shell, as CLI usage needs further investigation
CMD ["bash"] 