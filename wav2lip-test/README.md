# Wav2Lip CLIテスト用GPU Docker環境

## 構成
- CUDA 11.8, cuDNN, PyTorch (GPU)
- Wav2Lip公式リポジトリ
- 依存パッケージはrequirements.txt管理
- モデル・データは`models/`・`data/input/`に配置

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

# 4. テスト用動画・音声を data/input/ に配置

# 5. コンテナ起動
sudo docker run --gpus all -it --rm \
  -v ~/aaaaa/wav2lip-test/data:/workspace/data \
  -v ~/aaaaa/wav2lip-test/models:/workspace/models \
  -v ~/aaaaa/wav2lip-test/scripts:/workspace/scripts \
  wav2lip-gpu /bin/bash

# 6. CLIテスト
cd /workspace/scripts
bash run_wav2lip.sh
```

## 注意
- 商用利用禁止（公式ライセンス参照）
- CUDA11.8, GPU必須
- Docker Desktopは使わずWSL2+Ubuntuで構築
