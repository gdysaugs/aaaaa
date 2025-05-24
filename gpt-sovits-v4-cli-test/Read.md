# GPT-SoVITS v4 CLI Test Environment

RTX3050 & CUDA 12.4用に最適化されたGPT-SoVITS v4のボイスクローンCLIテスト環境です。

## 🎯 特徴

- **RTX3050最適化**: 4GB VRAMに最適化されたメモリ設定
- **CUDA 12.4対応**: 最新のCUDA環境をサポート
- **マルチステージビルド**: 効率的なDockerイメージ構築
- **Git LFS対策**: 大きなモデルファイルも確実にダウンロード
- **CLI API**: コマンドラインからの音声合成
- **バッチ処理**: 複数テキストの一括処理

## 📋 必要環境

### ハードウェア
- **GPU**: NVIDIA RTX3050 (4GB VRAM)
- **RAM**: 16GB以上推奨
- **ストレージ**: 50GB以上の空き容量

### ソフトウェア
- **OS**: Ubuntu 22.04 (WSL2)
- **Docker**: 20.10.0以上
- **Docker Compose**: 2.0以上
- **NVIDIA Container Toolkit**: 最新版
- **NVIDIA Driver**: 550.54.14以上 (CUDA 12.4対応)

## 🚀 クイックスタート

### 1. 環境確認

```bash
# GPUドライバー確認
nvidia-smi

# Dockerが動作することを確認
docker --version
docker compose --version

# NVIDIA Container Toolkitの確認
docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi
```

### 2. プロジェクトのセットアップ

```bash
# プロジェクトディレクトリに移動
cd /home/adama/LLM/gpt-sovits-v4-cli-test

# 必要なディレクトリを作成
mkdir -p models pretrained_models input output reference logs GPT_weights SoVITS_weights configs

# 環境変数ファイルをコピー
cp env.example .env
```

### 3. Dockerイメージのビルド

```bash
# ビルドキットを使用してマルチステージビルド
DOCKER_BUILDKIT=1 docker compose build --no-cache
```

**注意**: 初回ビルドは30-60分程度かかります（Git LFSでの大きなファイルダウンロードを含む）。

### 4. コンテナの起動

```bash
# バックグラウンドで起動
docker compose up -d

# ログを確認
docker compose logs -f gpt-sovits-v4-cli
```

### 5. GPU動作確認

```bash
# コンテナ内でGPU確認
docker compose exec gpt-sovits-v4-cli /workspace/check_gpu.sh

# または
python3 cli_test.py --check-gpu
```

## 🎵 使用方法

### API サーバーの起動

```bash
# コンテナ内でAPIサーバーを起動
docker compose exec gpt-sovits-v4-cli /workspace/GPT-SoVITS/start_api.sh
```

### CLI テストスクリプトの使用

```bash
# GPU状態確認
python3 cli_test.py --check-gpu

# API接続テスト
python3 cli_test.py --test-api

# バッチテスト実行
python3 cli_test.py --batch-test

# 単一テキストの音声合成
python3 cli_test.py \
  --text "こんにちは、これはテストです" \
  --ref-audio /workspace/reference/sample.wav \
  --output /workspace/output/result.wav
```

### 直接API呼び出し

```bash
# cURLでAPI呼び出し
curl -X POST "http://localhost:9880/tts" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "こんにちは、世界！",
    "text_lang": "ja",
    "ref_audio_path": "/workspace/reference/sample.wav",
    "prompt_text": "こんにちは",
    "prompt_lang": "ja"
  }' \
  --output output.wav
```

## 📁 ディレクトリ構造

```
gpt-sovits-v4-cli-test/
├── Dockerfile                 # マルチステージDockerfile
├── docker-compose.yml         # Docker Compose設定
├── env.example               # 環境変数サンプル
├── cli_test.py              # CLIテストスクリプト
├── start_api.sh             # API起動スクリプト
├── README.md                # このファイル
├── models/                  # カスタムモデル
├── pretrained_models/       # 事前学習済みモデル
├── input/                   # 入力ファイル
├── output/                  # 出力ファイル
├── reference/               # 参照音声
├── logs/                    # ログファイル
├── GPT_weights/             # GPTモデル重み
├── SoVITS_weights/          # SoVITSモデル重み
└── configs/                 # 設定ファイル
```

