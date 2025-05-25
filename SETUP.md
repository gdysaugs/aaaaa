# 🚀 プロジェクトセットアップ手順書

このリポジトリをクローンした後の完全なセットアップ手順です。

## 📋 前提条件

### 必要な環境
- **OS**: WSL2 Ubuntu 22.04 
- **Docker**: Docker Engine + Docker Compose
- **GPU**: NVIDIA RTX 3050 (または対応GPU)
- **NVIDIA Driver**: 560.70以上
- **CUDA**: 11.8 (Docker内で管理)

### 初期確認
```bash
# GPU確認
nvidia-smi

# Docker確認  
docker --version
docker compose version

# WSL2のGPU確認
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi
```

## 🔄 基本セットアップ

### 1. リポジトリクローン
```bash
cd /home/adama/LLM
git clone https://github.com/gdysaugs/aaaaa.git
cd aaaaa
```

### 2. ディレクトリ構造作成
```bash
# 必要なディレクトリを作成（.gitignoreで除外されたディレクトリ）
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
```

## 🎯 プロジェクト別セットアップ

### 📸 FaceFusion (顔交換)

#### モデルファイル配置
FaceFusionは初回実行時に自動でモデルをダウンロードします。

#### テスト用データ準備
```bash
cd facefusion-test/data/source

# サンプル画像をダウンロード（またはお好みの画像を配置）
wget -O source_face.jpg "https://example.com/sample_face.jpg"
wget -O target_video.mp4 "https://example.com/sample_video.mp4"
```

#### Docker構築と実行
```bash
cd facefusion-test/docker
DOCKER_BUILDKIT=1 docker compose build
docker compose up -d

# ログ確認
docker logs facefusion-app

# CLIテスト実行
docker exec -it facefusion-app python3 facefusion.py headless-run \
  --source-paths /app/facefusion/.assets/test/source/source_face.jpg \
  --target-path /app/facefusion/.assets/test/source/target_video.mp4 \
  --output-path /app/facefusion/.assets/test/output/result.mp4 \
  --processors face_swapper \
  --execution-providers cuda \
  --output-video-quality 80
```

### 🎤 GPT-SoVITS v4 (音声合成)

#### プリトレインモデルダウンロード
```bash
cd gpt-sovits-v4-cli-test

# モデルダウンロードスクリプト実行
chmod +x download_correct_v4.sh
./download_correct_v4.sh

# または手動ダウンロード
./manual_download.sh
```

#### 必要なモデルファイル
```bash
pretrained_models/
├── chinese-hubert-base/
│   ├── config.json
│   ├── preprocessor_config.json  
│   └── pytorch_model.bin (361MB)
├── chinese-roberta-wwm-ext-large/
│   ├── config.json
│   ├── pytorch_model.bin (1.3GB)
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   └── vocab.txt
├── gsv-v4-pretrained/
│   ├── s2v4.ckpt (4KB)
│   ├── s2Gv4.pth (734MB)
│   └── vocoder.pth (56MB)
└── s1v3.ckpt (149MB)
```

#### Docker構築と実行
```bash
# PyTorch 2.6版（推奨）
docker compose -f docker-compose.v2.6.yml build
docker compose -f docker-compose.v2.6.yml up -d

# または標準版
docker compose build  
docker compose up -d

# CLIテスト
python3 cli_test.py
python3 test_multilingual.py
```

### 👄 Wav2Lip (リップシンク)

#### モデルファイルダウンロード
```bash
cd wav2lip-test

# Wav2Lipモデルダウンロード
wget -P models/ "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip.pth"

# 顔検出モデルダウンロード  
wget -P models/face_detection/detection/sfd/ "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/s3fd.pth"
```

#### 必要なモデルファイル
```bash
models/
├── wav2lip.pth (416MB)
└── face_detection/
    └── detection/
        └── sfd/
            └── s3fd.pth (86MB)
```

#### Docker構築と実行
```bash
cd wav2lip-test/docker
docker compose build
docker compose up -d

# テスト実行
./scripts/run_wav2lip.sh
```

### 🦙 LLaMA-cpp-cli (LLM推論)

#### モデルファイルダウンロード
```bash
cd llama-cpp-cli-test/models

# 例：小さめのモデル（7B量子化版）をダウンロード
wget "https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/pytorch_model.bin"

# または任意の.ggufモデルをダウンロード
# Hugging Face Hub等から適切なモデルを選択
```

