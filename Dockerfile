# ベースイメージとしてCUDAランタイムを使用
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 AS build

# ビルドに必要なパッケージをインストール
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
    build-essential \
    cmake \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /app

# 基本的なパッケージをアップグレード
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

# 特定バージョンのPyTorchをインストール
RUN pip3 install --no-cache-dir torch==2.0.1 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118

# Coqui TTSとその依存関係をインストール
RUN pip3 install --no-cache-dir TTS==0.22.0

# 日本語処理用ライブラリ
RUN pip3 install --no-cache-dir cutlet fugashi[unidic-lite] pyopenjtalk-prebuilt

# 音声処理ライブラリ
RUN pip3 install --no-cache-dir pydub numpy scipy librosa==0.9.2 soundfile

# その他必要なライブラリ
RUN pip3 install --no-cache-dir einops transformers

# DirectTorchLoaderヘルパースクリプト作成
RUN echo '#!/usr/bin/env python3\n\
import sys\n\
import torch\n\
import os\n\
import importlib.util\n\
\n\
# weights_onlyパラメータの問題を回避するための環境変数設定\n\
os.environ["TORCH_LOAD_WEIGHTS_ONLY"] = "0"\n\
# または明示的にweights_onlyをFalseに設定する環境変数\n\
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"\n\
print(f"環境変数設定: TORCH_LOAD_WEIGHTS_ONLY=0, TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1")\n\
\n\
# XttsConfigが利用可能か確認\n\
xtts_config_spec = importlib.util.find_spec("TTS.tts.configs.xtts_config")\n\
if xtts_config_spec:\n\
    from TTS.tts.configs.xtts_config import XttsConfig\n\
    # XTTS設定クラスを安全なグローバルとして追加\n\
    if hasattr(torch.serialization, "add_safe_globals"):\n\
        torch.serialization.add_safe_globals([XttsConfig])\n\
        print("XttsConfigを安全なグローバル変数リストに追加しました")\n\
\n\
# XttsAudioConfigが利用可能か確認\n\
xtts_audio_config_spec = importlib.util.find_spec("TTS.tts.models.xtts")\n\
if xtts_audio_config_spec:\n\
    from TTS.tts.models.xtts import XttsAudioConfig\n\
    # XttsAudioConfigクラスを安全なグローバルとして追加\n\
    if hasattr(torch.serialization, "add_safe_globals"):\n\
        torch.serialization.add_safe_globals([XttsAudioConfig])\n\
        print("XttsAudioConfigを安全なグローバル変数リストに追加しました")\n\
\n\
# BaseDatasetConfigが利用可能か確認\n\
base_dataset_config_spec = importlib.util.find_spec("TTS.config.shared_configs")\n\
if base_dataset_config_spec:\n\
    from TTS.config.shared_configs import BaseDatasetConfig\n\
    # BaseDatasetConfigクラスを安全なグローバルとして追加\n\
    if hasattr(torch.serialization, "add_safe_globals"):\n\
        torch.serialization.add_safe_globals([BaseDatasetConfig])\n\
        print("BaseDatasetConfigを安全なグローバル変数リストに追加しました")\n\
\n\
# モデルをダウンロードして保存\n\
print("XTTS v2モデルを事前にダウンロードしています...")\n\
try:\n\
    # ModelManagerを使用してモデルをダウンロード\n\
    from TTS.utils.manage import ModelManager\n\
    model_path = ModelManager().download_model("tts_models/multilingual/multi-dataset/xtts_v2")\n\
    print(f"モデルが正常にダウンロードされました: {model_path}")\n\
except Exception as e:\n\
    print(f"モデルのダウンロード中にエラーが発生しました: {str(e)}")\n\
    print("エラーはDockerビルド時に無視され、実行時に再試行されます")\n\
    # ビルド時のエラーは無視してコンテナ実行時に再試行\n\
    sys.exit(0)\n\
' > /app/download_model.py && chmod +x /app/download_model.py

# モデルの事前ダウンロードを試行（失敗しても続行）
RUN python3 /app/download_model.py || true

# 最終イメージ
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 必要なランタイムパッケージをインストール
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libsndfile1 \
    ffmpeg \
    espeak-ng \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    sox \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# ビルドステージからPythonパッケージをコピー
COPY --from=build /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /root/.local/share/tts /root/.local/share/tts

# 作業ディレクトリの設定
WORKDIR /app

# 音声ファイル保存用のディレクトリ
RUN mkdir -p /app/output /app/samples

# エントリポイントスクリプト
COPY voice_clone.py /app/

# 環境変数の設定
ENV COQUI_TOS_AGREED=1
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:32
ENV TORCH_LOAD_WEIGHTS_ONLY=0
ENV TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1

# 実行コマンド
ENTRYPOINT ["python3", "/app/voice_clone.py"] 