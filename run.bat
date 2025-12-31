@echo off
chcp 65001 > nul
echo.
echo ============================================================
echo 🚀 會議紀錄轉錄工具 - 啟動
echo ============================================================
echo.

REM 檢查 Python 是否安裝
python --version > nul 2>&1
if errorlevel 1 (
    echo ✗ 錯誤: 找不到 Python
    echo 請確保 Python 已安裝並添加到系統路徑
    pause
    exit /b 1
)

echo ✓ Python 已找到
echo.

REM 檢查必要文件
if not exist "config.json" (
    echo ✗ 錯誤: 找不到 config.json
    echo 請確保 config.json 存在於項目目錄
    pause
    exit /b 1
)
echo ✓ config.json 存在

if not exist "main.py" (
    echo ✗ 錯誤: 找不到 main.py
    echo 請確保 main.py 存在於項目目錄
    pause
    exit /b 1
)
echo ✓ main.py 存在

if not exist "templates\index.html" (
    echo ✗ 錯誤: 找不到 templates\index.html
    echo 請確保 templates 文件夾和 index.html 存在
    pause
    exit /b 1
)
echo ✓ templates\index.html 存在

echo.
echo ============================================================
echo 🌐 啟動 Flask 服務和瀏覽器
echo ============================================================
echo.

REM 等待 4 秒後打開瀏覽器（給 Flask 時間啟動）
timeout /t 5 /nobreak > nul

REM 使用默認瀏覽器打開 localhost:5000
start http://localhost:5000

REM 運行 Flask 應用
python main.py


