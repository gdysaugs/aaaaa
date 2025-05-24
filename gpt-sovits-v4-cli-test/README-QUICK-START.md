# GPT-SoVITS v4 CLIテスト クイックスタートガイド

## 🚀 基本起動コマンド

### 1. Dockerコンテナビルド
```bash
cd /home/adama/LLM/gpt-sovits-v4-cli-test
DOCKER_BUILDKIT=1 docker compose -f docker-compose.v2.6.yml build --no-cache
```

### 2. APIサーバー起動
```bash
cd /home/adama/LLM/gpt-sovits-v4-cli-test
docker compose -f docker-compose.v2.6.yml exec gpt-sovits-dev bash -c "
mkdir -p /tmp/numba_cache /tmp/matplotlib /tmp/torch_cache /tmp/pyopenjtalk_dict /tmp/nltk_data /tmp/g2pw_cache && \
chmod 777 /tmp/numba_cache /tmp/matplotlib /tmp/torch_cache /tmp/pyopenjtalk_dict /tmp/nltk_data /tmp/g2pw_cache && \
export NUMBA_CACHE_DIR=/tmp/numba_cache && \
export MPLCONFIGDIR=/tmp/matplotlib && \
export TORCH_HOME=/tmp/torch_cache && \
export PYOPENJTALK_DICT_DIR=/tmp/pyopenjtalk_dict && \
export NLTK_DATA=/tmp/nltk_data && \
export G2PW_CACHE_DIR=/tmp/g2pw_cache && \
/workspace/start_api.sh"
```

### 3. 簡単起動用エイリアス
```bash
# ~/.bashrcに追加推奨
alias gpt-sovits-start="cd /home/adama/LLM/gpt-sovits-v4-cli-test && docker compose -f docker-compose.v2.6.yml exec gpt-sovits-dev bash -c 'mkdir -p /tmp/numba_cache /tmp/matplotlib /tmp/torch_cache /tmp/pyopenjtalk_dict /tmp/nltk_data /tmp/g2pw_cache && chmod 777 /tmp/numba_cache /tmp/matplotlib /tmp/torch_cache /tmp/pyopenjtalk_dict /tmp/nltk_data /tmp/g2pw_cache && export NUMBA_CACHE_DIR=/tmp/numba_cache && export MPLCONFIGDIR=/tmp/matplotlib && export TORCH_HOME=/tmp/torch_cache && export PYOPENJTALK_DICT_DIR=/tmp/pyopenjtalk_dict && export NLTK_DATA=/tmp/nltk_data && export G2PW_CACHE_DIR=/tmp/g2pw_cache && /workspace/start_api.sh'"
```

## 📡 APIアクセス情報

- **APIサーバー**: http://localhost:9880
- **Swagger UI**: http://localhost:9880/docs
- **OpenAPI JSON**: http://localhost:9880/openapi.json

## 🎯 テスト用コマンド

### 基本テスト（ブラウザ）
```bash
# 日本語テスト
http://localhost:9880/tts?text=こんにちは世界&text_lang=ja&ref_audio_path=/workspace/reference/ohayougozaimasu_5sec.wav&prompt_text=おはようございます&prompt_lang=ja

# 英語テスト  
http://localhost:9880/tts?text=Hello+world&text_lang=en&ref_audio_path=/workspace/reference/ohayougozaimasu_5sec.wav&prompt_text=Test+audio&prompt_lang=en

# 中国語テスト
http://localhost:9880/tts?text=你好世界&text_lang=zh&ref_audio_path=/workspace/reference/ohayougozaimasu_5sec.wav&prompt_text=测试音频&prompt_lang=zh
```

### cURLテスト
```bash
# 日本語合成
curl -G "http://localhost:9880/tts" \
  --data-urlencode "text=こんにちは世界、これはGPT-SoVITS v4のテストです" \
  --data-urlencode "text_lang=ja" \
  --data-urlencode "ref_audio_path=/workspace/reference/ohayougozaimasu_5sec.wav" \
  --data-urlencode "prompt_text=おはようございます" \
  --data-urlencode "prompt_lang=ja" \
  --output test_output.wav

# 英語合成
curl -G "http://localhost:9880/tts" \
  --data-urlencode "text=Hello world, this is a GPT-SoVITS v4 test" \
  --data-urlencode "text_lang=en" \
  --data-urlencode "ref_audio_path=/workspace/reference/ohayougozaimasu_5sec.wav" \
  --data-urlencode "prompt_text=Good morning" \
  --data-urlencode "prompt_lang=en" \
  --output test_output_en.wav
```

