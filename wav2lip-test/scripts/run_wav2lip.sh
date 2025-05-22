#!/bin/bash
set -e

# サンプル実行コマンド
# s3fd.pthの場所を指定
mkdir -p /workspace/Wav2Lip/face_detection/detection/sfd
cp /workspace/models/face_detection/detection/sfd/s3fd.pth /workspace/Wav2Lip/face_detection/detection/sfd/

# 一時ディレクトリの作成
mkdir -p /workspace/Wav2Lip/temp

# Wav2Lipディレクトリに移動して実行
cd /workspace/Wav2Lip

# GANモデルを使うとより高品質になる場合があります
# ダウンロード先: https://drive.google.com/drive/folders/153HLrqlBNxzZcHi17PEvP09kkAfzRshM
# 現在はwav2lip.pthを使用

# オプション解説:
# --pads: 上下左右のパディング - 口元の認識精度を調整
# --face_det_batch_size: 顔検出のバッチサイズ - 小さくすると精度向上する可能性あり
# --wav2lip_batch_size: 口元合成のバッチサイズ - GPUメモリに応じて調整

python3 inference.py \
  --checkpoint_path /workspace/models/wav2lip.pth \
  --face "/workspace/data/input/画面録画 2025-05-16 222902.mp4" \
  --audio /workspace/data/input/ohayougozaimasu_10.wav \
  --outfile /workspace/data/output/result_smooth.mp4 \
  --pads 0 10 0 0 \
  --face_det_batch_size 1 \
  --wav2lip_batch_size 4
