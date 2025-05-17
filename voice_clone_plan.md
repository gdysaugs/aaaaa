# 🐸 Coqui TTS ボイスクローン実装計画

## システム要件
- **WSL2**: Ubuntu環境 
- **Docker**: GPUサポート付き
- **GPU**: RTX 3050 (CUDA 11.8対応)
- **ボイスクローン**: XTTS v2モデルを使用

## 実装ステップ

### 1. WSL2環境の確認と準備
- Dockerのインストール確認
- GPU対応確認 (nvidia-smi)
- CUDA/cuDNNのバージョン確認

### 2. Dockerイメージの作成
- マルチステージビルド
- CUDA 11.8ベースイメージの使用
- Coqui TTSとその依存関係のインストール
- GPUサポートの設定

### 3. ボイスクローン用スクリプト
- コマンドライン引数対応
- 入力音声ファイルの処理
- クローン音声の生成
- 複数言語サポート

### 4. 使用予定のモデル
- `tts_models/multilingual/multi-dataset/xtts_v2` (最新のXTTSモデル)

## Docker構成

```dockerfile
# Stage 1: ビルドステージ
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 AS builder

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    git-lfs \
    # 省略...

# Stage 2: 実行ステージ
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 省略...
```

## 実装詳細

### CLI引数
- `--text`: 合成するテキスト
- `--speaker_wav`: クローン元の音声ファイル
- `--language`: 言語コード (en, ja, など)
- `--output`: 出力ファイルパス

### 実行方法

```bash
# Docker実行例
docker run --gpus all -v $(pwd):/app/data tts-voice-clone \
    --text "これはボイスクローンのテストです" \
    --speaker_wav /app/data/my_voice.wav \
    --language ja \
    --output /app/data/output.wav
```

## 技術的な注意点
- RTX 3050のVRAM制限に注意 (モデル選択)
- WSL2でのGPUパススルー設定確認
- Docker内でのCUDA可視化設定
- Pythonのバージョン互換性

## 開発ロードマップ
1. 環境構築 (WSL+Docker+GPU)
2. 依存関係の解決
3. 基本的なCLIスクリプト実装
4. テスト実行とデバッグ
5. パフォーマンス最適化 