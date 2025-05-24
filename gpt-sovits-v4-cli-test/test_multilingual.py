#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT-SoVITS v4 多言語テストスクリプト
日本語・英語・多言語対応
"""

import requests
import json
import os
import time
import sys
from urllib.parse import urlencode

class MultilingualTester:
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
    
    def test_tts(self, text, text_lang, prompt_text, prompt_lang, output_file=None, description=""):
        """多言語音声合成テスト"""
        print(f"\n🎤 {description}: '{text}'")
        print(f"📝 言語: {text_lang} | 参照: {prompt_lang}")
        
        params = {
            'text': text,
            'text_lang': text_lang,
            'ref_audio_path': '/workspace/reference/ohayougozaimasu_5sec.wav',
            'prompt_text': prompt_text,
            'prompt_lang': prompt_lang
        }
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/tts", params=params, timeout=120)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                print(f"✅ 合成成功 ({processing_time:.2f}秒)")
                
                if output_file:
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    print(f"💾 保存: {output_file}")
                
                self.test_results.append({
                    'text': text,
                    'lang': text_lang,
                    'status': 'success',
                    'time': processing_time,
                    'size': len(response.content)
                })
                return True
            else:
                print(f"❌ 合成失敗: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   エラー詳細: {error_detail}")
                except:
                    print(f"   エラー内容: {response.text}")
                
                self.test_results.append({
                    'text': text,
                    'lang': text_lang,
                    'status': 'failed',
                    'error': response.status_code
                })
                return False
                
        except Exception as e:
            print(f"❌ リクエストエラー: {e}")
            self.test_results.append({
                'text': text,
                'lang': text_lang,
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def run_multilingual_tests(self):
        """多言語テストを実行"""
        print("🌍 === GPT-SoVITS v4 多言語テスト開始 ===")
        print("🎤 参照音声: ohayougozaimasu_5sec.wav (3.22秒、48kHz)")
        
        # APIヘルスチェック
        if not self.check_api_health():
            print("❌ APIサーバーに接続できません")
            return False
        
        # 多言語テストケース
        test_cases = [
            # 日本語テスト
            {
                'text': 'こんにちは、世界！これは日本語のテストです。',
                'text_lang': 'ja',
                'prompt_text': 'おはようございます',
                'prompt_lang': 'ja',
                'description': '日本語テスト',
                'output': '/workspace/output/japanese_test.wav'
            },
            {
                'text': 'GPT-SoVITSで美しい音声を生成しています。',
                'text_lang': 'ja',
                'prompt_text': 'おはようございます',
                'prompt_lang': 'ja',
                'description': '日本語長文テスト',
                'output': '/workspace/output/japanese_long.wav'
            },
            
            # 英語テスト
            {
                'text': 'Hello, world! This is an English test.',
                'text_lang': 'en',
                'prompt_text': 'Test audio',
                'prompt_lang': 'en',
                'description': '英語テスト',
                'output': '/workspace/output/english_test.wav'
            },
            {
                'text': 'GPT-SoVITS version 4 generates high-quality voice synthesis.',
                'text_lang': 'en',
                'prompt_text': 'Test audio',
                'prompt_lang': 'en',
                'description': '英語長文テスト',
                'output': '/workspace/output/english_long.wav'
            },
            
            # 中国語テスト
            {
                'text': '你好，世界！这是中文测试。',
                'text_lang': 'zh',
                'prompt_text': '测试音频',
                'prompt_lang': 'zh',
                'description': '中国語テスト',
                'output': '/workspace/output/chinese_test.wav'
            },
            
            # 多言語混合テスト（参照は日本語のまま）
            {
                'text': 'Hello! こんにちは！This is a multilingual test.',
                'text_lang': 'en',
                'prompt_text': 'おはようございます',
                'prompt_lang': 'ja',
                'description': '多言語混合テスト（英語）',
                'output': '/workspace/output/multilingual_en.wav'
            }
        ]
        
        print(f"\n📝 {len(test_cases)}個の多言語テストを実行します...")
        
        success_count = 0
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- テスト {i:02d}/{len(test_cases):02d} ---")
            if self.test_tts(
                text=test_case['text'],
                text_lang=test_case['text_lang'],
                prompt_text=test_case['prompt_text'],
                prompt_lang=test_case['prompt_lang'],
                output_file=test_case['output'],
                description=test_case['description']
            ):
                success_count += 1
            time.sleep(2)  # API負荷軽減
        
        # 結果サマリー
        print(f"\n📊 === 多言語テスト結果サマリー ===")
        print(f"総テスト数: {len(test_cases)}")
        print(f"成功: {success_count}")
        print(f"失敗: {len(test_cases) - success_count}")
        print(f"成功率: {success_count/len(test_cases)*100:.1f}%")
        
        # 言語別サマリー
        lang_results = {}
        for result in self.test_results:
            lang = result['lang']
            if lang not in lang_results:
                lang_results[lang] = {'success': 0, 'total': 0}
            lang_results[lang]['total'] += 1
            if result['status'] == 'success':
                lang_results[lang]['success'] += 1
        
        print(f"\n🌍 === 言語別結果 ===")
        lang_names = {'ja': '日本語', 'en': '英語', 'zh': '中国語', 'ko': '韓国語'}
        for lang, stats in lang_results.items():
            lang_name = lang_names.get(lang, lang)
            success_rate = stats['success'] / stats['total'] * 100
            print(f"{lang_name}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        return success_count == len(test_cases)

def main():
    print("🌍 GPT-SoVITS v4 多言語テスター")
    print("=" * 60)
    print("🎤 参照音声: ohayougozaimasu_5sec.wav (3.22秒、48kHz)")
    print("🌍 対応言語: 日本語・英語・中国語・多言語混合")
    
    tester = MultilingualTester()
    
    if len(sys.argv) > 2:
        # 単一テストモード: python script.py "text" "lang"
        text = sys.argv[1]
        lang = sys.argv[2] if len(sys.argv) > 2 else 'ja'
        
        # 言語に応じたプロンプト設定
        prompts = {
            'ja': ('おはようございます', 'ja'),
            'en': ('Test audio', 'en'),
            'zh': ('测试音频', 'zh')
        }
        prompt_text, prompt_lang = prompts.get(lang, ('おはようございます', 'ja'))
        
        tester.test_tts(
            text=text, 
            text_lang=lang,
            prompt_text=prompt_text,
            prompt_lang=prompt_lang,
            output_file=f"/workspace/output/single_{lang}.wav",
            description=f"単一テスト ({lang})"
        )
    else:
        # バッチテストモード
        success = tester.run_multilingual_tests()
        if success:
            print("\n🎉 全ての多言語テストが成功しました！")
            print("💡 出力音声ファイルを確認して各言語の音質を比較してください")
            sys.exit(0)
        else:
            print("\n😞 一部のテストが失敗しました")
            sys.exit(1)

if __name__ == "__main__":
    main() 