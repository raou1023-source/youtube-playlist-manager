# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Google API関連のすべてを収集
googleapi_datas, googleapi_binaries, googleapi_hiddenimports = collect_all('googleapiclient')

a = Analysis(
    ['src\\main.py'],
    pathex=['src'],
    binaries=googleapi_binaries,
    datas=googleapi_datas + [
        ('src', 'src'),
    ],
    hiddenimports=googleapi_hiddenimports + [
        'auth', 'backup_manager', 'config', 'config_temp', 'credentials_manager',
        'description_generator', 'export_manager', 'gui', 'history_manager',
        'integrated_playlist', 'language_manager', 'niconico_client', 'paths',
        'playlist_manager', 'preset_manager', 'setup_wizard', 'translations',
        'update_checker', 'video_classifier', 'vimeo_client', 'youtube_client',
        'google.oauth2.credentials', 'google_auth_oauthlib.flow',
        'googleapiclient.discovery', 'googleapiclient.errors',
        'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog',
        'dotenv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],  # ここを空にする（onefileではなくonedir）
    exclude_binaries=True,  # バイナリを別ファイルとして配置
    name='YouTubePlaylistManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='YouTubePlaylistManager',
)
