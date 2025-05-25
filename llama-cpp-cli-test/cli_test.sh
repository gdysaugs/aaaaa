#!/bin/bash

echo "=== llama-cpp-python GPU CLI テスト ==="

# GPU確認
echo "1. GPU確認中..."
nvidia-smi

echo -e "\n2. llama-cpp-python GPU テスト開始..."

# モデルファイルの確認
MODEL_FILE="/models/Berghof-NSFW-7B.i1-Q4_K_S.gguf"
if [ ! -f "$MODEL_FILE" ]; then
    echo "エラー: モデルファイルが見つかりません: $MODEL_FILE"
    exit 1
fi

echo "モデルファイル確認: $MODEL_FILE"

# 簡単なテスト
echo -e "\n3. 簡単な推論テスト..."
python3 -c "
from llama_cpp import Llama
print('llama-cpp-python読み込み中...')
llm = Llama(model_path='$MODEL_FILE', n_gpu_layers=-1, n_ctx=512, verbose=True)
print('推論テスト実行中...')
output = llm('こんにちは、', max_tokens=50, stop=['\n'], echo=True)
print('結果:', output['choices'][0]['text'])
print('GPU使用確認: BLAS=1 が表示されていればGPU使用中')
"

echo -e "\n4. チャットモード開始..."
echo "チャットを開始します。'exit'で終了。"
python3 chat_llama.py