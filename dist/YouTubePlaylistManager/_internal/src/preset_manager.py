"""プリセット管理モジュール - 検索条件の保存・読み込み"""

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
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from paths import PRESETS_FILE


@dataclass
class PresetSettings:
    """プリセットの設定内容"""
    era: str = "2020s"
    category: str = "music"
    keywords: list[str] = field(default_factory=list)
    additional_keyword: str = ""
    region_group: str = "全世界"
    country: str = "全世界"
    video_count: int = 20
    privacy: str = "private"
    prefer_official: bool = True
    search_precision: str = "standard"
    add_region_keywords: bool = True
    add_detailed_description: bool = True
    platforms: list[str] = field(default_factory=lambda: ["youtube"])


@dataclass
class Preset:
    """保存されたプリセット"""
    id: str
    name: str
    created_at: str
    settings: PresetSettings

    @classmethod
    def from_dict(cls, data: dict) -> "Preset":
        """辞書からPresetを作成"""
        settings_data = data.get("settings", {})
        settings = PresetSettings(
            era=settings_data.get("era", "2020s"),
            category=settings_data.get("category", "music"),
            keywords=settings_data.get("keywords", []),
            additional_keyword=settings_data.get("additional_keyword", ""),
            region_group=settings_data.get("region_group", "全世界"),
            country=settings_data.get("country", "全世界"),
            video_count=settings_data.get("video_count", 20),
            privacy=settings_data.get("privacy", "private"),
            prefer_official=settings_data.get("prefer_official", True),
            search_precision=settings_data.get("search_precision", "standard"),
            add_region_keywords=settings_data.get("add_region_keywords", True),
            add_detailed_description=settings_data.get("add_detailed_description", True),
            platforms=settings_data.get("platforms", ["youtube"]),
        )
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", "Untitled"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            settings=settings,
        )

    def to_dict(self) -> dict:
        """辞書に変換"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "settings": asdict(self.settings),
        }


class PresetManager:
    """プリセットの管理クラス"""

    DEFAULT_PATH = PRESETS_FILE

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or self.DEFAULT_PATH
        self._presets: list[Preset] = []
        self._load()

    def _load(self):
        """ファイルからプリセットを読み込む"""
        try:
            if self.file_path.exists():
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._presets = [
                        Preset.from_dict(p) for p in data.get("presets", [])
                    ]
        except (json.JSONDecodeError, IOError) as e:
            print(f"プリセット読み込みエラー: {e}")
            self._presets = []

    def _save(self):
        """プリセットをファイルに保存"""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"presets": [p.to_dict() for p in self._presets]},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
        except IOError as e:
            print(f"プリセット保存エラー: {e}")

    def get_all(self) -> list[Preset]:
        """すべてのプリセットを取得"""
        return self._presets.copy()

    def get_by_id(self, preset_id: str) -> Optional[Preset]:
        """IDでプリセットを取得"""
        for preset in self._presets:
            if preset.id == preset_id:
                return preset
        return None

    def get_by_name(self, name: str) -> Optional[Preset]:
        """名前でプリセットを取得"""
        for preset in self._presets:
            if preset.name == name:
                return preset
        return None

    def add(self, name: str, settings: PresetSettings) -> Preset:
        """新しいプリセットを追加"""
        preset = Preset(
            id=str(uuid.uuid4()),
            name=name,
            created_at=datetime.now().isoformat(),
            settings=settings,
        )
        self._presets.append(preset)
        self._save()
        return preset

    def update(self, preset_id: str, name: Optional[str] = None,
               settings: Optional[PresetSettings] = None) -> bool:
        """プリセットを更新"""
        for i, preset in enumerate(self._presets):
            if preset.id == preset_id:
                if name is not None:
                    self._presets[i].name = name
                if settings is not None:
                    self._presets[i].settings = settings
                self._save()
                return True
        return False

    def delete(self, preset_id: str) -> bool:
        """プリセットを削除"""
        for i, preset in enumerate(self._presets):
            if preset.id == preset_id:
                del self._presets[i]
                self._save()
                return True
        return False

    def get_preset_names(self) -> list[str]:
        """プリセット名のリストを取得"""
        return [p.name for p in self._presets]

    def export_to_file(self, file_path: Path) -> bool:
        """プリセットを別ファイルにエクスポート"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"presets": [p.to_dict() for p in self._presets]},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
            return True
        except IOError as e:
            print(f"エクスポートエラー: {e}")
            return False

    def import_from_file(self, file_path: Path, merge: bool = True) -> int:
        """別ファイルからプリセットをインポート

        Args:
            file_path: インポート元のファイルパス
            merge: Trueの場合は既存に追加、Falseの場合は置換

        Returns:
            インポートしたプリセット数
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                imported = [Preset.from_dict(p) for p in data.get("presets", [])]

            if merge:
                # 既存のIDと重複しないよう新しいIDを付与
                existing_ids = {p.id for p in self._presets}
                for preset in imported:
                    if preset.id in existing_ids:
                        preset.id = str(uuid.uuid4())
                    self._presets.append(preset)
            else:
                self._presets = imported

            self._save()
            return len(imported)
        except (json.JSONDecodeError, IOError) as e:
            print(f"インポートエラー: {e}")
            return 0
