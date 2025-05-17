# llama-cpp-python CLIテスト環境（Berghof-NSFW-7B-i1-GGUFモデル）

## 構成
- CUDA 11.8 + Python 3.10 + llama-cpp-python（GPUビルド）
- モデル: [Berghof-NSFW-7B-i1-GGUF](https://huggingface.co/mradermacher/Berghof-NSFW-7B-i1-GGUF)
- Dockerマルチステージビルド
- CLIテスト用スクリプト同梱

## 必要条件
- WSL2 + Ubuntu + NVIDIAドライバ + Docker + RTX3050以上
- ホスト側でnvidia-docker2セットアップ済み

## 使い方
1. モデルファイル（.gguf）を`models/`に配置（または自動DL）
2. Dockerビルド
3. CLIテスト実行

## 依存関係
- nvidia/cuda:11.8.0-devel-ubuntu22.04
- python3, pip, cmake, build-essential, git, git-lfs, ca-certificates
- llama-cpp-python[server]（CMAKE_ARGS="-DGGML_CUDA=on"指定でビルド）

## 主要コマンド
```bash
# ビルド
DOCKER_BUILDKIT=1 docker build -t llama-cpp-cli-test .

# CLIテスト
# モデルファイル名は適宜変更
# 例: Berghof-NSFW-7B-i1-GGUF.Q4_K_M.gguf

docker run --gpus all --rm -it -v $(pwd)/models:/models llama-cpp-cli-test \
  python3 -m llama_cpp.cli --model /models/Berghof-NSFW-7B-i1-GGUF.Q4_K_M.gguf --prompt "こんにちは"
```

## .env.example
```env
MODEL_PATH=/models/Berghof-NSFW-7B-i1-GGUF.Q4_K_M.gguf
``` 