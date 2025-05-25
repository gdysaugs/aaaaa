#!/bin/bash

# GPT-SoVITS v4 Model Download via Git LFS
# RTX3050 + CUDA 12.4対応版

echo "=== GPT-SoVITS v4 Git LFS Model Download ==="

# 作業ディレクトリに移動
cd /workspace/GPT-SoVITS/GPT_SoVITS/

# 事前学習済みモデルディレクトリを作成
mkdir -p pretrained_models
cd pretrained_models

echo "Initializing Git LFS..."
git lfs install

echo "Creating temporary directory for model downloads..."
mkdir -p temp_models

# XXXXRT/GPT-SoVITS-Pretrainedリポジトリからモデルをダウンロード
echo "Cloning pretrained models repository..."
cd temp_models
git clone https://huggingface.co/XXXXRT/GPT-SoVITS-Pretrained.git --depth 1

echo "Moving v4 models to pretrained_models directory..."
cd XXXXRT/GPT-SoVITS-Pretrained

# v4モデルファイルをチェック
if [ -f "s2G488k.pth" ]; then
    echo "Found s2G488k.pth (SoVITS model)"
    mv s2G488k.pth ../../../
fi

if [ -f "s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt" ]; then
    echo "Found s1bert25hz GPT model"
    mv s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt ../../../
fi

if [ -f "s2D488k.pth" ]; then
    echo "Found s2D488k.pth (SoVITS discriminator)"
    mv s2D488k.pth ../../../
fi

# v4用の代替的モデル配置
echo "Setting up v4 model structure..."
cd ../../..

# v4用ディレクトリ作成
mkdir -p gsv-v4-pretrained
mkdir -p chinese-hubert-base
mkdir -p chinese-roberta-wwm-ext-large

# 既存モデルをv4構造にコピー（互換性のため）
if [ -f "s2G488k.pth" ]; then
    echo "Copying models for v4 compatibility..."
    cp s2G488k.pth gsv-v4-pretrained/s2v4.ckpt
    echo "s2G488k.pth → gsv-v4-pretrained/s2v4.ckpt"
fi

# HuBERTとBERTモデルをダウンロード（小さなファイル）
echo "Downloading HuBERT model..."
cd chinese-hubert-base
wget -O config.json "https://huggingface.co/TencentGameMate/chinese-hubert-base/resolve/main/config.json"
wget -O preprocessor_config.json "https://huggingface.co/TencentGameMate/chinese-hubert-base/resolve/main/preprocessor_config.json"

echo "Downloading BERT model..."
cd ../chinese-roberta-wwm-ext-large
wget -O config.json "https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/resolve/main/config.json"
wget -O tokenizer.json "https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/resolve/main/tokenizer.json"

# 実際のモデルファイルサイズを確認
cd ../..
echo "=== Downloaded Model Files ==="
ls -la
ls -la gsv-v4-pretrained/
ls -la chinese-hubert-base/
ls -la chinese-roberta-wwm-ext-large/

# ゼロサイズファイルのクリーンアップ
echo "Cleaning up zero-size files..."
find . -name "*.bin" -size 0 -delete
find . -name "*.pth" -size 0 -delete
find . -name "*.ckpt" -size 0 -delete

# 一時ディレクトリクリーンアップ
rm -rf temp_models

echo "=== v4 Model setup completed! ==="
echo "Note: Large model files may need manual download due to LFS limitations"
echo "Available models:"
find . -name "*.pth" -o -name "*.ckpt" -o -name "*.bin" | head -10 