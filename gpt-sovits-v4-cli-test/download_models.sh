#!/bin/bash

# GPT-SoVITS v4 Model Download Script
# RTX3050 + CUDA 12.4対応版

echo "=== GPT-SoVITS v4 Model Download Script ==="

# 作業ディレクトリに移動
cd /workspace/GPT-SoVITS/GPT_SoVITS/pretrained_models/

echo "Creating model directories..."
mkdir -p gsv-v4-pretrained
mkdir -p chinese-hubert-base
mkdir -p chinese-roberta-wwm-ext-large

echo "Downloading v4 models from HuggingFace..."

# v4用SoVITSモデル
echo "Downloading s2v4.ckpt..."
wget -O gsv-v4-pretrained/s2v4.ckpt \
    "https://huggingface.co/rvc-boss/GPT-SoVITS/resolve/main/gsv-v4-pretrained/s2v4.ckpt"

# v4用ボコーダー
echo "Downloading vocoder.pth..."
wget -O gsv-v4-pretrained/vocoder.pth \
    "https://huggingface.co/rvc-boss/GPT-SoVITS/resolve/main/gsv-v4-pretrained/vocoder.pth"

# HuBERTモデル（必須）
echo "Downloading chinese-hubert-base..."
wget -O chinese-hubert-base/pytorch_model.bin \
    "https://huggingface.co/rvc-boss/GPT-SoVITS/resolve/main/chinese-hubert-base/pytorch_model.bin"

wget -O chinese-hubert-base/config.json \
    "https://huggingface.co/rvc-boss/GPT-SoVITS/resolve/main/chinese-hubert-base/config.json"

wget -O chinese-hubert-base/preprocessor_config.json \
    "https://huggingface.co/rvc-boss/GPT-SoVITS/resolve/main/chinese-hubert-base/preprocessor_config.json"

# BERT-baseモデル（必須）
echo "Downloading chinese-roberta-wwm-ext-large..."
wget -O chinese-roberta-wwm-ext-large/pytorch_model.bin \
    "https://huggingface.co/rvc-boss/GPT-SoVITS/resolve/main/chinese-roberta-wwm-ext-large/pytorch_model.bin"

wget -O chinese-roberta-wwm-ext-large/config.json \
    "https://huggingface.co/rvc-boss/GPT-SoVITS/resolve/main/chinese-roberta-wwm-ext-large/config.json"

wget -O chinese-roberta-wwm-ext-large/tokenizer.json \
    "https://huggingface.co/rvc-boss/GPT-SoVITS/resolve/main/chinese-roberta-wwm-ext-large/tokenizer.json"

echo "=== Download completed! ==="
echo "Checking downloaded files..."

ls -la gsv-v4-pretrained/
ls -la chinese-hubert-base/
ls -la chinese-roberta-wwm-ext-large/

echo "=== Model files ready for v4 inference! ===" 