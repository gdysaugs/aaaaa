# syntax=docker/dockerfile:1.4

FROM nvidia/cuda:11.8.0-devel-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_PATH=/usr/local/cuda
ENV CUDAToolkit_ROOT=/usr/local/cuda
ENV PATH=/usr/local/cuda/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip python3-dev python3-venv \
    build-essential cmake git git-lfs ca-certificates \
    libopenblas-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Git LFS初期化
RUN git lfs install

# CUDAスタブライブラリのリンク
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/lib/x86_64-linux-gnu/libcuda.so.1

# pipアップグレード
RUN pip3 install --upgrade pip setuptools wheel

# llama-cpp-pythonをGPU対応でビルド
ENV CMAKE_ARGS="-DGGML_CUDA=on"
ENV FORCE_CMAKE=1
RUN pip3 install llama-cpp-python[server] --no-cache-dir --verbose

# FastAPI関連パッケージをインストール
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt --no-cache-dir

# 実行用イメージ
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip git git-lfs ca-certificates \
    libgomp1 libopenblas-dev wget curl && \
    rm -rf /var/lib/apt/lists/*

# ビルダーからPythonパッケージをコピー
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /workspace

# アプリケーションファイルをコピー
COPY llama_api.py /workspace/
COPY chat_llama.py /workspace/
COPY cli_test.sh /workspace/
COPY llama_module.py /workspace/
COPY simple_api.py /workspace/

# 実行権限を付与
RUN chmod +x /workspace/cli_test.sh

# モデルディレクトリ
VOLUME ["/models"]

# ポート公開
EXPOSE 8000

# デフォルトコマンド（FastAPI サーバー）
CMD ["python3", "llama_api.py"]