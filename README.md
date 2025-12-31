# 會議紀錄轉錄工具 - 使用說明

## 快速開始

### 1️⃣ 環境設置

```bash
# 創建項目目錄
mkdir meeting_transcript_tool
cd meeting_transcript_tool

# 安裝依賴
pip install -r requirements.txt

# 安裝 ffmpeg (Windows)
# 使用 Chocolatey: choco install ffmpeg
# 或從 https://ffmpeg.org/download.html 下載

# 安裝 ffmpeg (macOS)
# brew install ffmpeg

# 安裝 ffmpeg (Linux - Ubuntu/Debian)
# sudo apt-get install ffmpeg
```

### 2️⃣ 配置 API Key

編輯 `config.json`，填入你的 Gemini API Key：

```json
{
  "gemini_api_key": "YOUR-API-KEY-HERE",
  "gemini_model": "gemini-2.0-flash",
  ...
}
```

獲取 API Key：https://ai.google.dev/

### 3️⃣ 啟動應用

```bash
python main.py
```

瀏覽器打開 `http://localhost:5000`

---

## 功能說明

### 🎤 音檔轉逐字稿+摘要
1. 點擊按鈕選擇音檔 (MP3, WAV, M4A 等)
2. 系統自動：
   - 使用 Whisper 轉換為逐字稿
   - 使用 Gemini 修正基本錯誤
   - 使用 Gemini 生成會議摘要
3. 結果保存到 `temp/transcript.txt` 和 `temp/transcript_summary.txt`

### 🎬 影片轉逐字稿+摘要
1. 點擊按鈕選擇影片 (MP4, MOV, AVI 等)
2. 系統自動：
   - 使用 ffmpeg 提取音檔
   - 使用 Whisper 轉換為逐字稿
   - 使用 Gemini 修正基本錯誤
   - 使用 Gemini 生成會議摘要
3. 結果保存到 `temp/transcript.txt` 和 `temp/transcript_summary.txt`

### ⚙️ 打開設定
修改 Gemini API Key 和提示詞，即時保存。

---

## 配置說明

### config.json 參數

```json
{
  "gemini_api_key": "API 金鑰",
  "gemini_model": "使用的 Gemini 模型版本",
  "output_filename": "輸出文件名稱前綴",
  "prompts": {
    "error_correction": "字幕修正的提示詞",
    "summary": "會議摘要的提示詞"
  }
}
```

### 自訂提示詞

在設定頁面修改提示詞可改變輸出效果：

**字幕修正提示詞範例：**
```
請修正以下逐字稿中的基本錯誤（如標點符號、重複詞彙、明顯的語法錯誤），
保持原意不變，直接返回修正後的完整文本。
```

**摘要提示詞範例：**
```
請用繁體中文為以下會議記錄製作摘要，包含：
1. 會議要點（3-5個重點）
2. 決議和行動項目
3. 下次會議建議時間

請直接返回摘要內容，格式清晰即可。
```

---

## 文件結構

```
meeting_transcript_tool/
├── main.py                 # Flask 應用主程序
├── function.py             # 核心功能模組
├── config.json             # 配置文件 (需自填 API Key)
├── requirements.txt        # Python 依賴列表
├── index.html              # Web 界面
├── templates/
│   └── index.html          # (Flask 模板目錄)
├── temp/                   # 輸出文件目錄 (自動創建)
│   ├── transcript.txt      # 修正後的逐字稿
│   └── transcript_summary.txt  # 會議摘要
└── README.md               # 本文件
```

---

## 工作流程詳解

### 音檔流程
```
選擇音檔
  ↓
Whisper 轉換為逐字稿
  ↓
Gemini 修正錯誤
  ↓
Gemini 生成摘要
  ↓
保存到 temp/ 文件夾
  ↓
網頁顯示結果
```

### 影片流程
```
選擇影片
  ↓
ffmpeg 提取音軌
  ↓
Whisper 轉換為逐字稿
  ↓
Gemini 修正錯誤
  ↓
Gemini 生成摘要
  ↓
保存到 temp/ 文件夾
  ↓
網頁顯示結果
  ↓
清理臨時音檔
```

---

## 常見問題

### Q: 如何獲取 Gemini API Key?
A: 前往 https://ai.google.dev/，登入 Google 帳號，點擊「Get API Key」，創建新的免費金鑰。

### Q: Whisper 模型大小
A: 使用 `base` 模型，約 140MB，首次運行會自動下載。

### Q: 支持的文件格式
**音檔：** MP3, WAV, M4A, FLAC, OGG
**影片：** MP4, MOV, AVI, MKV, WebM

### Q: 處理時間多長？
A: 取決於文件長度：
- 5 分鐘音檔：約 1-2 分鐘
- 30 分鐘音檔：約 3-5 分鐘
- 影片額外需要 ffmpeg 提取時間

### Q: 如何修改摘要格式？
A: 在「打開設定」頁面修改 `prompts.summary` 欄位。

### Q: 輸出文件存在哪裡？
A: 項目根目錄下的 `temp/` 文件夾。

---

## 系統要求

- Python 3.8+
- ffmpeg (音檔提取需要)
- 2GB+ 磁盤空間 (Whisper 模型)
- 互聯網連接 (Gemini API 調用)

---

## 成本估算

基於 Google 免費方案：
- Whisper: 完全本地，免費
- Gemini API: 免費層級支持每分鐘 15 請求，每月 1500 請求
- 典型使用：每 30 分鐘會議消耗 2 次 Gemini 請求

---

## 故障排查

### ffmpeg 找不到
```bash
# Windows - 添加 ffmpeg 到系統路徑
# macOS/Linux - 確保已安裝
which ffmpeg
```

### Gemini API 錯誤
```
檢查 config.json 中的 API Key 是否正確
確認網絡連接正常
```

### Whisper 轉換慢
第一次運行會下載模型，後續會快得多。

---

**版本：1.0**
**最後更新：2025-12-24**
