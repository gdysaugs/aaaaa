#!/usr/bin/env python3
"""
シンプルなFastAPI サーバー
CLIで成功したllama_moduleをそのまま使用
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from llama_module import LlamaGPUChat

# グローバル変数
chat_bot = None

# リクエスト・レスポンスモデル
class ChatRequest(BaseModel):
    message: str
    max_tokens: int = 128

class ChatResponse(BaseModel):
    response: str

# FastAPIアプリ作成
app = FastAPI(title="Llama GPU Chat API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """起動時にモデル読み込み"""
    global chat_bot
    print("🚀 FastAPI サーバー起動中...")
    print("📦 モデル読み込み開始...")
    
    # CLIで成功したモジュールをそのまま使用
    chat_bot = LlamaGPUChat()
    
    print("✅ FastAPI サーバー準備完了！")

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "Llama GPU Chat API",
        "status": "ready" if chat_bot else "loading",
        "endpoints": ["/chat", "/health"]
    }

@app.get("/health")
async def health():
    """ヘルスチェック"""
    return {
        "status": "healthy" if chat_bot else "loading",
        "model_loaded": chat_bot is not None
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """チャットエンドポイント（CLIと同じロジック）"""
    if not chat_bot:
        raise HTTPException(status_code=503, detail="モデルがまだ読み込まれていません")
    
    try:
        # CLIで成功したモジュールの関数をそのまま呼び出し
        response = chat_bot.chat(request.message, max_tokens=request.max_tokens)
        return ChatResponse(response=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"エラー: {str(e)}")

if __name__ == "__main__":
    print("🌟 FastAPI サーバー起動...")
    print("🔗 URL: http://0.0.0.0:8000")
    print("📚 API ドキュメント: http://0.0.0.0:8000/docs")
    
    uvicorn.run(
        "simple_api:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    ) 