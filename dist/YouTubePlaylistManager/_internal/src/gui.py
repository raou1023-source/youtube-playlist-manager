"""YouTube Playlist Manager - GUIモジュール（マルチプラットフォーム対応）"""

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
import random
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
import webbrowser
import urllib.request
import io

from youtube_client import YouTubeClient, VideoInfo, SearchPrecision
from playlist_manager import PlaylistManager
from config import (
    get_category_id, get_era_date_range, CATEGORY_NAME_TO_ID,
    get_official_keywords, is_official_channel, get_official_channel_score,
    is_official_channel_by_id,
    REGION_GROUPS, get_region_code, get_region_keywords
)
from preset_manager import PresetManager, PresetSettings, Preset
from history_manager import HistoryManager, HistoryEntry, SearchConditions
from niconico_client import NicoNicoClient, NicoVideoInfo
from integrated_playlist import (
    IntegratedPlaylistManager, IntegratedPlaylist, IntegratedVideoItem,
    create_integrated_item_from_youtube,
    create_integrated_item_from_niconico
)
from setup_wizard import SetupStatus, SetupWizard, run_setup_wizard
from credentials_manager import get_credentials_manager, CredentialsManager
from backup_manager import BackupManager
from export_manager import ExportManager
from paths import CONFIG_PATH
from translations import t, set_language, get_current_language, t_keyword, t_region


class PresetEditDialog:
    """プリセット編集ダイアログ"""

    def __init__(self, parent, preset: Optional[Preset] = None, current_settings: Optional[PresetSettings] = None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("プリセット編集" if preset else "新規プリセット")
        self.dialog.geometry("500x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # 設定を初期化
        self.settings = preset.settings if preset else (current_settings or PresetSettings())
        self.preset_name = preset.name if preset else ""

        self._create_widgets()

        # モーダルとして待機
        self.dialog.wait_window()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # プリセット名
        name_frame = ttk.LabelFrame(main_frame, text="プリセット名", padding="5")
        name_frame.pack(fill=tk.X, pady=(0, 10))

        self.name_var = tk.StringVar(value=self.preset_name)
        ttk.Entry(name_frame, textvariable=self.name_var, width=40).pack(fill=tk.X)

        # スクロール可能なフレーム
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 年代
        era_frame = ttk.LabelFrame(scrollable, text="年代", padding="5")
        era_frame.pack(fill=tk.X, pady=5, padx=5)

        self.era_var = tk.StringVar(value=self.settings.era)
        eras = ["2020s", "2010s", "2000s", "1990s", "1980s", "1970s", "1960s"]
        ttk.Combobox(era_frame, textvariable=self.era_var, values=eras, state="readonly").pack(fill=tk.X)

        # カテゴリ
        cat_frame = ttk.LabelFrame(scrollable, text="カテゴリ", padding="5")
        cat_frame.pack(fill=tk.X, pady=5, padx=5)

        self.category_var = tk.StringVar(value=self.settings.category)
        categories = ["music", "entertainment", "gaming", "sports", "education", "comedy",
                      "film", "news", "howto", "science", "travel", "pets", "autos", "anime", "documentary"]
        ttk.Combobox(cat_frame, textvariable=self.category_var, values=categories, state="readonly").pack(fill=tk.X)

        # キーワード
        kw_frame = ttk.LabelFrame(scrollable, text="キーワード（カンマ区切り）", padding="5")
        kw_frame.pack(fill=tk.X, pady=5, padx=5)

        self.keywords_var = tk.StringVar(value=", ".join(self.settings.keywords))
        ttk.Entry(kw_frame, textvariable=self.keywords_var).pack(fill=tk.X)

        # 追加キーワード
        add_kw_frame = ttk.LabelFrame(scrollable, text="追加キーワード", padding="5")
        add_kw_frame.pack(fill=tk.X, pady=5, padx=5)

        self.additional_var = tk.StringVar(value=self.settings.additional_keyword)
        ttk.Entry(add_kw_frame, textvariable=self.additional_var).pack(fill=tk.X)

        # 地域
        region_frame = ttk.LabelFrame(scrollable, text="地域", padding="5")
        region_frame.pack(fill=tk.X, pady=5, padx=5)

        ttk.Label(region_frame, text="地域グループ:").pack(anchor=tk.W)
        self.region_group_var = tk.StringVar(value=self.settings.region_group)
        ttk.Combobox(region_frame, textvariable=self.region_group_var,
                     values=list(REGION_GROUPS.keys()), state="readonly").pack(fill=tk.X)

        ttk.Label(region_frame, text="国:", padding=(0, 5, 0, 0)).pack(anchor=tk.W)
        self.country_var = tk.StringVar(value=self.settings.country)
        ttk.Entry(region_frame, textvariable=self.country_var).pack(fill=tk.X)

        # 動画数
        count_frame = ttk.LabelFrame(scrollable, text="動画数", padding="5")
        count_frame.pack(fill=tk.X, pady=5, padx=5)

        self.count_var = tk.IntVar(value=self.settings.video_count)
        ttk.Scale(count_frame, from_=1, to=50, variable=self.count_var, orient=tk.HORIZONTAL).pack(fill=tk.X)
        ttk.Label(count_frame, textvariable=self.count_var).pack()

        # プライバシー
        privacy_frame = ttk.LabelFrame(scrollable, text="プライバシー", padding="5")
        privacy_frame.pack(fill=tk.X, pady=5, padx=5)

        self.privacy_var = tk.StringVar(value=self.settings.privacy)
        for text, val in [("非公開", "private"), ("限定公開", "unlisted"), ("公開", "public")]:
            ttk.Radiobutton(privacy_frame, text=text, variable=self.privacy_var, value=val).pack(side=tk.LEFT)

        # オプション
        opt_frame = ttk.LabelFrame(scrollable, text="オプション", padding="5")
        opt_frame.pack(fill=tk.X, pady=5, padx=5)

        self.official_var = tk.BooleanVar(value=self.settings.prefer_official)
        ttk.Checkbutton(opt_frame, text="公式チャンネル優先", variable=self.official_var).pack(anchor=tk.W)

        self.region_kw_var = tk.BooleanVar(value=self.settings.add_region_keywords)
        ttk.Checkbutton(opt_frame, text="地域キーワード自動追加", variable=self.region_kw_var).pack(anchor=tk.W)

        self.detailed_var = tk.BooleanVar(value=self.settings.add_detailed_description)
        ttk.Checkbutton(opt_frame, text="詳細な説明を追加", variable=self.detailed_var).pack(anchor=tk.W)

        # 検索精度
        precision_frame = ttk.LabelFrame(scrollable, text="検索精度", padding="5")
        precision_frame.pack(fill=tk.X, pady=5, padx=5)

        self.precision_var = tk.StringVar(value=self.settings.search_precision)
        for text, val in [("標準", "standard"), ("高精度", "high"), ("最高精度", "highest")]:
            ttk.Radiobutton(precision_frame, text=text, variable=self.precision_var, value=val).pack(side=tk.LEFT)

        # プラットフォーム
        platform_frame = ttk.LabelFrame(scrollable, text="プラットフォーム", padding="5")
        platform_frame.pack(fill=tk.X, pady=5, padx=5)

        self.platform_vars = {}
        for platform in ["youtube", "niconico"]:
            self.platform_vars[platform] = tk.BooleanVar(value=platform in self.settings.platforms)
            ttk.Checkbutton(platform_frame, text=platform.capitalize(),
                           variable=self.platform_vars[platform]).pack(side=tk.LEFT, padx=10)

        # ボタン
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text="保存", command=self._save).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="キャンセル", command=self.dialog.destroy).pack(side=tk.RIGHT)

    def _save(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("エラー", "プリセット名を入力してください", parent=self.dialog)
            return

        keywords = [k.strip() for k in self.keywords_var.get().split(",") if k.strip()]
        platforms = [p for p, var in self.platform_vars.items() if var.get()]

        self.result = {
            "name": name,
            "settings": PresetSettings(
                era=self.era_var.get(),
                category=self.category_var.get(),
                keywords=keywords,
                additional_keyword=self.additional_var.get().strip(),
                region_group=self.region_group_var.get(),
                country=self.country_var.get(),
                video_count=int(self.count_var.get()),
                privacy=self.privacy_var.get(),
                prefer_official=self.official_var.get(),
                search_precision=self.precision_var.get(),
                add_region_keywords=self.region_kw_var.get(),
                add_detailed_description=self.detailed_var.get(),
                platforms=platforms if platforms else ["youtube"],
            )
        }
        self.dialog.destroy()


class IntegratedPlaylistViewer:
    """統合プレイリストビューワーウィンドウ"""

    def __init__(self, parent, playlist: IntegratedPlaylist):
        self.playlist = playlist
        self.window = tk.Toplevel(parent)
        self.window.title(f"統合プレイリスト - {playlist.title}")
        self.window.geometry("800x600")
        self.window.transient(parent)

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ヘッダー情報
        header_frame = ttk.LabelFrame(main_frame, text="プレイリスト情報", padding="10")
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(header_frame, text=f"タイトル: {self.playlist.title}", font=("", 12, "bold")).pack(anchor=tk.W)
        if self.playlist.description:
            ttk.Label(header_frame, text=f"説明: {self.playlist.description}").pack(anchor=tk.W)
        ttk.Label(header_frame, text=f"作成日: {self.playlist.get_formatted_date()}").pack(anchor=tk.W)

        counts = self.playlist.get_platform_counts()
        count_text = f"合計: {len(self.playlist.items)}本"
        if counts:
            count_parts = []
            for platform, count in counts.items():
                platform_names = {"youtube": "YouTube", "niconico": "ニコニコ"}
                count_parts.append(f"{platform_names.get(platform, platform)}: {count}")
            count_text += f" ({', '.join(count_parts)})"
        ttk.Label(header_frame, text=count_text).pack(anchor=tk.W)

        # プラットフォームリンク
        if self.playlist.youtube_playlist_url or self.playlist.niconico_mylist_url:
            link_frame = ttk.Frame(header_frame)
            link_frame.pack(fill=tk.X, pady=(5, 0))
            ttk.Label(link_frame, text="プラットフォームリンク:").pack(side=tk.LEFT)
            if self.playlist.youtube_playlist_url:
                btn = ttk.Button(link_frame, text="YouTube", command=lambda: webbrowser.open(self.playlist.youtube_playlist_url))
                btn.pack(side=tk.LEFT, padx=5)
            if self.playlist.niconico_mylist_url:
                btn = ttk.Button(link_frame, text="ニコニコ", command=lambda: webbrowser.open(self.playlist.niconico_mylist_url))
                btn.pack(side=tk.LEFT, padx=5)

        # フィルターボタン
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filter_frame, text="フィルター:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="all")

        ttk.Radiobutton(filter_frame, text="すべて", variable=self.filter_var, value="all", command=self._apply_filter).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="YouTube", variable=self.filter_var, value="youtube", command=self._apply_filter).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="ニコニコ", variable=self.filter_var, value="niconico", command=self._apply_filter).pack(side=tk.LEFT, padx=5)

        # 動画リスト
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for videos
        self.video_tree = ttk.Treeview(
            list_frame,
            columns=("platform", "title", "channel", "year", "views"),
            show="headings",
            height=15
        )
        self.video_tree.heading("platform", text="Platform")
        self.video_tree.heading("title", text="タイトル")
        self.video_tree.heading("channel", text="チャンネル")
        self.video_tree.heading("year", text="年")
        self.video_tree.heading("views", text="視聴回数")

        self.video_tree.column("platform", width=80)
        self.video_tree.column("title", width=350)
        self.video_tree.column("channel", width=150)
        self.video_tree.column("year", width=60)
        self.video_tree.column("views", width=80)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.video_tree.yview)
        self.video_tree.configure(yscrollcommand=scrollbar.set)

        self.video_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ダブルクリックで動画を開く
        self.video_tree.bind("<Double-1>", self._open_selected_video)

        # ボタンフレーム
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text="選択した動画を開く", command=self._open_selected_video).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="閉じる", command=self.window.destroy).pack(side=tk.RIGHT)

        # 動画リストを表示
        self._populate_videos()

    def _populate_videos(self, platform_filter: str = "all"):
        """動画リストを表示"""
        for item in self.video_tree.get_children():
            self.video_tree.delete(item)

        for video in self.playlist.items:
            if platform_filter != "all" and video.platform != platform_filter:
                continue

            view_str = f"{video.view_count:,}" if video.view_count else ""
            self.video_tree.insert(
                "",
                tk.END,
                iid=video.id,
                values=(
                    f"{video.get_platform_icon()} {video.get_platform_display()}",
                    video.title[:50] + "..." if len(video.title) > 50 else video.title,
                    video.channel_title[:20] + "..." if len(video.channel_title) > 20 else video.channel_title,
                    video.year if video.year else "",
                    view_str,
                ),
                tags=(video.platform,)
            )

        # 色分け
        self.video_tree.tag_configure("youtube", background="#ffe0e0")
        self.video_tree.tag_configure("niconico", background="#e0ffe0")

    def _apply_filter(self):
        """フィルターを適用"""
        self._populate_videos(self.filter_var.get())

    def _open_selected_video(self, event=None):
        """選択した動画をブラウザで開く"""
        selection = self.video_tree.selection()
        if not selection:
            return

        video_id = selection[0]
        for video in self.playlist.items:
            if video.id == video_id:
                webbrowser.open(video.url)
                break


