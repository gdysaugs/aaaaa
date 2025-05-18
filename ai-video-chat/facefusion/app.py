#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import uuid
import logging
import subprocess
from typing import Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# アプリケーション初期化
app = FastAPI(title="FaceFusion API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FaceFusionの実行パス
FACEFUSION_PATH = "/app/facefusion"
sys.path.append(FACEFUSION_PATH)

# 出力ディレクトリ
OUTPUT_DIR = "/app/data/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 進行状況追跡用
task_status = {}

# モデル定義
class SwapRequest(BaseModel):
    source_video: str
    target_face: str
    output_file: Optional[str] = None
    reference_face: Optional[str] = None
    reference_frame_number: Optional[int] = 0

class SwapResponse(BaseModel):
    output_path: str
    status: str
    
# ヘルスチェックエンドポイント
@app.get("/")
async def root():
    return {"status": "ok", "message": "FaceFusion API is running"}

# 顔入れ替え処理をバックグラウンドで実行
def run_face_swap(
    task_id: str,
    source_video: str,
    target_face: str,
    output_file: str,
    reference_face: Optional[str] = None,
    reference_frame_number: Optional[int] = 0
):
    try:
        # 入出力ファイルパスの確認
        if not os.path.exists(source_video):
            task_status[task_id] = {"status": "error", "message": f"Source video not found: {source_video}"}
            return
            
        if not os.path.exists(target_face):
            task_status[task_id] = {"status": "error", "message": f"Target face not found: {target_face}"}
            return
        
        # 出力ディレクトリの確認
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        
        # FaceFusionコマンドの構築
        cmd = [
            "python", 
            os.path.join(FACEFUSION_PATH, "facefusion.py"),
            "--source", target_face,
            "--target", source_video,
            "--output", output_file,
            "--execution-provider", "cuda",
            "--output-video-quality", "28",
            "--headless"
        ]
        
        # リファレンス顔が指定されている場合
        if reference_face and os.path.exists(reference_face):
            cmd.extend(["--reference-face", reference_face])
            cmd.extend(["--reference-frame-number", str(reference_frame_number)])
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        # FaceFusion実行
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # 進行状況更新
        task_status[task_id] = {"status": "processing"}
        
        # 処理完了待ち
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            logger.error(f"FaceFusion failed: {stderr}")
            task_status[task_id] = {"status": "error", "message": stderr}
            return
            
        if not os.path.exists(output_file):
            logger.error(f"Output file not created: {output_file}")
            task_status[task_id] = {"status": "error", "message": "Output file not created"}
            return
            
        # 成功
        task_status[task_id] = {"status": "completed", "output_path": output_file}
        logger.info(f"FaceFusion completed: {output_file}")
        
    except Exception as e:
        logger.error(f"Error in face swap: {str(e)}")
        task_status[task_id] = {"status": "error", "message": str(e)}

# 顔入れ替えエンドポイント
@app.post("/swap", response_model=SwapResponse)
async def swap_face(request: SwapRequest, background_tasks: BackgroundTasks):
    logger.info(f"Swap request: {request.source_video} -> {request.target_face}")
    
    # 出力ファイル名の設定
    source_name = os.path.basename(request.source_video).split(".")[0]
    target_name = os.path.basename(request.target_face).split(".")[0]
    output_filename = request.output_file if request.output_file else f"facefusion_{source_name}_{target_name}_{uuid.uuid4()}.mp4"
    
    if not output_filename.startswith("/"):
        output_path = os.path.join(OUTPUT_DIR, output_filename)
    else:
        output_path = output_filename
    
    # タスクID
    task_id = str(uuid.uuid4())
    
    # バックグラウンドで処理開始
    background_tasks.add_task(
        run_face_swap,
        task_id,
        request.source_video,
        request.target_face,
        output_path,
        request.reference_face,
        request.reference_frame_number
    )
    
    # タスク初期状態
    task_status[task_id] = {"status": "queued"}
    
    # 同期的に処理（小さなファイルなどでテスト用）
    run_face_swap(
        task_id,
        request.source_video,
        request.target_face,
        output_path,
        request.reference_face,
        request.reference_frame_number
    )
    
    # 処理結果確認
    if task_status[task_id]["status"] == "error":
        raise HTTPException(status_code=500, detail=task_status[task_id]["message"])
    
    return {"output_path": output_path, "status": "completed"}

# タスク状態確認エンドポイント
@app.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_status[task_id]

# 出力ファイル取得エンドポイント
@app.get("/video/{filename}")
async def get_video(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Video file not found: {filename}")
    
    return FileResponse(file_path, media_type="video/mp4")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003) 