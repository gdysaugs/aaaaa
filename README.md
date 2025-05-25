# 🎯 AI開発プラットフォーム Collection

WSL2 + Docker + GPU環境でのAI開発プロジェクト集です。

## 🚀 クイックスタート

### 1. 🔄 リポジトリクローン
```bash
git clone https://github.com/gdysaugs/aaaaa.git
cd aaaaa
```

### 2. 📖 詳細セットアップ
**[📋 SETUP.md](./SETUP.md) を参照してください**

### 3. ⚡ 一括構築（推奨）
```bash
chmod +x build_all.sh
./build_all.sh
```

## 🎯 搭載プロジェクト

### 📸 FaceFusion (顔交換)
- **機能**: 動画内の顔を指定した顔に交換
- **GPU加速**: CUDA 11.8対応
- **性能**: RTX 3050で94秒/488フレーム
- **ステータス**: ✅ 動作確認済み

### 🎤 GPT-SoVITS v4 (音声合成)
- **機能**: テキストから自然な音声生成
- **多言語対応**: 日本語、英語、中国語
- **品質**: 高品質音声合成
- **ステータス**: 🔧 構築済み

### 👄 Wav2Lip (リップシンク)
- **機能**: 音声に合わせて動画の口の動きを調整
- **用途**: 音声と映像の同期
- **処理**: GPU加速対応
- **ステータス**: 🔧 構築済み

### 🦙 LLaMA-cpp-cli (LLM推論)
- **機能**: 大規模言語モデルの推論
- **対応形式**: GGUF、GGML
- **最適化**: CPU/GPU両対応
- **ステータス**: 🔧 構築済み

### 🔧 MCP-for-Cursor (開発統合)
- **機能**: Cursor IDEとの統合
- **用途**: 開発効率化
- **ステータス**: 🔧 構築済み

## 🎯 成功実績

### ✅ FaceFusion テスト結果
```bash
🎉 成功！
📊 処理時間: 94秒
🖼️  フレーム数: 488フレーム
⚡ GPU: RTX 3050 (CUDA 11.8)
📈 フレームレート: 約5.2 FPS
```

## 🔧 技術スタック

### 基盤環境
- **OS**: WSL2 Ubuntu 22.04
- **コンテナ**: Docker + Docker Compose
- **GPU**: NVIDIA RTX 3050 (4GB VRAM)
- **CUDA**: 11.8 (Docker管理)

### AI/ML フレームワーク
- **PyTorch**: 2.0.1 / 2.6.0
- **ONNX Runtime**: GPU版
- **FaceFusion**: 3.2.0
- **LLaMA.cpp**: 最新版

### 開発ツール
- **ビルドシステム**: Docker BuildKit
- **プロジェクト管理**: Git + GitHub
- **IDE統合**: Cursor MCP

## 📊 動作要件

### 最小要件
- **GPU**: NVIDIA RTX 2060以上
- **VRAM**: 4GB以上
- **RAM**: 16GB以上
- **ストレージ**: 50GB以上の空き容量

### 推奨要件  
- **GPU**: NVIDIA RTX 3050/3060以上
- **VRAM**: 8GB以上
- **RAM**: 32GB以上
- **ストレージ**: 100GB以上の空き容量

## 🔍 トラブルシューティング

### よくある問題
1. **GPU認識されない** → `nvidia-smi` で確認
2. **モデル不足エラー** → SETUP.mdのダウンロード手順実行
3. **ポート競合** → docker-compose.ymlのポート変更
4. **メモリ不足** → バッチサイズを調整

詳細は **[📋 SETUP.md](./SETUP.md)** を参照してください。

## 📁 ディレクトリ構成

```
aaaaa/
├── 📸 facefusion-test/         # 顔交換プロジェクト
│   ├── docker/                # Docker設定
│   ├── data/                  # テストデータ（Git除外）
│   └── *.py                   # テストスクリプト
├── 🎤 gpt-sovits-v4-cli-test/ # 音声合成プロジェクト  
│   ├── pretrained_models/     # モデル（Git除外）
│   └── *.py                   # CLIスクリプト
├── 👄 wav2lip-test/           # リップシンクプロジェクト
│   ├── models/                # モデル（Git除外）
│   └── docker/                # Docker設定
├── 🦙 llama-cpp-cli-test/     # LLM推論プロジェクト
│   ├── models/                # モデル（Git除外）
│   └── llama-cpp-python/      # LLaMA.cpp統合
├── 🔧 mcp-for-cursor/         # Cursor統合
├── 📋 SETUP.md                # セットアップ手順書
├── ⚡ build_all.sh            # 一括構築スクリプト
└── 🚫 .gitignore              # 大きなファイル除外設定
```

## 🔄 開発ワークフロー

### 新規環境セットアップ
1. リポジトリクローン
2. `./build_all.sh` 実行
3. モデルファイルダウンロード
4. テスト実行

### 開発時の注意
- **大きなファイルはコミット禁止**（.gitignoreで保護済み）
- **ポート競合に注意**（各プロジェクト専用ポート割り当て済み）
- **GPU使用量監視**（4GB VRAM制限に注意）

## 🎉 プロジェクト実績

- ✅ **FaceFusion**: 動画顔交換成功（GPU加速）
- 🔧 **GPT-SoVITS v4**: 高品質音声合成実装
- 🔧 **Wav2Lip**: リップシンク処理実装
- 🔧 **LLaMA-cpp**: LLM推論システム構築
- 📦 **完全Docker化**: 環境依存性解決

## 📞 サポート

問題が発生した場合：

1. **[📋 SETUP.md](./SETUP.md)** のトラブルシューティング確認
2. ログファイル確認 (`docker logs コンテナ名`)
3. GPU状況確認 (`nvidia-smi`)
4. 必要に応じてIssue作成

---

**🚀 Happy AI Development!** 