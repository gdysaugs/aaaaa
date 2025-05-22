#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import torch
from TTS.api import TTS
import torch.serialization
from TTS.tts.configs.xtts_config import XttsConfig
import importlib
from TTS.tts.models.xtts import XttsAudioConfig
from TTS.config.shared_configs import BaseDatasetConfig
import numpy as np
import librosa
import soundfile as sf
from scipy.signal import butter, filtfilt, savgol_filter, hilbert
import tempfile
import shutil

# PyTorch 2.6以降ではweights_onlyパラメータがデフォルトでTrueになるため、
# 環境変数を設定して常にFalseを使用
os.environ["TORCH_LOAD_WEIGHTS_ONLY"] = "0"
# または明示的にweights_onlyをFalseに設定する環境変数
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"

def butter_bandpass(lowcut, highcut, fs, order=5):
    """バターワースバンドパスフィルター設計"""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_advanced_noise_reduction(audio_path, denoise_strength=0.05, high_pass_cutoff=80, low_pass_cutoff=8000, preserve_voice_range=True):
    """
    高度なノイズ除去処理を適用する関数（日本語音声に最適化）
    
    Parameters:
    -----------
    audio_path : str
        処理する音声ファイルのパス
    denoise_strength : float
        ノイズ除去の強度（0.0〜1.0）
    high_pass_cutoff : int
        ハイパスフィルターのカットオフ周波数（Hz）
    low_pass_cutoff : int
        ローパスフィルターのカットオフ周波数（Hz）
    preserve_voice_range : bool
        人間の声の周波数帯域（特に日本語）を保護するかどうか
    
    Returns:
    --------
    None
        処理した音声は同じファイルに上書き保存されます
    """
    print(f"高度なノイズ除去処理を適用しています...")
    
    # 音声ファイルの読み込み
    y, sr = librosa.load(audio_path, sr=None)
    
    # 一時ファイルを作成（元の音声を保存）
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_file.close()
    sf.write(temp_file.name, y, sr)
    
    # スペクトログラムに変換
    D = librosa.stft(y, n_fft=2048, hop_length=512, win_length=2048)
    
    # 振幅スペクトログラムの取得
    magnitude, phase = librosa.magphase(D)
    
    # 周波数ビンの計算
    freq_bins = librosa.fft_frequencies(sr=sr, n_fft=2048)
    
    # 周波数フィルタリング（ハイパスとローパス）
    mask = np.ones_like(magnitude)
    
    # ハイパスフィルター（よりなだらかな遷移）
    high_pass_idx = np.where(freq_bins < high_pass_cutoff)[0]
    if len(high_pass_idx) > 0:
        mask[high_pass_idx, :] = np.maximum(0, 1 - np.power((high_pass_cutoff - freq_bins[high_pass_idx]) / high_pass_cutoff, 2)[:, np.newaxis])
    
    # ローパスフィルター（よりなだらかな遷移）
    low_pass_idx = np.where(freq_bins > low_pass_cutoff)[0]
    if len(low_pass_idx) > 0:
        max_freq = freq_bins.max()
        mask[low_pass_idx, :] = np.maximum(0, 1 - np.power((freq_bins[low_pass_idx] - low_pass_cutoff) / (max_freq - low_pass_cutoff), 2)[:, np.newaxis])
    
    # 日本語の声の主要周波数帯域を強調（約300Hz〜3.4kHz）
    if preserve_voice_range:
        voice_mask = np.ones_like(magnitude)
        voice_idx = np.where((freq_bins >= 300) & (freq_bins <= 3400))[0]
        if len(voice_idx) > 0:
            voice_boost = 1.2  # 声の周波数帯域をブースト
            for idx in voice_idx:
                mask[idx, :] = np.minimum(mask[idx, :] * voice_boost, 1.0)
    
    # スペクトラルゲーティング（ノイズ除去）
    # ノイズフロア推定（よりロバストな推定）
    noise_floor = np.percentile(magnitude, 15, axis=1, keepdims=True)
    
    # 各時間フレームでのSN比の計算
    snr = np.maximum(0, magnitude - noise_floor * (1.0 + denoise_strength * 15))
    
    # ノイズ抑制のためのゲイン計算（ソフトなゲーティング）
    gain = np.power(snr / (snr + noise_floor * denoise_strength * 15), 1.2)
    
    # スペクトログラムとマスク・ゲインを掛け合わせる
    magnitude_filtered = magnitude * mask * gain
    
    # 位相情報を元に戻してISTFT
    D_filtered = magnitude_filtered * np.exp(1.j * np.angle(D))
    y_filtered = librosa.istft(D_filtered, hop_length=512, win_length=2048)
    
    # バンドパスフィルターを適用（80-7500Hz）
    b, a = butter_bandpass(80, 7500, sr, order=4)
    y_filtered = filtfilt(b, a, y_filtered)
    
    # 韻律を保持しながらダイナミックレンジを圧縮
    # エンベロープの抽出（scipy.signalのhilbertを使用）
    analytic_signal = hilbert(y_filtered)
    envelope = np.abs(analytic_signal)
    smoothed_envelope = savgol_filter(envelope, 1001, 2)
    smoothed_envelope = np.maximum(smoothed_envelope, 1e-8) # Smooth envelope must be positive
    
    # 音量変化を保ちながらダイナミックレンジ圧縮
    y_normalized = y_filtered / smoothed_envelope * np.power(smoothed_envelope, 0.8)
    
    # クリッピングを避けるために正規化
    y_normalized = librosa.util.normalize(y_normalized, norm=np.inf, axis=0) * 0.95
    
    # 処理した音声を保存
    sf.write(audio_path, y_normalized, sr)
    
    # 元の音声と処理済み音声をブレンド（自然さを保持）
    y_orig, sr_orig = librosa.load(temp_file.name, sr=None)
    if len(y_orig) > len(y_normalized):
        y_orig = y_orig[:len(y_normalized)]
    elif len(y_orig) < len(y_normalized):
        y_normalized = y_normalized[:len(y_orig)]
    
    # 自然さを保持するため少量の原音をミックス
    blend_ratio = 0.15  # 15%の原音をミックス
    y_final = (1 - blend_ratio) * y_normalized + blend_ratio * y_orig
    
    # 最終的な音声を保存
    sf.write(audio_path, y_final, sr)
    
    # 一時ファイルを削除
    os.unlink(temp_file.name)
    
    print(f"✅ 高度なノイズ除去処理が完了しました")

