"""
Wav2Lip CLI Wrapper
CLIで成功したコマンドをそのまま関数化するモジュール
"""

import os
import subprocess
import asyncio
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Wav2LipCLIWrapper:
    """CLIで成功したWav2Lipコマンドをそのまま実行するラッパー"""
    
    def __init__(self):
        self.base_dir = Path("/home/LLmmmmmm/projects/aaaaa/wav2lip-test")
        self.models_dir = self.base_dir / "models"
        self.temp_dir = self.base_dir / "temp"
        
        # 必要なディレクトリを作成
        self.temp_dir.mkdir(exist_ok=True)
        
        # モデルファイルのパス
        self.wav2lip_model = self.models_dir / "wav2lip.pth"
        self.s3fd_model = self.models_dir / "face_detection" / "detection" / "sfd" / "s3fd.pth"
    
    def is_model_loaded(self) -> bool:
        """モデルファイルが存在するかチェック"""
        return self.wav2lip_model.exists() and self.s3fd_model.exists()
    
    async def process_video_cli(
        self,
        job_id: str,
        video_content: bytes,
        audio_content: bytes,
        video_filename: str,
        audio_filename: str,
        pads: str = "0 10 0 0",
        face_det_batch_size: int = 1,
        wav2lip_batch_size: int = 4,
        resize_factor: int = 1,
        processing_status: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        CLIで成功したコマンドをそのまま実行する関数
        
        Args:
            job_id: ジョブID
            video_content: 動画ファイルのバイト配列
            audio_content: 音声ファイルのバイト配列
            video_filename: 動画ファイル名
            audio_filename: 音声ファイル名
            pads: パディング設定（スペース区切り）
            face_det_batch_size: 顔検出バッチサイズ
            wav2lip_batch_size: Wav2Lipバッチサイズ
            resize_factor: リサイズ係数
            processing_status: 処理状況を管理する辞書
        
        Returns:
            処理結果の辞書
        """
        
        # 作業ディレクトリを作成
        job_dir = self.temp_dir / job_id
        job_dir.mkdir(exist_ok=True)
        
        input_dir = job_dir / "input"
        output_dir = job_dir / "output"
        input_dir.mkdir(exist_ok=True)
        output_dir.mkdir(exist_ok=True)
        
        try:
            # ファイルを保存
            video_path = input_dir / f"video{Path(video_filename).suffix}"
            audio_path = input_dir / f"audio{Path(audio_filename).suffix}"
            output_path = output_dir / "result.mp4"
            
            # ファイル内容を保存
            with open(video_path, "wb") as f:
                f.write(video_content)
            
            with open(audio_path, "wb") as f:
                f.write(audio_content)
            
            logger.info(f"Saved files: video={video_path}, audio={audio_path}")
            
            # 処理状況を更新
            if processing_status and job_id in processing_status:
                processing_status[job_id].update({
                    "status": "processing",
                    "progress": 30,
                    "message": "Dockerコンテナで処理中..."
                })
            
            # CLIで成功したコマンドをそのまま実行
            await self._run_wav2lip_docker(
                video_path=video_path,
                audio_path=audio_path,
                output_path=output_path,
                pads=pads,
                face_det_batch_size=face_det_batch_size,
                wav2lip_batch_size=wav2lip_batch_size,
                resize_factor=resize_factor,
                job_id=job_id,
                processing_status=processing_status
            )
            
            # 出力ファイルの存在確認
            if not output_path.exists():
                raise Exception("出力ファイルが生成されませんでした")
            
            return {
                "output_path": str(output_path),
                "job_id": job_id,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error processing video for job {job_id}: {str(e)}")
            raise e
    
    async def _run_wav2lip_docker(
        self,
        video_path: Path,
        audio_path: Path,
        output_path: Path,
        pads: str,
        face_det_batch_size: int,
        wav2lip_batch_size: int,
        resize_factor: int,
        job_id: str,
        processing_status: Optional[Dict] = None
    ):
        """
        CLIで成功したDockerコマンドをそのまま実行
        """
        
        # パディングをスペース区切りで処理（CLIで成功した形式）
        pads_list = pads.strip().split()
        if len(pads_list) != 4:
            pads_list = ["0", "10", "0", "0"]
        
        # CLIで成功したDockerコマンドを構築
        docker_cmd = [
            "sudo", "docker", "run", "--gpus", "all", "--rm",
            "-v", f"{video_path.parent}:/workspace/data/input",
            "-v", f"{output_path.parent}:/workspace/data/output", 
            "-v", f"{self.models_dir}:/workspace/models",
            "wav2lip-gpu",
            "bash", "-c",
            f"""
            # s3fd.pthの場所を指定
            mkdir -p /workspace/Wav2Lip/face_detection/detection/sfd
            cp /workspace/models/face_detection/detection/sfd/s3fd.pth /workspace/Wav2Lip/face_detection/detection/sfd/
            
            # 一時ディレクトリの作成
            mkdir -p /workspace/Wav2Lip/temp
            
            # Wav2Lipディレクトリに移動して実行
            cd /workspace/Wav2Lip
            
            # CLIで成功したコマンドをそのまま実行
            python3 inference.py \\
              --checkpoint_path /workspace/models/wav2lip.pth \\
              --face /workspace/data/input/{video_path.name} \\
              --audio /workspace/data/input/{audio_path.name} \\
              --outfile /workspace/data/output/result.mp4 \\
              --pads {' '.join(pads_list)} \\
              --face_det_batch_size {face_det_batch_size} \\
              --wav2lip_batch_size {wav2lip_batch_size}
            """
        ]
        
        # リサイズ係数を追加（必要な場合）
        if resize_factor > 1:
            # コマンドの最後の部分にresize_factorを追加
            docker_cmd[-1] = docker_cmd[-1].rstrip() + f" \\\n              --resize_factor {resize_factor}"
        
        logger.info(f"Executing Docker command for job {job_id}")
        
        # 処理状況を更新
        if processing_status and job_id in processing_status:
            processing_status[job_id].update({
                "progress": 50,
                "message": "Wav2Lip推論実行中..."
            })
        
        try:
            # Docker処理を実行
            process = await asyncio.create_subprocess_exec(
                *docker_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"Docker process failed: {error_msg}")
                raise Exception(f"Docker process failed: {error_msg}")
            
            logger.info(f"Docker process completed successfully for job {job_id}")
            
            # 処理状況を更新
            if processing_status and job_id in processing_status:
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