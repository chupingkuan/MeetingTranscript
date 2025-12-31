from flask import Flask, render_template, request, jsonify, send_file
from function import process_audio, process_video, load_config, save_config
import os
import json
from datetime import datetime
import time
import threading

app = Flask(__name__)

def log(message):
    """統一的日誌輸出函數"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

@app.route('/')
def index():
    log("✓ 主頁面請求")
    return render_template('index.html')

@app.route('/api/config', methods=['GET', 'POST'])
def config_api():
    if request.method == 'GET':
        log("→ 讀取配置文件")
        config = load_config()
        log(f"  ✓ 配置讀取成功 (API Model: {config['gemini_model']})")
        return jsonify(config)
    
    if request.method == 'POST':
        log("→ 保存配置文件")
        new_config = request.get_json()
        save_config(new_config)
        log(f"  ✓ 配置保存成功")
        return jsonify({"status": "success"})

@app.route('/api/process', methods=['POST'])
def process_file():
    file = request.files['file']
    file_type = request.form.get('type')  # 'audio' 或 'video'
    
    log(f"→ 開始處理文件")
    log(f"  檔案名稱: {file.filename}")
    log(f"  檔案類型: {file_type}")
    log(f"  檔案大小: {len(file.read()) / (1024*1024):.2f} MB")
    file.seek(0)  # 重置文件指針
    
    file_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)
    log(f"  → 保存暫存文件到: {file_path}")
    file.save(file_path)
    log(f"    ✓ 暫存文件保存完成")
    
    if file_type == 'audio':
        log(f"→ 執行音檔處理流程")
        log(f"  [1/4] 開始 Whisper 轉錄...")
        result = process_audio(file_path)
        log(f"  [2/4] Whisper 轉錄完成")
        log(f"  [3/4] Gemini 修正和摘要進行中...")
        log(f"  [4/4] 所有步驟完成")
    else:  # video
        log(f"→ 執行影片處理流程")
        log(f"  [1/5] 開始 ffmpeg 音檔提取...")
        log(f"  [2/5] ffmpeg 提取完成")
        log(f"  [3/5] 開始 Whisper 轉錄...")
        result = process_video(file_path)
        log(f"  [4/5] Whisper 轉錄完成")
        log(f"  [5/5] Gemini 修正和摘要完成")
    
    # 清理上傳的源文件
    log(f"→ 清理暫存文件")
    os.remove(file_path)
    log(f"  ✓ 暫存文件已刪除")
    
    log(f"✓ 處理完成")
    log(f"  逐字稿長度: {len(result['transcript'])} 字")
    log(f"  摘要長度: {len(result['summary'])} 字")
    
    return jsonify(result)

@app.route('/api/download/<file_type>')
def download_file(file_type):
    """下載逐字稿或摘要文件"""
    config = load_config()
    output_name = config['output_filename']
    
    if file_type == 'transcript':
        file_path = os.path.join('temp', f'{output_name}.txt')
        download_name = f'{output_name}_逐字稿.txt'
        log(f"→ 下載逐字稿: {file_path}")
    elif file_type == 'summary':
        file_path = os.path.join('temp', f'{output_name}_summary.txt')
        download_name = f'{output_name}_摘要.txt'
        log(f"→ 下載摘要: {file_path}")
    else:
        log(f"✗ 不支持的下載類型: {file_type}")
        return jsonify({"error": "Invalid file type"}), 400
    
    if not os.path.exists(file_path):
        log(f"✗ 文件不存在: {file_path}")
        return jsonify({"error": "File not found"}), 404
    
    log(f"  ✓ 文件下載開始: {download_name}")
    return send_file(file_path, as_attachment=True, download_name=download_name)

@app.route('/api/open-config')
def open_config():
    """返回 config.json 路徑供用戶編輯"""
    config_path = os.path.abspath('config.json')
    log(f"✓ 打開配置文件: {config_path}")
    return jsonify({"path": config_path})

#監測網頁是否啟動
last_heartbeat = time.time()
server_shutdown_timer = None
def heartbeat_monitor():
    """背景監測線程：如果超過 10 秒沒收到心跳，就關閉伺服器"""
    global last_heartbeat
    log("→ 啟動心跳監測 (自動關閉功能)")
    
    while True:
        time.sleep(10) # 每 3 秒檢查一次
        current_time = time.time()
        time_diff = current_time - last_heartbeat
        
        # 如果超過 10 秒沒收到心跳
        if time_diff > 120:
            log(f"⚠ 超過 {int(time_diff)} 秒未收到網頁心跳，判定使用者已離開")
            log("正在自動關閉程式...")
            os._exit(0)

@app.route('/api/heartbeat', methods=['POST'])
def heartbeat():
    """接收網頁的心跳訊號"""
    global last_heartbeat
    last_heartbeat = time.time()
    return jsonify({"status": "alive"})

if __name__ == '__main__':
    log("=" * 60)
    log("🚀 會議紀錄轉錄工具 - 啟動")
    log("=" * 60)
    
    # 檢查必要文件
    log("→ 檢查必要文件...")
    if os.path.exists('config.json'):
        log("  ✓ config.json 存在")
    else:
        log("  ✗ config.json 不存在")
    
    if os.path.exists('templates/index.html'):
        log("  ✓ templates/index.html 存在")
    else:
        log("  ✗ templates/index.html 不存在")
    
    # 創建 temp 目錄
    if not os.path.exists('temp'):
        os.makedirs('temp')
        log("  ✓ 創建 temp 目錄")
    else:
        log("  ✓ temp 目錄已存在")
    
    log("→ 嘗試讀取配置...")
    try:
        config = load_config()
        log(f"  ✓ 配置讀取成功")
        log(f"  - Gemini 模型: {config['gemini_model']}")
        log(f"  - 輸出文件名: {config['output_filename']}")
        if config['gemini_api_key'] == 'your-gemini-api-key-here':
            log("  ⚠️  警告: API Key 未設置，請編輯 config.json")
        else:
            log(f"  ✓ API Key 已設置")
    except Exception as e:
        log(f"  ✗ 配置讀取失敗: {e}")
    
    log("=" * 60)
    log("🌐 Flask 服務啟動")
    log("   地址: http://localhost:5000")
    log("   按 Ctrl+C 停止服務")
    log("=" * 60)
    log("")
    
    # 啟動監測程序
    monitor_thread = threading.Thread(target=heartbeat_monitor, daemon=True)
    monitor_thread.start()
    
    # 啟動時先更新一次時間，避免剛啟動就關閉
    last_heartbeat = time.time()


    app.run(debug=False, port=5000)
