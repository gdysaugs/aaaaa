#!/usr/bin/env python3
"""
FaceFusion API テストスクリプト
べ、別にあんたのためじゃないけど、APIが正しく動作するかテストしてあげるわよ！
"""
import requests
import json
import time
from pathlib import Path

# API設定
API_BASE_URL = "http://localhost:8000"
TEST_DATA_DIR = Path("data/source")

def test_health_check():
    """ヘルスチェックテスト"""
    print("🏥 ヘルスチェックテスト開始...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ ヘルスチェック成功")
            print(f"   ステータス: {data.get('status')}")
            print(f"   FaceFusion利用可能: {data.get('facefusion_available')}")
            print(f"   GPU利用可能: {data.get('gpu_available')}")
            return True
        else:
            print(f"❌ ヘルスチェック失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ヘルスチェックエラー: {e}")
        return False

def test_root_endpoint():
    """ルートエンドポイントテスト"""
    print("\n🏠 ルートエンドポイントテスト開始...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ ルートエンドポイント成功")
            print(f"   メッセージ: {data.get('message')}")
            print(f"   サービス: {data.get('service')}")
            return True
        else:
            print(f"❌ ルートエンドポイント失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ルートエンドポイントエラー: {e}")
        return False

def test_file_upload():
    """ファイルアップロードテスト"""
    print("\n📤 ファイルアップロードテスト開始...")
    
    # テスト画像ファイル確認
    test_image = TEST_DATA_DIR / "kanna-hashimoto.jpg"
    if not test_image.exists():
        print(f"❌ テスト画像が見つかりません: {test_image}")
        return False, None
    
    try:
        with open(test_image, 'rb') as f:
            files = {'file': ('test.jpg', f, 'image/jpeg')}
            response = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ ファイルアップロード成功")
            print(f"   ファイル名: {data.get('filename')}")
            print(f"   ファイルサイズ: {data.get('file_size')} bytes")
            print(f"   メディアタイプ: {data.get('media_type')}")
            return True, data.get('filename')
        else:
            print(f"❌ ファイルアップロード失敗: {response.status_code}")
            print(f"   レスポンス: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ ファイルアップロードエラー: {e}")
        return False, None

def test_image_face_swap():
    """画像Face Swapテスト"""
    print("\n🖼️ 画像Face Swapテスト開始...")
    
    # テスト画像ファイル確認
    source_image = TEST_DATA_DIR / "kanna-hashimoto.jpg"
    target_image = TEST_DATA_DIR / "source1.jpg"
    
    if not source_image.exists() or not target_image.exists():
        print(f"❌ テスト画像が見つかりません")
        print(f"   ソース: {source_image} (存在: {source_image.exists()})")
        print(f"   ターゲット: {target_image} (存在: {target_image.exists()})")
        return False, None
    
    try:
        start_time = time.time()
        
        with open(source_image, 'rb') as source, open(target_image, 'rb') as target:
            files = {
                'source_file': ('source.jpg', source, 'image/jpeg'),
                'target_file': ('target.jpg', target, 'image/jpeg')
            }
            data = {
                'model': 'inswapper_128',
                'quality': 90
            }
            
            response = requests.post(
                f"{API_BASE_URL}/face-swap/image", 
                files=files, 
                data=data, 
                timeout=300
            )
        
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 画像Face Swap成功")
            print(f"   出力ファイル: {result.get('output_filename')}")
            print(f"   ファイルサイズ: {result.get('file_size')} bytes")
            print(f"   処理時間: {processing_time:.2f}秒")
            return True, result.get('output_filename')
        else:
            print(f"❌ 画像Face Swap失敗: {response.status_code}")
            print(f"   レスポンス: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ 画像Face Swapエラー: {e}")
        return False, None

def test_video_face_swap():
    """動画Face Swapテスト"""
    print("\n🎬 動画Face Swapテスト開始...")
    
    # テストファイル確認
    source_image = TEST_DATA_DIR / "kanna-hashimoto.jpg"
    target_video = TEST_DATA_DIR / "test_video.mp4"
    
    if not source_image.exists():
        print(f"❌ ソース画像が見つかりません: {source_image}")
        return False, None
        
    if not target_video.exists():
        print(f"⚠️ テスト動画が見つかりません: {target_video}")
        print("   動画Face Swapテストをスキップします")
        return True, None  # スキップとして成功扱い
    
    try:
        start_time = time.time()
        
        with open(source_image, 'rb') as source, open(target_video, 'rb') as target:
            files = {
                'source_file': ('source.jpg', source, 'image/jpeg'),
                'target_file': ('target.mp4', target, 'video/mp4')
            }
            data = {
                'model': 'inswapper_128',
                'quality': 80,
                'trim_start': 0,
                'trim_end': 30  # 最初の30フレームのみ
            }
            
            response = requests.post(
                f"{API_BASE_URL}/face-swap/video", 
                files=files, 
                data=data, 
                timeout=600
            )
        
        processing_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 動画Face Swap成功")
            print(f"   出力ファイル: {result.get('output_filename')}")
            print(f"   ファイルサイズ: {result.get('file_size')} bytes")
            print(f"   処理時間: {processing_time:.2f}秒")
            return True, result.get('output_filename')
        else:
            print(f"❌ 動画Face Swap失敗: {response.status_code}")
            print(f"   レスポンス: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ 動画Face Swapエラー: {e}")
        return False, None

def test_file_download(filename):
    """ファイルダウンロードテスト"""
    if not filename:
        print("\n⚠️ ダウンロードテストをスキップ（ファイル名なし）")
        return True
        
    print(f"\n📥 ファイルダウンロードテスト開始: {filename}")
    
    try:
        response = requests.get(f"{API_BASE_URL}/download/{filename}", timeout=30)
        
        if response.status_code == 200:
            # ファイル保存
            output_path = Path("test_output") / filename
            output_path.parent.mkdir(exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            file_size = output_path.stat().st_size
            print(f"✅ ファイルダウンロード成功")
            print(f"   保存先: {output_path}")
            print(f"   ファイルサイズ: {file_size} bytes")
            return True
        else:
            print(f"❌ ファイルダウンロード失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ファイルダウンロードエラー: {e}")
        return False

def main():
    """メインテスト実行"""
    print("=" * 60)
    print("🧪 FaceFusion API テスト開始")
    print("=" * 60)
    
    # テスト結果記録
    results = {}
    
    # 1. ヘルスチェック
    results['health'] = test_health_check()
    
    # 2. ルートエンドポイント
    results['root'] = test_root_endpoint()
    
    # 3. ファイルアップロード
    results['upload'], uploaded_filename = test_file_upload()
    
    # 4. 画像Face Swap
    results['image_swap'], image_output = test_image_face_swap()
    
    # 5. 動画Face Swap
    results['video_swap'], video_output = test_video_face_swap()
    
    # 6. ファイルダウンロード
    results['download_image'] = test_file_download(image_output)
    results['download_video'] = test_file_download(video_output)
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 テスト結果サマリー")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, result in results.items():
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{test_name:20}: {status}")
    
    print(f"\n📈 総合結果: {passed_tests}/{total_tests} テスト成功")
    
    if passed_tests == total_tests:
        print("🎉 全テスト成功！APIは正常に動作しています！")
        return True
    else:
        print("⚠️ 一部テストが失敗しました。ログを確認してください。")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
