"""ニコニコ動画 API クライアントモジュール"""

import json
import urllib.request
import urllib.parse
import http.cookiejar
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Generator
import os
import re


@dataclass
class NicoVideoInfo:
    """ニコニコ動画情報"""
    video_id: str  # sm12345678 形式
    title: str
    description: str
    channel_title: str  # 投稿者名
    channel_id: str  # 投稿者ID
    published_at: str
    year: int
    duration: int  # seconds
    view_count: int
    like_count: int  # マイリスト数
    comment_count: int
    thumbnail_url: str
    url: str
    tags: list[str]
    platform: str = "niconico"

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
            "comment_count": self.comment_count,
            "thumbnail_url": self.thumbnail_url,
            "url": self.url,
            "tags": self.tags,
            "platform": self.platform,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NicoVideoInfo":
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
            comment_count=data.get("comment_count", 0),
            thumbnail_url=data.get("thumbnail_url", ""),
            url=data.get("url", ""),
            tags=data.get("tags", []),
            platform=data.get("platform", "niconico"),
        )


class NicoNicoClient:
    """ニコニコ動画 API クライアント

    Note:
        スナップショット検索API v2を使用（ログイン不要）
        https://site.nicovideo.jp/search-api-docs/snapshot

        より詳細な情報取得にはログインが必要な場合があります。
    """

    # スナップショット検索API
    SNAPSHOT_API_URL = "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"

    # 動画情報取得API（ログイン不要の公開情報のみ）
    VIDEO_INFO_URL = "https://ext.nicovideo.jp/api/getthumbinfo/"

    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Args:
            email: ニコニコアカウントのメールアドレス（オプション）
            password: パスワード（オプション）
                      環境変数 NICONICO_EMAIL, NICONICO_PASSWORD からも取得可能
        """
        self.email = email or os.getenv("NICONICO_EMAIL")
        self.password = password or os.getenv("NICONICO_PASSWORD")
        self._session_cookie = None
        self._logged_in = False

        # Cookie管理
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )

    def login(self) -> bool:
        """ニコニコ動画にログイン

        Returns:
            ログイン成功した場合True
        """
        if not self.email or not self.password:
            print("警告: ニコニコ動画の認証情報が設定されていません")
            return False

        login_url = "https://account.nicovideo.jp/login/redirector"
        data = urllib.parse.urlencode({
            "mail_tel": self.email,
            "password": self.password,
        }).encode("utf-8")

        try:
            request = urllib.request.Request(
                login_url,
                data=data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                }
            )
            with self.opener.open(request, timeout=30) as response:
                # ログイン成功の確認（Cookieにuser_sessionがあるか）
                for cookie in self.cookie_jar:
                    if cookie.name == "user_session":
                        self._logged_in = True
                        print("ニコニコ動画にログインしました")
                        return True

            print("ニコニコ動画へのログインに失敗しました")
            return False

        except Exception as e:
            print(f"ニコニコ動画ログインエラー: {e}")
            return False

    def _parse_duration(self, duration_str: str) -> int:
        """再生時間文字列を秒数に変換 (例: "3:45" -> 225)"""
        try:
            parts = duration_str.split(":")
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            return 0
        except (ValueError, AttributeError):
            return 0

    def _parse_snapshot_video(self, data: dict) -> NicoVideoInfo:
        """スナップショットAPIレスポンスからVideoInfoを作成"""
        # 投稿日時をパース
        start_time = data.get("startTime", "")
        try:
            dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            year = dt.year
            published_at = dt.isoformat()
        except (ValueError, AttributeError):
            year = 0
            published_at = start_time

        video_id = data.get("contentId", "")

        return NicoVideoInfo(
            video_id=video_id,
            title=data.get("title", ""),
            description=data.get("description", "") or "",
            channel_title=data.get("channelId", "") or data.get("userId", "") or "Unknown",
            channel_id=str(data.get("channelId", "") or data.get("userId", "")),
            published_at=published_at,
            year=year,
            duration=data.get("lengthSeconds", 0),
            view_count=data.get("viewCounter", 0),
            like_count=data.get("mylistCounter", 0),
            comment_count=data.get("commentCounter", 0),
            thumbnail_url=data.get("thumbnailUrl", ""),
            url=f"https://www.nicovideo.jp/watch/{video_id}",
            tags=data.get("tags", "").split(" ") if data.get("tags") else [],
        )

    def search_videos(
        self,
        query: str,
        max_results: int = 50,
        sort: str = "-viewCounter",
        targets: str = "title,description,tags",
        genre_keyword: Optional[str] = None,
    ) -> Generator[NicoVideoInfo, None, None]:
        """動画を検索（スナップショット検索API）

        Args:
            query: 検索クエリ
            max_results: 最大結果数
            sort: ソート順
                  -viewCounter: 再生数降順
                  -mylistCounter: マイリスト数降順
                  -commentCounter: コメント数降順
                  -startTime: 投稿日時降順
                  +startTime: 投稿日時昇順
            targets: 検索対象 (title, description, tags)
            genre_keyword: ジャンルキーワード（例: "音楽", "ゲーム"）

        Yields:
            NicoVideoInfo
        """
        params = {
            "q": query,
            "targets": targets,
            "fields": "contentId,title,description,userId,channelId,viewCounter,mylistCounter,commentCounter,thumbnailUrl,startTime,lengthSeconds,tags",
            "_sort": sort,
            "_limit": min(max_results, 100),  # APIの最大は100
            "_context": "youtube-playlist-manager",
        }

        if genre_keyword:
            params["q"] = f"{query} {genre_keyword}"

        url = f"{self.SNAPSHOT_API_URL}?{urllib.parse.urlencode(params)}"

        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                }
            )

            offset = 0
            total_fetched = 0

            while total_fetched < max_results:
                params["_offset"] = offset
                url = f"{self.SNAPSHOT_API_URL}?{urllib.parse.urlencode(params)}"
                request = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    }
                )

                with urllib.request.urlopen(request, timeout=30) as response:
                    result = json.loads(response.read().decode("utf-8"))

                if result.get("meta", {}).get("status") != 200:
                    print(f"ニコニコAPI エラー: {result.get('meta', {}).get('errorMessage', 'Unknown error')}")
                    break

                videos = result.get("data", [])
                if not videos:
                    break

                for video_data in videos:
                    if total_fetched >= max_results:
                        break
                    yield self._parse_snapshot_video(video_data)
                    total_fetched += 1

                if len(videos) < 100:  # これ以上結果がない
                    break

                offset += 100

        except urllib.error.HTTPError as e:
            print(f"ニコニコAPI HTTPエラー: {e.code} - {e.reason}")
        except Exception as e:
            print(f"ニコニコAPI エラー: {e}")

    def get_video_info(self, video_id: str) -> Optional[NicoVideoInfo]:
        """動画IDから動画情報を取得（getthumbinfo API）

        Args:
            video_id: 動画ID (例: sm12345678)

        Returns:
            NicoVideoInfo or None
        """
        url = f"{self.VIDEO_INFO_URL}{video_id}"

        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                }
            )

            with urllib.request.urlopen(request, timeout=30) as response:
                # XMLレスポンスをパース（簡易的な実装）
                xml_content = response.read().decode("utf-8")

                # 正規表現で主要な情報を抽出
                def extract_tag(tag_name: str) -> str:
                    match = re.search(f"<{tag_name}>(.*?)</{tag_name}>", xml_content, re.DOTALL)
                    return match.group(1) if match else ""

                # 投稿日時をパース
                first_retrieve = extract_tag("first_retrieve")
                try:
                    dt = datetime.fromisoformat(first_retrieve.replace("+09:00", "+09:00"))
                    year = dt.year
                    published_at = dt.isoformat()
                except (ValueError, AttributeError):
                    year = 0
                    published_at = first_retrieve

                return NicoVideoInfo(
                    video_id=video_id,
                    title=extract_tag("title"),
                    description=extract_tag("description"),
                    channel_title=extract_tag("user_nickname") or extract_tag("ch_name") or "Unknown",
                    channel_id=extract_tag("user_id") or extract_tag("ch_id") or "",
                    published_at=published_at,
                    year=year,
                    duration=self._parse_duration(extract_tag("length")),
                    view_count=int(extract_tag("view_counter") or 0),
                    like_count=int(extract_tag("mylist_counter") or 0),
                    comment_count=int(extract_tag("comment_num") or 0),
                    thumbnail_url=extract_tag("thumbnail_url"),
                    url=f"https://www.nicovideo.jp/watch/{video_id}",
                    tags=re.findall(r'<tag[^>]*>([^<]+)</tag>', xml_content),
                )

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"動画が見つかりません: {video_id}")
            else:
                print(f"ニコニコAPI HTTPエラー: {e.code} - {e.reason}")
            return None
        except Exception as e:
            print(f"ニコニコAPI エラー: {e}")
            return None

    def search_by_tag(
        self,
        tag: str,
        max_results: int = 50,
        sort: str = "-viewCounter",
    ) -> Generator[NicoVideoInfo, None, None]:
        """タグで動画を検索

        Args:
            tag: 検索タグ
            max_results: 最大結果数
            sort: ソート順

        Yields:
            NicoVideoInfo
        """
        # タグ検索はtargetsをtagsに限定
        yield from self.search_videos(
            query=tag,
            max_results=max_results,
            sort=sort,
            targets="tags",
        )

    def is_logged_in(self) -> bool:
        """ログイン状態を確認"""
        return self._logged_in

    def is_available(self) -> bool:
        """APIが利用可能かチェック（スナップショットAPIはログイン不要）"""
        return True


# テスト用
if __name__ == "__main__":
    client = NicoNicoClient()
    print("ニコニコ動画検索テスト（ログイン不要）")

    for video in client.search_videos("VOCALOID", max_results=5):
        print(f"- {video.title}")
        print(f"  URL: {video.url}")
        print(f"  再生数: {video.view_count}")
        print(f"  タグ: {', '.join(video.tags[:5])}")
        print()
