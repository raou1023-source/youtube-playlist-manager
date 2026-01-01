# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# すべての必要なPythonファイルを明示的にリストアップ
python_files = [
    ('src\\youtube_client.py', '.'),
    ('src\\playlist_manager.py', '.'),
    ('src\\video_classifier.py', '.'),
    ('src\\config.py', '.'),
    ('src\\setup_wizard.py', '.'),
    ('src\\translations.py', '.'),
    ('src\\settings.py', '.'),
    ('src\\gui.py', '.'),
    ('src\\vimeo_client.py', '.'),
    ('src\\update_checker.py', '.'),
    ('src\\__init__.py', '.'),  # もし存在すれば
]

a = Analysis(
    ['src\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=python_files,  # すべてのPythonファイルを追加
    hiddenimports=[
        # Google API関連
        'googleapiclient',
        'googleapiclient.discovery',
        'googleapiclient.errors',
        'googleapiclient.http',
        'google.oauth2',
        'google.oauth2.credentials',
        'google_auth_oauthlib',
        'google_auth_oauthlib.flow',
        'google.auth.transport.requests',
        # GUI関連
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        # その他
        'dotenv',
        'argparse',
        'datetime',
        'pathlib',
        'json',
        'csv',
        'configparser',
        'webbrowser',
        'threading',
        'urllib',
        'urllib.parse',
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

# すべての.pyファイルをPureセクションに追加
a.pure += [
    ('youtube_client', 'src\\youtube_client.py', 'PYMODULE'),
    ('playlist_manager', 'src\\playlist_manager.py', 'PYMODULE'),
    ('video_classifier', 'src\\video_classifier.py', 'PYMODULE'),
    ('config', 'src\\config.py', 'PYMODULE'),
    ('setup_wizard', 'src\\setup_wizard.py', 'PYMODULE'),
    ('translations', 'src\\translations.py', 'PYMODULE'),
    ('settings', 'src\\settings.py', 'PYMODULE'),
    ('gui', 'src\\gui.py', 'PYMODULE'),
    ('vimeo_client', 'src\\vimeo_client.py', 'PYMODULE'),
    ('update_checker', 'src\\update_checker.py', 'PYMODULE'),
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTubePlaylistManager',
    debug=True,  # デバッグ情報を有効化
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # コンソールを表示
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
