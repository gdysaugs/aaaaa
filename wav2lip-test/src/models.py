"""
Pydantic models for Wav2Lip API
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from fastapi import UploadFile

class ProcessRequest(BaseModel):
    """動画処理リクエスト"""
    job_id: str
    video_content: bytes  # 動画ファイルの内容
    audio_content: bytes  # 音声ファイルの内容
    video_filename: str   # 動画ファイル名
    audio_filename: str   # 音声ファイル名
    pads: str = Field(default="0 10 0 0", description="パディング設定 (上 下 左 右) - スペース区切り")
    face_det_batch_size: int = Field(default=1, description="顔検出バッチサイズ")
    wav2lip_batch_size: int = Field(default=4, description="Wav2Lipバッチサイズ")
    resize_factor: int = Field(default=1, description="リサイズ係数")
    quality: str = Field(default="high", description="品質設定")
    
    class Config:
        arbitrary_types_allowed = True

class ProcessResponse(BaseModel):
    """動画処理レスポンス"""
    job_id: str
    status: str
    message: str

class ProcessStatus(BaseModel):
    """処理状況"""
    status: str = Field(description="処理状況 (uploading, processing, completed, failed)")
    progress: int = Field(description="進捗率 (0-100)")
    message: str = Field(description="状況メッセージ")
    output_path: Optional[str] = Field(default=None, description="出力ファイルパス")
    processing_time: Optional[float] = Field(default=None, description="処理時間（秒）")

class HealthResponse(BaseModel):
    """ヘルスチェックレスポンス"""
    status: str
    models_loaded: bool
    gpu_available: bool 