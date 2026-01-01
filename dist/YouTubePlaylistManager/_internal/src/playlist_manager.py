"""再生リスト管理モジュール"""

import sys
import os

# 親ディレクトリをパスに追加（通常のPython実行用）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from dataclasses import dataclass
from typing import Optional
from googleapiclient.discovery import Resource

from auth import get_authenticated_service
from youtube_client import VideoInfo, YouTubeClient
from video_classifier import VideoClassifier, create_classifier
from description_generator import DescriptionGenerator


@dataclass
class PlaylistCreationResult:
    """再生リスト作成結果"""
    playlist_id: str
    title: str
    video_count: int
    url: str


class PlaylistManager:
    """再生リストの作成・管理を行うクラス"""

    def __init__(self, service: Optional[Resource] = None):
        self._service = service
        self._description_generator = DescriptionGenerator()

    @property
    def service(self) -> Resource:
        """遅延初期化されたYouTubeサービスを取得"""
        if self._service is None:
            self._service = get_authenticated_service()
        return self._service

    def create_playlist(
        self,
        title: str,
        description: str = "",
        privacy_status: str = "private",
    ) -> str:
        """新しい再生リストを作成"""
        request = self.service.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                },
                "status": {
                    "privacyStatus": privacy_status,
                },
            },
        )
        response = request.execute()
        return response["id"]

    def create_playlist_with_details(
        self,
        title: str,
        era: str,
        category: str,
        keywords: list[str],
        additional_keyword: str,
        country: str,
        video_count: int,
        privacy_status: str = "private",
        add_detailed_description: bool = True,
    ) -> str:
        """詳細な説明文付きで再生リストを作成

        Args:
            title: プレイリストタイトル
            era: 年代
            category: カテゴリ
            keywords: 選択されたキーワード
            additional_keyword: 追加キーワード
            country: 国/地域
            video_count: 動画数
            privacy_status: プライバシー設定
            add_detailed_description: 詳細な説明を追加するか

        Returns:
            作成されたプレイリストのID
        """
        description = self._description_generator.generate_description(
            era=era,
            category=category,
            keywords=keywords,
            additional_keyword=additional_keyword,
            country=country,
            video_count=video_count,
            add_detailed=add_detailed_description,
        )
        return self.create_playlist(title, description, privacy_status)

    def generate_description(
        self,
        era: str,
        category: str,
        keywords: list[str],
        additional_keyword: str,
        country: str,
        video_count: int,
        add_detailed: bool = True,
    ) -> str:
        """説明文を生成（外部から呼び出し用）"""
        return self._description_generator.generate_description(
            era=era,
            category=category,
            keywords=keywords,
            additional_keyword=additional_keyword,
            country=country,
            video_count=video_count,
            add_detailed=add_detailed,
        )

    def add_video_to_playlist(self, playlist_id: str, video_id: str) -> bool:
        """再生リストに動画を追加"""
        try:
            request = self.service.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id,
                        },
                    },
                },
            )
            request.execute()
            return True
        except Exception as e:
            print(f"動画追加エラー (video_id={video_id}): {e}")
            return False

    def add_videos_to_playlist(
        self, playlist_id: str, video_ids: list[str]
    ) -> tuple[int, int]:
        """複数の動画を再生リストに追加

        Returns:
            (成功数, 失敗数)
        """
        success_count = 0
        fail_count = 0
        for video_id in video_ids:
            if self.add_video_to_playlist(playlist_id, video_id):
                success_count += 1
            else:
                fail_count += 1
        return success_count, fail_count

    def delete_playlist(self, playlist_id: str) -> bool:
        """再生リストを削除"""
        try:
            request = self.service.playlists().delete(id=playlist_id)
            request.execute()
            return True
        except Exception as e:
            print(f"再生リスト削除エラー: {e}")
            return False

    def find_playlist_by_title(self, title: str) -> Optional[str]:
        """タイトルで再生リストを検索"""
        client = YouTubeClient(self.service)
        playlists = client.get_my_playlists(max_results=200)
        for playlist in playlists:
            if playlist.title == title:
                return playlist.playlist_id
        return None

    def get_or_create_playlist(
        self,
        title: str,
        description: str = "",
        privacy_status: str = "private",
    ) -> str:
        """再生リストを取得または作成"""
        existing_id = self.find_playlist_by_title(title)
        if existing_id:
            return existing_id
        return self.create_playlist(title, description, privacy_status)

    def create_era_playlists(
        self,
        videos: list[VideoInfo],
        era_unit: str = "decade",
        title_prefix: str = "",
        privacy_status: str = "private",
    ) -> list[PlaylistCreationResult]:
        """年代別の再生リストを作成

        Args:
            videos: 分類対象の動画リスト
            era_unit: "decade" (10年), "half_decade" (5年), "three_year" (3年)
            title_prefix: 再生リストタイトルの接頭辞
            privacy_status: プライバシー設定

        Returns:
            作成した再生リストの結果リスト
        """
        classifier = create_classifier(era_unit)
        grouped = classifier.group_by_era(videos)

        results = []
        for era_label, era_videos in sorted(grouped.items()):
            title = f"{title_prefix}{era_label}" if title_prefix else era_label
            description = f"{era_label}に公開された動画 ({len(era_videos)}本)"

            playlist_id = self.get_or_create_playlist(
                title=title,
                description=description,
                privacy_status=privacy_status,
            )

            video_ids = [v.video_id for v in era_videos]
            success, fail = self.add_videos_to_playlist(playlist_id, video_ids)

            results.append(PlaylistCreationResult(
                playlist_id=playlist_id,
                title=title,
                video_count=success,
                url=f"https://www.youtube.com/playlist?list={playlist_id}",
            ))
            print(f"作成完了: {title} ({success}本追加, {fail}本失敗)")

        return results

    def create_category_playlists(
        self,
        videos: list[VideoInfo],
        title_prefix: str = "",
        privacy_status: str = "private",
    ) -> list[PlaylistCreationResult]:
        """カテゴリ（ジャンル）別の再生リストを作成"""
        classifier = create_classifier()
        grouped = classifier.group_by_category(videos)

        results = []
        for category, cat_videos in sorted(grouped.items()):
            title = f"{title_prefix}{category}" if title_prefix else category
            description = f"{category}カテゴリの動画 ({len(cat_videos)}本)"

            playlist_id = self.get_or_create_playlist(
                title=title,
                description=description,
                privacy_status=privacy_status,
            )

            video_ids = [v.video_id for v in cat_videos]
            success, fail = self.add_videos_to_playlist(playlist_id, video_ids)

            results.append(PlaylistCreationResult(
                playlist_id=playlist_id,
                title=title,
                video_count=success,
                url=f"https://www.youtube.com/playlist?list={playlist_id}",
            ))
            print(f"作成完了: {title} ({success}本追加, {fail}本失敗)")

        return results
