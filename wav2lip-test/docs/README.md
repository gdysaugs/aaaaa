# Wav2Lip FastAPI 口パク動画生成API

## 概要

このプロジェクトは、Wav2Lipを使用して動画と音声から自然な口パク動画を生成するFastAPI RESTful APIです。DockerとGPUを活用して高品質な口パク動画を効率的に生成できます。

## 特徴

- 🎬 **高品質な口パク動画生成**: Wav2Lipモデルを使用した自然な口の動き
- 🚀 **FastAPI**: 高性能で使いやすいRESTful API
- 🐳 **Docker対応**: GPU対応のDockerコンテナで安定した処理環境
- 📊 **リアルタイム進捗**: 処理状況をリアルタイムで確認可能
- 🔧 **カスタマイズ可能**: パディング、バッチサイズなど詳細設定が可能
- 🧹 **自動クリーンアップ**: 一時ファイルの自動削除機能

## システム要件

### ハードウェア要件
- **GPU**: NVIDIA GPU (CUDA 11.8対応)
- **メモリ**: 8GB以上推奨
- **ストレージ**: 10GB以上の空き容量

### ソフトウェア要件
- **OS**: Ubuntu 20.04/22.04 (WSL2対応)
- **Docker**: Docker Engine with GPU support
- **Python**: 3.8以上
- **CUDA**: 11.8

## インストール

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd wav2lip-test
```

### 2. 必要なモデルファイルのダウンロード

#### s3fd.pth (顔検出モデル)
```bash
sudo mkdir -p models/face_detection/detection/sfd
sudo wget -O models/face_detection/detection/sfd/s3fd.pth \
  https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth
```

#### wav2lip.pth (メインモデル)
```bash
sudo wget -O models/wav2lip.pth \
  https://huggingface.co/numz/wav2lip_studio/resolve/main/Wav2lip/wav2lip.pth
```

### 3. Dockerイメージのビルド
```bash
cd docker
sudo docker build --build-arg BUILDKIT_INLINE_CACHE=1 -t wav2lip-gpu .
```

### 4. Python依存関係のインストール
```bash
pip install -r requirements.txt
```

### 5. 環境変数の設定
```bash
cp .env.example .env
# 必要に応じて .env ファイルを編集
```

## 使用方法

### APIサーバーの起動
```bash
python start_api.py
```

サーバーは `http://localhost:8000` で起動します。

### API ドキュメント
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 基本的な使用例

#### 1. 動画処理の開始
```bash
curl -X POST "http://localhost:8000/process" \
  -H "Content-Type: multipart/form-data" \
  -F "video=@input_video.mp4" \
  -F "audio=@input_audio.wav" \
  -F "pads=0,10,0,0" \
  -F "quality=high"
```

レスポンス:
```json
{
  "job_id": "uuid-string",
  "status": "processing",
  "message": "処理を開始しました"
}
```

#### 2. 処理状況の確認
```bash
curl "http://localhost:8000/status/{job_id}"
```

レスポンス:
```json
{
  "status": "processing",
  "progress": 75,
  "message": "Wav2Lip推論実行中...",
  "output_path": null,
  "processing_time": null
}
```

#### 3. 結果のダウンロード
```bash
curl -O "http://localhost:8000/download/{job_id}"
```

#### 4. ジョブのクリーンアップ
```bash
curl -X DELETE "http://localhost:8000/cleanup/{job_id}"
```

## API エンドポイント

### GET /
ヘルスチェック

### GET /health
詳細なヘルスチェック（モデル読み込み状況、GPU利用可能性）

### POST /process
動画処理の開始

**パラメータ:**
- `video`: 動画ファイル (.mp4, .avi)
- `audio`: 音声ファイル (.wav, .mp3)
- `pads`: パディング設定 (デフォルト: "0,10,0,0")
- `face_det_batch_size`: 顔検出バッチサイズ (デフォルト: 1)
- `wav2lip_batch_size`: Wav2Lipバッチサイズ (デフォルト: 4)
- `resize_factor`: リサイズ係数 (デフォルト: 1)
- `quality`: 品質設定 (low/medium/high, デフォルト: high)

