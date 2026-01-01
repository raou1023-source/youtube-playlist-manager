"""YouTube Playlist Manager - メインエントリーポイント"""

import sys
import os

# 親ディレクトリをパスに追加（通常のPython実行用）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import argparse
import random
from datetime import datetime
from dotenv import load_dotenv

from youtube_client import YouTubeClient
from playlist_manager import PlaylistManager
from video_classifier import create_classifier
from config import get_category_id, get_era_date_range, CATEGORY_NAME_TO_ID
from setup_wizard import SetupStatus


def list_liked_videos(args):
    """高く評価した動画を一覧表示"""
    client = YouTubeClient()
    videos = list(client.get_liked_videos(max_results=args.limit))

    print(f"\n高く評価した動画 ({len(videos)}本):\n")
    for i, video in enumerate(videos, 1):
        print(f"{i:3}. [{video.year}] {video.title}")
        print(f"     チャンネル: {video.channel_title}")
        print(f"     ID: {video.video_id}\n")


def list_playlists(args):
    """自分の再生リストを一覧表示"""
    client = YouTubeClient()
    playlists = client.get_my_playlists(max_results=args.limit)

    print(f"\n再生リスト一覧 ({len(playlists)}件):\n")
    for playlist in playlists:
        print(f"- {playlist.title} ({playlist.item_count}本)")
        print(f"  ID: {playlist.playlist_id}\n")


def analyze_videos(args):
    """動画を年代別に分析"""
    client = YouTubeClient()

    # ソースを決定
    if args.playlist:
        print(f"再生リスト '{args.playlist}' を分析中...")
        videos = list(client.get_playlist_videos(args.playlist, max_results=args.limit))
    else:
        print("高く評価した動画を分析中...")
        videos = list(client.get_liked_videos(max_results=args.limit))

    if not videos:
        print("動画が見つかりませんでした。")
        return

    classifier = create_classifier(args.era_unit)
    grouped = classifier.group_by_era(videos)

    print(f"\n年代別分析 ({args.era_unit}単位):\n")
    for era_label in sorted(grouped.keys()):
        era_videos = grouped[era_label]
        print(f"{era_label}: {len(era_videos)}本")

    if args.category:
        print("\nカテゴリ別分析:\n")
        cat_grouped = classifier.group_by_category(videos)
        for category in sorted(cat_grouped.keys()):
            cat_videos = cat_grouped[category]
            print(f"{category}: {len(cat_videos)}本")


def create_playlists(args):
    """年代別/カテゴリ別の再生リストを作成"""
    client = YouTubeClient()
    manager = PlaylistManager()

    # ソースを決定
    if args.playlist:
        print(f"再生リスト '{args.playlist}' から動画を取得中...")
        videos = list(client.get_playlist_videos(args.playlist, max_results=args.limit))
    else:
        print("高く評価した動画を取得中...")
        videos = list(client.get_liked_videos(max_results=args.limit))

    if not videos:
        print("動画が見つかりませんでした。")
        return

    print(f"{len(videos)}本の動画を取得しました。\n")

    results = []

    if args.by_era:
        print(f"年代別再生リストを作成中 ({args.era_unit}単位)...")
        era_results = manager.create_era_playlists(
            videos=videos,
            era_unit=args.era_unit,
            title_prefix=args.prefix,
            privacy_status=args.privacy,
        )
        results.extend(era_results)

    if args.by_category:
        print("カテゴリ別再生リストを作成中...")
        cat_results = manager.create_category_playlists(
            videos=videos,
            title_prefix=args.prefix,
            privacy_status=args.privacy,
        )
        results.extend(cat_results)

    print(f"\n作成完了: {len(results)}個の再生リスト\n")
    for result in results:
        print(f"- {result.title} ({result.video_count}本)")
        print(f"  {result.url}\n")


