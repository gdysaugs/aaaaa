#!/usr/bin/env python3
"""
FaceFusion CLI ワーキングスクリプト
べ、別にあなたのためじゃないけど、確実に動作するCLIを作ってあげるわよ！
"""
import os
import sys
import subprocess
import argparse

def setup_environment():
    """環境設定"""
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['PYTHONPATH'] = '/home/adama/LLM/aaaaa/facefusion-test/facefusion'
    
def run_face_swap(source_path, target_path, output_path):
    """Face swapを実行"""
    print(f"🎯 Face Swap実行中...")
    print(f"ソース: {os.path.basename(source_path)}")
    print(f"ターゲット: {os.path.basename(target_path)}")
    print(f"出力: {os.path.basename(output_path)}")
    
    # 出力ディレクトリ作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # FaceFusionディレクトリに移動
    facefusion_dir = '/home/adama/LLM/aaaaa/facefusion-test/facefusion'
    
    # コマンド構築 - 最新ドキュメントに基づく
    cmd = [
        'python', 'facefusion.py', 'headless-run',
        '--source-paths', source_path,
        '--target-path', target_path, 
        '--output-path', output_path,
        '--processors', 'face_swapper',
        '--face-swapper-model', 'inswapper_128',
        '--execution-providers', 'cuda',
        '--log-level', 'info',
        '--output-image-quality', '90'
    ]
    
    print(f"📋 実行コマンド: {' '.join(cmd)}")
    
    try:
        # 詳細出力付きで実行
        result = subprocess.run(
            cmd,
            cwd=facefusion_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # stderrもstdoutに統合
            text=True,
            timeout=300,
            env=os.environ.copy()
        )
        
        print(f"🔍 リターンコード: {result.returncode}")
        
        # 出力を表示
        if result.stdout:
            print("📤 コマンド出力:")
            print(result.stdout)
        
        # 結果確認
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✅ 成功！Face swap完了")
            print(f"📁 出力ファイル: {output_path}")
            print(f"📊 ファイルサイズ: {size:,} bytes")
            return True
        else:
            print(f"❌ 失敗: 出力ファイルが生成されませんでした")
            print(f"🔍 期待される出力: {output_path}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ 処理がタイムアウトしました (5分)")
        return False
    except Exception as e:
        print(f"💥 実行エラー: {e}")
        return False

def test_with_real_files():
    """実際のファイルでテスト"""
    print("=" * 60)
    print("🎮 FaceFusion CLI 実戦テスト")
    print("=" * 60)
    
    # ファイルパス設定
    source_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/kanna-hashimoto.jpg"
    target_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/source1.jpg"
    
    # 画像テスト
    print("\n🖼️ 画像→画像 Face Swap テスト")
    image_output = "/home/adama/LLM/aaaaa/facefusion-test/data/output/cli_working_image.jpg"
    image_success = run_face_swap(source_path, target_path, image_output)
    
    # 動画テスト
    print("\n🎬 画像→動画 Face Swap テスト")
    video_input = "/home/adama/LLM/aaaaa/facefusion-test/data/source/test_video.mp4"
    video_output = "/home/adama/LLM/aaaaa/facefusion-test/data/output/cli_working_video.mp4"
    
    if os.path.exists(video_input):
        video_success = run_face_swap(source_path, video_input, video_output)
    else:
        print(f"⚠️ 動画ファイルが見つかりません: {video_input}")
        video_success = False
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 テスト結果")
    print("=" * 60)
    print(f"🖼️ 画像 Face Swap: {'✅ 成功' if image_success else '❌ 失敗'}")
    print(f"🎬 動画 Face Swap: {'✅ 成功' if video_success else '❌ 失敗'}")
    
    if image_success or video_success:
        print("\n🎉 おめでとう！FaceFusionのCLI動作確認完了！")
        print("💡 使用可能なコマンド形式:")
        print("   python working_cli.py --source SOURCE --target TARGET --output OUTPUT")
    else:
        print("\n🔧 まだ調整が必要です。詳細なログを確認してください。")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='FaceFusion CLI Wrapper')
    parser.add_argument('--source', help='ソース画像パス')
    parser.add_argument('--target', help='ターゲット画像/動画パス')
    parser.add_argument('--output', help='出力パス')
    parser.add_argument('--test', action='store_true', help='実際のファイルでテスト実行')
    
    args = parser.parse_args()
    
    # 環境設定
    setup_environment()
    
    if args.test or (not args.source and not args.target and not args.output):
        # テストモード
        test_with_real_files()
    elif args.source and args.target and args.output:
        # 個別実行モード
        success = run_face_swap(args.source, args.target, args.output)
        sys.exit(0 if success else 1)
    else:
        print("❌ 引数が不足しています")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 