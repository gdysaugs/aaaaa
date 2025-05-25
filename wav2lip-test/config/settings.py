"""
Wav2Lip API Configuration Settings
"""

import os
from pathlib import Path
from typing import List

class Settings:
    """アプリケーション設定"""
    
    # API設定
    API_TITLE: str = "Wav2Lip API"
    API_DESCRIPTION: str = "口パク動画生成API - 動画と音声から自然な口パク動画を生成"
    API_VERSION: str = "1.0.0"
    
    # サーバー設定
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # ファイル設定
    MAX_FILE_SIZE: int = 500 * 1024 * 1024  # 500MB
    ALLOWED_VIDEO_EXTENSIONS: List[str] = [".mp4", ".avi"]
    ALLOWED_AUDIO_EXTENSIONS: List[str] = [".wav", ".mp3"]
    
    # Docker設定
    DOCKER_IMAGE: str = "wav2lip-gpu"
    USE_GPU: bool = True
    
    # モデル設定
    MODEL_DIR: Path = Path("/home/LLmmmmmm/projects/aaaaa/wav2lip-test/models")
    WAV2LIP_MODEL: str = "wav2lip.pth"
    S3FD_MODEL: str = "face_detection/detection/sfd/s3fd.pth"
    
    # 処理設定
    DEFAULT_PADS: str = "0,10,0,0"
    DEFAULT_FACE_DET_BATCH_SIZE: int = 1
    DEFAULT_WAV2LIP_BATCH_SIZE: int = 4
    DEFAULT_RESIZE_FACTOR: int = 1
    DEFAULT_QUALITY: str = "high"
    
    # ログ設定
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # セキュリティ設定
    CORS_ORIGINS: List[str] = ["*"]
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # クリーンアップ設定
    AUTO_CLEANUP_HOURS: int = 24  # 24時間後に自動クリーンアップ
    MAX_CONCURRENT_JOBS: int = 5  # 同時処理可能ジョブ数

settings = Settings() 