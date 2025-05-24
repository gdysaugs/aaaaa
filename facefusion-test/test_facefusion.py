#!/usr/bin/env python3
"""
FaceFusion 動作テストスクリプト
べ、別に面倒見てあげてるわけじゃないんだからね！
"""
import os
import sys

# FaceFusionのパスを追加
sys.path.insert(0, '/home/adama/LLM/aaaaa/facefusion-test/facefusion')

def test_basic_import():
    """基本的なモジュールインポートテスト"""
    print("[TEST] 基本インポートテスト...")
    try:
        import facefusion
        print("✓ facefusion インポート成功")
        
        from facefusion import core
        print("✓ core モジュールインポート成功")
        
        from facefusion import metadata
        print("✓ metadata モジュールインポート成功")
        print(f"  バージョン: {metadata.get('version')}")
        
        return True
    except Exception as e:
        print(f"✗ インポートエラー: {e}")
        return False

def test_model_availability():
    """モデルファイルの可用性テスト"""
    print("\n[TEST] モデルファイルテスト...")
    
    model_path = os.path.expanduser("~/.facefusion/models/inswapper_128.onnx")
    if os.path.exists(model_path):
        size = os.path.getsize(model_path)
        print(f"✓ inswapper_128.onnx 存在 ({size} bytes)")
        return True
    else:
        print("✗ inswapper_128.onnx が見つかりません")
        return False

def test_source_files():
    """ソースファイル存在確認"""
    print("\n[TEST] ソースファイルテスト...")
    
    source_files = [
        "/home/adama/LLM/aaaaa/facefusion-test/data/source/source1.jpg",
        "/home/adama/LLM/aaaaa/facefusion-test/data/source/source2.jpg"
    ]
    
    for file_path in source_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {os.path.basename(file_path)} 存在 ({size} bytes)")
        else:
            print(f"✗ {os.path.basename(file_path)} が見つかりません")
            return False
    
    return True

def test_manual_face_swap():
    """手動でface swapを実行"""
    print("\n[TEST] 実際のface swap実行...")
    
    try:
        # 環境変数設定
        os.environ['OMP_NUM_THREADS'] = '1'
        
        # FaceFusionを再起動して設定をクリア
        import sys
        modules_to_remove = [module for module in sys.modules if module.startswith('facefusion')]
        for module in modules_to_remove:
            if module in sys.modules:
                del sys.modules[module]
        
        import facefusion
        from facefusion import core, state_manager, config
        
        # 設定読み込み
        config.read_config('/home/adama/LLM/aaaaa/facefusion-test/facefusion/facefusion.ini')
        
        # 設定
        source_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/source1.jpg"
        target_path = "/home/adama/LLM/aaaaa/facefusion-test/data/source/source2.jpg"
        output_path = "/home/adama/LLM/aaaaa/facefusion-test/data/output/swapped_test.jpg"
        
        # 状態管理設定
        state_manager.set_item('source_paths', [source_path])
        state_manager.set_item('target_path', target_path)
        state_manager.set_item('output_path', output_path)
        state_manager.set_item('processors', ['face_swapper'])
        state_manager.set_item('log_level', 'debug')
        state_manager.set_item('execution_providers', ['cuda'])
        
        print(f"ソース: {source_path}")
        print(f"ターゲット: {target_path}")
        print(f"出力: {output_path}")
        
        # 出力ディレクトリ作成
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 実際の実行
        print("🚀 Face swap処理開始...")
        try:
            # conditional_process関数を直接呼び出し
            from facefusion import core
            if hasattr(core, 'conditional_process'):
                result = core.conditional_process()
                print(f"処理結果: {result}")
            else:
                print("⚠️ conditional_process関数が見つかりません")
        except Exception as exec_error:
            print(f"実行エラー: {exec_error}")
        
        # 結果確認
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✓ Face swap成功！出力ファイル: {output_path} ({size} bytes)")
            return True
        else:
            print("✗ 出力ファイルが生成されませんでした")
            return False
        
    except Exception as e:
        print(f"✗ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("FaceFusion Face Swap 完全テスト")
    print("作成者: ツンデレAI (べ、別にあなたのためじゃないんだからね！)")
    print("=" * 60)
    
    success = 0
    total = 4
    
    if test_basic_import():
        success += 1
    
    if test_model_availability():
        success += 1
        
    if test_source_files():
        success += 1
        
    if test_manual_face_swap():
        success += 1
    
    print("\n" + "=" * 60)
    print(f"テスト結果: {success}/{total} 成功")
    
    if success == total:
        print("🎉 完全成功！FaceFusionのface swapが正常動作確認！")
        print("これでCLIでの顔交換処理が可能になったわよ！")
    else:
        print("❌ 一部テストが失敗。さらなる調整が必要")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 