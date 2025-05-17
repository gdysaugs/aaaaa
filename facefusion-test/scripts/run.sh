#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR/docker"
docker-compose build
docker-compose up -d
echo "FaceFusionが起動しました！"
echo "ブラウザで http://localhost:7860 にアクセスしてください。"
echo "ログを表示中... (Ctrl+Cで終了)"
docker logs -f facefusion