## 🔧 設定

### 環境変数

主要な環境変数は`env.example`を参照してください。

```bash
# RTX3050用メモリ最適化
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512,roundup_power2_divisions:2

# GPU設定
CUDA_VISIBLE_DEVICES=0

# API設定
API_HOST=0.0.0.0
API_PORT=9880
```

### v4用モデルファイル

GPT-SoVITS v4では以下のモデルファイルが必要です：

```
pretrained_models/
├── gsv-v4-pretrained/
│   ├── s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt  # GPTモデル
│   ├── s2v4.ckpt                                        # SoVITSモデル
│   └── vocoder.pth                                      # ボコーダー
├── chinese-hubert-base/                                 # HuBERTモデル
└── chinese-roberta-wwm-ext-large/                       # BERTモデル
```

## 🐛 トラブルシューティング

### よくある問題

#### 1. GPU認識されない
```bash
# ドライバー確認
nvidia-smi

# NVIDIA Container Toolkit再インストール
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

#### 2. メモリ不足エラー
```bash
# RTX3050用設定を確認
echo $PYTORCH_CUDA_ALLOC_CONF

# コンテナ再起動
docker compose restart gpt-sovits-v4-cli
```

#### 3. モデル読み込み失敗
```bash
# モデルファイルを確認
docker compose exec gpt-sovits-v4-cli ls -la /workspace/GPT-SoVITS/GPT_SoVITS/pretrained_models/

# 権限確認
docker compose exec gpt-sovits-v4-cli chown -R 1000:1000 /workspace/
```

#### 4. API接続失敗
```bash
# ポート確認
docker compose ps
netstat -tulpn | grep 9880

# ファイアウォール確認
sudo ufw status
```

### ログ確認

```bash
# コンテナログ
docker compose logs gpt-sovits-v4-cli

# リアルタイムログ
docker compose logs -f gpt-sovits-v4-cli

# GPU使用状況監視
watch -n 1 nvidia-smi
```

## 📊 パフォーマンス

### RTX3050での期待値

- **音声合成時間**: 10秒の音声で約5-10秒
- **VRAM使用量**: 2-3GB
- **最大バッチサイズ**: 1-2
- **コンテキスト長**: 最大4096トークン

## 🔄 アップデート

```bash
# 最新のGPT-SoVITSに更新
docker compose build --no-cache

# コンテナ再起動
docker compose down && docker compose up -d
```

## 📝 v4の新機能

- **48kHz音声出力**: v3の24kHzから向上
- **金属音アーティファクト修正**: より自然な音質
- **新しいボコーダー**: vocoder.pthによる高品質変換
- **改善されたアップサンプリング**: 整数倍アップサンプリング

## ⚠️ 注意事項

1. **メモリ使用量**: RTX3050は4GB VRAMのため、大きなモデル/長いテキストでOOMが発生する可能性があります
2. **モデルダウンロード**: 初回起動時に大きなモデルファイルをダウンロードするため、十分な帯域幅が必要です
3. **ライセンス**: GPT-SoVITSのMITライセンスを遵守してください
4. **商用利用**: モデルのライセンスに従って適切に使用してください

## 🆘 サポート

問題が発生した場合：

1. このREADMEのトラブルシューティングセクションを確認
2. [GPT-SoVITS GitHub Issues](https://github.com/RVC-Boss/GPT-SoVITS/issues)を検索
3. ログファイルとGPU情報を添えてイシューを作成

## 🙏 謝辞

- [RVC-Boss/GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) - 元プロジェクト
- NVIDIAコミュニティ - CUDA最適化のヒント
- Dockerコミュニティ - マルチステージビルドのベストプラクティス 