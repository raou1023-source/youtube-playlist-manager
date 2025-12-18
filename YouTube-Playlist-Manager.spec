# -*- mode: python ; coding: utf-8 -*-
# YouTube Playlist Manager - PyInstaller Spec File
#
# 重要: credentials/ と config/ フォルダはEXEに含めません
# これらのユーザーデータはEXEと同じディレクトリに自動作成されます

import os

# srcフォルダ内の全Pythonファイルを収集
src_files = []
for f in os.listdir('src'):
    if f.endswith('.py'):
        src_files.append((os.path.join('src', f), 'src'))

a = Analysis(
    ['main.py'],
    pathex=['src', '.'],
    binaries=[],
    datas=[
        ('src', 'src'),  # srcフォルダのみをコピー（ユーザーデータは含めない）
        # 注意: credentials/ と config/ はEXEに含めない
        # これらはアプリ起動時に自動作成される
    ],
    hiddenimports=[
        # プロジェクト内モジュール
        'paths',  # パス管理モジュール（EXE化対応）
        'gui',
        'youtube_client',
        'playlist_manager',
        'auth',
        'config',
        'video_classifier',
        'description_generator',
        'preset_manager',
        'history_manager',
        'vimeo_client',
        'niconico_client',
        'integrated_playlist',
        'setup_wizard',
        'credentials_manager',
        # Google API関連
        'google.auth',
        'google.auth.transport.requests',
        'google.oauth2.credentials',
        'google_auth_oauthlib.flow',
        'googleapiclient.discovery',
        'googleapiclient.errors',
        'googleapiclient.http',
        # その他の依存関係
        'cryptography',
        'cryptography.fernet',
        'cryptography.hazmat.primitives',
        'cryptography.hazmat.primitives.kdf.pbkdf2',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='YouTube-Playlist-Manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUIアプリなのでコンソールは非表示
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
