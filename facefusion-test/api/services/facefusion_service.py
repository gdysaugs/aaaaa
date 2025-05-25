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
from pathlib import Path
from typing import Optional, Dict, Any
import logging

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
            # 現在のディレクトリから相対的にfacefusionを探す
            current_dir = Path(__file__).parent.parent.parent
            facefusion_path = current_dir / "facefusion"
        
        self.facefusion_path = Path(facefusion_path)
        self.setup_environment()
        
    def setup_environment(self):
        """環境変数設定"""
        os.environ['OMP_NUM_THREADS'] = '1'
        os.environ['PYTHONPATH'] = str(self.facefusion_path)
        
    def face_swap_image(
        self,
        source_path: str,
        target_path: str,
        output_path: str,
        model: str = "inswapper_128",
        quality: int = 90
    ) -> Dict[str, Any]:
        """
        画像のface swap処理
        
        Args:
            source_path: ソース画像パス
            target_path: ターゲット画像パス  
            output_path: 出力画像パス
            model: 使用するモデル
            quality: 出力品質
            
        Returns:
            処理結果辞書
        """
        logger.info(f"画像Face Swap開始: {Path(source_path).name} -> {Path(target_path).name}")
        
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
            '--execution-providers', 'cuda',
            '--log-level', 'info',
            '--output-image-quality', str(quality)
        ]
        
        return self._execute_command(cmd, output_path, "image")
        
    def face_swap_video(
        self,
        source_path: str,
        target_path: str,
        output_path: str,
        model: str = "inswapper_128",
        quality: int = 80,
        trim_start: int = 0,
        trim_end: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        動画のface swap処理
        
        Args:
            source_path: ソース画像パス
            target_path: ターゲット動画パス
            output_path: 出力動画パス
            model: 使用するモデル
            quality: 出力品質
            trim_start: 開始フレーム
            trim_end: 終了フレーム
            
        Returns:
            処理結果辞書
        """
        logger.info(f"動画Face Swap開始: {Path(source_path).name} -> {Path(target_path).name}")
        
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
            '--execution-providers', 'cuda',
            '--log-level', 'info',
            '--output-video-quality', str(quality),
            '--trim-frame-start', str(trim_start)
        ]
        
        # デフォルトで30フレームに制限（テスト用）
        if trim_end is None:
            trim_end = 30
        cmd.extend(['--trim-frame-end', str(trim_end)])
            
        return self._execute_command(cmd, output_path, "video")
        
    def _execute_command(self, cmd: list, output_path: str, media_type: str) -> Dict[str, Any]:
        """
        コマンド実行
        
        Args:
            cmd: 実行コマンド
            output_path: 出力パス
            media_type: メディアタイプ
            
        Returns:
            実行結果辞書
        """
        try:
            logger.info(f"実行コマンド: {' '.join(cmd)}")
            
            # タイムアウト設定（動画は長め）
            timeout = 600 if media_type == "video" else 300
            
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
            
            # 結果確認
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"✅ {media_type} Face Swap成功: {file_size:,} bytes")
                
                return {
                    "success": True,
                    "output_path": output_path,
                    "file_size": file_size,
                    "media_type": media_type,
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
                    "stderr": result.stderr
                }
                
        except subprocess.TimeoutExpired:
            logger.error(f"⏰ 処理がタイムアウトしました ({timeout}秒)")
            return {
                "success": False,
                "error": f"Process timeout after {timeout} seconds"
            }
        except Exception as e:
            logger.error(f"💥 実行エラー: {e}")
            return {
                "success": False,
                "error": str(e)
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
        
        # ソースファイル確認
        if not os.path.exists(source_path):
            errors.append(f"Source file not found: {source_path}")
        elif not source_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            errors.append(f"Source file must be an image: {source_path}")
            
        # ターゲットファイル確認
        if not os.path.exists(target_path):
            errors.append(f"Target file not found: {target_path}")
        elif not target_path.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.avi', '.mov')):
            errors.append(f"Target file must be an image or video: {target_path}")
            
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
