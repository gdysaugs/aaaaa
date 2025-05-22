# AI Video Chat

リアルタイムでチャットするAI動画キャラクターを作成するプロジェクトです。

## 概要

このシステムは、以下のAI技術を組み合わせて、ユーザーのチャット入力から合成動画を自動生成するWebサービスです。

- **FaceFusion**: 動画の顔を入れ替える
- **llama-cpp-python**: チャット応答を生成する（大規模言語モデル）
- **CoquiTTS**: 音声合成（指定の声で応答を読み上げる）
- **Wav2Lip**: 音声に合わせて動画の口の動きを合成する

## セットアップ

### 前提条件

- Docker と Docker Compose
- NVIDIA GPU と CUDA 11.8 以上
- Git LFS

### インストール手順

1. リポジトリをクローン

```bash
git clone <repository-url>
cd ai-video-chat
```

2. 環境変数の設定

```bash
cp .env.example .env
# 必要に応じて.envを編集
```

3. モデルの配置

- llama-cpp-python用のモデル: `llama/models/model.gguf`を配置
- Wav2Lip用のモデル: `wav2lip/models/wav2lip_gan.pth`を配置

4. ビルドと起動

```bash
docker compose up -d
```

## 使用方法

1. ブラウザで `http://localhost:5173` にアクセス
2. 「素材を準備する」をクリック
3. 以下の素材をアップロードまたは選択:
   - 動画素材
   - 顔画像
   - 音声サンプル
4. 「チャットの準備をする」をクリック
5. チャット画面でメッセージを入力して会話開始

## システム構成

- **フロントエンド**: React, Vite, Tailwind CSS (ポート: 5173)
- **バックエンド**: FastAPI (ポート: 8000)
- **AI サービス**:
  - llama-cpp-python (ポート: 8001)
  - CoquiTTS (ポート: 8002)
  - FaceFusion (ポート: 8003)
  - Wav2Lip (ポート: 8004)

## 注意点

- GPUメモリの使用量が大きいため、十分なGPUメモリ(最低8GB以上推奨)が必要です
- 処理に時間がかかる場合があります
- 動画・画像の著作権に注意してください

## ライセンス

- このプロジェクトのコードはMITライセンスです
- 各AIライブラリは、それぞれのライセンスに従います
  - llama-cpp-python: MIT
  - FaceFusion: GPL-3.0
  - Wav2Lip: MIT
  - CoquiTTS: MPL-2.0

## トラブルシューティング

問題が発生した場合は、以下を試してください:

- コンテナログの確認: `docker compose logs -f サービス名`
- GPUの確認: `docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi`
- 十分なディスク容量があることを確認
- 各AIサービスの個別テストを実行 