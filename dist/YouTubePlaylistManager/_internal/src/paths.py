"""パス管理モジュール - EXE化対応

PyInstallerでビルドされた場合とスクリプト実行の場合で
適切なパスを返すユーティリティモジュール。
ユーザーデータ（credentials, config）はEXEと同じディレクトリに配置。
"""

import sys
import os
from pathlib import Path


def get_base_path() -> Path:
    """アプリケーションのベースパスを取得

    PyInstallerでビルドされた場合: EXEファイルのあるディレクトリ
    通常のPython実行の場合: プロジェクトルートディレクトリ
    """
    if getattr(sys, 'frozen', False):
        # PyInstallerでビルドされた場合
        return Path(os.path.dirname(sys.executable))
    else:
        # 通常のPython実行の場合
        # paths.py は src/ にあるので、parent で src、parent.parent でプロジェクトルート
        return Path(__file__).parent.parent


def get_internal_path() -> Path:
    """内部リソース（バンドルされたファイル）のパスを取得

    PyInstallerでビルドされた場合: _MEIPASS（一時展開ディレクトリ）
    通常のPython実行の場合: プロジェクトルートディレクトリ
    """
    if getattr(sys, 'frozen', False):
        # PyInstallerでビルドされた場合
        return Path(sys._MEIPASS)
    else:
        # 通常のPython実行の場合
        return Path(__file__).parent.parent


# ベースパス（EXEと同じディレクトリ、またはプロジェクトルート）
BASE_PATH = get_base_path()

# ユーザーデータディレクトリ（EXEの横に配置）
CREDENTIALS_PATH = BASE_PATH / 'credentials'
CONFIG_PATH = BASE_PATH / 'config'

# 各ファイルパス
CLIENT_SECRET_FILE = CREDENTIALS_PATH / 'client_secret.json'
TOKEN_FILE = CREDENTIALS_PATH / 'token.pickle'
VIMEO_TOKEN_FILE = CONFIG_PATH / 'vimeo_token.txt'
NICONICO_AUTH_FILE = CONFIG_PATH / 'niconico_auth.json'
SETUP_COMPLETE_FILE = CONFIG_PATH / 'setup_complete.json'
PRESETS_FILE = CONFIG_PATH / 'presets.json'
HISTORY_FILE = CONFIG_PATH / 'history.json'
INTEGRATED_PLAYLISTS_FILE = CONFIG_PATH / 'integrated_playlists.json'


def ensure_directories() -> None:
    """必要なディレクトリを作成"""
    CREDENTIALS_PATH.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.mkdir(parents=True, exist_ok=True)


def get_credentials_path() -> Path:
    """認証情報ディレクトリのパスを取得"""
    return CREDENTIALS_PATH


def get_config_path() -> Path:
    """設定ディレクトリのパスを取得"""
    return CONFIG_PATH


def get_client_secret_path() -> Path:
    """クライアントシークレットファイルのパスを取得"""
    env_path = os.getenv("GOOGLE_CLIENT_SECRET_PATH")
    if env_path:
        return Path(env_path)
    return CLIENT_SECRET_FILE


def get_token_path() -> Path:
    """トークンファイルのパスを取得"""
    env_path = os.getenv("GOOGLE_TOKEN_PATH")
    if env_path:
        return Path(env_path)
    return TOKEN_FILE


# 起動時にディレクトリを作成
ensure_directories()