class PlaylistManagerGUI:
    """YouTube Playlist Manager GUI アプリケーション"""

    # 利用可能な年代（1960sから2020sまで）
    ERAS = ["2020s", "2010s", "2000s", "1990s", "1980s", "1970s", "1960s"]

    # 利用可能なカテゴリ（よく使われるものを選択）
    CATEGORIES = [
        "music",
        "entertainment",
        "gaming",
        "sports",
        "education",
        "comedy",
        "film",
        "news",
        "howto",
        "science",
        "travel",
        "pets",
        "autos",
        "anime",
        "documentary",
    ]

    # タブ別キーワード定義 (tab_key -> [API keywords])
    KEYWORD_TABS = {
        "tab_music": ["rock", "jazz", "pop", "classical", "hip-hop", "electronic", "country", "reggae", "blues", "metal"],
        "tab_movies": ["action", "comedy", "drama", "horror", "sci-fi", "animation", "documentary", "thriller"],
        "tab_education": ["science", "history", "math", "language", "technology", "tutorial", "lecture"],
        "tab_news": ["world_news", "politics", "economy", "sports_news", "technology_news"],
    }

    # 地域リスト (internal keys for region lookup)
    REGION_LIST = [
        "japan", "korea", "china", "india", "thailand", "vietnam", "philippines", "indonesia",
        "uk", "france", "germany", "italy", "spain", "netherlands", "sweden",
        "norway", "denmark", "poland", "russia",
        "usa", "canada", "mexico", "brazil", "argentina",
        "worldwide", "africa", "middle_east", "australia", "new_zealand",
    ]

    # 地域タブ - 「全世界」は「その他」タブの先頭に配置 (legacy, for reference)
    REGION_TABS = {
        "アジア": ["日本", "韓国", "中国", "インド", "タイ", "ベトナム", "フィリピン", "インドネシア"],
        "ヨーロッパ": ["イギリス", "フランス", "ドイツ", "イタリア", "スペイン", "オランダ", "スウェーデン", "ノルウェー", "デンマーク", "ポーランド", "ロシア"],
        "北米・南米": ["アメリカ", "カナダ", "メキシコ", "ブラジル", "アルゼンチン"],
        "その他": ["全世界", "アフリカ", "中東", "オーストラリア", "ニュージーランド"],
    }

    def __init__(self, root: tk.Tk, skip_setup_check: bool = False):
        self.root = root
        self.root.title("YouTube Playlist Manager")
        self.root.geometry("800x800")
        self.root.resizable(True, True)


        # 最小サイズを設定
        self.root.minsize(800, 600)

        # 実行中フラグ
        self.is_running = False

        # 内部スクロール可能なウィジェットのリスト（除外用）
        self._inner_scrollable_widgets: list[tk.Widget] = []

        # 結果保存用
        self.selected_videos: list[VideoInfo] = []
        self.playlist_url: Optional[str] = None

        # 現在のプレイリスト情報（動画確認用）
        self.current_playlist_id: Optional[str] = None
        self.current_playlist_title: Optional[str] = None

        # マルチプラットフォーム検索結果
        self.niconico_videos: list[NicoVideoInfo] = []

        # キーワードチェックボックス変数
        self.keyword_vars: dict[str, tk.BooleanVar] = {}

        # プリセットマネージャーと履歴マネージャー
        self.preset_manager = PresetManager()
        self.history_manager = HistoryManager()
        self.integrated_playlist_manager = IntegratedPlaylistManager()

        # プラットフォームクライアント
        self.niconico_client = NicoNicoClient()

        # 現在の検索条件（履歴保存用）
        self.current_search_conditions: Optional[SearchConditions] = None

        # プラットフォーム選択変数
        self.platform_vars: dict[str, tk.BooleanVar] = {}

        # 現在の統合プレイリスト
        self.current_integrated_playlist: Optional[IntegratedPlaylist] = None

        # 言語設定を読み込み
        self._load_language_preference()

        # メニューバーを作成
        self._create_menu()

        # UIを構築
        self._create_widgets()

        # ステータスバーを作成
        self._create_statusbar()

        # セットアップチェック（初回起動時）
        if not skip_setup_check:
            self.root.after(100, self._check_setup)

        # サイレント更新チェック（起動後3秒）
        self.root.after(3000, self._silent_update_check)

    def _open_url_safely(self, url: str) -> bool:
        """URLを安全に開く

        Args:
            url: 開くURL

        Returns:
            成功した場合True
        """
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"URLを開けませんでした: {url}")
            print(f"エラー: {e}")
            messagebox.showerror(
                "エラー",
                f"URLを開けませんでした:\n{url}\n\n"
                f"手動でブラウザにコピーしてください。\n\n"
                f"エラー詳細: {str(e)[:100]}"
            )
            return False

    def _copy_to_clipboard(self, text: str):
        """テキストをクリップボードにコピー

        Args:
            text: コピーするテキスト
        """
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
            messagebox.showinfo("コピー完了", "URLをクリップボードにコピーしました")
        except Exception as e:
            messagebox.showerror("エラー", f"クリップボードにコピーできませんでした:\n{str(e)}")

    def _load_language_preference(self):
        """Load saved language preference"""
        config_file = os.path.join(CONFIG_PATH, 'settings.json')
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    lang_code = settings.get('language', 'ja')
                    set_language(lang_code)
        except Exception:
            set_language('ja')  # Default to Japanese

    def _change_language(self, lang_code: str):
        """Change language and refresh UI"""
        # Save current keyword/region selections before changing language
        keyword_selections = {kw: var.get() for kw, var in self.keyword_vars.items()}
        region_selections = {region: var.get() for region, var in self.region_vars.items()}
        additional_keyword = self.keyword_var.get() if hasattr(self, 'keyword_var') else ""
        add_region_keywords = self.add_region_keywords_var.get() if hasattr(self, 'add_region_keywords_var') else True

        # Set new language
        set_language(lang_code)

        # Save preference
        config_file = os.path.join(CONFIG_PATH, 'settings.json')
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            else:
                settings = {}

            settings['language'] = lang_code

            # Ensure directory exists
            os.makedirs(CONFIG_PATH, exist_ok=True)

            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        # Rebuild menu bar
        self._create_menu()

        # Rebuild keyword tabs
        self._rebuild_keyword_tabs()

        # Restore selections
        for kw, selected in keyword_selections.items():
            if kw in self.keyword_vars:
                self.keyword_vars[kw].set(selected)
        for region, selected in region_selections.items():
            if region in self.region_vars:
                self.region_vars[region].set(selected)
        if hasattr(self, 'keyword_var'):
            self.keyword_var.set(additional_keyword)
        if hasattr(self, 'add_region_keywords_var'):
            self.add_region_keywords_var.set(add_region_keywords)

        # Update all UI text elements
        self._update_all_ui_text()

        # Update displays
        self._update_selected_keywords_display()
        self._update_selected_regions_display()

        # Show message
        messagebox.showinfo("Info", t('language_changed'))

    def _update_all_ui_text(self):
        """Update all UI text elements with current language"""
        # Update section frame labels
        if hasattr(self, 'basic_frame'):
            self.basic_frame.config(text=t('section_basic'))
        if hasattr(self, 'keyword_frame'):
            self.keyword_frame.config(text=t('section_keywords'))
        if hasattr(self, 'search_options_frame'):
            self.search_options_frame.config(text=t('section_search_options'))
        if hasattr(self, 'privacy_frame'):
            self.privacy_frame.config(text=t('section_privacy'))
        if hasattr(self, 'platform_frame'):
            self.platform_frame.config(text=t('section_platform'))
        if hasattr(self, 'preset_section_frame'):
            self.preset_section_frame.config(text=t('section_preset'))
        if hasattr(self, 'progress_label_frame'):
            self.progress_label_frame.config(text=t('section_progress'))
        if hasattr(self, 'result_frame'):
            self.result_frame.config(text=t('section_result'))

        # Update basic settings labels
        if hasattr(self, 'era_label_widget'):
            self.era_label_widget.config(text=t('label_era'))
        if hasattr(self, 'category_label_widget'):
            self.category_label_widget.config(text=t('label_category'))
        if hasattr(self, 'video_count_label_widget'):
            self.video_count_label_widget.config(text=t('label_video_count'))
        if hasattr(self, 'video_range_label'):
            self.video_range_label.config(text=t('label_video_range'))

        # Update search precision section
        if hasattr(self, 'precision_label'):
            self.precision_label.config(text=t('search_precision_label'))
        if hasattr(self, 'precision_radio_frames'):
            for option_frame, rb, desc_label, label_key, desc_key in self.precision_radio_frames:
                rb.config(text=t(label_key))
                desc_label.config(text=f"  └ {t(desc_key)}")

        # Update official channel section
        if hasattr(self, 'official_label'):
            self.official_label.config(text=t('section_official_channel'))
        if hasattr(self, 'prefer_official_cb'):
            self.prefer_official_cb.config(text=t('option_official_channel'))
        if hasattr(self, 'verified_cb'):
            self.verified_cb.config(text=t('option_verified_badge'))
        if hasattr(self, 'subscribers_cb'):
            self.subscribers_cb.config(text=t('option_subscriber_100k'))
        if hasattr(self, 'views_cb'):
            self.views_cb.config(text=t('option_video_views_100k'))
        if hasattr(self, 'vevo_cb'):
            self.vevo_cb.config(text=t('option_vevo_only'))
        if hasattr(self, 'detailed_desc_cb'):
            self.detailed_desc_cb.config(text=t('option_add_detailed_desc'))

        # Update privacy radio buttons
        if hasattr(self, 'privacy_radio_buttons'):
            for rb, label_key, desc_key in self.privacy_radio_buttons:
                rb.config(text=f"{t(label_key)}  ({t(desc_key)})")

        # Update platform checkboxes
        if hasattr(self, 'platform_checkboxes'):
            if 'youtube' in self.platform_checkboxes:
                self.platform_checkboxes['youtube'].config(text=t('platform_youtube'))
            if 'niconico' in self.platform_checkboxes:
                self.platform_checkboxes['niconico'].config(text=t('platform_niconico'))

        # Update preset section
        if hasattr(self, 'preset_label'):
            self.preset_label.config(text=t('label_preset'))
        if hasattr(self, 'preset_buttons') and hasattr(self, 'preset_button_keys'):
            for btn, key in zip(self.preset_buttons, self.preset_button_keys):
                btn.config(text=t(key))

        # Update action buttons
        if hasattr(self, 'execute_btn'):
            self.execute_btn.config(text=t('btn_create_playlist'))
        if hasattr(self, 'cancel_btn'):
            self.cancel_btn.config(text=t('btn_cancel'))

        # Update result section
        if hasattr(self, 'url_label_widget'):
            self.url_label_widget.config(text=t('label_playlist_url'))
        if hasattr(self, 'copy_btn'):
            self.copy_btn.config(text=t('btn_copy_url'))
        if hasattr(self, 'open_btn'):
            self.open_btn.config(text=t('btn_open'))

        # Update progress
        if hasattr(self, 'progress_var'):
            current_progress = self.progress_var.get()
            # Only update if it's the default waiting message
            if current_progress in ['待機中...', 'Waiting...']:
                self.progress_var.set(t('progress_waiting'))

        # Update additional keyword label
        if hasattr(self, 'additional_keyword_label'):
            self.additional_keyword_label.config(text=t('additional_keyword'))

        # Update region keyword checkbox
        if hasattr(self, 'region_keyword_cb'):
            self.region_keyword_cb.config(text=t('region_keyword_auto'))

        # Update history section
        if hasattr(self, 'history_frame'):
            self.history_frame.config(text=t('section_history'))
        if hasattr(self, 'history_buttons'):
            self.history_buttons['refresh'].config(text=t('btn_refresh'))
            self.history_buttons['delete_all'].config(text=t('btn_delete_all'))
            self.history_buttons['export'].config(text=t('btn_export'))
            self.history_buttons['import'].config(text=t('btn_import'))
        if hasattr(self, 'history_action_buttons'):
            self.history_action_buttons['recreate'].config(text=t('btn_recreate_same'))
            self.history_action_buttons['open_url'].config(text=t('btn_open_url'))
            self.history_action_buttons['video_confirm'].config(text=f"📺 {t('btn_video_confirm')}")
            self.history_action_buttons['delete'].config(text=t('btn_delete_history'))
            self.history_action_buttons['csv_export'].config(text=t('btn_csv_export'))
        if hasattr(self, 'history_tree'):
            self.history_tree.heading("date", text=t('col_created_date'))
            self.history_tree.heading("title", text=t('col_title'))
            self.history_tree.heading("videos", text=t('col_video_count'))
            self.history_tree.heading("platform", text=t('col_platform'))
            self.history_tree.heading("category", text=t('col_category'))
            self.history_tree.heading("era", text=t('col_era'))

        # Update integrated playlist viewer section
        if hasattr(self, 'integrated_frame'):
            self.integrated_frame.config(text=t('section_integrated_viewer'))
        if hasattr(self, 'integrated_buttons'):
            self.integrated_buttons['refresh'].config(text=t('btn_refresh'))
            self.integrated_buttons['create_new'].config(text=t('btn_create_new'))
            self.integrated_buttons['json_export'].config(text=t('btn_json_export'))
            self.integrated_buttons['html_export'].config(text=t('btn_html_export'))
            self.integrated_buttons['delete'].config(text=t('btn_delete'))
        if hasattr(self, 'integrated_tree'):
            self.integrated_tree.heading("date", text=t('col_created_date'))
            self.integrated_tree.heading("title", text=t('col_title'))
            self.integrated_tree.heading("videos", text=t('col_total'))
            self.integrated_tree.heading("youtube", text=t('col_youtube'))
            self.integrated_tree.heading("niconico", text=t('col_niconico'))

    def _rebuild_keyword_tabs(self):
        """Rebuild keyword tabs with new language"""
        # Clear existing tabs
        for tab_id in self.keyword_notebook.tabs():
            self.keyword_notebook.forget(tab_id)

        # Clear internal scrollable widgets list for these tabs
        self._inner_scrollable_widgets = [w for w in self._inner_scrollable_widgets
                                          if not str(w).startswith(str(self.keyword_notebook))]

        # Clear keyword_vars and region_vars (will be recreated)
        self.keyword_vars.clear()
        self.region_vars.clear()

        # Recreate keyword tabs
        for tab_key, keywords in self.KEYWORD_TABS.items():
            tab_frame = ttk.Frame(self.keyword_notebook)
            self.keyword_notebook.add(tab_frame, text=t(tab_key))

            # スクロール可能なキャンバスを作成（高さ150px）
            tab_canvas = tk.Canvas(tab_frame, highlightthickness=0, height=150)
            tab_scrollbar = ttk.Scrollbar(
                tab_frame,
                orient="vertical",
                command=tab_canvas.yview,
                style="Keyword.Vertical.TScrollbar"
            )
            tab_scrollable = ttk.Frame(tab_canvas, padding="10")

            tab_scrollable.bind(
                "<Configure>",
                lambda e, c=tab_canvas: c.configure(scrollregion=c.bbox("all"))
            )

            tab_canvas_window = tab_canvas.create_window((0, 0), window=tab_scrollable, anchor="nw")

            def _on_tab_canvas_configure(event, canvas=tab_canvas, window=tab_canvas_window):
                canvas.itemconfig(window, width=event.width - 20)
            tab_canvas.bind("<Configure>", _on_tab_canvas_configure)

            tab_canvas.configure(yscrollcommand=tab_scrollbar.set)
            tab_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            tab_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self._register_inner_scrollable(tab_scrollable, tab_canvas)

            num_cols = 3
            for i, keyword in enumerate(keywords):
                var = tk.BooleanVar(value=False)
                self.keyword_vars[keyword] = var
                cb = ttk.Checkbutton(
                    tab_scrollable,
                    text=t_keyword(keyword),
                    variable=var
                )
                row = i // num_cols
                col = i % num_cols
                cb.grid(row=row, column=col, sticky=tk.W, padx=15, pady=5)

            for col in range(num_cols):
                tab_scrollable.columnconfigure(col, weight=1)

            self.bind_mousewheel(tab_scrollable)

        # Recreate region tab
        region_tab_frame = ttk.Frame(self.keyword_notebook)
        self.keyword_notebook.add(region_tab_frame, text=t('tab_region'))

        region_canvas = tk.Canvas(region_tab_frame, highlightthickness=0, height=180)
        region_scrollbar = ttk.Scrollbar(
            region_tab_frame,
            orient="vertical",
            command=region_canvas.yview,
            style="Keyword.Vertical.TScrollbar"
        )
        region_scrollable = ttk.Frame(region_canvas, padding="10")

        region_scrollable.bind(
            "<Configure>",
            lambda e: region_canvas.configure(scrollregion=region_canvas.bbox("all"))
        )

        region_canvas_window = region_canvas.create_window((0, 0), window=region_scrollable, anchor="nw")

        def _on_region_canvas_configure(event):
            region_canvas.itemconfig(region_canvas_window, width=event.width - 20)
        region_canvas.bind("<Configure>", _on_region_canvas_configure)

        region_canvas.configure(yscrollcommand=region_scrollbar.set)
        region_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        region_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._register_inner_scrollable(region_scrollable, region_canvas)

        num_cols = 4
        for i, region in enumerate(self.REGION_LIST):
            default_value = (region == "worldwide")
            var = tk.BooleanVar(value=default_value)
            self.region_vars[region] = var
            cb = ttk.Checkbutton(
                region_scrollable,
                text=t_region(region),
                variable=var
            )
            row = i // num_cols
            col = i % num_cols
            cb.grid(row=row, column=col, sticky=tk.W, padx=10, pady=3)

        for col in range(num_cols):
            region_scrollable.columnconfigure(col, weight=1)

        self.bind_mousewheel(region_scrollable)

        # Rebind trace callbacks for display updates
        for var in self.keyword_vars.values():
            var.trace_add("write", self._update_selected_keywords_display)
        for var in self.region_vars.values():
            var.trace_add("write", self._update_selected_regions_display)

        # Update labels
        if hasattr(self, 'additional_keyword_label'):
            self.additional_keyword_label.config(text=t('additional_keyword'))
        if hasattr(self, 'region_keyword_cb'):
            self.region_keyword_cb.config(text=t('region_keyword_auto'))

    def _create_menu(self):
        """メニューバーを作成"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # ファイルメニュー
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=t('menu_file'), menu=file_menu)
        file_menu.add_command(label=t('export_history'), command=self._export_history)
        file_menu.add_command(label=t('import_history'), command=self._import_history)
        file_menu.add_separator()

        # エクスポートサブメニュー
        export_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label=t('menu_export'), menu=export_menu)
        export_menu.add_command(label=t('export_csv'), command=lambda: self._export_data('csv'))
        export_menu.add_command(label=t('export_json'), command=lambda: self._export_data('json'))
        export_menu.add_command(label=t('export_txt'), command=lambda: self._export_data('txt'))
        file_menu.add_separator()

        # バックアップ機能
        file_menu.add_command(label=t('backup_create'), command=self._create_backup)
        file_menu.add_command(label=t('backup_restore'), command=self._restore_from_backup)
        file_menu.add_command(label=t('backup_manage'), command=self._manage_backups)
        file_menu.add_separator()
        file_menu.add_command(label=t('menu_exit'), command=self.root.quit)

        # お気に入りメニュー
        favorites_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=t('menu_favorites'), menu=favorites_menu)
        favorites_menu.add_command(label=t('favorites_save'), command=self._save_current_as_favorite)
        favorites_menu.add_command(label=t('favorites_load'), command=self._load_favorite)
        favorites_menu.add_separator()
        favorites_menu.add_command(label=t('favorites_manage'), command=self._manage_favorites)

        # 設定メニュー
        settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=t('menu_settings'), menu=settings_menu)

        # 言語サブメニュー
        language_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label=t('menu_language'), menu=language_menu)
        language_menu.add_command(label='日本語', command=lambda: self._change_language('ja'))
        language_menu.add_command(label='English', command=lambda: self._change_language('en'))
        language_menu.add_command(label='简体中文', command=lambda: self._change_language('zh-CN'))
        language_menu.add_command(label='繁體中文', command=lambda: self._change_language('zh-TW'))
        language_menu.add_command(label='한국어', command=lambda: self._change_language('ko'))
        language_menu.add_command(label='Español', command=lambda: self._change_language('es'))
        language_menu.add_command(label='Français', command=lambda: self._change_language('fr'))
        language_menu.add_command(label='Deutsch', command=lambda: self._change_language('de'))
        
        settings_menu.add_separator()

        settings_menu.add_command(label=t('setup_wizard'), command=self._open_setup_wizard)
        settings_menu.add_separator()
        settings_menu.add_command(label=t('youtube_auth'), command=self._reset_credentials)
        settings_menu.add_command(label=t('niconico_auth'), command=self._open_niconico_auth_dialog)
        settings_menu.add_separator()
        settings_menu.add_command(label=t('check_auth_status'), command=self._check_auth_status)

        # ヘルプメニュー
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=t('menu_help'), menu=help_menu)
        help_menu.add_command(label=t('youtube_api_help'), command=self._show_youtube_api_help)
        help_menu.add_command(label=t('niconico_help'), command=self._show_niconico_help)
        help_menu.add_separator()
        help_menu.add_command(label=t('usage_guide'), command=lambda: self._open_url_safely("https://developers.google.com/youtube/v3/getting-started"))
        help_menu.add_command(label=t('troubleshooting'), command=lambda: self._open_url_safely("https://developers.google.com/youtube/v3/getting-started#before-you-start"))
        help_menu.add_separator()
        help_menu.add_command(label=t('update_check'), command=self._check_for_updates)
        help_menu.add_separator()
        help_menu.add_command(label=t('about'), command=self._show_about)

    def _create_statusbar(self):
        """ステータスバーを作成"""
        self.statusbar_frame = ttk.Frame(self.root, relief=tk.SUNKEN)
        self.statusbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # 認証状態（マルチプラットフォーム対応）
        self.platform_status_var = tk.StringVar(value="認証状態: 確認中...")
        self.platform_status_label = ttk.Label(
            self.statusbar_frame,
            textvariable=self.platform_status_var,
            padding=(10, 2)
        )
        self.platform_status_label.pack(side=tk.LEFT)

        # セパレータ
        ttk.Separator(self.statusbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # バージョン情報
        version_label = ttk.Label(
            self.statusbar_frame,
            text="v1.0.0",
            foreground="gray",
            padding=(10, 2)
        )
        version_label.pack(side=tk.RIGHT)

        # 認証状態を更新
        self.root.after(500, self.refresh_auth_status)

    def _update_auth_status(self):
        """ステータスバーの認証状態を更新（マルチプラットフォーム対応）"""
        try:
            manager = get_credentials_manager()
            status_text = manager.get_status_display()
            self.platform_status_var.set(status_text)
        except Exception:
            # フォールバック: 従来のYouTubeのみ表示
            if SetupStatus.has_token():
                self.platform_status_var.set("✓ YouTube")
            else:
                self.platform_status_var.set("✗ YouTube")

    def refresh_auth_status(self):
        """認証状態を再読み込みして全UIを更新（認証完了後に呼び出す）"""
        # ステータスバーを更新
        self._update_auth_status()
        # プラットフォームチェックボックスの有効/無効を更新
        self._update_platform_checkboxes()

    def _check_setup(self):
        """セットアップ状態をチェックし、必要に応じてウィザードを起動"""
        if SetupStatus.needs_setup():
            result = messagebox.askyesno(
                "初回セットアップ",
                "YouTube Playlist Managerへようこそ！\n\n"
                "初回セットアップが必要です。\n"
                "セットアップウィザードを起動しますか？\n\n"
                "（「いいえ」を選択した場合、「設定」メニューから後で設定できます）"
            )
            if result:
                self._open_setup_wizard()

    def _open_setup_wizard(self):
        """セットアップウィザードを開く"""
        def on_complete(success):
            # 認証状態を再読み込みしてUIを更新（再起動不要にする）
            self.refresh_auth_status()
            if success:
                messagebox.showinfo("完了", "セットアップが完了しました！\nすぐにプラットフォームを使用できます。")

        wizard = SetupWizard(self.root, on_complete=on_complete)

    def _reset_credentials(self):
        """認証情報をリセット"""
        # カスタム確認ダイアログを表示
        dialog = tk.Toplevel(self.root)
        dialog.title("認証の再設定")
        dialog.geometry("450x220")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # 中央に配置
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        result = {"confirmed": False}

        # メッセージフレーム
        message_frame = ttk.Frame(dialog, padding=20)
        message_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            message_frame,
            text="認証情報をリセットしますか？",
            font=("", 12, "bold")
        ).pack(pady=(10, 15))

        ttk.Label(
            message_frame,
            text="この操作により、保存されている認証トークンが削除されます。\n次回使用時に再ログインが必要になります。",
            justify=tk.CENTER
        ).pack(pady=5)

        ttk.Label(
            message_frame,
            text="※ この操作は取り消せません",
            foreground="red"
        ).pack(pady=(10, 0))

        # ボタンフレーム（下部に固定）
        button_frame = ttk.Frame(dialog, padding=10)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        def on_cancel():
            dialog.destroy()

        def on_ok():
            result["confirmed"] = True
            dialog.destroy()

        ttk.Button(button_frame, text="キャンセル", command=on_cancel, width=12).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="OK", command=on_ok, width=12).pack(side=tk.RIGHT, padx=10)

        # ダイアログが閉じるまで待機
        dialog.wait_window()

        if not result["confirmed"]:
            return

        # トークンファイルを削除
        from paths import TOKEN_FILE
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()

        # セットアップ状態をリセット
        SetupStatus.reset_setup()

        self.refresh_auth_status()
        messagebox.showinfo("完了", "認証情報をリセットしました。\n再度ログインが必要です。")

    def _check_auth_status(self):
        """認証状態を確認して表示（マルチプラットフォーム対応）"""
        manager = get_credentials_manager()
        auth_status = manager.check_and_update_all_status()

        has_secret = SetupStatus.has_client_secret()
        has_token = SetupStatus.has_token()

        status_text = "認証状態の確認:\n\n"
        status_text += "【YouTube】\n"
        status_text += f"• 認証情報ファイル (client_secret.json): {'✓ 設定済み' if has_secret else '✗ 未設定'}\n"
        status_text += f"• 認証トークン (token.pickle): {'✓ 存在' if has_token else '✗ 未作成'}\n"

        status_text += "\n【ニコニコ動画】\n"
        status_text += f"• ログイン情報: {'✓ 設定済み' if auth_status.get('niconico', False) else '✗ 未設定'}\n"

        # 総合判定
        status_text += "\n─────────────────────\n"
        if has_secret and has_token:
            status_text += "✓ YouTubeは利用可能です。"
        elif has_secret:
            status_text += "⚠ YouTubeへのログインが必要です。"
        else:
            status_text += "✗ YouTubeのセットアップが必要です。"

        messagebox.showinfo("認証状態", status_text)
        self.refresh_auth_status()

    def _open_niconico_auth_dialog(self):
        """ニコニコ動画認証ダイアログを開く"""
        dialog = tk.Toplevel(self.root)
        dialog.title("ニコニコ動画認証設定")
        dialog.geometry("450x400")
        dialog.transient(self.root)
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # タイトル
        ttk.Label(
            main_frame,
            text="📺 ニコニコ動画ログイン設定",
            font=("", 14, "bold")
        ).pack(pady=(0, 15))

        # セキュリティ注意
        ttk.Label(
            main_frame,
            text="🔒 ログイン情報は暗号化して保存されます",
            foreground="blue"
        ).pack()

        # ログイン情報入力
        login_frame = ttk.LabelFrame(main_frame, text="ログイン情報", padding="15")
        login_frame.pack(fill=tk.X, pady=10)

        # メールアドレス
        email_frame = ttk.Frame(login_frame)
        email_frame.pack(fill=tk.X, pady=5)
        ttk.Label(email_frame, text="メールアドレス:", width=15).pack(side=tk.LEFT)
        email_var = tk.StringVar()
        ttk.Entry(email_frame, textvariable=email_var, width=35).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # パスワード
        password_frame = ttk.Frame(login_frame)
        password_frame.pack(fill=tk.X, pady=5)
        ttk.Label(password_frame, text="パスワード:", width=15).pack(side=tk.LEFT)
        password_var = tk.StringVar()
        ttk.Entry(password_frame, textvariable=password_var, width=35, show="●").pack(side=tk.LEFT, fill=tk.X, expand=True)

        manager = get_credentials_manager()
        if manager.has_niconico_credentials():
            creds = manager.get_niconico_credentials()
            if creds:
                email_var.set(creds.get("email", ""))
                # パスワードは表示しない

        status_var = tk.StringVar()
        if manager.has_niconico_credentials():
            status_var.set("✓ 認証情報は設定済みです")
        status_label = ttk.Label(login_frame, textvariable=status_var)
        status_label.pack(pady=(10, 0))

        # ボタン
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=15)

        def save_credentials():
            email = email_var.get().strip()
            password = password_var.get()

            if not email:
                status_var.set("✗ メールアドレスを入力してください")
                status_label.config(foreground="red")
                return

            if not password:
                status_var.set("✗ パスワードを入力してください")
                status_label.config(foreground="red")
                return

            if manager.save_niconico_credentials(email, password):
                status_var.set("✓ 暗号化して保存しました")
                status_label.config(foreground="green")
                password_var.set("")
                self.refresh_auth_status()
            else:
                status_var.set("✗ 保存に失敗しました")
                status_label.config(foreground="red")

        def delete_credentials():
            if messagebox.askyesno("確認", "ニコニコ動画の認証情報を削除しますか？", parent=dialog):
                manager.delete_niconico_credentials()
                email_var.set("")
                password_var.set("")
                status_var.set("✓ 削除しました")
                status_label.config(foreground="green")
                self.refresh_auth_status()

        ttk.Button(btn_frame, text="保存", command=save_credentials).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="削除", command=delete_credentials).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="閉じる", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def _show_about(self):
        """バージョン情報を表示"""
        from update_checker import CURRENT_VERSION
        about_text = (
            "YouTube Playlist Manager\n\n"
            f"バージョン: {CURRENT_VERSION}\n\n"
            "機能:\n"
            "• YouTube再生リストの自動作成\n"
            "• マルチプラットフォーム検索（ニコニコ動画）\n"
            "• プリセット管理\n"
            "• 履歴管理\n"
            "• 統合プレイリストビューワー\n\n"
            "© 2024 YouTube Playlist Manager"
        )
        messagebox.showinfo("バージョン情報", about_text)

    def _check_for_updates(self):
        """更新を確認してダイアログを表示"""
        from update_checker import UpdateChecker

        # ステータス表示
        self.platform_status_var.set("更新を確認中...")

        def check_in_thread():
            result = UpdateChecker.check_for_updates()
            self.root.after(0, lambda: self._show_update_result(result))

        threading.Thread(target=check_in_thread, daemon=True).start()

    def _show_update_result(self, result: dict):
        """更新確認結果を表示"""
        # ステータスを戻す
        self.root.after(500, self.refresh_auth_status)

        if result.get("error"):
            messagebox.showerror("エラー", f"更新の確認に失敗しました:\n{result['error']}")
            return

        if result["update_available"]:
            self._show_update_dialog(result)
        else:
            messagebox.showinfo("更新", f"最新バージョンです (v{result['current_version']})")

    def _show_update_dialog(self, update_info: dict):
        """更新利用可能ダイアログを表示"""
        from update_checker import UpdateChecker

        dialog = tk.Toplevel(self.root)
        dialog.title("更新が利用可能")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # 中央に配置
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 250
        y = (dialog.winfo_screenheight() // 2) - 200
        dialog.geometry(f"+{x}+{y}")

        # コンテンツ
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="新しいバージョンが利用可能です",
                 font=('Arial', 14, 'bold')).pack(pady=10)

        ttk.Label(main_frame, 
         text=f"現在のバージョン: {update_info['current_version']}\n"
              f"最新バージョン: {update_info['latest_version']}",
         font=('Arial', 10)).pack(pady=5)
        # リリースノート
        notes_frame = ttk.LabelFrame(main_frame, text="更新内容", padding=10)
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        notes_text = tk.Text(notes_frame, wrap=tk.WORD, height=10)
        notes_text.insert('1.0', update_info.get('release_notes', ''))
        notes_text.config(state=tk.DISABLED)
        notes_text.pack(fill=tk.BOTH, expand=True)

        # ボタン
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        def download_and_close():
            UpdateChecker.download_update(update_info['download_url'])
            dialog.destroy()

        ttk.Button(btn_frame, text="今すぐダウンロード",
                  command=download_and_close).pack(side=tk.LEFT, padx=5)

        ttk.Button(btn_frame, text="後で",
                  command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def _silent_update_check(self):
        """起動時のサイレント更新チェック"""
        def check():
            from update_checker import UpdateChecker
            result = UpdateChecker.check_for_updates()
            if result.get("update_available"):
                self.root.after(0, lambda: self._show_update_dialog(result))

        threading.Thread(target=check, daemon=True).start()

    def _show_youtube_api_help(self):
        """YouTube API取得方法のヘルプを表示"""
        self._show_api_help_window(
            "YouTube Data API v3 の取得手順",
            """YouTube Data API v3 の取得手順

