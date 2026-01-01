"""YouTube APIクライアントモジュール"""

import sys
import os

# 親ディレクトリをパスに追加（通常のPython実行用）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Iterator
from enum import Enum
from googleapiclient.discovery import Resource

from auth import get_authenticated_service
from config import (
    get_official_channel_ids,
    is_official_channel_by_id,
    is_official_channel,
    get_official_channel_score,
    ALL_OFFICIAL_CHANNEL_IDS,
)


class SearchPrecision(Enum):
    """検索精度レベル"""
    STANDARD = "standard"        # 通常の検索 + 公式優先
    HIGH = "high"                # 登録済み公式チャンネルのみから検索
    HIGHEST = "highest"          # チャンネルIDリストから直接検索


@dataclass
class ChannelInfo:
    """チャンネル情報を格納するデータクラス"""
    channel_id: str
    title: str
    description: str
    subscriber_count: Optional[int] = None
    video_count: Optional[int] = None
    view_count: Optional[int] = None
    is_verified: bool = False
    custom_url: Optional[str] = None


@dataclass
class VideoInfo:
    """動画情報を格納するデータクラス"""
    video_id: str
    title: str
    description: str
    published_at: datetime
    channel_id: str
    channel_title: str
    category_id: Optional[int] = None
    tags: Optional[list[str]] = None
    # 追加フィールド（品質スコアリング用）
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    subscriber_count: Optional[int] = None
    is_verified: bool = False
    quality_score: int = 0

    @property
    def year(self) -> int:
        """公開年を取得"""
        return self.published_at.year

    def calculate_quality_score(self) -> int:
        """品質スコアを計算

        スコアリング基準:
        - 公式チャンネル（IDベース）: +100点
        - 公式チャンネル（名前ベース）: +50点
        - 認証済み: +50点
        - 登録者100万人以上: +30点
        - 登録者10万人以上: +15点
        - 視聴回数100万回以上: +20点
        - 視聴回数10万回以上: +10点

        Returns:
            品質スコア（0-250）
        """
        score = 0

        # 公式チャンネルID判定（最高スコア）
        if is_official_channel_by_id(self.channel_id):
            score += 100

        # 公式チャンネル名判定
        if is_official_channel(self.channel_title):
            score += 50

        # タイトル・チャンネル名ベースの公式スコア
        name_score = get_official_channel_score(self.channel_title, self.title)
        score += name_score // 2  # 重複を避けるため半分

        # 認証済みチャンネル
        if self.is_verified:
            score += 50

        # 登録者数
        if self.subscriber_count:
            if self.subscriber_count >= 1_000_000:
                score += 30
            elif self.subscriber_count >= 100_000:
                score += 15

        # 視聴回数
        if self.view_count:
            if self.view_count >= 1_000_000:
                score += 20
            elif self.view_count >= 100_000:
                score += 10

        self.quality_score = min(score, 250)
        return self.quality_score


@dataclass
class PlaylistInfo:
    """再生リスト情報を格納するデータクラス"""
    playlist_id: str
    title: str
    description: str
    item_count: int


