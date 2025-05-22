#!/bin/bash

# Coqui TTSでボイスクローンを実行するスクリプト
set -e

# 現在のディレクトリ
CURRENT_DIR=$(pwd)
echo "作業ディレクトリ: $CURRENT_DIR"

# 必要なディレクトリが存在するか確認
mkdir -p samples output

# 入力音声がない場合のメッセージ
if [ ! -f samples/voice.wav ]; then
  echo "警告: samples/voice.wavが見つかりません。"
  echo "クローンしたい声のサンプル音声(WAVファイル)を samples/voice.wav として保存してください。"
  echo "音声は10〜30秒程度、クリアで背景ノイズの少ない発話のものが理想的です。"
  echo "サンプリングレート44.1kHzか48kHz、16bit、モノラルのWAVファイルを推奨します。"
  exit 1
fi

# ヘルプメッセージ
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
  echo "使用方法: $0 [テキスト] [ノイズ除去強度] [長さペナルティ]"
  echo "  テキスト: 合成するテキスト (デフォルト: 'これはテストです。ボイスクローンのサンプルです。')"
  echo "  ノイズ除去強度: 0.0-1.0の値 (デフォルト: 0.005, 大きいほど強い)"
  echo "  長さペナルティ: 通常は0.5-2.0の値 (デフォルト: 1.0, 大きいほど長く発話)"
  echo ""
  echo "このスクリプトはCoqui TTS (XTTS v2)モデルを使用し、日本語専用に最適化されています。"
  echo "入力音声のノイズを除去する強度と、生成される音声の長さを調整することができます。"
  echo ""
  echo "例:"
  echo "  $0 'こんにちは、これはテストです。' 0.01 1.2"
  echo "  $0 '山田さんは明日東京に行きます。' 0.005 1.0"
  exit 0
fi

# パラメータの設定
TEXT="${1:-これはテストです。ボイスクローンのサンプルです。}"
DENOISE_STRENGTH="${2:-0.005}"
LENGTH_PENALTY="${3:-1.0}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILENAME="voice_clone_ja_${TIMESTAMP}.wav"

echo "====================================="
echo "🎙️ Coqui TTS 日本語ボイスクローン (XTTS v2)"
echo "====================================="
echo "入力テキスト: $TEXT"
echo "ノイズ除去強度: $DENOISE_STRENGTH"
echo "長さペナルティ: $LENGTH_PENALTY"
echo "出力ファイル: output/$OUTPUT_FILENAME"
echo "====================================="

# Dockerイメージをビルド
echo "🔧 Dockerイメージをビルドしています..."
DOCKER_BUILDKIT=1 docker build -t tts-voice-clone .

# コンテナを実行
echo "🚀 ボイスクローンを実行しています..."
docker run --rm --gpus all \
  -v "$CURRENT_DIR/samples:/app/samples" \
  -v "$CURRENT_DIR/output:/app/output" \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  tts-voice-clone \
  --text "$TEXT" \
  --speaker_wav /app/samples/voice.wav \
  --output "/app/output/$OUTPUT_FILENAME" \
  --denoise_strength "$DENOISE_STRENGTH" \
  --length_penalty "$LENGTH_PENALTY"

# 完了メッセージ
echo "✅ 処理が完了しました！"
echo "出力ファイル: $CURRENT_DIR/output/$OUTPUT_FILENAME" 