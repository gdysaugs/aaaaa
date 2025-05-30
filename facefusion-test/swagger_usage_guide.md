# 🎭 FaceFusion API Swagger UI 使用ガイド

## 🌐 アクセス方法

ブラウザで以下のURLにアクセス:
```
http://localhost:8000
```

## 📋 主要エンドポイント

### 1. 基本情報
- `GET /health` - ヘルスチェック
- `GET /api` - API情報
- `GET /system/info` - システム情報
- `GET /models` - 利用可能なモデル

### 2. ファイル操作
- `POST /upload` - ファイルアップロード
- `GET /download/{filename}` - ファイルダウンロード

### 3. Face Swap
- `POST /face-swap/image` - 画像Face Swap
- `POST /face-swap/video` - 動画Face Swap（推奨）
- `POST /cli/face-swap` - CLI形式Face Swap

## 🎬 動画Face Swapの使用方法

### Swagger UIでのテスト手順:

1. **`POST /face-swap/video`** エンドポイントを展開
2. **"Try it out"** ボタンをクリック
3. パラメータを設定:
   - `source_file`: ソース画像をアップロード（顔を変換したい画像）
   - `target_file`: ターゲット動画をアップロード（変換対象の動画）
   - `model`: モデル選択（デフォルト: `inswapper_128`）
   - `quality`: 動画品質（1-100、デフォルト: 80）
   - `max_frames`: 最大フレーム数（デフォルト: 50）

4. **"Execute"** ボタンをクリック
5. 処理完了後、レスポンスで `output_filename` を確認
6. **`GET /download/{filename}`** で結果をダウンロード

### 利用可能なモデル:
- `inswapper_128` - 高速・標準品質（推奨）
- `ghost_2_256` - 最高品質
- `blendswap_256` - 自然な仕上がり

## 🖥️ CLI形式Face Swapの使用方法

### パラメータ例:
```json
{
  "source_path": "/app/data/source/source.jpg",
  "target_path": "/app/data/source/target.mp4", 
  "output_path": "/app/data/output/result.mp4",
  "face_swapper_model": "inswapper_128",
  "output_video_quality": 80,
  "trim_frame_start": 0,
  "trim_frame_end": 50
}
```

## 📁 ファイルパス

- **ソースファイル**: `/home/adamna/LLM/facefusion-test/data/source/`
- **出力ファイル**: `/home/adamna/LLM/facefusion-test/data/output/`
- **一時アップロード**: `/home/adamna/LLM/facefusion-test/api/static/uploads/`
- **API出力**: `/home/adamna/LLM/facefusion-test/api/static/outputs/`

## ⚠️ 注意事項

- 動画処理には時間がかかります（1-3分程度）
- ファイルサイズ制限: 500MB
- サポート形式:
  - 画像: JPG, JPEG, PNG
  - 動画: MP4, AVI, MOV
