#!/bin/bash
# 🎤 GPT-SoVITS v4 モデル自動ダウンロードスクリプト
# 使用方法: ./download_models.sh

set -e  # エラー時に停止

echo "🎤 GPT-SoVITS v4 モデルダウンロード開始..."
echo ""

# 必要ディレクトリ作成
echo "📁 ディレクトリ作成中..."
mkdir -p pretrained_models/{chinese-hubert-base,chinese-roberta-wwm-ext-large,gsv-v4-pretrained}
mkdir -p {GPT_weights,SoVITS_weights,input,output,logs,reference,test_samples}

# ダウンロード関数
download_file() {
    local url=$1
    local output=$2
    local description=$3
    local size=$4
    
    echo "📥 $description ($size) ダウンロード中..."
    echo "   URL: $url"
    echo "   出力: $output"
    
    if [ -f "$output" ]; then
        echo "   ✅ ファイルが既に存在します: $output"
        return 0
    fi
    
    # ディレクトリ作成
    mkdir -p "$(dirname "$output")"
    
    # ダウンロード実行
    if wget -O "$output" "$url"; then
        echo "   ✅ ダウンロード完了: $output"
        # ファイルサイズ確認
        actual_size=$(du -h "$output" | cut -f1)
        echo "   📊 ファイルサイズ: $actual_size"
    else
        echo "   ❌ ダウンロード失敗: $output"
        rm -f "$output"  # 失敗したファイルを削除
        return 1
    fi
}

echo "🔍 必要なモデルファイルをダウンロードします..."
echo "📊 総ダウンロードサイズ: 約2.6GB"
echo ""

# 1. chinese-hubert-base (361MB)
echo "1️⃣ Chinese HuBERT Base モデル"
download_file \
    "https://huggingface.co/TencentGameMate/chinese-hubert-base/resolve/main/pytorch_model.bin" \
    "pretrained_models/chinese-hubert-base/pytorch_model.bin" \
    "Chinese HuBERT Base - PyTorch Model" \
    "361MB"

download_file \
    "https://huggingface.co/TencentGameMate/chinese-hubert-base/resolve/main/config.json" \
    "pretrained_models/chinese-hubert-base/config.json" \
    "Chinese HuBERT Base - Config" \
    "1KB"

download_file \
    "https://huggingface.co/TencentGameMate/chinese-hubert-base/resolve/main/preprocessor_config.json" \
    "pretrained_models/chinese-hubert-base/preprocessor_config.json" \
    "Chinese HuBERT Base - Preprocessor Config" \
    "1KB"

echo ""

# 2. chinese-roberta-wwm-ext-large (1.3GB)
echo "2️⃣ Chinese RoBERTa WWM Ext Large モデル"
download_file \
    "https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/resolve/main/pytorch_model.bin" \
    "pretrained_models/chinese-roberta-wwm-ext-large/pytorch_model.bin" \
    "Chinese RoBERTa WWM Ext Large - PyTorch Model" \
    "1.3GB"

download_file \
    "https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/resolve/main/config.json" \
    "pretrained_models/chinese-roberta-wwm-ext-large/config.json" \
    "Chinese RoBERTa WWM Ext Large - Config" \
    "1KB"

download_file \
    "https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/resolve/main/tokenizer.json" \
    "pretrained_models/chinese-roberta-wwm-ext-large/tokenizer.json" \
    "Chinese RoBERTa WWM Ext Large - Tokenizer" \
    "2MB"

download_file \
    "https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/resolve/main/tokenizer_config.json" \
    "pretrained_models/chinese-roberta-wwm-ext-large/tokenizer_config.json" \
    "Chinese RoBERTa WWM Ext Large - Tokenizer Config" \
    "1KB"

download_file \
    "https://huggingface.co/hfl/chinese-roberta-wwm-ext-large/resolve/main/vocab.txt" \
    "pretrained_models/chinese-roberta-wwm-ext-large/vocab.txt" \
    "Chinese RoBERTa WWM Ext Large - Vocabulary" \
    "110KB"

echo ""

# 3. GPT-SoVITS v4 プリトレインモデル (790MB)
echo "3️⃣ GPT-SoVITS v4 プリトレインモデル"
download_file \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/gsv-v4-pretrained/s2G.pth" \
    "pretrained_models/gsv-v4-pretrained/s2G.pth" \
    "GPT-SoVITS v4 - Generator Model" \
    "395MB"

download_file \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/gsv-v4-pretrained/s2D.pth" \
    "pretrained_models/gsv-v4-pretrained/s2D.pth" \
    "GPT-SoVITS v4 - Discriminator Model" \
    "246MB"

download_file \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/gsv-v4-pretrained/vocoder.pth" \
    "pretrained_models/gsv-v4-pretrained/vocoder.pth" \
    "GPT-SoVITS v4 - Vocoder Model" \
    "149MB"

echo ""

# 4. s1v3.ckpt (149MB)
echo "4️⃣ GPT-SoVITS v4 S1 モデル"
download_file \
    "https://huggingface.co/lj1995/GPT-SoVITS/resolve/main/s1v3.ckpt" \
    "pretrained_models/s1v3.ckpt" \
    "GPT-SoVITS v4 - S1 Checkpoint" \
    "149MB"

echo ""

# ダウンロード結果確認
echo "📊 ダウンロード結果確認:"
echo ""

models=(
    "pretrained_models/chinese-hubert-base/pytorch_model.bin"
    "pretrained_models/chinese-roberta-wwm-ext-large/pytorch_model.bin"
    "pretrained_models/gsv-v4-pretrained/s2G.pth"
    "pretrained_models/gsv-v4-pretrained/s2D.pth"
    "pretrained_models/gsv-v4-pretrained/vocoder.pth"
    "pretrained_models/s1v3.ckpt"
)

success_count=0
total_count=${#models[@]}

for model in "${models[@]}"; do
    if [ -f "$model" ]; then
        size=$(du -h "$model" | cut -f1)
        echo "✅ $model ($size)"
        ((success_count++))
    else
        echo "❌ $model (見つかりません)"
    fi
done

echo ""
echo "📊 ダウンロード完了: $success_count/$total_count"

if [ $success_count -eq $total_count ]; then
    echo "🎉 全モデルファイルのダウンロードが完了しました！"
    
    # 総サイズ計算
    total_size=$(du -sh pretrained_models/ | cut -f1)
    echo "📊 総ダウンロードサイズ: $total_size"
    
    echo ""
    echo "🚀 次のステップ:"
    echo "  1. 参照音声ファイルを reference/ ディレクトリに配置"
    echo "  2. Docker構築: docker compose -f docker-compose.fastapi.yml build"
    echo "  3. FastAPI起動: ./start_all_apis.sh"
    echo ""
    echo "✅ GPT-SoVITS v4 の準備が完了しました！"
    
    exit 0
else
    echo "⚠️  一部のモデルファイルのダウンロードに失敗しました"
    echo "🔄 再実行してください: ./download_models.sh"
    
    exit 1
fi 