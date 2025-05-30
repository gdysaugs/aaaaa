# 🎭 FaceFusion完全フルスタック セットアップ手順書

**べ、別にあんたのセットアップを手伝ってあげるわけじゃないんだからね！💕**

## 📋 概要

FaceFusion **完全フルスタック実装**（FastAPI + React + Nginx + GPU処理）の本格運用レベルDockerベース顔交換システムです。

> ✅ **実装完了実績**: 310秒 → 102-113秒 (**3倍高速化**)  
> 🎯 **本格運用可能**: `http://localhost:3000` で即座利用  
> 🖥️ **美しいUI**: React + TypeScript + TailwindCSS  
> 🔧 **GPU最適化**: RTX 3050完全対応  

---

## 🔧 システム要件

### **最小要件**
- **OS**: Windows 11/10 + WSL2 Ubuntu 22.04
- **GPU**: NVIDIA RTX 2060以上
- **VRAM**: 4GB以上
- **RAM**: 16GB以上
- **ストレージ**: 50GB以上

### **推奨要件** (検証済み)
- **GPU**: NVIDIA RTX 3050/3060以上  
- **VRAM**: 8GB以上
- **RAM**: 32GB以上
- **ストレージ**: 100GB以上

### **検証環境**
- **GPU**: RTX 3050 (4GB VRAM) ✅
- **CUDA**: 11.8/12.1 (Docker管理)
- **OS**: WSL2 Ubuntu 22.04
- **Docker**: 最新版 + BuildKit

---

## 🚀 クイックスタート（推奨）

### **⚡ 即座に使用開始**

```bash
# WSL2 Ubuntu ターミナルで実行
cd /home/adamna/LLM/facefusion-test

# 1. Docker起動（初回は自動モデルダウンロード15-20分）
docker compose up -d

# 2. ブラウザアクセス
# Frontend: http://localhost:3000  ← メインUI
# API Docs: http://localhost:8000/docs  ← Swagger UI

# 3. 停止
docker compose down
```

### **📊 動作確認**

```bash
# コンテナ状況確認
docker compose ps

# 期待される結果:
# facefusion-test-api-1       Up (healthy)    8000:8000
# facefusion-test-frontend-1  Up (healthy)    3000:3000

# GPU使用状況
nvidia-smi

# API ヘルスチェック
curl http://localhost:8000/health
# {"status":"healthy","gpu_available":true,"cuda_version":"12.1"}
```

---

## 🏗️ 詳細セットアップ

### **1. 前提条件確認**

```bash
# WSL2 + Ubuntu 22.04確認
lsb_release -a

# Docker + GPU確認  
docker --version
nvidia-smi
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu22.04 nvidia-smi
```

### **2. プロジェクト取得**

```bash
# リポジトリクローン
cd /home/$(whoami)
git clone https://github.com/gdysaugs/aaaaa.git
cd aaaaa/facefusion-test
```

### **3. 初回ビルド（推奨）**

```bash
# 完全クリーンビルド
docker compose down
docker compose build --no-cache

# 起動（初回はモデルダウンロードで15-20分）
docker compose up -d

# ログ監視（初回モデルダウンロード確認）
docker compose logs -f api
```

### **4. 初回モデルダウンロード確認**

```bash
# モデルダウンロード進行確認
docker compose logs api | grep -i "download"

# 完了までの目安:
# - inswapper_128.onnx: ~527MB
# - 1k3d68.onnx: ~43MB  
# - 2dfan4.onnx: ~271MB
# - ghost_unet.onnx: ~550MB
# 合計: 約1.4GB, 15-20分
```

---

## 🎮 使用方法

### **1. Web UI使用** (推奨)

