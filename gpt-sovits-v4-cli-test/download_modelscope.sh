#!/bin/bash

# GPT-SoVITS v4 Model Download from ModelScope
# RTX3050 + CUDA 12.4対応版

echo "=== GPT-SoVITS v4 ModelScope Download ==="

# 作業ディレクトリに移動
cd /workspace/GPT-SoVITS/GPT_SoVITS/pretrained_models/

echo "Creating model directories..."
mkdir -p gsv-v4-pretrained
mkdir -p chinese-hubert-base
mkdir -p chinese-roberta-wwm-ext-large

echo "Downloading from ModelScope (China mirror)..."

# v3 GPTモデル (v4で使用)
echo "Downloading s1v3.ckpt (GPT model for v4)..."
wget -O s1v3.ckpt \
    "https://www.modelscope.cn/models/XXXXRT/GPT-SoVITS-Pretrained/resolve/master/s1v3.ckpt" \
    --timeout=60 --tries=3

# v4 SoVITSモデル
echo "Downloading s2v4.ckpt (SoVITS v4 model)..."
wget -O gsv-v4-pretrained/s2v4.ckpt \
    "https://www.modelscope.cn/models/XXXXRT/GPT-SoVITS-Pretrained/resolve/master/gsv-v4-pretrained/s2v4.ckpt" \
    --timeout=60 --tries=3

# 代替: v3モデルをv4として使用
if [ ! -f "gsv-v4-pretrained/s2v4.ckpt" ]; then
    echo "Downloading s2Gv3.pth as fallback..."
    wget -O s2Gv3.pth \
        "https://www.modelscope.cn/models/XXXXRT/GPT-SoVITS-Pretrained/resolve/master/s2Gv3.pth" \
        --timeout=60 --tries=3
    
    if [ -f "s2Gv3.pth" ]; then
        cp s2Gv3.pth gsv-v4-pretrained/s2v4.ckpt
        echo "Using s2Gv3.pth as s2v4.ckpt"
    fi
fi

# HuBERTモデル（小さなファイル）
echo "Downloading HuBERT model files..."
cd chinese-hubert-base
wget -O config.json \
    "https://www.modelscope.cn/models/TencentGameMate/chinese-hubert-base/resolve/master/config.json" \
    --timeout=30 --tries=3

wget -O preprocessor_config.json \
    "https://www.modelscope.cn/models/TencentGameMate/chinese-hubert-base/resolve/master/preprocessor_config.json" \
    --timeout=30 --tries=3

# BERT-baseモデル（小さなファイル）
echo "Downloading BERT model files..."
cd ../chinese-roberta-wwm-ext-large
wget -O config.json \
    "https://www.modelscope.cn/models/hfl/chinese-roberta-wwm-ext-large/resolve/master/config.json" \
    --timeout=30 --tries=3

wget -O tokenizer.json \
    "https://www.modelscope.cn/models/hfl/chinese-roberta-wwm-ext-large/resolve/master/tokenizer.json" \
    --timeout=30 --tries=3

# ファイルサイズ確認
cd ..
echo "=== Downloaded Files Check ==="
echo "GPT Model (s1v3.ckpt):"
ls -lh s1v3.ckpt 2>/dev/null || echo "❌ s1v3.ckpt not found"

echo "SoVITS Model (s2v4.ckpt):"
ls -lh gsv-v4-pretrained/s2v4.ckpt 2>/dev/null || echo "❌ s2v4.ckpt not found"

echo "HuBERT config:"
ls -lh chinese-hubert-base/config.json 2>/dev/null || echo "❌ HuBERT config not found"

echo "BERT config:"
ls -lh chinese-roberta-wwm-ext-large/config.json 2>/dev/null || echo "❌ BERT config not found"

# ゼロサイズファイルのクリーンアップ
echo "Cleaning up zero-size files..."
find . -name "*.ckpt" -size 0 -delete
find . -name "*.pth" -size 0 -delete
find . -name "*.bin" -size 0 -delete

echo "=== ModelScope Download Completed! ===" 