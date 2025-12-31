# 打包為 EXE 完整指南

## 📋 前置準備

### 1. 安裝 PyInstaller
```bash
pip install pyinstaller
```

### 2. 確保項目完整
```
meeting_transcript_tool/
├── main.py
├── function.py
├── config.json
├── build.py                ← 打包腳本
├── build.spec              ← PyInstaller 配置（可選）
├── requirements.txt
├── templates/
│   └── index.html
└── temp/                   （自動創建）
```

---

## 🚀 打包步驟

### **方法 1：使用打包腳本（推薦）**

最簡單的方法，自動檢查並執行打包：

```bash
python build.py
```

**腳本會自動執行：**
- ✓ 檢查 PyInstaller 是否安裝（未安裝會自動安裝）
- ✓ 清理舊的打包文件
- ✓ 檢查必要文件
- ✓ 運行 PyInstaller 打包
- ✓ 顯示打包結果和下一步說明

---

### **方法 2：手動使用 PyInstaller**

如果你想自己控制打包過程：

```bash
pyinstaller --name=MeetingTranscript \
            --onefile \
            --windowed \
            --add-data="templates:templates" \
            --add-data="config.json:." \
            --hidden-import=flask \
            --hidden-import=whisper \
            --hidden-import=google.generativeai \
            main.py
```

---

### **方法 3：使用 Spec 文件**

使用提供的 `build.spec` 文件：

```bash
pyinstaller build.spec
```

---

## 📦 打包後的文件結構

打包完成後會生成：

```
meeting_transcript_tool/
├── dist/
│   └── MeetingTranscript.exe        ← 可執行文件
├── build/                            ← 臨時打包文件（可刪除）
├── MeetingTranscript.spec            ← PyInstaller 配置（可刪除）
└── ... (其他源文件)
```

---

## 🎯 分發 EXE

### **最小化分發包**

只需要以下文件：

```
MeetingTranscript/
├── MeetingTranscript.exe             ← EXE 主程序
├── templates/
│   └── index.html                   ← Web 界面
├── config.json                       ← 配置文件
└── temp/                             ← 輸出文件夾（自動創建）
```

### **分發步驟**

1. **創建發布文件夾**
```bash
mkdir MeetingTranscript_Release
cd MeetingTranscript_Release
```

2. **複製必要文件**
```bash
# 複製 EXE
copy ..\dist\MeetingTranscript.exe .

# 複製 templates 文件夾
xcopy ..\templates templates /E /I

# 複製 config.json
copy ..\config.json .

# 複製 README（可選）
copy ..\README.md .
```

3. **創建啟動批次檔**（可選）
```batch
@echo off
MeetingTranscript.exe
pause
```

4. **壓縮分發**
```bash
# 使用 7-Zip 或 WinRAR 壓縮整個文件夾
```

---

## ⚠️ 重要注意事項

### **依賴環境**
分發的 EXE 仍需要以下環境：
- **ffmpeg** - 用於影片音檔提取
  - Windows: 須單獨安裝或添加到 PATH
  - macOS/Linux: 使用包管理器安裝

### **首次運行緩慢**
- EXE 首次運行會較慢（需要解包和初始化）
- 後續運行會快得多
- Whisper 模型首次運行會下載（~140MB）

### **配置文件**
- config.json 必須與 EXE 在同級目錄
- 使用者可在應用內修改 API Key 和提示詞

### **Gemini API Key**
- 使用者需要自行填寫 API Key
- 在應用的「打開設定」頁面編輯

---

## 🔧 常見問題

### Q: EXE 文件很大（>500MB）？
**A:** 正常現象，包含了 Python 和所有依賴。使用 `--onefile` 會較大，使用分散文件方式會較小。

修改打包命令去掉 `--onefile`：
```bash
pyinstaller --name=MeetingTranscript \
            --windowed \
            --add-data="templates:templates" \
            --add-data="config.json:." \
            --hidden-import=flask \
            --hidden-import=whisper \
            --hidden-import=google.generativeai \
            main.py
```

### Q: 運行 EXE 時出現 ffmpeg 錯誤？
**A:** 需要安裝 ffmpeg：
- **Windows**: 下載 https://ffmpeg.org/download.html，添加到 PATH
- **或使用 Chocolatey**: `choco install ffmpeg`

### Q: 如何自訂 EXE 圖標？
**A:** 在打包命令中添加 `--icon` 參數：
```bash
pyinstaller --icon=icon.ico ... main.py
```

### Q: EXE 無法執行，提示 module not found？
**A:** 確保所有依賴已安裝：
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Q: 如何縮小 EXE 文件大小？
**A:** 使用 UPX 壓縮（Windows 需要下載 upx.exe）：
```bash
pyinstaller --upx-dir=upx ... main.py
```

---

## 📝 腳本說明

### **build.py**
自動化打包腳本，功能包括：
- 自動檢查和安裝 PyInstaller
- 清理舊的打包文件
- 檢查必要文件是否存在
- 調用 PyInstaller 進行打包
- 顯示打包成功和下一步指導

### **build.spec**
PyInstaller 配置文件，定義：
- 隱藏導入模塊
- 數據文件包含路徑
- EXE 輸出名稱和設置

---

## 🎓 進階用法

### **為不同平台打包**

**Windows (從 Windows 打包)**
```bash
pyinstaller --onefile main.py
```

**macOS (從 macOS 打包)**
```bash
pyinstaller --onefile --windowed main.py
```

**Linux (從 Linux 打包)**
```bash
pyinstaller --onefile main.py
# 輸出為 ELF 可執行文件，非 EXE
```

### **跨平台打包技巧**
跨平台打包通常有兼容性問題。最穩妥的方法是：
- 在 Windows 打包 Windows 版本
- 在 macOS 打包 macOS 版本
- 在 Linux 打包 Linux 版本

---

## 📊 打包時間參考

打包時間取決於機器性能：
- **首次打包**: 3-10 分鐘（下載和安裝依賴）
- **後續打包**: 1-3 分鐘

---

**完成後，你將獲得一個獨立的 EXE 文件，可以直接分發給用戶使用！** 🎉
