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
app = FastAPI(title="Wav2Lip API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wav2Lipの実行パス
WAV2LIP_PATH = "/workspace/Wav2Lip"
sys.path.append(WAV2LIP_PATH)

# モデルパス
WAV2LIP_MODEL = os.environ.get("WAV2LIP_MODEL_PATH", "/workspace/models/wav2lip_gan.pth")

# 出力ディレクトリ
OUTPUT_DIR = "/workspace/data/output"
TEMP_DIR = "/workspace/Wav2Lip/temp"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# 進行状況追跡用
task_status = {}

# モデル定義
class GenerateRequest(BaseModel):
    video_file: str
    audio_file: str
    output_file: Optional[str] = None
    nosmooth: Optional[bool] = False

class GenerateResponse(BaseModel):
    output_file: str
    status: str
    
# ヘルスチェックエンドポイント
@app.get("/")
async def root():
    return {"status": "ok", "message": "Wav2Lip API is running"}

# リップシンク処理をバックグラウンドで実行
def run_lip_sync(
    task_id: str,
    video_file: str,
    audio_file: str,
    output_file: str,
    nosmooth: bool = False
):
    try:
        # 入出力ファイルパスの確認
        if not os.path.exists(video_file):
            task_status[task_id] = {"status": "error", "message": f"Video file not found: {video_file}"}
            return
            
        if not os.path.exists(audio_file):
            task_status[task_id] = {"status": "error", "message": f"Audio file not found: {audio_file}"}
            return
            
        if not os.path.exists(WAV2LIP_MODEL):
            task_status[task_id] = {"status": "error", "message": f"Model file not found: {WAV2LIP_MODEL}"}
            return
        
        # 出力ディレクトリの確認
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        
        # Wav2Lipコマンドの構築
        cmd = [
            "python", 
            os.path.join(WAV2LIP_PATH, "inference.py"),
            "--checkpoint_path", WAV2LIP_MODEL,
            "--face", video_file,
            "--audio", audio_file,
            "--outfile", output_file,
            "--pads", "0", "0", "0", "0"  # 必要に応じて調整
        ]
        
        # スムージングオプション
        if nosmooth:
            cmd.append("--nosmooth")
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        # Wav2Lip実行
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
            logger.error(f"Wav2Lip failed: {stderr}")
            task_status[task_id] = {"status": "error", "message": stderr}
            return
            
        if not os.path.exists(output_file):
            logger.error(f"Output file not created: {output_file}")
            task_status[task_id] = {"status": "error", "message": "Output file not created"}
            return
            
        # 成功
        task_status[task_id] = {"status": "completed", "output_file": output_file}
        logger.info(f"Wav2Lip completed: {output_file}")
        
    except Exception as e:
        logger.error(f"Error in lip sync: {str(e)}")
        task_status[task_id] = {"status": "error", "message": str(e)}

# リップシンク生成エンドポイント
@app.post("/generate", response_model=GenerateResponse)
async def generate_lip_sync(request: GenerateRequest, background_tasks: BackgroundTasks):
    logger.info(f"Generate request: video={request.video_file}, audio={request.audio_file}")
    
    # 出力ファイル名の設定
    output_filename = request.output_file if request.output_file else f"wav2lip_{uuid.uuid4()}.mp4"
    
    if not output_filename.startswith("/"):
        output_path = os.path.join(OUTPUT_DIR, output_filename)
    else:
        output_path = output_filename
    
    # タスクID
    task_id = str(uuid.uuid4())
    
    # バックグラウンドで処理開始
    background_tasks.add_task(
        run_lip_sync,
        task_id,
        request.video_file,
        request.audio_file,
        output_path,
        request.nosmooth
    )
    
    # タスク初期状態
    task_status[task_id] = {"status": "queued"}
    
    # 同期的に処理（テスト用）
    run_lip_sync(
        task_id,
        request.video_file,
        request.audio_file,
        output_path,
        request.nosmooth
    )
    
    # 処理結果確認
    if task_status[task_id]["status"] == "error":
        raise HTTPException(status_code=500, detail=task_status[task_id]["message"])
    
    return {"output_file": output_path, "status": "completed"}

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
    uvicorn.run(app, host="0.0.0.0", port=8004) 