#### Docker構築と実行  
```bash
cd llama-cpp-cli-test
docker build -t llama-cpp-cli .
docker run --gpus all -v $(pwd)/models:/app/models llama-cpp-cli

# CLIテスト
./cli_test.sh
```

### 🔧 MCP-for-Cursor (Cursor統合)

#### セットアップ
```bash
cd mcp-for-cursor

# 必要に応じて設定ファイルを調整
# 特別なモデルファイルは不要
```

## 🐋 全体Docker環境構築

### 一括構築スクリプト
```bash
#!/bin/bash
# build_all.sh

echo "🚀 全プロジェクトDocker環境構築開始..."

# FaceFusion
echo "📸 FaceFusion構築中..."
cd facefusion-test/docker && DOCKER_BUILDKIT=1 docker compose build && cd ../..

# GPT-SoVITS v4  
echo "🎤 GPT-SoVITS v4構築中..."
cd gpt-sovits-v4-cli-test && docker compose -f docker-compose.v2.6.yml build && cd ..

# Wav2Lip
echo "👄 Wav2Lip構築中..."  
cd wav2lip-test/docker && docker compose build && cd ../..

# LLaMA-cpp-cli
echo "🦙 LLaMA-cpp-cli構築中..."
cd llama-cpp-cli-test && docker build -t llama-cpp-cli . && cd ..

echo "✅ 全プロジェクトDocker構築完了！"
```

### 実行権限付与と実行
```bash
chmod +x build_all.sh
./build_all.sh
```

## 🔍 動作確認

### GPUアクセス確認
```bash
# 各コンテナでGPU確認
docker exec -it facefusion-app nvidia-smi
docker exec -it gpt-sovits-v4-dev-pytorch26 nvidia-smi  
docker exec -it wav2lip-gpu nvidia-smi
```

### パフォーマンステスト
```bash
# FaceFusion：顔交換テスト（約94秒想定）
cd facefusion-test && python3 working_cli.py

# GPT-SoVITS：音声合成テスト
cd gpt-sovits-v4-cli-test && python3 simple_test.py

# Wav2Lip：リップシンクテスト  
cd wav2lip-test && python3 test_basic.py
```

## 📊 トラブルシューティング

### よくある問題

#### 1. GPU認識されない
```bash
# WSL2のGPU設定確認
wsl.exe --update
# Windows側でNVIDIAドライバを最新に更新

# Dockerランタイム確認
docker info | grep nvidia
```

#### 2. モデルファイル不足エラー
```bash
# 不足しているモデルを個別ダウンロード
# エラーメッセージでファイル名を確認し、適切なソースからダウンロード
```

#### 3. メモリ不足エラー  
```bash
# Docker設定調整
# RTX 3050は4GB VRAMなので、バッチサイズやモデルサイズを調整
```

#### 4. ポート競合
```bash
# 使用中ポート確認
netstat -tlnp | grep :7860

# docker-compose.ymlでポート番号変更
# 7860 → 7862等
```

## 🔄 定期メンテナンス

### モデル更新
```bash
# 各プロジェクトのモデルを定期的に更新
cd gpt-sovits-v4-cli-test && ./download_correct_v4.sh
```

### Docker環境更新
```bash
# イメージ更新
docker compose pull
docker compose build --no-cache
```

### ディスク使用量確認
```bash
# 大きなファイル確認  
find . -size +100M -type f -exec ls -lh {} \;

# Docker使用量確認
docker system df
```

## 📝 開発時の注意点

### .gitignoreの重要性
- **大きなファイルは絶対にコミットしない**
- モデルファイル（.bin, .ckpt, .pth, .onnx, .gguf）は除外済み
- output/ディレクトリも除外済み

### GPU最適化
- RTX 3050 (4GB VRAM)に合わせた設定  
- バッチサイズやモデルサイズを適切に調整
- CUDA 11.8で統一（互換性確保）

### ポート管理
- FaceFusion: 7862-7863
- GPT-SoVITS: 7860-7861  
- Wav2Lip: 9870-9871
- 競合回避のため事前に割り当て

---

## 🎉 セットアップ完了！

すべての手順が完了すれば、以下の機能が利用可能になります：

- 🎯 **FaceFusion**: GPU加速顔交換（94秒/488フレーム）
- 🎤 **GPT-SoVITS v4**: 高品質音声合成  
- 👄 **Wav2Lip**: リップシンク処理
- 🦙 **LLaMA-cpp-cli**: LLM推論
- 🔧 **MCP-for-Cursor**: Cursor統合

**Happy AI Development! 🚀** 