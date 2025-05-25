#!/usr/bin/env python3
"""
Wav2Lip API Server Startup Script - CLI Wrapper Version
CLIで成功したコマンドをそのまま使用するバージョン
"""

import uvicorn
import logging
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """ログ設定"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("wav2lip_api.log")
        ]
    )

def main():
    """メイン関数"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Wav2Lip API Server - CLI Wrapper Version...")
    logger.info("Version: 2.0.0 (CLIで成功したコマンドをそのまま使用)")
    logger.info("Host: 0.0.0.0")
    logger.info("Port: 8000")
    logger.info("Debug: False")
    logger.info("パディング形式: スペース区切り (例: '0 10 0 0')")
    
    try:
        uvicorn.run(
            "api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
