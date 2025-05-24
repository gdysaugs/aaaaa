#!/bin/bash

# GPT-SoVITS v4 API起動スクリプト
# RTX3050用に最適化

set -e

echo "=== Starting GPT-SoVITS v4 API Server ==="
echo "PyTorch Latest + CUDA 12.4 + RTX3050 Optimized"
echo ""

# GPU確認
python3 -c "import torch; print(f'GPU Status: {torch.cuda.is_available()}')"

# v4用設定ファイル作成
mkdir -p /workspace/GPT-SoVITS/GPT_SoVITS/configs

cat > /workspace/GPT-SoVITS/GPT_SoVITS/configs/tts_infer_v4.yaml << 'EOF'
custom:
  bert_base_path: GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large
  cnhuhbert_base_path: GPT_SoVITS/pretrained_models/chinese-hubert-base
  device: cuda
  is_half: true
  t2s_weights_path: GPT_SoVITS/pretrained_models/s1v3.ckpt
  version: v4
  vits_weights_path: GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2Gv4.pth
EOF

echo "v4 configuration file created!"

# APIサーバー起動
cd /workspace/GPT-SoVITS
python3 api_v2.py \
    -a 0.0.0.0 \
    -p 9880 \
    -c GPT_SoVITS/configs/tts_infer_v4.yaml 