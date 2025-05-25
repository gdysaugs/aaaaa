#!/usr/bin/env python3
"""
Wav2Lip CLI Wrapper Test Script
CLIラッパーの動作をテストするスクリプト
"""

import asyncio
import sys
from pathlib import Path
import logging

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.wav2lip_cli_wrapper import Wav2LipCLIWrapper

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_cli_wrapper():
    """CLIラッパーのテスト"""
    
    # CLIラッパーを初期化
    cli_wrapper = Wav2LipCLIWrapper()
    
    # モデル情報を確認
    logger.info("=== モデル情報確認 ===")
    model_info = cli_wrapper.get_model_info()
    logger.info(f"モデル情報: {model_info}")
    
    if not cli_wrapper.is_model_loaded():
        logger.error("モデルファイルが見つかりません！")
        logger.error("以下のファイルが必要です:")
        logger.error(f"- {cli_wrapper.wav2lip_model}")
        logger.error(f"- {cli_wrapper.s3fd_model}")
        return False
    
    logger.info("✅ モデルファイルが正常に見つかりました")
    
    # テスト用ファイルの確認
    test_data_dir = Path("data/input")
    if not test_data_dir.exists():
        logger.error(f"テストデータディレクトリが見つかりません: {test_data_dir}")
        return False
    
    # テスト用動画と音声ファイルを探す
    video_files = list(test_data_dir.glob("*.mp4")) + list(test_data_dir.glob("*.avi"))
    audio_files = list(test_data_dir.glob("*.wav")) + list(test_data_dir.glob("*.mp3"))
    
    if not video_files:
        logger.error("テスト用動画ファイルが見つかりません")
        return False
    
    if not audio_files:
        logger.error("テスト用音声ファイルが見つかりません")
        return False
    
    video_file = video_files[0]
    audio_file = audio_files[0]
    
    logger.info(f"テスト用動画: {video_file}")
    logger.info(f"テスト用音声: {audio_file}")
    
    # ファイル内容を読み込み
    try:
        with open(video_file, "rb") as f:
            video_content = f.read()
        
        with open(audio_file, "rb") as f:
            audio_content = f.read()
        
        logger.info(f"動画ファイルサイズ: {len(video_content)} bytes")
        logger.info(f"音声ファイルサイズ: {len(audio_content)} bytes")
        
    except Exception as e:
        logger.error(f"ファイル読み込みエラー: {e}")
        return False
    
    # CLIラッパーでテスト処理
    job_id = "test_job_001"
    
    try:
        logger.info("=== CLIラッパーテスト開始 ===")
        
        result = await cli_wrapper.process_video_cli(
            job_id=job_id,
            video_content=video_content,
            audio_content=audio_content,
            video_filename=video_file.name,
            audio_filename=audio_file.name,
            pads="0 10 0 0",  # CLIで成功したパディング設定
            face_det_batch_size=1,
            wav2lip_batch_size=4,
            resize_factor=1
        )
        
        logger.info(f"✅ 処理成功: {result}")
        
        # 出力ファイルの確認
        output_path = Path(result["output_path"])
        if output_path.exists():
            logger.info(f"✅ 出力ファイル生成成功: {output_path}")
            logger.info(f"出力ファイルサイズ: {output_path.stat().st_size} bytes")
        else:
            logger.error("❌ 出力ファイルが見つかりません")
            return False
        
        # クリーンアップ
        await cli_wrapper.cleanup_job(job_id)
        logger.info("✅ クリーンアップ完了")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 処理エラー: {e}")
        return False

def main():
    """メイン関数"""
    logger.info("Wav2Lip CLI Wrapper Test Script")
    logger.info("=" * 50)
    
    try:
        success = asyncio.run(test_cli_wrapper())
        
        if success:
            logger.info("=" * 50)
            logger.info("✅ すべてのテストが成功しました！")
            logger.info("CLIラッパーは正常に動作しています")
        else:
            logger.error("=" * 50)
            logger.error("❌ テストが失敗しました")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("テストが中断されました")
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 