#!/usr/bin/env python3
"""
FaceFusion v3.2.0 JOB-based CLI
べ、別にあなたのためじゃないけど、最新のJOBベースアーキテクチャで動作させてあげるわよ！
参考: https://github.com/facefusion/facefusion
"""
import os
import sys
import subprocess
import argparse
import time

def run_job_based_face_swap(source_path, target_path, output_path):
    """JOBベースのFace Swap実行"""
    print(f"🎯 JOB-based Face Swap実行中...")
    print(f"ソース: {os.path.basename(source_path)}")
    print(f"ターゲット: {os.path.basename(target_path)}")
    print(f"出力: {os.path.basename(output_path)}")
    
    # 出力ディレクトリ作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    facefusion_dir = '/home/adama/LLM/aaaaa/facefusion-test/facefusion'
    
    try:
        # ステップ1: JOB作成
        print("📝 ステップ1: JOB作成中...")
        job_create_cmd = [
            'python', 'facefusion.py', 'job-create',
            '--source-paths', source_path,
            '--target-path', target_path,
            '--output-path', output_path,
            '--processors', 'face_swapper',
            '--face-swapper-model', 'inswapper_128',
            '--execution-providers', 'cuda'
        ]
        
        result = subprocess.run(
            job_create_cmd,
            cwd=facefusion_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(f"JOB作成結果: {result.returncode}")
        if result.stdout:
            print(f"stdout: {result.stdout}")
        if result.stderr:
            print(f"stderr: {result.stderr}")
        
        # ステップ2: JOB一覧確認
        print("📋 ステップ2: JOB一覧確認...")
        job_list_cmd = ['python', 'facefusion.py', 'job-list']
        
        result = subprocess.run(
            job_list_cmd,
            cwd=facefusion_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"JOB一覧結果: {result.returncode}")
        if result.stdout:
            print(f"JOB一覧:\n{result.stdout}")
        
        # ステップ3: JOB実行
        print("🚀 ステップ3: JOB実行中...")
        job_run_cmd = ['python', 'facefusion.py', 'job-run-all']
        
        result = subprocess.run(
            job_run_cmd,
            cwd=facefusion_dir,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        print(f"JOB実行結果: {result.returncode}")
        if result.stdout:
            print(f"JOB実行出力:\n{result.stdout}")
        if result.stderr:
            print(f"JOB実行エラー:\n{result.stderr}")
        
        # 結果確認
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✅ JOBベース Face Swap 成功！")
            print(f"📁 出力: {output_path}")
            print(f"📊 サイズ: {size:,} bytes")
            return True
        else:
            print(f"❌ JOBベース処理完了後も出力ファイルが見つかりません")
            return False
            
    except Exception as e:
        print(f"💥 JOBベース実行エラー: {e}")
        return False

def alternative_direct_method(source_path, target_path, output_path):
    """代替手法: 直接的なface swap"""
    print(f"\n🔄 代替手法: 直接実行方式")
    
    facefusion_dir = '/home/adama/LLM/aaaaa/facefusion-test/facefusion'
    
    # Python内部から直接実行
    script_content = f'''
import sys
import os
sys.path.insert(0, '{facefusion_dir}')
os.chdir('{facefusion_dir}')

try:
    # 環境変数設定
    os.environ["OMP_NUM_THREADS"] = "1"
    
    # FaceFusionモジュールをインポート
    import facefusion
    from facefusion import core, program, state_manager
    
    print("✓ FaceFusion modules loaded")
    
    # 仮想的な引数設定
    sys.argv = [
        'facefusion.py', 'headless-run',
        '--source-paths', '{source_path}',
        '--target-path', '{target_path}',
        '--output-path', '{output_path}',
        '--processors', 'face_swapper',
        '--face-swapper-model', 'inswapper_128',
        '--execution-providers', 'cpu',  # 安全のためCPU
        '--log-level', 'info'
    ]
    
    print("✓ Arguments set")
    
    # プログラム実行
    parser = program.create_program()
    args = parser.parse_args(sys.argv[1:])
    
    print("✓ Arguments parsed")
    print("🚀 Starting face swap process...")
    
    # コア実行
    core.apply_execution_provider(args.execution_providers)
    core.apply_log_level(args.log_level)
    
    print("✓ Configuration applied")
    
except Exception as e:
    print(f"❌ Direct method error: {{e}}")
    import traceback
    traceback.print_exc()
'''
    
    try:
        with open('/tmp/direct_facefusion.py', 'w') as f:
            f.write(script_content)
        
        result = subprocess.run(
            ['python', '/tmp/direct_facefusion.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        print(f"代替手法結果: {result.returncode}")
        if result.stdout:
            print(f"出力:\n{result.stdout}")
        if result.stderr:
            print(f"エラー:\n{result.stderr}")
        
        return os.path.exists(output_path)
        
    except Exception as e:
        print(f"代替手法エラー: {e}")
        return False

def main():
    """メイン実行"""
    print("=" * 80)
    print("🎮 FaceFusion v3.2.0 JOB-based CLI 完全テスト")
    print("参考: https://github.com/facefusion/facefusion")
    print("=" * 80)
    
    # テストファイル設定
    source_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/kanna-hashimoto.jpg"
    target_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/source1.jpg"
    
    # 方式1: JOBベース
    print("\n🎯 方式1: JOBベースアーキテクチャ")
    job_output = "/home/adama/LLM/aaaaa/facefusion-test/data/output/job_based_result.jpg"
    job_success = run_job_based_face_swap(source_path, target_path, job_output)
    
    # 方式2: 代替手法
    if not job_success:
        print("\n🔄 方式2: 代替実行手法")
        alt_output = "/home/adama/LLM/aaaaa/facefusion-test/data/output/alternative_result.jpg"
        alt_success = alternative_direct_method(source_path, target_path, alt_output)
    else:
        alt_success = False
    
    # 最終結果
    print("\n" + "=" * 80)
    print("📊 最終結果")
    print("=" * 80)
    print(f"🎯 JOBベース方式: {'✅ 成功' if job_success else '❌ 失敗'}")
    print(f"🔄 代替実行方式: {'✅ 成功' if alt_success else '❌ 失敗'}")
    
    if job_success or alt_success:
        print("\n🎉 おめでとう！FaceFusion CLI での Face Swap が成功しました！")
        print("\n💡 推奨使用方法:")
        print("1. JOBベース: python job_based_cli.py")
        print("2. WebUI経由: python facefusion.py --ui-layouts default")
    else:
        print("\n🔧 さらなる調査が必要です")
        print("💬 推奨: GitHub Issues や Discord で開発者に相談")
        print("🔗 https://github.com/facefusion/facefusion/issues")

if __name__ == "__main__":
    main() 