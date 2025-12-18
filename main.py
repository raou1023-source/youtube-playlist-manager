#!/usr/bin/env python3
"""YouTube Playlist Manager - エントリーポイント

PyInstallerでEXE化する際のインポート問題を解決するためのメインモジュール。
このファイルからアプリケーションを起動することで、相対インポートの問題を回避します。
"""

import sys
import os
from pathlib import Path

# 実行ファイルまたはスクリプトのディレクトリを取得
if getattr(sys, 'frozen', False):
    # PyInstallerでビルドされた場合
    BASE_DIR = Path(sys._MEIPASS)
    APP_DIR = Path(os.path.dirname(sys.executable))
else:
    # 通常のPython実行の場合
    BASE_DIR = Path(__file__).parent
    APP_DIR = BASE_DIR

# srcディレクトリをパスに追加
SRC_DIR = BASE_DIR / "src"
if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))
else:
    # PyInstallerビルド時は直接srcがBASE_DIRにコピーされる場合がある
    sys.path.insert(0, str(BASE_DIR))

# プロジェクトルートもパスに追加
sys.path.insert(0, str(BASE_DIR))

# 起動時にユーザーデータディレクトリを作成
# paths.pyがインポートされた時点でensure_directories()が実行される
try:
    from paths import ensure_directories, CREDENTIALS_PATH, CONFIG_PATH
    ensure_directories()
except ImportError:
    # paths.pyがない場合はフォールバック
    CREDENTIALS_PATH = APP_DIR / "credentials"
    CONFIG_PATH = APP_DIR / "config"
    CREDENTIALS_PATH.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.mkdir(parents=True, exist_ok=True)


def main():
    """アプリケーションのエントリーポイント"""
    try:
        # guiモジュールをインポートして起動
        from gui import main as gui_main
        gui_main()
    except ImportError as e:
        # フォールバック: src.gui を試す
        try:
            from src.gui import main as gui_main
            gui_main()
        except ImportError:
            print(f"Error: Could not import GUI module: {e}")
            print(f"sys.path: {sys.path}")
            sys.exit(1)


if __name__ == "__main__":
    main()
