# FaceFusion API + Frontend セットアップ手順書

## 📋 概要

この手順書では、FaceFusion API（FastAPI + GPU処理）とReactフロントエンドを含む完全なDockerベースの顔交換システムのセットアップ方法を説明します。

## 🔧 必要な環境

### システム要件
- **OS**: Windows 11/10 + WSL2 Ubuntu 22.04
- **GPU**: NVIDIA RTX 2060以上（推奨: RTX 3050以上）
- **VRAM**: 4GB以上（推奨: 8GB以上）
- **RAM**: 16GB以上（推奨: 32GB以上）
- **ストレージ**: 20GB以上の空き容量

### 前提条件
- WSL2 + Ubuntu 22.04がインストール済み
- Docker Engine（WSL2内）がインストール済み
- NVIDIA Container Toolkit がインストール済み
- CUDA 11.8/12.1ドライバーがインストール済み

## 🚀 セットアップ手順

### 1. リポジトリのクローン

```bash
# WSL2 Ubuntu ターミナルで実行
cd /home/$(whoami)
git clone https://github.com/gdysaugs/aaaaa.git
cd aaaaa/facefusion-test
```

### 2. 環境の確認

```bash
# GPU確認
nvidia-smi

# Docker確認
docker --version
docker compose version

# NVIDIA Container Toolkit確認
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu22.04 nvidia-smi
```

### 3. Dockerイメージのビルド

```bash
# コンテナが動いている場合は停止
docker compose down

# キャッシュを使わずにビルド（推奨）
docker compose build --no-cache

# または通常ビルド
docker compose build
```

### 4. サービスの起動

```bash
# バックグラウンドで起動
docker compose up -d

# ログを確認しながら起動（デバッグ用）
docker compose up
```

### 5. 動作確認

#### API確認
```bash
# ヘルスチェック
curl http://localhost:8000/health

# 期待される結果:
# {"status":"healthy","gpu_available":true,"cuda_version":"12.1","gpu_memory_used":"17%"}
```

#### フロントエンド確認
```bash
# ブラウザでアクセス
# http://localhost:3000
```

### 6. コンテナ状況確認

```bash
# 実行中のコンテナ確認
docker compose ps

# 期待される結果:
# facefusion-api        Up (healthy)    8000:8000
# facefusion-frontend   Up (healthy)    3000:3000

# ログ確認
docker compose logs -f facefusion-api
docker compose logs -f facefusion-frontend
```

## 🎯 使用方法

### フロントエンド操作
1. ブラウザで `http://localhost:3000` にアクセス
2. **Source Image**: 交換元の顔画像をアップロード
3. **Target Video**: 交換先の動画をアップロード
4. **Process Video** ボタンをクリック
5. 処理完了後、結果動画をダウンロード

### API直接操作
```bash
# curlでの例
curl -X POST http://localhost:8000/face-swap \
  -F "source_image=@source.jpg" \
  -F "target_video=@target.mp4"
```

## 📁 プロジェクト構成

```
facefusion-test/
├── api/                        # FastAPIバックエンド
│   ├── app/
│   │   ├── main.py            # APIメイン
│   │   ├── services/          # サービス層
│   │   └── static/            # 静的ファイル
│   └── requirements.txt       # Python依存関係
├── facefusion-frontend/        # Reactフロントエンド
│   ├── src/
│   │   ├── components/        # UIコンポーネント
│   │   ├── services/          # API通信
│   │   └── App.tsx           # メインアプリ
│   ├── nginx.conf            # Nginx設定
│   ├── package.json          # Node.js依存関係
│   └── Dockerfile           # フロントエンドビルド
├── models/                   # FaceFusionモデル（自動ダウンロード）
├── data/                     # 入出力データ
│   ├── source/              # ソース画像
│   └── output/              # 出力動画
├── docker-compose.yml        # Docker Compose設定
├── Dockerfile               # APIコンテナビルド
└── README.md               # プロジェクト説明
```

## ⚙️ 設定詳細

### ポート設定
- **API**: 8000番ポート
- **Frontend**: 3000番ポート
- **Nginx Proxy**: フロントエンド内で3000番

### ファイルサイズ制限
- **最大アップロードサイズ**: 500MB
- **対応形式**: 
  - 画像: PNG, JPG, JPEG, GIF, BMP, WebP
  - 動画: MP4, AVI, MOV, WMV, FLV, WebM, MKV

### タイムアウト設定
- **API処理タイムアウト**: 30分
- **Nginx プロキシタイムアウト**: 30分
- **フロントエンド通信タイムアウト**: 30分

## 🔧 トラブルシューティング

### よくある問題と解決方法

#### 1. コンテナが起動しない
```bash
# ログ確認
docker compose logs

# GPU確認
nvidia-smi

# ポート競合確認
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :3000
```

#### 2. GPU認識されない
```bash
# NVIDIA Container Toolkit再インストール
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

#### 3. アップロードエラー (413 Request Entity Too Large)
```bash
# Nginx設定確認
docker compose logs facefusion-frontend | grep "413"

# 解決済み: client_max_body_size 500M に設定済み
```

#### 4. タイムアウトエラー (504 Gateway Time-out)
```bash
# 処理時間確認
docker compose logs facefusion-api | grep "Processing"

# 解決済み: 30分タイムアウトに設定済み
```

#### 5. NaN エラー（数値解析エラー）
```bash
# ブラウザコンソールでエラー確認
# 解決済み: react-dropzone accept属性を適切なオブジェクト形式に修正済み
```

### メンテナンスコマンド

```bash
# コンテナ再起動
docker compose restart

# 完全再ビルド
docker compose down
docker compose build --no-cache
docker compose up -d

# ログ監視
docker compose logs -f

# 不要なリソース削除
docker system prune -f
docker volume prune -f
```

## 📊 パフォーマンス指標

### 実績データ (RTX 3050 Laptop GPU)
- **処理時間**: 94秒
- **フレーム数**: 488フレーム  
- **フレームレート**: 約5.2 FPS
- **GPU使用率**: 約17%
- **VRAM使用量**: 約1.5GB

### 最適化のヒント
1. **バッチサイズ調整**: VRAMに応じて調整
2. **入力解像度**: 1080p推奨、4Kは処理時間増加
3. **動画長**: 長時間動画は分割処理推奨

## 🔄 アップデート手順

```bash
# 最新コード取得
git pull origin main

# 強制再ビルド
docker compose down
docker compose build --no-cache
docker compose up -d
```

## 🛡️ セキュリティ注意事項

- ローカル環境での使用を想定
- 外部公開する場合は認証機能の追加を推奨
- アップロードファイルのウイルススキャン推奨
- 定期的なセキュリティアップデート実施

## 📞 サポート

問題が発生した場合：

1. このドキュメントのトラブルシューティングを確認
2. ログファイルでエラー詳細を確認
3. GitHub Issuesで報告

---

**🎉 セットアップ完了！素晴らしい顔交換体験をお楽しみください！** 