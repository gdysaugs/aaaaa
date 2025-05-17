#!/bin/bash
set -e

MODEL_PATH=${MODEL_PATH:-/models/Berghof-NSFW-7B-i1-GGUF.Q4_K_M.gguf}
PROMPT=${1:-"こんにちは。これはテストです。"}

python3 -m llama_cpp.cli --model "$MODEL_PATH" --prompt "$PROMPT" 