#!/usr/bin/env python3
"""
FaceFusion FastAPI Application
べ、別にあんたのためじゃないけど、ちゃんとしたAPIを作ってあげるわよ！
"""
import os
import time
import uuid
import shutil
import asyncio
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from api.services.facefusion_service import FaceFusionService
from models.schemas import (
    FaceSwapImageRequest, FaceSwapVideoRequest, FaceSwapResponse, 
    ErrorResponse, HealthResponse, FileUploadResponse, MediaType,
    SystemInfo, ModelsInfo, CLIFaceSwapRequest
)

# アプリケーション初期化
app = FastAPI(
    title="FaceFusion API",
    description="""
    ## 🎭 FaceFusion Face Swap API
    
    べ、別にあんたのためじゃないけど、Face SwapができるAPIよ！
    
    ### 機能:
    - 画像 Face Swap
    - 動画 Face Swap  
    - ファイルアップロード/ダウンロード
    - システム情報取得
    - CLI コマンド実行
    
    ### 使用方法:
    1. ソース画像をアップロード
    2. ターゲット画像/動画をアップロード
    3. Face Swap実行
    4. 結果をダウンロード
    """,
    version="1.0.0",
    docs_url="/",  # Swagger UIをルートに設置
    redoc_url="/redoc"
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

# ディレクトリ設定
UPLOAD_DIR = static_dir / "uploads"
OUTPUT_DIR = static_dir / "outputs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/api", response_model=dict, tags=["情報"])
async def api_info():
    """API情報"""
    return {
        "message": "べ、別にあんたを歓迎してるわけじゃないからね！",
        "service": "FaceFusion API",
        "version": "1.0.0",
        "documentation": "/",
        "redoc": "/redoc",
        "endpoints": {
            "health": "/health",
            "system_info": "/system/info",
            "models": "/models",
            "upload": "/upload",
            "face_swap_image": "/face-swap/image",
            "face_swap_video": "/face-swap/video",
            "cli_face_swap": "/cli/face-swap",
            "download": "/download/{filename}"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["システム"])
async def health_check():
    """ヘルスチェック"""
    try:
        # GPU確認
        import torch
        gpu_available = torch.cuda.is_available()
        cuda_version = torch.version.cuda if gpu_available else None
        
        # FaceFusion確認
        facefusion_available = facefusion_service.facefusion_path.exists()
        
        # メモリ使用量確認
        memory_usage = None
        try:
            import psutil
            memory = psutil.virtual_memory()
            memory_usage = {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent
            }
        except ImportError:
            pass
        
        return HealthResponse(
            status="healthy" if facefusion_available and gpu_available else "degraded",
            version="1.0.0",
            facefusion_available=facefusion_available,
            gpu_available=gpu_available,
            cuda_version=cuda_version,
            memory_usage=memory_usage
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            version="1.0.0",
            facefusion_available=False,
            gpu_available=False
        )

@app.get("/system/info", response_model=SystemInfo, tags=["システム"])
async def get_system_info():
    """システム情報取得"""
    try:
        return SystemInfo(**facefusion_service.get_system_info())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"システム情報取得エラー: {str(e)}")

