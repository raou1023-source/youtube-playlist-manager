# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

# Google API関連のすべてを収集
googleapi_datas, googleapi_binaries, googleapi_hiddenimports = collect_all('googleapiclient')

a = Analysis(
    ['src\\main.py'],
    pathex=['src'],  # srcをモジュール検索パスに追加
    binaries=googleapi_binaries,
    datas=googleapi_datas + [
        ('src', 'src'),  # srcディレクトリ全体をsrcとして含める
    ],
    hiddenimports=googleapi_hiddenimports + [
        # プロジェクト内モジュール（srcなしで参照）
        'youtube_client',
        'playlist_manager',
        'video_classifier',
        'config',
        'setup_wizard',
        'translations',
        'settings',
        'gui',
        'vimeo_client',
        'update_checker',
        # Google API
        'google.oauth2.credentials',
        'google_auth_oauthlib.flow',
        'google.auth.transport.requests',
        # GUI
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        # その他
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTubePlaylistManager',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # デバッグ用
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
