#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPT-SoVITS v4 Simple Test Script
基本的なAPI動作確認用
"""

import requests
import time
import sys

def test_api_basic():
    """基本API接続テスト"""
    try:
        print("🔍 API接続テスト中...")
        response = requests.get("http://localhost:9880/docs", timeout=10)
        if response.status_code == 200:
            print("✅ APIサーバー動作中")
            return True
        else:
            print(f"⚠️ APIエラー: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API接続失敗")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_tts_simple():
    """シンプルTTSテスト（中国語のみ）"""
    print("\n🎵 中国語TTSテスト...")
    
    params = {
        "text": "你好世界",
        "text_lang": "zh", 
        "ref_audio_path": "/workspace/reference/dummy_5sec.wav",
        "prompt_text": "测试",
        "prompt_lang": "zh"
    }
    
    try:
        response = requests.get("http://localhost:9880/tts", params=params, timeout=60)
        print(f"Status: {response.status_code}")
        print(f"Size: {len(response.content)} bytes")
        
        if response.status_code == 200 and len(response.content) > 1000:
            with open("test_output.wav", "wb") as f:
                f.write(response.content)
            print("✅ 音声ファイル生成成功: test_output.wav")
            return True
        else:
            print(f"❌ TTS失敗: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def main():
    print("🎤 GPT-SoVITS v4 Simple Test")
    print("=" * 40)
    
    # API接続テスト
    if not test_api_basic():
        print("❌ APIサーバーに接続できません")
        return
    
    # TTS基本テスト  
    if test_tts_simple():
        print("\n🎉 テスト成功！音声合成が動作しています")
    else:
        print("\n⚠️ TTS処理にエラーがあります")

if __name__ == "__main__":
    main() 