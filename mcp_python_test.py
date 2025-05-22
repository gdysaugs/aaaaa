#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import datetime

# MCP経由で作成したPythonスクリプト
class McpTest:
    def __init__(self):
        self.creation_time = datetime.datetime.now()
        
    def show_info(self):
        print("="*50)
        print("🤖 ClaudeCode MCP で作成したPythonファイルです！")
        print("="*50)
        print(f"📅 作成時刻: {self.creation_time}")
        # WSLではgetlogin()が失敗するのでUSERまたはLOGNAME環境変数を使用
        username = os.environ.get('USER') or os.environ.get('LOGNAME') or 'unknown'
        print(f"👤 実行ユーザー: {username}")
        print(f"💻 OS情報: {platform.platform()}")
        print(f"🐍 Python情報: {sys.version}")
        print(f"📁 実行ディレクトリ: {os.getcwd()}")
        print("="*50)
        
        # ファイル一覧を表示
        print("\n📂 ディレクトリ内のPythonファイル:")
        for file in os.listdir('.'):
            if file.endswith('.py'):
                file_stats = os.stat(file)
                size = file_stats.st_size
                print(f"  - {file} ({size} bytes)")

if __name__ == "__main__":
    test = McpTest()
    test.show_info() 