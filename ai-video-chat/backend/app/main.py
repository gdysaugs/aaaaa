import os
import time
import uuid
import httpx
import asyncio
import logging
from typing import List, Optional
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# 環境変数のロード
load_dotenv()

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# アプリケーション初期化
app = FastAPI(title="AI Video Chat API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設定
DATA_SOURCE_DIR = os.getenv("DATA_SOURCE_DIR", "/app/data/source")
DATA_OUTPUT_DIR = os.getenv("DATA_OUTPUT_DIR", "/app/data/output")
LLAMA_API_URL = os.getenv("LLAMA_API_URL", "http://llama:8001")
COQUI_API_URL = os.getenv("COQUI_API_URL", "http://coquitts:8002")
FACEFUSION_API_URL = os.getenv("FACEFUSION_API_URL", "http://facefusion:8003")
WAV2LIP_API_URL = os.getenv("WAV2LIP_API_URL", "http://wav2lip:8004")

# ディレクトリが存在することを確認
os.makedirs(DATA_SOURCE_DIR, exist_ok=True)
os.makedirs(DATA_OUTPUT_DIR, exist_ok=True)

# モデル定義
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    video_id: Optional[str] = None

class ChatResponse(BaseModel):
    text: str
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    processing: bool = False

class VideoOptions(BaseModel):
    source_video: str
    target_face: str
    voice_sample: Optional[str] = None
    
# ヘルスチェックエンドポイント
@app.get("/")
async def root():
    return {"status": "ok", "message": "AI Video Chat API is running"}

# 素材動画一覧取得
@app.get("/videos/source")
async def list_source_videos():
    videos = []
    for file in Path(DATA_SOURCE_DIR).glob("*.mp4"):
        videos.append({
            "id": file.stem,
            "name": file.name,
            "url": f"/data/source/{file.name}",
            "created": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
        })
    return {"videos": videos}

# 顔画像一覧取得
@app.get("/faces")
async def list_faces():
    faces = []
    for file in Path(DATA_SOURCE_DIR).glob("*.jpg"):
        faces.append({
            "id": file.stem,
            "name": file.name,
            "url": f"/data/source/{file.name}",
            "created": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
        })
    for file in Path(DATA_SOURCE_DIR).glob("*.png"):
        faces.append({
            "id": file.stem,
            "name": file.name,
            "url": f"/data/source/{file.name}",
            "created": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
        })
    return {"faces": faces}

# 音声サンプル一覧取得
@app.get("/voices")
async def list_voices():
    voices = []
    for file in Path(DATA_SOURCE_DIR).glob("*.wav"):
        voices.append({
            "id": file.stem,
            "name": file.name,
            "url": f"/data/source/{file.name}",
            "created": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
        })
    return {"voices": voices}

# 素材アップロード
@app.post("/upload/{file_type}")
async def upload_file(file_type: str, file: UploadFile = File(...)):
    if file_type not in ["video", "face", "voice"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # ファイル拡張子チェック
    valid_extensions = {
        "video": [".mp4"],
        "face": [".jpg", ".png"],
        "voice": [".wav"]
    }
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in valid_extensions[file_type]:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file extension. Allowed: {valid_extensions[file_type]}"
        )
    
    # ファイル保存
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(DATA_SOURCE_DIR, filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {
        "filename": filename,
        "file_type": file_type,
        "url": f"/data/source/{filename}"
    }

# FaceFusionで顔入れ替え処理
async def process_face_fusion(source_video: str, target_face: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=600) as client:  # 10分タイムアウト
            response = await client.post(
                f"{FACEFUSION_API_URL}/swap",
                json={
                    "source_video": f"/app/data/source/{source_video}",
                    "target_face": f"/app/data/source/{target_face}",
                    "output_file": f"/app/data/output/facefusion_{uuid.uuid4()}.mp4"
                }
            )
            if response.status_code != 200:
                logger.error(f"FaceFusion error: {response.text}")
                raise HTTPException(status_code=500, detail="FaceFusion processing failed")
            
            result = response.json()
            return result["output_path"].split("/")[-1]
    except Exception as e:
        logger.error(f"FaceFusion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"FaceFusion processing failed: {str(e)}")

# Llama.cppでチャット応答生成
async def get_llama_response(messages: List[ChatMessage]) -> str:
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{LLAMA_API_URL}/v1/chat/completions",
                json={
                    "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            )
            if response.status_code != 200:
                logger.error(f"Llama.cpp error: {response.text}")
                raise HTTPException(status_code=500, detail="Failed to get response from LLM")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Llama.cpp error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get response from LLM: {str(e)}")

# CoquiTTSで音声合成
async def synthesize_speech(text: str, voice_sample: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{COQUI_API_URL}/synthesize",
                json={
                    "text": text,
                    "speaker_wav": f"/app/data/source/{voice_sample}",
                    "language": "ja"  # 日本語を指定
                }
            )
            if response.status_code != 200:
                logger.error(f"CoquiTTS error: {response.text}")
                raise HTTPException(status_code=500, detail="Speech synthesis failed")
            
            result = response.json()
            return result["output_file"].split("/")[-1]
    except Exception as e:
        logger.error(f"CoquiTTS error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")

# Wav2Lipでリップシンク
async def create_lip_sync(video_file: str, audio_file: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=300) as client:  # 5分タイムアウト
            response = await client.post(
                f"{WAV2LIP_API_URL}/generate",
                json={
                    "video_file": f"/workspace/data/output/{video_file}",
                    "audio_file": f"/workspace/data/output/{audio_file}",
                    "output_file": f"/workspace/data/output/final_{uuid.uuid4()}.mp4"
                }
            )
            if response.status_code != 200:
                logger.error(f"Wav2Lip error: {response.text}")
                raise HTTPException(status_code=500, detail="Lip sync failed")
            
            result = response.json()
            return result["output_file"].split("/")[-1]
    except Exception as e:
        logger.error(f"Wav2Lip error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lip sync failed: {str(e)}")

# バックグラウンドで全処理を実行
async def process_video_chat(
    request_id: str,
    messages: List[ChatMessage],
    video_file: str,
    face_file: str,
    voice_file: str
):
    try:
        # 1. Llama.cppで返答生成
        llm_response = await get_llama_response(messages)
        
        # 進捗状況更新（ファイルベース）
        with open(os.path.join(DATA_OUTPUT_DIR, f"{request_id}_progress.txt"), "w") as f:
            f.write("llm_response_completed\n")
            f.write(llm_response)
        
        # 2. CoquiTTSで音声合成
        audio_file = await synthesize_speech(llm_response, voice_file)
        
        # 進捗状況更新
        with open(os.path.join(DATA_OUTPUT_DIR, f"{request_id}_progress.txt"), "a") as f:
            f.write("\naudio_completed\n")
            f.write(audio_file)
        
        # 3. FaceFusionで顔入れ替え（まだ処理されていない場合）
        face_fusion_file = await process_face_fusion(video_file, face_file)
        
        # 進捗状況更新
        with open(os.path.join(DATA_OUTPUT_DIR, f"{request_id}_progress.txt"), "a") as f:
            f.write("\nface_fusion_completed\n")
            f.write(face_fusion_file)
        
        # 4. Wav2Lipでリップシンク
        final_video = await create_lip_sync(face_fusion_file, audio_file)
        
        # 処理完了
        with open(os.path.join(DATA_OUTPUT_DIR, f"{request_id}_progress.txt"), "a") as f:
            f.write("\ncompleted\n")
            f.write(final_video)

    except Exception as e:
        logger.error(f"Processing error for {request_id}: {str(e)}")
        with open(os.path.join(DATA_OUTPUT_DIR, f"{request_id}_progress.txt"), "a") as f:
            f.write(f"\nerror\n{str(e)}")

# 事前に処理した顔入れ替え動画を使用してチャット処理
@app.post("/chat")
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    request_id = str(uuid.uuid4())
    
    # ビデオIDが指定されていない場合はエラー
    if not request.video_id:
        raise HTTPException(status_code=400, detail="Video ID is required")
    
    # ビデオID形式をパース
    try:
        parts = request.video_id.split("_")
        video_file = parts[0]
        face_file = parts[1]
        voice_file = parts[2] if len(parts) > 2 else None
    except:
        raise HTTPException(status_code=400, detail="Invalid video_id format")

    # 必要なファイルが存在するか確認
    video_path = Path(DATA_SOURCE_DIR) / video_file
    face_path = Path(DATA_SOURCE_DIR) / face_file
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail=f"Source video {video_file} not found")
    if not face_path.exists():
        raise HTTPException(status_code=404, detail=f"Target face {face_file} not found")
    
    if voice_file:
        voice_path = Path(DATA_SOURCE_DIR) / voice_file
        if not voice_path.exists():
            raise HTTPException(status_code=404, detail=f"Voice sample {voice_file} not found")
    else:
        # 音声が指定されていない場合はデフォルトを使用
        # TODO: デフォルト音声の実装
        raise HTTPException(status_code=400, detail="Voice sample is required")
    
    # バックグラウンドで処理開始
    background_tasks.add_task(
        process_video_chat,
        request_id,
        request.messages,
        video_file,
        face_file, 
        voice_file
    )
    
    # 処理開始を示す進捗ファイル作成
    with open(os.path.join(DATA_OUTPUT_DIR, f"{request_id}_progress.txt"), "w") as f:
        f.write("started\n")
    
    return {
        "request_id": request_id,
        "status": "processing",
        "message": "Video chat processing started"
    }

# チャット処理状況確認
@app.get("/chat/status/{request_id}")
async def chat_status(request_id: str):
    progress_file = Path(DATA_OUTPUT_DIR) / f"{request_id}_progress.txt"
    
    if not progress_file.exists():
        raise HTTPException(status_code=404, detail="Request not found")
    
    # 進捗ファイル読み取り
    with open(progress_file, "r") as f:
        progress = f.read()
    
    lines = progress.strip().split("\n")
    status = lines[0]
    
    response = {
        "request_id": request_id,
        "status": status
    }
    
    # 進捗状況に応じた追加情報
    if status == "completed":
        final_video = lines[-1]
        response["video_url"] = f"/data/output/{final_video}"
    elif status == "error":
        response["error"] = lines[-1] if len(lines) > 1 else "Unknown error"
    elif status == "llm_response_completed":
        response["text"] = lines[1] if len(lines) > 1 else ""
    elif status in ["audio_completed", "face_fusion_completed"]:
        response["text"] = lines[1] if len(lines) > 1 else ""
        audio_file = lines[3] if len(lines) > 3 and status == "face_fusion_completed" else \
                   lines[3] if len(lines) > 3 and status == "audio_completed" else ""
        if audio_file:
            response["audio_url"] = f"/data/output/{audio_file}"
    
    return response

# 素材準備（FaceFusionで顔入れ替えを事前に実行）
@app.post("/prepare")
async def prepare_video(options: VideoOptions, background_tasks: BackgroundTasks):
    video_file = options.source_video
    face_file = options.target_face
    voice_file = options.voice_sample
    
    # 必要なファイルが存在するか確認
    video_path = Path(DATA_SOURCE_DIR) / video_file
    face_path = Path(DATA_SOURCE_DIR) / face_file
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail=f"Source video {video_file} not found")
    if not face_path.exists():
        raise HTTPException(status_code=404, detail=f"Target face {face_file} not found")
    
    if voice_file:
        voice_path = Path(DATA_SOURCE_DIR) / voice_file
        if not voice_path.exists():
            raise HTTPException(status_code=404, detail=f"Voice sample {voice_file} not found")
    
    # 組み合わせのIDを生成
    combo_id = f"{video_file}_{face_file}"
    if voice_file:
        combo_id += f"_{voice_file}"
    
    # すでに処理済みかチェック
    existing_fusions = list(Path(DATA_OUTPUT_DIR).glob(f"facefusion_{video_file}_{face_file}_*.mp4"))
    if existing_fusions:
        return {
            "video_id": combo_id,
            "status": "ready",
            "message": "Video preparation already completed"
        }
    
    # バックグラウンドでFaceFusion処理
    request_id = str(uuid.uuid4())
    background_tasks.add_task(
        process_face_fusion,
        video_file,
        face_file
    )
    
    return {
        "request_id": request_id,
        "video_id": combo_id,
        "status": "processing",
        "message": "Video preparation started"
    }

# 静的ファイル提供（開発環境用 - 本番では別途Nginxなどを使用）
@app.get("/data/{folder}/{filename}")
async def get_data_file(folder: str, filename: str):
    if folder not in ["source", "output"]:
        raise HTTPException(status_code=404, detail="Folder not found")
    
    file_path = Path(f"/app/data/{folder}/{filename}")
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 