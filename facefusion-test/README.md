# FaceFusion API

べ、別にあんたのためじゃないけど、ちゃんとしたFace Swap APIを作ってあげたわよ！

## 🎯 概要

FaceFusionをベースにしたFace Swap APIサービスです。画像と動画の顔交換処理をREST APIで提供します。

## 🚀 機能

- **画像Face Swap**: 画像の顔を別の画像の顔に交換
- **動画Face Swap**: 動画の顔を画像の顔に交換
- **ファイルアップロード**: 画像・動画ファイルのアップロード
- **ファイルダウンロード**: 処理済みファイルのダウンロード
- **Swagger UI**: インタラクティブなAPI文書（http://localhost:8000/）
- **CLI API**: コマンドライン形式での直接実行
- **ヘルスチェック**: API・GPU・FaceFusionの状態確認
- **システム情報**: GPU、CUDA、メモリなどの詳細情報

## 📋 必要な環境

- Ubuntu 22.04 (WSL2推奨)
- Python 3.10+
- CUDA 11.8
- Docker & Docker Compose
- NVIDIA GPU (RTX 3050以上推奨)

## 🛠️ インストール

### 1. リポジトリクローン

```bash
git clone <repository-url>
cd facefusion-test
```

### 2. 環境変数設定（オプション）

```bash
cp .env.example .env
# .envファイルを編集して環境に合わせて設定
```

### 3. Dockerビルド・起動

```bash
# ビルドキット使用でビルド
./docker_start.sh build

# サービス起動
./docker_start.sh start

# ログ確認
./docker_start.sh logs

# サービス停止
./docker_start.sh stop
```

### 4. ローカル開発環境

```bash
# 依存関係インストール
pip install -r requirements.txt

# ローカルAPI起動
python start_api_local.py

# APIテスト実行
python test_api_local.py
```

## 📚 API エンドポイント

### 🏠 メインエンドポイント

- **Swagger UI**: `GET /` - インタラクティブなAPI文書
- **ReDoc**: `GET /redoc` - API文書（代替）
- **CLI Help**: `GET /cli-help` - CLI使用方法ガイド

### 📊 情報取得

```http
# ヘルスチェック
GET /health

# システム情報
GET /system/info

# 利用可能モデル
GET /models

# API情報
GET /api
```

### 📤 ファイル操作

```http
# ファイルアップロード
POST /upload
Content-Type: multipart/form-data
Body: file=<画像または動画ファイル>

# ファイルダウンロード
GET /download/{filename}
```

### 🎭 Face Swap

#### 画像Face Swap
```http
POST /face-swap/image
Content-Type: multipart/form-data

Body:
- source_file: <ソース画像ファイル>
- target_file: <ターゲット画像ファイル>
- model: inswapper_128 (オプション)
- quality: 90 (オプション, 1-100)
- pixel_boost: 128x128 (オプション)
```

#### 動画Face Swap
```http
POST /face-swap/video
Content-Type: multipart/form-data

Body:
- source_file: <ソース画像ファイル>
- target_file: <ターゲット動画ファイル>
- model: inswapper_128 (オプション)
- quality: 80 (オプション, 1-100)
- pixel_boost: 128x128 (オプション)
- trim_start: 0 (オプション, 開始フレーム)
- trim_end: null (オプション, 終了フレーム)
- max_frames: 50 (オプション, 最大フレーム数)
```

### 🖥️ CLI API

```http
POST /cli/face-swap
Content-Type: application/json

Body:
{
  "source_path": "/app/data/source/source.jpg",
  "target_path": "/app/data/source/target.jpg",
  "output_path": "/app/data/output/result.jpg",
  "face_swapper_model": "inswapper_128",
  "output_image_quality": 90
}
```

## 🎮 使用例

### Web UI での使用

1. ブラウザで http://localhost:8000/ にアクセス
2. Swagger UIで各エンドポイントをテスト
3. 「Try it out」ボタンでインタラクティブにテスト可能

### cURLでの使用例

```bash
# ヘルスチェック
curl http://localhost:8000/health

# ファイルアップロード
curl -X POST http://localhost:8000/upload \
  -F "file=@source.jpg"

# 画像Face Swap
curl -X POST http://localhost:8000/face-swap/image \
  -F "source_file=@source.jpg" \
  -F "target_file=@target.jpg" \
  -F "quality=90" \
  -F "model=ghost_2_256"

# CLI形式でのFace Swap
curl -X POST http://localhost:8000/cli/face-swap \
  -H "Content-Type: application/json" \
  -d '{
    "source_path": "/app/data/source/source.jpg",
    "target_path": "/app/data/source/target.jpg",
    "output_path": "/app/data/output/result.jpg",
    "face_swapper_model": "ghost_2_256"
  }'
```

### Pythonでの使用例

```python
import requests

# システム情報取得
response = requests.get('http://localhost:8000/system/info')
print(response.json())

# 画像Face Swap
with open('source.jpg', 'rb') as source, open('target.jpg', 'rb') as target:
    response = requests.post(
        'http://localhost:8000/face-swap/image',
        files={
            'source_file': source,
            'target_file': target
        },
        data={
            'quality': 90,
            'model': 'ghost_2_256'
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

### Docker環境

```bash
# サービス状態確認
./docker_start.sh status