def random_search(args):
    """年代・カテゴリを指定してランダムに動画を選択し、再生リストを作成"""
    client = YouTubeClient()
    manager = PlaylistManager()

    # カテゴリIDを取得
    category_id = get_category_id(args.category)
    if not category_id:
        available_categories = ", ".join(sorted(CATEGORY_NAME_TO_ID.keys()))
        print(f"エラー: 不明なカテゴリ '{args.category}'")
        print(f"利用可能なカテゴリ: {available_categories}")
        sys.exit(1)

    # 年代から日付範囲を取得
    date_range = get_era_date_range(args.era)
    if not date_range:
        print(f"エラー: 不明な年代 '{args.era}'")
        print("利用可能な年代: 2020s, 2010s, 2000s, 1990s, 1980s")
        sys.exit(1)

    start_date, end_date = date_range
    published_after = datetime.fromisoformat(start_date)
    published_before = datetime.fromisoformat(end_date)

    # 検索クエリを構築
    search_query = args.query if args.query else ""

    # ランダム性を高めるための検索キーワードリスト
    random_keywords = [
        "", "official", "live", "MV", "video", "full",
        "best", "new", "hit", "top", "classic", "popular"
    ]

    # 追加のランダムキーワードを選択
    random_suffix = random.choice(random_keywords)
    if search_query:
        full_query = f"{search_query} {random_suffix}".strip()
    else:
        full_query = random_suffix if random_suffix else "popular"

    print(f"\n検索条件:")
    print(f"  年代: {args.era}")
    print(f"  カテゴリ: {args.category} (ID: {category_id})")
    print(f"  検索クエリ: {full_query}")
    print(f"  選択数: {args.count}本\n")

    # 多めに検索してからランダムに選択
    search_count = min(args.count * 5, 200)  # 最大200本を検索
    print(f"YouTubeから動画を検索中 (最大{search_count}本)...")

    videos = list(client.search_videos(
        query=full_query,
        max_results=search_count,
        published_after=published_after,
        published_before=published_before,
        video_category_id=category_id,
    ))

    if not videos:
        print("条件に合う動画が見つかりませんでした。")
        print("検索クエリや条件を変更してお試しください。")
        return

    print(f"{len(videos)}本の動画が見つかりました。")

    # ランダムにN本選択
    if len(videos) <= args.count:
        selected_videos = videos
    else:
        selected_videos = random.sample(videos, args.count)

    print(f"{len(selected_videos)}本をランダムに選択しました。\n")

    # 再生リストを作成
    playlist_title = f"Mix lists - {args.era} {args.category.capitalize()}"
    if args.query:
        playlist_title += f" ({args.query})"

    description = f"ランダムに選択された{args.era}の{args.category}動画 ({len(selected_videos)}本)"

    print(f"再生リスト '{playlist_title}' を作成中...")

    playlist_id = manager.create_playlist(
        title=playlist_title,
        description=description,
        privacy_status=args.privacy,
    )

    # 動画を追加
    video_ids = [v.video_id for v in selected_videos]
    success, fail = manager.add_videos_to_playlist(playlist_id, video_ids)

    print(f"\n作成完了!")
    print(f"  再生リスト: {playlist_title}")
    print(f"  追加成功: {success}本")
    if fail > 0:
        print(f"  追加失敗: {fail}本")
    print(f"  URL: https://www.youtube.com/playlist?list={playlist_id}")

    print(f"\n選択された動画:")
    for i, video in enumerate(selected_videos[:10], 1):
        print(f"  {i:2}. [{video.year}] {video.title[:50]}...")
    if len(selected_videos) > 10:
        print(f"  ... 他{len(selected_videos) - 10}本")


