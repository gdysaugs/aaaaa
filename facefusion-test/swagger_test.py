#!/usr/bin/env python3
"""
Swagger UI テスト確認スクリプト
べ、別にあんたのためじゃないけど、Swagger UIが正常に動作するか確認してあげるわよ！
"""

import requests
import json
from pathlib import Path

def test_swagger_ui_access():
    """Swagger UIアクセステスト"""
    print("🌐 Swagger UIアクセステスト開始")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # 1. Swagger UIページ確認
    print("📄 Swagger UIページ確認...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Swagger UIアクセス成功")
            print(f"   URL: {base_url}/")
        else:
            print(f"❌ Swagger UIアクセス失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ Swagger UIアクセスエラー: {e}")
    
    # 2. OpenAPI仕様確認
    print("\n📋 OpenAPI仕様確認...")
    try:
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            spec = response.json()
            print("✅ OpenAPI仕様取得成功")
            print(f"   タイトル: {spec.get('info', {}).get('title')}")
            print(f"   バージョン: {spec.get('info', {}).get('version')}")
            print(f"   エンドポイント数: {len(spec.get('paths', {}))}")
            
            # エンドポイント一覧表示
            print("\n📍 利用可能なエンドポイント:")
            for path, methods in spec.get('paths', {}).items():
                for method in methods.keys():
                    if method.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
                        description = methods[method].get('summary', '')
                        print(f"   {method.upper():4} {path:25} - {description}")
        else:
            print(f"❌ OpenAPI仕様取得失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ OpenAPI仕様取得エラー: {e}")
    
    # 3. 主要エンドポイントの簡易テスト
    print("\n🔧 主要エンドポイント簡易テスト...")
    endpoints = [
        ("GET", "/health", "ヘルスチェック"),
        ("GET", "/api", "API情報"),
        ("GET", "/models", "モデル情報"),
        ("GET", "/system/info", "システム情報")
    ]
    
    for method, path, description in endpoints:
        try:
            response = requests.get(f"{base_url}{path}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {method} {path:15} - {description} ({response.status_code})")
        except Exception as e:
            print(f"   ❌ {method} {path:15} - {description} (ERROR)")

def create_swagger_usage_guide():
    """Swagger UI使用ガイド作成"""
    guide_content = """# 🎭 FaceFusion API Swagger UI 使用ガイド

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
"""
    
    guide_path = Path("swagger_usage_guide.md")
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"\n📝 使用ガイドを作成しました: {guide_path}")

def main():
    """メイン実行"""
    print("🎭 Swagger UI テスト確認")
    print("べ、別にあんたのためじゃないけど、確認してあげるわよ！\n")
    
    # Swagger UIアクセステスト
    test_swagger_ui_access()
    
    # 使用ガイド作成
    create_swagger_usage_guide()
    
    print("\n" + "=" * 60)
    print("🎉 Swagger UIテスト確認完了!")
    print("=" * 60)
    print("\n🌐 今すぐテストしてみる:")
    print("1. ブラウザで http://localhost:8000 にアクセス")
    print("2. POST /face-swap/video を展開")
    print("3. 'Try it out' をクリック")
    print("4. ファイルをアップロードして実行")
    print("\n📄 詳細な使用方法は swagger_usage_guide.md を参照してください")

if __name__ == "__main__":
    main() 