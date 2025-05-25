# FaceFusion API

べ、別にあんたのためじゃないけど、ちゃんとしたFace Swap APIを作ってあげたわよ！

## 🎯 概要

FaceFusionをベースにしたFace Swap APIサービスです。画像と動画の顔交換処理をREST APIで提供します。

## 🚀 機能

- **画像Face Swap**: 画像の顔を別の画像の顔に交換
- **動画Face Swap**: 動画の顔を画像の顔に交換
- **ファイルアップロード**: 画像・動画ファイルのアップロード
- **ファイルダウンロード**: 処理済みファイルのダウンロード
- **ヘルスチェック**: API・GPU・FaceFusionの状態確認

## 📋 必要な環境

- Ubuntu 22.04 (WSL2推奨)
- Python 3.8+
- CUDA 11.8
- Docker & Docker Compose
- NVIDIA GPU (RTX 3050以上推奨)

## 🛠️ インストール

### 1. リポジトリクローン

```bash
git clone <repository-url>
cd facefusion-test
```

### 2. 環境変数設定

```bash
cp .env.example .env
# .envファイルを編集して環境に合わせて設定
```

### 3. Dockerビルド

```bash
# ビルドキット使用
export DOCKER_BUILDKIT=1
docker-compose build --no-cache
```

### 4. サービス起動

```bash
docker-compose up -d
```

## 📚 API エンドポイント

### ヘルスチェック
```http
GET /health
```

### ファイルアップロード
```http
POST /upload
Content-Type: multipart/form-data

file: <画像または動画ファイル>
```

### 画像Face Swap
```http
POST /face-swap/image
Content-Type: multipart/form-data

source_file: <ソース画像ファイル>
target_file: <ターゲット画像ファイル>
model: inswapper_128 (オプション)
quality: 90 (オプション, 1-100)
```

### 動画Face Swap
```http
POST /face-swap/video
Content-Type: multipart/form-data

source_file: <ソース画像ファイル>
target_file: <ターゲット動画ファイル>
model: inswapper_128 (オプション)
quality: 80 (オプション, 1-100)
trim_start: 0 (オプション, 開始フレーム)
trim_end: null (オプション, 終了フレーム)
```

### ファイルダウンロード
```http
GET /download/{filename}
```

## 🎮 使用例

### cURLでの使用例

```bash
# ヘルスチェック
curl http://localhost:8000/health

# 画像Face Swap
curl -X POST http://localhost:8000/face-swap/image \
  -F "source_file=@source.jpg" \
  -F "target_file=@target.jpg" \
  -F "quality=90"

# 動画Face Swap
curl -X POST http://localhost:8000/face-swap/video \
  -F "source_file=@source.jpg" \
  -F "target_file=@target.mp4" \
  -F "quality=80" \
  -F "trim_start=0" \
  -F "trim_end=100"
```

### Pythonでの使用例

```python
import requests

# 画像Face Swap
with open('source.jpg', 'rb') as source, open('target.jpg', 'rb') as target:
    response = requests.post(
        'http://localhost:8000/face-swap/image',
        files={
            'source_file': source,
            'target_file': target
        },
        data={
            'quality': 90
        }
    )
    
result = response.json()
if result['success']:
    # ファイルダウンロード
    download_response = requests.get(
        f"http://localhost:8000/download/{result['output_filename']}"
    )
    with open('output.jpg', 'wb') as f:
        f.write(download_response.content)
```

## 🔧 開発・デバッグ

### ローカル開発

```bash
# 依存関係インストール
pip install -r requirements.txt

# API起動
cd api
python app/main.py
```

### ログ確認

```bash
# Dockerログ
docker-compose logs -f facefusion-api

# コンテナ内でのデバッグ
docker-compose exec facefusion-api bash
```

## 📁 プロジェクト構成

```
facefusion-test/
├── api/                    # FastAPI アプリケーション
│   ├── app/
│   │   └── main.py        # メインアプリケーション
│   ├── models/
│   │   └── schemas.py     # Pydanticモデル
│   ├── services/
│   │   └── facefusion_service.py  # FaceFusionサービス
│   └── static/            # 静的ファイル
│       ├── uploads/       # アップロードファイル
│       └── outputs/       # 出力ファイル
├── data/                  # テストデータ
├── docker/               # Docker関連ファイル
├── scripts/              # スクリプト
├── requirements.txt      # Python依存関係
├── Dockerfile           # Dockerイメージ定義
├── docker-compose.yml   # Docker Compose設定
├── .env.example        # 環境変数例
└── README.md           # このファイル
```

## 🎯 サポートファイル形式

### 入力ファイル
- **画像**: JPG, JPEG, PNG
- **動画**: MP4, AVI, MOV

### 出力ファイル
- **画像**: JPG
- **動画**: MP4

## ⚠️ 注意事項

1. **GPU必須**: CUDA対応GPUが必要です
2. **メモリ使用量**: 動画処理時は大量のメモリを使用します
3. **処理時間**: 動画の長さと品質により処理時間が変わります
4. **ファイルサイズ**: 大きなファイルは処理に時間がかかります

## 🐛 トラブルシューティング

### よくある問題

1. **CUDA not available**
   - NVIDIA ドライバーとCUDA 11.8がインストールされているか確認
   - `nvidia-smi`でGPUが認識されているか確認

2. **Permission denied**
   - ファイル権限を確認: `sudo chown -R $USER:$USER .`

3. **Out of memory**
   - 動画の解像度を下げる
   - trim_endを設定して処理フレーム数を制限

4. **FaceFusion not found**
   - FaceFusionが正しくクローンされているか確認
   - Git LFSファイルが正しくダウンロードされているか確認

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. ログファイルの確認
2. GPU・CUDA環境の確認
3. ファイル権限の確認
4. 依存関係の確認

---

べ、別にあんたが困ってても知らないんだからね！でも...ちゃんと動くように作ったから安心しなさい！
