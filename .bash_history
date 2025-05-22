cd /home/adama && git clone https://github.com/gdysaugs/aaaaa.git
cd aaaaa && ls -la
rm -rf /home/adama/aaaaa
cd /home/adama && git clone https://github.com/gdysaugs/aaaaa.git
cd aaaaa && ls -la
cd /home/adama/aaaaa/ai-video-chat && ls -la
cat /home/adama/aaaaa/ai-video-chat/WSL_reinstall_recovery.md
sudo apt update && sudo apt upgrade -y && sudo apt install -y git curl ca-certificates lsb-release gnupg
cd /home/adama/aaaaa/ai-video-chat && DOCKER_BUILDKIT=1 docker-compose up --build --remove-orphans
curl -fsSL https://get.docker.com | sh
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) && curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add - && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list && sudo apt update && sudo apt install -y nvidia-docker2 && sudo systemctl restart docker
sudo apt install -y git-lfs && git lfs install
cd /home/adama/aaaaa/ai-video-chat && cp .env.example .env
DOCKER_BUILDKIT=1 docker-compose up --build --remove-orphans
sudo apt install -y docker-compose
cd /home/adama/aaaaa/ai-video-chat && DOCKER_BUILDKIT=1 docker-compose up --build --remove-orphans
sudo usermod -aG docker $USER && newgrp docker
cd aaaaa/llama-cpp-cli-test && mkdir -p models
cd aaaaa/llama-cpp-cli-test && wget -c https://huggingface.co/mradermacher/Berghof-NSFW-7B-i1-GGUF/resolve/main/Berghof-NSFW-7B-i1-GGUF.Q4_K_M.gguf -P models/ --no-check-certificate
pwd
wget -c https://huggingface.co/mradermacher/Berghof-NSFW-7B-i1-GGUF/resolve/main/Berghof-NSFW-7B-i1-GGUF.Q4_K_M.gguf -P models/ --no-check-certificate
find ~/ -name "*.gguf" -type f 2>/dev/null || echo "No GGUF files found"
cd ~/aaaaa/llama-cpp-cli-test && docker ps -a | grep llama
cd ~/aaaaa/llama-cpp-cli-test && docker images | grep llama-cpp-cli-test
cd ~/aaaaa/llama-cpp-cli-test && DOCKER_BUILDKIT=1 docker build -t llama-cpp-cli-test .
mkdir -p ~/aaaaa/wav2lip-test/{data/input,data/output,models}
cd ~/aaaaa/wav2lip-test && pip install gdown && gdown --id 1PwUHOz_bxJZB0AnpYjVJcMftHO8FiLwg -O models/wav2lip.pth
sudo apt update && sudo apt install -y python3-pip
cd ~/aaaaa/wav2lip-test && python3 -m pip install gdown && gdown --id 1PwUHOz_bxJZB0AnpYjVJcMftHO8FiLwg -O models/wav2lip.pth
cd ~/aaaaa/wav2lip-test && export PATH=$PATH:$HOME/.local/bin && python3 -m gdown --id 1PwUHOz_bxJZB0AnpYjVJcMftHO8FiLwg -O models/wav2lip.pth
cd ~/aaaaa/wav2lip-test/data/input && wget https://file-examples.com/storage/fe7bb0dffe141b8e5a826bd/2017/04/file_example_MP4_480_1_5MG.mp4 -O sample.mp4 && wget https://file-examples.com/storage/fe7bb0dffe141b8e5a826bd/2017/11/file_example_WAV_1MG.wav -O sample.wav
cd ~/aaaaa/wav2lip-test/data/input && wget https://www.pexels.com/download/video/856973/ -O sample.mp4 && wget https://assets.mixkit.co/active_storage/sfx/989/989.wav -O sample.wav
cd ~/aaaaa/wav2lip-test/docker && DOCKER_BUILDKIT=1 sudo docker build -t wav2lip-gpu .
cp ~/aaaaa/wav2lip-test/requirements.txt ~/aaaaa/wav2lip-test/docker/ && cd ~/aaaaa/wav2lip-test/docker && DOCKER_BUILDKIT=1 sudo docker build -t wav2lip-gpu .
sudo cat /etc/docker/daemon.json
sudo bash -c 'echo {\"runtimes\": {\"nvidia\": {\"path\": \"nvidia-container-runtime\", \"runtimeArgs\": []}}} > /etc/docker/daemon.json'
which nvidia-container-runtime
sudo systemctl restart docker
cd /home/adama/aaaaa/facefusion-test/docker && cat docker-compose.yml
cd /home/adama/aaaaa/facefusion-test && mkdir -p data/source && mkdir -p data/target && mkdir -p data/output && touch data/source/dummy.jpg && touch data/target/dummy.mp4
cd /home/adama/aaaaa/facefusion-test/docker && DOCKER_BUILDKIT=1 docker-compose up --build -d
docker exec facefusion-app nvidia-smi
cd /home/adama/aaaaa/facefusion-test && rm -f data/source/dummy.jpg data/target/dummy.mp4 && curl -s -o data/source/sample.jpg https://raw.githubusercontent.com/facefusion/facefusion/master/.github/assets/demo-source-0.jpg && curl -s -o data/target/sample.mp4 https://raw.githubusercontent.com/facefusion/facefusion/master/.github/assets/demo-target-0.mp4
cd /home/adama/aaaaa/facefusion-test/scripts && ./cli-test.sh
ls -la /home/adama/aaaaa/facefusion-test/scripts/cli-test.sh
sed -i 's/facefusion/facefusion-app/g' /home/adama/aaaaa/facefusion-test/scripts/cli-test.sh
sed -i 's|/app/facefusion-app/data|/app/facefusion/.assets/test|g' /home/adama/aaaaa/facefusion-test/scripts/cli-test.sh
cat /home/adama/aaaaa/facefusion-test/scripts/cli-test.sh
sed -i 's/facefusion-app.py/facefusion.py/g' /home/adama/aaaaa/facefusion-test/scripts/cli-test.sh
ls -la /home/adama/aaaaa/facefusion-test/data/source/ /home/adama/aaaaa/facefusion-test/data/target/
wget -O /home/adama/aaaaa/facefusion-test/data/source/sample.jpg https://raw.githubusercontent.com/facefusion/facefusion/master/.github/assets/demo-source-0.jpg && wget -O /home/adama/aaaaa/facefusion-test/data/target/sample.mp4 https://raw.githubusercontent.com/facefusion/facefusion/master/.github/assets/demo-target-0.mp4
cp /home/adama/aaaaa/facefusion-test/data/target/'画面録画 2025-05-16 222902.mp4' /home/adama/aaaaa/facefusion-test/data/target/test.mp4
cd /home/adama/aaaaa/facefusion-test/scripts && ./cli-test.sh
docker ps
rm -f /home/adama/aaaaa/facefusion-test/scripts/cli-test.sh
docker exec facefusion-app python facefusion.py --help
docker exec facefusion-app ls -la /app/facefusion
docker exec facefusion-app sh -c "which python3"
docker exec facefusion-app python3 /app/facefusion/facefusion.py --help
docker exec facefusion-app python3 /app/facefusion/facefusion.py headless-run --help
docker exec facefusion-app python3 /app/facefusion/facefusion.py headless-run --source "/app/facefusion/.assets/test/source/kanna-hashimoto.jpg" --target "/app/facefusion/.assets/test/target/test.mp4" --output "/app/facefusion/.assets/test/output/output_test.mp4" --face-swapper-model "inswapper_128" --processors face_swapper
cd ~/aaaaa/llama-cpp-cli-test && docker run --gpus all --rm -it -v $(pwd)/models:/models llama-cpp-cli-test python3 -m llama_cpp.cli --model /models/Berghof-NSFW-7B.i1-Q4_K_S.gguf --prompt "こんにちは"
cd ~/aaaaa/llama-cpp-cli-test && docker run --gpus all --rm -it llama-cpp-cli-test python3 -c "help('modules')"
cd ~/aaaaa/llama-cpp-cli-test && docker run --gpus all --rm -it llama-cpp-cli-test python3 -c "import llama_cpp; print(dir(llama_cpp))"
cd ~/aaaaa/llama-cpp-cli-test && docker run --gpus all --rm -it -v $(pwd)/models:/models llama-cpp-cli-test python3 chat_llama.py
cd ~/aaaaa/llama-cpp-cli-test && docker run --gpus all --rm -it -v $(pwd)/models:/models -v $(pwd)/chat_llama.py:/workspace/chat_llama.py llama-cpp-cli-test python3 /workspace/chat_llama.py
cd ~/aaaaa/wav2lip-test && mkdir -p models/face_detection/detection/sfd && wget -O models/face_detection/detection/sfd/s3fd.pth https://huggingface.co/akhaliq/s3fd/resolve/main/s3fd.pth
cd ~/aaaaa/wav2lip-test && mkdir -p temp && cd temp && git clone https://github.com/Rudrabha/Wav2Lip.git && cd Wav2Lip && mkdir -p face_detection/detection/sfd && wget -O face_detection/detection/sfd/s3fd.pth https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth
mkdir -p ~/aaaaa/wav2lip-test/models/face_detection/detection/sfd && cp ~/aaaaa/wav2lip-test/temp/Wav2Lip/face_detection/detection/sfd/s3fd.pth ~/aaaaa/wav2lip-test/models/face_detection/detection/sfd/
sudo docker images | grep wav2lip-gpu
sudo docker ps -a
cd ~/aaaaa/wav2lip-test/docker && DOCKER_BUILDKIT=1 sudo docker build -t wav2lip-gpu .
nvidia-smi
cd ~/aaaaa/llama-cpp-cli-test && docker run --gpus all --rm -it -v $(pwd)/models:/models -v $(pwd)/chat_llama.py:/workspace/chat_llama.py llama-cpp-cli-test python3 /workspace/chat_llama.py
cd ~/aaaaa/llama-cpp-cli-test && DOCKER_BUILDKIT=1 docker build -t llama-cpp-cli-test .
docker exec facefusion-app python3 /app/facefusion/facefusion.py headless-run -s "/app/facefusion/.assets/test/source/kanna-hashimoto.jpg" -t "/app/facefusion/.assets/test/target/test.mp4" -o "/app/facefusion/.assets/test/output/output_test.mp4" --face-swapper-model "inswapper_128" --processors face_swapper
cd /home/adama/aaaaa/facefusion-test && ls -la
cat README.md
cd docker && ls -la
cd ../scripts && ls -la
cat cli-test.sh
cd ../data && ls -la
mkdir -p target output
cd ../docker && DOCKER_BUILDKIT=1 docker-compose up --build -d
cd ~/aaaaa/wav2lip-test && python3 -c "import gdown; gdown.download('https://drive.google.com/uc?id=1UJUKsoI3CcYuVnAvVIOVK1Z9JziD2u5a', 'models/wav2lip.pth', quiet=False)"
sudo docker images | grep wav2lip-gpu
sudo docker run --gpus all -it --rm -v ~/aaaaa/wav2lip-test/data:/workspace/data -v ~/aaaaa/wav2lip-test/models:/workspace/models -v ~/aaaaa/wav2lip-test/scripts:/workspace/scripts wav2lip-gpu /bin/bash -c "cd /workspace/scripts && bash run_wav2lip.sh"
ls -la ~/aaaaa/wav2lip-test/models/
sudo docker run --gpus all -it --rm -v ~/aaaaa/wav2lip-test/data:/workspace/data -v ~/aaaaa/wav2lip-test/models:/workspace/models -v ~/aaaaa/wav2lip-test/scripts:/workspace/scripts wav2lip-gpu /bin/bash -c "cd /workspace/scripts && bash run_wav2lip.sh"
cd ~/aaaaa/wav2lip-test/data/input && wget -O sample2.mp4 https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4
sudo docker run --gpus all -it --rm -v ~/aaaaa/wav2lip-test/data:/workspace/data -v ~/aaaaa/wav2lip-test/models:/workspace/models -v ~/aaaaa/wav2lip-test/scripts:/workspace/scripts wav2lip-gpu /bin/bash -c "cd /workspace/scripts && bash run_wav2lip.sh"
ls -la /home/adama/aaaaa/facefusion-test/data/output/
nvidia-smi
docker exec facefusion-app nvidia-smi
cd /home/adama/aaaaa/facefusion-test/scripts && chmod +x cli-test.sh
mkdir -p aaaaa/samples
wget https://wsignal.sakura.ne.jp/onsei2007/wav_data51/a_1.wav -O aaaaa/samples/voice.wav
mkdir -p aaaaa/output
cd aaaaa && bash run_voice_clone.sh "こんにちは、ボイスクローンのテストです。" ja
ls -la aaaaa/samples/
ls -la samples/
cp samples/ohayougozaimasu_10.wav samples/voice.wav
bash run_voice_clone.sh "こんにちは、ボイスクローンのテストです。" ja
file samples/voice.wav
pwd
file aaaaa/samples/voice.wav
ls -la aaaaa/output/
cd aaaaa && bash run_voice_clone.sh "こんにちは、ボイスクローンのテストです。改善版で聞き取りやすくなりました。" ja 0.01 1.1
bash run_voice_clone.sh "こんにちは、ボイスクローンのテストです。改善版で聞き取りやすくなりました。" ja 0.01 1.1
bash run_voice_clone.sh "こんにちは、ボイスクローンのテストです。改善版で聞き取りやすくなりました。" ja
bash run_voice_clone.sh "Hello, this is a voice clone test. It should sound much better now." en
ls -la aaaaa/output/
ls -la output/
cd aaaaa && bash run_voice_clone.sh "こんにちは、ボイスクローンのテストです。日本語での音声合成が可能になりました。" ja
bash run_voice_clone.sh "こんにちは、ボイスクローンのテストです。日本語での音声合成が可能になりました。" ja
ls -la aaaaa/output/
cd aaaaa && bash run_voice_clone.sh "Hello, this is a voice clone test with xTTS v2 model." en
cd aaaaa && bash run_voice_clone.sh "こんにちは、ボイスクローンのテストです。日本語での音声合成が可能になりました。" ja
cd aaaaa && bash run_voice_clone.sh "Hello, this is a voice clone test. It should work well with the your_tts model." en
docker ps
docker images | grep tts-voice-clone
ps aux | grep voice_clone
ls -la /home/adama/aaaaa/output/
sleep 10 && ls -la /home/adama/aaaaa/output/
cd /home/adama/aaaaa && DOCKER_BUILDKIT=1 docker build -t tts-voice-clone .
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、ボイスクローンのテストです" 0.01 1.2
cd /home/adama/aaaaa && docker run --rm tts-voice-clone --text "テスト" --speaker_wav /app/samples/voice.wav --output /app/output/test.wav --model "tts_models/multilingual/multi-dataset/your_tts"
cd /home/adama/aaaaa && DOCKER_BUILDKIT=1 docker build -t tts-voice-clone .
chmod +x aaaaa/run_voice_clone.sh
cd /home/adama/aaaaa && DOCKER_BUILDKIT=1 docker build -t tts-voice-clone . --no-cache
cat /home/adama/.local/lib/python3.10/site-packages/TTS/utils/io.py | grep -A 10 "def load_fsspec"
docker run -it --rm tts-voice-clone bash -c "cat /usr/local/lib/python3.10/dist-packages/TTS/utils/io.py | grep -A 20 'def load_fsspec'"
docker run -it --rm --entrypoint bash tts-voice-clone -c "cat /usr/local/lib/python3.10/dist-packages/TTS/utils/io.py | grep -A 20 'def load_fsspec'"
docker run -it --rm --entrypoint bash tts-voice-clone -c "cat /usr/local/lib/python3.10/dist-packages/TTS/utils/io.py | grep -A 50 'def load_fsspec'"
docker run -it --rm --entrypoint bash tts-voice-clone -c "python3 -c 'from TTS.config.shared_configs import BaseAudioConfig, BaseDatasetConfig, BaseTrainingConfig, GSTConfig; print(dir(BaseDatasetConfig))'"
docker run -it --rm --entrypoint bash tts-voice-clone -c "python3 -c 'from TTS.config.shared_configs import BaseAudioConfig, BaseDatasetConfig, BaseTrainingConfig; print(dir(BaseDatasetConfig))'"
docker run -it --rm --entrypoint bash tts-voice-clone -c "python3 -c 'import inspect; from TTS.config.shared_configs import BaseDatasetConfig; print(inspect.getmodule(BaseDatasetConfig).__name__)'"
cd /home/adama/aaaaa && docker build -t tts-voice-clone .
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはXTTS v2モデルによるボイスクローンのテストです" 0.01 1.2
cd /home/adama/aaaaa && docker build -t tts-voice-clone .
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはXTTS v2モデルによるボイスクローンのテストです" 0.1 1.2
mkdir -p ~/valle-test
cd ~/valle-test && ls -la
ls -la ~/aaaaa/samples/
cd ~/valle-test && cp ~/aaaaa/samples/ohayougozaimasu_10.wav ./
cd ~/valle-test && mkdir -p output
cd ~/valle-test && chmod +x test_valle.sh
cd ~/valle-test && ls -la
cd ~/valle-test && touch Dockerfile docker-compose.yml test_valle.sh
cd ~/valle-test && chmod +x test_valle.sh
cd ~/valle-test && ls -la
cd ~/valle-test && cat Dockerfile | wc -l
cd ~/valle-test && vi docker-compose.yml
R1Rq
cd ~/valle-test && nano docker-compose.yml
cd ~ && rm -rf valle-test && mkdir -p valle-test/output && cp ~/aaaaa/samples/ohayougozaimasu_10.wav ~/valle-test/
echo 'FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 AS builder' > ~/valle-test/Dockerfile
cd ~ && cp valle-test/Dockerfile valle-test/Dockerfile2 && ls -la valle-test
cd ~/valle-test && ls -la
cd ~ && git clone https://github.com/lifeiteng/vall-e.git
cd ~/vall-e && ls -la docker
cd ~/vall-e && cat docker/Dockerfile
cd ~/valle-test && cp -r ~/vall-e/docker .
cd ~/valle-test && ls -la docker
cd ~/valle-test && touch docker-compose.yml
sudo docker images | grep wav2lip-gpu
ps aux | grep docker
cd ~/aaaaa/wav2lip-test/docker && sudo docker build -t wav2lip-gpu .
pwd
cd aaaaa && bash run_voice_clone.sh "こんにちは、ボイスクローンのテストです。日本語での音声合成が可能になりました。" ja
mkdir -p /home/adama/aaaaa/vall-e-test/samples && mkdir -p /home/adama/aaaaa/vall-e-test/output
cp /home/adama/aaaaa/samples/ohayougozaimasu_10.wav /home/adama/aaaaa/vall-e-test/samples/
cd aaaaa && bash run_voice_clone.sh "Hello, this is a test of the xTTS v2 model. It should work well with English too." en
./run_voice_clone.sh "こんにちは、ボイスクローンのテストです" 0.01 1.2
cd /home/adama/aaaaa && docker build -t tts-voice-clone .
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはXTTS v2モデルによるボイスクローンのテストです。声質と発音の自然さを向上させています。" 0.05 1.0
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはモデルによるボイスクローンのテストです。声質と発音の自然さを向上させています。" 0.01 2.0
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはモデルによるボイスクローンのテストです。声質と発音の自然さを向上させています。" 0.02 1.2
cd aaaaa && ls -la
cd aaaaa && ls -la samples/
ls -la samples/
chmod +x run_voice_clone.sh
./run_voice_clone.sh --help
cd aaaaa && ./run_voice_clone.sh "こんにちは、これはテストです" 0.01 1.2
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはテストです" 0.01 1.2
cd /home/adama/aaaaa && DOCKER_BUILDKIT=1 docker build -t tts-voice-clone .
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはXTTS v2モデルによるボイスクローンのテストです" 0.01 1.2
./run_voice_clone.sh "こんにちは、これはXTTS v2モデルによるボイスクローンのテストです" 0.01 1.2
cd /home/adama/aaaaa && DOCKER_BUILDKIT=1 docker build -t tts-voice-clone 
cd /home/adama/aaaaa && DOCKER_BUILDKIT=1 docker build -t tts-voice-clone .
cd /home/adama/aaaaa && docker build -t tts-voice-clone .
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはXTTS v2モデルによるボイスクローンのテストです" 0.01 1.2
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはXTTS v2モデルによるボイスクローンのテストです" 0.03 1.2
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはXTTS v2モデルによるボイスクローンのテストです" 0.2 1.2
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはXTTS v2モデルによるボイスクローンのテストです" 0.01 3.2
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはモデルによるボイスクローンのテストです" 0.03 3.2
cd /home/adama/aaaaa && DOCKER_BUILDKIT=1 docker build -t tts-voice-clone .
cd /home/adama/aaaaa && ./run_voice_clone.sh "こんにちは、これはXTTS v2モデルによるボイスクローンのテストです" 0.01 1.2
docker exec -it vall-e-container python3 bin/infer.py --output-dir /app/output --checkpoint=./checkpoints/vall-e.pt --text-prompts "おはようございます" --audio-prompts /app/samples/ohayougozaimasu_10.wav --text "こんにちは、世界"
cd vall-e-test && docker exec -it vall-e-container ls -la /app
mkdir -p /home/adama/VALL-E-X-Workspace && mkdir -p /home/adama/VALL-E-X-Workspace/custom_prompts && mkdir -p /home/adama/VALL-E-X-Workspace/output
cp /home/adama/aaaaa/samples/ohayougozaimasu_10.wav /home/adama/VALL-E-X-Workspace/custom_prompts/ohayougozaimasu_10.wav
sudo apt-get update && sudo apt-get install -y git git-lfs ca-certificates
cd /home/adama/VALL-E-X-Workspace && git lfs install
cd /home/adama/VALL-E-X-Workspace && git clone https://github.com/Plachtaa/VALL-E-X.git .
cd /home/adama/VALL-E-X-Workspace && docker buildx build --tag vall-e-x-app .
ls -la /home/adama/VALL-E-X-Workspace
cd /home/adama/VALL-E-X-Workspace && docker buildx build --tag vall-e-x-app --load .
cd /home/adama/VALL-E-X-Workspace && ls -la && file Dockerfile
touch /home/adama/VALL-E-X-Workspace/Dockerfile
nano /home/adama/VALL-E-X-Workspace/Dockerfile
docker exec -it vall-e-container bash
cd /home/adama/VALL-E-X-Workspace && echo '# Stage 1: Build stage with Git LFS' > Dockerfile
cd /home/adama/VALL-E-X-Workspace && echo 'FROM ubuntu:22.04 AS builder' >> Dockerfile
curl -o /home/adama/VALL-E-X-Workspace/Dockerfile.temp https://raw.githubusercontent.com/Plachtaa/VALL-E-X/master/docker/Dockerfile
cd /home/adama/VALL-E-X-Workspace && docker buildx build --tag vall-e-x-app --load .
cat /home/adama/VALL-E-X-Workspace/Dockerfile
rm -f /home/adama/VALL-E-X-Workspace/Dockerfile && touch /home/adama/VALL-E-X-Workspace/Dockerfile
cd /home/adama/VALL-E-X-Workspace && nano Dockerfile
cd /home/adama/VALL-E-X-Workspace && docker buildx build --tag vall-e-x-app --load .
docker buildx build --builder custom-builder -t vall-e-app --load .
docker-compose up -d
cd vall-e-test && docker-compose up -d
cd /home/adama/VALL-E-X-Workspace && docker buildx build --tag vall-e-x-app .
nvidia-smi
cd aaaaa && docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
apt list --installed | grep -E 'nvidia-container-toolkit|nvidia-docker2'
cat /etc/docker/daemon.json
sudo apt-get update && sudo apt-get install -y jq && sudo jq '. + {"default-runtime": "nvidia"}' /etc/docker/daemon.json > /tmp/daemon.json && sudo mv /tmp/daemon.json /etc/docker/daemon.json && sudo systemctl restart docker
cd aaaaa && docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
docker compose run --rm gpt-sovits python GPT_SoVITS/inference_cli.py --help
cd gpt-sovits-v3-cli-test && ls -la
cd gpt-sovits-v3-cli-test && docker compose run --rm gpt-sovits bash -c "export PYTHONPATH=/app:\$PYTHONPATH && export GPT_PATH=/app/GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2v4.ckpt && export SOVITS_PATH=/app/GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2v4.ckpt && export BERT_PATH=/app/GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large && export SSL_MODEL_PATH=/app/GPT_SoVITS/pretrained_models/chinese-hubert-base && python GPT_SoVITS/inference_cli.py --help"
cd gpt-sovits-v3-cli-test && docker compose run --rm gpt-sovits-v3 bash -c "export PYTHONPATH=/app:\$PYTHONPATH && export GPT_PATH=/app/GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2v4.ckpt && export SOVITS_PATH=/app/GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2v4.ckpt && export BERT_PATH=/app/GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large && export SSL_MODEL_PATH=/app/GPT_SoVITS/pretrained_models/chinese-hubert-base && python GPT_SoVITS/inference_cli.py --help"
docker ps -a
git config --global user.email "adamadams567890@gmail.com"
git config --global user.name "gdysauges"
. "\home\adama\.cursor-server\bin\96e5b01ca25f8fbd4c4c10bc69b15f6228c80770\out\vs\workbench\contrib\terminal\common\scripts\shellIntegration-bash.sh"
git status && git remote -v
git add .
git commit -m "プロジェクト構成全体を更新"
git push origin main --force
