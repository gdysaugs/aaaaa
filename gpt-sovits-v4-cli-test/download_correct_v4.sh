#!/bin/bash

# GPT-SoVITS v4 Correct Model Download Script
# 公式GitHub Issue #2312に基づく正しいモデルファイル
# RTX3050 + CUDA 12.4対応版

echo "=== GPT-SoVITS v4 Correct Model Download ==="
echo "参照: https://github.com/RVC-Boss/GPT-SoVITS/issues/2312"
echo ""

# 作業ディレクトリに移動
cd /workspace/GPT-SoVITS/GPT_SoVITS/pretrained_models/

echo "Creating model directories..."
mkdir -p gsv-v4-pretrained

echo "=== 正しいGPT-SoVITS v4構成 ==="
echo ""
echo "✅ 必要なファイル:"
echo "1. s1v3.ckpt (GPTモデル) - 既にダウンロード済み ✅"
echo "2. s2Gv4.pth (SoVITSモデル) - これをダウンロード"
echo "3. vocoder.pth (ボコーダー) - 既にダウンロード済み ✅"
echo "4. HuBERT & RoBERTa - 既にダウンロード済み ✅"
echo ""
echo "❌ 不要なファイル:"
echo "- s2v4.ckpt - 存在しない・不要 (公式確認済み)"
echo ""

echo "=== s2Gv4.pthダウンロード中 ==="

# 正しいSoVITSモデルをダウンロード
echo "Downloading s2Gv4.pth (SoVITS v4 model)..."
curl -L -o gsv-v4-pretrained/s2Gv4.pth \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/gsv-v4-pretrained/s2Gv4.pth" \
    --connect-timeout 30 --max-time 600 || echo "❌ s2Gv4.pth download failed"

# 代替URL（もしメインが失敗した場合）
if [ ! -f "gsv-v4-pretrained/s2Gv4.pth" ] || [ ! -s "gsv-v4-pretrained/s2Gv4.pth" ]; then
    echo "Trying alternative URL for s2Gv4.pth..."
    curl -L -o gsv-v4-pretrained/s2Gv4.pth \
        "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/s2Gv4.pth" \
        --connect-timeout 30 --max-time 600 || echo "❌ s2Gv4.pth alternative download failed"
fi

# 結果確認
echo ""
echo "=== Download Results ==="
echo "Current model files:"
find . -name "*.ckpt" -o -name "*.pth" -o -name "*.bin" | xargs ls -lh 2>/dev/null || echo "No model files found"

echo ""
echo "=== GPT-SoVITS v4 Correct Model Status ==="
if [ -f "s1v3.ckpt" ] && [ -s "s1v3.ckpt" ]; then
    echo "✅ s1v3.ckpt (GPT): $(ls -lh s1v3.ckpt | awk '{print $5}')"
else
    echo "❌ s1v3.ckpt (GPT): Missing"
fi

if [ -f "gsv-v4-pretrained/s2Gv4.pth" ] && [ -s "gsv-v4-pretrained/s2Gv4.pth" ]; then
    echo "✅ s2Gv4.pth (SoVITS): $(ls -lh gsv-v4-pretrained/s2Gv4.pth | awk '{print $5}')"
else
    echo "❌ s2Gv4.pth (SoVITS): Missing or failed"
fi

if [ -f "gsv-v4-pretrained/vocoder.pth" ] && [ -s "gsv-v4-pretrained/vocoder.pth" ]; then
    echo "✅ vocoder.pth (Vocoder): $(ls -lh gsv-v4-pretrained/vocoder.pth | awk '{print $5}')"
else
    echo "❌ vocoder.pth (Vocoder): Missing"
fi

echo ""
echo "=== Manual Download (if needed) ==="
echo "If s2Gv4.pth download failed:"
echo "URL: https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/gsv-v4-pretrained/s2Gv4.pth"
echo "配置場所: pretrained_models/gsv-v4-pretrained/s2Gv4.pth"
echo ""
echo "参照: https://github.com/RVC-Boss/GPT-SoVITS/issues/2312" 