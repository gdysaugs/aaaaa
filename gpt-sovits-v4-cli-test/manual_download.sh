#!/bin/bash

# GPT-SoVITS v4 Manual Model Download Script
# 手動で正しいURLからモデルファイルをダウンロード
# RTX3050 + CUDA 12.4対応版

echo "=== GPT-SoVITS v4 Manual Model Download ==="

# 作業ディレクトリに移動
cd /workspace/GPT-SoVITS/GPT_SoVITS/pretrained_models/

echo "Creating model directories..."
mkdir -p gsv-v4-pretrained
mkdir -p chinese-hubert-base
mkdir -p chinese-roberta-wwm-ext-large

echo "=== Manual Download Guide ==="
echo ""
echo "ダウンロードが失敗した場合、以下のURLから手動でダウンロードしてください："
echo ""

echo "1. GPT v3モデル (s1v3.ckpt - 約1.2GB):"
echo "   URL: https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/s1v3.ckpt"
echo "   配置場所: pretrained_models/s1v3.ckpt"
echo ""

echo "2. SoVITS v4モデル (s2v4.ckpt - 約300MB):"
echo "   URL: https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/gsv-v4-pretrained/s2v4.ckpt"
echo "   配置場所: pretrained_models/gsv-v4-pretrained/s2v4.ckpt"
echo ""

echo "3. v4ボコーダー (vocoder.pth - 約50MB):"
echo "   URL: https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/gsv-v4-pretrained/vocoder.pth"
echo "   配置場所: pretrained_models/gsv-v4-pretrained/vocoder.pth"
echo ""

echo "4. HuBERTモデル (pytorch_model.bin - 約380MB):"
echo "   URL: https://huggingface.co/TencentGameMate/chinese-hubert-base/resolve/main/pytorch_model.bin"
echo "   配置場所: pretrained_models/chinese-hubert-base/pytorch_model.bin"
echo ""

echo "5. RoBERTaモデル (pytorch_model.bin - 約1.3GB):"
echo "   URL: https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/resolve/main/pytorch_model.bin"
echo "   配置場所: pretrained_models/chinese-roberta-wwm-ext-large/pytorch_model.bin"
echo ""

echo "=== 自動ダウンロードを試行中 ==="

# 最新の正しいURLで再試行
echo "Downloading GPT v3 model (s1v3.ckpt)..."
curl -L -o s1v3.ckpt \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/s1v3.ckpt" \
    --connect-timeout 30 --max-time 600 || echo "❌ s1v3.ckpt download failed"

echo "Downloading SoVITS v4 model (s2v4.ckpt)..."
curl -L -o gsv-v4-pretrained/s2v4.ckpt \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/gsv-v4-pretrained/s2v4.ckpt" \
    --connect-timeout 30 --max-time 600 || echo "❌ s2v4.ckpt download failed"

echo "Downloading v4 vocoder (vocoder.pth)..."
curl -L -o gsv-v4-pretrained/vocoder.pth \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/gsv-v4-pretrained/vocoder.pth" \
    --connect-timeout 30 --max-time 300 || echo "❌ vocoder.pth download failed"

echo "Downloading HuBERT model..."
curl -L -o chinese-hubert-base/pytorch_model.bin \
    "https://huggingface.co/TencentGameMate/chinese-hubert-base/resolve/main/pytorch_model.bin" \
    --connect-timeout 30 --max-time 600 || echo "❌ HuBERT download failed"

echo "Downloading RoBERTa model..."
curl -L -o chinese-roberta-wwm-ext-large/pytorch_model.bin \
    "https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/resolve/main/pytorch_model.bin" \
    --connect-timeout 30 --max-time 600 || echo "❌ RoBERTa download failed"

# 設定ファイルもダウンロード
echo "Downloading config files..."
curl -L -o chinese-hubert-base/config.json \
    "https://huggingface.co/TencentGameMate/chinese-hubert-base/resolve/main/config.json" || echo "❌ HuBERT config failed"

curl -L -o chinese-roberta-wwm-ext-large/config.json \
    "https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/resolve/main/config.json" || echo "❌ RoBERTa config failed"

# 結果確認
echo ""
echo "=== Download Results ==="
find . -name "*.ckpt" -o -name "*.pth" -o -name "*.bin" | xargs ls -lh 2>/dev/null || echo "No model files found"

echo ""
echo "=== Manual Download Completed! ==="
echo ""
echo "❗ 重要: ファイルサイズが0Bまたは非常に小さい場合は、手動でダウンロードしてください！"
echo "📥 ブラウザで上記URLにアクセスして直接ダウンロードできます。"
echo "📁 ダウンロード後、正しいフォルダに配置してください。" 