@app.get("/models", response_model=ModelsInfo, tags=["モデル"])
async def get_models():
    """利用可能なモデル一覧"""
    try:
        models = facefusion_service.get_available_models()
        return ModelsInfo(
            available_models=models,
            default_model="inswapper_128",
            model_details={
                "inswapper_128": "高品質・高速",
                "inswapper_128_fp16": "高品質・高速（FP16）",
                "ghost_2_256": "最高品質（推奨）",
                "blendswap_256": "自然な仕上がり"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"モデル情報取得エラー: {str(e)}")

@app.post("/upload", response_model=FileUploadResponse, tags=["ファイル"])
async def upload_file(file: UploadFile = File(..., description="アップロードするファイル（画像/動画）")):
    """ファイルアップロード"""
    try:
        # ファイル拡張子確認
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ['.jpg', '.jpeg', '.png', '.mp4', '.avi', '.mov']:
            raise HTTPException(
                status_code=400, 
                detail=f"サポートされていないファイル形式です: {file_ext}"
            )
        
        # ファイルサイズ確認（500MB制限）
        max_size = 500 * 1024 * 1024  # 500MB
        file_content = await file.read()
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"ファイルサイズが大きすぎます: {len(file_content) / 1024 / 1024:.1f}MB（制限: 500MB）"
            )
        
        # ユニークファイル名生成
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOAD_DIR / unique_filename
        
        # ファイル保存
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # メディアタイプ判定
        media_type = MediaType.VIDEO if file_ext in ['.mp4', '.avi', '.mov'] else MediaType.IMAGE
        
        return FileUploadResponse(
            success=True,
            filename=unique_filename,
            file_path=str(file_path),
            file_size=len(file_content),
            media_type=media_type,
            message=f"ファイル「{file.filename}」をアップロードしました"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ファイルアップロードエラー: {str(e)}")

@app.post("/face-swap/image", response_model=FaceSwapResponse, tags=["Face Swap"])
async def face_swap_image(
    background_tasks: BackgroundTasks,
    source_file: UploadFile = File(..., description="ソース画像ファイル"),
    target_file: UploadFile = File(..., description="ターゲット画像ファイル"),
    model: str = Form(default="inswapper_128", description="使用するモデル"),
    quality: int = Form(default=90, ge=1, le=100, description="出力品質"),
    pixel_boost: str = Form(default="128x128", description="ピクセルブースト解像度")
):
    """画像Face Swap処理"""
    start_time = time.time()
    
    try:
        # ファイル検証
        for file in [source_file, target_file]:
            file_ext = Path(file.filename).suffix.lower()
            if file_ext not in ['.jpg', '.jpeg', '.png']:
                raise HTTPException(
                    status_code=400, 
                    detail=f"画像ファイルのみ対応: {file.filename}"
                )
        
        # ファイル保存
        source_filename = f"source_{uuid.uuid4()}{Path(source_file.filename).suffix}"
        target_filename = f"target_{uuid.uuid4()}{Path(target_file.filename).suffix}"
        output_filename = f"output_{uuid.uuid4()}.jpg"
        
        source_path = UPLOAD_DIR / source_filename
        target_path = UPLOAD_DIR / target_filename
        output_path = OUTPUT_DIR / output_filename
        
        # ファイル保存
        for file, path in [(source_file, source_path), (target_file, target_path)]:
            content = await file.read()
            with open(path, "wb") as f:
                f.write(content)
        
        # ファイル検証
        validation = facefusion_service.validate_files(str(source_path), str(target_path))
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail="; ".join(validation["errors"]))
        
        # Face Swap実行
        result = facefusion_service.face_swap_image(
            source_path=str(source_path),
            target_path=str(target_path),
            output_path=str(output_path),
            model=model,
            quality=quality,
            pixel_boost=pixel_boost
        )
        
        # 一時ファイル削除をバックグラウンドタスクに追加
        background_tasks.add_task(cleanup_temp_files, [source_path, target_path])
        
        if result["success"]:
            return FaceSwapResponse(
                success=True,
                message="🎭 画像Face Swap完了！",
                output_filename=output_filename,
                file_size=result["file_size"],
                media_type=MediaType.IMAGE,
                processing_time=result["processing_time"],
                model_used=result.get("model_used"),
                quality=result.get("quality")
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "処理に失敗しました"))
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"画像処理エラー: {str(e)}")

@app.post("/face-swap/video", response_model=FaceSwapResponse, tags=["Face Swap"])
async def face_swap_video(
    background_tasks: BackgroundTasks,
    source_file: UploadFile = File(..., description="ソース画像ファイル"),
    target_file: UploadFile = File(..., description="ターゲット動画ファイル"),
    model: str = Form(default="inswapper_128", description="使用するモデル"),
    quality: int = Form(default=80, ge=1, le=100, description="動画品質"),
    pixel_boost: str = Form(default="128x128", description="ピクセルブースト解像度"),
    trim_start: int = Form(default=0, ge=0, description="開始フレーム"),
    trim_end: Optional[int] = Form(default=None, description="終了フレーム"),
    max_frames: int = Form(default=50, ge=1, le=200, description="最大フレーム数")
):
    """動画Face Swap処理"""
    start_time = time.time()
    
    try:
        # ファイル検証
        source_ext = Path(source_file.filename).suffix.lower()
        target_ext = Path(target_file.filename).suffix.lower()
        
        if source_ext not in ['.jpg', '.jpeg', '.png']:
            raise HTTPException(status_code=400, detail="ソースは画像ファイルである必要があります")
        
        if target_ext not in ['.mp4', '.avi', '.mov']:
            raise HTTPException(status_code=400, detail="ターゲットは動画ファイルである必要があります")
        
        # ファイル保存
        source_filename = f"source_{uuid.uuid4()}{source_ext}"
        target_filename = f"target_{uuid.uuid4()}{target_ext}"
        output_filename = f"output_{uuid.uuid4()}.mp4"
        
        source_path = UPLOAD_DIR / source_filename
        target_path = UPLOAD_DIR / target_filename
        output_path = OUTPUT_DIR / output_filename
        
        # ファイル保存
        for file, path in [(source_file, source_path), (target_file, target_path)]:
            content = await file.read()
            with open(path, "wb") as f:
                f.write(content)
        
        # ファイル検証
        validation = facefusion_service.validate_files(str(source_path), str(target_path))
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail="; ".join(validation["errors"]))
        
        # Face Swap実行
        result = facefusion_service.face_swap_video(
            source_path=str(source_path),
            target_path=str(target_path),
            output_path=str(output_path),
            model=model,
            quality=quality,
            pixel_boost=pixel_boost,
            trim_start=trim_start,
            trim_end=trim_end,
            max_frames=max_frames
        )
        
        # 一時ファイル削除をバックグラウンドタスクに追加
        background_tasks.add_task(cleanup_temp_files, [source_path, target_path])
        
        if result["success"]:
            return FaceSwapResponse(
                success=True,
                message="🎬 動画Face Swap完了！",
                output_filename=output_filename,
                file_size=result["file_size"],
                media_type=MediaType.VIDEO,
                processing_time=result["processing_time"],
                model_used=result.get("model_used"),
                quality=result.get("quality")
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "処理に失敗しました"))
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"動画処理エラー: {str(e)}")

