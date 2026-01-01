"""OAuth2認証処理モジュール"""

import sys
import os

# 親ディレクトリをパスに追加（通常のPython実行用）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import pickle
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

from config import (
    YOUTUBE_API_SCOPES,
    get_client_secret_path,
    get_token_path,
)


class YouTubeAuthenticator:
    """YouTube API認証を管理するクラス"""

    def __init__(
        self,
        client_secret_path: Optional[Path] = None,
        token_path: Optional[Path] = None,
        scopes: Optional[list[str]] = None,
    ):
        self.client_secret_path = client_secret_path or get_client_secret_path()
        self.token_path = token_path or get_token_path()
        self.scopes = scopes or YOUTUBE_API_SCOPES
        self._credentials: Optional[Credentials] = None

    def get_credentials(self) -> Credentials:
        """認証情報を取得（必要に応じて認証フローを実行）"""
        if self._credentials and self._credentials.valid:
            return self._credentials

        # 保存済みトークンを読み込み
        if self.token_path.exists():
            with open(self.token_path, "rb") as token_file:
                self._credentials = pickle.load(token_file)

        # トークンが無効または期限切れの場合
        if not self._credentials or not self._credentials.valid:
            if self._credentials and self._credentials.expired and self._credentials.refresh_token:
                # トークンをリフレッシュ
                self._credentials.refresh(Request())
            else:
                # 新規認証フローを実行
                self._credentials = self._run_auth_flow()

            # トークンを保存
            self._save_credentials()

        return self._credentials

    def _run_auth_flow(self) -> Credentials:
        """OAuth2認証フローを実行"""
        if not self.client_secret_path.exists():
            raise FileNotFoundError(
                f"クライアントシークレットファイルが見つかりません: {self.client_secret_path}\n"
                "Google Cloud Consoleからダウンロードして配置してください。"
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            str(self.client_secret_path),
            self.scopes,
        )
        credentials = flow.run_local_server(port=0)
        return credentials

    def _save_credentials(self) -> None:
        """認証情報をファイルに保存"""
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.token_path, "wb") as token_file:
            pickle.dump(self._credentials, token_file)

    def get_youtube_service(self) -> Resource:
        """認証済みのYouTube APIサービスを取得"""
        credentials = self.get_credentials()
        return build("youtube", "v3", credentials=credentials)

    def revoke_credentials(self) -> bool:
        """認証情報を取り消し"""
        if self.token_path.exists():
            self.token_path.unlink()
            self._credentials = None
            return True
        return False


def get_authenticated_service() -> Resource:
    """認証済みYouTubeサービスを取得するヘルパー関数"""
    auth = YouTubeAuthenticator()
    return auth.get_youtube_service()
