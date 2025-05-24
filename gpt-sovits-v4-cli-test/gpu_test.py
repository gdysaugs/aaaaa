#!/usr/bin/env python3
"""
GPU Test Script for GPT-SoVITS v4 CLI Environment
RTX3050 CUDA 12.4 compatibility check
"""

import sys
import subprocess

def run_nvidia_smi():
    """nvidia-smiコマンドを実行してGPU情報を表示"""
    print("=== NVIDIA-SMI Information ===")
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"nvidia-smi failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("nvidia-smi command not found!")
        return False
    except Exception as e:
        print(f"Error running nvidia-smi: {e}")
        return False

def test_pytorch_cuda():
    """PyTorchのCUDA接続をテスト"""
    print("\n=== PyTorch CUDA Test ===")
    try:
        import torch
        print(f"PyTorch Version: {torch.__version__}")
        
        # CUDA利用可能性チェック
        cuda_available = torch.cuda.is_available()
        print(f"CUDA Available: {cuda_available}")
        
        if cuda_available:
            # CUDA詳細情報
            print(f"CUDA Version: {torch.version.cuda}")
            print(f"cuDNN Version: {torch.backends.cudnn.version()}")
            
            # GPU情報
            device_count = torch.cuda.device_count()
            print(f"Device Count: {device_count}")
            
            for i in range(device_count):
                device_name = torch.cuda.get_device_name(i)
                memory_total = torch.cuda.get_device_properties(i).total_memory / 1024**3
                print(f"GPU {i}: {device_name} ({memory_total:.1f}GB)")
            
            # メモリ使用状況
            if device_count > 0:
                torch.cuda.set_device(0)
                memory_allocated = torch.cuda.memory_allocated(0) / 1024**3
                memory_cached = torch.cuda.memory_reserved(0) / 1024**3
                print(f"Memory Allocated: {memory_allocated:.2f}GB")
                print(f"Memory Cached: {memory_cached:.2f}GB")
            
            # 簡単なCUDA演算テスト
            print("\n=== CUDA Computation Test ===")
            device = torch.device('cuda:0')
            test_tensor = torch.randn(1000, 1000, device=device)
            result = torch.matmul(test_tensor, test_tensor.t())
            print(f"CUDA computation test passed! Result shape: {result.shape}")
            
            return True
        else:
            print("CUDA is not available in PyTorch!")
            return False
            
    except ImportError:
        print("PyTorch is not installed!")
        return False
    except Exception as e:
        print(f"Error testing PyTorch CUDA: {e}")
        return False

def test_environment_variables():
    """環境変数の確認"""
    print("\n=== Environment Variables ===")
    import os
    
    cuda_vars = [
        'CUDA_VISIBLE_DEVICES',
        'NVIDIA_VISIBLE_DEVICES', 
        'PYTORCH_CUDA_ALLOC_CONF',
        'TOKENIZERS_PARALLELISM'
    ]
    
    for var in cuda_vars:
        value = os.environ.get(var, 'Not set')
        print(f"{var}: {value}")

def main():
    """メイン実行関数"""
    print("GPT-SoVITS v4 GPU Test Script")
    print("=" * 50)
    
    # nvidia-smi テスト
    smi_ok = run_nvidia_smi()
    
    # PyTorch CUDA テスト
    torch_ok = test_pytorch_cuda()
    
    # 環境変数確認
    test_environment_variables()
    
    # 結果判定
    print("\n" + "=" * 50)
    print("=== Test Results ===")
    print(f"NVIDIA-SMI: {'✓ PASS' if smi_ok else '✗ FAIL'}")
    print(f"PyTorch CUDA: {'✓ PASS' if torch_ok else '✗ FAIL'}")
    
    if smi_ok and torch_ok:
        print("\n🎉 All tests passed! GPU environment is ready for GPT-SoVITS v4!")
        return 0
    else:
        print("\n❌ Some tests failed. Please check your GPU setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 