## 📁 参考音声設定

### 現在利用可能な参考音声
- `/workspace/reference/ohayougozaimasu_5sec.wav` (3.22秒, 48kHz, 日本語最適化済み)
- `/workspace/reference/dummy_5sec.wav` (5秒ダミー音声)

### 新しい参考音声追加方法
```bash
# Windows音声をWSLにコピー
cp /mnt/c/Users/adama/Downloads/your_audio.wav .

# ffmpegで最適化（3-10秒、48kHzに調整）
docker compose -f docker-compose.v2.6.yml exec gpt-sovits-dev ffmpeg -i input.wav -ar 48000 -ac 1 -af "apad=whole_dur=5" output_5sec.wav

# コンテナ内に配置
docker compose -f docker-compose.v2.6.yml exec gpt-sovits-dev cp /workspace/output_5sec.wav /workspace/reference/
```

## 🔧 ロードされるモデル情報

```
device              : cuda
is_half             : True  
version             : v2
t2s_weights_path    : GPT_SoVITS/pretrained_models/s1v3.ckpt
vits_weights_path   : GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2Gv4.pth
bert_base_path      : GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large
cnhuhbert_base_path : GPT_SoVITS/pretrained_models/chinese-hubert-base
```

## 🎛️ APIパラメータ仕様

### 必須パラメータ
- `text`: 合成したいテキスト
- `text_lang`: テキストの言語 (ja/en/zh)
- `ref_audio_path`: 参考音声ファイルパス
- `prompt_text`: 参考音声のテキスト
- `prompt_lang`: 参考音声の言語

### オプションパラメータ
- `cut_punc`: 句読点で分割 (default: true)
- `top_k`: GPTサンプリングtop_k (default: 15)
- `top_p`: GPTサンプリングtop_p (default: 1.0)
- `temperature`: GPTサンプリング温度 (default: 1.0)
- `speed_factor`: 音声速度倍率 (default: 1.0)

## 🚨 トラブルシューティング

### よくあるエラーと対処法

1. **Permission denied: /.config**
   ```bash
   # 環境変数で解決済み
   export MPLCONFIGDIR=/tmp/matplotlib
   ```

2. **ModuleNotFoundError: No module named 'X'**
   ```bash
   # 依存関係再インストール
   docker compose -f docker-compose.v2.6.yml exec gpt-sovits-dev pip install ffmpeg-python pytorch_lightning x_transformers peft fast_langdetect
   ```

3. **参考音声エラー (400 Bad Request)**
   - 音声ファイルが3-10秒の範囲にあることを確認
   - 音声ファイルパスが正しいことを確認
   - サンプルレートが適切であることを確認 (推奨: 48kHz)

4. **CUDA out of memory**
   ```bash
   # 並列処理無効化
   # APIリクエスト時にparallel_infer=falseを追加
   ```

## 🎉 成功ログ例

```
Loading Text2Semantic weights from GPT_SoVITS/pretrained_models/s1v3.ckpt
Removing weight norm...
loading vocoder <All keys matched successfully>
Loading VITS weights from GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2Gv4.pth. <All keys matched successfully>
Loading BERT weights from GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large
Loading CNHuBERT weights from GPT_SoVITS/pretrained_models/chinese-hubert-base
INFO:     Started server process [XXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9880 (Press CTRL+C to quit)
```

## 📝 メモ

- 初回起動時は各言語の辞書ダウンロードで時間がかかる場合がある
- 中国語処理時はg2pwモデルの自動ダウンロードが発生
- 日本語処理時はopen_jtalk辞書の自動ダウンロードが発生
- 音声合成は通常3-10秒程度で完了
- 48kHz高品質出力に対応（v4の改善点）

---
*作成日: 2024年12月23日*
*GPT-SoVITS v4 + PyTorch 2.6 + CUDA 12.6対応版* 