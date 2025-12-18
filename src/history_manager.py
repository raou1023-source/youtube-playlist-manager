"""履歴管理モジュール - 作成した再生リストの記録"""

import sys
import os

# 親ディレクトリをパスに追加（通常のPython実行用）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import csv
import json
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from paths import HISTORY_FILE


@dataclass
class SearchConditions:
    """検索条件"""
    era: str = ""
    category: str = ""
    keywords: list[str] = field(default_factory=list)
    additional_keyword: str = ""
    region_group: str = "全世界"
    country: str = "全世界"
    video_count: int = 0
    privacy: str = "private"
    prefer_official: bool = True
    search_precision: str = "standard"
    platforms: list[str] = field(default_factory=lambda: ["youtube"])


@dataclass
class HistoryEntry:
    """履歴エントリー"""
    id: str
    title: str
    url: str
    playlist_id: str
    created_at: str
    video_count: int
    conditions: SearchConditions
    platform: str = "youtube"  # youtube, vimeo, niconico, integrated

    @classmethod
    def from_dict(cls, data: dict) -> "HistoryEntry":
        """辞書からHistoryEntryを作成"""
        conditions_data = data.get("conditions", {})
        conditions = SearchConditions(
            era=conditions_data.get("era", ""),
            category=conditions_data.get("category", ""),
            keywords=conditions_data.get("keywords", []),
            additional_keyword=conditions_data.get("additional_keyword", ""),
            region_group=conditions_data.get("region_group", "全世界"),
            country=conditions_data.get("country", "全世界"),
            video_count=conditions_data.get("video_count", 0),
            privacy=conditions_data.get("privacy", "private"),
            prefer_official=conditions_data.get("prefer_official", True),
            search_precision=conditions_data.get("search_precision", "standard"),
            platforms=conditions_data.get("platforms", ["youtube"]),
        )
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", ""),
            url=data.get("url", ""),
            playlist_id=data.get("playlist_id", ""),
            created_at=data.get("created_at", datetime.now().isoformat()),
            video_count=data.get("video_count", 0),
            conditions=conditions,
            platform=data.get("platform", "youtube"),
        )

    def to_dict(self) -> dict:
        """辞書に変換"""
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "playlist_id": self.playlist_id,
            "created_at": self.created_at,
            "video_count": self.video_count,
            "conditions": asdict(self.conditions),
            "platform": self.platform,
        }

    def get_formatted_date(self) -> str:
        """フォーマットされた日付を取得"""
        try:
            dt = datetime.fromisoformat(self.created_at)
            return dt.strftime("%Y/%m/%d %H:%M")
        except ValueError:
            return self.created_at

    def get_platform_display(self) -> str:
        """プラットフォーム表示名を取得"""
        platform_names = {
            "youtube": "YouTube",
            "vimeo": "Vimeo",
            "niconico": "ニコニコ動画",
            "integrated": "統合",
        }
        return platform_names.get(self.platform, self.platform)


