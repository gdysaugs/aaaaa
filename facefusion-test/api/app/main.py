#!/usr/bin/env python3
"""
FaceFusion FastAPI Application
べ、別にあんたのためじゃないけど、ちゃんとしたAPIを作ってあげるわよ！
"""
import os
import time
import uuid
import shutil
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import sys
sys.path.append(str(Path(__file__).parent.parent))

from services.facefusion_service import FaceFusionService
from models.schemas import (
    FaceSwapRequest, VideoFaceSwapRequest, FaceSwapResponse, 
    ErrorResponse, HealthResponse, FileUploadResponse, MediaType
)

# アプリケーション初期化
app = FastAPI(
    title="FaceFusion API",
    description="べ、別にあんたのためじゃないけど、Face SwapができるAPIよ！",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイル設定
static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# FaceFusionサービス初期化
facefusion_service = FaceFusionService()

# アップロード・出力ディレクトリ
UPLOAD_DIR = static_dir / "uploads"
OUTPUT_DIR = static_dir / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

@app.get("/", response_model=dict)
async def root():
    """ルートエンドポイント"""
    return {
        "message": "べ、別にあんたを歓迎してるわけじゃないからね！",
        "service": "FaceFusion API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "upload": "/upload",
            "face_swap_image": "/face-swap/image",
            "face_swap_video": "/face-swap/video",
            "download": "/download/{filename}"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """ヘルスチェック"""
    try:
        # GPU確認
        import torch
        gpu_available = torch.cuda.is_available()
        
        # FaceFusion確認
        facefusion_available = facefusion_service.facefusion_path.exists()
        
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            facefusion_available=facefusion_available,
            gpu_available=gpu_available
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            version="1.0.0",
            facefusion_available=False,
            gpu_available=False
        )

@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """ファイルアップロード"""
    try:
        # ファイル拡張子確認
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.jpg', '.jpeg', '.png', '.mp4', '.avi', '.mov']:
            raise HTTPException(
                status_code=400, 
                detail="サポートされていないファイル形式です"
            )
        
        # ユニークファイル名生成
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        # ファイル保存
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # メディアタイプ判定
        media_type = MediaType.VIDEO if file_ext in ['.mp4', '.avi', '.mov'] else MediaType.IMAGE
        
        return FileUploadResponse(
            success=True,
            filename=unique_filename,
            file_path=str(file_path),
            file_size=file_path.stat().st_size,
            media_type=media_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ファイルアップロードエラー: {str(e)}")

@app.post("/face-swap/image", response_model=FaceSwapResponse)
async def face_swap_image(
    background_tasks: BackgroundTasks,
    source_file: UploadFile = File(..., description="ソース画像ファイル"),
    target_file: UploadFile = File(..., description="ターゲット画像ファイル"),
    model: str = Form(default="inswapper_128", description="使用するモデル"),
    quality: int = Form(default=90, description="出力品質")
):
    """画像Face Swap処理"""
    start_time = time.time()
    
    try:
        # ファイル保存
        source_filename = f"source_{uuid.uuid4()}{Path(source_file.filename).suffix}"
        target_filename = f"target_{uuid.uuid4()}{Path(target_file.filename).suffix}"
        output_filename = f"output_{uuid.uuid4()}.jpg"
        
        source_path = UPLOAD_DIR / source_filename
        target_path = UPLOAD_DIR / target_filename
        output_path = OUTPUT_DIR / output_filename
        
        # ファイル保存
        with open(source_path, "wb") as f:
            shutil.copyfileobj(source_file.file, f)
        with open(target_path, "wb") as f:
            shutil.copyfileobj(target_file.file, f)
        
        # ファイル検証
        validation = facefusion_service.validate_files(str(source_path), str(target_path))
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=validation["errors"])
        
        # Face Swap実行
        result = facefusion_service.face_swap_image(
            source_path=str(source_path),
            target_path=str(target_path),
            output_path=str(output_path),
            model=model,
            quality=quality
        )
        
        # 一時ファイル削除をバックグラウンドタスクに追加
        background_tasks.add_task(cleanup_temp_files, [source_path, target_path])
        
        if result["success"]:
            processing_time = time.time() - start_time
            return FaceSwapResponse(
                success=True,
                message="画像Face Swap完了！",
                output_filename=output_filename,
                file_size=result["file_size"],
                media_type=MediaType.IMAGE,
                processing_time=processing_time
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "処理に失敗しました"))
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"画像処理エラー: {str(e)}")

@app.post("/face-swap/video", response_model=FaceSwapResponse)
async def face_swap_video(
    background_tasks: BackgroundTasks,
    source_file: UploadFile = File(..., description="ソース画像ファイル"),
    target_file: UploadFile = File(..., description="ターゲット動画ファイル"),
    model: str = Form(default="inswapper_128", description="使用するモデル"),
    quality: int = Form(default=80, description="動画品質"),
    trim_start: int = Form(default=0, description="開始フレーム"),
    trim_end: Optional[int] = Form(default=None, description="終了フレーム")
):
    """動画Face Swap処理"""
    start_time = time.time()
    
    try:
        # ファイル保存
        source_filename = f"source_{uuid.uuid4()}{Path(source_file.filename).suffix}"
        target_filename = f"target_{uuid.uuid4()}{Path(target_file.filename).suffix}"
        output_filename = f"output_{uuid.uuid4()}.mp4"
        
        source_path = UPLOAD_DIR / source_filename
        target_path = UPLOAD_DIR / target_filename
        output_path = OUTPUT_DIR / output_filename
        
        # ファイル保存
        with open(source_path, "wb") as f:
            shutil.copyfileobj(source_file.file, f)
        with open(target_path, "wb") as f:
            shutil.copyfileobj(target_file.file, f)
        
        # ファイル検証
        validation = facefusion_service.validate_files(str(source_path), str(target_path))
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=validation["errors"])
        
        # Face Swap実行
        result = facefusion_service.face_swap_video(
            source_path=str(source_path),
            target_path=str(target_path),
            output_path=str(output_path),
            model=model,
            quality=quality,
            trim_start=trim_start,
            trim_end=trim_end
        )
        
        # 一時ファイル削除をバックグラウンドタスクに追加
        background_tasks.add_task(cleanup_temp_files, [source_path, target_path])
        
        if result["success"]:
            processing_time = time.time() - start_time
            return FaceSwapResponse(
                success=True,
                message="動画Face Swap完了！",
                output_filename=output_filename,
                file_size=result["file_size"],
                media_type=MediaType.VIDEO,
                processing_time=processing_time
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "処理に失敗しました"))
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"動画処理エラー: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """ファイルダウンロード"""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="ファイルが見つかりません")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type='application/octet-stream'
    )

async def cleanup_temp_files(file_paths: list):
    """一時ファイル削除"""
    for file_path in file_paths:
        try:
            if Path(file_path).exists():
                os.remove(file_path)
        except Exception:
            pass  # エラーは無視

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 