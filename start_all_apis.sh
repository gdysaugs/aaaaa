#!/bin/bash
# 🚀 AI開発プラットフォーム - 全FastAPI一括起動スクリプト
# 使用方法: ./start_all_apis.sh

set -e  # エラー時に停止

echo "🚀 全AIライブラリのFastAPI起動開始..."
echo "📊 起動予定サービス:"
echo "  📸 FaceFusion:    http://localhost:7862"
echo "  🎤 GPT-SoVITS:    http://localhost:8000"
echo "  👄 Wav2Lip:       http://localhost:8001"
echo "  🦙 LLaMA-cpp:     http://localhost:8002"
echo ""

# 現在のディレクトリを保存
ORIGINAL_DIR=$(pwd)

# FaceFusion FastAPI
echo "📸 FaceFusion FastAPI起動中..."
cd facefusion-test
if [ -f "docker-compose.yml" ]; then
    DOCKER_BUILDKIT=1 docker compose up -d
    echo "✅ FaceFusion FastAPI起動完了 (ポート7862)"
else
    echo "❌ FaceFusion docker-compose.yml が見つかりません"
fi
cd "$ORIGINAL_DIR"

# GPT-SoVITS v4 FastAPI
echo "🎤 GPT-SoVITS v4 FastAPI起動中..."
cd gpt-sovits-v4-cli-test

# GPT-SoVITS v4 APIサーバー起動
if [ -f "docker-compose.fastapi.yml" ]; then
    docker compose -f docker-compose.fastapi.yml up -d
    echo "✅ GPT-SoVITS v4 内部API起動完了 (ポート9880)"
    
    # FastAPIラッパー起動
    sleep 5  # 内部APIの起動を待つ
    if [ -f "gpt_sovits_fastapi.py" ]; then
        python3 gpt_sovits_fastapi.py --host 0.0.0.0 --port 8000 --api-url http://localhost:9880 > fastapi.log 2>&1 &
        echo "✅ GPT-SoVITS FastAPIラッパー起動完了 (ポート8000)"
    else
        echo "❌ gpt_sovits_fastapi.py が見つかりません"
    fi
else
    echo "❌ GPT-SoVITS docker-compose.fastapi.yml が見つかりません"
fi
cd "$ORIGINAL_DIR"

# Wav2Lip FastAPI
echo "👄 Wav2Lip FastAPI起動中..."
cd wav2lip-test
if [ -f "docker-compose.yml" ]; then
    docker compose up -d
    echo "✅ Wav2Lip FastAPI起動完了 (ポート8001)"
else
    echo "❌ Wav2Lip docker-compose.yml が見つかりません"
fi
cd "$ORIGINAL_DIR"

# LLaMA-cpp FastAPI
echo "🦙 LLaMA-cpp FastAPI起動中..."
cd llama-cpp-cli-test

# 既存のコンテナを停止・削除
docker stop llama-cpp-api 2>/dev/null || true
docker rm llama-cpp-api 2>/dev/null || true

if [ -f "Dockerfile" ]; then
    # Dockerイメージをビルド（存在しない場合）
    if ! docker images | grep -q llama-cpp-api; then
        docker build -t llama-cpp-api .
    fi
    
    # FastAPI起動
    docker run -d --name llama-cpp-api \
        --gpus all \
        -p 8002:8000 \
        -v $(pwd)/models:/app/models \
        llama-cpp-api
    echo "✅ LLaMA-cpp FastAPI起動完了 (ポート8002)"
else
    echo "❌ LLaMA-cpp Dockerfile が見つかりません"
fi
cd "$ORIGINAL_DIR"

echo ""
echo "🎉 全FastAPI起動完了！"
echo ""
echo "📊 サービス一覧:"
echo "  📸 FaceFusion:    http://localhost:7862"
echo "  🎤 GPT-SoVITS:    http://localhost:8000"
echo "  👄 Wav2Lip:       http://localhost:8001"
echo "  🦙 LLaMA-cpp:     http://localhost:8002"
echo ""
echo "🔍 ヘルスチェック実行中..."
sleep 10  # サービス起動を待つ

# ヘルスチェック
services=(
  "FaceFusion:http://localhost:7862/health"
  "GPT-SoVITS:http://localhost:8000/health"
  "Wav2Lip:http://localhost:8001/health"
  "LLaMA-cpp:http://localhost:8002/health"
)

for service in "${services[@]}"; do
  name=$(echo $service | cut -d: -f1)
  url=$(echo $service | cut -d: -f2-)
  
  if curl -s $url > /dev/null 2>&1; then
    echo "✅ $name: 正常"
  else
    echo "❌ $name: エラー (起動中の可能性があります)"
  fi
done

echo ""
echo "🚀 AI開発プラットフォーム起動完了！"
echo "📝 ログ確認: docker logs <コンテナ名>"
echo "🛑 停止方法: ./stop_all_apis.sh" 