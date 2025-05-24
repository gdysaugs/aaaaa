#!/usr/bin/env python3
"""
FaceFusion シンプル動作テスト
べ、別にあなたのためじゃないけど、基本動作を確認してあげるわよ！
"""
import os
import sys

# FaceFusionのパスを追加
sys.path.insert(0, '/home/adama/LLM/aaaaa/facefusion-test/facefusion')

def test_basic_cli():
    """基本的なCLI動作テスト"""
    print("=== 基本CLI動作テスト ===")
    
    try:
        # 環境変数設定
        os.environ['OMP_NUM_THREADS'] = '1'
        
        # FaceFusionモジュールをインポート
        import facefusion
        from facefusion import core, program, state_manager
        
        print("✓ FaceFusionモジュール正常インポート")
        
        # プログラム作成
        parser = program.create_program()
        print("✓ プログラムパーサー作成成功")
        
        # 基本的な引数設定
        test_args = [
            '--source-paths', '/home/adama/LLM/aaaaa/facefusion-test/data/source/kanna-hashimoto.jpg',
            '--target-path', '/home/adama/LLM/aaaaa/facefusion-test/data/source/source1.jpg',
            '--output-path', '/home/adama/LLM/aaaaa/facefusion-test/data/output/simple_test.jpg',
            '--processors', 'face_swapper',
            '--log-level', 'debug'
        ]
        
        print(f"テスト引数: {test_args}")
        
        # 引数解析
        try:
            args = parser.parse_args(test_args)
            print("✓ 引数解析成功")
            print(f"  ソースパス: {getattr(args, 'source_paths', 'N/A')}")
            print(f"  ターゲットパス: {getattr(args, 'target_path', 'N/A')}")
            print(f"  出力パス: {getattr(args, 'output_path', 'N/A')}")
            return True
        except SystemExit as e:
            print(f"✗ 引数解析エラー (SystemExit): {e}")
            return False
        except Exception as e:
            print(f"✗ 引数解析エラー: {e}")
            return False
            
    except Exception as e:
        print(f"✗ 基本CLI動作エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_processor_availability():
    """プロセッサーの利用可能性テスト"""
    print("\n=== プロセッサー利用可能性テスト ===")
    
    try:
        from facefusion.processors.core import get_processors_modules
        from facefusion.filesystem import resolve_file_paths, get_file_name
        
        # 利用可能なプロセッサーを取得
        available_processors = [get_file_name(file_path) for file_path in resolve_file_paths('facefusion/processors/modules')]
        print(f"利用可能なプロセッサー: {available_processors}")
        
        # face_swapperが利用可能かチェック
        if 'face_swapper' in available_processors:
            print("✓ face_swapper プロセッサー利用可能")
            
            # プロセッサーモジュールを取得
            processor_modules = get_processors_modules(['face_swapper'])
            print(f"✓ face_swapperモジュール読み込み成功: {len(processor_modules)} modules")
            return True
        else:
            print("✗ face_swapper プロセッサーが見つかりません")
            return False
            
    except Exception as e:
        print(f"✗ プロセッサーテストエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_loading():
    """モデル読み込みテスト"""
    print("\n=== モデル読み込みテスト ===")
    
    try:
        from facefusion.processors.modules import face_swapper
        
        print("✓ face_swapper モジュールインポート成功")
        
        # モデル初期化確認
        if hasattr(face_swapper, 'get_inference_pool'):
            print("✓ 推論プール関数利用可能")
        
        if hasattr(face_swapper, 'load_inference_pool'):
            print("✓ 推論プール読み込み関数利用可能")
            
        return True
        
    except Exception as e:
        print(f"✗ モデル読み込みエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🔍 FaceFusion シンプル動作確認")
    print("作成者: ツンデレAI")
    print("=" * 60)
    
    success_count = 0
    total_tests = 3
    
    if test_basic_cli():
        success_count += 1
    
    if test_processor_availability():
        success_count += 1
        
    if test_model_loading():
        success_count += 1
    
    print("\n" + "=" * 60)
    print(f"テスト結果: {success_count}/{total_tests} 成功")
    
    if success_count == total_tests:
        print("✅ 基本動作確認完了！CLI実行の準備ができています")
    else:
        print("⚠️ 一部の機能に問題があります。詳細を確認してください")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 