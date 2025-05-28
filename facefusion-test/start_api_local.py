#!/usr/bin/env python3
"""
FaceFusion API Local Startup Script
べ、別にあんたのためじゃないけど、ローカルでAPIを起動してあげるわよ！
"""
import os
import sys
import uvicorn
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_environment():
    """環境変数設定"""
    # 基本設定
    os.environ.setdefault('API_HOST', '0.0.0.0')
    os.environ.setdefault('API_PORT', '8000')
    os.environ.setdefault('LOG_LEVEL', 'INFO')
    
    # CUDA設定
    os.environ.setdefault('CUDA_VISIBLE_DEVICES', '0')
    os.environ.setdefault('OMP_NUM_THREADS', '1')
    
    # FaceFusion設定
    facefusion_path = project_root / "facefusion"
    os.environ.setdefault('FACEFUSION_PATH', str(facefusion_path))
    os.environ['PYTHONPATH'] = f"{facefusion_path}:{os.environ.get('PYTHONPATH', '')}"
    
    print("🔧 環境変数設定完了:")
    print(f"   - API_HOST: {os.environ.get('API_HOST')}")
    print(f"   - API_PORT: {os.environ.get('API_PORT')}")
    print(f"   - FACEFUSION_PATH: {os.environ.get('FACEFUSION_PATH')}")
    print(f"   - CUDA_VISIBLE_DEVICES: {os.environ.get('CUDA_VISIBLE_DEVICES')}")

def check_requirements():
    """必要な依存関係を確認"""
    print("🔍 依存関係チェック中...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'torch',
        'PIL',
        'cv2',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'cv2':
                import cv2
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ 以下のパッケージがインストールされていません:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n以下のコマンドでインストールできます:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 全ての依存関係が確認できました")
    return True

def check_gpu():
    """GPU使用可能性チェック"""
    print("\n🎮 GPU チェック中...")
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            print(f"   ✅ CUDA利用可能")
            print(f"   - GPU数: {gpu_count}")
            print(f"   - GPU名: {gpu_name}")
            print(f"   - CUDAバージョン: {torch.version.cuda}")
            return True
        else:
            print("   ⚠️ CUDAが利用できません（CPU処理になります）")
            return False
    except Exception as e:
        print(f"   ❌ GPU チェックエラー: {e}")
        return False

def check_facefusion():
    """FaceFusionインストールチェック"""
    print("\n🎭 FaceFusion チェック中...")
    
    facefusion_path = Path(os.environ.get('FACEFUSION_PATH', './facefusion'))
    
    if not facefusion_path.exists():
        print(f"   ❌ FaceFusionが見つかりません: {facefusion_path}")
        print("   以下のコマンドでクローンできます:")
        print("   git clone https://github.com/facefusion/facefusion.git")
        return False
    
    facefusion_script = facefusion_path / "facefusion.py"
    if not facefusion_script.exists():
        print(f"   ❌ facefusion.pyが見つかりません: {facefusion_script}")
        return False
    
    print(f"   ✅ FaceFusion確認: {facefusion_path}")
    return True

def create_directories():
    """必要なディレクトリ作成"""
    print("\n📁 ディレクトリ作成中...")
    
    directories = [
        "api/static/uploads",
        "api/static/outputs", 
        "data/source",
        "data/output",
        "logs"
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")

def main():
    """メイン実行関数"""
    print("🚀 FaceFusion API ローカル起動")
    print("=" * 50)
    
    # 環境設定
    setup_environment()
    
    # 前提条件チェック
    if not check_requirements():
        print("\n❌ 依存関係が不足しています。インストール後に再実行してください。")
        sys.exit(1)
    
    check_gpu()
    
    if not check_facefusion():
        print("\n❌ FaceFusionが見つかりません。インストール後に再実行してください。")
        sys.exit(1)
    
    # ディレクトリ作成
    create_directories()
    
    # API起動
    print("\n🌟 API起動中...")
    host = os.environ.get('API_HOST', '0.0.0.0')
    port = int(os.environ.get('API_PORT', '8000'))
    
    print(f"📡 APIサーバー起動:")
    print(f"   - URL: http://{host}:{port}")
    print(f"   - Swagger UI: http://{host}:{port}/")
    print(f"   - ReDoc: http://{host}:{port}/redoc")
    print(f"   - CLI Help: http://{host}:{port}/cli-help")
    
    print("\n💡 終了するには Ctrl+C を押してください")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "api.app.main:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 APIサーバーが停止しました")
    except Exception as e:
        print(f"\n❌ APIサーバー起動エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 