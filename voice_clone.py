#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import torch
from TTS.api import TTS

def main():
    """
    Coqui TTSを使用したボイスクローンCLIスクリプト
    """
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description="Coqui TTS ボイスクローン")
    parser.add_argument("--text", type=str, required=True, help="合成するテキスト")
    parser.add_argument("--speaker_wav", type=str, required=True, help="クローン元の音声ファイル")
    parser.add_argument("--language", type=str, default="ja", help="言語コード (en, ja, など)")
    parser.add_argument("--output", type=str, default="/app/output/output.wav", help="出力ファイルパス")
    parser.add_argument("--model", type=str, default="tts_models/multilingual/multi-dataset/xtts_v2", 
                         help="使用するTTSモデル")
    
    args = parser.parse_args()
    
    # デバイスの設定
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用デバイス: {device}")
    
    # CUDAデバイス情報の表示
    if device == "cuda":
        print(f"利用可能なGPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU数: {torch.cuda.device_count()}")
        print(f"GPU使用メモリ: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB")
        print(f"GPU総メモリ: {torch.cuda.get_device_properties(0).total_memory / 1024**2:.2f} MB")
    
    try:
        # 利用可能なモデルのリスト表示
        print("利用可能なモデル:")
        tts_api = TTS()
        available_models = tts_api.list_models()
        print(f"DEBUG: type(available_models) = {type(available_models)}")
        if hasattr(available_models, "list") and callable(available_models.list):
            available_models = list(available_models.list())
        elif isinstance(available_models, (list, tuple)):
            available_models = list(available_models)
        else:
            print("DEBUG: available_modelsはリスト化できません")
            available_models = []
        for i, model in enumerate(available_models):
            if "xtts" in model.lower() or "your_tts" in model.lower():
                print(f"  - {model}")
        
        # モデルのロード
        print(f"\nモデル '{args.model}' をロードしています...")
        tts = TTS(args.model).to(device)
        
        # 入力情報の表示
        print(f"\n入力テキスト: {args.text}")
        print(f"クローン元音声: {args.speaker_wav}")
        print(f"言語: {args.language}")
        print(f"出力ファイル: {args.output}")
        
        # 音声合成の実行
        print("\n音声合成を開始します...")
        output_dir = os.path.dirname(args.output)
        os.makedirs(output_dir, exist_ok=True)
        
        tts.tts_to_file(
            text=args.text,
            speaker_wav=args.speaker_wav,
            language=args.language,
            file_path=args.output
        )
        
        print(f"\n✅ 音声合成が完了しました: {args.output}")
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main()) 