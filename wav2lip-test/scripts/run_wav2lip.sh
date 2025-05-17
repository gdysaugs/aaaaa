#!/bin/bash
set -e

# サンプル実行コマンド
python3 /workspace/Wav2Lip/inference.py \
  --checkpoint_path /workspace/models/wav2lip.pth \
  --face /workspace/data/input/sample.mp4 \
  --audio /workspace/data/input/sample.wav \
  --outfile /workspace/data/output/result.mp4