1. **ブラウザアクセス**: `http://localhost:3000`
2. **ソース画像**: 交換元の顔画像をドラッグ&ドロップ
3. **ターゲット動画**: 交換先の動画をドラッグ&ドロップ
4. **設定調整**: 品質・フレーム範囲・AIモデル選択
5. **Face Swap実行**: ボタンクリックで処理開始
6. **リアルタイム監視**: 処理状況をリアルタイム表示
7. **結果取得**: 完了後ダウンロード・共有

### **2. API直接使用**

```bash
# Swagger UI
http://localhost:8000/docs

# CLI例: 動画顔交換
curl -X POST "http://localhost:8000/face-swap/video" \
  -F "source_file=@source.jpg" \
  -F "target_file=@target.mp4" \
  -F "quality=80" \
  -F "start_frame=0" \
  -F "end_frame=50"

# CLI例: 画像顔交換  
curl -X POST "http://localhost:8000/face-swap/image" \
  -F "source_file=@source.jpg" \
  -F "target_file=@target.jpg"
```

---

## 📁 プロジェクト構成

```
facefusion-test/
├── 🔧 api/                     # FastAPI バックエンド
│   ├── app/main.py            # API エンドポイント
│   ├── services/              # Face Swap処理サービス
│   └── static/                # アップロード・出力ファイル
├── 🖥️ frontend/                # React フロントエンド
│   ├── src/components/        # UI コンポーネント
│   ├── src/utils/api.ts       # API通信
│   ├── nginx.conf            # Nginx プロキシ設定
│   └── Dockerfile            # フロントエンドビルド
├── 🤖 facefusion/             # FaceFusion コア（GitSubmodule）
├── 📦 models/                 # AIモデル（自動ダウンロード）
├── 📁 data/                   # 入出力データ
│   ├── source/               # ソースファイル配置場所
│   └── output/               # 処理結果出力場所
├── 🐳 docker-compose.yml      # Docker構成設定
├── 🐳 Dockerfile             # API コンテナビルド
├── 📋 SETUP.md               # このセットアップ手順書
└── ⚙️ requirements.txt        # Python依存関係
```

---

## ⚙️ 設定詳細

### **ポート設定**
- **Frontend**: `3000` → 美しいWeb UI
- **API**: `8000` → RESTful API + Swagger
- **Internal**: Nginx プロキシで内部通信

### **ファイル制限**
- **最大サイズ**: 500MB
- **対応画像**: PNG, JPG, JPEG, GIF, BMP, WebP
- **対応動画**: MP4, AVI, MOV, WMV, FLV, WebM, MKV
- **タイムアウト**: 30分（大容量ファイル対応）

### **GPU最適化設定**
```bash
# 実際の最適化パラメータ
--execution-thread-count 8      # 8倍並列処理
--execution-queue-count 4       # 4倍キュー効率  
--execution-providers cuda      # CUDA最適化
--face-detector-size 640x640    # 高速検出
--system-memory-limit 8         # メモリ管理
```

---

## 📊 実測パフォーマンス (RTX 3050)

### **🎯 高速化実績**

| 項目 | Before | After | 改善率 |
|------|--------|-------|---------|
| **処理時間** | 310秒 | 102-113秒 | **3倍高速** |
| **GPU使用率** | 60-70% | 80-90% | **最適化** |
| **スレッド数** | 1 | 8 | **8倍並列** |
| **キュー数** | 1 | 4 | **4倍効率** |
| **VRAM使用** | 2GB | 2.5GB | **完全活用** |

### **🚀 処理例**
- **入力**: 50フレーム動画
- **出力**: 1.8MB MP4ファイル
- **所要時間**: 102-113秒
- **品質**: 80% (高品質設定)

---

## 🛠️ トラブルシューティング

### **よくある問題**

