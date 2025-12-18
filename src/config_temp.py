"""設定管理モジュール - 年代分類設定（10年/5年/3年単位）"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional
import os
from pathlib import Path


class EraUnit(Enum):
    """年代分類の単位"""
    DECADE = 10      # 10年単位: 2020s, 2010s, 2000s...
    HALF_DECADE = 5  # 5年単位: 2020-2024, 2015-2019...
    THREE_YEAR = 3   # 3年単位: 2022-2024, 2019-2021...


@dataclass
class EraConfig:
    """年代分類の設定"""
    unit: EraUnit
    min_year: int = 1990  # 分類対象の最小年
    max_year: int = 2025  # 分類対象の最大年

    def get_era_label(self, year: int) -> str:
        """年から年代ラベルを生成"""
        if self.unit == EraUnit.DECADE:
            decade_start = (year // 10) * 10
            return f"{decade_start}s"
        elif self.unit == EraUnit.HALF_DECADE:
            half_decade_start = (year // 5) * 5
            return f"{half_decade_start}-{half_decade_start + 4}"
        elif self.unit == EraUnit.THREE_YEAR:
            three_year_start = ((year - self.min_year) // 3) * 3 + self.min_year
            return f"{three_year_start}-{three_year_start + 2}"
        return str(year)

    def get_all_eras(self) -> list[str]:
        """設定範囲内の全年代ラベルを取得"""
        eras = set()
        for year in range(self.min_year, self.max_year + 1):
            eras.add(self.get_era_label(year))
        return sorted(list(eras))


# YouTube Data API の設定
YOUTUBE_API_SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
]



# YouTube動画カテゴリID（参考用）
# https://developers.google.com/youtube/v3/docs/videoCategories/list
VIDEO_CATEGORIES = {
    1: "Film & Animation",
    2: "Autos & Vehicles",
    10: "Music",
    15: "Pets & Animals",
    17: "Sports",
    18: "Short Movies",
    19: "Travel & Events",
    20: "Gaming",
    21: "Videoblogging",
    22: "People & Blogs",
    23: "Comedy",
    24: "Entertainment",
    25: "News & Politics",
    26: "Howto & Style",
    27: "Education",
    28: "Science & Technology",
    29: "Nonprofits & Activism",
    30: "Movies",
    31: "Anime/Animation",
    32: "Action/Adventure",
    33: "Classics",
    34: "Comedy",
    35: "Documentary",
    36: "Drama",
    37: "Family",
    38: "Foreign",
    39: "Horror",
    40: "Sci-Fi/Fantasy",
    41: "Thriller",
    42: "Shorts",
    43: "Shows",
    44: "Trailers",
}

# カテゴリ名（小文字）からカテゴリIDへのマッピング
CATEGORY_NAME_TO_ID = {
    "music": "10",
    "entertainment": "24",
    "gaming": "20",
    "sports": "17",
    "education": "27",
    "film": "1",
    "animation": "1",
    "autos": "2",
    "vehicles": "2",
    "pets": "15",
    "animals": "15",
    "travel": "19",
    "events": "19",
    "blogs": "22",
    "people": "22",
    "comedy": "23",
    "news": "25",
    "politics": "25",
    "howto": "26",
    "style": "26",
    "science": "28",
    "technology": "28",
    "tech": "28",
    "nonprofits": "29",
    "activism": "29",
    "movies": "30",
    "anime": "31",
    "documentary": "35",
    "drama": "36",
    "shorts": "42",
    "shows": "43",
    "trailers": "44",
}

# 年代の日付範囲マッピング
ERA_DATE_RANGES = {
    "2020s": ("2020-01-01", "2029-12-31"),
    "2010s": ("2010-01-01", "2019-12-31"),
    "2000s": ("2000-01-01", "2009-12-31"),
    "1990s": ("1990-01-01", "1999-12-31"),
    "1980s": ("1980-01-01", "1989-12-31"),
    "1970s": ("1970-01-01", "1979-12-31"),
    "1960s": ("1960-01-01", "1969-12-31"),
}


def get_category_id(category_name: str) -> Optional[str]:
    """カテゴリ名からカテゴリIDを取得

    Args:
        category_name: カテゴリ名（大文字小文字は問わない）

    Returns:
        カテゴリID文字列、見つからない場合はNone
    """
    return CATEGORY_NAME_TO_ID.get(category_name.lower())


def get_era_date_range(era: str) -> Optional[tuple[str, str]]:
    """年代から日付範囲を取得

    Args:
        era: 年代（例: "2020s", "2010s"）

    Returns:
        (開始日, 終了日) のタプル、見つからない場合はNone
    """
    return ERA_DATE_RANGES.get(era.lower())


# プリセット設定
PRESET_CONFIGS = {
    "decade": EraConfig(unit=EraUnit.DECADE),
    "half_decade": EraConfig(unit=EraUnit.HALF_DECADE),
    "three_year": EraConfig(unit=EraUnit.THREE_YEAR),
}


# ========================================
# 公式チャンネル優先設定
# ========================================

# カテゴリ別の公式キーワード定義
OFFICIAL_KEYWORDS_BY_CATEGORY = {
    "music": ["official", "official audio", "official video", "official MV", "VEVO"],
    "news": ["official", "公式", "報道", "ニュース"],
    "entertainment": ["official", "公式"],
    "default": ["official", "公式"],
}

# チャンネル名に含まれる公式インジケータ
OFFICIAL_CHANNEL_INDICATORS = [
    "Official",
    "VEVO",
    "公式",
    "オフィシャル",
    "Verified",
    "Topic",  # YouTube Auto-generated artist channels (e.g., "Artist - Topic")
]

# ========================================
# 公式チャンネルIDデータベース（高精度検索用）
# ========================================

# 音楽系公式チャンネルID
OFFICIAL_MUSIC_CHANNEL_IDS = {
    # グローバルレーベル・VEVO
    "UCbXgNpp0jedKWcQiULLbDTA": "PewDiePie",  # 参考用（大規模チャンネル）
    "UC-9-kyTW8ZkZNDHQJ6FgpwQ": "Music (YouTube)",
    "UCVHFbqXqoYvEWM1Ddxl0QKg": "Warner Records",
    "UC0RhatS1pyxInC00YKjjBqQ": "Warner Music",
    "UCddiUEpeqJcYeBxX1IVBKvQ": "Warner Music Japan",
    "UCgwv23FVv3lqh567yagM9IQ": "Lil Nas X",
    "UCiMhD4jzUqG-IgPzUmmytRQ": "Republic Records",
    "UCnJvmzFzPTiKJSga7RS0a7w": "Atlantic Records",
    "UC0Cz-FXPjpgGg6xFZyPADhw": "Atlantic Records UK",
    "UC9ALqqC4aIeG5iDs7i90aBg": "Interscope Records",
    "UCIwFjwMjI0y7PDBVEO9-bkQ": "Def Jam Recordings",
    "UCqECaJ8Gagnn7YCbPEzWH6g": "Capitol Records",
    "UCZkURf9tDolFOeuw_4RD7XQ": "RCA Records",
    "UC_oe_t0cSjtLJ-LTr_6Agvw": "Epic Records",
    "UC-lHJZR3Gqxm24_Vd_AJ5Yw": "Sony Music",
    "UCPkv7nzYDO1eiVORJMawdlw": "Universal Music Group",
    # VEVO関連
    "UC4-TgOSMJHn-LtY4zCzbQhw": "TaylorSwiftVEVO",
    "UCuHzBCaKmtaLcRAOoazhCPA": "JustinBieberVEVO",
    "UCk1SpWNzOs4MYmr0uICEntg": "EdSheeranVEVO",
    "UC0WP5P-ufpRPOp9sP4nz2Y": "ArianaGrandeVEVO",
    "UCqc6fHuMiBnG5sJxPHdX9RQ": "DuaLipaVEVO",
    "UCbW18JZRgko_mOGm5er8Yzg": "TheWeekndVEVO",
    "UCp-Hy1N5vF5hIgRErgcqDPg": "BrunoMarsVEVO",
    "UCN1hnUccO4FD5WfM7ithXaw": "LadyGagaVEVO",
    "UCHkj014U2CQ2Nv0UZeYpE_A": "BillieEilishVEVO",
    # 日本のレーベル
    "UCAd7S4MOMtNJrL-hU4avZAQ": "avex",
    "UCG_kosK8f98ukMgtoHaivgQ": "UNIVERSAL MUSIC JAPAN",
    "UC_R1n5itCIWQvbkzCDOeYFA": "Sony Music (Japan)",
    "UCZVCcap5K7p_7eLVOX8sL3A": "Victor Entertainment",
    "UCG7KU-4eTEHGrFhHaAjFmag": "King Records",
    "UCMo8CpT0bJkNFI5e3WkC1bw": "TOY'S FACTORY",
    "UCLMcprQqJzRKLEhC8sHOrlw": "Being Inc.",
    "UC1ok2FXQX8A7V-eTYAiK6Gw": "PONY CANYON",
    "UCBrCqVsLq5HPZxLcPEbhJxg": "Lantis",
    # K-POP
    "UCEf_Bc-KVd7onSeifS3py9g": "BLACKPINK",
    "UC3IZKseVpdzPSBaWxBxundA": "HYBE LABELS",
    "UCweOkPb1wVVH0Q0Tlj4a5Pw": "BTS",
    "UCnhTT93w4m8k8qCSCONLIFA": "JYP Entertainment",
    "UCdCWrnjRyzQAFvWq8UBUhyg": "YG Entertainment",
    "UC3F6r4J0tV2TnQz4tGYKyNw": "SM Entertainment",
}

# ニュース系公式チャンネルID
OFFICIAL_NEWS_CHANNEL_IDS = {
    # 国際ニュース
    "UC16niRr50-MSBwiO3YDb3RA": "BBC News",
    "UCupvZG-5ko_eiXAupbDfxWw": "CNN",
    "UCNye-wNBqNL5ZzHSJj3l8Bg": "Al Jazeera English",
    "UChqUTb7kYRX8-EiaN3XFrSQ": "Reuters",
    "UC52X5wxOL_s5yw0dQk7NtgA": "Associated Press",
    "UCg3m2mN0gPPpF6mKxD-aOXw": "AFP News Agency",
    "UCknLrEdhRCp1aegoMqRaCZg": "DW News",
    "UCQfwfsi5VrQ8yKZ-UWmAEFg": "France 24 English",
    "UCoMdktPbSTixAyNGwb-UYkQ": "Sky News",
    "UCeY0bbntWzzVIaj2z3QigXg": "NBC News",
    "UCBi2mrWuNuyYy4gbM6fU18Q": "ABC News",
    "UC8p1vwvWtl6T73JiExfWs1g": "CBS News",
    "UCXIJgqnII2ZOINSWNOGFThA": "Fox News",
    "UCvJJ_dzjViJCoLf5uKUTwoA": "CNBC",
    "UCUMZ7gohGI9HcU9VNsr2FJQ": "Bloomberg Television",
    # 日本のニュース
    "UCGCZAYq5Xxojl_tSXcVJhiQ": "NHK",
    "UCuTAXTexrhetbOe3zgskJBQ": "日テレNEWS",
    "UCRTWs4R1fGHyVptXwKYNsHw": "TBS NEWS DIG",
    "UCGqvH6p3NagGNvJq4TtLJRQ": "テレ朝news",
    "UCkKvhXPN_vMkFu0gafNdMZg": "FNNプライムオンライン",
    "UCPyNsNSTUtywkekbDdCA_8Q": "ANNnewsCH",
    "UC6AG81pAkf6Lbi_1VC5NmPA": "テレビ東京 公式",
    "UCKnTp_-wBJhJkZAhGMmZxdA": "時事通信映像センター",
}

# エンターテインメント系公式チャンネルID
OFFICIAL_ENTERTAINMENT_CHANNEL_IDS = {
    # 日本のテレビ局
    "UCLTwul80LuxVdp3JlK7Z0HA": "日テレ公式チャンネル",
    "UCX_HqDLpqieLv7S3Y4-LdQg": "テレビ朝日",
    "UCMNMdMlQslEKWkyTJAVu3jw": "フジテレビ",
    "UCBN8YkXdj6M95VwlFBhKUGA": "TBS公式",
    # グローバルエンタメ
    "UCVPYbobPRzz0SjinWekjUBw": "Netflix",
    "UCMtFAi84ehTSYSE9XoHefig": "Prime Video",
    "UCnIup-Jnwr6emLxO-yJQzeA": "Disney",
}

# カテゴリ別チャンネルIDマッピング
OFFICIAL_CHANNEL_IDS_BY_CATEGORY = {
    "music": OFFICIAL_MUSIC_CHANNEL_IDS,
    "news": OFFICIAL_NEWS_CHANNEL_IDS,
    "entertainment": OFFICIAL_ENTERTAINMENT_CHANNEL_IDS,
}

# 主要公式チャンネルリスト（音楽レーベル）- 名前ベース（後方互換性）
OFFICIAL_MUSIC_CHANNELS = [
    # グローバルレーベル
    "Universal Music",
    "Sony Music",
    "Warner Music",
    "VEVO",
    "Atlantic Records",
    "Columbia Records",
    "Republic Records",
    "Interscope Records",
    "Def Jam Recordings",
    "Capitol Records",
    "RCA Records",
    "Epic Records",
    # 日本のレーベル
    "Sony Music (Japan)",
    "avex",
    "UNIVERSAL MUSIC JAPAN",
    "Victor Entertainment",
    "King Records",
    "Warner Music Japan",
    "TOY'S FACTORY",
    "Being Inc.",
    "PONY CANYON",
    "Lantis",
    # K-POP
    "HYBE LABELS",
    "JYP Entertainment",
    "YG Entertainment",
    "SM Entertainment",
]

# 主要公式チャンネルリスト（ニュース）
OFFICIAL_NEWS_CHANNELS = [
    # 国際ニュース
    "BBC News",
    "CNN",
    "Al Jazeera English",
    "Reuters",
    "Associated Press",
    "AFP",
    "DW News",
    "France 24 English",
    "Sky News",
    "NBC News",
    "ABC News",
    "CBS News",
    "Fox News",
    "CNBC",
    "Bloomberg",
    # 日本のニュース
    "NHK",
    "日テレNEWS",
    "TBS NEWS DIG",
    "テレビ朝日",
    "フジテレビ",
    "テレビ東京",
    "ANNnewsCH",
    "FNNプライムオンライン",
    "共同通信",
    "時事通信映像センター",
]

# すべての公式チャンネルリスト（結合）
ALL_OFFICIAL_CHANNELS = OFFICIAL_MUSIC_CHANNELS + OFFICIAL_NEWS_CHANNELS

# すべての公式チャンネルIDを結合
ALL_OFFICIAL_CHANNEL_IDS = {
    **OFFICIAL_MUSIC_CHANNEL_IDS,
    **OFFICIAL_NEWS_CHANNEL_IDS,
    **OFFICIAL_ENTERTAINMENT_CHANNEL_IDS,
}


def get_official_channel_ids(category: Optional[str] = None) -> dict[str, str]:
    """カテゴリに対応する公式チャンネルIDを取得

    Args:
        category: カテゴリ名（None=すべて）

    Returns:
        チャンネルID -> チャンネル名 のマッピング
    """
    if category is None:
        return ALL_OFFICIAL_CHANNEL_IDS
    return OFFICIAL_CHANNEL_IDS_BY_CATEGORY.get(category.lower(), {})


def is_official_channel_by_id(channel_id: str) -> bool:
    """チャンネルIDが公式チャンネルかどうかを判定

    Args:
        channel_id: チャンネルID

    Returns:
        公式チャンネルの場合True
    """
    return channel_id in ALL_OFFICIAL_CHANNEL_IDS


def get_official_keywords(category: str) -> list[str]:
    """カテゴリに対応する公式キーワードを取得

    Args:
        category: カテゴリ名（小文字）

    Returns:
        公式キーワードのリスト
    """
    return OFFICIAL_KEYWORDS_BY_CATEGORY.get(
        category.lower(),
        OFFICIAL_KEYWORDS_BY_CATEGORY["default"]
    )


def is_official_channel(channel_title: str) -> bool:
    """チャンネルが公式チャンネルかどうかを判定

    Args:
        channel_title: チャンネル名

    Returns:
        公式チャンネルの場合True
    """
    # チャンネル名に公式インジケータが含まれるか確認
    for indicator in OFFICIAL_CHANNEL_INDICATORS:
        if indicator.lower() in channel_title.lower():
            return True

    # 主要公式チャンネルリストに含まれるか確認
    for official_channel in ALL_OFFICIAL_CHANNELS:
        if official_channel.lower() in channel_title.lower():
            return True

    return False


def get_official_channel_score(channel_title: str, video_title: str = "") -> int:
    """公式チャンネルのスコアを計算（高いほど公式度が高い）

    Args:
        channel_title: チャンネル名
        video_title: 動画タイトル（オプション）

    Returns:
        公式スコア（0-100）
    """
    score = 0

    # チャンネル名のチェック
    channel_lower = channel_title.lower()

    # VEVOは最高スコア
    if "vevo" in channel_lower:
        score += 50

    # "Official" が含まれる
    if "official" in channel_lower:
        score += 40

    # 日本語の「公式」が含まれる
    if "公式" in channel_title:
        score += 40

    # "- Topic" チャンネル（YouTube自動生成のアーティストチャンネル）
    if "- topic" in channel_lower:
        score += 30

    # 主要公式チャンネルリストに含まれる
    for official_channel in ALL_OFFICIAL_CHANNELS:
        if official_channel.lower() in channel_lower:
            score += 25
            break

    # 動画タイトルのチェック
    if video_title:
        title_lower = video_title.lower()

        # タイトルに公式を示す文字列が含まれる
        official_title_keywords = [
            "official video", "official audio", "official mv",
            "official music video", "公式", "オフィシャル",
            "(official)", "[official]",
        ]
        for keyword in official_title_keywords:
            if keyword in title_lower:
                score += 10
                break

    return min(score, 100)  # 最大100点


# ========================================
# 地域・国別検索設定
# ========================================

# 地域グループ定義（階層構造）
REGION_GROUPS = {
    "全世界": {
        "全世界": None,  # regionCode なし
    },
    "アジア": {
        "日本": "JP",
        "韓国": "KR",
        "中国": "CN",
        "インド": "IN",
        "タイ": "TH",
        "ベトナム": "VN",
        "フィリピン": "PH",
        "インドネシア": "ID",
    },
    "ヨーロッパ": {
        "イギリス": "GB",
        "フランス": "FR",
        "ドイツ": "DE",
        "イタリア": "IT",
        "スペイン": "ES",
        "オランダ": "NL",
        "スウェーデン": "SE",
        "ノルウェー": "NO",
        "デンマーク": "DK",
        "ポーランド": "PL",
        "ロシア": "RU",
    },
    "北米・南米": {
        "アメリカ": "US",
        "カナダ": "CA",
        "メキシコ": "MX",
        "ブラジル": "BR",
        "アルゼンチン": "AR",
    },
    "アフリカ": {
        "アフリカ地域": "ZA",  # 南アフリカをデフォルトとして使用
    },
    "中東": {
        "中東地域": "AE",  # UAEをデフォルトとして使用
    },
    "オセアニア": {
        "オーストラリア": "AU",
        "ニュージーランド": "NZ",
    },
}

# 国名からISO 3166-1 alpha-2コードへのフラットマッピング
COUNTRY_TO_REGION_CODE: dict[str, Optional[str]] = {}
for group_name, countries in REGION_GROUPS.items():
    for country_name, code in countries.items():
        COUNTRY_TO_REGION_CODE[country_name] = code

# 国別の言語キーワード（検索クエリに自動追加）
REGION_KEYWORDS = {
    # アジア
    "JP": ["日本", "Japanese", "J-POP", "邦楽"],
    "KR": ["韓国", "Korean", "K-POP", "한국"],
    "CN": ["中国", "Chinese", "C-POP", "华语", "中文"],
    "IN": ["India", "Indian", "Bollywood", "Hindi"],
    "TH": ["Thailand", "Thai", "ไทย", "T-POP"],
    "VN": ["Vietnam", "Vietnamese", "Việt Nam", "V-POP"],
    "PH": ["Philippines", "Filipino", "Pinoy", "OPM"],
    "ID": ["Indonesia", "Indonesian", "Indo"],
    # ヨーロッパ
    "GB": ["UK", "British", "English"],
    "FR": ["France", "French", "français"],
    "DE": ["Germany", "German", "deutsch"],
    "IT": ["Italy", "Italian", "italiano"],
    "ES": ["Spain", "Spanish", "español", "Latino"],
    "NL": ["Netherlands", "Dutch", "Nederlands"],
    "SE": ["Sweden", "Swedish", "svenska"],
    "NO": ["Norway", "Norwegian", "norsk"],
    "DK": ["Denmark", "Danish", "dansk"],
    "PL": ["Poland", "Polish", "polski"],
    "RU": ["Russia", "Russian", "русский", "Россия"],
    # 北米・南米
    "US": ["USA", "US", "American", "United States"],
    "CA": ["Canada", "Canadian"],
    "MX": ["Mexico", "Mexican", "mexicano"],
    "BR": ["Brazil", "Brazilian", "Brasil", "português"],
    "AR": ["Argentina", "Argentine", "argentino"],
    # アフリカ
    "ZA": ["Africa", "African", "Afrobeat", "Afro"],
    # 中東
    "AE": ["Middle East", "Arabic", "Arab", "عربي"],
    # オセアニア
    "AU": ["Australia", "Australian", "Aussie"],
    "NZ": ["New Zealand", "Kiwi", "NZ"],
}

# 地域のデフォルト言語キーワード（regionCodeがNoneの場合）
DEFAULT_REGION_KEYWORDS: list[str] = []


def get_region_code(country_name: str) -> Optional[str]:
    """国名からYouTube APIの地域コードを取得

    Args:
        country_name: 国名（日本語）

    Returns:
        ISO 3166-1 alpha-2コード、見つからない場合はNone
    """
    return COUNTRY_TO_REGION_CODE.get(country_name)


def get_region_keywords(region_code: Optional[str]) -> list[str]:
    """地域コードから検索キーワードを取得

    Args:
        region_code: ISO 3166-1 alpha-2コード

    Returns:
        その地域に関連するキーワードのリスト
    """
    if region_code is None:
        return DEFAULT_REGION_KEYWORDS
    return REGION_KEYWORDS.get(region_code, [])


def get_all_countries() -> list[str]:
    """すべての国名をリストで取得

    Returns:
        国名のリスト（グループ順）
    """
    countries = []
    for group_name, group_countries in REGION_GROUPS.items():
        for country_name in group_countries.keys():
            countries.append(country_name)
    return countries


def get_country_display_name(country_name: str) -> str:
    """国名の表示用文字列を取得（地域コード付き）

    Args:
        country_name: 国名

    Returns:
        表示用文字列（例: "日本 (JP)"）
    """
    code = get_region_code(country_name)
    if code:
        return f"{country_name} ({code})"
    return country_name