def main():
    """メイン関数"""
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="YouTube再生リスト管理ツール - 年代別・ジャンル別に再生リストを作成",
    )
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    # list-liked コマンド
    liked_parser = subparsers.add_parser("list-liked", help="高く評価した動画を一覧表示")
    liked_parser.add_argument("-l", "--limit", type=int, default=50, help="取得する動画数")
    liked_parser.set_defaults(func=list_liked_videos)

    # list-playlists コマンド
    playlists_parser = subparsers.add_parser("list-playlists", help="再生リスト一覧を表示")
    playlists_parser.add_argument("-l", "--limit", type=int, default=50, help="取得する再生リスト数")
    playlists_parser.set_defaults(func=list_playlists)

    # analyze コマンド
    analyze_parser = subparsers.add_parser("analyze", help="動画を年代別に分析")
    analyze_parser.add_argument("-p", "--playlist", help="分析する再生リストID")
    analyze_parser.add_argument("-l", "--limit", type=int, default=200, help="取得する動画数")
    analyze_parser.add_argument(
        "-u", "--era-unit",
        choices=["decade", "half_decade", "three_year", "10", "5", "3"],
        default="decade",
        help="年代の単位 (decade=10年, half_decade=5年, three_year=3年)",
    )
    analyze_parser.add_argument("-c", "--category", action="store_true", help="カテゴリ別も分析")
    analyze_parser.set_defaults(func=analyze_videos)

    # create コマンド
    create_parser = subparsers.add_parser("create", help="年代別/カテゴリ別の再生リストを作成")
    create_parser.add_argument("-p", "--playlist", help="ソースとなる再生リストID")
    create_parser.add_argument("-l", "--limit", type=int, default=500, help="取得する動画数")
    create_parser.add_argument(
        "-u", "--era-unit",
        choices=["decade", "half_decade", "three_year", "10", "5", "3"],
        default="decade",
        help="年代の単位 (decade=10年, half_decade=5年, three_year=3年)",
    )
    create_parser.add_argument("--by-era", action="store_true", help="年代別の再生リストを作成")
    create_parser.add_argument("--by-category", action="store_true", help="カテゴリ別の再生リストを作成")
    create_parser.add_argument("--prefix", default="", help="再生リストタイトルの接頭辞")
    create_parser.add_argument(
        "--privacy",
        choices=["private", "unlisted", "public"],
        default="private",
        help="再生リストのプライバシー設定",
    )
    create_parser.set_defaults(func=create_playlists)

    # random コマンド
    random_parser = subparsers.add_parser(
        "random",
        help="年代・カテゴリを指定してランダムに動画を選択し再生リストを作成",
    )
    random_parser.add_argument(
        "-e", "--era",
        required=True,
        help="年代 (例: 2020s, 2010s, 2000s, 1990s, 1980s)",
    )
    random_parser.add_argument(
        "-c", "--category",
        required=True,
        help="カテゴリ (例: music, entertainment, gaming, sports, education)",
    )
    random_parser.add_argument(
        "-n", "--count",
        type=int,
        default=20,
        help="選択する動画数 (デフォルト: 20)",
    )
    random_parser.add_argument(
        "-q", "--query",
        help="追加の検索キーワード (オプション)",
    )
    random_parser.add_argument(
        "--privacy",
        choices=["private", "unlisted", "public"],
        default="private",
        help="再生リストのプライバシー設定",
    )
    random_parser.set_defaults(func=random_search)

    # setup コマンド
    setup_parser = subparsers.add_parser(
        "setup",
        help="セットアップウィザードを起動",
    )
    setup_parser.add_argument(
        "--reset",
        action="store_true",
        help="セットアップ状態をリセット",
    )
    setup_parser.add_argument(
        "--status",
        action="store_true",
        help="セットアップ状態を表示",
    )
    setup_parser.set_defaults(func=run_setup_command)

    # gui コマンド
    gui_parser = subparsers.add_parser(
        "gui",
        help="GUIアプリケーションを起動",
    )
    gui_parser.add_argument(
        "--skip-setup",
        action="store_true",
        help="セットアップチェックをスキップ",
    )
    gui_parser.set_defaults(func=run_gui_command)

    args = parser.parse_args()

    if args.command is None:
        # コマンドなしの場合はGUIを起動
        run_gui_command(argparse.Namespace(skip_setup=False))
        return

    args.func(args)


def run_setup_command(args):
    """セットアップコマンドを実行"""
    if args.status:
        # セットアップ状態を表示
        print("\nセットアップ状態:")
        print(f"  セットアップ完了: {'✓ Yes' if SetupStatus.is_setup_complete() else '✗ No'}")
        print(f"  client_secret.json: {'✓ 存在' if SetupStatus.has_client_secret() else '✗ 未設定'}")
        print(f"  token.pickle: {'✓ 存在' if SetupStatus.has_token() else '✗ 未作成'}")
        return

    if args.reset:
        # セットアップ状態をリセット
        SetupStatus.reset_setup()
        print("セットアップ状態をリセットしました。")
        return

    # GUIでセットアップウィザードを起動
    import tkinter as tk
    from setup_wizard import SetupWizard

    root = tk.Tk()
    root.withdraw()  # メインウィンドウを隠す

    def on_complete(success):
        if success:
            print("セットアップが完了しました！")
        root.destroy()

    wizard = SetupWizard(on_complete=on_complete)
    wizard.run()


def run_gui_command(args):
    """GUIコマンドを実行"""
    import tkinter as tk
    from tkinter import ttk
    from gui import PlaylistManagerGUI

    root = tk.Tk()

    # スタイル設定
    style = ttk.Style()
    style.configure("TLabel", padding=2)
    style.configure("TButton", padding=5)

    app = PlaylistManagerGUI(root, skip_setup_check=args.skip_setup)
    root.mainloop()


if __name__ == "__main__":
    main()
