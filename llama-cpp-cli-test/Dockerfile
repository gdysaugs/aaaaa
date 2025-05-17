# syntax=docker/dockerfile:1.4

FROM nvidia/cuda:11.8.0-devel-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV CUDAToolkit_ROOT=/usr/local/cuda

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv \
    build-essential cmake git git-lfs ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# git-lfs初期化
RUN git lfs install

# CUDAスタブをlibcuda.so.1としてリンク
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/lib/x86_64-linux-gnu/libcuda.so.1

# llama-cpp-pythonインストール（GPU対応）
RUN pip install --upgrade pip
RUN pip install llama-cpp-python[server] --prefer-binary --extra-index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118

# 実行用イメージ
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3 python3-pip git git-lfs ca-certificates \
      libgomp1 libopenblas-dev wget curl python3-venv && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /workspace

# モデルはホストのmodels/を-vでマウント
VOLUME ["/models"]

CMD ["python3", "-m", "llama_cpp.cli", "--help"] 