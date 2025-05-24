#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT-SoVITS v4 日本語専用テストスクリプト
"""

import requests
import json
import os
import time
import sys
from urllib.parse import urlencode

class JapaneseOnlyTester:
    def __init__(self, base_url="http://localhost:9880"):
        self.base_url = base_url
        self.test_results = []
        
    def check_api_health(self):
        """APIの基本的な動作確認"""
        try:
            response = requests.get(f"{self.base_url}/docs")
            if response.status_code == 200:
                print("✅ APIサーバーは正常に動作中")
                return True
            else:
                print(f"❌ APIサーバーエラー: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API接続エラー: {e}")
            return False
    
    def test_japanese_tts(self, text, prompt_text="テスト音声", output_file=None):
        """日本語音声合成テスト"""
        print(f"\n🎌 日本語テスト: '{text}'")
        
        params = {
            'text': text,
            'text_lang': 'ja',
            'ref_audio_path': '/workspace/reference/dummy_5sec.wav',
            'prompt_text': prompt_text,
            'prompt_lang': 'ja'
        }
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/tts", params=params, timeout=120)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                print(f"✅ 合成成功 ({processing_time:.2f}秒)")
                
                # 音声ファイルを保存
                if output_file:
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    print(f"💾 保存: {output_file}")
                
                self.test_results.append({
                    'text': text,
                    'status': 'success',
                    'time': processing_time,
                    'size': len(response.content)
                })
                return True
            else:
                print(f"❌ 合成失敗: {response.status_code}")
                print(f"   エラー内容: {response.text}")
                self.test_results.append({
                    'text': text,
                    'status': 'failed',
                    'error': response.status_code
                })
                return False
                
        except Exception as e:
            print(f"❌ リクエストエラー: {e}")
            self.test_results.append({
                'text': text,
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def run_japanese_tests(self):
        """日本語テストバッチを実行"""
        print("🗾 === GPT-SoVITS v4 日本語専用テスト開始 ===")
        
        # APIヘルスチェック
        if not self.check_api_health():
            print("❌ APIサーバーに接続できません")
            return False
        
        # 日本語テストケース
        japanese_tests = [
            "こんにちは、世界",
            "おはようございます",
            "ありがとうございます",
            "今日は良い天気ですね",
            "GPT-SoVITSで音声合成をテストしています",
            "日本語の音声合成が正常に動作することを確認します"
        ]
        
        print(f"\n📝 {len(japanese_tests)}個の日本語テストを実行します...")
        
        success_count = 0
        for i, text in enumerate(japanese_tests, 1):
            output_file = f"/workspace/output/japanese_test_{i:02d}.wav"
            if self.test_japanese_tts(text, output_file=output_file):
                success_count += 1
            time.sleep(2)  # API負荷軽減
        
        # 結果サマリー
        print(f"\n📊 === テスト結果サマリー ===")
        print(f"総テスト数: {len(japanese_tests)}")
        print(f"成功: {success_count}")
        print(f"失敗: {len(japanese_tests) - success_count}")
        print(f"成功率: {success_count/len(japanese_tests)*100:.1f}%")
        
        # 詳細結果
        print(f"\n📋 === 詳細結果 ===")
        for i, result in enumerate(self.test_results, 1):
            status_icon = "✅" if result['status'] == 'success' else "❌"
            text = result['text'][:30] + "..." if len(result['text']) > 30 else result['text']
            
            if result['status'] == 'success':
                print(f"{status_icon} {i:02d}. {text} ({result['time']:.2f}s, {result['size']}bytes)")
            else:
                print(f"{status_icon} {i:02d}. {text} (エラー: {result.get('error', 'unknown')})")
        
        return success_count == len(japanese_tests)

def main():
    print("🎌 GPT-SoVITS v4 日本語専用テスター")
    print("=" * 50)
    
    tester = JapaneseOnlyTester()
    
    if len(sys.argv) > 1:
        # 単一テキストテスト
        text = " ".join(sys.argv[1:])
        tester.test_japanese_tts(text, output_file="/workspace/output/single_test.wav")
    else:
        # バッチテスト
        success = tester.run_japanese_tests()
        if success:
            print("\n🎉 全ての日本語テストが成功しました！")
            sys.exit(0)
        else:
            print("\n😞 一部のテストが失敗しました")
            sys.exit(1)

if __name__ == "__main__":
    main() 