### GET /status/{job_id}
処理状況の取得

### GET /download/{job_id}
結果動画のダウンロード

### DELETE /cleanup/{job_id}
ジョブのクリーンアップ

## 設定

### 環境変数

| 変数名 | デフォルト値 | 説明 |
|--------|-------------|------|
| HOST | 0.0.0.0 | サーバーホスト |
| PORT | 8000 | サーバーポート |
| DEBUG | False | デバッグモード |
| LOG_LEVEL | INFO | ログレベル |
| MAX_FILE_SIZE | 524288000 | 最大ファイルサイズ（バイト） |
| MAX_CONCURRENT_JOBS | 5 | 同時処理可能ジョブ数 |

### パラメータ調整のコツ

#### pads (パディング)
- 形式: "上,下,左,右"
- 例: "0,10,0,0" (下に10ピクセルのパディング)
- 顔の検出範囲を調整し、あごの領域を含めることで品質向上

#### face_det_batch_size
- 小さい値: 精度向上、処理時間増加
- 大きい値: 処理速度向上、メモリ使用量増加

#### wav2lip_batch_size
- GPUメモリに応じて調整
- RTX 3050の場合: 4-8が推奨

#### resize_factor
- 1: 元解像度
- 2以上: 解像度を下げて処理速度向上

## トラブルシューティング

### よくある問題

#### 1. GPU が認識されない
```bash
# NVIDIA ドライバーの確認
nvidia-smi

# Docker GPU サポートの確認
sudo docker run --gpus all nvidia/cuda:11.8-base nvidia-smi
```

#### 2. モデルファイルが見つからない
```bash
# モデルファイルの存在確認
ls -la models/wav2lip.pth
ls -la models/face_detection/detection/sfd/s3fd.pth
```

#### 3. メモリ不足エラー
- `wav2lip_batch_size` を小さくする
- `resize_factor` を大きくして解像度を下げる

#### 4. 処理が遅い
- GPU が正しく使用されているか確認
- バッチサイズを調整
- 入力動画の解像度を下げる

### ログの確認
```bash
# APIサーバーのログ
tail -f wav2lip_api.log

# Dockerコンテナのログ
sudo docker logs <container_id>
```

## 開発

### 開発環境のセットアップ
```bash
# 開発用依存関係のインストール
pip install -r requirements.txt

# コードフォーマット
black .

# リンター
flake8 .

# テスト実行
pytest
```

### プロジェクト構造
```
wav2lip-test/
├── api/                    # FastAPI アプリケーション
│   └── main.py
├── src/                    # ソースコード
│   ├── models.py          # Pydantic モデル
│   └── wav2lip_service.py # Wav2Lip サービス
├── config/                 # 設定ファイル
│   └── settings.py
├── docs/                   # ドキュメント
│   └── README.md
├── docker/                 # Docker 関連
│   ├── Dockerfile
│   └── requirements.txt
├── models/                 # モデルファイル
├── data/                   # データディレクトリ
├── temp/                   # 一時ファイル
├── requirements.txt        # Python 依存関係
├── start_api.py           # API サーバー起動スクリプト
└── .env.example           # 環境変数サンプル
```

## ライセンス

このプロジェクトは研究・個人利用のみを目的としています。商用利用については、Wav2Lipの公式ライセンスを確認してください。

## 参考文献

- [Wav2Lip: Accurately Lip-syncing Videos In The Wild](https://github.com/Rudrabha/Wav2Lip)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker GPU Support](https://docs.docker.com/config/containers/resource_constraints/#gpu)

## サポート

問題が発生した場合は、以下を確認してください：

1. システム要件を満たしているか
2. モデルファイルが正しくダウンロードされているか
3. GPU ドライバーが正しくインストールされているか
4. Docker GPU サポートが有効になっているか

詳細なエラーログと共にIssueを作成してください。 