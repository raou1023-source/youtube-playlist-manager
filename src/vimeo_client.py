"""Vimeo API クライアントモジュール"""

import json
import urllib.request
import urllib.parse
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Generator
import os


@dataclass
class VimeoVideoInfo:
    """Vimeo動画情報"""
    video_id: str
    title: str
    description: str
    channel_title: str  # user name
    channel_id: str  # user id
    published_at: str
    year: int
    duration: int  # seconds
    view_count: int
    like_count: int
    thumbnail_url: str
    url: str
    platform: str = "vimeo"

    def to_dict(self) -> dict:
        return {
            "video_id": self.video_id,
            "title": self.title,
            "description": self.description,
            "channel_title": self.channel_title,
            "channel_id": self.channel_id,
            "published_at": self.published_at,
            "year": self.year,
            "duration": self.duration,
            "view_count": self.view_count,
            "like_count": self.like_count,
            "thumbnail_url": self.thumbnail_url,
            "url": self.url,
            "platform": self.platform,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VimeoVideoInfo":
        return cls(
            video_id=data.get("video_id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            channel_title=data.get("channel_title", ""),
            channel_id=data.get("channel_id", ""),
            published_at=data.get("published_at", ""),
            year=data.get("year", 0),
            duration=data.get("duration", 0),
            view_count=data.get("view_count", 0),
            like_count=data.get("like_count", 0),
            thumbnail_url=data.get("thumbnail_url", ""),
            url=data.get("url", ""),
            platform=data.get("platform", "vimeo"),
        )


class VimeoClient:
    """Vimeo API クライアント

    Note:
        Vimeo APIを使用するには、アクセストークンが必要です。
        https://developer.vimeo.com/ でアプリを作成し、
        アクセストークンを取得してください。
    """

    BASE_URL = "https://api.vimeo.com"

    def __init__(self, access_token: Optional[str] = None):
        """
        Args:
            access_token: Vimeo APIアクセストークン
                          環境変数 VIMEO_ACCESS_TOKEN からも取得可能
        """
        self.access_token = access_token or os.getenv("VIMEO_ACCESS_TOKEN")
        if not self.access_token:
            print("警告: Vimeoアクセストークンが設定されていません")

    def _make_request(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """APIリクエストを実行"""
        if not self.access_token:
            return None

        url = f"{self.BASE_URL}{endpoint}"
        if params:
            url += "?" + urllib.parse.urlencode(params)

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/vnd.vimeo.*+json;version=3.4",
        }

        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"Vimeo API HTTPエラー: {e.code} - {e.reason}")
            return None
        except Exception as e:
            print(f"Vimeo API エラー: {e}")
            return None

    def _parse_video(self, video_data: dict) -> VimeoVideoInfo:
        """APIレスポンスからVideoInfoを作成"""
        # video_idを抽出 (/videos/123456789 -> 123456789)
        uri = video_data.get("uri", "")
        video_id = uri.split("/")[-1] if uri else ""

        # 公開日をパース
        created_time = video_data.get("created_time", "")
        try:
            dt = datetime.fromisoformat(created_time.replace("Z", "+00:00"))
            year = dt.year
            published_at = dt.isoformat()
        except (ValueError, AttributeError):
            year = 0
            published_at = created_time

        # ユーザー情報
        user = video_data.get("user", {})
        user_uri = user.get("uri", "")
        user_id = user_uri.split("/")[-1] if user_uri else ""

        # サムネイル
        pictures = video_data.get("pictures", {})
        sizes = pictures.get("sizes", [])
        thumbnail_url = sizes[-1].get("link", "") if sizes else ""

        # 統計情報
        stats = video_data.get("stats", {})

        return VimeoVideoInfo(
            video_id=video_id,
            title=video_data.get("name", ""),
            description=video_data.get("description", "") or "",
            channel_title=user.get("name", ""),
            channel_id=user_id,
            published_at=published_at,
            year=year,
            duration=video_data.get("duration", 0),
            view_count=stats.get("plays", 0) or 0,
            like_count=video_data.get("metadata", {}).get("connections", {}).get("likes", {}).get("total", 0),
            thumbnail_url=thumbnail_url,
            url=video_data.get("link", f"https://vimeo.com/{video_id}"),
        )

    def search_videos(
        self,
        query: str,
        max_results: int = 50,
        sort: str = "relevant",
        direction: str = "desc",
        filter_duration: Optional[str] = None,
    ) -> Generator[VimeoVideoInfo, None, None]:
        """動画を検索

        Args:
            query: 検索クエリ
            max_results: 最大結果数
            sort: ソート順 (relevant, date, alphabetical, plays, likes, comments, duration)
            direction: ソート方向 (asc, desc)
            filter_duration: 長さフィルタ (short, medium, long)

        Yields:
            VimeoVideoInfo
        """
        params = {
            "query": query,
            "per_page": min(max_results, 100),  # Vimeo APIの最大は100
            "sort": sort,
            "direction": direction,
        }

        if filter_duration:
            params["filter"] = f"duration.{filter_duration}"

        page = 1
        total_fetched = 0

        while total_fetched < max_results:
            params["page"] = page
            response = self._make_request("/videos", params)

            if not response:
                break

            videos = response.get("data", [])
            if not videos:
                break

            for video_data in videos:
                if total_fetched >= max_results:
                    break
                yield self._parse_video(video_data)
                total_fetched += 1

            # 次のページがあるか確認
            paging = response.get("paging", {})
            if not paging.get("next"):
                break

            page += 1

    def get_video(self, video_id: str) -> Optional[VimeoVideoInfo]:
        """動画IDから動画情報を取得"""
        response = self._make_request(f"/videos/{video_id}")
        if response:
            return self._parse_video(response)
        return None

    def get_user_videos(
        self,
        user_id: str,
        max_results: int = 50,
    ) -> Generator[VimeoVideoInfo, None, None]:
        """ユーザーの動画を取得"""
        params = {
            "per_page": min(max_results, 100),
        }

        page = 1
        total_fetched = 0

        while total_fetched < max_results:
            params["page"] = page
            response = self._make_request(f"/users/{user_id}/videos", params)

            if not response:
                break

            videos = response.get("data", [])
            if not videos:
                break

            for video_data in videos:
                if total_fetched >= max_results:
                    break
                yield self._parse_video(video_data)
                total_fetched += 1

            paging = response.get("paging", {})
            if not paging.get("next"):
                break

            page += 1

    def is_available(self) -> bool:
        """APIが利用可能かチェック"""
        return self.access_token is not None


# テスト用
if __name__ == "__main__":
    client = VimeoClient()
    if client.is_available():
        print("Vimeo API is available")
        for video in client.search_videos("music", max_results=5):
            print(f"- {video.title} ({video.url})")
    else:
        print("Vimeo API is not available (no access token)")
