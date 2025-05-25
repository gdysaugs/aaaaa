#!/bin/bash

# GPT-SoVITS v4 Official Model Download Script
# HuggingFace公式リポジトリからダウンロード
# RTX3050 + CUDA 12.4対応版

echo "=== GPT-SoVITS v4 Official Model Download ==="

# 作業ディレクトリに移動
cd /workspace/GPT-SoVITS/GPT_SoVITS/pretrained_models/

echo "Creating model directories..."
mkdir -p gsv-v4-pretrained
mkdir -p chinese-hubert-base
mkdir -p chinese-roberta-wwm-ext-large
mkdir -p gsv-v3-pretrained

echo "Installing git-lfs for large file handling..."
apt-get update && apt-get install -y git-lfs
git lfs install

echo "Downloading v4 models from official HuggingFace repository..."

# v4用モデル（lj1995/GPT-SoVITSから）
echo "Downloading v4 SoVITS model (s2v4.ckpt)..."
wget -O gsv-v4-pretrained/s2v4.ckpt \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2v4.ckpt" \
    --timeout=120 --tries=3

echo "Downloading v4 vocoder (vocoder.pth)..."
wget -O gsv-v4-pretrained/vocoder.pth \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/GPT_SoVITS/pretrained_models/gsv-v4-pretrained/vocoder.pth" \
    --timeout=120 --tries=3

# v3 GPTモデル（v4で使用）
echo "Downloading v3 GPT model for v4 (s1v3.ckpt)..."
wget -O s1v3.ckpt \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/GPT_SoVITS/pretrained_models/s1v3.ckpt" \
    --timeout=120 --tries=3

# HuBERTモデル
echo "Downloading Chinese HuBERT model..."
cd chinese-hubert-base
wget -O pytorch_model.bin \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/GPT_SoVITS/pretrained_models/chinese-hubert-base/pytorch_model.bin" \
    --timeout=120 --tries=3

wget -O config.json \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/GPT_SoVITS/pretrained_models/chinese-hubert-base/config.json" \
    --timeout=60 --tries=3

# BERT-largeモデル
echo "Downloading Chinese RoBERTa model..."
cd ../chinese-roberta-wwm-ext-large
wget -O pytorch_model.bin \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large/pytorch_model.bin" \
    --timeout=120 --tries=3

wget -O config.json \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large/config.json" \
    --timeout=60 --tries=3

# 結果確認
cd ..
echo "=== Download Results ==="
echo "v4 SoVITS model:"
ls -lh gsv-v4-pretrained/s2v4.ckpt 2>/dev/null || echo "❌ s2v4.ckpt failed"

echo "v4 Vocoder:"
ls -lh gsv-v4-pretrained/vocoder.pth 2>/dev/null || echo "❌ vocoder.pth failed"

echo "v3 GPT model:"
ls -lh s1v3.ckpt 2>/dev/null || echo "❌ s1v3.ckpt failed"

echo "HuBERT model:"
ls -lh chinese-hubert-base/pytorch_model.bin 2>/dev/null || echo "❌ HuBERT failed"

echo "BERT model:"
ls -lh chinese-roberta-wwm-ext-large/pytorch_model.bin 2>/dev/null || echo "❌ BERT failed"

# ゼロサイズファイルのクリーンアップ
echo "Cleaning up failed downloads..."
find . -name "*.ckpt" -size 0 -delete
find . -name "*.pth" -size 0 -delete
find . -name "*.bin" -size 0 -delete

echo "=== GPT-SoVITS v4 Official Download Completed! ==="
echo "Available model files:"
find . -name "*.ckpt" -o -name "*.pth" -o -name "*.bin" | xargs ls -lh 