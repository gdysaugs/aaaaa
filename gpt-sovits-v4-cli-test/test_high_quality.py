#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT-SoVITS v4 高品質音声テストスクリプト
ohayougozaimasu_5sec.wav 参照音声使用 (3.22秒、48kHz)
"""

import requests
import json
import os
import time
import sys
from urllib.parse import urlencode

class HighQualityTester:
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
    
    def test_high_quality_tts(self, text, prompt_text="おはようございます", output_file=None):
        """高品質48kHz参照音声を使った音声合成テスト"""
        print(f"\n🎵 高品質テスト: '{text}'")
        print(f"🎤 参照音声: ohayougozaimasu_5sec.wav (3.22秒、48kHz)")
        
        params = {
            'text': text,
            'text_lang': 'ja',
            'ref_audio_path': '/workspace/reference/ohayougozaimasu_5sec.wav',  # 3.22秒版を使用
            'prompt_text': prompt_text,
            'prompt_lang': 'ja'
        }
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/tts", params=params, timeout=120)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                print(f"✅ 高品質合成成功 ({processing_time:.2f}秒)")
                
                # 音声ファイルを保存
                if output_file:
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    print(f"💾 保存: {output_file}")
                    
                    # 音声ファイルの詳細情報を表示
                    try:
                        import subprocess
                        result = subprocess.run([
                            'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                            '-show_streams', output_file
                        ], capture_output=True, text=True)
                        
                        if result.returncode == 0:
                            import json
                            info = json.loads(result.stdout)
                            stream = info['streams'][0]
                            print(f"📊 出力音声情報:")
                            print(f"   サンプリングレート: {stream['sample_rate']}Hz")
                            print(f"   チャンネル数: {stream['channels']}")
                            print(f"   長さ: {float(stream['duration']):.2f}秒")
                            print(f"   ビットレート: {stream['bit_rate']}bps")
                    except:
                        pass
                
                self.test_results.append({
                    'text': text,
                    'status': 'success',
                    'time': processing_time,
                    'size': len(response.content),
                    'quality': '48kHz'
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
    
    def run_quality_comparison_tests(self):
        """音質比較テストを実行"""
        print("🎵 === GPT-SoVITS v4 高品質音声テスト開始 ===")
        
        # APIヘルスチェック
        if not self.check_api_health():
            print("❌ APIサーバーに接続できません")
            return False
        
        # 高品質音声テストケース
        quality_tests = [
            "おはようございます、これは高品質な音声テストです",
            "GPT-SoVITSバージョン4で48キロヘルツの音声を生成しています",
            "ノイズのないクリアな音声が生成されることを確認します",
            "声の質感とクリアさをテストしています"
        ]
        
        print(f"\n📝 {len(quality_tests)}個の高品質テストを実行します...")
        print(f"🎤 参照音声: ohayougozaimasu_5sec.wav (3.22秒、48kHz最適化)")
        
        success_count = 0
        for i, text in enumerate(quality_tests, 1):
            output_file = f"/workspace/output/high_quality_test_{i:02d}.wav"
            if self.test_high_quality_tts(text, output_file=output_file):
                success_count += 1
            time.sleep(2)  # API負荷軽減
        
        # 結果サマリー
        print(f"\n📊 === 高品質テスト結果サマリー ===")
        print(f"総テスト数: {len(quality_tests)}")
        print(f"成功: {success_count}")
        print(f"失敗: {len(quality_tests) - success_count}")
        print(f"成功率: {success_count/len(quality_tests)*100:.1f}%")
        
        # 詳細結果
        print(f"\n📋 === 詳細結果 ===")
        for i, result in enumerate(self.test_results, 1):
            status_icon = "✅" if result['status'] == 'success' else "❌"
            text = result['text'][:40] + "..." if len(result['text']) > 40 else result['text']
            
            if result['status'] == 'success':
                quality = result.get('quality', 'unknown')
                print(f"{status_icon} {i:02d}. {text} ({result['time']:.2f}s, {result['size']}bytes, {quality})")
            else:
                print(f"{status_icon} {i:02d}. {text} (エラー: {result.get('error', 'unknown')})")
        
        return success_count == len(quality_tests)

def main():
    print("🎵 GPT-SoVITS v4 高品質音声テスター")
    print("=" * 60)
    print("🎤 参照音声: ohayougozaimasu_5sec.wav (3.22秒、48kHz最適化)")
    
    tester = HighQualityTester()
    
    if len(sys.argv) > 1:
        # 単一テキストテスト
        text = " ".join(sys.argv[1:])
        tester.test_high_quality_tts(text, output_file="/workspace/output/high_quality_single.wav")
    else:
        # バッチテスト
        success = tester.run_quality_comparison_tests()
        if success:
            print("\n🎉 全ての高品質テストが成功しました！")
            print("💡 出力音声ファイルを確認して音質を比較してください")
            sys.exit(0)
        else:
            print("\n😞 一部のテストが失敗しました")
            sys.exit(1)

if __name__ == "__main__":
    main() 