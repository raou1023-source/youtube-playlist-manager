"""説明文生成モジュール - 再生リストの説明文を自動生成"""

import urllib.request
import urllib.parse
import json
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


# ========================================
# 配信サービスリンク定義
# ========================================

MUSIC_STREAMING_SERVICES = {
    "Amazon Music": "https://music.amazon.co.jp/",
    "Spotify": "https://open.spotify.com/",
    "Apple Music": "https://music.apple.com/",
    "YouTube Music": "https://music.youtube.com/",
}

VIDEO_STREAMING_SERVICES = {
    "Netflix": "https://www.netflix.com/",
    "Prime Video": "https://www.amazon.co.jp/Prime-Video/",
    "Disney+": "https://www.disneyplus.com/",
    "U-NEXT": "https://video.unext.jp/",
    "Hulu": "https://www.hulu.jp/",
}

# カテゴリと配信サービスのマッピング
CATEGORY_SERVICE_MAP = {
    # 音楽系カテゴリ
    "music": "music",
    # 映画・映像系カテゴリ
    "film": "video",
    "movies": "video",
    "entertainment": "video",
    "anime": "video",
    "documentary": "video",
    "drama": "video",
    "shows": "video",
    # 両方（音楽と映像の複合カテゴリ）
    "trailers": "both",
}


@dataclass
class ArtistInfo:
    """アーティスト情報"""
    name: str
    summary: str = ""
    official_site: str = ""
    twitter: str = ""
    instagram: str = ""
    wikipedia_url: str = ""


class WikipediaAPI:
    """Wikipedia API クライアント"""

    BASE_URL = "https://ja.wikipedia.org/w/api.php"
    EN_BASE_URL = "https://en.wikipedia.org/w/api.php"

    @classmethod
    def search_artist(cls, name: str, lang: str = "ja") -> Optional[ArtistInfo]:
        """アーティスト情報をWikipediaから検索

        Args:
            name: アーティスト名
            lang: 言語コード（"ja" or "en"）

        Returns:
            ArtistInfo or None
        """
        base_url = cls.BASE_URL if lang == "ja" else cls.EN_BASE_URL

        try:
            # まず検索してページタイトルを取得
            search_params = {
                "action": "query",
                "list": "search",
                "srsearch": name,
                "srlimit": 1,
                "format": "json",
                "utf8": 1,
            }
            search_url = f"{base_url}?{urllib.parse.urlencode(search_params)}"

            with urllib.request.urlopen(search_url, timeout=10) as response:
                search_data = json.loads(response.read().decode("utf-8"))

            search_results = search_data.get("query", {}).get("search", [])
            if not search_results:
                # 日本語で見つからない場合は英語で再検索
                if lang == "ja":
                    return cls.search_artist(name, lang="en")
                return None

            page_title = search_results[0]["title"]

            # ページの概要を取得
            extract_params = {
                "action": "query",
                "titles": page_title,
                "prop": "extracts|info",
                "exintro": True,
                "explaintext": True,
                "exsentences": 3,
                "inprop": "url",
                "format": "json",
                "utf8": 1,
            }
            extract_url = f"{base_url}?{urllib.parse.urlencode(extract_params)}"

            with urllib.request.urlopen(extract_url, timeout=10) as response:
                extract_data = json.loads(response.read().decode("utf-8"))

            pages = extract_data.get("query", {}).get("pages", {})
            if not pages:
                return None

            page = list(pages.values())[0]
            summary = page.get("extract", "")
            wikipedia_url = page.get("fullurl", "")

            # 外部リンクを取得（公式サイト、SNSなど）
            extlinks_params = {
                "action": "query",
                "titles": page_title,
                "prop": "extlinks",
                "ellimit": 50,
                "format": "json",
                "utf8": 1,
            }
            extlinks_url = f"{base_url}?{urllib.parse.urlencode(extlinks_params)}"

            official_site = ""
            twitter = ""
            instagram = ""

            try:
                with urllib.request.urlopen(extlinks_url, timeout=10) as response:
                    extlinks_data = json.loads(response.read().decode("utf-8"))

                pages = extlinks_data.get("query", {}).get("pages", {})
                if pages:
                    page = list(pages.values())[0]
                    extlinks = page.get("extlinks", [])

                    for link_obj in extlinks:
                        link = link_obj.get("*", "")
                        if "twitter.com" in link or "x.com" in link:
                            if not twitter:
                                twitter = link
                        elif "instagram.com" in link:
                            if not instagram:
                                instagram = link
                        elif ("official" in link.lower() or
                              "公式" in link or
                              name.lower().replace(" ", "") in link.lower()):
                            if not official_site:
                                official_site = link
            except Exception:
                pass  # 外部リンク取得失敗は無視

            return ArtistInfo(
                name=name,
                summary=summary,
                official_site=official_site,
                twitter=twitter,
                instagram=instagram,
                wikipedia_url=wikipedia_url,
            )

        except Exception as e:
            print(f"Wikipedia API エラー: {e}")
            return None


