"""統合プレイリスト管理モジュール - 複数プラットフォーム対応"""

import json
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
from html import escape


@dataclass
class IntegratedVideoItem:
    """統合プレイリストの動画アイテム"""
    id: str
    platform: str  # youtube, vimeo, niconico
    video_id: str
    title: str
    channel_title: str
    published_at: str
    year: int
    duration: int
    view_count: int
    thumbnail_url: str
    url: str
    added_at: str = ""

    def __post_init__(self):
        if not self.added_at:
            self.added_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "IntegratedVideoItem":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            platform=data.get("platform", "youtube"),
            video_id=data.get("video_id", ""),
            title=data.get("title", ""),
            channel_title=data.get("channel_title", ""),
            published_at=data.get("published_at", ""),
            year=data.get("year", 0),
            duration=data.get("duration", 0),
            view_count=data.get("view_count", 0),
            thumbnail_url=data.get("thumbnail_url", ""),
            url=data.get("url", ""),
            added_at=data.get("added_at", ""),
        )

    def get_platform_icon(self) -> str:
        """プラットフォームアイコンを取得"""
        icons = {
            "youtube": "▶️",
            "niconico": "📺",
        }
        return icons.get(self.platform, "🎵")

    def get_platform_display(self) -> str:
        """プラットフォーム表示名を取得"""
        names = {
            "youtube": "YouTube",
            "niconico": "ニコニコ動画",
        }
        return names.get(self.platform, self.platform)

    def format_duration(self) -> str:
        """再生時間をフォーマット"""
        if self.duration <= 0:
            return ""
        minutes = self.duration // 60
        seconds = self.duration % 60
        if minutes >= 60:
            hours = minutes // 60
            minutes = minutes % 60
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"


@dataclass
class IntegratedPlaylist:
    """統合プレイリスト"""
    id: str
    title: str
    description: str
    created_at: str
    updated_at: str
    items: list[IntegratedVideoItem] = field(default_factory=list)
    # 各プラットフォームのプレイリストID（作成された場合）
    youtube_playlist_id: str = ""
    youtube_playlist_url: str = ""
    # ニコニコはマイリストID
    niconico_mylist_id: str = ""
    niconico_mylist_url: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "items": [item.to_dict() for item in self.items],
            "youtube_playlist_id": self.youtube_playlist_id,
            "youtube_playlist_url": self.youtube_playlist_url,
            "niconico_mylist_id": self.niconico_mylist_id,
            "niconico_mylist_url": self.niconico_mylist_url,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "IntegratedPlaylist":
        items = [IntegratedVideoItem.from_dict(item) for item in data.get("items", [])]
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", "Untitled"),
            description=data.get("description", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            items=items,
            youtube_playlist_id=data.get("youtube_playlist_id", ""),
            youtube_playlist_url=data.get("youtube_playlist_url", ""),
            niconico_mylist_id=data.get("niconico_mylist_id", ""),
            niconico_mylist_url=data.get("niconico_mylist_url", ""),
        )

    def add_item(self, item: IntegratedVideoItem):
        """アイテムを追加"""
        self.items.append(item)
        self.updated_at = datetime.now().isoformat()

    def remove_item(self, item_id: str) -> bool:
        """アイテムを削除"""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                self.updated_at = datetime.now().isoformat()
                return True
        return False

    def get_items_by_platform(self, platform: str) -> list[IntegratedVideoItem]:
        """プラットフォーム別にアイテムを取得"""
        return [item for item in self.items if item.platform == platform]

    def get_platform_counts(self) -> dict[str, int]:
        """プラットフォーム別の動画数を取得"""
        counts = {}
        for item in self.items:
            counts[item.platform] = counts.get(item.platform, 0) + 1
        return counts

    def get_formatted_date(self) -> str:
        """フォーマットされた作成日時を取得"""
        try:
            dt = datetime.fromisoformat(self.created_at)
            return dt.strftime("%Y/%m/%d %H:%M")
        except ValueError:
            return self.created_at


