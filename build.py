#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
打包腳本：將應用打包成 exe (修正版 - 解決 Whisper 資源缺失問題)
使用方法: python build.py
"""

import os
import sys
import subprocess
import shutil
import platform

def main():
    print("=" * 60)
    print("🔨 會議紀錄轉錄工具 - 打包為 EXE (Whisper 修正版)")
    print("=" * 60)
    print()
    
    # 1. 檢查並獲取 Whisper 路徑
    print("→ 定位依賴庫...")
    try:
        import whisper
        whisper_path = os.path.dirname(whisper.__file__)
        print(f"  ✓ 找到 Whisper: {whisper_path}")
    except ImportError:
        print("  ✗ 找不到 whisper，請先 pip install openai-whisper")
        sys.exit(1)

    # 2. 定義路徑分隔符 (Windows 使用 ;, Linux/Mac 使用 :)
    sep = ';' if platform.system() == 'Windows' else ':'

    # 3. 準備打包參數
    # 關鍵修正：將 whisper/assets 資料夾強制複製到打包檔內部的 whisper/assets
    whisper_assets_arg = f"{os.path.join(whisper_path, 'assets')}{sep}whisper/assets"
    
    print()
    print("→ 清理舊文件...")
    for folder in ["build"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  ✓ 刪除 {folder}")
    if os.path.exists("MeetingTranscript.spec"):
        os.remove("MeetingTranscript.spec")

    # 4. 運行 PyInstaller
    print()
    print("→ 開始打包 (包含 Whisper 資源)...")
    
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=MeetingTranscript",
        "--onefile",
        "--console",  # 如果你想看到錯誤訊息，可以暫時改為 "--console" 或去掉這行
        
        # 數據文件
        "--add-data=templates:templates",
        "--add-data=config.json:.",
        f"--add-data={whisper_assets_arg}",  # <--- 關鍵修正
        
        # 隱藏導入 (增加 scipy 相關以防萬一)
        "--hidden-import=flask",
        "--hidden-import=whisper",
        "--hidden-import=google.generativeai",
        "--hidden-import=scipy.special.cython_special",
        "--hidden-import=sklearn.utils._cython_blas",
        "--hidden-import=sklearn.neighbors.typedefs",
        "--hidden-import=sklearn.neighbors.quad_tree",
        "--hidden-import=sklearn.tree",
        "--hidden-import=sklearn.tree._utils",
        
        # 忽略不必要的模組 (減小體積)
        "--exclude-module=matplotlib",
        "--exclude-module=tkinter",
        
        "main.py"
    ]
    
    # 打印執行的命令以便調試
    print(f"  執行命令: {' '.join(cmd)}")
    print()
    
    result = subprocess.call(cmd)
    
    if result == 0:
        print()
        print("=" * 60)
        print("✓ 打包成功！")
        print("=" * 60)
        print("EXE 位置: dist/MeetingTranscript.exe")
        print()
        print("⚠️ 運行注意：")
        print("1. 請確保 'templates' 資料夾和 'config.json' 與 exe 在同一目錄")
        print("2. 首次執行時，Whisper 仍需聯網下載模型 (約 140MB) 到使用者目錄")
        print("3. 如果仍有問題，請嘗試在命令行運行 exe 以查看具體報錯")
    else:
        print("✗ 打包失敗")
        sys.exit(1)

if __name__ == "__main__":
    main()
