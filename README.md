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

**🎯 FaceFusion詳細**: [facefusion-test/SETUP.md](./facefusion-test/SETUP.md)

### 3. ⚡ 一括構築（推奨）
```bash
chmod +x build_all.sh
./build_all.sh
```

## 🎯 搭載プロジェクト

### 📸 FaceFusion (顔交換) - **完全実装済み**
- **機能**: 動画内の顔を指定した顔に交換
- **アーキテクチャ**: FastAPI + React + Nginx + Docker
- **GPU加速**: CUDA 11.8/12.1対応
- **⚡ 高速化実績**: 310秒 → 102秒 (**3倍高速化！**)
- **最適化**: スレッド8個・キュー4個・GPU直接制御
- **UI**: 美しいReactフロントエンド（ツンデレ風）
- **API**: RESTful API、500MBファイル対応、30分タイムアウト
- **ステータス**: ✅ **本格運用可能**

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

### ✅ FaceFusion 完全実装成功
```bash
🎉 フルスタック実装完了！
🖥️  Frontend: React + TypeScript + Tailwind CSS
🔧 Backend: FastAPI + GPU処理
🌐 Proxy: Nginx (500MB対応、30分タイムアウト)
⚡ 高速化: 310秒 → 102秒 (3倍高速化！)
🚀 最適化: スレッド数8・キュー数4・GPU最適化
📊 処理性能: 50フレーム/102秒 (RTX 3050)
🎯 GPU使用率: 80-90% (最適化後)
🌐 運用: http://localhost:3000 で本格利用可能
```

## 🔧 技術スタック

### 基盤環境
- **OS**: WSL2 Ubuntu 22.04
- **コンテナ**: Docker + Docker Compose
- **GPU**: NVIDIA RTX 3050 (4GB VRAM)
- **CUDA**: 11.8/12.1 (Docker管理)

### FaceFusion フルスタック
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI + Uvicorn + FaceFusion 3.2.0
- **Proxy**: Nginx (リバースプロキシ)
- **AI/ML**: PyTorch 2.6.0 + ONNX Runtime GPU
- **Processing**: GPU加速顔交換処理

### 開発ツール
- **ビルドシステム**: Docker BuildKit + マルチステージビルド
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
5. **ファイルアップロードエラー** → 500MB制限確認
6. **タイムアウトエラー** → 30分設定確認

詳細は **[📋 SETUP.md](./SETUP.md)** および **[facefusion-test/SETUP.md](./facefusion-test/SETUP.md)** を参照してください。

## 📁 ディレクトリ構成

```
aaaaa/
├── 📸 facefusion-test/         # 🎯 完全実装済み顔交換プロジェクト
│   ├── api/                   # FastAPIバックエンド
│   ├── facefusion-frontend/   # React + Nginx フロントエンド
│   ├── models/                # FaceFusionモデル（自動DL）
│   ├── data/                  # 入出力データ（Git除外）
│   ├── docker-compose.yml     # 本格運用設定
│   ├── Dockerfile             # APIコンテナ
│   └── SETUP.md              # 完全セットアップ手順
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
├── 📋 SETUP.md                # 全体セットアップ手順書
├── ⚡ build_all.sh            # 一括構築スクリプト
└── 🚫 .gitignore              # 大きなファイル除外設定
```

## 🔄 開発ワークフロー

### 新規環境セットアップ
1. リポジトリクローン
2. `./build_all.sh` 実行（全体）or `cd facefusion-test && docker compose up -d`（個別）
3. モデルファイルダウンロード（自動）
4. テスト実行

### 開発時の注意
- **大きなファイルはコミット禁止**（.gitignoreで保護済み）
- **ポート競合に注意**（各プロジェクト専用ポート割り当て済み）
- **GPU使用量監視**（4GB VRAM制限に注意）

## 🎉 プロジェクト実績

- ✅ **FaceFusion**: **完全フルスタック実装成功**（API + Frontend + GPU処理）
- ⚡ **高速化達成**: **310秒→102秒の3倍高速化**（スレッド・キュー・GPU最適化）
- ✅ **React Frontend**: 美しいUI、500MBファイル対応、エラーハンドリング完備
- ✅ **FastAPI Backend**: RESTful API、GPU加速、30分タイムアウト対応
- ✅ **Docker化**: 本格運用レベルのコンテナ構成
- 🔧 **GPT-SoVITS v4**: 高品質音声合成実装
- 🔧 **Wav2Lip**: リップシンク処理実装
- 🔧 **LLaMA-cpp**: LLM推論システム構築
- 📦 **完全Docker化**: 環境依存性解決

## 📞 サポート

問題が発生した場合：

1. **[📋 SETUP.md](./SETUP.md)** のトラブルシューティング確認
2. **[facefusion-test/SETUP.md](./facefusion-test/SETUP.md)** のFaceFusion専用手順確認
3. ログファイル確認 (`docker logs コンテナ名`)
4. GPU状況確認 (`nvidia-smi`)
5. 必要に応じてIssue作成

---

**🚀 Happy AI Development!** 