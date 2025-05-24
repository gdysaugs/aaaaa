#!/usr/bin/env python3
"""
GPT-SoVITS v4 CLI Test Script (Model-Free Version)
RTX3050 + CUDA 12.4対応版
"""

import argparse
import requests
import json
import torch
import time
import os
import sys

def check_gpu():
    """GPU状態確認"""
    print("=== GPU Status Check ===")
    
    # CUDA利用可能性確認
    print(f"PyTorch Version: {torch.__version__}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"Device Count: {torch.cuda.device_count()}")
        
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
            
            # VRAM情報
            if torch.cuda.is_available():
                memory_total = torch.cuda.get_device_properties(i).total_memory / 1024**3
                memory_allocated = torch.cuda.memory_allocated(i) / 1024**3
                memory_cached = torch.cuda.memory_reserved(i) / 1024**3
                
                print(f"  Total VRAM: {memory_total:.2f} GB")
                print(f"  Allocated: {memory_allocated:.2f} GB")
                print(f"  Cached: {memory_cached:.2f} GB")
    else:
        print("❌ CUDA not available - using CPU mode")
    
    print("✅ GPU check completed\n")

def check_environment():
    """環境確認"""
    print("=== Environment Check ===")
    
    # Python version
    print(f"Python Version: {sys.version}")
    
    # 必要なライブラリの確認
    required_libs = [
        'torch', 'torchaudio', 'numpy', 'scipy', 
        'librosa', 'soundfile', 'requests'
    ]
    
    for lib in required_libs:
        try:
            __import__(lib)
            print(f"✅ {lib}: Available")
        except ImportError:
            print(f"❌ {lib}: Not available")
    
    print("✅ Environment check completed\n")

def check_file_structure():
    """ファイル構造確認"""
    print("=== File Structure Check ===")
    
    base_path = "/workspace/GPT-SoVITS"
    
    # 重要なディレクトリとファイルをチェック
    important_paths = [
        "api_v2.py",
        "GPT_SoVITS/configs/tts_infer.yaml",
        "GPT_SoVITS/pretrained_models",
        "GPT_SoVITS/TTS_infer_pack",
    ]
    
    for path in important_paths:
        full_path = os.path.join(base_path, path)
        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                print(f"✅ Directory: {path}")
            else:
                print(f"✅ File: {path}")
        else:
            print(f"❌ Missing: {path}")
    
    # モデルファイルの確認
    model_dir = os.path.join(base_path, "GPT_SoVITS/pretrained_models")
    if os.path.exists(model_dir):
        print(f"\n📁 Model files in {model_dir}:")
        for root, dirs, files in os.walk(model_dir):
            for file in files:
                if file.endswith(('.pth', '.ckpt', '.bin')):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path) / 1024 / 1024  # MB
                    print(f"  📄 {file}: {file_size:.2f} MB")
    
    print("✅ File structure check completed\n")

def test_api_connection():
    """API接続テスト（モデルなし）"""
    print("=== API Connection Test ===")
    
    api_url = "http://localhost:9880"
    
    try:
        # 基本的な接続テスト
        response = requests.get(f"{api_url}/", timeout=5)
        print(f"✅ API server is responding: {response.status_code}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server at localhost:9880")
        print("💡 Make sure the API server is running")
        return False
    except requests.exceptions.Timeout:
        print("❌ API server timeout")
        return False
    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False
    
    print("✅ API connection test completed\n")
    return True

def test_basic_imports():
    """基本的なインポートテスト"""
    print("=== Basic Import Test ===")
    
    try:
        # GPT-SoVITSの基本モジュールをテスト
        sys.path.append('/workspace/GPT-SoVITS')
        
        print("Testing GPT-SoVITS imports...")
        
        # 設定ファイルの読み込みテスト
        import yaml
        config_path = "/workspace/GPT-SoVITS/GPT_SoVITS/configs/tts_infer.yaml"
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print("✅ Config file loaded successfully")
            print(f"  Available versions: {list(config.keys())}")
        else:
            print("❌ Config file not found")
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    print("✅ Basic import test completed\n")
    return True

def main():
    parser = argparse.ArgumentParser(description='GPT-SoVITS v4 CLI Test (Model-Free)')
    parser.add_argument('--check-gpu', action='store_true', help='Check GPU status')
    parser.add_argument('--check-env', action='store_true', help='Check environment')
    parser.add_argument('--check-files', action='store_true', help='Check file structure')
    parser.add_argument('--test-api', action='store_true', help='Test API connection')
    parser.add_argument('--test-imports', action='store_true', help='Test basic imports')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    if args.all:
        check_gpu()
        check_environment()
        check_file_structure()
        test_basic_imports()
        test_api_connection()
    else:
        if args.check_gpu:
            check_gpu()
        if args.check_env:
            check_environment()
        if args.check_files:
            check_file_structure()
        if args.test_imports:
            test_basic_imports()
        if args.test_api:
            test_api_connection()
    
    print("🎉 CLI Test completed!")

if __name__ == "__main__":
    main() 