#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
if ! docker ps | grep -q facefusion; then
    echo "FaceFusionコンテナが動いていません。先に run.sh を実行してください。"
    exit 1
fi
SOURCE_IMAGE=$(ls -1 "$PROJECT_DIR/data/source" | head -1)
TARGET_VIDEO=$(ls -1 "$PROJECT_DIR/data/target" | head -1)
echo "ソース画像: $SOURCE_IMAGE"
echo "ターゲット: $TARGET_VIDEO"
echo "顔入れ替え処理を実行します..."
docker exec facefusion python facefusion.py \
    --source "/app/facefusion/data/source/$SOURCE_IMAGE" \
    --target "/app/facefusion/data/target/$TARGET_VIDEO" \
    --output "/app/facefusion/data/output/output_$(date +%s).mp4" \
    --face-swapper-model "inswapper_128" \
    --face-analyser-order "large-small" \
    --face-analyser-age "adult" \
    --headless
echo "処理が完了しました！ 出力ファイルは data/output ディレクトリにあります。"
