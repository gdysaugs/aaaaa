# Wav2Lip CLIテスト用GPU Docker環境 + FastAPI CLIラッパー

## 構成
- CUDA 11.8, cuDNN, PyTorch (GPU)
- Wav2Lip公式リポジトリ
- 依存パッケージはrequirements.txt管理
- モデル・データは`models/`・`data/input/`に配置
- **NEW**: CLIで成功したコマンドをそのまま関数化したFastAPI

## 新機能: CLIラッパー版 FastAPI

CLIで成功したWav2Lipコマンドをそのまま関数化し、FastAPIで呼び出せるようになりました！

### 主な特徴
- ✅ CLIで成功したコマンドをそのまま使用
- ✅ パディング設定はスペース区切り（例: `0 10 0 0`）
- ✅ 非同期処理でバックグラウンド実行
- ✅ 処理状況のリアルタイム監視
- ✅ ファイルアップロード・ダウンロード対応

### API使用方法

```bash
# 1. APIサーバー起動
python3 start_api.py

# 2. ブラウザでSwagger UI確認
# http://localhost:8000/docs

# 3. API呼び出し例
curl -X POST "http://localhost:8000/process" \
  -F "video=@data/input/video.mp4" \
  -F "audio=@data/input/audio.wav" \
  -F "pads=0 10 0 0" \
  -F "face_det_batch_size=1" \
  -F "wav2lip_batch_size=4"
```

### CLIラッパーテスト

```bash
# CLIラッパーの動作テスト
python3 test_cli_wrapper.py
```

## セットアップ手順

```bash
# 1. ディレクトリ作成
sudo mkdir -p ~/aaaaa/wav2lip-test/{docker,scripts,data/input,data/output,models}

# 2. Dockerイメージビルド
cd ~/aaaaa/wav2lip-test/docker
sudo docker build -t wav2lip-gpu .

# 3. モデルDL（Google Driveから手動DL推奨）
#   - Wav2Lip: https://drive.google.com/drive/folders/153HLrqlBNxzZcHi17PEvP09kkAfzRshM?usp=share_link
#   - models/wav2lip.pth に配置
#   - models/face_detection/detection/sfd/s3fd.pth に配置

# 4. テスト用動画・音声を data/input/ に配置

# 5. CLIテスト（従来通り）
sudo docker run --gpus all -it --rm \
  -v ~/aaaaa/wav2lip-test/data:/workspace/data \
  -v ~/aaaaa/wav2lip-test/models:/workspace/models \
  -v ~/aaaaa/wav2lip-test/scripts:/workspace/scripts \
  wav2lip-gpu /bin/bash

# 6. FastAPI起動（新機能）
python3 start_api.py
```

## API エンドポイント

| エンドポイント | メソッド | 説明 |
|---------------|---------|------|
| `/` | GET | ヘルスチェック |
| `/health` | GET | 詳細なヘルスチェック |
| `/process` | POST | 動画処理開始 |
| `/status/{job_id}` | GET | 処理状況確認 |
| `/download/{job_id}` | GET | 結果ダウンロード |
| `/cleanup/{job_id}` | DELETE | ジョブクリーンアップ |
| `/models/info` | GET | モデル情報取得 |

## パラメータ設定

### パディング設定（重要！）
- **形式**: スペース区切り（例: `0 10 0 0`）
- **順序**: 上 下 左 右
- **CLIで成功した設定**: `0 10 0 0`

### その他のパラメータ
- `face_det_batch_size`: 顔検出バッチサイズ（デフォルト: 1）
- `wav2lip_batch_size`: Wav2Lipバッチサイズ（デフォルト: 4）
- `resize_factor`: リサイズ係数（デフォルト: 1）

## 注意
- 商用利用禁止（公式ライセンス参照）
- CUDA11.8, GPU必須
- Docker Desktopは使わずWSL2+Ubuntuで構築
- パディング設定は必ずスペース区切りで指定
