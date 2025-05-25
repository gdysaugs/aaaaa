#!/bin/bash
# FaceFusion API 起動スクリプト
# べ、別にあんたのためじゃないけど、簡単に起動できるようにしてあげるわよ！

set -e

echo "🚀 FaceFusion API 起動スクリプト"
echo "================================"

# 現在のディレクトリ確認
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 作業ディレクトリ: $SCRIPT_DIR"

# 環境変数読み込み
if [ -f .env ]; then
    echo "📋 環境変数を読み込み中..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️ .envファイルが見つかりません。デフォルト設定を使用します。"
fi

# Python環境確認
echo "🐍 Python環境確認中..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3がインストールされていません"
    exit 1
fi

python3 --version

# 依存関係確認
echo "📦 依存関係確認中..."
if [ ! -f requirements.txt ]; then
    echo "❌ requirements.txtが見つかりません"
    exit 1
fi

# FaceFusion確認
FACEFUSION_PATH="${FACEFUSION_PATH:-/home/LLmmmmmm/projects/aaaaa/facefusion-test/facefusion}"
echo "🔍 FaceFusion確認中: $FACEFUSION_PATH"

if [ ! -d "$FACEFUSION_PATH" ]; then
    echo "❌ FaceFusionが見つかりません: $FACEFUSION_PATH"
    echo "💡 FaceFusionをクローンしてください:"
    echo "   git clone https://github.com/facefusion/facefusion.git"
    exit 1
fi

# GPU確認
echo "🎮 GPU確認中..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits
else
    echo "⚠️ nvidia-smiが見つかりません。CPUモードで動作します。"
fi

# ディレクトリ作成
echo "📁 必要なディレクトリを作成中..."
mkdir -p api/static/uploads
mkdir -p api/static/outputs
mkdir -p test_output

# 権限確認
echo "🔐 権限確認中..."
if [ ! -w api/static/uploads ] || [ ! -w api/static/outputs ]; then
    echo "⚠️ 書き込み権限がありません。権限を修正中..."
    chmod -R 755 api/static/
fi

# API起動
echo "🚀 FaceFusion API起動中..."
echo "   ホスト: ${API_HOST:-0.0.0.0}"
echo "   ポート: ${API_PORT:-8000}"
echo "   FaceFusionパス: $FACEFUSION_PATH"

# 環境変数設定
export PYTHONPATH="$FACEFUSION_PATH:$SCRIPT_DIR/api"
export OMP_NUM_THREADS=1

# API起動
cd api
python3 app/main.py
