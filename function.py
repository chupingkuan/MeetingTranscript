import os
import json
import subprocess
import whisper
import google.generativeai as genai

CONFIG_PATH = "config.json"
TEMP_DIR = "temp"

def ensure_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def video_to_audio(video_path):
    """使用 ffmpeg 從影片提取音檔"""
    ensure_temp_dir()
    audio_path = os.path.join(TEMP_DIR, "temp_audio.mp3")
    
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-q:a', '9',
        '-n',
        audio_path
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)
    return audio_path

def audio_to_transcript(audio_path):
    """使用 Whisper 將音檔轉換為逐字稿"""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="zh")
    return result["text"]

def correct_transcript(text):
    """使用 Gemini 修正逐字稿中的基本錯誤"""
    config = load_config()
    genai.configure(api_key=config["gemini_api_key"])
    
    model = genai.GenerativeModel(config["gemini_model"])
    prompt = config["prompts"]["error_correction"]
    
    message = model.generate_content(f"{prompt}\n\n{text}")
    return message.text

def summarize_transcript(text):
    """使用 Gemini 生成會議摘要"""
    config = load_config()
    genai.configure(api_key=config["gemini_api_key"])
    
    model = genai.GenerativeModel(config["gemini_model"])
    prompt = config["prompts"]["summary"]
    
    message = model.generate_content(f"{prompt}\n\n{text}")
    return message.text

def save_output(transcript, summary):
    """保存逐字稿和摘要到 temp 資料夾"""
    ensure_temp_dir()
    config = load_config()
    
    output_name = config["output_filename"]
    
    transcript_path = os.path.join(TEMP_DIR, f"{output_name}.txt")
    summary_path = os.path.join(TEMP_DIR, f"{output_name}_summary.txt")
    
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    return transcript_path, summary_path

def process_audio(audio_path):
    """完整的音檔處理流程"""
    transcript = audio_to_transcript(audio_path)
    corrected = correct_transcript(transcript)
    summary = summarize_transcript(corrected)
    save_output(corrected, summary)
    
    return {
        "transcript": corrected,
        "summary": summary
    }

def process_video(video_path):
    """完整的影片處理流程"""
    audio_path = video_to_audio(video_path)
    transcript = audio_to_transcript(audio_path)
    corrected = correct_transcript(transcript)
    summary = summarize_transcript(corrected)
    save_output(corrected, summary)
    
    os.remove(audio_path)  # 清理臨時音檔
    
    return {
        "transcript": corrected,
        "summary": summary
    }
