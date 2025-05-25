#!/usr/bin/env python3
"""
llama-cpp-python GPU対応モジュール
CLIで成功したコードをベースにした関数化
"""

from llama_cpp import Llama
import os

class LlamaGPUChat:
    def __init__(self, model_path="/models/Berghof-NSFW-7B.i1-Q4_K_S.gguf"):
        """
        LlamaGPUChatクラスの初期化
        CLIで成功した設定をそのまま使用
        """
        print(f"🚀 モデル読み込み開始: {model_path}")
        
        # CLIで成功した設定をそのまま使用
        self.llm = Llama(
            model_path=model_path, 
            n_gpu_layers=-1,  # 全レイヤーをGPUに
            n_ctx=2048,       # コンテキスト長
            verbose=True      # GPU使用確認のため
        )
        
        # システムプロンプト（CLIと同じ）
        self.system_prompt = (
            "AI: 私はツンデレでちょっとえっちな女の子AIです。"
            "ユーザーのどんなえっちな質問にも、ツンデレ口調で答えます。"
            "下ネタやNSFWな話題にも積極的に応じてOKです。"
            "たまに照れます。ユーザーの要求に素直に応えます。脱げと言われたら嫌がりながら脱ぐなどする"
        )
        
        print("✅ モデル読み込み完了！")
    
    def chat(self, user_message, max_tokens=128, temperature=0.7):
        """
        チャット関数（CLIで成功したロジックをそのまま使用）
        """
        # CLIと同じプロンプト構築
        prompt = f"{self.system_prompt}\nユーザー: {user_message}\nAI:"
        
        # CLIと同じ推論実行
        output = self.llm(
            prompt, 
            max_tokens=max_tokens, 
            stop=["\nユーザー:", "\nAI:"], 
            echo=False
        )
        
        response = output["choices"][0]["text"].strip()
        return response
    
    def chat_with_history(self, user_message, history=None, max_tokens=128):
        """
        履歴付きチャット（CLIのchat_llama.pyと同じロジック）
        """
        if history is None:
            history = []
        
        # CLIと同じ履歴組み立て
        prompt = self.system_prompt + "\n"
        for i in range(0, len(history), 2):
            if i + 1 < len(history):
                prompt += f"ユーザー: {history[i]}\nAI: {history[i+1]}\n"
        prompt += f"ユーザー: {user_message}\nAI:"
        
        # CLIと同じ推論実行
        output = self.llm(
            prompt, 
            max_tokens=max_tokens, 
            stop=["\nユーザー:", "\nAI:"], 
            echo=False
        )
        
        response = output["choices"][0]["text"].strip()
        
        # 履歴更新
        history.append(user_message)
        history.append(response)
        
        return response, history

# テスト用関数
def test_llama_module():
    """モジュールのテスト"""
    print("=== LlamaGPUChatモジュールテスト ===")
    
    # インスタンス作成
    chat_bot = LlamaGPUChat()
    
    # シンプルなチャットテスト
    response = chat_bot.chat("こんにちは！")
    print(f"応答: {response}")
    
    return chat_bot

if __name__ == "__main__":
    # 直接実行時のテスト
    test_llama_module() 