1. Google Cloud Console にアクセス
   https://console.cloud.google.com/

2. 新規プロジェクトを作成
   - 画面上部の「プロジェクトを選択」をクリック
   - 「新しいプロジェクト」をクリック
   - プロジェクト名: 任意（例: YouTube Playlist Manager）
   - 「作成」をクリック

3. APIライブラリで「YouTube Data API v3」を検索
   - 左側メニューから「APIとサービス」→「ライブラリ」
   - 検索ボックスに「YouTube Data API v3」と入力
   - 検索結果から「YouTube Data API v3」を選択
   - 「有効にする」をクリック

4. 認証情報を作成
   - 左側メニューから「APIとサービス」→「認証情報」
   - 「認証情報を作成」→「OAuth クライアントID」を選択
   - 同意画面の設定が必要な場合は先に設定
     - ユーザーの種類: 外部
     - アプリ名: 任意
     - サポートメール: 自分のメールアドレス

5. OAuth クライアントIDの作成
   - アプリケーションの種類: デスクトップアプリ
   - 名前: 任意（例: Playlist Manager Desktop）
   - 「作成」をクリック

6. JSONをダウンロード
   - 作成したクライアントIDの右側にある
     ダウンロードアイコン (↓) をクリック
   - ファイル名: client_secret_xxxxx.json

7. このアプリでファイルを選択
   - セットアップウィザードでダウンロードした
     JSONファイルを選択してください""",
            "https://console.cloud.google.com/"
        )

    def _show_niconico_help(self):
        """ニコニコ動画のヘルプを表示"""
        self._show_api_help_window(
            "ニコニコ動画のログイン情報",
            """ニコニコ動画のログイン情報

必要な情報:
1. メールアドレス
   - ニコニコ動画アカウントのメールアドレス

2. パスワード
   - ニコニコ動画アカウントのパスワード

セキュリティ:
- パスワードは暗号化して保存されます
- ローカルPC内にのみ保存されます
- インターネットに送信されることはありません
- 暗号化にはcryptographyライブラリを使用

アカウント作成:
https://account.nicovideo.jp/register

注意:
- プレミアム会員でなくても利用可能です
- 一部の機能は無料会員でも使用できます
- APIの利用規約に違反しないようご注意ください
- 短時間に大量のリクエストは避けてください

