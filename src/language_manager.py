"""言語管理モジュール - 多言語対応"""

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
from pathlib import Path
from typing import Optional

from paths import CONFIG_PATH, get_internal_path


class LanguageManager:
    """言語管理クラス"""

    SUPPORTED_LANGUAGES = {
        'ja': '日本語',
        'en': 'English'
    }

    def __init__(self):
        self.current_language = 'ja'  # デフォルト: 日本語
        self.translations: dict[str, dict] = {}
        self._load_translations()
        self._load_preference()

    def _load_translations(self):
        """翻訳ファイルを読み込む"""
        # PyInstaller対応: get_internal_path()を使用
        internal_path = get_internal_path()
        lang_dir = internal_path / 'src' / 'languages'

        print(f"[DEBUG] Language manager: internal_path = {internal_path}")
        print(f"[DEBUG] Language manager: lang_dir = {lang_dir}")
        print(f"[DEBUG] Language manager: lang_dir.exists() = {lang_dir.exists()}")

        # フォールバック: 直接srcディレクトリ内を参照
        if not lang_dir.exists():
            lang_dir = Path(__file__).parent / 'languages'
            print(f"[DEBUG] Language manager: fallback lang_dir = {lang_dir}")

        for lang_code in self.SUPPORTED_LANGUAGES.keys():
            filepath = lang_dir / f'{lang_code}.json'
            print(f"[DEBUG] Language manager: loading {filepath} (exists={filepath.exists()})")

            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                        print(f"[DEBUG] Language manager: loaded {len(self.translations[lang_code])} translations for {lang_code}")
                except (json.JSONDecodeError, IOError) as e:
                    print(f"翻訳ファイル読み込みエラー ({lang_code}): {e}")
                    self.translations[lang_code] = {}

    def _load_preference(self):
        """保存された言語設定を読み込む"""
        config_file = CONFIG_PATH / 'settings.json'
        try:
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    lang_code = settings.get('language', 'ja')
                    if lang_code in self.SUPPORTED_LANGUAGES:
                        self.current_language = lang_code
        except (json.JSONDecodeError, IOError):
            pass

    def save_preference(self):
        """言語設定を保存する"""
        config_file = CONFIG_PATH / 'settings.json'
        try:
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            else:
                settings = {}

            settings['language'] = self.current_language

            CONFIG_PATH.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except (json.JSONDecodeError, IOError) as e:
            print(f"言語設定保存エラー: {e}")

    def set_language(self, lang_code: str) -> bool:
        """言語を設定する

        Args:
            lang_code: 言語コード ('ja', 'en')

        Returns:
            設定に成功した場合True
        """
        if lang_code in self.SUPPORTED_LANGUAGES:
            self.current_language = lang_code
            self.save_preference()
            return True
        return False

    def get(self, key: str, default: Optional[str] = None) -> str:
        """翻訳テキストを取得する

        Args:
            key: 翻訳キー
            default: キーが見つからない場合のデフォルト値

        Returns:
            翻訳されたテキスト
        """
        if self.current_language in self.translations:
            return self.translations[self.current_language].get(key, default or key)
        return default or key

    def get_current_language(self) -> str:
        """現在の言語コードを取得する"""
        return self.current_language

    def get_current_language_name(self) -> str:
        """現在の言語名を取得する"""
        return self.SUPPORTED_LANGUAGES.get(self.current_language, 'Unknown')

    def get_available_languages(self) -> dict[str, str]:
        """利用可能な言語のリストを取得する"""
        return self.SUPPORTED_LANGUAGES.copy()


# グローバルインスタンス
lang_manager = LanguageManager()


def t(key: str, default: Optional[str] = None) -> str:
    """翻訳のショートカット関数

    Args:
        key: 翻訳キー
        default: キーが見つからない場合のデフォルト値

    Returns:
        翻訳されたテキスト
    """
    return lang_manager.get(key, default)
