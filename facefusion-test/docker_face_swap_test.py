#!/usr/bin/env python3
"""
FaceFusion Docker GPU顔交換テストスクリプト
Dockerコンテナを使って実際の画像・動画ファイルでface swapをGPUで動作させるわよ！
"""
import os
import sys
import subprocess
import time

# 現在のパス設定
BASE_PATH = '/home/adamna/LLM/facefusion-test'
SOURCE_PATH = f'{BASE_PATH}/data/source'
OUTPUT_PATH = f'{BASE_PATH}/data/output'

def check_docker_and_gpu():
    """DockerとGPU使用可能性確認"""
    print("=== Docker & GPU確認 ===")
    
    # Docker確認
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Docker: {result.stdout.strip()}")
        else:
            print("✗ Docker未検出")
            return False
    except FileNotFoundError:
        print("✗ Docker コマンドが見つかりません")
        return False
    
    # NVIDIA Docker確認
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

def check_docker_image():
    """FaceFusion Dockerイメージ確認"""
    print("\n=== Docker Image確認 ===")
    
    try:
        result = subprocess.run(
            ['docker', 'images', '--format', 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}'],
            capture_output=True, text=True
        )
        
        if 'facefusion' in result.stdout:
            print("✓ FaceFusion Dockerイメージが見つかりました:")
            for line in result.stdout.split('\n'):
                if 'facefusion' in line:
                    print(f"  {line}")
            return True
        else:
            print("✗ FaceFusion Dockerイメージが見つかりません")
            return False
            
    except Exception as e:
        print(f"✗ Docker image確認エラー: {e}")
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

def test_docker_face_swap():
    """Docker経由で顔交換テスト"""
    print("\n=== Docker FaceFusion 顔交換テスト ===")
    
    # ファイルパス設定（Dockerコンテナ内から見えるパス）
    source_image = "kanna-hashimoto.jpg"
    target_video = "画面録画 2025-05-16 222902.mp4"
    output_video = "docker_face_swap_result.mp4"
    
    print(f"ソース画像: {source_image}")
    print(f"ターゲット動画: {target_video}")
    print(f"出力動画: {output_video}")
    
    # 既存の出力ファイルを削除
    output_full_path = f"{OUTPUT_PATH}/{output_video}"
    if os.path.exists(output_full_path):
        os.remove(output_full_path)
        print("既存の出力ファイルを削除しました")
    
    # Dockerコマンド構築（正しいFaceFusion形式）
    cmd = [
        'docker', 'run', '--rm',
        '--gpus', 'all',  # GPU使用
        '-v', f'{SOURCE_PATH}:/app/input',     # ソースファイル
        '-v', f'{OUTPUT_PATH}:/app/output',    # 出力ディレクトリ
        'facefusion:cuda11.8-optimized',
        'python3', 'facefusion.py', 'run',
        '--source-paths', f'/app/input/{source_image}',
        '--target-path', f'/app/input/{target_video}',
        '--output-path', f'/app/output/{output_video}',
        '--processors', 'face_swapper',
        '--execution-providers', 'cuda',
        '--execution-thread-count', '4',
        '--face-detector-model', 'retinaface',
        '--face-swapper-model', 'inswapper_128',
        '--log-level', 'info'
    ]
    
    print(f"実行コマンド: {' '.join(cmd)}")
    print("Docker処理開始...")
    
    start_time = time.time()
    
    try:
        # Dockerコンテナで実行
        result = subprocess.run(
            cmd,
            text=True,
            timeout=900  # 15分タイムアウト
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"処理時間: {processing_time:.2f}秒")
        print(f"リターンコード: {result.returncode}")
        
        # 結果確認
        if os.path.exists(output_full_path):
            size = os.path.getsize(output_full_path)
            print(f"✓ 成功！出力動画生成: {size:,} bytes")
            print(f"出力パス: {output_full_path}")
            return True
        else:
            print("✗ 出力動画が生成されませんでした")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 処理がタイムアウトしました（15分）")
        return False
    except Exception as e:
        print(f"✗ 実行エラー: {e}")
        return False

def test_docker_help():
    """Docker FaceFusion ヘルプテスト"""
    print("\n=== Docker FaceFusion ヘルプテスト ===")
    
    try:
        result = subprocess.run(
            ['docker', 'run', '--rm', 'facefusion:cuda11.8-optimized', 'python3', 'facefusion.py', '--help'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✓ Docker FaceFusion ヘルプコマンド正常動作")
            # ヘルプの一部を表示
            help_lines = result.stdout.split('\n')[:10]
            print("ヘルプ出力（最初の10行）:")
            for line in help_lines:
                print(f"  {line}")
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
    print("🎯 FaceFusion Docker GPU 顔交換テスト")
    print("作成者: ツンデレAI (べ、べつにあなたのためじゃないんだからね！)")
    print("=" * 80)
    
    # Docker & GPU確認
    docker_gpu_ok = check_docker_and_gpu()
    if not docker_gpu_ok:
        print("❌ DockerまたはGPUが利用できません。処理を中断します。")
        return
    
    # Dockerイメージ確認
    image_ok = check_docker_image()
    if not image_ok:
        print("❌ FaceFusion Dockerイメージが見つかりません。処理を中断します。")
        return
    
    # ファイル確認
    files_ok = test_files_existence()
    if not files_ok:
        print("❌ 必要なファイルが不足しています。処理を中断します。")
        return
    
    # ヘルプテスト
    print("\n" + "="*50)
    help_success = test_docker_help()
    
    # メイン処理
    print("\n" + "="*50)
    swap_success = test_docker_face_swap()
    
    # 結果サマリー
    print("\n" + "="*80)
    print("📊 テスト結果サマリー")
    print("="*80)
    print(f"Docker & GPU: {'✓' if docker_gpu_ok else '✗'}")
    print(f"Dockerイメージ: {'✓' if image_ok else '✗'}")
    print(f"テストファイル: {'✓' if files_ok else '✗'}")
    print(f"ヘルプコマンド: {'✓' if help_success else '✗'}")
    print(f"顔交換処理: {'✓' if swap_success else '✗'}")
    
    if swap_success:
        print("\n🎉 おめでとう！Docker顔交換テストが成功したわよ！")
        print(f"出力ファイル: {OUTPUT_PATH}/docker_face_swap_result.mp4")
        print("これでRTX3050のGPUパワーを使って顔交換ができたのよ！")
    else:
        print("\n💢 ちっ...何か問題があったみたいね...")
        print("Dockerコンテナのログやパラメータを確認してみなさい！")
    
    print("="*80)

if __name__ == "__main__":
    main() 