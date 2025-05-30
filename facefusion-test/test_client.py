#!/usr/bin/env python3
"""
FaceFusion APIテストクライアント
べ、別にあんたのためじゃないけど、ちゃんとテストできるようにしてあげるわよ！
"""

import os
import json
import time
import requests
from pathlib import Path
from typing import Optional

class FaceFusionTestClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = (10, 300)  # 接続10秒、読み取り5分

    def health_check(self) -> dict:
        """ヘルスチェック"""
        print("🔍 ヘルスチェック中...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            result = response.json()
            print(f"✅ ヘルスチェック成功: {result.get('status')}")
            return result
        except Exception as e:
            print(f"❌ ヘルスチェック失敗: {e}")
            return {"status": "error", "error": str(e)}

    def get_system_info(self) -> dict:
        """システム情報取得"""
        print("📊 システム情報取得中...")
        try:
            response = self.session.get(f"{self.base_url}/system/info")
            response.raise_for_status()
            result = response.json()
            print(f"✅ システム情報取得成功")
            return result
        except Exception as e:
            print(f"❌ システム情報取得失敗: {e}")
            return {"error": str(e)}

    def get_models(self) -> dict:
        """利用可能なモデル一覧"""
        print("🤖 モデル情報取得中...")
        try:
            response = self.session.get(f"{self.base_url}/models")
            response.raise_for_status()
            result = response.json()
            print(f"✅ モデル情報取得成功: {len(result.get('available_models', []))}個のモデル")
            return result
        except Exception as e:
            print(f"❌ モデル情報取得失敗: {e}")
            return {"error": str(e)}

    def test_file_upload(self, file_path: str) -> Optional[dict]:
        """ファイルアップロードテスト"""
        if not os.path.exists(file_path):
            print(f"❌ ファイルが見つかりません: {file_path}")
            return None

        print(f"📤 ファイルアップロード中: {os.path.basename(file_path)}")
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                response = self.session.post(f"{self.base_url}/upload", files=files)
                response.raise_for_status()
                result = response.json()
                print(f"✅ アップロード成功: {result.get('filename')}")
                return result
        except Exception as e:
            print(f"❌ アップロード失敗: {e}")
            return None

    def test_video_face_swap_upload(self, source_path: str, target_path: str, 
                                   model: str = "inswapper_128", quality: int = 80,
                                   max_frames: int = 50) -> Optional[dict]:
        """動画Face Swap（アップロード形式）"""
        if not os.path.exists(source_path) or not os.path.exists(target_path):
            print(f"❌ ファイルが見つかりません")
            return None

        print(f"🎬 動画Face Swap開始...")
        print(f"   ソース: {os.path.basename(source_path)}")
        print(f"   ターゲット: {os.path.basename(target_path)}")
        print(f"   モデル: {model}")
        print(f"   最大フレーム: {max_frames}")

        try:
            with open(source_path, 'rb') as source_file, open(target_path, 'rb') as target_file:
                files = {
                    'source_file': (os.path.basename(source_path), source_file),
                    'target_file': (os.path.basename(target_path), target_file)
                }
                data = {
                    'model': model,
                    'quality': quality,
                    'max_frames': max_frames
                }
                
                print("⏳ 処理中... (数分かかる場合があります)")
                start_time = time.time()
                
                response = self.session.post(
                    f"{self.base_url}/face-swap/video", 
                    files=files, 
                    data=data
                )
                response.raise_for_status()
                result = response.json()
                
                processing_time = time.time() - start_time
                print(f"✅ 動画Face Swap完了!")
                print(f"   出力ファイル: {result.get('output_filename')}")
                print(f"   処理時間: {processing_time:.1f}秒")
                print(f"   ファイルサイズ: {result.get('file_size', 0) / 1024 / 1024:.1f}MB")
                
                return result
        except Exception as e:
            print(f"❌ 動画Face Swap失敗: {e}")
            return None

    def test_cli_face_swap(self, source_path: str, target_path: str, output_path: str,
                          model: str = "inswapper_128") -> Optional[dict]:
        """CLI形式でのFace Swap"""
        print(f"🖥️  CLI Face Swap開始...")
        print(f"   ソース: {source_path}")
        print(f"   ターゲット: {target_path}")
        print(f"   出力: {output_path}")

        # パスをコンテナ内パスに変換
        container_source = source_path.replace('/home/adamna/LLM/facefusion-test', '/app')
        container_target = target_path.replace('/home/adamna/LLM/facefusion-test', '/app')
        container_output = output_path.replace('/home/adamna/LLM/facefusion-test', '/app')

        # 動画かどうか判定
        target_ext = Path(target_path).suffix.lower()
        is_video = target_ext in ['.mp4', '.avi', '.mov']

        data = {
            "source_path": container_source,
            "target_path": container_target,
            "output_path": container_output,
            "face_swapper_model": model
        }

        if is_video:
            data.update({
                "output_video_quality": 80,
                "trim_frame_start": 0,
                "trim_frame_end": 50
            })
        else:
            data.update({
                "output_image_quality": 90
            })

        try:
            print("⏳ CLI実行中...")
            response = self.session.post(
                f"{self.base_url}/cli/face-swap",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ CLI Face Swap完了!")
            print(f"   結果: {result}")
            
            return result
        except Exception as e:
            print(f"❌ CLI Face Swap失敗: {e}")
            return None

    def download_file(self, filename: str, output_dir: str = "./downloads") -> bool:
        """ファイルダウンロード"""
        print(f"📥 ファイルダウンロード中: {filename}")
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            response = self.session.get(f"{self.base_url}/download/{filename}")
            response.raise_for_status()
            
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ ダウンロード完了: {output_path}")
            return True
        except Exception as e:
            print(f"❌ ダウンロード失敗: {e}")
            return False

    def run_full_test(self, source_path: str, target_path: str):
        """完全テスト実行"""
        print("=" * 60)
        print("🎭 FaceFusion API 完全テスト開始")
        print("=" * 60)

        # 1. ヘルスチェック
        health = self.health_check()
        if health.get('status') != 'healthy':
            print("❌ サービスが正常ではありません。テストを中止します。")
            return

        # 2. システム情報
        system_info = self.get_system_info()
        
        # 3. モデル情報
        models = self.get_models()

        # 4. 動画Face Swap（アップロード形式）テスト
        print("\n" + "=" * 40)
        print("🎬 動画Face Swap（アップロード形式）テスト")
        print("=" * 40)
        
        upload_result = self.test_video_face_swap_upload(source_path, target_path)
        if upload_result and upload_result.get('success'):
            output_filename = upload_result.get('output_filename')
            if output_filename:
                self.download_file(output_filename, "./test_outputs")

        # 5. CLI形式テスト
        print("\n" + "=" * 40)
        print("🖥️  CLI形式テスト")
        print("=" * 40)
        
        output_path = "/home/adamna/LLM/facefusion-test/data/output/cli_test_output.mp4"
        cli_result = self.test_cli_face_swap(source_path, target_path, output_path)

        print("\n" + "=" * 60)
        print("🎉 テスト完了!")
        print("=" * 60)

        # 結果サマリー
        print("\n📊 テスト結果サマリー:")
        print(f"   ヘルスチェック: {'✅' if health.get('status') == 'healthy' else '❌'}")
        print(f"   アップロード形式: {'✅' if upload_result and upload_result.get('success') else '❌'}")
        print(f"   CLI形式: {'✅' if cli_result and cli_result.get('success') else '❌'}")

def main():
    """メイン実行"""
    print("🎭 FaceFusion APIテストクライアント")
    print("べ、別にあんたのためじゃないけど、テストしてあげるわよ！")
    
    # ファイルパス設定
    base_dir = Path("/home/adamna/LLM/facefusion-test")
    source_path = str(base_dir / "data/source/kanna-hashimoto.jpg")
    target_path = str(base_dir / "data/source/画面録画 2025-05-16 222902.mp4")

    # ファイル存在確認
    if not os.path.exists(source_path):
        print(f"❌ ソース画像が見つかりません: {source_path}")
        return
    
    if not os.path.exists(target_path):
        print(f"❌ ターゲット動画が見つかりません: {target_path}")
        return

    print(f"📁 ソース画像: {source_path}")
    print(f"🎬 ターゲット動画: {target_path}")

    # テスト実行
    client = FaceFusionTestClient()
    client.run_full_test(source_path, target_path)

    # Swagger UI案内
    print("\n" + "=" * 60)
    print("🌐 Swagger UI でのテスト方法:")
    print("=" * 60)
    print("1. ブラウザで http://localhost:8000 にアクセス")
    print("2. 各エンドポイントを展開して 'Try it out' をクリック")
    print("3. ファイルをアップロードしてテスト実行")
    print("\n主要エンドポイント:")
    print("   GET  /health          - ヘルスチェック")
    print("   GET  /models          - モデル情報")
    print("   POST /upload          - ファイルアップロード")
    print("   POST /face-swap/video - 動画Face Swap")
    print("   POST /cli/face-swap   - CLI形式Face Swap")
    print("   GET  /download/{filename} - ファイルダウンロード")

if __name__ == "__main__":
    main() 