class DescriptionGenerator:
    """再生リスト説明文生成クラス"""

    def __init__(self):
        self.wikipedia = WikipediaAPI()

    def generate_streaming_links(self, category: str) -> str:
        """配信サービスリンクを生成

        Args:
            category: カテゴリ名

        Returns:
            フォーマットされた配信サービスリンク文字列
        """
        service_type = CATEGORY_SERVICE_MAP.get(category.lower(), "music")
        lines = []

        if service_type in ("music", "both"):
            lines.append("📀 音楽配信サービス:")
            for name, url in MUSIC_STREAMING_SERVICES.items():
                lines.append(f"・{name}: {url}")
            lines.append("")

        if service_type in ("video", "both"):
            lines.append("🎬 動画配信サービス:")
            for name, url in VIDEO_STREAMING_SERVICES.items():
                lines.append(f"・{name}: {url}")
            lines.append("")

        return "\n".join(lines)

    def generate_artist_info(self, artist_name: str) -> str:
        """アーティスト情報を生成

        Args:
            artist_name: アーティスト名

        Returns:
            フォーマットされたアーティスト情報文字列
        """
        info = self.wikipedia.search_artist(artist_name)
        if not info:
            return ""

        lines = ["👤 アーティスト情報:"]

        if info.summary:
            # 概要を適度な長さに制限
            summary = info.summary[:300]
            if len(info.summary) > 300:
                summary += "..."
            lines.append(summary)
            lines.append("")

        # 公式リンク
        has_links = info.official_site or info.twitter or info.instagram or info.wikipedia_url
        if has_links:
            lines.append("🔗 公式リンク:")
            if info.official_site:
                lines.append(f"・公式サイト: {info.official_site}")
            if info.twitter:
                lines.append(f"・Twitter: {info.twitter}")
            if info.instagram:
                lines.append(f"・Instagram: {info.instagram}")
            if info.wikipedia_url:
                lines.append(f"・Wikipedia: {info.wikipedia_url}")
            lines.append("")

        return "\n".join(lines)

    def is_single_keyword_search(self, keywords: list[str], additional: str) -> tuple[bool, str]:
        """単一キーワード検索かどうかを判定

        Args:
            keywords: 選択されたキーワードリスト
            additional: 追加キーワード

        Returns:
            (単一キーワードかどうか, アーティスト名)
        """
        all_keywords = keywords.copy()
        if additional:
            all_keywords.extend(additional.split())

        # 1つのキーワードのみの場合はアーティスト名として扱う
        if len(all_keywords) == 1:
            return True, all_keywords[0]

        # 追加キーワードのみが入力され、スペースを含まない場合
        if not keywords and additional and " " not in additional.strip():
            return True, additional.strip()

        return False, ""

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
        """完全な説明文を生成

        Args:
            era: 年代
            category: カテゴリ
            keywords: 選択されたキーワード
            additional_keyword: 追加キーワード
            country: 国/地域
            video_count: 動画数
            add_detailed: 詳細な説明を追加するか

        Returns:
            生成された説明文
        """
        lines = []

        # 基本情報
        all_keywords = keywords.copy()
        if additional_keyword:
            all_keywords.append(additional_keyword)
        keyword_str = ", ".join(all_keywords) if all_keywords else "なし"

        lines.append(f"📋 再生リスト情報")
        lines.append(f"・年代: {era}")
        lines.append(f"・カテゴリ: {category}")
        lines.append(f"・キーワード: {keyword_str}")
        if country != "全世界":
            lines.append(f"・地域: {country}")
        lines.append(f"・動画数: {video_count}本")
        lines.append(f"・作成日: {datetime.now().strftime('%Y/%m/%d')}")
        lines.append("")

        if not add_detailed:
            return "\n".join(lines)

        # アーティスト情報（単一キーワードの場合）
        is_single, artist_name = self.is_single_keyword_search(keywords, additional_keyword)
        if is_single and artist_name:
            artist_info = self.generate_artist_info(artist_name)
            if artist_info:
                lines.append(artist_info)

        # 配信サービスリンク
        streaming_links = self.generate_streaming_links(category)
        if streaming_links:
            lines.append(streaming_links)

        return "\n".join(lines)

    def generate_simple_description(
        self,
        era: str,
        category: str,
        video_count: int,
        country: str = "全世界",
    ) -> str:
        """シンプルな説明文を生成

        Args:
            era: 年代
            category: カテゴリ
            video_count: 動画数
            country: 国/地域

        Returns:
            生成された説明文
        """
        desc = f"ランダムに選択された{era}の{category}動画 ({video_count}本)"
        if country != "全世界":
            desc += f" - 地域: {country}"
        return desc


# モジュール直接実行時のテスト
if __name__ == "__main__":
    generator = DescriptionGenerator()

    # テスト: 配信サービスリンク
    print("=== 音楽カテゴリ ===")
    print(generator.generate_streaming_links("music"))

    print("=== 映画カテゴリ ===")
    print(generator.generate_streaming_links("film"))

    # テスト: アーティスト情報
    print("=== アーティスト情報 ===")
    print(generator.generate_artist_info("宇多田ヒカル"))

    # テスト: 完全な説明文
    print("=== 完全な説明文 ===")
    print(generator.generate_description(
        era="2020s",
        category="music",
        keywords=["宇多田ヒカル"],
        additional_keyword="",
        country="日本",
        video_count=20,
        add_detailed=True,
    ))
