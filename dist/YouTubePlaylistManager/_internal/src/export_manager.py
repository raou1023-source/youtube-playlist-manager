"""エクスポート管理モジュール - プレイリストデータのエクスポート"""

import sys
import os

# 親ディレクトリをパスに追加（通常のPython実行用）
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import csv
import json
from datetime import datetime
from pathlib import Path


class ExportManager:
    """エクスポートの管理クラス"""

    @staticmethod
    def export_to_csv(data: list, filepath: Path) -> None:
        """プレイリストデータをCSV形式でエクスポート

        Args:
            data: エクスポートするプレイリストデータのリスト
            filepath: 出力ファイルパス
        """
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            if not data:
                return

            writer = csv.writer(f)

            # ヘッダー
            writer.writerow([
                '再生リスト名', '作成日時', '年代', 'カテゴリ', 'キーワード', '地域',
                '動画タイトル', 'チャンネル名', 'URL', '公開日'
            ])

            # データ行
            for playlist in data:
                playlist_name = playlist.get('title', '')
                created_at = playlist.get('created_at', '')
                era = playlist.get('era', '')
                category = playlist.get('category', '')
                keywords = ', '.join(playlist.get('keywords', []))
                region = playlist.get('region', '')

                videos = playlist.get('videos', [])
                if videos:
                    for video in videos:
                        writer.writerow([
                            playlist_name,
                            created_at,
                            era,
                            category,
                            keywords,
                            region,
                            video.get('title', ''),
                            video.get('channel', ''),
                            video.get('url', ''),
                            video.get('published_at', '')
                        ])
                else:
                    # 動画情報がない場合
                    writer.writerow([
                        playlist_name, created_at, era, category,
                        keywords, region, '', '', '', ''
                    ])

    @staticmethod
    def export_to_json(data: list, filepath: Path) -> None:
        """プレイリストデータをJSON形式でエクスポート

        Args:
            data: エクスポートするプレイリストデータのリスト
            filepath: 出力ファイルパス
        """
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'version': '1.0.0',
            'playlists': data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def export_to_txt(data: list, filepath: Path) -> None:
        """プレイリストデータをテキスト形式でエクスポート

        Args:
            data: エクスポートするプレイリストデータのリスト
            filepath: 出力ファイルパス
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("YouTube Playlist Manager - エクスポート\n")
            f.write(f"エクスポート日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            for playlist in data:
                f.write(f"■ {playlist.get('title', 'タイトルなし')}\n")
                f.write(f"  作成日時: {playlist.get('created_at', 'N/A')}\n")
                f.write(f"  年代: {playlist.get('era', 'N/A')}\n")
                f.write(f"  カテゴリ: {playlist.get('category', 'N/A')}\n")
                f.write(f"  キーワード: {', '.join(playlist.get('keywords', []))}\n")
                f.write(f"  地域: {playlist.get('region', 'N/A')}\n")
                f.write(f"  URL: {playlist.get('url', 'N/A')}\n")
                f.write("\n  動画一覧:\n")

                videos = playlist.get('videos', [])
                if videos:
                    for i, video in enumerate(videos, 1):
                        f.write(f"    {i}. {video.get('title', 'N/A')}\n")
                        f.write(f"       チャンネル: {video.get('channel', 'N/A')}\n")
                        f.write(f"       URL: {video.get('url', 'N/A')}\n")
                else:
                    f.write("    (動画情報なし)\n")

                f.write("\n" + "-" * 60 + "\n\n")

    @staticmethod
    def export_history_to_csv(history_entries: list, filepath: Path) -> None:
        """履歴エントリーをCSV形式でエクスポート

        Args:
            history_entries: HistoryEntryオブジェクトのリスト
            filepath: 出力ファイルパス
        """
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)

            # ヘッダー
            writer.writerow([
                '作成日時', 'タイトル', 'URL', '動画数', 'プラットフォーム',
                '年代', 'カテゴリ', 'キーワード', '地域', '国'
            ])

            # データ行
            for entry in history_entries:
                writer.writerow([
                    entry.get_formatted_date(),
                    entry.title,
                    entry.url,
                    entry.video_count,
                    entry.get_platform_display(),
                    entry.conditions.era,
                    entry.conditions.category,
                    ', '.join(entry.conditions.keywords),
                    entry.conditions.region_group,
                    entry.conditions.country,
                ])

    @staticmethod
    def export_history_to_json(history_entries: list, filepath: Path) -> None:
        """履歴エントリーをJSON形式でエクスポート

        Args:
            history_entries: HistoryEntryオブジェクトのリスト
            filepath: 出力ファイルパス
        """
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'version': '1.0.0',
            'history': [entry.to_dict() for entry in history_entries]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def export_history_to_txt(history_entries: list, filepath: Path) -> None:
        """履歴エントリーをテキスト形式でエクスポート

        Args:
            history_entries: HistoryEntryオブジェクトのリスト
            filepath: 出力ファイルパス
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("YouTube Playlist Manager - 履歴エクスポート\n")
            f.write(f"エクスポート日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            for entry in history_entries:
                f.write(f"■ {entry.title}\n")
                f.write(f"  作成日時: {entry.get_formatted_date()}\n")
                f.write(f"  URL: {entry.url}\n")
                f.write(f"  動画数: {entry.video_count}\n")
                f.write(f"  プラットフォーム: {entry.get_platform_display()}\n")
                f.write(f"  年代: {entry.conditions.era}\n")
                f.write(f"  カテゴリ: {entry.conditions.category}\n")
                f.write(f"  キーワード: {', '.join(entry.conditions.keywords)}\n")
                f.write(f"  地域: {entry.conditions.region_group}\n")
                f.write(f"  国: {entry.conditions.country}\n")
                f.write("\n" + "-" * 60 + "\n\n")
