#!/usr/bin/env python3
"""
FaceFusion ダウンロード問題の診断スクリプト
あら...問題解決のお手伝いなんて、べ、別にあなたのためじゃないんだからね！
"""
import os
import subprocess
import sys
import time
import signal
from pathlib import Path

def signal_handler(sig, frame):
    print("\n[DEBUG] 強制終了されました...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def check_model_files():
    """モデルファイルの状態をチェック"""
    print("[DEBUG] モデルファイルの状態をチェック中...")
    
    # 一般的なモデル保存場所をチェック
    model_paths = [
        os.path.expanduser("~/.facefusion/models"),
        "./models",
        "./facefusion/models", 
        os.path.expanduser("~/.insightface/models"),
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            print(f"[DEBUG] 発見: {path}")
            for file in os.listdir(path):
                print(f"  - {file} ({os.path.getsize(os.path.join(path, file))} bytes)")
        else:
            print(f"[DEBUG] 存在しない: {path}")

def check_running_processes():
    """実行中のcurlプロセスをチェック"""
    print("[DEBUG] 実行中のcurlプロセスをチェック...")
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        curl_processes = [line for line in result.stdout.split('\n') if 'curl' in line and 'facefusion' in line]
        
        if curl_processes:
            print("[DEBUG] 発見されたcurlプロセス:")
            for process in curl_processes:
                print(f"  {process}")
        else:
            print("[DEBUG] curlプロセスは見つかりませんでした")
    except Exception as e:
        print(f"[DEBUG] プロセスチェックエラー: {e}")

def test_network_connectivity():
    """ネットワーク接続性をテスト"""
    print("[DEBUG] ネットワーク接続性をテスト中...")
    
    test_urls = [
        "https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx",
        "https://huggingface.co/uwg/upscaler/resolve/main/Face_Restore/FaceFusion/inswapper_128.onnx",
        "https://drive.google.com/file/d/1krOLgjW2tAPaqV-Bw4YALz0xT5zlb5HF/view"
    ]
    
    for url in test_urls:
        try:
            print(f"[DEBUG] テスト中: {url}")
            result = subprocess.run(['curl', '-I', '--connect-timeout', '5', url], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                status_line = result.stdout.split('\n')[0]
                print(f"  ✓ 応答: {status_line}")
            else:
                print(f"  ✗ 失敗: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"  ✗ タイムアウト")
        except Exception as e:
            print(f"  ✗ エラー: {e}")

def check_facefusion_config():
    """FaceFusionの設定をチェック"""
    print("[DEBUG] FaceFusion設定をチェック中...")
    
    config_file = "./facefusion/facefusion.ini"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            content = f.read()
            print(f"[DEBUG] 設定ファイルサイズ: {len(content)} 文字")
            
            # 重要な設定をチェック
            important_keys = ['download_providers', 'log_level', 'execution_providers']
            for key in important_keys:
                if f"{key} =" in content:
                    lines = content.split('\n')
                    for line in lines:
                        if line.strip().startswith(f"{key} ="):
                            print(f"  {key}: {line.strip()}")
    else:
        print("[DEBUG] 設定ファイルが見つかりません")

def simulate_download_process():
    """ダウンロードプロセスをシミュレート"""
    print("[DEBUG] ダウンロードプロセスのシミュレーション...")
    
    # 簡単なcurlテストでタイムアウト動作を確認
    test_url = "https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx"
    
    print(f"[DEBUG] テストダウンロード開始: {test_url}")
    start_time = time.time()
    
    try:
        # FaceFusionと同じcurlオプションを使用
        cmd = [
            'curl', 
            '--user-agent', 'facefusion/3.2.0',
            '--insecure',
            '--location', 
            '--silent',
            '--connect-timeout', '10',
            '--head',  # ヘッダーのみ取得
            test_url
        ]
        
        print(f"[DEBUG] 実行コマンド: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        elapsed = time.time() - start_time
        print(f"[DEBUG] 完了時間: {elapsed:.2f}秒")
        print(f"[DEBUG] リターンコード: {result.returncode}")
        
        if result.stdout:
            print(f"[DEBUG] レスポンスヘッダー:")
            for line in result.stdout.split('\n')[:5]:  # 最初の5行のみ表示
                if line.strip():
                    print(f"  {line}")
                    
    except subprocess.TimeoutExpired:
        print("[DEBUG] ✗ タイムアウトが発生しました")
    except Exception as e:
        print(f"[DEBUG] ✗ エラー: {e}")

def main():
    print("=" * 60)
    print("FaceFusion ダウンロード問題診断スクリプト")
    print("開発者: ツンデレAI (べ、別にあなたのためじゃないんだからね！)")
    print("=" * 60)
    
    print("\n1. モデルファイル状態チェック")
    check_model_files()
    
    print("\n2. 実行中プロセスチェック")
    check_running_processes()
    
    print("\n3. ネットワーク接続性テスト")
    test_network_connectivity()
    
    print("\n4. FaceFusion設定チェック")
    check_facefusion_config()
    
    print("\n5. ダウンロードプロセスシミュレーション")
    simulate_download_process()
    
    print("\n" + "=" * 60)
    print("診断完了！")
    print("問題が特定できない場合は、より詳細なログを有効にしてFaceFusionを再実行してみて")
    print("=" * 60)

if __name__ == "__main__":
    main() 