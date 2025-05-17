# 🐸 Coqui TTS ボイスクローン

WSL2とDockerを使用して、Coqui TTSでボイスクローンを行うためのプロジェクトです。

## 前提条件

- WSL2 (Ubuntu)
- Docker with GPU support
- NVIDIA GPU (RTX 3050で動作確認済み)
- CUDA 11.8
- 音声サンプル (WAVファイル)

## セットアップ

1. このリポジトリをクローンまたはダウンロード
2. クローンしたい声のサンプル音声(WAVファイル)を `samples/voice.wav` として保存
   - 音声は5〜30秒程度、クリアな発話のものが良い
   - 16kHzのモノラルWAVファイルを推奨

## 使い方

### シェルスクリプトで実行

```bash
# デフォルト設定で実行（日本語）
./run_voice_clone.sh

# カスタムテキストで実行
./run_voice_clone.sh "こんにちは、これはボイスクローンのテストです。"

# 英語で実行
./run_voice_clone.sh "Hello, this is a voice cloning test." en
```

### Docker Composeで実行

```bash
# Docker Composeでビルドと実行
docker compose up --build
```

## ファイル構成

- `Dockerfile`: TTSをインストールするためのDockerfile
- `docker-compose.yml`: Docker Compose設定ファイル
- `voice_clone.py`: ボイスクローン用Pythonスクリプト
- `run_voice_clone.sh`: 簡単に実行するためのシェルスクリプト
- `samples/`: 入力音声を保存するディレクトリ
- `output/`: 生成された音声を保存するディレクトリ

## 注意点

- 初回実行時はモデルのダウンロードが行われるため、時間がかかります
- RTX 3050は4GB VRAMのため、大きなモデルは実行できない可能性があります
- 必要に応じて `voice_clone.py` の `--model` オプションで別のモデルを指定できます
- WSL2でGPUを使用するには、ホストマシンに適切なNVIDIAドライバがインストールされている必要があります

## トラブルシューティング

### GPUが認識されない場合

```bash
# Docker内でGPUが認識されているか確認
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### 音声生成に失敗する場合

- 入力音声ファイルのフォーマットを確認（WAV、16kHz推奨）
- 非常に短い音声や品質の悪い音声は避ける
- 使用するモデルを変更してみる（`--model` オプション）

## モデルオプション

- `tts_models/multilingual/multi-dataset/xtts_v2`: 最新のXTTSモデル (デフォルト)
- `tts_models/multilingual/multi-dataset/your_tts`: YourTTSモデル
- その他のモデルは `tts.list_models()` で確認できます

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
使用するCoqui TTSはMPL-2.0ライセンスです。 