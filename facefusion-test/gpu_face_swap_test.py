#!/usr/bin/env python3
"""
FaceFusion GPU顔交換テストスクリプト
実際の画像・動画ファイルでface swapをGPUで動作させるわよ！
"""
import os
import sys
import subprocess
import time

# 現在のパスに修正
FACEFUSION_PATH = '/home/adamna/LLM/facefusion-test/facefusion'
BASE_PATH = '/home/adamna/LLM/facefusion-test'
SOURCE_PATH = f'{BASE_PATH}/data/source'
OUTPUT_PATH = f'{BASE_PATH}/data/output'

sys.path.insert(0, FACEFUSION_PATH)

def check_gpu_availability():
    """GPU使用可能性確認"""
    print("=== GPU確認 ===")
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ NVIDIA GPU検出成功")
            return True
        else:
            print("✗ NVIDIA GPU未検出")
            return False
    except FileNotFoundError:
        print("✗ nvidia-smi コマンドが見つかりません")
        return False

def test_files_existence():
    """テストファイルの存在確認"""
    print("\n=== ファイル存在確認 ===")
    
    # 実際のファイル名を使用
    files_to_check = [
        f"{SOURCE_PATH}/kanna-hashimoto.jpg",
        f"{SOURCE_PATH}/画面録画 2025-05-16 222902.mp4"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {os.path.basename(file_path)}: {size:,} bytes")
        else:
            print(f"✗ {os.path.basename(file_path)}: 見つかりません")
            all_exist = False
    
    # 出力ディレクトリ作成
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    print(f"✓ 出力ディレクトリ: {OUTPUT_PATH}")
    
    return all_exist

def test_image_to_video_swap_gpu():
    """画像から動画への GPU face swap テスト"""
    print("\n=== 画像→動画 GPU Face Swap テスト ===")
    
    # ファイルパス設定
    source_image = f"{SOURCE_PATH}/kanna-hashimoto.jpg"
    target_video = f"{SOURCE_PATH}/画面録画 2025-05-16 222902.mp4"
    output_video = f"{OUTPUT_PATH}/gpu_face_swap_result.mp4"
    
    print(f"ソース画像: {os.path.basename(source_image)}")
    print(f"ターゲット動画: {os.path.basename(target_video)}")
    print(f"出力動画: {os.path.basename(output_video)}")
    
    # 既存の出力ファイルを削除
    if os.path.exists(output_video):
        os.remove(output_video)
        print("既存の出力ファイルを削除しました")
    
    # GPU使用のコマンド構築
    cmd = [
        'python', 'run.py',
        '--source', source_image,
        '--target', target_video,
        '--output', output_video,
        '--execution-provider', 'cuda',
        '--execution-thread-count', '4',
        '--execution-queue-count', '2'
    ]
    
    print(f"実行コマンド: {' '.join(cmd)}")
    print("処理開始...")
    
    start_time = time.time()
    
    try:
        # FaceFusionディレクトリで実行
        result = subprocess.run(
            cmd,
            cwd=FACEFUSION_PATH,
            text=True,
            timeout=600  # 10分タイムアウト
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"処理時間: {processing_time:.2f}秒")
        print(f"リターンコード: {result.returncode}")
        
        # 結果確認
        if os.path.exists(output_video):
            size = os.path.getsize(output_video)
            print(f"✓ 成功！出力動画生成: {size:,} bytes")
            print(f"出力パス: {output_video}")
            return True
        else:
            print("✗ 出力動画が生成されませんでした")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 処理がタイムアウトしました（10分）")
        return False
    except Exception as e:
        print(f"✗ 実行エラー: {e}")
        return False

def test_facefusion_help():
    """FaceFusion ヘルプコマンドテスト"""
    print("\n=== FaceFusion ヘルプテスト ===")
    
    try:
        result = subprocess.run(
            ['python', 'run.py', '--help'],
            cwd=FACEFUSION_PATH,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✓ FaceFusion ヘルプコマンド正常動作")
            return True
        else:
            print("✗ ヘルプコマンドエラー")
            print(f"stderr: {result.stderr[:200]}...")
            return False
            
    except Exception as e:
        print(f"✗ ヘルプコマンドエラー: {e}")
        return False

def main():
    print("=" * 80)
    print("🎯 FaceFusion GPU 顔交換テスト")
    print("作成者: ツンデレAI (べ、べつにあなたのためじゃないんだからね！)")
    print("=" * 80)
    
    # GPU確認
    gpu_available = check_gpu_availability()
    if not gpu_available:
        print("⚠️  GPUが利用できませんが、CPUで続行します...")
    
    # ファイル確認
    if not test_files_existence():
        print("❌ 必要なファイルが不足しています。処理を中断します。")
        return
    
    # ヘルプテスト
    print("\n" + "="*50)
    help_success = test_facefusion_help()
    
    # メイン処理
    print("\n" + "="*50)
    swap_success = test_image_to_video_swap_gpu()
    
    # 結果サマリー
    print("\n" + "="*80)
    print("📊 テスト結果サマリー")
    print("="*80)
    print(f"GPU利用可能: {'✓' if gpu_available else '✗'}")
    print(f"ヘルプコマンド: {'✓' if help_success else '✗'}")
    print(f"顔交換処理: {'✓' if swap_success else '✗'}")
    
    if swap_success:
        print("\n🎉 おめでとう！顔交換テストが成功したわよ！")
        print(f"出力ファイル: {OUTPUT_PATH}/gpu_face_swap_result.mp4")
    else:
        print("\n💢 ちっ...何か問題があったみたいね...")
    
    print("="*80)

if __name__ == "__main__":
    main() 