def main():
    """
    Coqui TTSを使用した日本語ボイスクローンCLIスクリプト
    """
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description="Coqui TTS 日本語ボイスクローン")
    parser.add_argument("--text", type=str, required=True, help="合成する日本語テキスト")
    parser.add_argument("--speaker_wav", type=str, required=True, help="クローン元の音声ファイル")
    parser.add_argument("--output", type=str, default="/app/output/output.wav", help="出力ファイルパス")
    parser.add_argument("--model", type=str, default="tts_models/multilingual/multi-dataset/xtts_v2", 
                         help="使用するTTSモデル")
    parser.add_argument("--denoise_strength", type=float, default=0.005, help="ノイズ除去強度（0.0〜1.0）")
    parser.add_argument("--length_penalty", type=float, default=1.0, help="長さペナルティ（0.5〜2.0推奨）")
    
    args = parser.parse_args()
    
    # 言語を日本語に固定
    language = "ja"
    
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
        # PyTorch 2.6のweights_onlyパラメータ問題に対応
        print(f"PyTorchバージョン: {torch.__version__}")
        
        # XTTSの必要なクラスを安全なグローバル変数リストに追加
        if hasattr(torch.serialization, "add_safe_globals"):
            torch.serialization.add_safe_globals([
                XttsConfig, 
                XttsAudioConfig,
                BaseDatasetConfig
            ])
            print("必要なクラスを安全なグローバル変数リストに追加しました")
        
        # モデルのロード
        print(f"\nモデル '{args.model}' をロードしています...")
        tts = TTS(args.model)
        if device == "cuda":
            tts.to(torch.device("cuda"))
        
        # 入力情報の表示
        print(f"\n入力テキスト: {args.text}")
        print(f"クローン元音声: {args.speaker_wav}")
        print(f"言語: {language} (固定)")
        print(f"出力ファイル: {args.output}")
        print(f"ノイズ除去強度: {args.denoise_strength}")
        print(f"長さペナルティ: {args.length_penalty}")
        
        # 音声合成の実行
        print("\n音声合成を開始します...")
        output_dir = os.path.dirname(args.output)
        os.makedirs(output_dir, exist_ok=True)
        
        # 日本語合成の最適化パラメータ
        temperature = 0.65  # さらに下げて安定性を最優先
        repetition_penalty = 1.5  # 繰り返しをより強く抑制
        top_k = 20  # より決定的な選択に
        top_p = 0.8  # より安定した日本語発音のため
        
        # XTTS v2モデルでの音声合成（モデル内部APIを使用）
        if hasattr(tts, "synthesizer") and hasattr(tts.synthesizer, "tts_with_params"):
            # モデル内部APIが利用可能な場合は最適化パラメータを設定
            tts.synthesizer.tts_to_file(
                text=args.text,
                speaker_wav=args.speaker_wav,
                language=language,
                file_path=args.output,
                temperature=temperature,
                length_penalty=args.length_penalty,
                repetition_penalty=repetition_penalty,
                top_k=top_k,
                top_p=top_p
            )
        else:
            # 標準APIの場合
            tts.tts_to_file(
                text=args.text,
                speaker_wav=args.speaker_wav,
                language=language,
                file_path=args.output
            )
        
        print(f"\n✅ 音声合成が完了しました: {args.output}")
        
        # 高度なノイズ除去処理を適用（より控えめな設定で）
        apply_advanced_noise_reduction(
            args.output, 
            denoise_strength=args.denoise_strength * 0.5,  # デノイズ強度を半分に
            high_pass_cutoff=80,   # 80Hz以下の低周波ノイズを除去
            low_pass_cutoff=7000,  # 7kHz以上の高周波ノイズを除去
            preserve_voice_range=True  # 日本語音声の周波数帯域を保護
        )
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main()) 