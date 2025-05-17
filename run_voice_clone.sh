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
  echo "音声は5〜30秒程度、クリアな発話のものが良いでしょう。"
  exit 1
fi

# ヘルプメッセージ
if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
  echo "使用方法: $0 [テキスト] [言語]"
  echo "  テキスト: 合成するテキスト (デフォルト: 'これはテストです。ボイスクローンのサンプルです。')"
  echo "  言語: 言語コード (デフォルト: 'ja', 他: 'en', 'zh', etc.)"
  echo ""
  echo "例:"
  echo "  $0 'こんにちは、これはテストです。' ja"
  echo "  $0 'Hello, this is a test.' en"
  exit 0
fi

# パラメータの設定
TEXT="${1:-これはテストです。ボイスクローンのサンプルです。}"
LANGUAGE="${2:-ja}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILENAME="voice_clone_${LANGUAGE}_${TIMESTAMP}.wav"

echo "====================================="
echo "🎙️ Coqui TTS ボイスクローン"
echo "====================================="
echo "入力テキスト: $TEXT"
echo "使用言語: $LANGUAGE"
echo "出力ファイル: output/$OUTPUT_FILENAME"
echo "====================================="

# Dockerイメージをビルド
echo "🔧 Dockerイメージをビルドしています..."
docker build -t tts-voice-clone .

# コンテナを実行
echo "🚀 ボイスクローンを実行しています..."
docker run --rm --gpus all \
  -v "$CURRENT_DIR/samples:/app/samples" \
  -v "$CURRENT_DIR/output:/app/output" \
  tts-voice-clone \
  --text "$TEXT" \
  --speaker_wav /app/samples/voice.wav \
  --language "$LANGUAGE" \
  --output "/app/output/$OUTPUT_FILENAME"

# 完了メッセージ
echo "✅ 処理が完了しました！"
echo "出力ファイル: $CURRENT_DIR/output/$OUTPUT_FILENAME" 