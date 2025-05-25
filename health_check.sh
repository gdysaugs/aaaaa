#!/bin/bash
# 🔍 AI開発プラットフォーム - 全FastAPIヘルスチェックスクリプト
# 使用方法: ./health_check.sh

echo "🔍 全AIライブラリのFastAPIヘルスチェック開始..."
echo ""

# ヘルスチェック関数
check_service() {
    local name=$1
    local url=$2
    local port=$3
    
    echo -n "🔍 $name (ポート$port): "
    
    # ポート確認
    if ! netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        echo "❌ ポートが開いていません"
        return 1
    fi
    
    # HTTP確認
    if curl -s --max-time 5 "$url" > /dev/null 2>&1; then
        echo "✅ 正常"
        return 0
    else
        echo "❌ HTTPエラー"
        return 1
    fi
}

# GPU状況確認
echo "🎮 GPU状況確認:"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits | while read line; do
        echo "  📊 $line"
    done
else
    echo "  ❌ nvidia-smi が見つかりません"
fi
echo ""

# Docker状況確認
echo "🐳 Docker状況確認:"
docker_containers=(
    "facefusion-api"
    "gpt-sovits-v4-api"
    "wav2lip-api"
    "llama-cpp-api"
)

for container in "${docker_containers[@]}"; do
    if docker ps --format "table {{.Names}}" | grep -q "$container"; then
        status=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null || echo "not found")
        echo "  ✅ $container: $status"
    else
        echo "  ❌ $container: 停止中"
    fi
done
echo ""

# サービスヘルスチェック
echo "🌐 FastAPIサービスヘルスチェック:"

services=(
    "FaceFusion:http://localhost:7862/health:7862"
    "GPT-SoVITS:http://localhost:8000/health:8000"
    "Wav2Lip:http://localhost:8001/health:8001"
    "LLaMA-cpp:http://localhost:8002/health:8002"
)

success_count=0
total_count=${#services[@]}

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    url=$(echo $service | cut -d: -f2-3)
    port=$(echo $service | cut -d: -f4)
    
    if check_service "$name" "$url" "$port"; then
        ((success_count++))
    fi
done

echo ""

# GPU状況詳細確認（各コンテナ内）
echo "🎮 各コンテナのGPU確認:"
for container in "${docker_containers[@]}"; do
    if docker ps --format "table {{.Names}}" | grep -q "$container"; then
        echo "  🔍 $container:"
        docker exec "$container" nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader,nounits 2>/dev/null | head -1 | while read line; do
            echo "    📊 $line"
        done || echo "    ❌ GPU情報取得失敗"
    fi
done
echo ""

# 結果サマリー
echo "📊 ヘルスチェック結果:"
echo "  ✅ 正常サービス: $success_count/$total_count"

if [ $success_count -eq $total_count ]; then
    echo "  🎉 全サービス正常動作中！"
    exit_code=0
else
    echo "  ⚠️  一部サービスに問題があります"
    exit_code=1
fi

echo ""
echo "🔧 トラブルシューティング:"
echo "  📝 ログ確認: docker logs <コンテナ名>"
echo "  🔄 再起動: ./stop_all_apis.sh && ./start_all_apis.sh"
echo "  🎮 GPU確認: nvidia-smi"
echo "  🌐 ポート確認: netstat -tlnp | grep -E ':(7862|8000|8001|8002|9880)'"

exit $exit_code 