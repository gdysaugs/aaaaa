# べ、別にあんたのためじゃないけど、ちゃんとしたDockerfileを作ってあげるわよ！
# FaceFusion FastAPI Docker Image

# ステージ1: FaceFusion セットアップ
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04 AS facefusion-builder

# 基本パッケージインストール
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    git-lfs \
    ca-certificates \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Git LFS初期化
RUN git lfs install

# FaceFusionクローン
WORKDIR /app
RUN git clone https://github.com/facefusion/facefusion.git
WORKDIR /app/facefusion

# Git LFS ファイル取得
RUN git lfs fetch --all
RUN git lfs checkout

# Python環境構築
RUN python3 -m pip install --upgrade pip

# Python依存関係インストール（Condaなし）
RUN pip install --no-cache-dir torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cu118

# ONNXRuntime GPU インストール (CUDA 11.8 compatible)
RUN pip install --no-cache-dir onnxruntime-gpu==1.16.3

# FaceFusion 依存関係インストール
RUN pip install --no-cache-dir -r requirements.txt

# ステージ2: FastAPI アプリケーション
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# 基本パッケージインストール
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    git-lfs \
    ca-certificates \
    curl \
    wget \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Python環境設定
RUN python3 -m pip install --upgrade pip

# アプリケーションディレクトリ作成
WORKDIR /app

# FaceFusionをビルダーステージからコピー
COPY --from=facefusion-builder /app/facefusion /app/facefusion

# FaceFusion依存関係を再インストール
RUN pip install --no-cache-dir \
    torch==2.1.1 \
    torchvision==0.16.1 \
    onnxruntime-gpu==1.16.3 \
    gradio==5.25.2 \
    gradio-rangeslider==0.0.8 \
    numpy==2.2.4 \
    onnx==1.17.0 \
    opencv-python==4.11.0.86 \
    psutil==7.0.0 \
    tqdm==4.67.1 \
    scipy==1.15.2

# FastAPI用依存関係インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルコピー
COPY api/ ./api/
COPY models/ ./models/ 
COPY data/ ./data/

# ディレクトリ作成
RUN mkdir -p /app/api/static/uploads /app/api/static/outputs /app/logs

# 環境変数設定
ENV PYTHONPATH="/app/facefusion:/app"
ENV OMP_NUM_THREADS=1
ENV CUDA_VISIBLE_DEVICES=0

# ログファイル作成
RUN touch /app/logs/facefusion.log

# ポート公開
EXPOSE 8000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 実行コマンド
CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