class YouTubeClient:
    """YouTube Data API v3のラッパークラス"""

    def __init__(self, service: Optional[Resource] = None):
        self._service = service

    @property
    def service(self) -> Resource:
        """遅延初期化されたYouTubeサービスを取得"""
        if self._service is None:
            self._service = get_authenticated_service()
        return self._service

    def get_liked_videos(self, max_results: int = 50) -> Iterator[VideoInfo]:
        """高く評価した動画を取得"""
        return self._get_playlist_videos("LL", max_results)

    def get_watch_later_videos(self, max_results: int = 50) -> Iterator[VideoInfo]:
        """後で見る動画を取得"""
        return self._get_playlist_videos("WL", max_results)

    def get_playlist_videos(self, playlist_id: str, max_results: int = 50) -> Iterator[VideoInfo]:
        """指定した再生リストの動画を取得"""
        return self._get_playlist_videos(playlist_id, max_results)

    def _get_playlist_videos(self, playlist_id: str, max_results: int) -> Iterator[VideoInfo]:
        """再生リストから動画を取得するジェネレータ"""
        next_page_token = None
        fetched_count = 0

        while fetched_count < max_results:
            request = self.service.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=min(50, max_results - fetched_count),
                pageToken=next_page_token,
            )
            response = request.execute()

            video_ids = [
                item["contentDetails"]["videoId"]
                for item in response.get("items", [])
            ]

            if video_ids:
                videos_details = self._get_videos_details(video_ids)
                for video in videos_details:
                    yield video
                    fetched_count += 1
                    if fetched_count >= max_results:
                        break

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    def _get_videos_details(
        self,
        video_ids: list[str],
        include_statistics: bool = False
    ) -> list[VideoInfo]:
        """複数の動画IDから詳細情報を取得

        Args:
            video_ids: 動画IDのリスト
            include_statistics: 統計情報（視聴回数など）を含めるか

        Returns:
            VideoInfoのリスト
        """
        parts = ["snippet"]
        if include_statistics:
            parts.append("statistics")

        request = self.service.videos().list(
            part=",".join(parts),
            id=",".join(video_ids),
        )
        response = request.execute()

        videos = []
        for item in response.get("items", []):
            snippet = item["snippet"]
            published_at = datetime.fromisoformat(
                snippet["publishedAt"].replace("Z", "+00:00")
            )

            # 統計情報を取得
            view_count = None
            like_count = None
            if include_statistics and "statistics" in item:
                stats = item["statistics"]
                view_count = int(stats.get("viewCount", 0)) if stats.get("viewCount") else None
                like_count = int(stats.get("likeCount", 0)) if stats.get("likeCount") else None

            videos.append(VideoInfo(
                video_id=item["id"],
                title=snippet["title"],
                description=snippet.get("description", ""),
                published_at=published_at,
                channel_id=snippet["channelId"],
                channel_title=snippet["channelTitle"],
                category_id=int(snippet.get("categoryId")) if snippet.get("categoryId") else None,
                tags=snippet.get("tags"),
                view_count=view_count,
                like_count=like_count,
            ))
        return videos

    def get_video_info(self, video_id: str) -> Optional[VideoInfo]:
        """単一の動画情報を取得"""
        videos = self._get_videos_details([video_id])
        return videos[0] if videos else None

    def get_my_playlists(self, max_results: int = 50) -> list[PlaylistInfo]:
        """自分の再生リスト一覧を取得"""
        playlists = []
        next_page_token = None

        while len(playlists) < max_results:
            request = self.service.playlists().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=min(50, max_results - len(playlists)),
                pageToken=next_page_token,
            )
            response = request.execute()

            for item in response.get("items", []):
                playlists.append(PlaylistInfo(
                    playlist_id=item["id"],
                    title=item["snippet"]["title"],
                    description=item["snippet"].get("description", ""),
                    item_count=item["contentDetails"]["itemCount"],
                ))

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return playlists

    def search_videos(
        self,
        query: str,
        max_results: int = 50,
        published_after: Optional[datetime] = None,
        published_before: Optional[datetime] = None,
        video_category_id: Optional[str] = None,
        region_code: Optional[str] = None,
    ) -> Iterator[VideoInfo]:
        """動画を検索

        Args:
            query: 検索クエリ
            max_results: 取得する最大動画数
            published_after: この日時以降に公開された動画
            published_before: この日時以前に公開された動画
            video_category_id: YouTubeカテゴリID（例: "10"=Music, "24"=Entertainment）
            region_code: ISO 3166-1 alpha-2国コード（例: "JP"=日本, "US"=アメリカ）
        """
        next_page_token = None
        fetched_count = 0

        while fetched_count < max_results:
            request_params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": min(50, max_results - fetched_count),
            }

            if next_page_token:
                request_params["pageToken"] = next_page_token
            if published_after:
                request_params["publishedAfter"] = published_after.isoformat() + "Z"
            if published_before:
                request_params["publishedBefore"] = published_before.isoformat() + "Z"
            if video_category_id:
                request_params["videoCategoryId"] = video_category_id
            if region_code:
                request_params["regionCode"] = region_code

            request = self.service.search().list(**request_params)
            response = request.execute()

            video_ids = [
                item["id"]["videoId"]
                for item in response.get("items", [])
            ]

            if video_ids:
                videos_details = self._get_videos_details(video_ids)
                for video in videos_details:
                    yield video
                    fetched_count += 1
                    if fetched_count >= max_results:
                        break

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    def get_channel_info(self, channel_ids: list[str]) -> dict[str, ChannelInfo]:
        """チャンネル情報を取得

        Args:
            channel_ids: チャンネルIDのリスト（最大50件）

        Returns:
            チャンネルID -> ChannelInfo のマッピング
        """
        if not channel_ids:
            return {}

        request = self.service.channels().list(
            part="snippet,statistics,status",
            id=",".join(channel_ids[:50]),
        )
        response = request.execute()

        channels = {}
        for item in response.get("items", []):
            channel_id = item["id"]
            snippet = item["snippet"]
            stats = item.get("statistics", {})

            # 登録者数が非公開の場合はNone
            subscriber_count = None
            if not stats.get("hiddenSubscriberCount", True):
                subscriber_count = int(stats.get("subscriberCount", 0)) if stats.get("subscriberCount") else None

            channels[channel_id] = ChannelInfo(
                channel_id=channel_id,
                title=snippet["title"],
                description=snippet.get("description", ""),
                subscriber_count=subscriber_count,
                video_count=int(stats.get("videoCount", 0)) if stats.get("videoCount") else None,
                view_count=int(stats.get("viewCount", 0)) if stats.get("viewCount") else None,
                custom_url=snippet.get("customUrl"),
            )

        return channels

    def search_videos_from_channels(
        self,
        channel_ids: list[str],
        query: str = "",
        max_results: int = 50,
        published_after: Optional[datetime] = None,
        published_before: Optional[datetime] = None,
    ) -> Iterator[VideoInfo]:
        """指定チャンネルから動画を検索（高精度検索用）

        Args:
            channel_ids: 検索対象チャンネルIDのリスト
            query: 検索クエリ（オプション）
            max_results: 取得する最大動画数
            published_after: この日時以降に公開された動画
            published_before: この日時以前に公開された動画
        """
        fetched_count = 0

        for channel_id in channel_ids:
            if fetched_count >= max_results:
                break

            next_page_token = None
            while fetched_count < max_results:
                request_params = {
                    "part": "snippet",
                    "channelId": channel_id,
                    "type": "video",
                    "maxResults": min(50, max_results - fetched_count),
                    "order": "relevance" if query else "date",
                }

                if query:
                    request_params["q"] = query
                if next_page_token:
                    request_params["pageToken"] = next_page_token
                if published_after:
                    request_params["publishedAfter"] = published_after.isoformat() + "Z"
                if published_before:
                    request_params["publishedBefore"] = published_before.isoformat() + "Z"

                request = self.service.search().list(**request_params)
                response = request.execute()

                video_ids = [
                    item["id"]["videoId"]
                    for item in response.get("items", [])
                ]

                if video_ids:
                    videos_details = self._get_videos_details(video_ids, include_statistics=True)
                    for video in videos_details:
                        yield video
                        fetched_count += 1
                        if fetched_count >= max_results:
                            break

                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break

    def search_videos_advanced(
        self,
        query: str,
        max_results: int = 50,
        published_after: Optional[datetime] = None,
        published_before: Optional[datetime] = None,
        video_category_id: Optional[str] = None,
        region_code: Optional[str] = None,
        precision: SearchPrecision = SearchPrecision.STANDARD,
        category: Optional[str] = None,
    ) -> Iterator[VideoInfo]:
        """高精度検索オプション付きの動画検索

        Args:
            query: 検索クエリ
            max_results: 取得する最大動画数
            published_after: この日時以降に公開された動画
            published_before: この日時以前に公開された動画
            video_category_id: YouTubeカテゴリID
            region_code: 地域コード
            precision: 検索精度レベル
            category: カテゴリ名（公式チャンネルフィルタ用）
        """
        if precision == SearchPrecision.HIGHEST:
            # 最高精度: 公式チャンネルIDから直接検索
            official_ids = list(get_official_channel_ids(category).keys())
            if official_ids:
                yield from self.search_videos_from_channels(
                    channel_ids=official_ids,
                    query=query,
                    max_results=max_results,
                    published_after=published_after,
                    published_before=published_before,
                )
            return

        elif precision == SearchPrecision.HIGH:
            # 高精度: 通常検索後、公式チャンネルのみフィルタ
            official_ids = set(get_official_channel_ids(category).keys())
            filtered_count = 0
            search_count = max_results * 5  # フィルタで減るため多めに取得

            for video in self.search_videos(
                query=query,
                max_results=search_count,
                published_after=published_after,
                published_before=published_before,
                video_category_id=video_category_id,
                region_code=region_code,
            ):
                if video.channel_id in official_ids or is_official_channel(video.channel_title):
                    yield video
                    filtered_count += 1
                    if filtered_count >= max_results:
                        break
            return

        # 標準精度: 通常検索（統計情報付き）
        next_page_token = None
        fetched_count = 0

        while fetched_count < max_results:
            request_params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": min(50, max_results - fetched_count),
            }

            if next_page_token:
                request_params["pageToken"] = next_page_token
            if published_after:
                request_params["publishedAfter"] = published_after.isoformat() + "Z"
            if published_before:
                request_params["publishedBefore"] = published_before.isoformat() + "Z"
            if video_category_id:
                request_params["videoCategoryId"] = video_category_id
            if region_code:
                request_params["regionCode"] = region_code

            request = self.service.search().list(**request_params)
            response = request.execute()

            video_ids = [
                item["id"]["videoId"]
                for item in response.get("items", [])
            ]

            if video_ids:
                videos_details = self._get_videos_details(video_ids, include_statistics=True)
                for video in videos_details:
                    yield video
                    fetched_count += 1
                    if fetched_count >= max_results:
                        break

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    def enrich_videos_with_channel_info(
        self,
        videos: list[VideoInfo]
    ) -> list[VideoInfo]:
        """動画リストにチャンネル情報を付加

        Args:
            videos: 動画リスト

        Returns:
            チャンネル情報が付加された動画リスト
        """
        if not videos:
            return videos

        # ユニークなチャンネルIDを収集
        channel_ids = list(set(v.channel_id for v in videos))

        # チャンネル情報を取得（50件ずつ）
        all_channels = {}
        for i in range(0, len(channel_ids), 50):
            batch = channel_ids[i:i+50]
            channels = self.get_channel_info(batch)
            all_channels.update(channels)

        # 動画にチャンネル情報を付加
        for video in videos:
            if video.channel_id in all_channels:
                channel = all_channels[video.channel_id]
                video.subscriber_count = channel.subscriber_count
                # 品質スコアを計算
                video.calculate_quality_score()

        return videos
