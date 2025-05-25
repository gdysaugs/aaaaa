#!/bin/bash
# 🛑 AI開発プラットフォーム - 全FastAPI一括停止スクリプト
# 使用方法: ./stop_all_apis.sh

echo "🛑 全AIライブラリのFastAPI停止開始..."

# 現在のディレクトリを保存
ORIGINAL_DIR=$(pwd)

# FaceFusion FastAPI停止
echo "📸 FaceFusion FastAPI停止中..."
cd facefusion-test
if [ -f "docker-compose.yml" ]; then
    docker compose down
    echo "✅ FaceFusion FastAPI停止完了"
else
    echo "❌ FaceFusion docker-compose.yml が見つかりません"
fi
cd "$ORIGINAL_DIR"

# GPT-SoVITS v4 FastAPI停止
echo "🎤 GPT-SoVITS v4 FastAPI停止中..."
cd gpt-sovits-v4-cli-test

# FastAPIラッパープロセス停止
pkill -f "gpt_sovits_fastapi.py" 2>/dev/null || true
echo "✅ GPT-SoVITS FastAPIラッパー停止完了"

# GPT-SoVITS v4 内部API停止
if [ -f "docker-compose.fastapi.yml" ]; then
    docker compose -f docker-compose.fastapi.yml down
    echo "✅ GPT-SoVITS v4 内部API停止完了"
else
    echo "❌ GPT-SoVITS docker-compose.fastapi.yml が見つかりません"
fi
cd "$ORIGINAL_DIR"

# Wav2Lip FastAPI停止
echo "👄 Wav2Lip FastAPI停止中..."
cd wav2lip-test
if [ -f "docker-compose.yml" ]; then
    docker compose down
    echo "✅ Wav2Lip FastAPI停止完了"
else
    echo "❌ Wav2Lip docker-compose.yml が見つかりません"
fi
cd "$ORIGINAL_DIR"

# LLaMA-cpp FastAPI停止
echo "🦙 LLaMA-cpp FastAPI停止中..."
docker stop llama-cpp-api 2>/dev/null || true
docker rm llama-cpp-api 2>/dev/null || true
echo "✅ LLaMA-cpp FastAPI停止完了"

# 残存プロセス確認と停止
echo "🔍 残存プロセス確認中..."

# ポート使用状況確認
ports=(7862 8000 8001 8002 9880)
for port in "${ports[@]}"; do
    pid=$(lsof -t -i:$port 2>/dev/null || true)
    if [ ! -z "$pid" ]; then
        echo "⚠️  ポート $port を使用中のプロセス $pid を停止します"
        sudo kill -9 $pid 2>/dev/null || true
    fi
done

# Docker関連のクリーンアップ
echo "🧹 Docker環境クリーンアップ中..."
docker container prune -f 2>/dev/null || true

echo ""
echo "✅ 全FastAPI停止完了！"
echo ""
echo "📊 停止されたサービス:"
echo "  📸 FaceFusion:    http://localhost:7862"
echo "  🎤 GPT-SoVITS:    http://localhost:8000"
echo "  👄 Wav2Lip:       http://localhost:8001"
echo "  🦙 LLaMA-cpp:     http://localhost:8002"
echo ""
echo "🔍 停止確認:"
for port in "${ports[@]}"; do
    if ! netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        echo "✅ ポート $port: 停止済み"
    else
        echo "❌ ポート $port: まだ使用中"
    fi
done

echo ""
echo "🚀 再起動方法: ./start_all_apis.sh" 