# 會議紀錄轉錄軟體 - 專案結構

## 目錄布局
```
meeting_transcript_tool/
├── main.py                 # Flask 主程序 + 路由
├── function.py             # 核心功能模組
├── config.json             # API key 和提示詞配置
├── requirements.txt        # Python 依賴
├── index.html              # Web 界面
├── temp/                   # 暫存輸出文件夾 (自動創建)
└── README.md               # 使用說明
```

## 各文件職責

### config.json
- 存儲 Gemini API Key
- 存儲 error_correction 和 summary 的提示詞
- 存儲輸出配置 (輸出目錄、檔案名)

### function.py
- `load_config()` - 讀取配置
- `audio_to_transcript(audio_path)` - 音檔→逐字稿
- `video_to_audio(video_path)` - 影片→音檔
- `correct_transcript(text)` - Gemini 字幕修正
- `summarize_transcript(text)` - Gemini 摘要生成
- `save_output(transcript, summary)` - 保存到 temp/

### main.py
- Flask 應用初始化
- `/` - 主頁面
- `/api/config` - 讀寫配置 API
- `/api/process` - 處理音檔/影片 API

### index.html
- 3 個按鈕：打開配置、音檔處理、影片處理
- 進度提示
- 結果預覽

## 工作流程

**音檔流程：**
音檔 → Whisper → 逐字稿 → Gemini修正 → Gemini摘要 → 輸出

**影片流程：**
影片 → ffmpeg提取音軌 → Whisper → 逐字稿 → Gemini修正 → Gemini摘要 → 輸出

**打開配置：**
編輯 config.json 文件

## 輸出文件
- `temp/transcript.txt` - 修正後的逐字稿
- `temp/summary.txt` - 會議摘要
