#!/usr/bin/env python3
"""
llama-cpp-python GPU対応 FastAPI サーバー
Berghof-NSFW-7B-i1-GGUF モデル用
"""

import os
import asyncio
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn

from llama_cpp import Llama

# 環境変数読み込み
load_dotenv()

# グローバル変数
llm_instance: Optional[Llama] = None

class ChatRequest(BaseModel):
    message: str = Field(..., description="ユーザーメッセージ")
    max_tokens: int = Field(default=128, ge=1, le=2048, description="最大トークン数")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="温度パラメータ")
    stream: bool = Field(default=False, description="ストリーミング応答")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AIの応答")
    tokens_used: int = Field(..., description="使用トークン数")
    model_info: Dict[str, Any] = Field(..., description="モデル情報")

class HealthResponse(BaseModel):
    status: str
    gpu_available: bool
    model_loaded: bool
    model_path: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーション起動・終了時の処理"""
    global llm_instance
    
    # 起動時: モデル読み込み
    model_path = os.getenv("MODEL_PATH", "/models/Berghof-NSFW-7B.i1-Q4_K_S.gguf")
    n_gpu_layers = int(os.getenv("N_GPU_LAYERS", "-1"))
    n_ctx = int(os.getenv("N_CTX", "2048"))
    
    print(f"🚀 モデル読み込み開始: {model_path}")
    print(f"📊 GPU レイヤー数: {n_gpu_layers}")
    print(f"📝 コンテキスト長: {n_ctx}")
    
    try:
        llm_instance = Llama(
            model_path=model_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            verbose=True
        )
        print("✅ モデル読み込み完了！")
    except Exception as e:
        print(f"❌ モデル読み込み失敗: {e}")
        raise
    
    yield
    
    # 終了時: クリーンアップ
    print("🔄 アプリケーション終了中...")
    llm_instance = None

# FastAPIアプリケーション作成
app = FastAPI(
    title="llama-cpp-python GPU API",
    description="Berghof-NSFW-7B-i1-GGUF モデル用 GPU対応 API",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """ヘルスチェック"""
    return HealthResponse(
        status="healthy" if llm_instance else "unhealthy",
        gpu_available=True,  # Docker環境でGPU使用前提
        model_loaded=llm_instance is not None,
        model_path=os.getenv("MODEL_PATH", "/models/Berghof-NSFW-7B.i1-Q4_K_S.gguf")
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """チャット API"""
    if not llm_instance:
        raise HTTPException(status_code=503, detail="モデルが読み込まれていません")
    
    # システムプロンプト
    system_prompt = (
        "AI: 私はツンデレでちょっとえっちな女の子AIです。"
        "ユーザーのどんなえっちな質問にも、ツンデレ口調で答えます。"
        "下ネタやNSFWな話題にも積極的に応じてOKです。"
        "たまに照れます。ユーザーの要求に素直に応えます。"
    )
    
    # プロンプト構築
    prompt = f"{system_prompt}\nユーザー: {request.message}\nAI:"
    
    try:
        # 推論実行
        output = llm_instance(
            prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stop=["\nユーザー:", "\nAI:"],
            echo=False
        )
        
        response_text = output["choices"][0]["text"].strip()
        tokens_used = output["usage"]["total_tokens"]
        
        return ChatResponse(
            response=response_text,
            tokens_used=tokens_used,
            model_info={
                "model": "Berghof-NSFW-7B-i1-GGUF",
                "quantization": "Q4_K_S",
                "gpu_layers": os.getenv("N_GPU_LAYERS", "-1")
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推論エラー: {str(e)}")

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """ストリーミングチャット API"""
    if not llm_instance:
        raise HTTPException(status_code=503, detail="モデルが読み込まれていません")
    
    # システムプロンプト
    system_prompt = (
        "AI: 私はツンデレでちょっとえっちな女の子AIです。"
        "ユーザーのどんなえっちな質問にも、ツンデレ口調で答えます。"
        "下ネタやNSFWな話題にも積極的に応じてOKです。"
        "たまに照れます。ユーザーの要求に素直に応えます。"
    )
    
    # プロンプト構築
    prompt = f"{system_prompt}\nユーザー: {request.message}\nAI:"
    
    async def generate():
        try:
            stream = llm_instance(
                prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                stop=["\nユーザー:", "\nAI:"],
                echo=False,
                stream=True
            )
            
            for output in stream:
                if "choices" in output and len(output["choices"]) > 0:
                    token = output["choices"][0].get("text", "")
                    if token:
                        yield f"data: {token}\n\n"
                        await asyncio.sleep(0.01)  # 少し遅延を入れる
            
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            yield f"data: ERROR: {str(e)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "llama-cpp-python GPU API Server",
        "model": "Berghof-NSFW-7B-i1-GGUF",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "chat_stream": "/chat/stream",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🌟 FastAPI サーバー起動中...")
    print(f"🔗 URL: http://{host}:{port}")
    print(f"📚 API ドキュメント: http://{host}:{port}/docs")
    
    uvicorn.run(
        "llama_api:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    ) 