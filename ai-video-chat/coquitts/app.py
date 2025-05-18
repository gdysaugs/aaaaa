#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import uuid
import torch
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Coqui TTS APIをインポート
from TTS.api import TTS

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# アプリケーション初期化
app = FastAPI(title="CoquiTTS API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 出力ディレクトリ
OUTPUT_DIR = "/app/data/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# モデル定義
class SynthesisRequest(BaseModel):
    text: str
    speaker_wav: str
    language: str = "ja"
    output_file: Optional[str] = None

class SynthesisResponse(BaseModel):
    output_file: str
    text: str
    
# デバイスの設定
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {device}")

# モデルをグローバル変数として保持（初回呼び出し時にロード）
tts_model = None

def get_tts_model():
    global tts_model
    if tts_model is None:
        logger.info("Loading TTS model...")
        try:
            tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
            logger.info("TTS model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading TTS model: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to load TTS model: {str(e)}")
    return tts_model

# ヘルスチェックエンドポイント
@app.get("/")
async def root():
    return {"status": "ok", "message": "CoquiTTS API is running"}

# 音声合成エンドポイント
@app.post("/synthesize", response_model=SynthesisResponse)
async def synthesize(request: SynthesisRequest):
    logger.info(f"Synthesis request: {request.text[:50]}... (lang: {request.language})")
    
    # 話者音声ファイルの存在確認
    speaker_wav_path = request.speaker_wav
    if not os.path.exists(speaker_wav_path):
        raise HTTPException(status_code=404, detail=f"Speaker audio file not found: {speaker_wav_path}")
    
    # 出力ファイル名の設定
    output_filename = request.output_file if request.output_file else f"tts_{uuid.uuid4()}.wav"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    try:
        # TTSモデル取得
        tts = get_tts_model()
        
        # 音声合成実行
        logger.info(f"Generating speech for: {request.text[:50]}...")
        tts.tts_to_file(
            text=request.text,
            speaker_wav=speaker_wav_path,
            language=request.language,
            file_path=output_path
        )
        
        logger.info(f"Speech synthesis completed: {output_path}")
        return {"output_file": output_path, "text": request.text}
        
    except Exception as e:
        logger.error(f"Error in speech synthesis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to synthesize speech: {str(e)}")

# 音声ファイル取得エンドポイント
@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Audio file not found: {filename}")
    
    return FileResponse(file_path, media_type="audio/wav")

# 利用可能なモデル情報取得
@app.get("/models")
async def list_models():
    try:
        tts_api = TTS()
        available_models = tts_api.list_models()
        
        # XTTSとYour TTSモデルだけをフィルタリング
        xtts_models = [model for model in available_models if "xtts" in model.lower() or "your_tts" in model.lower()]
        
        return {"models": xtts_models}
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 