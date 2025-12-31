# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Meeting Transcript Tool

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import sys
import os

block_cipher = None

# 收集必要的隱藏模塊
hiddenimports = [
    'flask',
    'whisper',
    'google.generativeai',
]

# 收集數據文件
datas = [
    ('templates', 'templates'),
    ('config.json', '.'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MeetingTranscript',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # 可選：如果有 icon.ico 文件
)
