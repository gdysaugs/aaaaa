# GPT-SoVITS v4 CLI Test Docker Image
# Optimized for RTX 3050 with CUDA 12.4
FROM nvidia/cuda:12.4.0-devel-ubuntu22.04 as base

LABEL maintainer="GPT-SoVITS-v4-CLI"
LABEL version="v4.0"
LABEL description="GPT-SoVITS v4 CLI inference container optimized for RTX3050"

# 基本環境設定
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo
ENV PYTHONUNBUFFERED=1
ENV TOKENIZERS_PARALLELISM=false

# 基本パッケージとPython 3.10のインストール
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    git \
    git-lfs \
    ca-certificates \
    curl \
    wget \
    unzip \
    ffmpeg \
    libsox-dev \
    build-essential \
    cmake \
    libssl-dev \
    libffi-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    liblzma-dev \
    && rm -rf /var/lib/apt/lists/*

# Python3.10をデフォルトにする
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# pipをアップグレード
RUN python3 -m pip install --upgrade pip setuptools wheel

# 作業ディレクトリ設定
WORKDIR /workspace

# Git LFS初期化（確実に実行）
RUN git lfs install

# Git LFS対策付きクローンステージ
FROM base as clone_stage

# GPT-SoVITSリポジトリのクローン（Git LFS対策）
RUN echo "Cloning GPT-SoVITS repository..." && \
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git /workspace/GPT-SoVITS

WORKDIR /workspace/GPT-SoVITS

# Git LFS ファイルの取得（ステップごとに分離）
RUN echo "Fetching LFS files..." && \
    git lfs fetch --all && \
    git lfs checkout

# 依存関係ビルドステージ
FROM clone_stage as build_stage

# PyTorchとCUDA 12.4対応の依存関係をインストール
RUN pip install torch==2.4.0+cu121 torchvision==0.19.0+cu121 torchaudio==2.4.0+cu121 \
    --index-url https://download.pytorch.org/whl/cu121

# GPT-SoVITS依存関係をインストール
RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        echo "requirements.txt not found, installing core dependencies"; \
        pip install numpy scipy torch torchaudio transformers; \
    fi

# extra requirements もインストール
RUN if [ -f extra-req.txt ]; then \
        pip install --no-cache-dir --no-deps -r extra-req.txt; \
    else \
        echo "extra-req.txt not found, skipping"; \
    fi

# v4用の追加依存関係
RUN pip install \
    "fastapi[standard]>=0.115.2" \
    "ctranslate2>=4.0,<5" \
    "huggingface_hub>=0.13" \
    "tokenizers>=0.13,<1"

# 最終実行ステージ
FROM base as runtime

# ビルドステージから必要なファイルをコピー
COPY --from=build_stage /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=build_stage /usr/local/bin /usr/local/bin
COPY --from=build_stage /workspace/GPT-SoVITS /workspace/GPT-SoVITS

WORKDIR /workspace/GPT-SoVITS

# 環境変数設定（RTX3050最適化）
ENV CUDA_VISIBLE_DEVICES=0
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
ENV TOKENIZERS_PARALLELISM=false

# ポート設定
EXPOSE 9880 9871 9872 9873 9874

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python3 -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('Device Count:', torch.cuda.device_count())" || exit 1

# GPU情報確認用スクリプト
RUN echo '#!/bin/bash\necho "=== GPU Information ==="\nnvidia-smi\necho "=== PyTorch CUDA Check ==="\npython3 -c "import torch; print(f\"PyTorch Version: {torch.__version__}\"); print(f\"CUDA Available: {torch.cuda.is_available()}\"); print(f\"CUDA Version: {torch.version.cuda}\"); print(f\"Device Count: {torch.cuda.device_count()}\"); [print(f\"GPU {i}: {torch.cuda.get_device_name(i)}\") for i in range(torch.cuda.device_count())]"' > /workspace/check_gpu.sh && \
    chmod +x /workspace/check_gpu.sh

# エントリーポイント
CMD ["/bin/bash"] 