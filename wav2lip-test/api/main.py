"""
Wav2Lip FastAPI Application
口パク動画生成のためのRESTful API - CLIで成功したコマンドをそのまま使用
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import shutil
import asyncio
import time
from pathlib import Path
from typing import Optional
import logging

from src.wav2lip_cli_wrapper import Wav2LipCLIWrapper
from src.models import ProcessRequest, ProcessResponse, ProcessStatus

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Wav2Lip API - CLI Wrapper",
    description="口パク動画生成API - CLIで成功したコマンドをそのまま使用",
    version="2.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CLIラッパーサービス初期化
wav2lip_cli = Wav2LipCLIWrapper()

# 処理状況を管理する辞書
processing_status = {}

@app.get("/")
async def root():
    """ヘルスチェック"""
    return {
        "message": "Wav2Lip CLI Wrapper API is running", 
        "status": "healthy",
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    """詳細なヘルスチェック"""
    model_info = wav2lip_cli.get_model_info()
    return {
        "status": "healthy",
        "models_loaded": wav2lip_cli.is_model_loaded(),
        "model_info": model_info
    }

@app.post("/process", response_model=ProcessResponse)
async def process_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(..., description="入力動画ファイル (.mp4, .avi)"),
    audio: UploadFile = File(..., description="音声ファイル (.wav, .mp3)"),
    pads: Optional[str] = "0 10 0 0",  # スペース区切りに変更
    face_det_batch_size: Optional[int] = 1,
    wav2lip_batch_size: Optional[int] = 4,
    resize_factor: Optional[int] = 1,
    quality: Optional[str] = "high"
):
    """
    動画と音声から口パク動画を生成（CLIで成功したコマンドを使用）
    
    Args:
        video: 入力動画ファイル
        audio: 音声ファイル
        pads: パディング設定 (上 下 左 右) - スペース区切り
        face_det_batch_size: 顔検出バッチサイズ
        wav2lip_batch_size: Wav2Lipバッチサイズ
        resize_factor: リサイズ係数
        quality: 品質設定 (low, medium, high)
    """
    
    # ジョブIDを生成
    job_id = str(uuid.uuid4())
    
    try:
        # ファイル検証
        if not video.filename.lower().endswith(('.mp4', '.avi')):
            raise HTTPException(status_code=400, detail="動画ファイルは .mp4 または .avi 形式である必要があります")
        
        if not audio.filename.lower().endswith(('.wav', '.mp3')):
            raise HTTPException(status_code=400, detail="音声ファイルは .wav または .mp3 形式である必要があります")
        
        # パディング設定の検証（スペース区切り）
        try:
            pads_list = pads.strip().split()
            if len(pads_list) != 4:
                raise ValueError("パディングは4つの値が必要です")
            # 数値に変換できるかチェック
            [int(p) for p in pads_list]
        except ValueError:
            raise HTTPException(status_code=400, detail="パディング設定が無効です。例: '0 10 0 0'")
        
        # 処理状況を初期化
        processing_status[job_id] = {
            "status": "uploading",
            "progress": 0,
            "message": "ファイルをアップロード中..."
        }
        
        # ファイル内容を事前に読み込み
        video_content = await video.read()
        audio_content = await audio.read()
        
        logger.info(f"Read video file: {video.filename}, size: {len(video_content)} bytes")
        logger.info(f"Read audio file: {audio.filename}, size: {len(audio_content)} bytes")
        
        # バックグラウンドで処理を開始
        background_tasks.add_task(
            process_video_background_cli,
            job_id=job_id,
            video_content=video_content,
            audio_content=audio_content,
            video_filename=video.filename,
            audio_filename=audio.filename,
            pads=pads,
            face_det_batch_size=face_det_batch_size,
            wav2lip_batch_size=wav2lip_batch_size,
            resize_factor=resize_factor
        )
        
        return ProcessResponse(
            job_id=job_id,
            status="processing",
            message="処理を開始しました（CLIラッパー使用）"
        )
        
    except Exception as e:
        logger.error(f"Error starting process: {str(e)}")
        raise HTTPException(status_code=500, detail=f"処理開始エラー: {str(e)}")

@app.get("/status/{job_id}", response_model=ProcessStatus)
async def get_status(job_id: str):
    """処理状況を取得"""
    if job_id not in processing_status:
        raise HTTPException(status_code=404, detail="ジョブが見つかりません")
    
    return ProcessStatus(**processing_status[job_id])

@app.get("/download/{job_id}")
async def download_result(job_id: str):
    """結果動画をダウンロード"""
    if job_id not in processing_status:
        raise HTTPException(status_code=404, detail="ジョブが見つかりません")
    
    status = processing_status[job_id]
    if status["status"] != "completed":
        raise HTTPException(status_code=400, detail="処理が完了していません")
    
    output_path = status.get("output_path")
    if not output_path or not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="出力ファイルが見つかりません")
    
    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename=f"wav2lip_result_{job_id}.mp4"
    )

async def process_video_background_cli(
    job_id: str,
    video_content: bytes,
    audio_content: bytes,
    video_filename: str,
    audio_filename: str,
    pads: str,
    face_det_batch_size: int,
    wav2lip_batch_size: int,
    resize_factor: int
):
    """バックグラウンドでの動画処理（CLIラッパー使用）"""
    
    start_time = time.time()
    
    try:
        # 処理状況を更新
        processing_status[job_id].update({
            "status": "processing",
            "progress": 10,
            "message": "CLIラッパーで処理を開始中..."
        })
        
        # CLIラッパーで処理
        result = await wav2lip_cli.process_video_cli(
            job_id=job_id,
            video_content=video_content,
            audio_content=audio_content,
            video_filename=video_filename,
            audio_filename=audio_filename,
            pads=pads,
            face_det_batch_size=face_det_batch_size,
            wav2lip_batch_size=wav2lip_batch_size,
            resize_factor=resize_factor,
            processing_status=processing_status
        )
        
        # 処理時間を計算
        processing_time = time.time() - start_time
        
        # 処理完了
        processing_status[job_id].update({
            "status": "completed",
            "progress": 100,
            "message": "処理が完了しました",
            "output_path": result["output_path"],
            "processing_time": processing_time
        })
        
        logger.info(f"Job {job_id} completed successfully in {processing_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Background processing error for job {job_id}: {str(e)}")
        processing_status[job_id].update({
            "status": "failed",
            "progress": 0,
            "message": f"処理エラー: {str(e)}"
        })

@app.delete("/cleanup/{job_id}")
async def cleanup_job(job_id: str):
    """ジョブのクリーンアップ"""
    if job_id in processing_status:
        # 一時ファイルを削除
        await wav2lip_cli.cleanup_job(job_id)
        del processing_status[job_id]
        return {"message": "ジョブをクリーンアップしました"}
    else:
        raise HTTPException(status_code=404, detail="ジョブが見つかりません")

@app.get("/models/info")
async def get_model_info():
    """モデル情報を取得"""
    return wav2lip_cli.get_model_info()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 