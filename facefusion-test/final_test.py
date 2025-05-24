#!/usr/bin/env python3
"""
FaceFusion v3.2.0 最終動作テスト
正しいコマンド形式でface swapを実行するわよ！
作成者: ツンデレAI (べ、別にあなたのためじゃないからね！)
"""
import os
import sys
import subprocess
import time

def test_webui_startup():
    """WebUI起動テスト"""
    print("=== WebUI起動テスト ===")
    
    try:
        # WebUIを短時間起動してみる
        proc = subprocess.Popen(
            ['python', 'facefusion.py', '--ui-layouts', 'default'],
            cwd='/home/adama/LLM/aaaaa/facefusion-test/facefusion',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 5秒待機
        time.sleep(5)
        
        # プロセス状態確認
        if proc.poll() is None:
            print("✓ WebUI正常起動中")
            proc.terminate()
            proc.wait(timeout=10)
            return True
        else:
            stdout, stderr = proc.communicate()
            print(f"✗ WebUI起動失敗")
            print(f"stdout: {stdout[:200]}...")
            print(f"stderr: {stderr[:200]}...")
            return False
            
    except Exception as e:
        print(f"✗ WebUI起動エラー: {e}")
        return False

def test_headless_image_swap():
    """ヘッドレス画像face swapテスト"""
    print("\n=== ヘッドレス画像 Face Swap テスト ===")
    
    # 出力ディレクトリ作成
    output_dir = "/home/adama/LLM/aaaaa/facefusion-test/data/output"
    os.makedirs(output_dir, exist_ok=True)
    
    # パラメータ設定
    source_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/kanna-hashimoto.jpg"
    target_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/source1.jpg"
    output_path = "/home/adama/LLM/aaaaa/facefusion-test/data/output/headless_image.jpg"
    
    print(f"ソース: {os.path.basename(source_path)}")
    print(f"ターゲット: {os.path.basename(target_path)}")
    print(f"出力: {os.path.basename(output_path)}")
    
    # コマンド実行
    cmd = [
        'python', 'facefusion.py', 'headless-run',
        '--source-paths', source_path,
        '--target-path', target_path,
        '--output-path', output_path,
        '--processors', 'face_swapper',
        '--execution-providers', 'cuda',
        '--face-swapper-model', 'inswapper_128'
    ]
    
    print(f"実行コマンド: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd='/home/adama/LLM/aaaaa/facefusion-test/facefusion',
            capture_output=True,
            text=True,
            timeout=180
        )
        
        print(f"リターンコード: {result.returncode}")
        
        if result.stdout:
            print("=== 標準出力 ===")
            print(result.stdout[:300] + "..." if len(result.stdout) > 300 else result.stdout)
        
        if result.stderr:
            print("=== エラー出力 ===")
            print(result.stderr[:300] + "..." if len(result.stderr) > 300 else result.stderr)
        
        # 結果確認
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✓ 成功！画像face swap完了: {size} bytes")
            return True
        else:
            print("✗ 出力画像が生成されませんでした")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 処理がタイムアウトしました")
        return False
    except Exception as e:
        print(f"✗ 実行エラー: {e}")
        return False

def test_headless_video_swap():
    """ヘッドレス動画face swapテスト"""
    print("\n=== ヘッドレス動画 Face Swap テスト ===")
    
    # パラメータ設定
    source_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/kanna-hashimoto.jpg"
    target_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/test_video.mp4"
    output_path = "/home/adama/LLM/aaaaa/facefusion-test/data/output/headless_video.mp4"
    
    print(f"ソース: {os.path.basename(source_path)}")
    print(f"ターゲット: {os.path.basename(target_path)}")
    print(f"出力: {os.path.basename(output_path)}")
    
    # コマンド実行
    cmd = [
        'python', 'facefusion.py', 'headless-run',
        '--source-paths', source_path,
        '--target-path', target_path,
        '--output-path', output_path,
        '--processors', 'face_swapper',
        '--execution-providers', 'cuda',
        '--face-swapper-model', 'inswapper_128',
        '--trim-frame-start', '0',
        '--trim-frame-end', '30',  # 最初の30フレームのみ
        '--output-video-quality', '80'
    ]
    
    print(f"実行コマンド: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd='/home/adama/LLM/aaaaa/facefusion-test/facefusion',
            capture_output=True,
            text=True,
            timeout=300
        )
        
        print(f"リターンコード: {result.returncode}")
        
        if result.stdout:
            print("=== 標準出力 ===")
            print(result.stdout[:300] + "..." if len(result.stdout) > 300 else result.stdout)
        
        if result.stderr:
            print("=== エラー出力 ===")
            print(result.stderr[:300] + "..." if len(result.stderr) > 300 else result.stderr)
        
        # 結果確認
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✓ 成功！動画face swap完了: {size} bytes")
            return True
        else:
            print("✗ 出力動画が生成されませんでした")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 処理がタイムアウトしました")
        return False
    except Exception as e:
        print(f"✗ 実行エラー: {e}")
        return False

def test_available_commands():
    """利用可能なコマンド一覧テスト"""
    print("\n=== 利用可能コマンド確認 ===")
    
    try:
        result = subprocess.run(
            ['python', 'facefusion.py', '--help'],
            cwd='/home/adama/LLM/aaaaa/facefusion-test/facefusion',
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout:
            print("利用可能なコマンド:")
            for line in result.stdout.split('\n'):
                if '{' in line and '}' in line:
                    print(f"  {line.strip()}")
            return True
        else:
            print("✗ コマンド一覧取得失敗")
            return False
            
    except Exception as e:
        print(f"✗ コマンド確認エラー: {e}")
        return False

def check_files():
    """ファイル存在確認"""
    print("=== ファイル存在確認 ===")
    
    files_to_check = [
        "/home/adama/LLM/aaaaa/facefusion-test/data/source/kanna-hashimoto.jpg",
        "/home/adama/LLM/aaaaa/facefusion-test/data/source/source1.jpg",
        "/home/adama/LLM/aaaaa/facefusion-test/data/source/test_video.mp4",
        os.path.expanduser("~/.facefusion/models/inswapper_128.onnx")
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {os.path.basename(file_path)}: {size:,} bytes")
        else:
            print(f"✗ {os.path.basename(file_path)}: 見つかりません")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 80)
    print("🎯 FaceFusion v3.2.0 完全動作テスト")
    print("実際の画像・動画ファイルでface swapを確実に実行します！")
    print("作成者: ツンデレAI (べ、別にあなたのためじゃないからね...)")
    print("=" * 80)
    
    success_count = 0
    total_tests = 4
    
    # ファイル確認
    if check_files():
        success_count += 1
    
    # コマンド確認
    if test_available_commands():
        success_count += 1
    
    # 画像face swapテスト
    if test_headless_image_swap():
        success_count += 1
    
    # 動画face swapテスト
    if test_headless_video_swap():
        success_count += 1
    
    # 最終結果
    print("\n" + "=" * 80)
    print(f"🏆 最終テスト結果: {success_count}/{total_tests} 成功")
    
    if success_count == total_tests:
        print("🎉 完全成功！FaceFusionのface swapが完璧に動作しています！")
        print("🚀 画像→画像、画像→動画の両方のface swapが利用可能です！")
        print("💫 実際のファイルでの顔交換処理が可能になりました！")
    elif success_count >= 2:
        print("⚡ 部分的成功！基本機能は動作しています")
        print("🔧 一部調整が必要ですが、メイン機能は利用可能です")
    else:
        print("❌ さらなる調整が必要です")
        print("🔍 詳細なエラーログを確認して問題を解決しましょう")
    
    print("=" * 80)

if __name__ == "__main__":
    main() 