# リアルタイムログ監視
./docker_start.sh logs

# コンテナ内でのデバッグ
docker compose exec facefusion-api bash

# 環境クリーンアップ
./docker_start.sh cleanup
```

### ローカル開発

```bash
# API起動（開発モード）
python start_api_local.py

# テスト実行
python test_api_local.py

# 依存関係確認
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

## 📁 プロジェクト構成

```
facefusion-test/
├── api/                    # FastAPI アプリケーション
│   ├── app/
│   │   └── main.py        # メインアプリケーション
│   ├── services/
│   │   └── facefusion_service.py  # FaceFusionサービス
│   └── static/            # 静的ファイル
│       ├── uploads/       # アップロードファイル
│       └── outputs/       # 出力ファイル
├── models/                # Pydanticモデル
│   ├── __init__.py
│   └── schemas.py         # APIスキーマ定義
├── data/                  # データファイル
│   ├── source/           # ソースファイル
│   └── output/           # 出力ファイル
├── facefusion/           # FaceFusionライブラリ
├── logs/                 # ログファイル
├── scripts/              # 各種スクリプト
├── requirements.txt      # Python依存関係
├── Dockerfile           # Dockerイメージ定義
├── docker-compose.yml   # Docker Compose設定
├── docker_start.sh      # Docker管理スクリプト
├── start_api_local.py   # ローカルAPI起動
├── test_api_local.py    # APIテストスクリプト
└── README.md           # このファイル
```

## 🎯 サポートファイル形式

### 入力ファイル
- **画像**: JPG, JPEG, PNG
- **動画**: MP4, AVI, MOV

### 出力ファイル
- **画像**: JPG
- **動画**: MP4

## 🎨 利用可能モデル

| モデル名 | 説明 | 推奨用途 |
|---------|------|----------|
| `inswapper_128` | 高速・標準品質 | 一般用途 |
| `inswapper_128_fp16` | 高速・標準品質（FP16） | メモリ節約 |
| `ghost_2_256` | 最高品質 | 高品質処理（推奨） |
| `blendswap_256` | 自然な仕上がり | リアルな表現 |
| `simswap_256` | バランス型 | 汎用処理 |
| `uniface_256` | 統一顔型 | 特殊効果 |

## ⚠️ 注意事項

1. **GPU必須**: CUDA対応GPUが必要です
2. **メモリ使用量**: 動画処理時は大量のメモリを使用します
3. **処理時間**: 動画の長さと品質により処理時間が変わります
4. **ファイルサイズ制限**: アップロードは100MB、動画は最大200フレームに制限
5. **セキュリティ**: 本番環境では適切な認証・認可を実装してください

## 🐛 トラブルシューティング

### よくある問題

1. **CUDA not available**
   - NVIDIA ドライバーとCUDA 11.8がインストールされているか確認
   - `nvidia-smi`でGPUが認識されているか確認

2. **Permission denied**
   - ファイル権限を確認: `sudo chown -R $USER:$USER .`

3. **Out of memory**
   - 動画の解像度を下げる
   - `max_frames`を設定して処理フレーム数を制限

4. **FaceFusion not found**
   - FaceFusionが正しくクローンされているか確認
   - Git LFSファイルが正しくダウンロードされているか確認

5. **Docker build failed**
   - CUDAドライバーのバージョン確認
   - Dockerのリソース設定（メモリ・CPU）を増やす

### デバッグ手順

1. **環境確認**
   ```bash
   python start_api_local.py  # 環境チェック機能付き
   ```

2. **ログ確認**
   ```bash
   ./docker_start.sh logs     # Docker環境
   tail -f logs/facefusion.log  # ローカル環境
   ```

3. **リソース監視**
   ```bash
   ./docker_start.sh status   # Docker環境
   nvidia-smi                 # GPU使用状況
   ```

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. ログファイルの確認
2. GPU・CUDA環境の確認
3. ファイル権限の確認
4. 依存関係の確認

## 🌟 新機能

### v1.0.0で追加された機能
- ✨ **Swagger UI**: ルートパス（/）でアクセス可能
- 🖥️ **CLI API**: コマンドライン形式でのFace Swap実行
- 📊 **詳細なシステム情報**: GPU、CUDA、メモリ情報の取得
- 🎭 **モデル情報API**: 利用可能なモデルの詳細情報
- 🚀 **自動環境チェック**: 起動時の依存関係・GPU確認
- 📝 **包括的なログ**: 処理時間、モデル、品質の詳細ログ
- 🔒 **ファイルサイズ制限**: セキュリティ向上のための制限
- 🎨 **ピクセルブースト**: 高解像度処理オプション

---

べ、別にあんたが困ってても知らないんだからね！でも...ちゃんと動くように作ったから安心しなさい！

💡 **クイックスタート**: 
1. `./docker_start.sh build` 
2. `./docker_start.sh start`
3. ブラウザで http://localhost:8000/ にアクセス
