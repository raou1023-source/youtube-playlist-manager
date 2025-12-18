"""
オンライン更新チェッカー

アプリケーションの更新を確認し、新しいバージョンが利用可能な場合に
ユーザーに通知する機能を提供します。
"""

import requests
import webbrowser
from packaging import version

# 現在のバージョン
CURRENT_VERSION = "1.0.0"

# バージョン情報を取得するURL
# 注意: USERNAME/REPO を実際のGitHubリポジトリに置き換えてください
VERSION_CHECK_URL = "https://github.com/raou1023-source/youtube-playlist-manager.git"


class UpdateChecker:
    """アプリケーションの更新をチェックするクラス"""

    @staticmethod
    def check_for_updates() -> dict:
        """新しいバージョンが利用可能か確認する

        Returns:
            dict: 更新情報を含む辞書
                - update_available: 更新が利用可能かどうか
                - current_version: 現在のバージョン
                - latest_version: 最新バージョン（更新がある場合）
                - download_url: ダウンロードURL（更新がある場合）
                - release_notes: リリースノート（更新がある場合）
                - error: エラーメッセージ（エラーがある場合）
        """
        try:
            response = requests.get(VERSION_CHECK_URL, timeout=5)
            response.raise_for_status()
            data = response.json()

            latest_version = data["version"]
            download_url = data["download_url"]
            release_notes = data.get("release_notes", "")

            if version.parse(latest_version) > version.parse(CURRENT_VERSION):
                return {
                    "update_available": True,
                    "current_version": CURRENT_VERSION,
                    "latest_version": latest_version,
                    "download_url": download_url,
                    "release_notes": release_notes
                }
            return {
                "update_available": False,
                "current_version": CURRENT_VERSION
            }
        except requests.exceptions.Timeout:
            return {
                "update_available": False,
                "error": "サーバーへの接続がタイムアウトしました"
            }
        except requests.exceptions.ConnectionError:
            return {
                "update_available": False,
                "error": "インターネット接続を確認してください"
            }
        except requests.exceptions.HTTPError as e:
            return {
                "update_available": False,
                "error": f"サーバーエラー: {e.response.status_code}"
            }
        except Exception as e:
            return {
                "update_available": False,
                "error": str(e)
            }

    @staticmethod
    def download_update(url: str) -> bool:
        """ダウンロードURLをブラウザで開く

        Args:
            url: ダウンロードURL

        Returns:
            bool: 成功した場合True
        """
        try:
            webbrowser.open(url)
            return True
        except Exception:
            return False