class HistoryManager:
    """履歴の管理クラス"""

    DEFAULT_PATH = HISTORY_FILE
    MAX_ENTRIES = 100  # 最大履歴数

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or self.DEFAULT_PATH
        self._history: list[HistoryEntry] = []
        self._load()

    def _load(self):
        """ファイルから履歴を読み込む"""
        try:
            if self.file_path.exists():
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._history = [
                        HistoryEntry.from_dict(h) for h in data.get("history", [])
                    ]
        except (json.JSONDecodeError, IOError) as e:
            print(f"履歴読み込みエラー: {e}")
            self._history = []

    def _save(self):
        """履歴をファイルに保存"""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"history": [h.to_dict() for h in self._history]},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
        except IOError as e:
            print(f"履歴保存エラー: {e}")

    def get_all(self) -> list[HistoryEntry]:
        """すべての履歴を取得（新しい順）"""
        return sorted(
            self._history,
            key=lambda h: h.created_at,
            reverse=True,
        )

    def get_by_id(self, entry_id: str) -> Optional[HistoryEntry]:
        """IDで履歴を取得"""
        for entry in self._history:
            if entry.id == entry_id:
                return entry
        return None

    def add(
        self,
        title: str,
        url: str,
        playlist_id: str,
        video_count: int,
        conditions: SearchConditions,
        platform: str = "youtube",
    ) -> HistoryEntry:
        """新しい履歴を追加"""
        entry = HistoryEntry(
            id=str(uuid.uuid4()),
            title=title,
            url=url,
            playlist_id=playlist_id,
            created_at=datetime.now().isoformat(),
            video_count=video_count,
            conditions=conditions,
            platform=platform,
        )
        self._history.append(entry)

        # 最大数を超えた場合、古いものを削除
        if len(self._history) > self.MAX_ENTRIES:
            self._history = sorted(
                self._history,
                key=lambda h: h.created_at,
                reverse=True,
            )[:self.MAX_ENTRIES]

        self._save()
        return entry

    def delete(self, entry_id: str) -> bool:
        """履歴を削除"""
        for i, entry in enumerate(self._history):
            if entry.id == entry_id:
                del self._history[i]
                self._save()
                return True
        return False

    def clear_all(self) -> int:
        """すべての履歴を削除"""
        count = len(self._history)
        self._history = []
        self._save()
        return count

    def search(self, keyword: str) -> list[HistoryEntry]:
        """キーワードで履歴を検索"""
        keyword_lower = keyword.lower()
        results = []
        for entry in self._history:
            if (keyword_lower in entry.title.lower() or
                keyword_lower in entry.conditions.category.lower() or
                any(keyword_lower in kw.lower() for kw in entry.conditions.keywords)):
                results.append(entry)
        return sorted(results, key=lambda h: h.created_at, reverse=True)

    def export_to_file(self, file_path: Path) -> bool:
        """履歴を別ファイルにエクスポート"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"history": [h.to_dict() for h in self._history]},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
            return True
        except IOError as e:
            print(f"エクスポートエラー: {e}")
            return False

    def import_from_file(self, file_path: Path, merge: bool = True) -> int:
        """別ファイルから履歴をインポート

        Args:
            file_path: インポート元のファイルパス
            merge: Trueの場合は既存に追加、Falseの場合は置換

        Returns:
            インポートした履歴数
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                imported = [HistoryEntry.from_dict(h) for h in data.get("history", [])]

            if merge:
                # 既存のIDと重複しないよう新しいIDを付与
                existing_ids = {h.id for h in self._history}
                for entry in imported:
                    if entry.id in existing_ids:
                        entry.id = str(uuid.uuid4())
                    self._history.append(entry)
            else:
                self._history = imported

            self._save()
            return len(imported)
        except (json.JSONDecodeError, IOError) as e:
            print(f"インポートエラー: {e}")
            return 0

    def get_recent(self, count: int = 10) -> list[HistoryEntry]:
        """最近の履歴を取得"""
        return self.get_all()[:count]

    def get_by_category(self, category: str) -> list[HistoryEntry]:
        """カテゴリで履歴をフィルタ"""
        return [
            h for h in self.get_all()
            if h.conditions.category.lower() == category.lower()
        ]

    def get_by_platform(self, platform: str) -> list[HistoryEntry]:
        """プラットフォームで履歴をフィルタ"""
        return [
            h for h in self.get_all()
            if h.platform.lower() == platform.lower()
        ]

    def export_to_csv(self, file_path: Path) -> bool:
        """履歴をCSV形式でエクスポート

        Args:
            file_path: エクスポート先のファイルパス

        Returns:
            成功した場合True
        """
        try:
            with open(file_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                # ヘッダー
                writer.writerow([
                    "作成日時",
                    "タイトル",
                    "URL",
                    "動画数",
                    "プラットフォーム",
                    "年代",
                    "カテゴリ",
                    "キーワード",
                    "地域",
                    "国",
                ])
                # データ
                for entry in self.get_all():
                    writer.writerow([
                        entry.get_formatted_date(),
                        entry.title,
                        entry.url,
                        entry.video_count,
                        entry.get_platform_display(),
                        entry.conditions.era,
                        entry.conditions.category,
                        ", ".join(entry.conditions.keywords),
                        entry.conditions.region_group,
                        entry.conditions.country,
                    ])
            return True
        except IOError as e:
            print(f"CSVエクスポートエラー: {e}")
            return False