@app.post("/cli/face-swap", response_model=dict, tags=["CLI"])
async def cli_face_swap(request: CLIFaceSwapRequest):
    """CLI形式でのFace Swap実行"""
    try:
        # パスの検証
        if not os.path.exists(request.source_path):
            raise HTTPException(status_code=400, detail=f"ソースファイルが見つかりません: {request.source_path}")
        
        if not os.path.exists(request.target_path):
            raise HTTPException(status_code=400, detail=f"ターゲットファイルが見つかりません: {request.target_path}")
        
        # 出力ディレクトリ作成
        os.makedirs(os.path.dirname(request.output_path), exist_ok=True)
        
        # メディアタイプ判定
        target_ext = Path(request.target_path).suffix.lower()
        is_video = target_ext in ['.mp4', '.avi', '.mov']
        
        # Face Swap実行
        if is_video:
            result = facefusion_service.face_swap_video(
                source_path=request.source_path,
                target_path=request.target_path,
                output_path=request.output_path,
                model=request.face_swapper_model,
                quality=request.output_video_quality,
                trim_start=request.trim_frame_start or 0,
                trim_end=request.trim_frame_end
            )
        else:
            result = facefusion_service.face_swap_image(
                source_path=request.source_path,
                target_path=request.target_path,
                output_path=request.output_path,
                model=request.face_swapper_model,
                quality=request.output_image_quality
            )
        
        return {
            "success": result["success"],
            "message": "CLI Face Swap実行完了",
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CLI実行エラー: {str(e)}")

@app.get("/download/{filename}", tags=["ファイル"])
async def download_file(filename: str):
    """ファイルダウンロード"""
    try:
        file_path = OUTPUT_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="ファイルが見つかりません")
        
        # メディアタイプ判定
        ext = file_path.suffix.lower()
        if ext in ['.mp4', '.avi', '.mov']:
            media_type = "video/mp4"
        elif ext in ['.jpg', '.jpeg']:
            media_type = "image/jpeg"
        elif ext == '.png':
            media_type = "image/png"
        else:
            media_type = "application/octet-stream"
        
        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ダウンロードエラー: {str(e)}")

@app.get("/cli-help", response_class=HTMLResponse, tags=["CLI"])
async def cli_help():
    """CLI使用方法ヘルプ"""
    help_html = """
    <html>
    <head>
        <title>FaceFusion CLI Help</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            code { background-color: #f4f4f4; padding: 10px; display: block; }
            .example { background-color: #e8f4fd; padding: 15px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>🎭 FaceFusion CLI Help</h1>
        <p>べ、別にあんたのために説明してあげるわけじゃないけど...</p>
        
        <h2>基本的な使用方法</h2>
        <div class="example">
            <h3>画像Face Swap</h3>
            <code>
curl -X POST "http://localhost:8000/cli/face-swap" \\
     -H "Content-Type: application/json" \\
     -d '{
       "source_path": "/app/data/source/source.jpg",
       "target_path": "/app/data/source/target.jpg", 
       "output_path": "/app/data/output/result.jpg",
       "face_swapper_model": "inswapper_128",
       "output_image_quality": 90
     }'
            </code>
        </div>
        
        <div class="example">
            <h3>動画Face Swap</h3>
            <code>
curl -X POST "http://localhost:8000/cli/face-swap" \\
     -H "Content-Type: application/json" \\
     -d '{
       "source_path": "/app/data/source/source.jpg",
       "target_path": "/app/data/source/target.mp4",
       "output_path": "/app/data/output/result.mp4",
       "face_swapper_model": "ghost_2_256",
       "output_video_quality": 80,
       "trim_frame_start": 0,
       "trim_frame_end": 100
     }'
            </code>
        </div>
        
        <h2>利用可能なモデル</h2>
        <ul>
            <li><strong>inswapper_128</strong> - 高速・標準品質</li>
            <li><strong>ghost_2_256</strong> - 最高品質（推奨）</li>
            <li><strong>blendswap_256</strong> - 自然な仕上がり</li>
        </ul>
        
        <h2>パスの指定</h2>
        <ul>
            <li>ソースファイル: <code>/app/data/source/</code></li>
            <li>出力ファイル: <code>/app/data/output/</code></li>
        </ul>
    </body>
    </html>
    """
    return help_html

async def cleanup_temp_files(file_paths: list):
    """一時ファイル削除"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete temp file {file_path}: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        timeout_keep_alive=1800,  # 30分のkeep-alive
        timeout_graceful_shutdown=30
    ) 