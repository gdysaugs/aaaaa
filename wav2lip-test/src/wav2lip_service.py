"""
Wav2Lip Service Class
Dockerコンテナを使用した口パク動画生成サービス
"""

import os
import time
import asyncio
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class Wav2LipService:
    """Wav2Lip処理サービス"""
    
    def __init__(self):
        self.base_dir = Path("/home/LLmmmmmm/projects/aaaaa/wav2lip-test")
        self.data_dir = self.base_dir / "data"
        self.models_dir = self.base_dir / "models"
        self.scripts_dir = self.base_dir / "scripts"
        self.temp_dir = self.base_dir / "temp"
        
        # 一時ディレクトリを作成
        self.temp_dir.mkdir(exist_ok=True)
        
        # モデルファイルの存在確認
        self.wav2lip_model = self.models_dir / "wav2lip.pth"
        self.s3fd_model = self.models_dir / "face_detection" / "detection" / "sfd" / "s3fd.pth"
    
    def is_model_loaded(self) -> bool:
        """モデルファイルが存在するかチェック"""
        return self.wav2lip_model.exists() and self.s3fd_model.exists()
    
    def is_gpu_available(self) -> bool:
        """GPU利用可能性をチェック"""
        try:
            result = subprocess.run(
                ["nvidia-smi"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    async def process_video(self, request, processing_status: Dict) -> Dict[str, Any]:
        """動画処理のメイン関数"""
        job_id = request.job_id
        start_time = time.time()
        
        try:
            # 作業ディレクトリを作成
            job_dir = self.temp_dir / job_id
            job_dir.mkdir(exist_ok=True)
            
            input_dir = job_dir / "input"
            output_dir = job_dir / "output"
            input_dir.mkdir(exist_ok=True)
            output_dir.mkdir(exist_ok=True)
            
            # ファイル内容を直接保存（既にバイト配列として受け取っている）
            logger.info(f"Saving video file: {len(request.video_content)} bytes")
            logger.info(f"Saving audio file: {len(request.audio_content)} bytes")
            
            # ファイルを保存
            video_path = await self._save_file_content(request.video_content, input_dir / "video.mp4")
            audio_path = await self._save_file_content(request.audio_content, input_dir / "audio.wav")
            
            # 処理状況を更新
            processing_status[job_id].update({
                "status": "processing",
                "progress": 30,
                "message": "Dockerコンテナで処理中..."
            })
            
            # Dockerコマンドを構築
            output_file = output_dir / "result.mp4"
            docker_cmd = self._build_docker_command(
                video_path, audio_path, output_file, request
            )
            
            # Docker処理を実行
            await self._run_docker_process(docker_cmd, job_id, processing_status)
            
            # 処理時間を計算
            processing_time = time.time() - start_time
            
            return {
                "output_path": str(output_file),
                "processing_time": processing_time
            }
            
        except Exception as e:
            logger.error(f"Error processing video for job {job_id}: {str(e)}")
            raise e
    
    async def _save_file_content(self, content: bytes, destination: Path) -> Path:
        """ファイル内容を保存"""
        try:
            # ファイルに書き込み
            with open(destination, "wb") as buffer:
                buffer.write(content)
            
            logger.info(f"Saved file to {destination}, size: {len(content)} bytes")
            return destination
            
        except Exception as e:
            logger.error(f"Error saving file to {destination}: {str(e)}")
            raise e
    
    def _build_docker_command(self, video_path: Path, audio_path: Path, 
                            output_path: Path, request) -> list:
        """Dockerコマンドを構築"""
        
        # パディング設定を解析
        pads = request.pads.split(',')
        if len(pads) != 4:
            pads = ["0", "10", "0", "0"]
        
        # Dockerコマンドを構築
        cmd = [
            "sudo", "docker", "run", "--gpus", "all", "--rm",
            "-v", f"{video_path.parent}:/workspace/input",
            "-v", f"{output_path.parent}:/workspace/output",
            "-v", f"{self.models_dir}:/workspace/models",
            "wav2lip-gpu",
            "python3", "/workspace/Wav2Lip/inference.py",
            "--checkpoint_path", "/workspace/models/wav2lip.pth",
            "--face", "/workspace/input/video.mp4",
            "--audio", "/workspace/input/audio.wav",
            "--outfile", "/workspace/output/result.mp4",
            "--pads", " ".join(pads),
            "--face_det_batch_size", str(request.face_det_batch_size),
            "--wav2lip_batch_size", str(request.wav2lip_batch_size)
        ]
        
        # リサイズ係数を追加
        if request.resize_factor > 1:
            cmd.extend(["--resize_factor", str(request.resize_factor)])
        
        return cmd
    
    async def _run_docker_process(self, cmd: list, job_id: str, 
                                processing_status: Dict):
        """Docker処理を実行"""
        try:
            # 処理状況を更新
            processing_status[job_id].update({
                "progress": 50,
                "message": "Wav2Lip推論実行中..."
            })
            
            # Docker処理を実行
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"Docker process failed: {error_msg}")
                raise Exception(f"Docker process failed: {error_msg}")
            
            # 処理状況を更新
            processing_status[job_id].update({
                "progress": 90,
                "message": "処理完了中..."
            })
            
        except Exception as e:
            logger.error(f"Docker process error for job {job_id}: {str(e)}")
            raise e
    
    async def cleanup_job(self, job_id: str):
        """ジョブの一時ファイルをクリーンアップ"""
        job_dir = self.temp_dir / job_id
        if job_dir.exists():
            shutil.rmtree(job_dir)
            logger.info(f"Cleaned up job directory: {job_dir}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """モデル情報を取得"""
        return {
            "wav2lip_model_exists": self.wav2lip_model.exists(),
            "s3fd_model_exists": self.s3fd_model.exists(),
            "wav2lip_model_size": self.wav2lip_model.stat().st_size if self.wav2lip_model.exists() else 0,
            "s3fd_model_size": self.s3fd_model.stat().st_size if self.s3fd_model.exists() else 0
        } 