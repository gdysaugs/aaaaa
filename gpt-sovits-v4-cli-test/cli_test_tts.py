#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT-SoVITS v4 CLI Test Tool
RTX3050 & Docker対応のCLIテストツール
"""

import argparse
import json
import sys
import time
import requests
from pathlib import Path

class GPTSoVITSCLI:
    def __init__(self, base_url="http://localhost:9880"):
        self.base_url = base_url
        
    def check_api_status(self):
        """APIサーバーの状態をチェック"""
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                print("✅ APIサーバーは正常に動作しています")
                return True
            else:
                print(f"⚠️ APIサーバーエラー: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ APIサーバーに接続できません")
            return False
        except Exception as e:
            print(f"❌ エラー: {e}")
            return False
    
    def test_tts_simple(self):
        """シンプルなTTSテスト（英語）"""
        print("\n=== シンプルTTSテスト（英語） ===")
        
        params = {
            "text": "Hello world, this is a test",
            "text_lang": "en",
            "ref_audio_path": "/workspace/reference/dummy_5sec.wav",
            "prompt_text": "Test audio",
            "prompt_lang": "en"
        }
        
        try:
            response = requests.get(f"{self.base_url}/tts", params=params, timeout=30)
            print(f"ステータスコード: {response.status_code}")
            print(f"レスポンスサイズ: {len(response.content)} bytes")
            
            if response.status_code == 200:
                # WAVファイルかチェック
                if response.headers.get('content-type', '').startswith('audio') or len(response.content) > 1000:
                    output_file = "output_english_test.wav"
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ 音声ファイル保存: {output_file}")
                    return True
                else:
                    print(f"⚠️ レスポンス内容: {response.text[:200]}")
            else:
                print(f"❌ エラー: {response.text}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
        
        return False
    
    def test_tts_chinese(self):
        """中国語TTSテスト"""
        print("\n=== 中国語TTSテスト ===")
        
        params = {
            "text": "你好世界，这是一个测试",
            "text_lang": "zh",
            "ref_audio_path": "/workspace/reference/dummy_5sec.wav", 
            "prompt_text": "测试音频",
            "prompt_lang": "zh"
        }
        
        try:
            response = requests.get(f"{self.base_url}/tts", params=params, timeout=30)
            print(f"ステータスコード: {response.status_code}")
            print(f"レスポンスサイズ: {len(response.content)} bytes")
            
            if response.status_code == 200:
                if response.headers.get('content-type', '').startswith('audio') or len(response.content) > 1000:
                    output_file = "output_chinese_test.wav"
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ 音声ファイル保存: {output_file}")
                    return True
                else:
                    print(f"⚠️ レスポンス内容: {response.text[:200]}")
            else:
                print(f"❌ エラー: {response.text}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
        
        return False
    
    def check_gpu_status(self):
        """GPU状態チェック"""
        print("\n=== GPU状態チェック ===")
        try:
            import subprocess
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ NVIDIA GPU detected")
                # GPU使用状況の抜粋表示
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'MiB' in line and ('python' in line.lower() or 'gpu' in line.lower()):
                        print(f"GPU使用状況: {line.strip()}")
                return True
            else:
                print("⚠️ nvidia-smiが実行できません")
                return False
        except Exception as e:
            print(f"❌ GPU確認エラー: {e}")
            return False
    
    def debug_permissions(self):
        """権限問題のデバッグ"""
        print("\n=== 権限デバッグ ===")
        print("pyopenjtalkの権限問題をチェック中...")
        
        # コンテナ内で権限確認
        import subprocess
        try:
            result = subprocess.run([
                'docker', 'compose', '-f', 'docker-compose.v2.6.yml', 
                'exec', 'gpt-sovits-dev', 'ls', '-la', 
                '/usr/local/lib/python3.10/dist-packages/pyopenjtalk/'
            ], capture_output=True, text=True, cwd='/home/adama/LLM/gpt-sovits-v4-cli-test')
            
            if result.returncode == 0:
                print("📁 pyopenjtalkディレクトリ:")
                print(result.stdout)
            else:
                print(f"⚠️ pyopenjtalkディレクトリ確認失敗: {result.stderr}")
                
        except Exception as e:
            print(f"❌ 権限確認エラー: {e}")

def main():
    parser = argparse.ArgumentParser(description='GPT-SoVITS v4 CLI Test Tool')
    parser.add_argument('--base-url', default='http://localhost:9880', 
                       help='APIサーバーのベースURL')
    parser.add_argument('--check-api', action='store_true', 
                       help='APIサーバーの状態をチェック')
    parser.add_argument('--check-gpu', action='store_true', 
                       help='GPU状態をチェック')
    parser.add_argument('--test-english', action='store_true', 
                       help='英語TTSテスト')
    parser.add_argument('--test-chinese', action='store_true', 
                       help='中国語TTSテスト')
    parser.add_argument('--debug-permissions', action='store_true', 
                       help='権限問題をデバッグ')
    parser.add_argument('--all-tests', action='store_true', 
                       help='全てのテストを実行')
    
    args = parser.parse_args()
    
    cli = GPTSoVITSCLI(args.base_url)
    
    print("🎤 GPT-SoVITS v4 CLI Test Tool")
    print("=" * 50)
    
    success_count = 0
    total_tests = 0
    
    if args.all_tests or args.check_api:
        total_tests += 1
        if cli.check_api_status():
            success_count += 1
    
    if args.all_tests or args.check_gpu:
        total_tests += 1
        if cli.check_gpu_status():
            success_count += 1
    
    if args.all_tests or args.debug_permissions:
        cli.debug_permissions()
    
    if args.all_tests or args.test_english:
        total_tests += 1
        if cli.test_tts_simple():
            success_count += 1
    
    if args.all_tests or args.test_chinese:
        total_tests += 1
        if cli.test_tts_chinese():
            success_count += 1
    
    if total_tests > 0:
        print(f"\n📊 テスト結果: {success_count}/{total_tests} 成功")
        if success_count == total_tests:
            print("🎉 全テスト成功！")
        else:
            print("⚠️ 一部テストが失敗しました")
    
    if len(sys.argv) == 1:
        parser.print_help()

if __name__ == "__main__":
    main() 