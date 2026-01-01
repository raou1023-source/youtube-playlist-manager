"""動画分類モジュール - 年代・ジャンル別に動画を分類"""

import sys
import os

# 親ディレクトリをパスに追加（通常のPython実行用）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from config import EraConfig, EraUnit, VIDEO_CATEGORIES
from youtube_client import VideoInfo


@dataclass
class ClassifiedVideo:
    """分類済み動画情報"""
    video: VideoInfo
    era_label: str
    category_name: Optional[str] = None


class VideoClassifier:
    """動画を年代・ジャンル別に分類するクラス"""

    def __init__(self, era_config: EraConfig):
        self.era_config = era_config

    def classify_by_era(self, video: VideoInfo) -> str:
        """動画を年代で分類"""
        return self.era_config.get_era_label(video.year)

    def classify_by_category(self, video: VideoInfo) -> Optional[str]:
        """動画をカテゴリ（ジャンル）で分類"""
        if video.category_id:
            return VIDEO_CATEGORIES.get(video.category_id)
        return None

    def classify_video(self, video: VideoInfo) -> ClassifiedVideo:
        """動画を年代とカテゴリで分類"""
        return ClassifiedVideo(
            video=video,
            era_label=self.classify_by_era(video),
            category_name=self.classify_by_category(video),
        )

    def group_by_era(self, videos: list[VideoInfo]) -> dict[str, list[VideoInfo]]:
        """動画リストを年代別にグループ化"""
        groups: dict[str, list[VideoInfo]] = defaultdict(list)
        for video in videos:
            era_label = self.classify_by_era(video)
            groups[era_label].append(video)
        return dict(groups)

    def group_by_category(self, videos: list[VideoInfo]) -> dict[str, list[VideoInfo]]:
        """動画リストをカテゴリ別にグループ化"""
        groups: dict[str, list[VideoInfo]] = defaultdict(list)
        for video in videos:
            category = self.classify_by_category(video) or "Unknown"
            groups[category].append(video)
        return dict(groups)

    def group_by_era_and_category(
        self, videos: list[VideoInfo]
    ) -> dict[str, dict[str, list[VideoInfo]]]:
        """動画リストを年代別→カテゴリ別にグループ化"""
        result: dict[str, dict[str, list[VideoInfo]]] = defaultdict(lambda: defaultdict(list))
        for video in videos:
            era_label = self.classify_by_era(video)
            category = self.classify_by_category(video) or "Unknown"
            result[era_label][category].append(video)
        return {era: dict(categories) for era, categories in result.items()}


def create_classifier(unit: str = "decade") -> VideoClassifier:
    """年代単位を指定して分類器を作成するファクトリ関数

    Args:
        unit: "decade" (10年), "half_decade" (5年), "three_year" (3年)
    """
    unit_map = {
        "decade": EraUnit.DECADE,
        "half_decade": EraUnit.HALF_DECADE,
        "three_year": EraUnit.THREE_YEAR,
        "10": EraUnit.DECADE,
        "5": EraUnit.HALF_DECADE,
        "3": EraUnit.THREE_YEAR,
    }

    era_unit = unit_map.get(unit.lower(), EraUnit.DECADE)
    config = EraConfig(unit=era_unit)
    return VideoClassifier(config)
