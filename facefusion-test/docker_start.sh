#!/bin/bash
# べ、別にあんたのためじゃないけど、Dockerでサービスを起動してあげるわよ！

set -e

echo "🐳 FaceFusion Docker Service Manager"
echo "=================================="

# 色付きメッセージ用関数
info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

success() {
    echo -e "\033[1;32m[SUCCESS]\033[0m $1"
}

warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# GPU確認
check_gpu() {
    info "GPU環境確認中..."
    
    if command -v nvidia-smi &> /dev/null; then
        nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits
        success "NVIDIA GPU検出完了"
    else
        warning "nvidia-smiが見つかりません。GPU機能は利用できません。"
    fi
}

# Docker確認
check_docker() {
    info "Docker環境確認中..."
    
    if ! command -v docker &> /dev/null; then
        error "Dockerがインストールされていません"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        error "Docker デーモンが起動していません"
        exit 1
    fi
    
    success "Docker確認完了"
}

# Docker Composeファイル確認
check_compose_file() {
    if [ ! -f "docker-compose.yml" ]; then
        error "docker-compose.ymlが見つかりません"
        exit 1
    fi
    success "docker-compose.yml確認完了"
}

# サービス構築
build_service() {
    info "Dockerイメージ構築中..."
    
    export DOCKER_BUILDKIT=1
    
    if docker compose build --no-cache; then
        success "イメージ構築完了"
    else
        error "イメージ構築失敗"
        exit 1
    fi
}

# サービス起動
start_service() {
    info "サービス起動中..."
    
    if docker compose up -d; then
        success "サービス起動完了"
        
        # サービス状態確認
        sleep 5
        info "サービス状態確認中..."
        docker compose ps
        
        # ヘルスチェック
        info "ヘルスチェック実行中..."
        for i in {1..30}; do
            if curl -s http://localhost:8000/health > /dev/null; then
                success "サービスが正常に起動しました"
                info "Swagger UI: http://localhost:8000/"
                info "ReDoc: http://localhost:8000/redoc"
                info "CLI Help: http://localhost:8000/cli-help"
                return 0
            fi
            echo -n "."
            sleep 2
        done
        
        warning "ヘルスチェックタイムアウト。ログを確認してください。"
        docker compose logs --tail=20
    else
        error "サービス起動失敗"
        exit 1
    fi
}

# サービス停止
stop_service() {
    info "サービス停止中..."
    
    if docker compose down; then
        success "サービス停止完了"
    else
        error "サービス停止失敗"
        exit 1
    fi
}

# ログ表示
show_logs() {
    info "サービスログ表示..."
    docker compose logs -f facefusion-api
}

# サービス再起動
restart_service() {
    info "サービス再起動中..."
    stop_service
    start_service
}

# 状態確認
check_status() {
    info "サービス状態:"
    docker compose ps
    
    info "リソース使用量:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
}

# クリーンアップ
cleanup() {
    info "クリーンアップ実行中..."
    
    # 停止したコンテナ削除
    docker compose down --remove-orphans
    
    # 未使用イメージ削除
    docker image prune -f
    
    # 未使用ボリューム削除（注意深く）
    read -p "未使用ボリュームも削除しますか？ (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker volume prune -f
    fi
    
    success "クリーンアップ完了"
}

# ヘルプ表示
show_help() {
    echo "使用方法: $0 [オプション]"
    echo ""
    echo "オプション:"
    echo "  build      - Dockerイメージを構築"
    echo "  start      - サービスを起動"
    echo "  stop       - サービスを停止"
    echo "  restart    - サービスを再起動"
    echo "  logs       - ログを表示"
    echo "  status     - 状態を確認"
    echo "  cleanup    - クリーンアップ"
    echo "  help       - このヘルプを表示"
    echo ""
    echo "例:"
    echo "  $0 build     # イメージ構築"
    echo "  $0 start     # サービス起動"
    echo "  $0 logs      # ログ表示"
}

# メイン処理
main() {
    case "${1:-help}" in
        "build")
            check_docker
            check_compose_file
            check_gpu
            build_service
            ;;
        "start")
            check_docker
            check_compose_file
            check_gpu
            start_service
            ;;
        "stop")
            check_docker
            stop_service
            ;;
        "restart")
            check_docker
            check_compose_file
            restart_service
            ;;
        "logs")
            check_docker
            show_logs
            ;;
        "status")
            check_docker
            check_status
            ;;
        "cleanup")
            check_docker
            cleanup
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# スクリプト実行
main "$@" 