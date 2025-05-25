# llama-cpp-python GPU対応 CLI & API テスト環境

## 🎯 概要

**Berghof-NSFW-7B-i1-GGUF** モデルを使用したGPU対応のllama-cpp-python環境です。
CLIチャットとFastAPI サーバーの両方に対応しています。

## 🏗️ 構成

- **ベースイメージ**: nvidia/cuda:11.8.0-devel-ubuntu22.04
- **Python**: 3.10
- **GPU**: CUDA 11.8 + cuBLAS対応
- **モデル**: [Berghof-NSFW-7B-i1-GGUF](https://huggingface.co/mradermacher/Berghof-NSFW-7B-i1-GGUF)
- **量子化**: Q4_K_S (4.2GB)
- **API**: FastAPI + uvicorn
- **コンテナ**: Docker + docker-compose

## 📋 必要条件

### ハードウェア
- **GPU**: NVIDIA RTX 3050以上（VRAM 4GB以上推奨）
- **RAM**: 8GB以上
- **ストレージ**: 10GB以上の空き容量

### ソフトウェア
- **OS**: WSL2 + Ubuntu 22.04 または Linux
- **Docker**: 20.10以上
- **nvidia-docker2**: GPU対応
- **NVIDIA Driver**: 470以上

## 🚀 クイックスタート

### 1. モデルダウンロード

```bash
# プロジェクトディレクトリに移動
cd /home/LLmmmmmm/projects/aaaaa/llama-cpp-cli-test

# モデルファイルをダウンロード
wget -O models/Berghof-NSFW-7B.i1-Q4_K_S.gguf \
  https://huggingface.co/mradermacher/Berghof-NSFW-7B-i1-GGUF/resolve/main/Berghof-NSFW-7B.i1-Q4_K_S.gguf
```

### 2. 環境設定

```bash
# .envファイルを作成
cp .env.example .env

# 必要に応じて設定を編集
nano .env
```

### 3. Docker ビルド

```bash
# GPU対応でビルド
DOCKER_BUILDKIT=1 docker build -t llama-cpp-cli-test .

# または docker-compose でビルド
docker-compose build
```

## 🎮 使用方法

### CLI チャットモード

```bash
# 直接実行
docker run --gpus all --rm -it \
  -v $(pwd)/models:/models \
  llama-cpp-cli-test python3 chat_llama.py

# docker-compose で実行
docker-compose --profile cli run --rm llama-cli
```

### FastAPI サーバーモード

```bash
# サーバー起動
docker-compose up llama-api

# バックグラウンド実行
docker-compose up -d llama-api

# ログ確認
docker-compose logs -f llama-api
```

### API エンドポイント

サーバー起動後、以下のエンドポイントが利用可能：

- **API ドキュメント**: http://localhost:8000/docs
- **ヘルスチェック**: http://localhost:8000/health
- **チャット**: http://localhost:8000/chat
- **ストリーミングチャット**: http://localhost:8000/chat/stream

#### API 使用例

```bash
# ヘルスチェック
curl http://localhost:8000/health

# チャット
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "こんにちは！",
    "max_tokens": 100,
    "temperature": 0.7
  }'

# ストリーミングチャット
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "message": "長い話をして",
    "max_tokens": 200
  }'
```

## 📁 プロジェクト構造

```
llama-cpp-cli-test/
├── models/                          # モデルファイル
│   └── Berghof-NSFW-7B.i1-Q4_K_S.gguf
├── Dockerfile                       # マルチステージビルド
├── docker-compose.yml              # サービス定義
├── requirements.txt                 # Python依存関係
├── llama_api.py                    # FastAPI サーバー
├── chat_llama.py                   # CLIチャット
├── cli_test.sh                     # テストスクリプト
├── .env.example                    # 環境変数テンプレート
├── .dockerignore                   # Docker除外ファイル
└── README.md                       # このファイル
```

## ⚙️ 設定

### 環境変数 (.env)

```env
# モデル設定
MODEL_PATH=/models/Berghof-NSFW-7B.i1-Q4_K_S.gguf
N_GPU_LAYERS=-1                     # -1: 全レイヤーをGPUに
N_CTX=2048                          # コンテキスト長
MAX_TOKENS=128                      # 最大生成トークン数

# サーバー設定
HOST=0.0.0.0
PORT=8000

# CUDA設定
CUDA_VISIBLE_DEVICES=0              # 使用するGPU ID
```

### パフォーマンス調整

#### GPU メモリ使用量の調整
```bash
# 部分的にGPUを使用（メモリ不足の場合）
N_GPU_LAYERS=20  # レイヤー数を調整

# コンテキスト長を調整
N_CTX=1024       # メモリ使用量を削減
```

#### 推論パラメータ
```python
# temperature: 0.1-2.0 (創造性)
# max_tokens: 1-2048 (応答長)
# top_p: 0.1-1.0 (多様性)
```

## 🔧 トラブルシューティング

### GPU認識されない場合

```bash
# nvidia-docker2 インストール確認
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi

# CUDA ドライバー確認
nvidia-smi

# Docker デーモン再起動
sudo systemctl restart docker
```

### メモリ不足エラー

```bash
# GPU レイヤー数を削減
N_GPU_LAYERS=10

# コンテキスト長を削減
N_CTX=1024

# 量子化レベルを下げる（別モデル使用）
# Q4_K_S → Q3_K_S → Q2_K
```

### ビルドエラー

```bash
# キャッシュクリア
docker system prune -a

# 強制リビルド
docker-compose build --no-cache

# ログ確認
docker-compose logs llama-api
```

## 📊 パフォーマンス

### RTX 3050 Laptop GPU での測定値

- **モデル読み込み**: 約30秒
- **推論速度**: 7-10 tokens/sec
- **VRAM使用量**: 約3.5GB
- **GPU使用率**: 80-95%

### 最適化のポイント

1. **量子化レベル**: Q4_K_S が速度と品質のバランス良好
2. **GPU レイヤー**: -1（全レイヤー）で最高性能
3. **コンテキスト長**: 用途に応じて調整
4. **バッチサイズ**: 1（llama.cppの制限）

## 🔗 関連リンク

### モデル情報
- **Hugging Face**: [mradermacher/Berghof-NSFW-7B-i1-GGUF](https://huggingface.co/mradermacher/Berghof-NSFW-7B-i1-GGUF)
- **ベースモデル**: [Elizezen/Berghof-NSFW-7B](https://huggingface.co/Elizezen/Berghof-NSFW-7B)
- **量子化情報**: imatrix量子化済み

### 技術文書
- **llama.cpp**: [GitHub](https://github.com/ggerganov/llama.cpp)
- **llama-cpp-python**: [GitHub](https://github.com/abetlen/llama-cpp-python)
- **CUDA Toolkit**: [NVIDIA Developer](https://developer.nvidia.com/cuda-toolkit)
- **FastAPI**: [公式ドキュメント](https://fastapi.tiangolo.com/)

### 代替モデル（同じ設定で使用可能）

| モデル | サイズ | 量子化 | 用途 |
|--------|--------|--------|------|
| Llama-2-7B-Chat-GGUF | 7B | Q4_K_M | 汎用チャット |
| CodeLlama-7B-Instruct-GGUF | 7B | Q4_K_M | コード生成 |
| Mistral-7B-Instruct-v0.2-GGUF | 7B | Q4_K_M | 高性能チャット |

## 📝 ライセンス

- **プロジェクト**: MIT License
- **llama.cpp**: MIT License  
- **モデル**: 各モデルのライセンスに従う

## 🤝 貢献

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 サポート

- **Issues**: GitHub Issues
- **Discord**: llama.cpp コミュニティ
- **Documentation**: [llama-cpp-python docs](https://llama-cpp-python.readthedocs.io/)

---

**⚠️ 注意**: このモデルはNSFW（成人向け）コンテンツを含む可能性があります。適切な環境でのみ使用してください。 