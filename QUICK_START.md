# ⚡ AI開発プラットフォーム - クイックスタートガイド

**他のPCでクローンした時の最短手順**で4つのAIライブラリのFastAPIを全て起動する方法です。

## 🚀 30分で完全セットアップ

### 1️⃣ 前提条件確認（5分）
```bash
# GPU確認
nvidia-smi

# Docker確認
docker --version
docker compose version

# WSL2のGPU確認
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi
```

### 2️⃣ リポジトリクローン（2分）
```bash
# WSL2のLinuxファイルシステム内にクローン（重要！）
cd /home/$USER
git clone https://github.com/gdysaugs/aaaaa.git
cd aaaaa
```

### 3️⃣ モデルファイル自動ダウンロード（15分）
```bash
# GPT-SoVITS v4 モデル（必須・約2.6GB）
cd gpt-sovits-v4-cli-test
./download_models.sh
cd ..

# Wav2Lip モデル（必須・約500MB）
cd wav2lip-test
wget -O models/wav2lip.pth "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/wav2lip.pth"
wget -O models/face_detection/detection/sfd/s3fd.pth "https://github.com/Rudrabha/Wav2Lip/releases/download/v1.0/s3fd.pth"
cd ..
```

### 4️⃣ 全FastAPI一括起動（5分）
```bash
# 一括起動スクリプト実行
./start_all_apis.sh
```

### 5️⃣ 動作確認（3分）
```bash
# ヘルスチェック実行
./health_check.sh
```

## 🎯 起動完了！

### 📊 利用可能なサービス
| サービス | URL | 機能 |
|---------|-----|------|
| 📸 **FaceFusion** | `http://localhost:7862` | 顔交換・顔スワップ |
| 🎤 **GPT-SoVITS v4** | `http://localhost:8000` | 音声合成・ボイスクローン |
| 👄 **Wav2Lip** | `http://localhost:8001` | リップシンク・口パク |
| 🦙 **LLaMA-cpp** | `http://localhost:8002` | LLM推論・テキスト生成 |

### 🧪 簡単テスト
```bash
# 全サービスのヘルスチェック
curl http://localhost:7862/health  # FaceFusion
curl http://localhost:8000/health  # GPT-SoVITS
curl http://localhost:8001/health  # Wav2Lip
curl http://localhost:8002/health  # LLaMA-cpp

# GPU状況確認
curl http://localhost:8000/gpu-status
```

## 🛠️ トラブルシューティング

### ❌ よくあるエラーと解決法

#### 1. モデルファイル不足
```bash
# GPT-SoVITS v4 モデル再ダウンロード
cd gpt-sovits-v4-cli-test && ./download_models.sh
```

#### 2. GPU認識されない
```bash
# WSL2のGPU設定確認
wsl.exe --update
# Windows側でNVIDIAドライバを最新に更新
```

#### 3. ポート競合
```bash
# 使用中ポート確認・停止
./stop_all_apis.sh
./start_all_apis.sh
```

#### 4. 権限エラー
```bash
sudo chown -R $USER:$USER .
chmod +x *.sh
```

## 📝 管理コマンド

### 🚀 起動・停止
```bash
./start_all_apis.sh    # 全サービス起動
./stop_all_apis.sh     # 全サービス停止
./health_check.sh      # ヘルスチェック
```

### 📊 ログ確認
```bash
# 各サービスのログ
docker logs facefusion-api
docker logs gpt-sovits-v4-api
docker logs wav2lip-api
docker logs llama-cpp-api

# FastAPIラッパーのログ
tail -f gpt-sovits-v4-cli-test/fastapi.log
```

### 🎮 GPU監視
```bash
# GPU使用状況
nvidia-smi

# 各コンテナのGPU確認
docker exec facefusion-api nvidia-smi
docker exec gpt-sovits-v4-api nvidia-smi
```

## 🎉 完了！

**🚀 これで4つのAIライブラリのFastAPIが全て利用可能になりました！**

詳細な設定や高度な使用方法は `SETUP.md` を参照してください。

---

## 📞 サポート

- 📖 **詳細ガイド**: `SETUP.md`
- 🔧 **トラブルシューティング**: `SETUP.md` のトラブルシューティング章
- 🌐 **GitHub**: https://github.com/gdysaugs/aaaaa 