| 問題 | 症状 | 解決方法 |
|------|------|----------|
| **コンテナ起動失敗** | `docker compose ps` でDown | `docker compose logs` でエラー確認 |
| **GPU認識されない** | CUDA使用不可 | `nvidia-smi` + Docker再起動 |
| **モデルDL失敗** | 初回起動エラー | 15-20分待機、ネット環境確認 |
| **ポート競合** | アクセス不可 | `sudo netstat -tulpn \| grep :3000` |
| **メモリ不足** | OOM Killed | フレーム数を50以下に調整 |
| **アップロード失敗** | 413エラー | 500MB制限確認、形式確認 |
| **処理タイムアウト** | 504エラー | 30分制限、大容量ファイル分割 |

### **🔧 トラブル解決コマンド**

```bash
# 1. ログ確認
docker compose logs -f api
docker compose logs -f frontend

# 2. GPU状況確認
nvidia-smi
watch -n 1 nvidia-smi

# 3. 完全再起動
docker compose down
docker compose up -d

# 4. 完全再ビルド
docker compose down
docker compose build --no-cache
docker compose up -d

# 5. システムクリーンアップ
docker system prune -f
docker volume prune -f
```

### **🚨 緊急対応**

```bash
# すべてのコンテナ停止
docker stop $(docker ps -q)

# 不要リソース削除
docker system prune -af

# GPU状況リセット
sudo systemctl restart docker
```

---

## 🔄 メンテナンス

### **定期更新**

```bash
# 1. 最新コード取得
cd /home/adamna/LLM/facefusion-test
git pull origin main

# 2. 強制再ビルド
docker compose down
docker compose build --no-cache  
docker compose up -d
```

### **パフォーマンス監視**

```bash
# リアルタイム監視
watch -n 1 'echo "🎭 System Status 📊"; docker compose ps; echo ""; nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv'

# 処理ログ監視
docker compose logs -f api | grep -E "(Face Swap|処理時間|成功)"
```

---

## 🌟 高度な使用方法

### **バッチ処理**

```bash
# 複数ファイル処理スクリプト例
#!/bin/bash
for video in data/source/*.mp4; do
  curl -X POST "http://localhost:8000/face-swap/video" \
    -F "source_file=@data/source/face.jpg" \
    -F "target_file=@$video" \
    -F "quality=80"
done
```

### **API統合**

```python
# Python例
import requests

def face_swap_api(source_path, target_path):
    files = {
        'source_file': open(source_path, 'rb'),
        'target_file': open(target_path, 'rb')
    }
    data = {'quality': 80, 'start_frame': 0, 'end_frame': 50}
    
    response = requests.post(
        'http://localhost:8000/face-swap/video',
        files=files, 
        data=data
    )
    return response.json()
```

---

## 🛡️ セキュリティ & 運用

### **セキュリティ注意事項**
- ローカル環境専用設計
- 外部公開時は認証システム追加推奨
- ファイルスキャン推奨
- 定期的セキュリティ更新

### **運用ベストプラクティス**
- 定期バックアップ（data/ディレクトリ）
- ログローテーション設定
- モニタリング設定
- リソース使用量監視

---

## 📞 サポート

### **ドキュメント**
- 📋 **[README.md](README.md)**: プロジェクト概要
- 📸 **[GitHub](https://github.com/gdysaugs/aaaaa)**: ソースコード

### **お問い合わせ**
- 🐛 **バグ報告**: [GitHub Issues](https://github.com/gdysaugs/aaaaa/issues)
- 💡 **機能提案**: [GitHub Discussions](https://github.com/gdysaugs/aaaaa/discussions)

### **ログ収集手順**
1. `docker compose logs api > api.log 2>&1`
2. `docker compose logs frontend > frontend.log 2>&1`
3. `nvidia-smi > gpu.log`
4. Issue作成時にログファイル添付

---

**🎭 Happy AI Face Swapping!**  
**べ、別にセットアップが簡単になったから喜んでるわけじゃないんだからね！💕**

> **🌟 完成度**: 本格運用レベル  
> **⚡ 高速化**: 3倍の処理速度向上  
> **🖥️ UI**: 美しいReactフロントエンド  
> **🔧 技術**: 最新Docker + GPU最適化 