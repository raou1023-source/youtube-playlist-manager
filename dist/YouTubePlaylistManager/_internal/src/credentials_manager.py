"""認証情報管理モジュール - Vimeo/ニコニコ動画の認証情報を安全に管理"""

import sys
import os

# 親ディレクトリをパスに追加（通常のPython実行用）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import json
import base64
import hashlib
import platform
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

# パス管理モジュールからインポート
from paths import (
    CONFIG_PATH as CONFIG_DIR,
    NICONICO_AUTH_FILE,
)

AUTH_STATUS_FILE = CONFIG_DIR / "auth_status.json"


class CredentialsManager:
    """認証情報を暗号化して管理するクラス"""

    def __init__(self):
        """初期化"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self._key: Optional[bytes] = None

    def _get_machine_id(self) -> str:
        """マシン固有のIDを取得（暗号化キー生成用）"""
        # ユーザー名とマシン名から固有IDを生成
        user = os.getenv("USERNAME") or os.getenv("USER") or "default"
        machine = platform.node()
        unique_str = f"{user}:{machine}:youtube-playlist-manager"
        return unique_str

    def _derive_key(self) -> bytes:
        """ユーザー固有の暗号化キーを生成"""
        if self._key is not None:
            return self._key

        if not CRYPTOGRAPHY_AVAILABLE:
            # cryptographyがない場合は簡易的なキーを生成
            machine_id = self._get_machine_id()
            key = hashlib.sha256(machine_id.encode()).digest()
            self._key = base64.urlsafe_b64encode(key)
            return self._key

        # cryptographyを使用した安全なキー導出
        machine_id = self._get_machine_id()
        salt = b'youtube-playlist-manager-salt-v1'

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(machine_id.encode()))
        self._key = key
        return self._key

    def encrypt(self, data: str) -> str:
        """文字列を暗号化"""
        if not CRYPTOGRAPHY_AVAILABLE:
            # cryptographyがない場合はBase64エンコードのみ（非推奨）
            return base64.b64encode(data.encode()).decode()

        key = self._derive_key()
        f = Fernet(key)
        encrypted = f.encrypt(data.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_data: str) -> str:
        """暗号化された文字列を復号"""
        if not CRYPTOGRAPHY_AVAILABLE:
            # cryptographyがない場合はBase64デコードのみ
            return base64.b64decode(encrypted_data.encode()).decode()

        key = self._derive_key()
        f = Fernet(key)
        decrypted = f.decrypt(encrypted_data.encode())
        return decrypted.decode()

    # ========================================
    # 認証状態管理
    # ========================================
    def get_auth_status(self) -> Dict[str, bool]:
        """認証状態を取得"""
        default_status = {
            "youtube": False,
            "niconico": False
        }

        if not AUTH_STATUS_FILE.exists():
            return default_status

        try:
            with open(AUTH_STATUS_FILE, "r", encoding="utf-8") as f:
                status = json.load(f)
                # デフォルト値とマージ
                for key in default_status:
                    if key not in status:
                        status[key] = False
                return status
        except (json.JSONDecodeError, IOError):
            return default_status

    def update_auth_status(self, platform: str, authenticated: bool):
        """認証状態を更新"""
        status = self.get_auth_status()
        status[platform] = authenticated

        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(AUTH_STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2)

    def check_and_update_all_status(self):
        """すべてのプラットフォームの認証状態をチェックして更新"""
        from setup_wizard import SetupStatus

        # YouTube
        youtube_status = SetupStatus.has_token()
        self.update_auth_status("youtube", youtube_status)

        # ニコニコ動画
        niconico_status = self.has_niconico_credentials()
        self.update_auth_status("niconico", niconico_status)

        return self.get_auth_status()

    # ========================================
    # ニコニコ動画認証情報管理
    # ========================================
    def save_niconico_credentials(self, email: str, password: str) -> bool:
        """ニコニコ動画の認証情報を暗号化して保存"""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)

            # パスワードを暗号化
            encrypted_password = self.encrypt(password)

            credentials = {
                "email": email,
                "password": encrypted_password,
                "encrypted": True,
                "created_at": datetime.now().isoformat(),  # ISO形式の文字列に変換
            }

            with open(NICONICO_AUTH_FILE, "w", encoding="utf-8") as f:
                json.dump(credentials, f, indent=2, ensure_ascii=False)

            self.update_auth_status("niconico", True)
            return True
        except Exception as e:
            print(f"ニコニコ動画認証保存エラー: {e}")
            return False

    def get_niconico_credentials(self) -> Optional[Dict[str, str]]:
        """ニコニコ動画の認証情報を取得（復号化済み）"""
        if not NICONICO_AUTH_FILE.exists():
            return None

        try:
            with open(NICONICO_AUTH_FILE, "r", encoding="utf-8") as f:
                credentials = json.load(f)

            email = credentials.get("email", "")
            encrypted_password = credentials.get("password", "")

            if not email or not encrypted_password:
                return None

            # パスワードを復号
            if credentials.get("encrypted", False):
                password = self.decrypt(encrypted_password)
            else:
                password = encrypted_password

            return {
                "email": email,
                "password": password
            }
        except Exception:
            return None

    def has_niconico_credentials(self) -> bool:
        """ニコニコ動画の認証情報が設定されているか確認"""
        return self.get_niconico_credentials() is not None

    def delete_niconico_credentials(self) -> bool:
        """ニコニコ動画の認証情報を削除"""
        try:
            if NICONICO_AUTH_FILE.exists():
                NICONICO_AUTH_FILE.unlink()
            self.update_auth_status("niconico", False)
            return True
        except IOError:
            return False

    # ========================================
    # ユーティリティ
    # ========================================
    def get_status_display(self) -> str:
        """ステータスバー用の表示文字列を生成"""
        status = self.check_and_update_all_status()

        parts = []
        platform_names = {
            "youtube": "YouTube",
            "niconico": "ニコニコ動画"
        }

        for platform, name in platform_names.items():
            if status.get(platform, False):
                parts.append(f"✓ {name}")
            else:
                parts.append(f"✗ {name}")

        return " | ".join(parts)


# グローバルインスタンス
_credentials_manager: Optional[CredentialsManager] = None


def get_credentials_manager() -> CredentialsManager:
    """CredentialsManagerのシングルトンインスタンスを取得"""
    global _credentials_manager
    if _credentials_manager is None:
        _credentials_manager = CredentialsManager()
    return _credentials_manager
