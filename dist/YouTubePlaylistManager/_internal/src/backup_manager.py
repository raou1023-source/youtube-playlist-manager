"""バックアップ管理モジュール - 設定とデータのバックアップ・復元"""

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
from datetime import datetime
from pathlib import Path
from typing import Optional

from paths import CONFIG_PATH


class BackupManager:
    """バックアップの管理クラス"""

    def __init__(self):
        self.backup_dir = CONFIG_PATH / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, data: dict, backup_name: Optional[str] = None) -> Path:
        """バックアップファイルを作成

        Args:
            data: バックアップするデータ
            backup_name: バックアップ名（省略時は日時から自動生成）

        Returns:
            作成したバックアップファイルのパス
        """
        if backup_name is None:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        backup_file = self.backup_dir / f"{backup_name}.json"

        backup_data = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "data": data
        }

        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)

        return backup_file

    def restore_backup(self, backup_file: Path) -> dict:
        """バックアップから復元

        Args:
            backup_file: バックアップファイルのパス

        Returns:
            復元されたデータ
        """
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        return backup_data.get('data', {})

    def list_backups(self) -> list[dict]:
        """利用可能なバックアップ一覧を取得

        Returns:
            バックアップ情報のリスト（新しい順）
        """
        backups = []
        for file in self.backup_dir.glob('*.json'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                backups.append({
                    'filename': file.name,
                    'path': str(file),
                    'created_at': data.get('created_at', 'Unknown'),
                    'version': data.get('version', 'Unknown')
                })
            except (json.JSONDecodeError, IOError):
                pass

        return sorted(backups, key=lambda x: x['created_at'], reverse=True)

    def delete_backup(self, backup_path: str) -> bool:
        """バックアップを削除

        Args:
            backup_path: 削除するバックアップファイルのパス

        Returns:
            削除に成功した場合True
        """
        path = Path(backup_path)
        if path.exists():
            path.unlink()
            return True
        return False

    def get_backup_dir(self) -> Path:
        """バックアップディレクトリのパスを取得

        Returns:
            バックアップディレクトリのパス
        """
        return self.backup_dir