機能制限（無料会員）:
- 混雑時の視聴制限あり
- 一部のAPIレスポンスが制限される場合あり""",
            "https://account.nicovideo.jp/register"
        )

    def _show_api_help_window(self, title: str, content: str, url: str):
        """API取得方法のヘルプウィンドウを表示"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("650x550")
        dialog.transient(self.root)
        dialog.grab_set()

        # ウィンドウを中央に配置
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # タイトル
        ttk.Label(
            main_frame,
            text=title,
            font=("", 12, "bold")
        ).pack(pady=(0, 10))

        # スクロール可能なテキストエリア
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("MS Gothic", 10),
            padx=10,
            pady=10
        )
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # テキストを挿入
        text_widget.insert("1.0", content)

        # URLをハイライト表示（青色、下線）
        text_widget.tag_configure("url", foreground="blue", underline=True)

        # URLを検索してタグ付け
        import re
        url_pattern = r'https?://[^\s]+'
        start = "1.0"
        while True:
            match = text_widget.search(url_pattern, start, tk.END, regexp=True)
            if not match:
                break
            # URLの終端を見つける
            line_end = text_widget.index(f"{match} lineend")
            url_match = re.match(url_pattern, text_widget.get(match, line_end))
            if url_match:
                end = f"{match}+{len(url_match.group())}c"
                text_widget.tag_add("url", match, end)
                start = end
            else:
                start = f"{match}+1c"

        # URLクリックでブラウザを開く（エラーハンドリング付き）
        def on_url_click(event):
            index = text_widget.index(f"@{event.x},{event.y}")
            tags = text_widget.tag_names(index)
            if "url" in tags:
                # クリック位置のURLを取得
                range_start = text_widget.index(f"{index} linestart")
                range_end = text_widget.index(f"{index} lineend")
                line_text = text_widget.get(range_start, range_end)
                urls = re.findall(url_pattern, line_text)
                if urls:
                    self._open_url_safely(urls[0])

        text_widget.tag_bind("url", "<Button-1>", on_url_click)
        text_widget.config(cursor="arrow")

        def on_enter_url(event):
            text_widget.config(cursor="hand2")

        def on_leave_url(event):
            text_widget.config(cursor="arrow")

        text_widget.tag_bind("url", "<Enter>", on_enter_url)
        text_widget.tag_bind("url", "<Leave>", on_leave_url)

        text_widget.config(state=tk.DISABLED)

        # ボタンフレーム
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        # コピーボタン
        def copy_content():
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("コピー完了", "内容をクリップボードにコピーしました", parent=dialog)

        def copy_url():
            self._copy_to_clipboard(url)

        ttk.Button(btn_frame, text="内容をコピー", command=copy_content, width=15).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="公式サイトを開く", command=lambda: self._open_url_safely(url), width=15).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(btn_frame, text="📋 URLをコピー", command=copy_url, width=15).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(btn_frame, text="閉じる", command=dialog.destroy, width=10).pack(side=tk.RIGHT)

    def _update_platform_checkboxes(self):
        """プラットフォームチェックボックスの状態を認証状態に基づいて更新"""
        try:
            manager = get_credentials_manager()
            auth_status = manager.check_and_update_all_status()

            # YouTube - 常に有効（認証状態は別途チェック）
            if hasattr(self, 'platform_checkboxes') and "youtube" in self.platform_checkboxes:
                youtube_authenticated = auth_status.get("youtube", False)
                if youtube_authenticated:
                    self.platform_checkboxes["youtube"].config(state=tk.NORMAL)
                else:
                    self.platform_checkboxes["youtube"].config(state=tk.DISABLED)
                    self.platform_vars["youtube"].set(False)

            # ニコニコ動画
            if hasattr(self, 'platform_checkboxes') and "niconico" in self.platform_checkboxes:
                niconico_authenticated = auth_status.get("niconico", False)
                if niconico_authenticated:
                    self.platform_checkboxes["niconico"].config(state=tk.NORMAL)
                else:
                    self.platform_checkboxes["niconico"].config(state=tk.DISABLED)
                    self.platform_vars["niconico"].set(False)

        except Exception:
            pass

    def _on_platform_checkbox_click(self, platform: str):
        """プラットフォームチェックボックスがクリックされた時の処理"""
        try:
            manager = get_credentials_manager()
            auth_status = manager.get_auth_status()

            # 認証されていない場合は選択を解除してダイアログを表示
            if not auth_status.get(platform, False):
                self.platform_vars[platform].set(False)

                platform_names = {
                    "niconico": "ニコニコ動画"
                }
                platform_name = platform_names.get(platform, platform)

                result = messagebox.askyesno(
                    "認証が必要です",
                    f"{platform_name}を使用するには認証が必要です。\n\n"
                    f"今すぐ{platform_name}の認証設定を開きますか？",
                    icon="warning"
                )

                if result:
                    if platform == "niconico":
                        self._open_niconico_auth_dialog()

                    # 認証後に再チェック
                    self.root.after(100, self._update_platform_checkboxes)
        except Exception:
            pass

    def _setup_global_mousewheel(self):
        """GUI全体でマウスホイールスクロールを有効化"""
        # すべてのウィジェットに再帰的にバインド
        self.bind_mousewheel(self.root)

    def _is_inside_inner_scrollable(self, widget):
        """ウィジェットが内部スクロール可能エリア内にあるかチェック"""
        current = widget
        while current:
            if current in self._inner_scrollable_widgets:
                return current
            try:
                current = current.master
            except (AttributeError, tk.TclError):
                break
        return None

    def bind_mousewheel(self, widget):
        """ウィジェットとその子要素すべてにマウスホイールをバインド"""

        def _on_mousewheel(event):
            """Windows用マウスホイールハンドラ"""
            # マウスポインタの下にあるウィジェットを取得
            try:
                target_widget = event.widget.winfo_containing(event.x_root, event.y_root)
            except (AttributeError, tk.TclError):
                target_widget = None

            if target_widget is None:
                # メインキャンバスをスクロール
                if hasattr(self, 'main_canvas'):
                    self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return "break"

            # 内部スクロール可能エリアをチェック
            inner_scrollable = self._is_inside_inner_scrollable(target_widget)
            if inner_scrollable:
                # 内部キャンバスのスクロール用情報を取得
                canvas_info = getattr(inner_scrollable, '_scroll_canvas', None)
                if canvas_info:
                    canvas_info.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return "break"

            # デフォルト: メインキャンバスをスクロール
            if hasattr(self, 'main_canvas'):
                self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        def _on_mousewheel_linux(event):
            """Linux/Mac用マウスホイールハンドラ"""
            try:
                target_widget = event.widget.winfo_containing(event.x_root, event.y_root)
            except (AttributeError, tk.TclError):
                target_widget = None

            delta = -1 if event.num == 4 else 1

            if target_widget is None:
                if hasattr(self, 'main_canvas'):
                    self.main_canvas.yview_scroll(delta, "units")
                return "break"

            inner_scrollable = self._is_inside_inner_scrollable(target_widget)
            if inner_scrollable:
                canvas_info = getattr(inner_scrollable, '_scroll_canvas', None)
                if canvas_info:
                    canvas_info.yview_scroll(delta, "units")
                return "break"

            if hasattr(self, 'main_canvas'):
                self.main_canvas.yview_scroll(delta, "units")
            return "break"

        # Windows用バインド
        widget.bind("<MouseWheel>", _on_mousewheel)
        # Linux/Mac用バインド
        widget.bind("<Button-4>", _on_mousewheel_linux)
        widget.bind("<Button-5>", _on_mousewheel_linux)

        # すべての子ウィジェットにも再帰的に適用
        for child in widget.winfo_children():
            self.bind_mousewheel(child)

    def _register_inner_scrollable(self, frame: tk.Widget, canvas: tk.Canvas):
        """内部スクロール可能エリアを登録"""
        self._inner_scrollable_widgets.append(frame)
        frame._scroll_canvas = canvas
        # 新しく登録されたエリアにもマウスホイールをバインド
        self.bind_mousewheel(frame)

    def _create_widgets(self):
        """ウィジェットを作成（縦長スクロールレイアウト）"""
        # スタイル設定
        style = ttk.Style()
        style.configure("Section.TLabelframe", padding=15)
        style.configure("Section.TLabelframe.Label", font=("", 10, "bold"))
        # キーワードタブ用スクロールバー（幅10px）
        style.configure("Keyword.Vertical.TScrollbar", width=10)
        # 地域チェックボックス用スタイル（フォントサイズ拡大）
        style.configure('Region.TCheckbutton', font=('', 10))

        # ========================================
        # 固定ヘッダー
        # ========================================
        header_frame = ttk.Frame(self.root, padding="15 10 15 10")
        header_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            header_frame,
            text="YouTube Playlist Manager",
            font=("", 18, "bold")
        )
        title_label.pack()

        # セパレータ
        ttk.Separator(self.root, orient="horizontal").pack(fill=tk.X)

        # ========================================
        # メインコンテンツエリア（スクロール可能）
        # ========================================
        content_container = ttk.Frame(self.root)
        content_container.pack(fill=tk.BOTH, expand=True)

        # スクロール可能なキャンバス
        self.main_canvas = tk.Canvas(
            content_container,
            highlightthickness=0,
            bg="#f0f0f0"
        )

        # スクロールバー（カスタムスタイル）
        self.main_scrollbar = ttk.Scrollbar(
            content_container,
            orient="vertical",
            command=self.main_canvas.yview
        )

        # スクロール可能なフレーム
        self.scrollable_frame = ttk.Frame(self.main_canvas, padding="15")

        # フレームのサイズ変更時にスクロール領域を更新
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        # キャンバスにフレームを配置
        self.canvas_window = self.main_canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        # キャンバスのサイズ変更時にフレームの幅を調整
        def _on_canvas_configure(event):
            canvas_width = event.width
            self.main_canvas.itemconfig(self.canvas_window, width=canvas_width - 4)
        self.main_canvas.bind("<Configure>", _on_canvas_configure)

        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)

        # グローバルマウスホイールスクロールを有効化（ウィジェット作成後に呼び出し）
        self.root.after(100, self._setup_global_mousewheel)

        # レイアウト
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ========================================
        # セクション1: 基本設定
        # ========================================
        self.basic_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text=t('section_basic'),
            padding="15",
            style="Section.TLabelframe"
        )
        self.basic_frame.pack(fill=tk.X, pady=(0, 20))

        # 基本設定を横並びグリッドで配置
        basic_grid = ttk.Frame(self.basic_frame)
        basic_grid.pack(fill=tk.X)

        # 年代
        self.era_label_widget = ttk.Label(basic_grid, text=t('label_era'))
        self.era_label_widget.grid(row=0, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.era_var = tk.StringVar(value=self.ERAS[0])
        era_combo = ttk.Combobox(
            basic_grid,
            textvariable=self.era_var,
            values=self.ERAS,
            state="readonly",
            width=15
        )
        era_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(0, 30))

        # カテゴリ
        self.category_label_widget = ttk.Label(basic_grid, text=t('label_category'))
        self.category_label_widget.grid(row=0, column=2, sticky=tk.W, pady=5, padx=(0, 10))
        self.category_var = tk.StringVar(value=self.CATEGORIES[0])
        category_combo = ttk.Combobox(
            basic_grid,
            textvariable=self.category_var,
            values=self.CATEGORIES,
            state="readonly",
            width=15
        )
        category_combo.grid(row=0, column=3, sticky=tk.W, pady=5)

        # 動画数
        count_frame = ttk.Frame(self.basic_frame)
        count_frame.pack(fill=tk.X, pady=(10, 0))

        self.video_count_label_widget = ttk.Label(count_frame, text=t('label_video_count'))
        self.video_count_label_widget.pack(side=tk.LEFT, padx=(0, 10))

        self.video_count_var = tk.IntVar(value=20)
        self.video_count_slider = ttk.Scale(
            count_frame,
            from_=1,
            to=50,
            orient=tk.HORIZONTAL,
            variable=self.video_count_var,
            command=self._on_slider_change,
            length=300
        )
        self.video_count_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.video_count_label = ttk.Label(count_frame, text="20", width=4, font=("", 10, "bold"))
        self.video_count_label.pack(side=tk.LEFT, padx=(10, 0))

        self.video_count_entry = ttk.Entry(count_frame, width=5)
        self.video_count_entry.insert(0, "20")
        self.video_count_entry.pack(side=tk.LEFT, padx=(10, 0))
        self.video_count_entry.bind("<Return>", self._on_entry_change)
        self.video_count_entry.bind("<FocusOut>", self._on_entry_change)

        self.video_range_label = ttk.Label(count_frame, text=t('label_video_range'), foreground="gray")
        self.video_range_label.pack(side=tk.LEFT, padx=(5, 0))

        # ========================================
        # セクション2: キーワード・地域（統合版）
        # ========================================
        self.keyword_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text=t('section_keywords'),
            padding="15",
            style="Section.TLabelframe"
        )
        self.keyword_frame.pack(fill=tk.X, pady=(0, 20))

        # 地域チェックボックス用の変数を格納する辞書（タブ作成前に初期化）
        self.region_vars = {}
        self.region_group_var = tk.StringVar(value="全世界")
        self.country_var = tk.StringVar(value="全世界")

        # タブコントロール
        self.keyword_notebook = ttk.Notebook(self.keyword_frame)
        self.keyword_notebook.pack(fill=tk.BOTH, expand=True)

        # 各タブを作成（2-3列配置、高さ150px）
        for tab_key, keywords in self.KEYWORD_TABS.items():
            tab_frame = ttk.Frame(self.keyword_notebook)
            self.keyword_notebook.add(tab_frame, text=t(tab_key))

            # スクロール可能なキャンバスを作成（高さ150px）
            tab_canvas = tk.Canvas(tab_frame, highlightthickness=0, height=150)
            # スクロールバー（幅10px）
            tab_scrollbar = ttk.Scrollbar(
                tab_frame,
                orient="vertical",
                command=tab_canvas.yview,
                style="Keyword.Vertical.TScrollbar"
            )
            tab_scrollable = ttk.Frame(tab_canvas, padding="10")

            tab_scrollable.bind(
                "<Configure>",
                lambda e, c=tab_canvas: c.configure(scrollregion=c.bbox("all"))
            )

            tab_canvas_window = tab_canvas.create_window((0, 0), window=tab_scrollable, anchor="nw")

            # キャンバスのサイズ変更時にフレームの幅を調整
            def _on_tab_canvas_configure(event, canvas=tab_canvas, window=tab_canvas_window):
                canvas.itemconfig(window, width=event.width - 20)
            tab_canvas.bind("<Configure>", _on_tab_canvas_configure)

            tab_canvas.configure(yscrollcommand=tab_scrollbar.set)

            tab_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            tab_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # 内部スクロール可能エリアとして登録（グローバルマウスホイールハンドラで使用）
            self._register_inner_scrollable(tab_scrollable, tab_canvas)

            # チェックボックスを配置（3列配置、縦並び）
            num_cols = 3
            for i, keyword in enumerate(keywords):
                var = tk.BooleanVar(value=False)
                # Store with API keyword as key (for API calls)
                self.keyword_vars[keyword] = var
                cb = ttk.Checkbutton(
                    tab_scrollable,
                    text=t_keyword(keyword),  # Display translated name
                    variable=var
                )
                row = i // num_cols
                col = i % num_cols
                cb.grid(row=row, column=col, sticky=tk.W, padx=15, pady=5)

            # 列の幅を均等に
            for col in range(num_cols):
                tab_scrollable.columnconfigure(col, weight=1)

            # チェックボックス追加後に再度マウスホイールをバインド
            self.bind_mousewheel(tab_scrollable)

        # ========================================
        # 地域タブ（すべての地域を1つのタブに配置）
        # ========================================
        region_tab_frame = ttk.Frame(self.keyword_notebook)
        self.keyword_notebook.add(region_tab_frame, text=t('tab_region'))

        # スクロール可能なキャンバスを作成（高さ180px）
        region_canvas = tk.Canvas(region_tab_frame, highlightthickness=0, height=180)
        region_scrollbar = ttk.Scrollbar(
            region_tab_frame,
            orient="vertical",
            command=region_canvas.yview,
            style="Keyword.Vertical.TScrollbar"
        )
        region_scrollable = ttk.Frame(region_canvas, padding="10")

        region_scrollable.bind(
            "<Configure>",
            lambda e: region_canvas.configure(scrollregion=region_canvas.bbox("all"))
        )

        region_canvas_window = region_canvas.create_window((0, 0), window=region_scrollable, anchor="nw")

        def _on_region_canvas_configure(event):
            region_canvas.itemconfig(region_canvas_window, width=event.width - 20)
        region_canvas.bind("<Configure>", _on_region_canvas_configure)

        region_canvas.configure(yscrollcommand=region_scrollbar.set)

        region_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        region_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 内部スクロール可能エリアとして登録
        self._register_inner_scrollable(region_scrollable, region_canvas)

        # すべての地域をフラットなリストにまとめる
        all_regions = self.REGION_LIST

        # チェックボックスを配置（4列配置）
        num_cols = 4
        for i, region in enumerate(all_regions):
            # 全世界はデフォルトでチェック
            default_value = (region == "worldwide")
            var = tk.BooleanVar(value=default_value)
            # Store with internal key (Japanese) for API/config compatibility
            self.region_vars[region] = var
            cb = ttk.Checkbutton(
                region_scrollable,
                text=t_region(region),  # Display translated name
                variable=var
            )
            row = i // num_cols
            col = i % num_cols
            cb.grid(row=row, column=col, sticky=tk.W, padx=10, pady=3)

        # 列の幅を均等に
        for col in range(num_cols):
            region_scrollable.columnconfigure(col, weight=1)

        # マウスホイールをバインド
        self.bind_mousewheel(region_scrollable)

        # 地域変更時に表示を更新
        for var in self.region_vars.values():
            var.trace_add("write", self._update_selected_regions_display)

        # 追加キーワード入力欄
        additional_frame = ttk.Frame(self.keyword_frame)
        additional_frame.pack(fill=tk.X, pady=(15, 0))
        self.additional_keyword_label = ttk.Label(additional_frame, text=t('additional_keyword'))
        self.additional_keyword_label.pack(side=tk.LEFT)
        self.keyword_var = tk.StringVar()
        keyword_entry = ttk.Entry(additional_frame, textvariable=self.keyword_var, width=40)
        keyword_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        # 選択中キーワード表示（大きく）
        selected_frame = ttk.Frame(self.keyword_frame)
        selected_frame.pack(fill=tk.X, pady=(10, 0))
        self.selected_keywords_var = tk.StringVar(value=t('selected_keywords'))
        selected_label = ttk.Label(
            selected_frame,
            textvariable=self.selected_keywords_var,
            foreground="blue",
            font=("", 10, "bold")
        )
        selected_label.pack(anchor=tk.W)

        # キーワード変更時に表示を更新
        for var in self.keyword_vars.values():
            var.trace_add("write", self._update_selected_keywords_display)

        # 選択中の地域表示
        selected_regions_frame = ttk.Frame(self.keyword_frame)
        selected_regions_frame.pack(fill=tk.X, pady=(10, 0))
        self.selected_regions_var = tk.StringVar(value=t('region_selected'))
        selected_regions_label = ttk.Label(
            selected_regions_frame,
            textvariable=self.selected_regions_var,
            foreground="green",
            font=("", 10, "bold")
        )
        selected_regions_label.pack(anchor=tk.W)

        # 地域オプション
        region_options_frame = ttk.Frame(self.keyword_frame)
        region_options_frame.pack(fill=tk.X, pady=(5, 0))

        self.add_region_keywords_var = tk.BooleanVar(value=True)
        self.region_keyword_cb = ttk.Checkbutton(
            region_options_frame,
            text=t('region_keyword_auto'),
            variable=self.add_region_keywords_var
        )
        self.region_keyword_cb.pack(side=tk.LEFT)

        # 地域コード表示ラベル
        self.region_code_var = tk.StringVar(value=t('region_code_none'))
        region_code_label = ttk.Label(region_options_frame, textvariable=self.region_code_var, foreground="gray")
        region_code_label.pack(side=tk.RIGHT)

        # ========================================
        # セクション3: 検索オプション（拡張版）
        # ========================================
        self.search_options_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text=t('section_search_options'),
            padding="15",
            style="Section.TLabelframe"
        )
        self.search_options_frame.pack(fill=tk.X, pady=(0, 20))

        # 検索精度セクション
        self.precision_label = ttk.Label(self.search_options_frame, text=t('search_precision_label'), font=("", 10, "bold"))
        self.precision_label.pack(anchor=tk.W)

        self.search_precision_var = tk.StringVar(value="standard")

        # 各精度オプションを詳細説明付きで表示
        # Store references for language updates
        self.precision_radio_frames = []
        precision_options = [
            ("standard", 'precision_standard', 'precision_standard_desc'),
            ("high", 'precision_high', 'precision_high_desc'),
            ("highest", 'precision_highest', 'precision_highest_desc'),
        ]

        for value, label_key, desc_key in precision_options:
            option_frame = ttk.Frame(self.search_options_frame)
            option_frame.pack(fill=tk.X, padx=(20, 0), pady=3)

            rb = ttk.Radiobutton(
                option_frame,
                text=t(label_key),
                variable=self.search_precision_var,
                value=value
            )
            rb.pack(side=tk.LEFT)

            desc_label = ttk.Label(
                option_frame,
                text=f"  └ {t(desc_key)}",
                foreground="gray"
            )
            desc_label.pack(side=tk.LEFT, padx=(10, 0))

            # Store references for language updates
            self.precision_radio_frames.append((option_frame, rb, desc_label, label_key, desc_key))

        # 説明ラベル
        self.precision_hint_var = tk.StringVar(value="")

        # 精度変更時の説明更新
        def _on_precision_change(*args):
            pass  # 詳細説明が常に表示されているので不要
        self.search_precision_var.trace_add("write", _on_precision_change)

        # セパレータ
        ttk.Separator(self.search_options_frame, orient="horizontal").pack(fill=tk.X, pady=15)

        # 公式チャンネル優先設定
        self.official_label = ttk.Label(self.search_options_frame, text=t('section_official_channel'), font=("", 10, "bold"))
        self.official_label.pack(anchor=tk.W)

        official_options_frame = ttk.Frame(self.search_options_frame)
        official_options_frame.pack(fill=tk.X, padx=(20, 0), pady=(5, 0))

        self.prefer_official_var = tk.BooleanVar(value=True)
        self.prefer_official_cb = ttk.Checkbutton(
            official_options_frame,
            text=t('option_official_channel'),
            variable=self.prefer_official_var
        )
        self.prefer_official_cb.grid(row=0, column=0, sticky=tk.W, pady=2)

        # 追加の詳細設定
        self.require_verified_var = tk.BooleanVar(value=False)
        self.verified_cb = ttk.Checkbutton(
            official_options_frame,
            text=t('option_verified_badge'),
            variable=self.require_verified_var
        )
        self.verified_cb.grid(row=0, column=1, sticky=tk.W, padx=(30, 0), pady=2)

        self.min_subscribers_var = tk.BooleanVar(value=False)
        self.subscribers_cb = ttk.Checkbutton(
            official_options_frame,
            text=t('option_subscriber_100k'),
            variable=self.min_subscribers_var
        )
        self.subscribers_cb.grid(row=1, column=0, sticky=tk.W, pady=2)

        self.min_views_var = tk.BooleanVar(value=False)
        self.views_cb = ttk.Checkbutton(
            official_options_frame,
            text=t('option_video_views_100k'),
            variable=self.min_views_var
        )
        self.views_cb.grid(row=1, column=1, sticky=tk.W, padx=(30, 0), pady=2)

        self.vevo_only_var = tk.BooleanVar(value=False)
        self.vevo_cb = ttk.Checkbutton(
            official_options_frame,
            text=t('option_vevo_only'),
            variable=self.vevo_only_var
        )
        self.vevo_cb.grid(row=2, column=0, sticky=tk.W, pady=2)

        # 詳細説明オプション
        self.add_detailed_description_var = tk.BooleanVar(value=True)
        self.detailed_desc_cb = ttk.Checkbutton(
            official_options_frame,
            text=t('option_add_detailed_desc'),
            variable=self.add_detailed_description_var
        )
        self.detailed_desc_cb.grid(row=2, column=1, sticky=tk.W, padx=(30, 0), pady=2)

        # ========================================
        # セクション5: プライバシー設定
        # ========================================
        self.privacy_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text=t('section_privacy'),
            padding="15",
            style="Section.TLabelframe"
        )
        self.privacy_frame.pack(fill=tk.X, pady=(0, 20))

        privacy_options_frame = ttk.Frame(self.privacy_frame)
        privacy_options_frame.pack(fill=tk.X)

        self.privacy_var = tk.StringVar(value="private")
        # Store references for language updates
        self.privacy_radio_buttons = []
        privacy_options = [
            ("private", 'privacy_private', 'privacy_private_desc'),
            ("unlisted", 'privacy_unlisted', 'privacy_unlisted_desc'),
            ("public", 'privacy_public', 'privacy_public_desc'),
        ]

        for i, (value, label_key, desc_key) in enumerate(privacy_options):
            rb = ttk.Radiobutton(
                privacy_options_frame,
                text=f"{t(label_key)}  ({t(desc_key)})",
                variable=self.privacy_var,
                value=value
            )
            rb.pack(anchor=tk.W, pady=3)
            self.privacy_radio_buttons.append((rb, label_key, desc_key))

        # ========================================
        # セクション6: プラットフォーム
        # ========================================
        self.platform_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text=t('section_platform'),
            padding="15",
            style="Section.TLabelframe"
        )
        self.platform_frame.pack(fill=tk.X, pady=(0, 20))

        platform_options_frame = ttk.Frame(self.platform_frame)
        platform_options_frame.pack(fill=tk.X)

        self.platform_checkboxes = {}

        self.platform_vars["youtube"] = tk.BooleanVar(value=True)
        self.platform_checkboxes["youtube"] = ttk.Checkbutton(
            platform_options_frame,
            text=t('platform_youtube'),
            variable=self.platform_vars["youtube"],
        )
        self.platform_checkboxes["youtube"].pack(side=tk.LEFT, padx=(0, 30))

        self.platform_vars["niconico"] = tk.BooleanVar(value=False)
        self.platform_checkboxes["niconico"] = ttk.Checkbutton(
            platform_options_frame,
            text=t('platform_niconico'),
            variable=self.platform_vars["niconico"],
            command=lambda: self._on_platform_checkbox_click("niconico")
        )
        self.platform_checkboxes["niconico"].pack(side=tk.LEFT)

        # プラットフォームの認証状態を初期化
        self.root.after(600, self._update_platform_checkboxes)

        # ========================================
        # セクション7: プリセット
        # ========================================
        self.preset_section_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text=t('section_preset'),
            padding="15",
            style="Section.TLabelframe"
        )
        self.preset_section_frame.pack(fill=tk.X, pady=(0, 20))

        preset_row = ttk.Frame(self.preset_section_frame)
        preset_row.pack(fill=tk.X)

        self.preset_label = ttk.Label(preset_row, text=t('label_preset'))
        self.preset_label.pack(side=tk.LEFT)
        self.preset_var = tk.StringVar()
        self.preset_combo = ttk.Combobox(
            preset_row,
            textvariable=self.preset_var,
            values=self.preset_manager.get_preset_names(),
            state="readonly",
            width=25
        )
        self.preset_combo.pack(side=tk.LEFT, padx=(10, 20))

        # プリセットボタンをリストに保存
        self.preset_buttons = []
        self.preset_button_keys = ['btn_load', 'btn_save', 'btn_delete', 'btn_edit']
        for text_key, cmd in [(t('btn_load'), self._load_preset), (t('btn_save'), self._save_preset),
                          (t('btn_delete'), self._delete_preset), (t('btn_edit'), self._edit_preset)]:
            btn = ttk.Button(preset_row, text=text_key, command=cmd, width=8)
            btn.pack(side=tk.LEFT, padx=(0, 5))
            self.preset_buttons.append(btn)

        # ========================================
        # セクション8: 実行ボタン
        # ========================================
        button_frame = ttk.Frame(self.scrollable_frame, padding="15")
        button_frame.pack(fill=tk.X, pady=(0, 20))

        self.execute_btn = ttk.Button(
            button_frame,
            text=t('btn_create_playlist'),
            command=self._execute,
            width=25
        )
        self.execute_btn.pack(side=tk.LEFT, padx=(0, 15))

        self.cancel_btn = ttk.Button(
            button_frame,
            text=t('btn_cancel'),
            command=self._cancel,
            state=tk.DISABLED,
            width=15
        )
        self.cancel_btn.pack(side=tk.LEFT)

        # ========================================
        # セパレータ
        # ========================================
        ttk.Separator(self.root, orient="horizontal").pack(fill=tk.X)

        # ========================================
        # 固定フッター: 進行状況
        # ========================================
        footer_frame = ttk.Frame(self.root, padding="10 10 10 5")
        footer_frame.pack(fill=tk.X)

        self.progress_label_frame = ttk.LabelFrame(footer_frame, text=t('section_progress'), padding="8")
        self.progress_label_frame.pack(fill=tk.X)

        self.progress_var = tk.StringVar(value=t('progress_waiting'))
        self.progress_label = ttk.Label(self.progress_label_frame, textvariable=self.progress_var)
        self.progress_label.pack(fill=tk.X)

        self.progress_bar = ttk.Progressbar(
            self.progress_label_frame,
            mode="indeterminate",
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))

        # ========================================
        # 結果表示エリア（スクロール可能フレーム内に配置）
        # ========================================
        self.result_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text=t('section_result'),
            padding="15",
            style="Section.TLabelframe"
        )
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # 結果表示用のスクロール可能なフレーム
        result_canvas = tk.Canvas(self.result_frame, height=150, highlightthickness=0)
        result_scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=result_canvas.yview)
        self.result_scrollable_frame = ttk.Frame(result_canvas)

        self.result_scrollable_frame.bind(
            "<Configure>",
            lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all"))
        )

        result_canvas.create_window((0, 0), window=self.result_scrollable_frame, anchor="nw")
        result_canvas.configure(yscrollcommand=result_scrollbar.set)

        result_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_canvas = result_canvas

        # 内部スクロール可能エリアとして登録（グローバルマウスホイールハンドラで使用）
        self._register_inner_scrollable(self.result_scrollable_frame, result_canvas)

        # テキスト結果も残す（ログ表示用）
        self.result_text = scrolledtext.ScrolledText(
            self.result_frame,
            wrap=tk.WORD,
            height=5,
            font=("Consolas", 9)
        )
        self.result_text.pack(fill=tk.X, pady=(10, 0))
        self.result_text.config(state=tk.DISABLED)

        # URL表示とコピーボタン
        url_frame = ttk.Frame(self.result_frame)
        url_frame.pack(fill=tk.X, pady=(10, 0))

        self.url_label_widget = ttk.Label(url_frame, text=t('label_playlist_url'))
        self.url_label_widget.pack(side=tk.LEFT)

        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, state="readonly", width=50)
        self.url_entry.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)

        self.copy_btn = ttk.Button(url_frame, text=t('btn_copy_url'), command=self._copy_url, width=10, state=tk.DISABLED)
        self.copy_btn.pack(side=tk.LEFT, padx=(5, 0))

        self.open_btn = ttk.Button(url_frame, text=t('btn_open'), command=self._open_playlist, width=8, state=tk.DISABLED)
        self.open_btn.pack(side=tk.LEFT, padx=(5, 0))

        self.view_videos_btn = ttk.Button(
            url_frame,
            text="📺 動画確認",
            command=self._view_playlist_videos,
            width=12,
            state=tk.DISABLED
        )
        self.view_videos_btn.pack(side=tk.LEFT, padx=(5, 0))

        # ========================================
        # 履歴フレーム
        # ========================================
        self.history_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text=t('section_history'),
            padding="15",
            style="Section.TLabelframe"
        )
        self.history_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # 履歴操作ボタン
        history_btn_frame = ttk.Frame(self.history_frame)
        history_btn_frame.pack(fill=tk.X, pady=(0, 10))

        # Store button references for language updates
        self.history_buttons = {}
        self.history_buttons['refresh'] = ttk.Button(history_btn_frame, text=t('btn_refresh'), command=self._refresh_history, width=8)
        self.history_buttons['refresh'].pack(side=tk.LEFT, padx=(0, 5))
        self.history_buttons['delete_all'] = ttk.Button(history_btn_frame, text=t('btn_delete_all'), command=self._clear_history, width=8)
        self.history_buttons['delete_all'].pack(side=tk.LEFT, padx=(0, 5))
        self.history_buttons['export'] = ttk.Button(history_btn_frame, text=t('btn_export'), command=self._export_history, width=12)
        self.history_buttons['export'].pack(side=tk.LEFT, padx=(0, 5))
        self.history_buttons['import'] = ttk.Button(history_btn_frame, text=t('btn_import'), command=self._import_history, width=12)
        self.history_buttons['import'].pack(side=tk.LEFT, padx=(0, 5))

        # 履歴リスト（Treeview）
        history_tree_frame = ttk.Frame(self.history_frame)
        history_tree_frame.pack(fill=tk.BOTH, expand=True)

        self.history_tree = ttk.Treeview(
            history_tree_frame,
            columns=("date", "title", "videos", "platform", "category", "era"),
            show="headings",
            height=5
        )
        self.history_tree.heading("date", text=t('col_created_date'))
        self.history_tree.heading("title", text=t('col_title'))
        self.history_tree.heading("videos", text=t('col_video_count'))
        self.history_tree.heading("platform", text=t('col_platform'))
        self.history_tree.heading("category", text=t('col_category'))
        self.history_tree.heading("era", text=t('col_era'))

        self.history_tree.column("date", width=100)
        self.history_tree.column("title", width=180)
        self.history_tree.column("videos", width=50)
        self.history_tree.column("platform", width=70)
        self.history_tree.column("category", width=70)
        self.history_tree.column("era", width=60)

        history_scrollbar = ttk.Scrollbar(history_tree_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 履歴アクションボタン
        history_action_frame = ttk.Frame(self.history_frame)
        history_action_frame.pack(fill=tk.X, pady=(10, 0))

        # Store action button references for language updates
        self.history_action_buttons = {}
        self.history_action_buttons['recreate'] = ttk.Button(history_action_frame, text=t('btn_recreate_same'), command=self._recreate_from_history, width=14)
        self.history_action_buttons['recreate'].pack(side=tk.LEFT, padx=(0, 5))
        self.history_action_buttons['open_url'] = ttk.Button(history_action_frame, text=t('btn_open_url'), command=self._open_history_url, width=12)
        self.history_action_buttons['open_url'].pack(side=tk.LEFT, padx=(0, 5))
        self.history_action_buttons['video_confirm'] = ttk.Button(history_action_frame, text=f"📺 {t('btn_video_confirm')}", command=self._view_history_videos, width=12)
        self.history_action_buttons['video_confirm'].pack(side=tk.LEFT, padx=(0, 5))
        self.history_action_buttons['delete'] = ttk.Button(history_action_frame, text=t('btn_delete_history'), command=self._delete_history_entry, width=12)
        self.history_action_buttons['delete'].pack(side=tk.LEFT, padx=(0, 5))
        self.history_action_buttons['csv_export'] = ttk.Button(history_action_frame, text=t('btn_csv_export'), command=self._export_history_csv, width=10)
        self.history_action_buttons['csv_export'].pack(side=tk.LEFT, padx=(0, 5))

        # 履歴を初期表示
        self._refresh_history()

        # ========================================
        # 統合プレイリストビューワーフレーム
        # ========================================
        self.integrated_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text=t('section_integrated_viewer'),
            padding="15",
            style="Section.TLabelframe"
        )
        self.integrated_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # 統合プレイリスト操作ボタン
        int_btn_frame = ttk.Frame(self.integrated_frame)
        int_btn_frame.pack(fill=tk.X, pady=(0, 10))

        # Store button references for language updates
        self.integrated_buttons = {}
        self.integrated_buttons['refresh'] = ttk.Button(int_btn_frame, text=t('btn_refresh'), command=self._refresh_integrated_playlists, width=8)
        self.integrated_buttons['refresh'].pack(side=tk.LEFT, padx=(0, 5))
        self.integrated_buttons['create_new'] = ttk.Button(int_btn_frame, text=t('btn_create_new'), command=self._create_new_integrated_playlist, width=10)
        self.integrated_buttons['create_new'].pack(side=tk.LEFT, padx=(0, 5))
        self.integrated_buttons['json_export'] = ttk.Button(int_btn_frame, text=t('btn_json_export'), command=self._export_integrated_json, width=10)
        self.integrated_buttons['json_export'].pack(side=tk.LEFT, padx=(0, 5))
        self.integrated_buttons['html_export'] = ttk.Button(int_btn_frame, text=t('btn_html_export'), command=self._export_integrated_html, width=10)
        self.integrated_buttons['html_export'].pack(side=tk.LEFT, padx=(0, 5))
        self.integrated_buttons['delete'] = ttk.Button(int_btn_frame, text=t('btn_delete'), command=self._delete_integrated_playlist, width=8)
        self.integrated_buttons['delete'].pack(side=tk.LEFT, padx=(0, 5))

        # 統合プレイリストリスト（Treeview）
        int_tree_frame = ttk.Frame(self.integrated_frame)
        int_tree_frame.pack(fill=tk.BOTH, expand=True)

        self.integrated_tree = ttk.Treeview(
            int_tree_frame,
            columns=("date", "title", "videos", "youtube", "niconico"),
            show="headings",
            height=4
        )
        self.integrated_tree.heading("date", text=t('col_created_date'))
        self.integrated_tree.heading("title", text=t('col_title'))
        self.integrated_tree.heading("videos", text=t('col_total'))
        self.integrated_tree.heading("youtube", text=t('col_youtube'))
        self.integrated_tree.heading("niconico", text=t('col_niconico'))

        self.integrated_tree.column("date", width=100)
        self.integrated_tree.column("title", width=200)
        self.integrated_tree.column("videos", width=50)
        self.integrated_tree.column("youtube", width=60)
        self.integrated_tree.column("niconico", width=60)

        int_scrollbar = ttk.Scrollbar(int_tree_frame, orient="vertical", command=self.integrated_tree.yview)
        self.integrated_tree.configure(yscrollcommand=int_scrollbar.set)

        self.integrated_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        int_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ダブルクリックでビューワーを開く
        self.integrated_tree.bind("<Double-1>", self._open_integrated_viewer)

        # 統合プレイリストを初期表示
        self._refresh_integrated_playlists()

    def _on_region_group_change(self, event=None):
        """地域グループ変更時のコールバック（チェックボックス対応）"""
        # チェックボックス使用時は_update_selected_regionsで処理
        pass

    def _update_selected_regions(self):
        """選択された地域を更新（後方互換性用）"""
        # 新しい_update_selected_regions_displayに処理を委譲
        self._update_selected_regions_display()

    def _get_selected_regions(self):
        """選択された地域のリストを取得"""
        return [country for country, var in self.region_vars.items() if var.get()]

    def _update_region_code_display(self):
        """地域コード表示を更新"""
        country = self.country_var.get() if hasattr(self, 'country_var') else ""
        if not country:
            self.region_code_var.set("(regionCode: なし)")
            return
        code = get_region_code(country)
        if code:
            self.region_code_var.set(f"(regionCode: {code})")
        else:
            self.region_code_var.set("(regionCode: なし)")

    def _update_selected_keywords_display(self, *args):
        """選択中のキーワードを表示更新"""
        selected = [kw for kw, var in self.keyword_vars.items() if var.get()]
        if selected:
            # Display translated keyword names
            display_names = [t_keyword(kw) for kw in selected]
            prefix = "Selected: " if get_current_language() == 'en' else "選択中: "
            self.selected_keywords_var.set(f"{prefix}{', '.join(display_names)}")
        else:
            self.selected_keywords_var.set(t('selected_keywords'))

    def _update_selected_regions_display(self, *args):
        """選択中の地域を表示更新（trace_add用）"""
        # 再帰呼び出し防止
        if hasattr(self, '_updating_regions') and self._updating_regions:
            return
        self._updating_regions = True

        try:
            selected = [region for region, var in self.region_vars.items() if var.get()]

            # 表示を更新
            if selected:
                # Display translated region names
                display_names = [t_region(region) for region in selected]
                prefix = t('region_selected') + " "
                if len(selected) <= 5:
                    self.selected_regions_var.set(f"{prefix}{', '.join(display_names)}")
                else:
                    # Show first 5 regions and count of remaining
                    self.selected_regions_var.set(f"{prefix}{', '.join(display_names[:5])}... (+{len(selected) - 5})")
                self.country_var.set(selected[0])
            else:
                none_text = t('region_selected') + " " + t('region_none')
                self.selected_regions_var.set(none_text)
                self.country_var.set("")

            # 地域コード表示を更新
            self._update_region_code_display()
        finally:
            self._updating_regions = False

    def _get_selected_keywords(self) -> list[str]:
        """選択されたキーワードを取得"""
        return [kw for kw, var in self.keyword_vars.items() if var.get()]

    def _on_slider_change(self, value):
        """スライダー変更時"""
        int_value = int(float(value))
        self.video_count_label.config(text=str(int_value))
        self.video_count_entry.delete(0, tk.END)
        self.video_count_entry.insert(0, str(int_value))

    def _on_entry_change(self, event=None):
        """入力欄変更時"""
        try:
            value = int(self.video_count_entry.get())
            value = max(1, min(50, value))
            self.video_count_var.set(value)
            self.video_count_label.config(text=str(value))
            self.video_count_entry.delete(0, tk.END)
            self.video_count_entry.insert(0, str(value))
        except ValueError:
            pass

    def _update_progress(self, message: str):
        """進行状況を更新"""
        self.progress_var.set(message)

    def _append_result(self, text: str):
        """結果テキストに追加"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)

    def _clear_result(self):
        """結果テキストをクリア"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.url_var.set("")
        self.copy_btn.config(state=tk.DISABLED)
        self.open_btn.config(state=tk.DISABLED)
        self.view_videos_btn.config(state=tk.DISABLED)

        # 現在のプレイリスト情報をクリア
        self.current_playlist_id = None
        self.current_playlist_title = None

        # 動画カードをクリア
        for widget in self.result_scrollable_frame.winfo_children():
            widget.destroy()

    def _copy_url(self):
        """URLをクリップボードにコピー"""
        url = self.url_var.get()
        if url:
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            messagebox.showinfo("コピー完了", "URLをクリップボードにコピーしました")

    def _open_playlist(self):
        """プレイリストをブラウザで開く"""
        url = self.url_var.get()
        if url:
            webbrowser.open(url)

    def _view_playlist_videos(self):
        """作成したプレイリストの動画を確認"""
        if self.current_playlist_id and self.current_playlist_title:
            self.show_playlist_videos(self.current_playlist_id, self.current_playlist_title)
        else:
            messagebox.showwarning("エラー", "プレイリスト情報がありません")

    # ========================================
    # プリセット操作メソッド
    # ========================================

    def _get_current_settings(self) -> PresetSettings:
        """現在のGUI設定をPresetSettingsとして取得"""
        return PresetSettings(
            era=self.era_var.get(),
            category=self.category_var.get(),
            keywords=self._get_selected_keywords(),
            additional_keyword=self.keyword_var.get().strip(),
            region_group=self.region_group_var.get(),
            country=self.country_var.get(),
            video_count=int(self.video_count_var.get()),
            privacy=self.privacy_var.get(),
            prefer_official=self.prefer_official_var.get(),
            search_precision=self.search_precision_var.get(),
            add_region_keywords=self.add_region_keywords_var.get(),
            add_detailed_description=self.add_detailed_description_var.get(),
            platforms=self._get_selected_platforms(),
        )

    def _get_selected_platforms(self) -> list[str]:
        """選択されたプラットフォームを取得"""
        return [p for p, var in self.platform_vars.items() if var.get()]

    def _apply_preset_settings(self, settings: PresetSettings):
        """PresetSettingsをGUIに適用"""
        # 年代
        if settings.era in self.ERAS:
            self.era_var.set(settings.era)

        # カテゴリ
        if settings.category in self.CATEGORIES:
            self.category_var.set(settings.category)

        # キーワード
        for kw, var in self.keyword_vars.items():
            var.set(kw in settings.keywords)

        # 追加キーワード
        self.keyword_var.set(settings.additional_keyword)

        # 地域（チェックボックス形式）
        # 全てのチェックボックスをリセット
        for region, var in self.region_vars.items():
            var.set(False)
        # 保存された地域を選択
        if settings.country and settings.country in self.region_vars:
            self.region_vars[settings.country].set(True)
        else:
            # デフォルトは全世界
            if "全世界" in self.region_vars:
                self.region_vars["全世界"].set(True)
        self._update_selected_regions_display()

        # 動画数
        self.video_count_var.set(settings.video_count)
        self.video_count_label.config(text=str(settings.video_count))
        self.video_count_entry.delete(0, tk.END)
        self.video_count_entry.insert(0, str(settings.video_count))

        # プライバシー
        self.privacy_var.set(settings.privacy)

        # 検索オプション
        self.prefer_official_var.set(settings.prefer_official)
        self.search_precision_var.set(settings.search_precision)
        self.add_region_keywords_var.set(settings.add_region_keywords)
        self.add_detailed_description_var.set(settings.add_detailed_description)

        # プラットフォーム設定
        if hasattr(settings, 'platforms') and settings.platforms:
            for platform, var in self.platform_vars.items():
                var.set(platform in settings.platforms)

        # 選択キーワード表示を更新
        self._update_selected_keywords_display()

    def _save_preset(self):
        """現在の設定をプリセットとして保存"""
        # プリセット名を入力
        name = simpledialog.askstring(
            "プリセット保存",
            "プリセット名を入力してください:",
            parent=self.root
        )
        if not name:
            return

        # 既存のプリセットと重複チェック
        existing = self.preset_manager.get_by_name(name)
        if existing:
            if not messagebox.askyesno(
                "上書き確認",
                f"プリセット「{name}」は既に存在します。上書きしますか？"
            ):
                return
            self.preset_manager.update(existing.id, settings=self._get_current_settings())
            messagebox.showinfo("保存完了", f"プリセット「{name}」を上書き保存しました")
        else:
            self.preset_manager.add(name, self._get_current_settings())
            messagebox.showinfo("保存完了", f"プリセット「{name}」を保存しました")

        # コンボボックスを更新
        self.preset_combo["values"] = self.preset_manager.get_preset_names()
        self.preset_var.set(name)

    def _load_preset(self):
        """選択されたプリセットを読み込む"""
        name = self.preset_var.get()
        if not name:
            messagebox.showwarning("選択なし", "読み込むプリセットを選択してください")
            return

        preset = self.preset_manager.get_by_name(name)
        if not preset:
            messagebox.showerror("エラー", f"プリセット「{name}」が見つかりません")
            return

        self._apply_preset_settings(preset.settings)
        messagebox.showinfo("読込完了", f"プリセット「{name}」を読み込みました")

    def _delete_preset(self):
        """選択されたプリセットを削除"""
        name = self.preset_var.get()
        if not name:
            messagebox.showwarning("選択なし", "削除するプリセットを選択してください")
            return

        if not messagebox.askyesno(
            "削除確認",
            f"プリセット「{name}」を削除しますか？"
        ):
            return

        preset = self.preset_manager.get_by_name(name)
        if preset:
            self.preset_manager.delete(preset.id)
            self.preset_combo["values"] = self.preset_manager.get_preset_names()
            self.preset_var.set("")
            messagebox.showinfo("削除完了", f"プリセット「{name}」を削除しました")

    def _edit_preset(self):
        """選択されたプリセットを編集"""
        name = self.preset_var.get()
        if not name:
            messagebox.showwarning("選択なし", "編集するプリセットを選択してください")
            return

        preset = self.preset_manager.get_by_name(name)
        if not preset:
            messagebox.showerror("エラー", f"プリセット「{name}」が見つかりません")
            return

        # 編集ダイアログを開く
        dialog = PresetEditDialog(self.root, preset=preset)
        if dialog.result:
            # 更新を保存
            self.preset_manager.update(
                preset.id,
                name=dialog.result["name"],
                settings=dialog.result["settings"]
            )
            self.preset_combo["values"] = self.preset_manager.get_preset_names()
            self.preset_var.set(dialog.result["name"])
            messagebox.showinfo("保存完了", f"プリセット「{dialog.result['name']}」を更新しました")

    # ========================================
    # 履歴操作メソッド
    # ========================================

    def _refresh_history(self):
        """履歴リストを更新"""
        # 既存のアイテムをクリア
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # 履歴を取得して表示
        for entry in self.history_manager.get_all():
            self.history_tree.insert(
                "",
                tk.END,
                iid=entry.id,
                values=(
                    entry.get_formatted_date(),
                    entry.title,
                    entry.video_count,
                    entry.get_platform_display(),
                    entry.conditions.category,
                    entry.conditions.era,
                )
            )

    def _clear_history(self):
        """全履歴を削除"""
        if not messagebox.askyesno(
            "全削除確認",
            "すべての履歴を削除しますか？この操作は取り消せません。"
        ):
            return

        count = self.history_manager.clear_all()
        self._refresh_history()
        messagebox.showinfo("削除完了", f"{count}件の履歴を削除しました")

    def _export_history(self):
        """履歴をエクスポート（JSON/CSV）"""
        file_path = filedialog.asksaveasfilename(
            title="履歴をエクスポート",
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ],
            initialfilename="playlist_history.json"
        )
        if not file_path:
            return

        path = Path(file_path)
        if path.suffix.lower() == ".csv":
            # CSVエクスポート
            if self.history_manager.export_to_csv(path):
                messagebox.showinfo("エクスポート完了", f"履歴をCSV形式で {file_path} にエクスポートしました")
            else:
                messagebox.showerror("エラー", "CSVエクスポートに失敗しました")
        else:
            # JSONエクスポート
            if self.history_manager.export_to_file(path):
                messagebox.showinfo("エクスポート完了", f"履歴を {file_path} にエクスポートしました")
            else:
                messagebox.showerror("エラー", "エクスポートに失敗しました")

    def _import_history(self):
        """履歴をインポート"""
        file_path = filedialog.askopenfilename(
            title="履歴をインポート",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        count = self.history_manager.import_from_file(Path(file_path), merge=True)
        if count > 0:
            self._refresh_history()
            messagebox.showinfo("インポート完了", f"{count}件の履歴をインポートしました")
        else:
            messagebox.showerror("エラー", "インポートに失敗しました（ファイル形式を確認してください）")

    def _get_selected_history_entry(self) -> Optional[HistoryEntry]:
        """選択された履歴エントリーを取得"""
        selection = self.history_tree.selection()
        if not selection:
            return None
        entry_id = selection[0]
        return self.history_manager.get_by_id(entry_id)

    def _recreate_from_history(self):
        """履歴から同じ条件で再作成"""
        entry = self._get_selected_history_entry()
        if not entry:
            messagebox.showwarning("選択なし", "履歴を選択してください")
            return

        # 条件をGUIに適用
        conditions = entry.conditions
        settings = PresetSettings(
            era=conditions.era,
            category=conditions.category,
            keywords=conditions.keywords,
            additional_keyword=conditions.additional_keyword,
            region_group=conditions.region_group,
            country=conditions.country,
            video_count=conditions.video_count,
            privacy=conditions.privacy,
            prefer_official=conditions.prefer_official,
            search_precision=conditions.search_precision,
            add_region_keywords=True,
            add_detailed_description=True,
        )
        self._apply_preset_settings(settings)
        messagebox.showinfo("条件適用", "検索条件を適用しました。「再生リストを作成」ボタンで実行してください。")

    def _open_history_url(self):
        """履歴のURLを開く"""
        entry = self._get_selected_history_entry()
        if not entry:
            messagebox.showwarning("選択なし", "履歴を選択してください")
            return

        webbrowser.open(entry.url)

    def _view_history_videos(self):
        """履歴のプレイリストの動画を確認"""
        entry = self._get_selected_history_entry()
        if not entry:
            messagebox.showwarning("選択なし", "履歴を選択してください")
            return

        # YouTubeプレイリストのみ対応
        if entry.platform != "youtube":
            messagebox.showinfo(
                "非対応",
                f"{entry.get_platform_display()}のプレイリストは動画確認に対応していません。\n「URLを開く」でブラウザで確認してください。"
            )
            return

        if not entry.playlist_id:
            messagebox.showwarning("エラー", "プレイリストIDが見つかりません")
            return

        self.show_playlist_videos(entry.playlist_id, entry.title)

    def _delete_history_entry(self):
        """選択された履歴を削除"""
        entry = self._get_selected_history_entry()
        if not entry:
            messagebox.showwarning("選択なし", "履歴を選択してください")
            return

        if not messagebox.askyesno(
            "削除確認",
            f"履歴「{entry.title}」を削除しますか？"
        ):
            return

        self.history_manager.delete(entry.id)
        self._refresh_history()

    def _export_history_csv(self):
        """履歴をCSV形式でエクスポート"""
        file_path = filedialog.asksaveasfilename(
            title="履歴をCSVでエクスポート",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfilename="playlist_history.csv"
        )
        if not file_path:
            return

        if self.history_manager.export_to_csv(Path(file_path)):
            messagebox.showinfo("エクスポート完了", f"履歴を {file_path} にエクスポートしました")
        else:
            messagebox.showerror("エラー", "CSVエクスポートに失敗しました")

    # ========================================
    # バックアップ機能
    # ========================================

    def _create_backup(self):
        """バックアップを作成"""
        manager = BackupManager()

        # バックアップするデータを収集
        backup_data = {
            'favorites': self._get_all_favorites(),
            'history': [h.to_dict() for h in self.history_manager.get_all()],
            'presets': [p.to_dict() for p in self.preset_manager.get_all()],
            'settings': self._get_current_settings()
        }

        backup_file = manager.create_backup(backup_data)
        messagebox.showinfo("成功", f"バックアップを作成しました:\n{backup_file.name}")

    def _restore_from_backup(self):
        """バックアップから復元"""
        manager = BackupManager()

        backup_file = filedialog.askopenfilename(
            title="バックアップファイルを選択",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=str(manager.get_backup_dir())
        )

        if not backup_file:
            return

        result = messagebox.askyesno(
            "確認",
            "バックアップを復元すると、現在の設定が上書きされます。\n続行しますか？"
        )

        if not result:
            return

        try:
            data = manager.restore_backup(Path(backup_file))

            # データを復元
            if 'favorites' in data:
                self._restore_favorites(data['favorites'])
            if 'history' in data:
                self._restore_history_data(data['history'])
            if 'presets' in data:
                self._restore_presets_data(data['presets'])

            messagebox.showinfo("成功", "バックアップを復元しました")
            self._refresh_history()
        except Exception as e:
            messagebox.showerror("エラー", f"エクスポートに失敗しました:\n{str(e)}")

    def _manage_backups(self):
        """バックアップ管理ダイアログを開く"""
        manager = BackupManager()

        dialog = tk.Toplevel(self.root)
        dialog.title("バックアップ管理")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # バックアップ一覧
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="バックアップ一覧", font=('Arial', 12, 'bold')).pack(pady=5)

        # リストボックスとスクロールバー
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=('Consolas', 10))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # バックアップをロード
        backups = manager.list_backups()

        for backup in backups:
            created = backup['created_at'][:19] if len(backup['created_at']) > 19 else backup['created_at']
            listbox.insert(tk.END, f"{backup['filename']} - {created}")

        # ボタンフレーム
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        def restore_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("警告", "バックアップを選択してください", parent=dialog)
                return

            backup = backups[selection[0]]
            dialog.destroy()

            # 復元確認
            if not messagebox.askyesno("確認", "バックアップを復元すると、現在の設定が上書きされます。\n続行しますか？"):
                return

            try:
                data = manager.restore_backup(Path(backup['path']))
                if 'favorites' in data:
                    self._restore_favorites(data['favorites'])
                if 'history' in data:
                    self._restore_history_data(data['history'])
                if 'presets' in data:
                    self._restore_presets_data(data['presets'])

                messagebox.showinfo("成功", "バックアップを復元しました")
                self._refresh_history()
            except Exception as e:
                messagebox.showerror("エラー", f"エクスポートに失敗しました:\n{str(e)}")

        def delete_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("警告", "バックアップを選択してください", parent=dialog)
                return

            backup = backups[selection[0]]
            result = messagebox.askyesno("確認", f"{backup['filename']} を削除しますか？", parent=dialog)

            if result:
                manager.delete_backup(backup['path'])
                listbox.delete(selection[0])
                backups.pop(selection[0])

        ttk.Button(btn_frame, text="復元", command=restore_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="削除", command=delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="閉じる", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def _restore_history_data(self, history_data: list):
        """履歴データを復元"""
        # 既存の履歴をクリアして新しいデータをインポート
        self.history_manager.clear_all()
        for entry_data in history_data:
            entry = HistoryEntry.from_dict(entry_data)
            self.history_manager._history.append(entry)
        self.history_manager._save()

    def _restore_presets_data(self, presets_data: list):
        """プリセットデータを復元"""
        # 既存のプリセットをクリアして新しいデータをインポート
        self.preset_manager._presets = []
        for preset_data in presets_data:
            preset = Preset.from_dict(preset_data)
            self.preset_manager._presets.append(preset)
        self.preset_manager._save()

    # ========================================
    # お気に入り機能
    # ========================================

    def _get_all_favorites(self) -> dict:
        """現在のお気に入り設定を取得"""
        return {
            'keywords': [kw for kw, var in self.keyword_vars.items() if var.get()],
            'regions': [r for r, var in self.region_vars.items() if var.get()],
            'era': self.era_var.get(),
            'category': self.category_var.get(),
            'additional_keyword': self.keyword_var.get().strip() if hasattr(self, 'keyword_var') else ''
        }

    def _get_current_settings(self) -> dict:
        """現在の設定を取得（バックアップ用）"""
        return {
            'era': self.era_var.get(),
            'category': self.category_var.get(),
            'keywords': [kw for kw, var in self.keyword_vars.items() if var.get()],
            'regions': [r for r, var in self.region_vars.items() if var.get()],
            'additional_keyword': self.keyword_var.get().strip() if hasattr(self, 'keyword_var') else ''
        }

    def _restore_favorites(self, favorites: dict):
        """お気に入り設定を復元"""
        try:
            # キーワード選択を復元
            if 'keywords' in favorites:
                # まず全てをクリア
                for var in self.keyword_vars.values():
                    var.set(False)
                # 保存されたキーワードを選択
                for kw in favorites['keywords']:
                    if kw in self.keyword_vars:
                        self.keyword_vars[kw].set(True)

            # 地域選択を復元
            if 'regions' in favorites:
                # まず全てをクリア
                for var in self.region_vars.values():
                    var.set(False)
                # 保存された地域を選択
                for region in favorites['regions']:
                    if region in self.region_vars:
                        self.region_vars[region].set(True)

            # 基本設定を復元
            if 'era' in favorites:
                self.era_var.set(favorites['era'])
            if 'category' in favorites:
                self.category_var.set(favorites['category'])
            if 'additional_keyword' in favorites and hasattr(self, 'keyword_var'):
                self.keyword_var.set(favorites['additional_keyword'])

        except Exception as e:
            print(f"Error restoring favorites: {e}")

    def _save_current_as_favorite(self):
        """現在の設定をお気に入りとして保存"""
        name = simpledialog.askstring("現在の設定を保存", "お気に入りの名前を入力してください:", parent=self.root)

        if not name:
            return

        favorites = self._get_all_favorites()
        favorites['name'] = name
        favorites['saved_at'] = datetime.now().isoformat()

        # お気に入りファイルに保存
        favorites_file = CONFIG_PATH / 'favorites.json'

        try:
            if favorites_file.exists():
                with open(favorites_file, 'r', encoding='utf-8') as f:
                    all_favorites = json.load(f)
            else:
                all_favorites = []

            all_favorites.append(favorites)

            with open(favorites_file, 'w', encoding='utf-8') as f:
                json.dump(all_favorites, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("成功", f"お気に入りを保存しました: '{name}'")
        except Exception as e:
            messagebox.showerror("エラー", f"エクスポートに失敗しました:\n{str(e)}")

    def _load_favorite(self):
        """保存したお気に入りを読み込む"""
        favorites_file = CONFIG_PATH / 'favorites.json'

        if not favorites_file.exists():
            messagebox.showinfo("情報", "保存されたお気に入りがありません")
            return

        try:
            with open(favorites_file, 'r', encoding='utf-8') as f:
                all_favorites = json.load(f)

            if not all_favorites:
                messagebox.showinfo("情報", "保存されたお気に入りがありません")
                return

            # 選択ダイアログを表示
            dialog = tk.Toplevel(self.root)
            dialog.title("お気に入りを読み込み")
            dialog.geometry("400x300")
            dialog.transient(self.root)
            dialog.grab_set()

            ttk.Label(dialog, text="お気に入りを選択してください",
                     font=('Arial', 10, 'bold')).pack(pady=10)

            # リストボックス
            list_frame = ttk.Frame(dialog)
            list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            scrollbar = ttk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=listbox.yview)

            for fav in all_favorites:
                listbox.insert(tk.END, fav.get('name', 'Unnamed'))

            def load_selected():
                selection = listbox.curselection()
                if not selection:
                    return

                favorite = all_favorites[selection[0]]
                self._restore_favorites(favorite)
                dialog.destroy()
                messagebox.showinfo("成功", "お気に入りを読み込みました")

            ttk.Button(dialog, text="読み込み", command=load_selected).pack(pady=5)

        except Exception as e:
            messagebox.showerror("エラー", f"エクスポートに失敗しました:\n{str(e)}")

    def _manage_favorites(self):
        """お気に入り管理ダイアログを開く"""
        favorites_file = CONFIG_PATH / 'favorites.json'

        dialog = tk.Toplevel(self.root)
        dialog.title("お気に入り管理")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="お気に入り一覧", font=('Arial', 12, 'bold')).pack(pady=5)

        # リストボックス
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=('Consolas', 10))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # お気に入りをロード
        all_favorites = []
        if favorites_file.exists():
            try:
                with open(favorites_file, 'r', encoding='utf-8') as f:
                    all_favorites = json.load(f)
            except:
                pass

        for fav in all_favorites:
            name = fav.get('name', 'Unnamed')
            saved_at = fav.get('saved_at', '')[:10]
            listbox.insert(tk.END, f"{name} ({saved_at})")

        # 詳細表示エリア
        detail_frame = ttk.LabelFrame(frame, text="詳細", padding=5)
        detail_frame.pack(fill=tk.X, pady=5)

        detail_text = tk.Text(detail_frame, height=5, state='disabled')
        detail_text.pack(fill=tk.X)

        def show_detail(event=None):
            selection = listbox.curselection()
            if not selection:
                return

            fav = all_favorites[selection[0]]
            detail_text.config(state='normal')
            detail_text.delete(1.0, tk.END)
            detail_text.insert(tk.END, f"年代: {fav.get('era', 'N/A')}\n")
            detail_text.insert(tk.END, f"カテゴリ: {fav.get('category', 'N/A')}\n")
            detail_text.insert(tk.END, f"Keywords: {', '.join(fav.get('keywords', []))}\n")
            detail_text.insert(tk.END, f"Regions: {', '.join(fav.get('regions', []))}\n")
            detail_text.config(state='disabled')

        listbox.bind('<<ListboxSelect>>', show_detail)

        # ボタンフレーム
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        def load_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("警告", "お気に入りを選択してください", parent=dialog)
                return

            favorite = all_favorites[selection[0]]
            self._restore_favorites(favorite)
            dialog.destroy()
            messagebox.showinfo("成功", "お気に入りを読み込みました")

        def delete_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("警告", "お気に入りを選択してください", parent=dialog)
                return

            fav = all_favorites[selection[0]]
            if not messagebox.askyesno("確認", f"'{fav.get('name', 'Unnamed')}' を削除しますか？", parent=dialog):
                return

            all_favorites.pop(selection[0])
            listbox.delete(selection[0])

            # ファイルに保存
            with open(favorites_file, 'w', encoding='utf-8') as f:
                json.dump(all_favorites, f, ensure_ascii=False, indent=2)

        ttk.Button(btn_frame, text="読み込み", command=load_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="削除", command=delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="閉じる", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    # ========================================
    # エクスポート機能
    # ========================================

    def _export_data(self, format_type: str):
        """プレイリストデータをエクスポート"""
        # エクスポートするデータを取得
        history = self.history_manager.get_all()

        if not history:
            messagebox.showinfo("情報", "エクスポートするデータがありません")
            return

        # ファイルダイアログ
        filetypes = {
            'csv': [("CSV files", "*.csv")],
            'json': [("JSON files", "*.json")],
            'txt': [("Text files", "*.txt")]
        }

        default_filename = f"playlist_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        filepath = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=filetypes.get(format_type, [("All files", "*.*")]),
            initialfile=default_filename
        )

        if not filepath:
            return

        try:
            if format_type == 'csv':
                ExportManager.export_history_to_csv(history, Path(filepath))
            elif format_type == 'json':
                ExportManager.export_history_to_json(history, Path(filepath))
            elif format_type == 'txt':
                ExportManager.export_history_to_txt(history, Path(filepath))

            messagebox.showinfo("成功", f"データをエクスポートしました:\n{os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("エラー", f"エクスポートに失敗しました:\n{str(e)}")

    # ========================================
    # 言語切り替え機能（一時的に無効化）
    # ========================================

    def _save_current_state(self) -> dict:
        """言語変更前のUI状態を保存

        Returns:
            現在のUI状態を格納した辞書
        """
        state = {
            'era_value': self.era_var.get() if hasattr(self, 'era_var') else None,
            'category_value': self.category_var.get() if hasattr(self, 'category_var') else None,
            'video_count': self.video_count_var.get() if hasattr(self, 'video_count_var') else 20,
            'keyword_selections': {},
            'region_selections': {},
            'additional_keyword': self.keyword_var.get() if hasattr(self, 'keyword_var') else '',
            'privacy': self.privacy_var.get() if hasattr(self, 'privacy_var') else 'private',
            'search_precision': self.search_precision_var.get() if hasattr(self, 'search_precision_var') else 'standard',
            'prefer_official': self.prefer_official_var.get() if hasattr(self, 'prefer_official_var') else True,
            'require_verified': self.require_verified_var.get() if hasattr(self, 'require_verified_var') else False,
            'min_subscribers': self.min_subscribers_var.get() if hasattr(self, 'min_subscribers_var') else False,
            'min_views': self.min_views_var.get() if hasattr(self, 'min_views_var') else False,
            'vevo_only': self.vevo_only_var.get() if hasattr(self, 'vevo_only_var') else False,
            'add_detailed_description': self.add_detailed_description_var.get() if hasattr(self, 'add_detailed_description_var') else True,
            'add_region_keywords': self.add_region_keywords_var.get() if hasattr(self, 'add_region_keywords_var') else True,
            'platform_youtube': self.platform_vars.get('youtube', tk.BooleanVar()).get() if hasattr(self, 'platform_vars') else True,
            'platform_niconico': self.platform_vars.get('niconico', tk.BooleanVar()).get() if hasattr(self, 'platform_vars') else False,
        }

        # キーワード選択状態を保存（API用キーワードをキーとして使用）
        if hasattr(self, 'keyword_vars'):
            for keyword, var in self.keyword_vars.items():
                state['keyword_selections'][keyword] = var.get()

        # 地域選択状態を保存（地域名をキーとして使用）
        if hasattr(self, 'region_vars'):
            for region, var in self.region_vars.items():
                state['region_selections'][region] = var.get()

        return state

    def _restore_current_state(self, state: dict):
        """言語変更後にUI状態を復元

        Args:
            state: 保存されたUI状態の辞書
        """
        if not state:
            return

        # 年代を復元（値ベースで復元）
        if state.get('era_value') and hasattr(self, 'era_var'):
            # 年代は言語非依存の値なのでそのまま復元
            if state['era_value'] in self.ERAS:
                self.era_var.set(state['era_value'])

        # カテゴリを復元
        if state.get('category_value') and hasattr(self, 'category_var'):
            if state['category_value'] in self.CATEGORIES:
                self.category_var.set(state['category_value'])

        # 動画数を復元
        if hasattr(self, 'video_count_var'):
            self.video_count_var.set(state.get('video_count', 20))
            if hasattr(self, 'video_count_label'):
                self.video_count_label.config(text=str(state.get('video_count', 20)))
            if hasattr(self, 'video_count_entry'):
                self.video_count_entry.delete(0, tk.END)
                self.video_count_entry.insert(0, str(state.get('video_count', 20)))

        # 追加キーワードを復元
        if hasattr(self, 'keyword_var'):
            self.keyword_var.set(state.get('additional_keyword', ''))

        # プライバシー設定を復元
        if hasattr(self, 'privacy_var'):
            self.privacy_var.set(state.get('privacy', 'private'))

        # 検索精度を復元
        if hasattr(self, 'search_precision_var'):
            self.search_precision_var.set(state.get('search_precision', 'standard'))

        # 各種オプションを復元
        if hasattr(self, 'prefer_official_var'):
            self.prefer_official_var.set(state.get('prefer_official', True))
        if hasattr(self, 'require_verified_var'):
            self.require_verified_var.set(state.get('require_verified', False))
        if hasattr(self, 'min_subscribers_var'):
            self.min_subscribers_var.set(state.get('min_subscribers', False))
        if hasattr(self, 'min_views_var'):
            self.min_views_var.set(state.get('min_views', False))
        if hasattr(self, 'vevo_only_var'):
            self.vevo_only_var.set(state.get('vevo_only', False))
        if hasattr(self, 'add_detailed_description_var'):
            self.add_detailed_description_var.set(state.get('add_detailed_description', True))
        if hasattr(self, 'add_region_keywords_var'):
            self.add_region_keywords_var.set(state.get('add_region_keywords', True))

        # プラットフォーム選択を復元
        if hasattr(self, 'platform_vars'):
            if 'youtube' in self.platform_vars:
                self.platform_vars['youtube'].set(state.get('platform_youtube', True))
            if 'niconico' in self.platform_vars:
                self.platform_vars['niconico'].set(state.get('platform_niconico', False))

        # キーワード選択を復元
        if hasattr(self, 'keyword_vars') and state.get('keyword_selections'):
            for keyword, selected in state['keyword_selections'].items():
                if keyword in self.keyword_vars:
                    self.keyword_vars[keyword].set(selected)

        # 地域選択を復元
        if hasattr(self, 'region_vars') and state.get('region_selections'):
            for region, selected in state['region_selections'].items():
                if region in self.region_vars:
                    self.region_vars[region].set(selected)

    # 以下の関数は言語機能と共に一時的に無効化
    # def _refresh_ui(self):
    #     """UIを完全にリフレッシュ（言語変更時に呼び出し）"""
    #     pass
    #
    # def _update_all_labels(self):
    #     """すべてのラベルテキストを更新"""
    #     pass
    #
    # def _update_keyword_tabs(self):
    #     """キーワードタブのラベルを更新"""
    #     pass
    #
    # def _update_buttons(self):
    #     """ボタンテキストを更新"""
    #     pass
    #
    # def _update_statusbar(self):
    #     """ステータスバーを更新"""
    #     pass

    # ========================================
    # 統合プレイリスト操作メソッド
    # ========================================

    def _refresh_integrated_playlists(self):
        """統合プレイリストリストを更新"""
        for item in self.integrated_tree.get_children():
            self.integrated_tree.delete(item)

        for playlist in self.integrated_playlist_manager.get_all():
            counts = playlist.get_platform_counts()
            self.integrated_tree.insert(
                "",
                tk.END,
                iid=playlist.id,
                values=(
                    playlist.get_formatted_date(),
                    playlist.title,
                    len(playlist.items),
                    counts.get("youtube", 0),
                    counts.get("niconico", 0),
                )
            )

    def _get_selected_integrated_playlist(self) -> Optional[IntegratedPlaylist]:
        """選択された統合プレイリストを取得"""
        selection = self.integrated_tree.selection()
        if not selection:
            return None
        return self.integrated_playlist_manager.get_by_id(selection[0])

    def _create_new_integrated_playlist(self):
        """新しい統合プレイリストを作成"""
        title = simpledialog.askstring(
            "新規作成",
            "統合プレイリストのタイトルを入力してください:",
            parent=self.root
        )
        if not title:
            return

        description = simpledialog.askstring(
            "説明",
            "説明を入力してください（任意）:",
            parent=self.root
        ) or ""

        playlist = self.integrated_playlist_manager.create(title, description)
        self._refresh_integrated_playlists()
        messagebox.showinfo("作成完了", f"統合プレイリスト「{title}」を作成しました")

    def _export_integrated_json(self):
        """統合プレイリストをJSON形式でエクスポート"""
        playlist = self._get_selected_integrated_playlist()
        if not playlist:
            messagebox.showwarning("選択なし", "エクスポートするプレイリストを選択してください")
            return

        file_path = filedialog.asksaveasfilename(
            title="JSONでエクスポート",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfilename=f"{playlist.title.replace(' ', '_')}.json"
        )
        if not file_path:
            return

        if self.integrated_playlist_manager.export_to_json(playlist.id, Path(file_path)):
            messagebox.showinfo("エクスポート完了", f"プレイリストを {file_path} にエクスポートしました")
        else:
            messagebox.showerror("エラー", "エクスポートに失敗しました")

    def _export_integrated_html(self):
        """統合プレイリストをHTML形式でエクスポート"""
        playlist = self._get_selected_integrated_playlist()
        if not playlist:
            messagebox.showwarning("選択なし", "エクスポートするプレイリストを選択してください")
            return

        file_path = filedialog.asksaveasfilename(
            title="HTMLでエクスポート",
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
            initialfilename=f"{playlist.title.replace(' ', '_')}.html"
        )
        if not file_path:
            return

        if self.integrated_playlist_manager.export_to_html(playlist.id, Path(file_path)):
            messagebox.showinfo("エクスポート完了", f"プレイリストを {file_path} にエクスポートしました\n\nブラウザで開きますか？")
            if messagebox.askyesno("確認", "ブラウザで開きますか？"):
                webbrowser.open(f"file://{file_path}")
        else:
            messagebox.showerror("エラー", "エクスポートに失敗しました")

    def _delete_integrated_playlist(self):
        """統合プレイリストを削除"""
        playlist = self._get_selected_integrated_playlist()
        if not playlist:
            messagebox.showwarning("選択なし", "削除するプレイリストを選択してください")
            return

        if not messagebox.askyesno(
            "削除確認",
            f"統合プレイリスト「{playlist.title}」を削除しますか？"
        ):
            return

        self.integrated_playlist_manager.delete(playlist.id)
        self._refresh_integrated_playlists()
        messagebox.showinfo("削除完了", f"統合プレイリスト「{playlist.title}」を削除しました")

    def _open_integrated_viewer(self, event=None):
        """統合プレイリストビューワーを開く"""
        playlist = self._get_selected_integrated_playlist()
        if not playlist:
            return

        # 新しいウィンドウでビューワーを開く
        viewer = IntegratedPlaylistViewer(self.root, playlist)

    def _open_video(self, video_id: str):
        """動画をブラウザで開く"""
        url = f"https://www.youtube.com/watch?v={video_id}"
        webbrowser.open(url)

    def show_playlist_videos(self, playlist_id: str, playlist_title: str):
        """再生リストの動画一覧を新しいウィンドウで表示"""
        # 新しいウィンドウを作成
        viewer_window = tk.Toplevel(self.root)
        viewer_window.title(f"再生リスト: {playlist_title}")
        viewer_window.geometry("900x700")
        viewer_window.transient(self.root)

        # ヘッダー
        header_frame = ttk.Frame(viewer_window, padding="10")
        header_frame.pack(fill=tk.X)

        ttk.Label(
            header_frame,
            text=f"📋 {playlist_title}",
            font=('', 14, 'bold')
        ).pack(side=tk.LEFT)

        ttk.Button(
            header_frame,
            text="🌐 YouTubeで開く",
            command=lambda: webbrowser.open(f"https://www.youtube.com/playlist?list={playlist_id}")
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            header_frame,
            text="📋 URLコピー",
            command=lambda: self._copy_to_clipboard(f"https://www.youtube.com/playlist?list={playlist_id}")
        ).pack(side=tk.RIGHT, padx=5)

        # セパレータ
        ttk.Separator(viewer_window, orient="horizontal").pack(fill=tk.X)

        # スクロール可能なキャンバス
        canvas_frame = ttk.Frame(viewer_window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 配置
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # マウスホイール対応
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # ウィンドウが閉じられたときにマウスホイールバインドを解除
        def _on_close():
            canvas.unbind_all("<MouseWheel>")
            viewer_window.destroy()

        viewer_window.protocol("WM_DELETE_WINDOW", _on_close)

        # 動画を取得して表示
        self._load_playlist_videos(scrollable_frame, playlist_id, canvas)

    def _load_playlist_videos(self, parent_frame: ttk.Frame, playlist_id: str, canvas: tk.Canvas):
        """再生リストから動画を取得して表示"""
        # ローディング表示
        loading_label = ttk.Label(
            parent_frame,
            text="動画を読み込み中...",
            font=('', 12)
        )
        loading_label.pack(pady=20)

        def fetch_videos():
            """別スレッドで動画を取得"""
            try:
                client = YouTubeClient()

                # 再生リストの動画を取得（最大100本）
                videos = list(client.get_playlist_videos(playlist_id, max_results=100))

                # UIスレッドで表示
                self.root.after(0, lambda: self._display_playlist_videos(
                    parent_frame, videos, loading_label, canvas
                ))

            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: loading_label.config(
                    text=f"エラー: {error_msg}",
                    foreground="red"
                ))

        # 別スレッドで実行
        thread = threading.Thread(target=fetch_videos, daemon=True)
        thread.start()

    def _display_playlist_videos(self, parent_frame: ttk.Frame, videos: list,
                                  loading_label: ttk.Label, canvas: tk.Canvas):
        """動画を表示"""
        # ローディングラベルを削除
        loading_label.destroy()

        if not videos:
            ttk.Label(
                parent_frame,
                text="動画が見つかりませんでした",
                font=('', 11)
            ).pack(pady=20)
            return

        # 合計表示（上部）
        total_label = ttk.Label(
            parent_frame,
            text=f"合計: {len(videos)}本の動画",
            font=('', 11, 'bold')
        )
        total_label.pack(pady=(0, 10), anchor=tk.W)

        # 各動画を表示
        for idx, video in enumerate(videos, 1):
            # 動画カード
            card_frame = ttk.LabelFrame(
                parent_frame,
                text=f"{idx}. {video.title[:50]}{'...' if len(video.title) > 50 else ''}",
                padding=10
            )
            card_frame.pack(fill=tk.X, padx=5, pady=5)

            # 情報表示
            info_frame = ttk.Frame(card_frame)
            info_frame.pack(fill=tk.X)

            ttk.Label(
                info_frame,
                text=f"チャンネル: {video.channel_title}",
                font=('', 9)
            ).pack(anchor="w")

            published_date = video.published_at.strftime("%Y/%m/%d") if video.published_at else "N/A"
            ttk.Label(
                info_frame,
                text=f"公開日: {published_date}",
                font=('', 9),
                foreground="gray"
            ).pack(anchor="w")

            # ボタン
            button_frame = ttk.Frame(card_frame)
            button_frame.pack(fill=tk.X, pady=(5, 0))

            video_url = f"https://www.youtube.com/watch?v={video.video_id}"

            ttk.Button(
                button_frame,
                text="▶ 再生",
                command=lambda url=video_url: webbrowser.open(url),
                width=10
            ).pack(side=tk.LEFT, padx=(0, 5))

            ttk.Button(
                button_frame,
                text="📋 URLコピー",
                command=lambda url=video_url: self._copy_to_clipboard(url),
                width=12
            ).pack(side=tk.LEFT, padx=5)

        # スクロール領域を更新
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _format_subscriber_count(self, count: Optional[int]) -> str:
        """登録者数をフォーマット"""
        if count is None:
            return "非公開"
        if count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M"
        if count >= 1_000:
            return f"{count / 1_000:.1f}K"
        return str(count)

    def _format_view_count(self, count: Optional[int]) -> str:
        """視聴回数をフォーマット"""
        if count is None:
            return ""
        if count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M回"
        if count >= 1_000:
            return f"{count / 1_000:.1f}K回"
        return f"{count}回"

    def _create_video_card(self, video: VideoInfo, index: int):
        """動画カードを作成（信頼性インジケーター付き）"""
        card_frame = ttk.Frame(self.result_scrollable_frame, relief="groove", borderwidth=1)
        card_frame.pack(fill=tk.X, pady=2, padx=2)

        # 内部フレーム
        inner_frame = ttk.Frame(card_frame, padding="5")
        inner_frame.pack(fill=tk.X)

        # サムネイル（プレースホルダー）
        thumb_frame = ttk.Frame(inner_frame, width=120, height=68)
        thumb_frame.pack(side=tk.LEFT, padx=(0, 10))
        thumb_frame.pack_propagate(False)

        # サムネイルボタン（クリックで再生）
        thumb_btn = ttk.Button(
            thumb_frame,
            text="▶ 再生",
            command=lambda vid=video.video_id: self._open_video(vid)
        )
        thumb_btn.pack(expand=True, fill=tk.BOTH)

        # 動画情報
        info_frame = ttk.Frame(inner_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # タイトル
        title = video.title[:55] + "..." if len(video.title) > 55 else video.title

        # 信頼性判定
        is_official_by_id = is_official_channel_by_id(video.channel_id)
        is_official_by_name = is_official_channel(video.channel_title)
        is_verified = getattr(video, 'is_verified', False)

        # 信頼性バッジを構築
        badges = []
        if is_official_by_id:
            badges.append("⭐公式ID")
        elif is_official_by_name:
            badges.append("✓公式")
        if is_verified:
            badges.append("✓認証済")

        badge_text = " ".join(badges) if badges else ""

        title_label = ttk.Label(
            info_frame,
            text=f"{index}. {title}",
            font=("", 9, "bold"),
            wraplength=450
        )
        title_label.pack(anchor=tk.W)

        # チャンネル名と信頼性インジケーター
        channel_info = f"📺 {video.channel_title}"
        if badge_text:
            channel_info += f" {badge_text}"
        channel_info += f" | 📅 {video.year}"

        # 登録者数表示
        if hasattr(video, 'subscriber_count') and video.subscriber_count:
            channel_info += f" | 👥 {self._format_subscriber_count(video.subscriber_count)}"

        # 視聴回数表示
        if hasattr(video, 'view_count') and video.view_count:
            channel_info += f" | 👁 {self._format_view_count(video.view_count)}"

        # 色分け（公式度に応じて）
        if is_official_by_id:
            meta_color = "#006600"  # 濃い緑（最高信頼性）
        elif is_official_by_name or is_verified:
            meta_color = "#0066cc"  # 青（高信頼性）
        else:
            meta_color = "gray"

        meta_label = ttk.Label(info_frame, text=channel_info, foreground=meta_color)
        meta_label.pack(anchor=tk.W)

        # 品質スコア表示（デバッグ用、スコアがある場合のみ）
        if hasattr(video, 'quality_score') and video.quality_score > 0:
            score_label = ttk.Label(
                info_frame,
                text=f"品質スコア: {video.quality_score}",
                foreground="purple",
                font=("", 8)
            )
            score_label.pack(anchor=tk.W)

        # 再生ボタン
        play_btn = ttk.Button(
            inner_frame,
            text="🌐 YouTubeで開く",
            command=lambda vid=video.video_id: self._open_video(vid),
            width=15
        )
        play_btn.pack(side=tk.RIGHT, padx=(10, 0))

    def _execute(self):
        """再生リスト作成を実行"""
        if self.is_running:
            return

        # 入力値を取得
        era = self.era_var.get()
        category = self.category_var.get()
        count = int(self.video_count_var.get())
        additional_keyword = self.keyword_var.get().strip()
        selected_keywords = self._get_selected_keywords()
        privacy = self.privacy_var.get()
        prefer_official = self.prefer_official_var.get()
        country = self.country_var.get()
        region_code = get_region_code(country)
        add_region_keywords = self.add_region_keywords_var.get()
        search_precision = self.search_precision_var.get()
        add_detailed_description = self.add_detailed_description_var.get()
        region_group = self.region_group_var.get()

        # キーワードを結合
        all_keywords = selected_keywords.copy()
        if additional_keyword:
            all_keywords.append(additional_keyword)
        keyword = " ".join(all_keywords) if all_keywords else ""

        # バリデーション
        category_id = get_category_id(category)
        if not category_id:
            messagebox.showerror("エラー", f"不明なカテゴリ: {category}")
            return

        date_range = get_era_date_range(era)
        if not date_range:
            messagebox.showerror("エラー", f"不明な年代: {era}")
            return

        # 選択されたプラットフォームを取得
        selected_platforms = self._get_selected_platforms()
        if not selected_platforms:
            messagebox.showerror("エラー", "少なくとも1つのプラットフォームを選択してください")
            return

        # 検索条件を保存（履歴用）
        self.current_search_conditions = SearchConditions(
            era=era,
            category=category,
            keywords=selected_keywords,
            additional_keyword=additional_keyword,
            region_group=region_group,
            country=country,
            video_count=count,
            privacy=privacy,
            prefer_official=prefer_official,
            search_precision=search_precision,
            platforms=selected_platforms,
        )

        # UI状態を更新
        self.is_running = True
        self.execute_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self._clear_result()
        self.progress_bar.start(10)

        # バックグラウンドで実行
        thread = threading.Thread(
            target=self._run_search,
            args=(era, category, category_id, date_range, count, keyword, privacy,
                  prefer_official, country, region_code, add_region_keywords, search_precision,
                  add_detailed_description, selected_keywords, additional_keyword, region_group,
                  selected_platforms),
            daemon=True
        )
        thread.start()

    def _cancel(self):
        """実行をキャンセル"""
        self.is_running = False
        self._update_progress(t('progress_cancelled'))
        self._finish_execution()

    def _finish_execution(self):
        """実行完了処理"""
        self.is_running = False
        self.execute_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.progress_bar.stop()

    def _run_search(self, era: str, category: str, category_id: str,
                    date_range: tuple, count: int, keyword: str, privacy: str,
                    prefer_official: bool = True, country: str = "全世界",
                    region_code: Optional[str] = None, add_region_keywords: bool = True,
                    search_precision: str = "standard",
                    add_detailed_description: bool = True,
                    selected_keywords: list[str] = None,
                    additional_keyword: str = "",
                    region_group: str = "全世界",
                    selected_platforms: list[str] = None):
        """バックグラウンドで検索・作成を実行（マルチプラットフォーム対応）"""
        if selected_keywords is None:
            selected_keywords = []
        if selected_platforms is None:
            selected_platforms = ["youtube"]

        # YouTubeが選択されているか
        youtube_selected = "youtube" in selected_platforms
        # ニコニコ動画が選択されているか
        niconico_selected = "niconico" in selected_platforms
        # マルチプラットフォーム検索かどうか
        is_multi_platform = len(selected_platforms) > 1 or (len(selected_platforms) == 1 and selected_platforms[0] != "youtube")

        try:
            # 検索精度をEnumに変換
            precision_map = {
                "standard": SearchPrecision.STANDARD,
                "high": SearchPrecision.HIGH,
                "highest": SearchPrecision.HIGHEST,
            }
            precision = precision_map.get(search_precision, SearchPrecision.STANDARD)
            precision_labels = {
                "standard": "標準",
                "high": "高精度",
                "highest": "最高精度",
            }

            # 選択されたプラットフォームを表示
            platform_names_disp = {"youtube": "YouTube", "niconico": "ニコニコ動画"}
            selected_platform_names = [platform_names_disp.get(p, p) for p in selected_platforms]
            self.root.after(0, lambda: self._append_result(f"選択されたプラットフォーム: {', '.join(selected_platform_names)}"))
            self.root.after(0, lambda: self._append_result(f"検索条件:"))
            self.root.after(0, lambda: self._append_result(f"  年代: {era}"))
            self.root.after(0, lambda: self._append_result(f"  カテゴリ: {category}"))
            self.root.after(0, lambda: self._append_result(f"  動画数: {count}"))
            self.root.after(0, lambda: self._append_result(f"  地域: {country}" + (f" ({region_code})" if region_code else "")))
            if keyword:
                self.root.after(0, lambda: self._append_result(f"  キーワード: {keyword}"))
            self.root.after(0, lambda: self._append_result(f"  プライバシー: {privacy}"))
            self.root.after(0, lambda: self._append_result(f"  公式優先: {'ON' if prefer_official else 'OFF'}"))
            self.root.after(0, lambda: self._append_result(f"  検索精度: {precision_labels.get(search_precision, search_precision)}"))
            self.root.after(0, lambda: self._append_result(""))

            # 共通の変数を初期化
            selected_videos = []
            playlist_id = None
            playlist_url = None
            playlist_title = f"Mix lists - {era} {category.capitalize()}"
            if country != "全世界":
                playlist_title += f" [{country}]"
            if keyword:
                playlist_title += f" ({keyword[:30]})"

            # 検索クエリを構築（共通処理）
            if prefer_official:
                official_keywords = get_official_keywords(category)
                random_suffix = random.choice(official_keywords)
            else:
                random_keywords = ["", "official", "live", "MV", "video", "full",
                                   "best", "new", "hit", "top", "classic", "popular"]
                random_suffix = random.choice(random_keywords)

            region_keyword_suffix = ""
            if add_region_keywords and region_code:
                region_keywords = get_region_keywords(region_code)
                if region_keywords:
                    region_keyword_suffix = random.choice(region_keywords)

            if keyword:
                full_query = f"{keyword} {random_suffix}".strip()
            else:
                full_query = random_suffix if random_suffix else "popular"

            if region_keyword_suffix and region_keyword_suffix.lower() not in full_query.lower():
                full_query = f"{full_query} {region_keyword_suffix}".strip()

            self.root.after(0, lambda: self._append_result(f"検索クエリ: {full_query}"))

            # ========================================
            # YouTubeが選択されていない場合: ニコニコ動画のみの処理
            # ========================================
            if not youtube_selected:
                self.root.after(0, lambda: self._append_result("\nYouTube: 選択されていません（スキップ）"))

                # ニコニコ動画のみの統合プレイリストを作成
                if niconico_selected:
                    self.root.after(0, lambda: self._append_result("\n" + "=" * 50))
                    self.root.after(0, lambda: self._append_result("ニコニコ動画検索を開始..."))

                    integrated_title = f"{playlist_title} (ニコニコ動画)"
                    integrated_playlist = self.integrated_playlist_manager.create(
                        title=integrated_title,
                        description=f"年代: {era}, カテゴリ: {category}, キーワード: {keyword}"
                    )

                    self.root.after(0, lambda: self._update_progress("ニコニコ動画で検索中..."))

                    nico_videos = []
                    try:
                        for video in self.niconico_client.search_videos(
                            query=full_query,
                            max_results=min(count, 50),
                        ):
                            if not self.is_running:
                                break
                            nico_videos.append(video)

                        if nico_videos:
                            self.root.after(0, lambda: self._append_result(f"ニコニコ動画: {len(nico_videos)}本の動画が見つかりました"))
                            for video in nico_videos:
                                item = create_integrated_item_from_niconico(video)
                                integrated_playlist.add_item(item)
                        else:
                            self.root.after(0, lambda: self._append_result("ニコニコ動画: 動画が見つかりませんでした"))
                    except Exception as e:
                        self.root.after(0, lambda: self._append_result(f"ニコニコ動画検索エラー: {str(e)}"))

                    # 統合プレイリストを保存
                    self.integrated_playlist_manager.update(integrated_playlist)
                    self.current_integrated_playlist = integrated_playlist

                    # 結果を表示
                    counts = integrated_playlist.get_platform_counts()
                    self.root.after(0, lambda: self._append_result("\n" + "=" * 50))
                    self.root.after(0, lambda: self._append_result("統合プレイリスト作成完了!"))
                    self.root.after(0, lambda: self._append_result(f"  タイトル: {integrated_title}"))
                    self.root.after(0, lambda: self._append_result(f"  合計: {len(integrated_playlist.items)}本"))
                    self.root.after(0, lambda: self._append_result("=" * 50))
                    self.root.after(0, lambda: self._append_result("※ ビューワーから動画を再生できます"))

                    # 統合プレイリストリストを更新
                    self.root.after(0, self._refresh_integrated_playlists)
                    self.root.after(0, lambda: self._update_progress("完了!"))

                else:
                    self.root.after(0, lambda: self._append_result("プラットフォームが選択されていません"))
                    self.root.after(0, lambda: self._update_progress("完了（処理なし）"))

                return  # YouTube以外の処理が完了したので終了

            # ========================================
            # YouTube検索処理
            # ========================================
            self.root.after(0, lambda: self._update_progress("YouTube APIに接続中..."))

            client = YouTubeClient()
            manager = PlaylistManager()

            # 日付範囲を取得
            start_date, end_date = date_range
            published_after = datetime.fromisoformat(start_date)
            published_before = datetime.fromisoformat(end_date)

            self.root.after(0, lambda: self._update_progress("動画を検索中..."))

            # 検索（精度に応じて異なる方法を使用）
            search_count = min(count * 5, 200)
            videos = []

            if precision in (SearchPrecision.HIGH, SearchPrecision.HIGHEST):
                # 高精度・最高精度検索
                self.root.after(0, lambda: self._append_result(
                    f"高精度検索モード: {'公式チャンネルIDから検索' if precision == SearchPrecision.HIGHEST else '公式チャンネルフィルタ'}"
                ))

                for video in client.search_videos_advanced(
                    query=full_query,
                    max_results=search_count,
                    published_after=published_after,
                    published_before=published_before,
                    video_category_id=category_id if precision != SearchPrecision.HIGHEST else None,
                    region_code=region_code,
                    precision=precision,
                    category=category,
                ):
                    if not self.is_running:
                        return
                    videos.append(video)
                    if len(videos) % 10 == 0:
                        msg = f"検索中... {len(videos)}本の動画を取得"
                        self.root.after(0, lambda m=msg: self._update_progress(m))
            else:
                # 標準検索
                for video in client.search_videos(
                    query=full_query,
                    max_results=search_count,
                    published_after=published_after,
                    published_before=published_before,
                    video_category_id=category_id,
                    region_code=region_code,
                ):
                    if not self.is_running:
                        return
                    videos.append(video)
                    if len(videos) % 10 == 0:
                        msg = f"検索中... {len(videos)}本の動画を取得"
                        self.root.after(0, lambda m=msg: self._update_progress(m))

            if not videos:
                self.root.after(0, lambda: self._update_progress("動画が見つかりませんでした"))
                self.root.after(0, lambda: self._append_result("\n条件に合う動画が見つかりませんでした。"))
                if precision == SearchPrecision.HIGHEST:
                    self.root.after(0, lambda: self._append_result("ヒント: 最高精度モードは登録済み公式チャンネルのみ検索します。"))
                    self.root.after(0, lambda: self._append_result("検索精度を「標準」または「高精度」に変更してお試しください。"))
                else:
                    self.root.after(0, lambda: self._append_result("検索クエリや条件を変更してお試しください。"))
                self.root.after(0, self._finish_execution)
                return

            self.root.after(0, lambda: self._append_result(f"\n{len(videos)}本の動画が見つかりました"))

            # チャンネル情報を付加して品質スコアを計算
            if precision in (SearchPrecision.HIGH, SearchPrecision.HIGHEST):
                self.root.after(0, lambda: self._update_progress("チャンネル情報を取得中..."))
                videos = client.enrich_videos_with_channel_info(videos)
            else:
                # 標準モードでも品質スコアを計算
                for video in videos:
                    video.calculate_quality_score()

            # 公式優先モードの場合、品質スコアでソート
            if prefer_official:
                self.root.after(0, lambda: self._update_progress("品質スコアで並び替え中..."))

                # 品質スコアでソート
                videos.sort(key=lambda v: v.quality_score, reverse=True)

                # 公式動画の数を集計（スコア50以上を公式とみなす）
                official_count = sum(1 for v in videos if v.quality_score >= 50)
                self.root.after(0, lambda: self._append_result(
                    f"公式/高品質チャンネルの動画: {official_count}本"
                ))

                # ソート済みリストから選択（上位を優先）
                if len(videos) <= count:
                    selected_videos = videos
                else:
                    # 上位の高品質動画を優先的に選択
                    top_count = min(count, official_count) if official_count > 0 else count
                    top_videos = videos[:top_count]

                    # 残りが必要な場合はランダムに追加
                    remaining_count = count - len(top_videos)
                    if remaining_count > 0 and len(videos) > top_count:
                        remaining_videos = videos[top_count:]
                        additional = random.sample(
                            remaining_videos,
                            min(remaining_count, len(remaining_videos))
                        )
                        top_videos.extend(additional)

                    selected_videos = top_videos
            else:
                # 通常モード: ランダムに選択
                if len(videos) <= count:
                    selected_videos = videos
                else:
                    selected_videos = random.sample(videos, count)

            self.selected_videos = selected_videos
            if prefer_official:
                self.root.after(0, lambda: self._append_result(
                    f"{len(selected_videos)}本を品質スコア優先で選択しました\n"
                ))
            else:
                self.root.after(0, lambda: self._append_result(
                    f"{len(selected_videos)}本をランダムに選択しました\n"
                ))

            # 動画カードを表示
            for i, video in enumerate(selected_videos, 1):
                self.root.after(0, lambda v=video, idx=i: self._create_video_card(v, idx))

            # 再生リスト作成
            self.root.after(0, lambda: self._update_progress("再生リストを作成中..."))

            playlist_title = f"Mix lists - {era} {category.capitalize()}"
            if country != "全世界":
                playlist_title += f" [{country}]"
            if keyword:
                playlist_title += f" ({keyword[:30]})"

            # 詳細説明を生成（オプションに応じて）
            if add_detailed_description:
                self.root.after(0, lambda: self._update_progress("説明文を生成中..."))
                playlist_id = manager.create_playlist_with_details(
                    title=playlist_title,
                    era=era,
                    category=category,
                    keywords=selected_keywords,
                    additional_keyword=additional_keyword,
                    country=country,
                    video_count=len(selected_videos),
                    privacy_status=privacy,
                    add_detailed_description=True,
                )
            else:
                description = f"ランダムに選択された{era}の{category}動画 ({len(selected_videos)}本)"
                if country != "全世界":
                    description += f" - 地域: {country}"
                playlist_id = manager.create_playlist(
                    title=playlist_title,
                    description=description,
                    privacy_status=privacy,
                )

            # 動画を追加
            self.root.after(0, lambda: self._update_progress("動画を追加中..."))

            video_ids = [v.video_id for v in selected_videos]
            success = 0
            fail = 0

            for i, video_id in enumerate(video_ids):
                if not self.is_running:
                    return
                if manager.add_video_to_playlist(playlist_id, video_id):
                    success += 1
                else:
                    fail += 1
                msg = f"動画を追加中... {i + 1}/{len(video_ids)}"
                self.root.after(0, lambda m=msg: self._update_progress(m))

            # 結果を表示
            playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
            self.playlist_url = playlist_url

            self.root.after(0, lambda: self._update_progress("完了!"))
            self.root.after(0, lambda: self._append_result("=" * 50))
            self.root.after(0, lambda: self._append_result("作成完了!"))
            self.root.after(0, lambda: self._append_result(f"  再生リスト: {playlist_title}"))
            self.root.after(0, lambda: self._append_result(f"  追加成功: {success}本"))
            if fail > 0:
                self.root.after(0, lambda: self._append_result(f"  追加失敗: {fail}本"))
            self.root.after(0, lambda: self._append_result(f"  URL: {playlist_url}"))
            self.root.after(0, lambda: self._append_result("=" * 50))

            # URLを設定
            self.root.after(0, lambda: self.url_var.set(playlist_url))
            self.root.after(0, lambda: self.copy_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.open_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.view_videos_btn.config(state=tk.NORMAL))

            # プレイリスト情報を保存（動画確認用）
            self.current_playlist_id = playlist_id
            self.current_playlist_title = playlist_title

            # 履歴に保存
            if self.current_search_conditions:
                self.history_manager.add(
                    title=playlist_title,
                    url=playlist_url,
                    playlist_id=playlist_id,
                    video_count=success,
                    conditions=self.current_search_conditions,
                )
                # 履歴表示を更新
                self.root.after(0, self._refresh_history)

            # ========================================
            # マルチプラットフォーム検索（ニコニコ動画）
            # ========================================
            if is_multi_platform:
                self.root.after(0, lambda: self._append_result("\n" + "=" * 50))
                self.root.after(0, lambda: self._append_result("マルチプラットフォーム検索を開始..."))

                # 統合プレイリストを作成
                integrated_title = f"{playlist_title} (統合)"
                integrated_playlist = self.integrated_playlist_manager.create(
                    title=integrated_title,
                    description=f"年代: {era}, カテゴリ: {category}, キーワード: {keyword}"
                )

                # YouTubeの動画を統合プレイリストに追加
                if "youtube" in selected_platforms and selected_videos:
                    for video in selected_videos:
                        item = create_integrated_item_from_youtube(video)
                        integrated_playlist.add_item(item)
                    integrated_playlist.youtube_playlist_id = playlist_id
                    integrated_playlist.youtube_playlist_url = playlist_url

                # ニコニコ動画検索
                if "niconico" in selected_platforms:
                    self.root.after(0, lambda: self._update_progress("ニコニコ動画で検索中..."))
                    self.root.after(0, lambda: self._append_result("\nニコニコ動画で検索中..."))

                    nico_videos = []
                    try:
                        for video in self.niconico_client.search_videos(
                            query=full_query,
                            max_results=min(count, 50),
                        ):
                            if not self.is_running:
                                break
                            nico_videos.append(video)

                        if nico_videos:
                            self.root.after(0, lambda: self._append_result(f"ニコニコ動画: {len(nico_videos)}本の動画が見つかりました"))
                            for video in nico_videos:
                                item = create_integrated_item_from_niconico(video)
                                integrated_playlist.add_item(item)
                        else:
                            self.root.after(0, lambda: self._append_result("ニコニコ動画: 動画が見つかりませんでした"))
                    except Exception as e:
                        self.root.after(0, lambda: self._append_result(f"ニコニコ動画検索エラー: {str(e)}"))

                # 統合プレイリストを保存
                self.integrated_playlist_manager.update(integrated_playlist)
                self.current_integrated_playlist = integrated_playlist

                # 結果を表示
                counts = integrated_playlist.get_platform_counts()
                self.root.after(0, lambda: self._append_result("\n" + "=" * 50))
                self.root.after(0, lambda: self._append_result("統合プレイリスト作成完了!"))
                self.root.after(0, lambda: self._append_result(f"  タイトル: {integrated_title}"))
                self.root.after(0, lambda: self._append_result(f"  合計: {len(integrated_playlist.items)}本"))
                for platform, cnt in counts.items():
                    platform_names = {"youtube": "YouTube", "niconico": "ニコニコ動画"}
                    self.root.after(0, lambda p=platform, c=cnt: self._append_result(f"    {platform_names.get(p, p)}: {c}本"))
                self.root.after(0, lambda: self._append_result("=" * 50))
                self.root.after(0, lambda: self._append_result("※ ビューワーから動画を再生できます"))

                # 統合プレイリストリストを更新
                self.root.after(0, self._refresh_integrated_playlists)

        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self._update_progress("エラーが発生しました"))
            self.root.after(0, lambda: self._append_result(f"\nエラー: {error_msg}"))

        finally:
            self.root.after(0, self._finish_execution)


def main():
    """メイン関数"""
    root = tk.Tk()

    # スタイル設定
    style = ttk.Style()
    style.configure("TLabel", padding=2)
    style.configure("TButton", padding=5)

    app = PlaylistManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
