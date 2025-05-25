#!/bin/bash

# =================================================================
# 🚀 全プロジェクトDocker環境一括構築スクリプト
# =================================================================

set -e  # エラー時に終了

echo "🚀 全プロジェクトDocker環境構築開始..."
echo "⚠️  注意: この処理には時間がかかります（30-60分程度）"
echo ""

# 必要なディレクトリを作成
echo "📁 必要なディレクトリ構造を作成中..."
mkdir -p facefusion-test/data/source
mkdir -p facefusion-test/data/output
mkdir -p gpt-sovits-v4-cli-test/pretrained_models
mkdir -p gpt-sovits-v4-cli-test/GPT_weights
mkdir -p gpt-sovits-v4-cli-test/SoVITS_weights
mkdir -p gpt-sovits-v4-cli-test/input
mkdir -p gpt-sovits-v4-cli-test/output
mkdir -p gpt-sovits-v4-cli-test/logs
mkdir -p wav2lip-test/models/face_detection/detection/sfd
mkdir -p wav2lip-test/data/input
mkdir -p wav2lip-test/data/output
mkdir -p llama-cpp-cli-test/models

echo "✅ ディレクトリ構造作成完了"
echo ""

# FaceFusion構築
echo "📸 FaceFusion構築中..."
cd facefusion-test/docker
if DOCKER_BUILDKIT=1 docker compose build; then
    echo "✅ FaceFusion構築完了"
else
    echo "❌ FaceFusion構築失敗"
    exit 1
fi
cd ../..
echo ""

# GPT-SoVITS v4構築
echo "🎤 GPT-SoVITS v4構築中..."
cd gpt-sovits-v4-cli-test
if docker compose -f docker-compose.v2.6.yml build; then
    echo "✅ GPT-SoVITS v4構築完了"
else
    echo "❌ GPT-SoVITS v4構築失敗"
    exit 1
fi
cd ..
echo ""

# Wav2Lip構築
echo "👄 Wav2Lip構築中..."
cd wav2lip-test/docker
if docker compose build; then
    echo "✅ Wav2Lip構築完了"
else
    echo "❌ Wav2Lip構築失敗"
    exit 1
fi
cd ../..
echo ""

# LLaMA-cpp-cli構築
echo "🦙 LLaMA-cpp-cli構築中..."
cd llama-cpp-cli-test
if docker build -t llama-cpp-cli .; then
    echo "✅ LLaMA-cpp-cli構築完了"
else
    echo "❌ LLaMA-cpp-cli構築失敗"
    exit 1
fi
cd ..
echo ""

# 構築結果確認
echo "🔍 構築結果確認..."
echo "Dockerイメージ一覧:"
docker images | grep -E "(facefusion|gpt-sovits|wav2lip|llama-cpp)"
echo ""

# GPU確認
echo "🔧 GPU動作確認..."
if docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi > /dev/null 2>&1; then
    echo "✅ GPU正常動作"
else
    echo "⚠️  GPU動作に問題がある可能性があります"
fi
echo ""

# 完了メッセージ
echo "🎉 全プロジェクトDocker構築完了！"
echo ""
echo "📋 次のステップ:"
echo "1. 各プロジェクトのモデルファイルをダウンロード (SETUP.mdを参照)"
echo "2. テスト用データを配置"
echo "3. 各プロジェクトの動作確認"
echo ""
echo "📖 詳細な手順はSETUP.mdを参照してください"
echo "🚀 Happy AI Development!" 