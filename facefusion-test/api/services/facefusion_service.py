#!/usr/bin/env python3
"""
FaceFusion Service Module
べ、別にあんたのためじゃないけど、ちゃんとしたサービスクラスを作ってあげるわよ！
"""
import os
import sys
import subprocess
import tempfile
import shutil
import time
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import torch

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FaceFusionService:
    """FaceFusion処理サービスクラス"""
    
    def __init__(self, facefusion_path: str = None):
        """
        初期化
        Args:
            facefusion_path: FaceFusionのインストールパス
        """
        if facefusion_path is None:
            # Dockerコンテナ内での標準パス
            facefusion_path = "/app/facefusion"
            
        self.facefusion_path = Path(facefusion_path)
        self.setup_environment()
        self.validate_environment()
        
    def setup_environment(self):
        """環境変数設定"""
        os.environ['OMP_NUM_THREADS'] = '1'
        os.environ['PYTHONPATH'] = str(self.facefusion_path)
        
        # CUDA設定
        if torch.cuda.is_available():
            os.environ['CUDA_VISIBLE_DEVICES'] = os.environ.get('CUDA_VISIBLE_DEVICES', '0')
            
    def validate_environment(self) -> Dict[str, Any]:
        """環境検証"""
        validation = {
            "facefusion_available": self.facefusion_path.exists(),
            "facefusion_script": (self.facefusion_path / "facefusion.py").exists(),
            "gpu_available": torch.cuda.is_available(),
            "cuda_version": None,
            "gpu_count": 0,
            "gpu_names": []
        }
        
        if torch.cuda.is_available():
            validation["cuda_version"] = torch.version.cuda
            validation["gpu_count"] = torch.cuda.device_count()
            validation["gpu_names"] = [
                torch.cuda.get_device_name(i) 
                for i in range(torch.cuda.device_count())
            ]
            
        logger.info(f"🔍 環境検証結果: {validation}")
        return validation
        
    def get_available_models(self) -> List[str]:
        """利用可能なモデル一覧を取得"""
        return [
            "inswapper_128",
            "inswapper_128_fp16", 
            "blendswap_256",
            "ghost_1_256",
            "ghost_2_256",
            "ghost_3_256",
            "simswap_256",
            "uniface_256"
        ]
        
    def face_swap_image(
        self,
        source_path: str,
        target_path: str,
        output_path: str,
        model: str = "inswapper_128",
        quality: int = 90,
        pixel_boost: str = "128x128"
    ) -> Dict[str, Any]:
        """
        画像のface swap処理
        
        Args:
            source_path: ソース画像パス
            target_path: ターゲット画像パス  
            output_path: 出力画像パス
            model: 使用するモデル
            quality: 出力品質
            pixel_boost: ピクセルブースト
            
        Returns:
            処理結果辞書
        """
        logger.info(f"🎭 画像Face Swap開始: {Path(source_path).name} -> {Path(target_path).name}")
        
        # 出力ディレクトリ作成
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # コマンド構築
        cmd = [
            'python3', 'facefusion.py', 'headless-run',
            '--source-paths', source_path,
            '--target-path', target_path,
            '--output-path', output_path,
            '--processors', 'face_swapper',
            '--face-swapper-model', model,
            '--face-swapper-pixel-boost', pixel_boost,
            '--execution-providers', 'cuda' if torch.cuda.is_available() else 'cpu',
            '--log-level', 'info',
            '--output-image-quality', str(quality)
        ]
        
        return self._execute_command(cmd, output_path, "image", model=model, quality=quality)
        
    def face_swap_video(
        self,
        source_path: str,
        target_path: str,
        output_path: str,
        model: str = "inswapper_128",
        quality: int = 80,
        pixel_boost: str = "128x128",
        trim_start: int = 0,
        trim_end: Optional[int] = None,
        max_frames: int = 100
    ) -> Dict[str, Any]:
        """
        動画のface swap処理
        
        Args:
            source_path: ソース画像パス
            target_path: ターゲット動画パス
            output_path: 出力動画パス
            model: 使用するモデル
            quality: 出力品質
            pixel_boost: ピクセルブースト
            trim_start: 開始フレーム
            trim_end: 終了フレーム
            max_frames: 最大フレーム数
            
        Returns:
            処理結果辞書
        """
        logger.info(f"🎬 動画Face Swap開始: {Path(source_path).name} -> {Path(target_path).name}")
        
        # 出力ディレクトリ作成
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # フレーム制限
        if trim_end is None:
            trim_end = min(trim_start + max_frames, trim_start + 50)  # デフォルトで50フレーム制限
            
        # コマンド構築
        cmd = [
            'python3', 'facefusion.py', 'headless-run',
            '--source-paths', source_path,
            '--target-path', target_path,
            '--output-path', output_path,
            '--processors', 'face_swapper',
            '--face-swapper-model', model,
            '--face-swapper-pixel-boost', pixel_boost,
            '--execution-providers', 'cuda' if torch.cuda.is_available() else 'cpu',
            '--log-level', 'info',
            '--output-video-quality', str(quality),
            '--trim-frame-start', str(trim_start),
            '--trim-frame-end', str(trim_end)
        ]
            
        return self._execute_command(cmd, output_path, "video", model=model, quality=quality)
        
    def _execute_command(
        self, 
        cmd: list, 
        output_path: str, 
        media_type: str,
        model: str = None,
        quality: int = None
    ) -> Dict[str, Any]:
        """
        コマンド実行
        
        Args:
            cmd: 実行コマンド
            output_path: 出力パス
            media_type: メディアタイプ
            model: 使用モデル
            quality: 品質
            
        Returns:
            実行結果辞書
        """
        start_time = time.time()
        
        try:
            logger.info(f"🚀 実行コマンド: {' '.join(cmd)}")
            
            # タイムアウト設定（動画は長め）
            timeout = 1200 if media_type == "video" else 600
            
            # 環境変数設定
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.facefusion_path)
            
            result = subprocess.run(
                cmd,
                cwd=self.facefusion_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
                env=env
            )
            
            processing_time = time.time() - start_time
            
            # 結果確認
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"✅ {media_type} Face Swap成功: {file_size:,} bytes ({processing_time:.2f}秒)")
                
                return {
                    "success": True,
                    "output_path": output_path,
                    "file_size": file_size,
                    "media_type": media_type,
                    "processing_time": processing_time,
                    "model_used": model,
                    "quality": quality,
                    "return_code": result.returncode,
                    "message": f"{media_type} face swap completed successfully"
                }
            else:
                logger.error(f"❌ 出力ファイルが生成されませんでした: {output_path}")
                logger.error(f"📋 リターンコード: {result.returncode}")
                logger.error(f"📤 標準出力: {result.stdout}")
                logger.error(f"📤 エラー出力: {result.stderr}")
                return {
                    "success": False,
                    "error": "Output file not generated",
                    "return_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "processing_time": processing_time
                }
                
        except subprocess.TimeoutExpired:
            processing_time = time.time() - start_time
            logger.error(f"⏰ 処理がタイムアウトしました ({timeout}秒)")
            return {
                "success": False,
                "error": f"Process timeout after {timeout} seconds",
                "processing_time": processing_time
            }
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"💥 実行エラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "processing_time": processing_time
            }
                
    def validate_files(self, source_path: str, target_path: str) -> Dict[str, Any]:
        """
        ファイル検証
        
        Args:
            source_path: ソースファイルパス
            target_path: ターゲットファイルパス
            
        Returns:
            検証結果辞書
        """
        errors = []
        
        # ファイル存在確認
        if not os.path.exists(source_path):
            errors.append(f"ソースファイルが見つかりません: {source_path}")
            
        if not os.path.exists(target_path):
            errors.append(f"ターゲットファイルが見つかりません: {target_path}")
            
        # ファイル拡張子確認
        source_ext = Path(source_path).suffix.lower()
        target_ext = Path(target_path).suffix.lower()
        
        valid_image_exts = ['.jpg', '.jpeg', '.png']
        valid_video_exts = ['.mp4', '.avi', '.mov']
        
        if source_ext not in valid_image_exts:
            errors.append(f"サポートされていないソースファイル形式: {source_ext}")
            
        if target_ext not in valid_image_exts + valid_video_exts:
            errors.append(f"サポートされていないターゲットファイル形式: {target_ext}")
            
        # ファイルサイズ確認（100MB制限）
        max_size = 100 * 1024 * 1024  # 100MB
        
        if os.path.exists(source_path):
            source_size = os.path.getsize(source_path)
            if source_size > max_size:
                errors.append(f"ソースファイルサイズが大きすぎます: {source_size / 1024 / 1024:.1f}MB")
                
        if os.path.exists(target_path):
            target_size = os.path.getsize(target_path)
            if target_size > max_size:
                errors.append(f"ターゲットファイルサイズが大きすぎます: {target_size / 1024 / 1024:.1f}MB")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
        
    def get_system_info(self) -> Dict[str, Any]:
        """システム情報取得"""
        import platform
        import psutil
        
        info = {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "torch_version": torch.__version__ if torch else "N/A",
            "cuda_available": torch.cuda.is_available() if torch else False,
            "gpu_count": 0,
            "gpu_names": [],
            "memory_total": psutil.virtual_memory().total if psutil else None,
            "memory_available": psutil.virtual_memory().available if psutil else None
        }
        
        if torch and torch.cuda.is_available():
            info["cuda_version"] = torch.version.cuda
            info["gpu_count"] = torch.cuda.device_count()
            info["gpu_names"] = [
                torch.cuda.get_device_name(i) 
                for i in range(torch.cuda.device_count())
            ]
            
        return info
