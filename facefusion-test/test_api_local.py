#!/usr/bin/env python3
"""
FaceFusion API Local Test Script
べ、別にあんたのためじゃないけど、ちゃんとテストスクリプトを作ってあげるわよ！
"""
import requests
import json
import time
from pathlib import Path

# API設定
BASE_URL = "http://localhost:8000"

def test_health_check():
    """ヘルスチェックテスト"""
    print("🏥 ヘルスチェック中...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ ヘルスチェック失敗: {e}")
        return False

def test_system_info():
    """システム情報テスト"""
    print("\n💻 システム情報取得中...")
    try:
        response = requests.get(f"{BASE_URL}/system/info")
        print(f"ステータス: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"プラットフォーム: {data.get('platform')}")
            print(f"Python: {data.get('python_version')}")
            print(f"PyTorch: {data.get('torch_version')}")
            print(f"CUDA利用可能: {data.get('cuda_available')}")
            print(f"GPU数: {data.get('gpu_count')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ システム情報取得失敗: {e}")
        return False

def test_models_info():
    """モデル情報テスト"""
    print("\n🎭 モデル情報取得中...")
    try:
        response = requests.get(f"{BASE_URL}/models")
        print(f"ステータス: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"利用可能モデル: {data.get('available_models')}")
            print(f"デフォルトモデル: {data.get('default_model')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ モデル情報取得失敗: {e}")
        return False

def test_file_upload():
    """ファイルアップロードテスト"""
    print("\n📤 ファイルアップロードテスト中...")
    
    # テスト用ダミーファイル作成
    test_file_path = Path("test_image.jpg")
    if not test_file_path.exists():
        # 1x1のダミー画像作成
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        img.save(test_file_path)
    
    try:
        with open(test_file_path, 'rb') as f:
            files = {'file': ('test_image.jpg', f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        print(f"ステータス: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"アップロード成功: {data.get('filename')}")
            return data.get('filename')
        else:
            print(f"❌ アップロード失敗: {response.text}")
            return None
    except Exception as e:
        print(f"❌ ファイルアップロード失敗: {e}")
        return None
    finally:
        # テストファイル削除
        if test_file_path.exists():
            test_file_path.unlink()

def test_cli_face_swap():
    """CLI Face Swapテスト"""
    print("\n🎭 CLI Face Swap テスト中...")
    
    # テストリクエスト
    request_data = {
        "source_path": "/app/data/source/kanna-hashimoto.jpg",
        "target_path": "/app/data/source/kanna-hashimoto.jpg",
        "output_path": "/app/data/output/test_result.jpg",
        "face_swapper_model": "inswapper_128",
        "output_image_quality": 90
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/cli/face-swap",
            headers={"Content-Type": "application/json"},
            data=json.dumps(request_data)
        )
        
        print(f"ステータス: {response.status_code}")
        print(f"レスポンス: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ CLI Face Swap失敗: {e}")
        return False

def test_swagger_ui():
    """Swagger UI アクセステスト"""
    print("\n📚 Swagger UI アクセステスト中...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"ステータス: {response.status_code}")
        if response.status_code == 200:
            print("✅ Swagger UI にアクセス可能")
            print(f"URL: {BASE_URL}/")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Swagger UI アクセス失敗: {e}")
        return False

def main():
    """メインテスト関数"""
    print("🚀 FaceFusion API テスト開始")
    print("=" * 50)
    
    # 各テスト実行
    tests = [
        ("ヘルスチェック", test_health_check),
        ("システム情報", test_system_info),
        ("モデル情報", test_models_info),
        ("Swagger UI", test_swagger_ui),
        ("ファイルアップロード", test_file_upload),
        ("CLI Face Swap", test_cli_face_swap),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"結果: {'✅ 成功' if result else '❌ 失敗'}")
        except Exception as e:
            print(f"❌ テスト実行エラー: {e}")
            results.append((test_name, False))
    
    # 結果サマリー
    print("\n" + "=" * 50)
    print("📊 テスト結果サマリー")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{test_name:<20} : {status}")
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    print(f"\n成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 全てのテストが成功しました！")
    else:
        print("⚠️ 一部のテストが失敗しました。")
    
    print(f"\n💡 Swagger UI URL: {BASE_URL}/")
    print(f"💡 ReDoc URL: {BASE_URL}/redoc")
    print(f"💡 CLI Help URL: {BASE_URL}/cli-help")

if __name__ == "__main__":
    main() 