class IntegratedPlaylistManager:
    """統合プレイリストの管理クラス"""

    DEFAULT_PATH = Path(__file__).parent.parent / "config" / "integrated_playlists.json"

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or self.DEFAULT_PATH
        self._playlists: list[IntegratedPlaylist] = []
        self._load()

    def _load(self):
        """ファイルからプレイリストを読み込む"""
        try:
            if self.file_path.exists():
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._playlists = [
                        IntegratedPlaylist.from_dict(p) for p in data.get("playlists", [])
                    ]
        except (json.JSONDecodeError, IOError) as e:
            print(f"統合プレイリスト読み込みエラー: {e}")
            self._playlists = []

    def _save(self):
        """プレイリストをファイルに保存"""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"playlists": [p.to_dict() for p in self._playlists]},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
        except IOError as e:
            print(f"統合プレイリスト保存エラー: {e}")

    def create(self, title: str, description: str = "") -> IntegratedPlaylist:
        """新しい統合プレイリストを作成"""
        playlist = IntegratedPlaylist(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            created_at="",
            updated_at="",
        )
        self._playlists.append(playlist)
        self._save()
        return playlist

    def get_all(self) -> list[IntegratedPlaylist]:
        """すべてのプレイリストを取得"""
        return sorted(
            self._playlists,
            key=lambda p: p.updated_at,
            reverse=True,
        )

    def get_by_id(self, playlist_id: str) -> Optional[IntegratedPlaylist]:
        """IDでプレイリストを取得"""
        for playlist in self._playlists:
            if playlist.id == playlist_id:
                return playlist
        return None

    def update(self, playlist: IntegratedPlaylist):
        """プレイリストを更新"""
        for i, p in enumerate(self._playlists):
            if p.id == playlist.id:
                playlist.updated_at = datetime.now().isoformat()
                self._playlists[i] = playlist
                self._save()
                return

    def delete(self, playlist_id: str) -> bool:
        """プレイリストを削除"""
        for i, playlist in enumerate(self._playlists):
            if playlist.id == playlist_id:
                del self._playlists[i]
                self._save()
                return True
        return False

    def add_video_to_playlist(
        self,
        playlist_id: str,
        video_item: IntegratedVideoItem,
    ) -> bool:
        """プレイリストに動画を追加"""
        playlist = self.get_by_id(playlist_id)
        if playlist:
            playlist.add_item(video_item)
            self.update(playlist)
            return True
        return False

    def export_to_json(self, playlist_id: str, file_path: Path) -> bool:
        """プレイリストをJSON形式でエクスポート"""
        playlist = self.get_by_id(playlist_id)
        if not playlist:
            return False

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(playlist.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"エクスポートエラー: {e}")
            return False

    def export_to_html(self, playlist_id: str, file_path: Path) -> bool:
        """プレイリストをHTML形式でエクスポート"""
        playlist = self.get_by_id(playlist_id)
        if not playlist:
            return False

        try:
            html_content = self._generate_html(playlist)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            return True
        except IOError as e:
            print(f"HTMLエクスポートエラー: {e}")
            return False

    def _generate_filter_buttons(self, platform_counts: dict) -> str:
        """フィルターボタンのHTMLを生成"""
        buttons = []
        sq = "'"  # シングルクォートを変数に格納
        for p in platform_counts.keys():
            item = IntegratedVideoItem(
                id="", platform=p, video_id="", title="", channel_title="",
                published_at="", year=0, duration=0, view_count=0,
                thumbnail_url="", url=""
            )
            icon = item.get_platform_icon()
            display = item.get_platform_display()
            buttons.append(f'<button class="filter-btn" onclick="filterVideos({sq}{p}{sq})">{icon} {display}</button>')
        return "".join(buttons)

    def _generate_html(self, playlist: IntegratedPlaylist) -> str:
        """プレイリストのHTMLを生成"""
        platform_counts = playlist.get_platform_counts()

        items_html = ""
        for item in playlist.items:
            items_html += f"""
            <div class="video-item" data-platform="{item.platform}">
                <div class="thumbnail">
                    <a href="{escape(item.url)}" target="_blank">
                        <img src="{escape(item.thumbnail_url)}" alt="{escape(item.title)}"
                             onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22120%22 height=%2268%22><rect fill=%22%23ccc%22 width=%22120%22 height=%2268%22/><text x=%2260%22 y=%2234%22 text-anchor=%22middle%22 fill=%22%23666%22>No Image</text></svg>'">
                        <span class="play-button">▶</span>
                    </a>
                </div>
                <div class="video-info">
                    <h3><a href="{escape(item.url)}" target="_blank">{escape(item.title)}</a></h3>
                    <p class="channel">{item.get_platform_icon()} {item.get_platform_display()} | {escape(item.channel_title)}</p>
                    <p class="meta">
                        {f'{item.year}年' if item.year else ''}
                        {f'| {item.format_duration()}' if item.duration else ''}
                        {f'| {item.view_count:,}回視聴' if item.view_count else ''}
                    </p>
                </div>
            </div>
            """

        # プラットフォーム別リンク
        platform_links = ""
        if playlist.youtube_playlist_url:
            platform_links += f'<a href="{escape(playlist.youtube_playlist_url)}" target="_blank" class="platform-link youtube">▶️ YouTube</a>'
        if playlist.niconico_mylist_url:
            platform_links += f'<a href="{escape(playlist.niconico_mylist_url)}" target="_blank" class="platform-link niconico">📺 ニコニコ</a>'

        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(playlist.title)} - 統合プレイリスト</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        header h1 {{ margin: 0 0 10px 0; }}
        header p {{ margin: 5px 0; opacity: 0.9; }}
        .stats {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }}
        .stat {{
            background: rgba(255,255,255,0.2);
            padding: 8px 15px;
            border-radius: 5px;
        }}
        .platform-links {{
            margin: 20px 0;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .platform-link {{
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            color: white;
            font-weight: bold;
        }}
        .platform-link.youtube {{ background: #ff0000; }}
        .platform-link.niconico {{ background: #252525; }}
        .filters {{
            margin: 20px 0;
            display: flex;
            gap: 10px;
        }}
        .filter-btn {{
            padding: 8px 16px;
            border: 2px solid #667eea;
            background: white;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: #667eea;
            color: white;
        }}
        .video-list {{
            display: grid;
            gap: 15px;
        }}
        .video-item {{
            display: flex;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .video-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }}
        .video-item.hidden {{ display: none; }}
        .thumbnail {{
            width: 180px;
            height: 101px;
            flex-shrink: 0;
            position: relative;
            overflow: hidden;
            background: #000;
        }}
        .thumbnail img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .thumbnail .play-button {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            color: white;
            text-shadow: 0 0 10px rgba(0,0,0,0.5);
            opacity: 0;
            transition: opacity 0.3s;
        }}
        .thumbnail:hover .play-button {{ opacity: 1; }}
        .video-info {{
            padding: 15px;
            flex: 1;
            overflow: hidden;
        }}
        .video-info h3 {{
            margin: 0 0 8px 0;
            font-size: 16px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .video-info h3 a {{
            color: #333;
            text-decoration: none;
        }}
        .video-info h3 a:hover {{ color: #667eea; }}
        .video-info .channel {{
            margin: 0 0 5px 0;
            color: #666;
            font-size: 13px;
        }}
        .video-info .meta {{
            margin: 0;
            color: #999;
            font-size: 12px;
        }}
        footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 12px;
        }}
        @media (max-width: 600px) {{
            .video-item {{ flex-direction: column; }}
            .thumbnail {{ width: 100%; height: 200px; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>{escape(playlist.title)}</h1>
        <p>{escape(playlist.description)}</p>
        <p>作成日: {playlist.get_formatted_date()}</p>
        <div class="stats">
            <span class="stat">合計: {len(playlist.items)}本</span>
            {"".join(f'<span class="stat">{IntegratedVideoItem(id="",platform=p,video_id="",title="",channel_title="",published_at="",year=0,duration=0,view_count=0,thumbnail_url="",url="").get_platform_display()}: {c}本</span>' for p, c in platform_counts.items())}
        </div>
    </header>

    {f'<div class="platform-links">{platform_links}</div>' if platform_links else ''}

    <div class="filters">
        <button class="filter-btn active" onclick="filterVideos('all')">すべて</button>
        {self._generate_filter_buttons(platform_counts)}
    </div>

    <div class="video-list">
        {items_html}
    </div>

    <footer>
        Generated by YouTube Playlist Manager
    </footer>

    <script>
        function filterVideos(platform) {{
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            document.querySelectorAll('.video-item').forEach(item => {{
                if (platform === 'all' || item.dataset.platform === platform) {{
                    item.classList.remove('hidden');
                }} else {{
                    item.classList.add('hidden');
                }}
            }});
        }}
    </script>
</body>
</html>"""
        return html

    def import_from_json(self, file_path: Path) -> Optional[IntegratedPlaylist]:
        """JSONファイルからプレイリストをインポート"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            playlist = IntegratedPlaylist.from_dict(data)
            playlist.id = str(uuid.uuid4())  # 新しいIDを付与
            self._playlists.append(playlist)
            self._save()
            return playlist
        except (json.JSONDecodeError, IOError) as e:
            print(f"インポートエラー: {e}")
            return None


# VideoInfoから統合アイテムを作成するヘルパー関数
def create_integrated_item_from_youtube(video_info) -> IntegratedVideoItem:
    """YouTubeのVideoInfoから統合アイテムを作成"""
    return IntegratedVideoItem(
        id=str(uuid.uuid4()),
        platform="youtube",
        video_id=video_info.video_id,
        title=video_info.title,
        channel_title=video_info.channel_title,
        published_at=video_info.published_at if hasattr(video_info, 'published_at') else "",
        year=video_info.year,
        duration=getattr(video_info, 'duration', 0),
        view_count=getattr(video_info, 'view_count', 0),
        thumbnail_url=getattr(video_info, 'thumbnail_url', f"https://img.youtube.com/vi/{video_info.video_id}/mqdefault.jpg"),
        url=f"https://www.youtube.com/watch?v={video_info.video_id}",
    )


def create_integrated_item_from_niconico(video_info) -> IntegratedVideoItem:
    """ニコニコ動画のVideoInfoから統合アイテムを作成"""
    return IntegratedVideoItem(
        id=str(uuid.uuid4()),
        platform="niconico",
        video_id=video_info.video_id,
        title=video_info.title,
        channel_title=video_info.channel_title,
        published_at=video_info.published_at,
        year=video_info.year,
        duration=video_info.duration,
        view_count=video_info.view_count,
        thumbnail_url=video_info.thumbnail_url,
        url=video_info.url,
    )
