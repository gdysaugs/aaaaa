#!/usr/bin/env python3
"""
FaceFusion CLI詳細テストスクリプト
実際の画像・動画ファイルでface swapを確実に動作させるわよ！
"""
import os
import sys
import subprocess

# FaceFusionのパスを追加
facefusion_path = '/home/adama/LLM/aaaaa/facefusion-test/facefusion'
sys.path.insert(0, facefusion_path)

def test_files_existence():
    """テストファイルの存在確認"""
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
            print(f"✓ {os.path.basename(file_path)}: {size} bytes")
        else:
            print(f"✗ {os.path.basename(file_path)}: 見つかりません")
            all_exist = False
    
    return all_exist

def test_image_to_image_swap():
    """画像から画像への face swap テスト"""
    print("\n=== 画像→画像 Face Swap テスト ===")
    
    # 出力ディレクトリ作成
    output_dir = "/home/adama/LLM/aaaaa/facefusion-test/data/output"
    os.makedirs(output_dir, exist_ok=True)
    
    # パラメータ設定
    source_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/kanna-hashimoto.jpg"
    target_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/source1.jpg"
    output_path = "/home/adama/LLM/aaaaa/facefusion-test/data/output/image_to_image.jpg"
    
    print(f"ソース: {os.path.basename(source_path)}")
    print(f"ターゲット: {os.path.basename(target_path)}")
    print(f"出力: {os.path.basename(output_path)}")
    
    # コマンド構築
    cmd = [
        'python', 'facefusion.py',
        '--source-paths', source_path,
        '--target-path', target_path,
        '--output-path', output_path,
        '--processors', 'face_swapper',
        '--execution-providers', 'cuda',
        '--log-level', 'debug'
    ]
    
    print(f"実行コマンド: {' '.join(cmd)}")
    
    try:
        # FaceFusionディレクトリで実行
        result = subprocess.run(
            cmd,
            cwd=facefusion_path,
            capture_output=True,
            text=True,
            timeout=300  # 5分タイムアウト
        )
        
        print(f"リターンコード: {result.returncode}")
        
        if result.stdout:
            print("=== 標準出力 ===")
            print(result.stdout)
        
        if result.stderr:
            print("=== エラー出力 ===")
            print(result.stderr)
        
        # 結果確認
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✓ 成功！出力ファイル生成: {size} bytes")
            return True
        else:
            print("✗ 出力ファイルが生成されませんでした")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 処理がタイムアウトしました")
        return False
    except Exception as e:
        print(f"✗ 実行エラー: {e}")
        return False

def test_image_to_video_swap():
    """画像から動画への face swap テスト"""
    print("\n=== 画像→動画 Face Swap テスト ===")
    
    # パラメータ設定
    source_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/kanna-hashimoto.jpg"
    target_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/test_video.mp4"
    output_path = "/home/adama/LLM/aaaaa/facefusion-test/data/output/image_to_video.mp4"
    
    print(f"ソース: {os.path.basename(source_path)}")
    print(f"ターゲット: {os.path.basename(target_path)}")
    print(f"出力: {os.path.basename(output_path)}")
    
    # コマンド構築
    cmd = [
        'python', 'facefusion.py',
        '--source-paths', source_path,
        '--target-path', target_path,
        '--output-path', output_path,
        '--processors', 'face_swapper',
        '--execution-providers', 'cuda',
        '--log-level', 'debug',
        '--trim-frame-start', '0',
        '--trim-frame-end', '30',  # 最初の30フレームのみ処理
        '--output-video-quality', '80'
    ]
    
    print(f"実行コマンド: {' '.join(cmd)}")
    
    try:
        # FaceFusionディレクトリで実行
        result = subprocess.run(
            cmd,
            cwd=facefusion_path,
            capture_output=True,
            text=True,
            timeout=600  # 10分タイムアウト
        )
        
        print(f"リターンコード: {result.returncode}")
        
        if result.stdout:
            print("=== 標準出力 ===")
            print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        
        if result.stderr:
            print("=== エラー出力 ===")
            print(result.stderr[:500] + "..." if len(result.stderr) > 500 else result.stderr)
        
        # 結果確認
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✓ 成功！出力動画生成: {size} bytes")
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

def test_help_command():
    """ヘルプコマンドテスト"""
    print("\n=== ヘルプコマンドテスト ===")
    
    try:
        result = subprocess.run(
            ['python', 'facefusion.py', '--help'],
            cwd=facefusion_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout:
            print("✓ ヘルプコマンド正常動作")
            print("使用可能なオプション数:", result.stdout.count('--'))
            return True
        else:
            print("✗ ヘルプコマンドが正常に動作しません")
            print(f"stdout: {result.stdout[:200]}...")
            print(f"stderr: {result.stderr[:200]}...")
            return False
            
    except Exception as e:
        print(f"✗ ヘルプコマンドエラー: {e}")
        return False

def main():
    print("=" * 70)
    print("🎯 FaceFusion CLI 実戦テスト")
    print("作成者: ツンデレAI (べ、べつにあなたのためじゃないんだからね！)")
    print("=" * 70)
    
    success_count = 0
    total_tests = 4
    
    # テスト実行
    if test_files_existence():
        success_count += 1
    
    if test_help_command():
        success_count += 1
    
    if test_image_to_image_swap():
        success_count += 1
    
    if test_image_to_video_swap():
        success_count += 1
    
    # 最終結果
    print("\n" + "=" * 70)
    print(f"🏆 テスト結果: {success_count}/{total_tests} 成功")
    
    if success_count == total_tests:
        print("🎉 完全成功！FaceFusionのCLI face swapが完璧に動作確認！")
        print("🚀 画像→画像、画像→動画の両方が利用可能です！")
    elif success_count >= 2:
        print("⚡ 部分的成功！基本機能は動作しています")
    else:
        print("❌ 修正が必要です。詳細なエラーログを確認してください")
    
    print("=" * 70)

if __name__ == "__main__":
    main() 