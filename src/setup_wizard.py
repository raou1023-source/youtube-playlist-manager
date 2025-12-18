"""セットアップウィザードモジュール - 初回セットアップをガイド"""

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
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Optional, Callable
import webbrowser
import threading

from paths import (
    CREDENTIALS_PATH as CREDENTIALS_DIR,
    CONFIG_PATH as CONFIG_DIR,
    CLIENT_SECRET_FILE,
    TOKEN_FILE,
    NICONICO_AUTH_FILE,
    SETUP_COMPLETE_FILE,
    ensure_directories,
)


class SetupStatus:
    """セットアップ状態管理"""

    @staticmethod
    def is_setup_complete() -> bool:
        """セットアップが完了しているかチェック"""
        if not SETUP_COMPLETE_FILE.exists():
            return False
        try:
            with open(SETUP_COMPLETE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("setup_complete", False)
        except (json.JSONDecodeError, IOError):
            return False

    @staticmethod
    def mark_setup_complete():
        """セットアップ完了をマーク"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(SETUP_COMPLETE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "setup_complete": True,
                "version": "1.0",
            }, f, indent=2)

    @staticmethod
    def reset_setup():
        """セットアップ状態をリセット"""
        if SETUP_COMPLETE_FILE.exists():
            SETUP_COMPLETE_FILE.unlink()

    @staticmethod
    def has_client_secret() -> bool:
        """client_secret.json が存在するかチェック"""
        return CLIENT_SECRET_FILE.exists()

    @staticmethod
    def has_token() -> bool:
        """token.pickle が存在するかチェック"""
        return TOKEN_FILE.exists()

    @staticmethod
    def needs_setup() -> bool:
        """セットアップが必要かチェック"""
        if SetupStatus.is_setup_complete():
            return False
        # client_secret.json がない場合はセットアップ必要
        if not SetupStatus.has_client_secret():
            return True
        return False


class SetupWizard:
    """セットアップウィザード"""

    # ステップ定義
    STEPS = [
        "ようこそ",
        "フォルダ準備",
        "Google Cloud設定",
        "認証情報アップロード",
        "YouTube認証",
        "テスト実行",
        "ニコニコ動画設定",
        "完了",
    ]

    def __init__(self, parent: Optional[tk.Tk] = None, on_complete: Optional[Callable] = None):
        """
        Args:
            parent: 親ウィンドウ（Noneの場合は新規作成）
            on_complete: 完了時のコールバック
        """
        self.on_complete = on_complete
        self.current_step = 0
        self.client_secret_valid = False
        self.auth_success = False
        self.test_success = False
        self.niconico_configured = False

        # ウィンドウ作成
        if parent:
            self.window = tk.Toplevel(parent)
        else:
            self.window = tk.Tk()

        self.window.title("セットアップウィザード - YouTube Playlist Manager")
        self.window.geometry("850x700")
        self.window.resizable(True, True)
        self.window.minsize(700, 600)

        # ウィンドウを中央に配置
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")

        # ディレクトリを作成
        CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        self._create_widgets()
        self._show_step(0)

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
                f"エラー詳細: {str(e)[:100]}",
                parent=self.window
            )
            return False

    def _copy_to_clipboard(self, text: str):
        """テキストをクリップボードにコピー

        Args:
            text: コピーするテキスト
        """
        try:
            self.window.clipboard_clear()
            self.window.clipboard_append(text)
            self.window.update()
            messagebox.showinfo(
                "コピー完了",
                "URLをクリップボードにコピーしました",
                parent=self.window
            )
        except Exception as e:
            messagebox.showerror(
                "エラー",
                f"クリップボードにコピーできませんでした:\n{str(e)}",
                parent=self.window
            )

    def _create_widgets(self):
        """ウィジェットを作成"""
        # メインフレーム
        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # ヘッダーフレーム（ステップインジケーター）
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        # ステップインジケーター
        self.step_label = ttk.Label(
            header_frame,
            text="ステップ 1/8",
            font=("", 10)
        )
        self.step_label.pack(side=tk.LEFT)

        # 進捗バー
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            header_frame,
            variable=self.progress_var,
            maximum=100,
            length=200,
            mode="determinate"
        )
        self.progress_bar.pack(side=tk.RIGHT)

        # ボタンフレーム（先にpackして下部に固定）
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0))

        # セパレータ
        separator = ttk.Separator(self.main_frame, orient=tk.HORIZONTAL)
        separator.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # スクロール可能なコンテンツエリア
        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # キャンバスの幅をフレームに合わせる
        def configure_canvas(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind("<Configure>", configure_canvas)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # マウスホイールでスクロール
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # コンテンツフレームへの参照を設定
        self.content_frame = self.scrollable_frame

        # ボタン
        self.skip_btn = ttk.Button(
            self.button_frame,
            text="後で設定",
            command=self._skip_setup,
            width=12
        )
        self.skip_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.next_btn = ttk.Button(
            self.button_frame,
            text="次へ",
            command=self._next_step,
            width=12
        )
        self.next_btn.pack(side=tk.RIGHT)

        self.back_btn = ttk.Button(
            self.button_frame,
            text="戻る",
            command=self._prev_step,
            state=tk.DISABLED,
            width=12
        )
        self.back_btn.pack(side=tk.RIGHT, padx=(0, 10))

    def _clear_content(self):
        """コンテンツフレームをクリア"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        # スクロール位置をリセット
        self.canvas.yview_moveto(0)

    def _update_step_indicator(self):
        """ステップインジケーターを更新"""
        self.step_label.config(text=f"ステップ {self.current_step + 1}/{len(self.STEPS)}")
        progress = (self.current_step / (len(self.STEPS) - 1)) * 100
        self.progress_var.set(progress)

        # ボタン状態を更新
        if self.current_step == 0:
            self.back_btn.config(state=tk.DISABLED)
        else:
            self.back_btn.config(state=tk.NORMAL)

        if self.current_step == len(self.STEPS) - 1:
            self.next_btn.config(text="アプリを開始")
            self.skip_btn.pack_forget()
        else:
            self.next_btn.config(text="次へ")
            self.skip_btn.pack(side=tk.LEFT)

    def _show_step(self, step: int):
        """指定されたステップを表示"""
        self.current_step = step
        self._clear_content()
        self._update_step_indicator()

        step_methods = [
            self._show_welcome,
            self._show_folder_prep,
            self._show_google_cloud,
            self._show_upload_credentials,
            self._show_youtube_auth,
            self._show_test,
            self._show_niconico_setup,
            self._show_complete,
        ]

        if 0 <= step < len(step_methods):
            step_methods[step]()

    def _next_step(self):
        """次のステップへ"""
        # ステップ固有のバリデーション
        if self.current_step == 3 and not self.client_secret_valid:
            messagebox.showwarning("確認", "認証情報ファイルを選択してください")
            return
        if self.current_step == 4 and not self.auth_success:
            if not messagebox.askyesno("確認", "YouTube認証が完了していません。スキップしますか？"):
                return

        if self.current_step < len(self.STEPS) - 1:
            self._show_step(self.current_step + 1)
        else:
            self._finish_setup()

    def _prev_step(self):
        """前のステップへ"""
        if self.current_step > 0:
            self._show_step(self.current_step - 1)

    def _skip_setup(self):
        """セットアップをスキップ"""
        if messagebox.askyesno(
            "確認",
            "セットアップをスキップしますか？\n\n"
            "後で「設定」→「セットアップウィザード」から再開できます。"
        ):
            self.window.destroy()
            if self.on_complete:
                self.on_complete(False)

    def _finish_setup(self):
        """セットアップを完了"""
        SetupStatus.mark_setup_complete()
        self.window.destroy()
        if self.on_complete:
            self.on_complete(True)

    # ========================================
    # ステップ1: ようこそ画面
    # ========================================
    def _show_welcome(self):
        """ようこそ画面を表示"""
        # アイコン/タイトル
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(pady=(20, 10))

        icon_label = ttk.Label(
            title_frame,
            text="🎬",
            font=("", 40)
        )
        icon_label.pack()

        title_label = ttk.Label(
            title_frame,
            text="YouTube Playlist Manager へようこそ",
            font=("", 16, "bold")
        )
        title_label.pack(pady=(8, 0))

        # 説明
        desc_frame = ttk.Frame(self.content_frame)
        desc_frame.pack(fill=tk.X, padx=30, pady=10)

        desc_text = (
            "このウィザードでは、YouTube Playlist Managerを使用するための\n"
            "初期設定を行います。\n\n"
            "セットアップには約5分かかります。\n\n"
            "必要なもの:\n"
            "  • Googleアカウント\n"
            "  • Google Cloud Consoleへのアクセス\n"
            "  • インターネット接続"
        )

        desc_label = ttk.Label(
            desc_frame,
            text=desc_text,
            font=("", 10),
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W)

        # 現在の状態
        status_frame = ttk.LabelFrame(self.content_frame, text="現在の状態", padding="10")
        status_frame.pack(fill=tk.X, padx=30, pady=10)

        has_secret = SetupStatus.has_client_secret()
        has_token = SetupStatus.has_token()

        secret_status = "✓ 設定済み" if has_secret else "✗ 未設定"
        secret_color = "green" if has_secret else "red"
        ttk.Label(
            status_frame,
            text=f"認証情報 (client_secret.json): {secret_status}",
            foreground=secret_color
        ).pack(anchor=tk.W)

        token_status = "✓ ログイン済み" if has_token else "✗ 未ログイン"
        token_color = "green" if has_token else "red"
        ttk.Label(
            status_frame,
            text=f"YouTubeアカウント: {token_status}",
            foreground=token_color
        ).pack(anchor=tk.W)


    # ========================================
    # ステップ1.5: フォルダ準備
    # ========================================
    def _show_folder_prep(self):
        """フォルダ準備画面を表示"""
        import os

        # タイトル
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(pady=(20, 10))

        ttk.Label(
            title_frame,
            text="📁 準備フォルダの作成",
            font=("", 16, "bold")
        ).pack()

        # 説明
        desc_label = ttk.Label(
            self.content_frame,
            text="API認証情報を保存するフォルダを準備します。\n"
                 "ダウンロードしたJSONファイルをこのフォルダに保存してください。",
            font=("", 10),
            wraplength=500,
            justify=tk.CENTER
        )
        desc_label.pack(pady=(10, 20))

        # フォルダパス表示
        folder_frame = ttk.LabelFrame(self.content_frame, text="保存先フォルダ", padding="15")
        folder_frame.pack(fill=tk.X, padx=30, pady=10)

        # フォルダパス
        folder_path_text = str(CREDENTIALS_DIR)
        path_label = ttk.Label(
            folder_frame,
            text=f"📁 {folder_path_text}",
            font=("Consolas", 9),
            foreground="blue"
        )
        path_label.pack(anchor=tk.W, pady=(0, 10))

        # フォルダを開くボタン
        def open_folder():
            # フォルダが存在しない場合は作成
            CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
            try:
                os.startfile(str(CREDENTIALS_DIR))
            except Exception as e:
                messagebox.showerror("エラー", f"フォルダを開けませんでした: {e}")

        open_btn = ttk.Button(
            folder_frame,
            text="📂 フォルダを開く",
            command=open_folder
        )
        open_btn.pack(pady=(0, 10))

        # 自動でフォルダを開く
        self.window.after(500, open_folder)

        # 説明文
        instructions_frame = ttk.LabelFrame(self.content_frame, text="手順", padding="15")
        instructions_frame.pack(fill=tk.X, padx=30, pady=10)

        instructions = [
            "1. 上のフォルダが自動的に開きます",
            "2. 次のステップでGoogle Cloud ConsoleからJSONファイルをダウンロード",
            "3. ダウンロードしたファイルをこのフォルダに保存",
            "4. ファイル名は変更しなくてOK（後で自動リネームされます）",
        ]

        for inst in instructions:
            ttk.Label(
                instructions_frame,
                text=inst,
                font=("", 10),
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=2)

        # 注意事項
        note_frame = ttk.Frame(self.content_frame)
        note_frame.pack(fill=tk.X, padx=30, pady=10)

        ttk.Label(
            note_frame,
            text="💡 このフォルダはEXEファイルと同じ場所に作成されます。\n"
                 "   アプリを別の場所に移動する場合は、このフォルダも一緒に移動してください。",
            font=("", 9),
            foreground="gray",
            justify=tk.LEFT
        ).pack(anchor=tk.W)

    # ========================================
    # ステップ2: Google Cloud Console設定
    # ========================================
    def _show_google_cloud(self):
        """Google Cloud Console設定画面を表示"""
        # タイトル
        ttk.Label(
            self.content_frame,
            text="☁️ Google Cloud Console設定",
            font=("", 14, "bold")
        ).pack(pady=(10, 5))

        # 説明
        ttk.Label(
            self.content_frame,
            text="YouTube Data APIを使用するため、Google Cloud Consoleで設定が必要です。",
            font=("", 10),
            wraplength=600
        ).pack(pady=(0, 10))

        # 手順リスト（コンパクト）
        steps_frame = ttk.LabelFrame(self.content_frame, text="設定手順", padding="10")
        steps_frame.pack(fill=tk.X, padx=20, pady=5)

        steps = [
            ("1.", "Google Cloud Consoleにアクセス"),
            ("2.", "新しいプロジェクトを作成（または既存を選択）"),
            ("3.", "APIライブラリで「YouTube Data API v3」を有効化"),
            ("4.", "認証情報 → OAuth クライアントIDを作成"),
            ("5.", "アプリケーション種類: デスクトップアプリ"),
            ("6.", "作成後「JSONをダウンロード」"),
        ]

        for num, text in steps:
            step_frame = ttk.Frame(steps_frame)
            step_frame.pack(fill=tk.X, pady=2, anchor=tk.W)
            ttk.Label(step_frame, text=num, font=("", 9, "bold"), width=3).pack(side=tk.LEFT)
            ttk.Label(step_frame, text=text, font=("", 9)).pack(side=tk.LEFT)

        # ボタン
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=10)

        google_cloud_url = "https://console.cloud.google.com/"

        ttk.Button(btn_frame, text="🌐 Google Cloud Console",
                  command=lambda: self._open_url_safely(google_cloud_url)).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="📋 URL",
                  command=lambda: self._copy_to_clipboard(google_cloud_url)).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="📖 詳細手順",
                  command=self._show_youtube_api_help).pack(side=tk.LEFT, padx=3)

    # ========================================
    # ステップ3: 認証情報のアップロード
    # ========================================
    def _show_upload_credentials(self):
        """認証情報アップロード画面を表示"""
        # タイトル
        ttk.Label(
            self.content_frame,
            text="📁 認証情報のアップロード",
            font=("", 14, "bold")
        ).pack(pady=(10, 5))

        # 説明
        ttk.Label(
            self.content_frame,
            text="ダウンロードした client_secret_xxxxx.json ファイルを選択してください。",
            font=("", 10),
            wraplength=600
        ).pack(pady=(0, 10))

        # ファイル選択エリア
        upload_frame = ttk.LabelFrame(self.content_frame, text="ファイル選択", padding="10")
        upload_frame.pack(fill=tk.X, padx=20, pady=5)

        self.file_path_var = tk.StringVar(value="ファイルが選択されていません")
        ttk.Label(upload_frame, textvariable=self.file_path_var, wraplength=500).pack(pady=(0, 8))
        ttk.Button(upload_frame, text="📂 ファイルを選択", command=self._select_credentials_file).pack()

        # ステータス表示
        self.upload_status_var = tk.StringVar(value="")
        self.upload_status_label = ttk.Label(upload_frame, textvariable=self.upload_status_var, font=("", 10))
        self.upload_status_label.pack(pady=(8, 0))

        # 既にファイルがある場合
        if SetupStatus.has_client_secret():
            self.client_secret_valid = True
            self.upload_status_var.set("✓ 認証情報ファイルは既に設定されています")
            self.upload_status_label.config(foreground="green")
            self.file_path_var.set(str(CLIENT_SECRET_FILE))

    def _select_credentials_file(self):
        """認証情報ファイルを選択"""
        file_path = filedialog.askopenfilename(
            title="認証情報ファイルを選択",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not file_path:
            return

        # JSONの妥当性チェック
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 必須フィールドを確認
            if "installed" in data:
                client_data = data["installed"]
            elif "web" in data:
                client_data = data["web"]
            else:
                raise ValueError("認証情報の形式が不正です")

            required_fields = ["client_id", "client_secret"]
            for field in required_fields:
                if field not in client_data:
                    raise ValueError(f"必須フィールド '{field}' がありません")

            # ファイルをコピー
            CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy(file_path, CLIENT_SECRET_FILE)

            self.client_secret_valid = True
            self.file_path_var.set(Path(file_path).name)
            self.upload_status_var.set("✓ 認証情報ファイルを正常に読み込みました")
            self.upload_status_label.config(foreground="green")

        except json.JSONDecodeError:
            self.client_secret_valid = False
            self.upload_status_var.set("✗ JSONファイルの形式が不正です")
            self.upload_status_label.config(foreground="red")
        except ValueError as e:
            self.client_secret_valid = False
            self.upload_status_var.set(f"✗ {str(e)}")
            self.upload_status_label.config(foreground="red")
        except Exception as e:
            self.client_secret_valid = False
            self.upload_status_var.set(f"✗ エラー: {str(e)}")
            self.upload_status_label.config(foreground="red")

    # ========================================
    # ステップ4: YouTube認証
    # ========================================
    def _show_youtube_auth(self):
        """YouTube認証画面を表示"""
        # タイトル
        ttk.Label(
            self.content_frame,
            text="🔐 YouTube認証",
            font=("", 14, "bold")
        ).pack(pady=(10, 5))

        # 説明
        ttk.Label(
            self.content_frame,
            text="YouTubeアカウントでログインして、アプリに権限を付与します。",
            font=("", 10),
            wraplength=600
        ).pack(pady=(0, 10))

        # ログインボタン
        auth_frame = ttk.LabelFrame(self.content_frame, text="認証", padding="10")
        auth_frame.pack(fill=tk.X, padx=20, pady=5)

        self.login_btn = ttk.Button(auth_frame, text="🌐 YouTubeにログイン", command=self._start_youtube_auth)
        self.login_btn.pack(pady=8)

        # ステータス表示
        self.auth_status_var = tk.StringVar(value="")
        self.auth_status_label = ttk.Label(auth_frame, textvariable=self.auth_status_var, font=("", 10))
        self.auth_status_label.pack()

        # 既にログイン済みの場合
        if SetupStatus.has_token():
            self.auth_success = True
            self.auth_status_var.set("✓ 既にログイン済みです")
            self.auth_status_label.config(foreground="green")

        # 注意事項（コンパクト）
        note_text = (
            "注意: 「このアプリは確認されていません」と表示された場合は\n"
            "「詳細」→「〇〇（安全ではないページ）に移動」をクリック"
        )
        ttk.Label(
            self.content_frame,
            text=note_text,
            font=("", 8),
            foreground="gray",
            justify=tk.LEFT
        ).pack(padx=20, pady=5, anchor=tk.W)

    def _start_youtube_auth(self):
        """YouTube認証を開始"""
        self.login_btn.config(state=tk.DISABLED)
        self.auth_status_var.set("認証中... ブラウザでログインしてください")
        self.auth_status_label.config(foreground="blue")

        # バックグラウンドで認証実行
        thread = threading.Thread(target=self._run_youtube_auth, daemon=True)
        thread.start()

    def _run_youtube_auth(self):
        """YouTube認証を実行（バックグラウンド）"""
        try:
            from auth import YouTubeAuthenticator

            authenticator = YouTubeAuthenticator()
            credentials = authenticator.get_credentials()

            if credentials:
                self.auth_success = True
                self.window.after(0, lambda: self.auth_status_var.set("✓ 認証成功！"))
                self.window.after(0, lambda: self.auth_status_label.config(foreground="green"))
            else:
                self.auth_success = False
                self.window.after(0, lambda: self.auth_status_var.set("✗ 認証に失敗しました"))
                self.window.after(0, lambda: self.auth_status_label.config(foreground="red"))

        except Exception as e:
            self.auth_success = False
            error_msg = str(e)
            self.window.after(0, lambda: self.auth_status_var.set(f"✗ エラー: {error_msg[:50]}"))
            self.window.after(0, lambda: self.auth_status_label.config(foreground="red"))

        finally:
            self.window.after(0, lambda: self.login_btn.config(state=tk.NORMAL))

    # ========================================
    # ステップ5: テスト実行
    # ========================================
    def _show_test(self):
        """テスト画面を表示"""
        # タイトル
        ttk.Label(
            self.content_frame,
            text="🧪 接続テスト",
            font=("", 14, "bold")
        ).pack(pady=(10, 5))

        # 説明
        ttk.Label(
            self.content_frame,
            text="設定が正しく行われたかテストします。",
            font=("", 10)
        ).pack(pady=(0, 10))

        # テスト結果フレーム
        test_frame = ttk.LabelFrame(self.content_frame, text="テスト結果", padding="10")
        test_frame.pack(fill=tk.X, padx=20, pady=5)

        # テスト項目
        self.test_items = []

        tests = [
            ("認証情報ファイル", "client_secret.json の確認"),
            ("認証トークン", "token.pickle の確認"),
            ("YouTube API接続", "APIへの接続テスト"),
        ]

        for name, desc in tests:
            item_frame = ttk.Frame(test_frame)
            item_frame.pack(fill=tk.X, pady=3)

            status_label = ttk.Label(item_frame, text="⏳", width=3)
            status_label.pack(side=tk.LEFT)

            ttk.Label(item_frame, text=name, font=("", 9, "bold"), width=14).pack(side=tk.LEFT)
            ttk.Label(item_frame, text=desc, font=("", 9), foreground="gray").pack(side=tk.LEFT)

            self.test_items.append(status_label)

        # テスト実行ボタン
        self.test_btn = ttk.Button(test_frame, text="🔄 テストを実行", command=self._run_tests)
        self.test_btn.pack(pady=(10, 0))

        # 総合結果
        self.test_result_var = tk.StringVar(value="")
        self.test_result_label = ttk.Label(
            self.content_frame, textvariable=self.test_result_var, font=("", 11, "bold")
        )
        self.test_result_label.pack(pady=10)

        # トラブルシューティング
        trouble_frame = ttk.Frame(self.content_frame)
        trouble_frame.pack(fill=tk.X, padx=20)

        troubleshoot_url = "https://developers.google.com/youtube/v3/getting-started#before-you-start"

        ttk.Button(trouble_frame, text="❓ ヘルプ",
                  command=lambda: self._open_url_safely(troubleshoot_url)).pack(side=tk.LEFT, padx=3)
        ttk.Button(trouble_frame, text="📋 URL",
                  command=lambda: self._copy_to_clipboard(troubleshoot_url)).pack(side=tk.LEFT, padx=3)

    def _run_tests(self):
        """テストを実行"""
        self.test_btn.config(state=tk.DISABLED)
        self.test_result_var.set("")

        # バックグラウンドで実行
        thread = threading.Thread(target=self._execute_tests, daemon=True)
        thread.start()

    def _execute_tests(self):
        """テストを実行（バックグラウンド）"""
        results = []

        # テスト1: client_secret.json
        self.window.after(0, lambda: self.test_items[0].config(text="⏳"))
        if SetupStatus.has_client_secret():
            results.append(True)
            self.window.after(100, lambda: self.test_items[0].config(text="✓", foreground="green"))
        else:
            results.append(False)
            self.window.after(100, lambda: self.test_items[0].config(text="✗", foreground="red"))

        # テスト2: token.pickle
        self.window.after(200, lambda: self.test_items[1].config(text="⏳"))
        if SetupStatus.has_token():
            results.append(True)
            self.window.after(300, lambda: self.test_items[1].config(text="✓", foreground="green"))
        else:
            results.append(False)
            self.window.after(300, lambda: self.test_items[1].config(text="✗", foreground="red"))

        # テスト3: API接続
        self.window.after(400, lambda: self.test_items[2].config(text="⏳"))
        try:
            from youtube_client import YouTubeClient
            client = YouTubeClient()
            # 簡単なAPIコールでテスト
            liked = list(client.get_liked_videos(max_results=1))
            if liked or True:  # APIコールが成功すれば OK
                results.append(True)
                self.window.after(500, lambda: self.test_items[2].config(text="✓", foreground="green"))
            else:
                results.append(True)  # 高評価動画がなくても接続は成功
                self.window.after(500, lambda: self.test_items[2].config(text="✓", foreground="green"))
        except Exception as e:
            results.append(False)
            self.window.after(500, lambda: self.test_items[2].config(text="✗", foreground="red"))

        # 総合結果
        self.test_success = all(results)
        if self.test_success:
            self.window.after(600, lambda: self.test_result_var.set("✓ すべてのテストに成功しました！"))
            self.window.after(600, lambda: self.test_result_label.config(foreground="green"))
        else:
            passed = sum(results)
            total = len(results)
            self.window.after(600, lambda: self.test_result_var.set(f"⚠ {passed}/{total} のテストに成功"))
            self.window.after(600, lambda: self.test_result_label.config(foreground="orange"))

        self.window.after(600, lambda: self.test_btn.config(state=tk.NORMAL))

    # ========================================
    # ステップ6: ニコニコ動画設定（オプション）
    # ========================================
    def _show_niconico_setup(self):
        """ニコニコ動画設定画面を表示"""
        # タイトル
        ttk.Label(
            self.content_frame,
            text="📺 ニコニコ動画設定（オプション）",
            font=("", 14, "bold")
        ).pack(pady=(10, 5))

        # 説明
        ttk.Label(
            self.content_frame,
            text="ニコニコ動画も検索したい場合、ログイン情報を設定してください。スキップ可能です。",
            font=("", 10),
            wraplength=600
        ).pack(pady=(0, 5))

        # セキュリティ注意とヘルプボタン
        security_frame = ttk.Frame(self.content_frame)
        security_frame.pack(fill=tk.X, padx=20, pady=5)

        ttk.Label(security_frame, text="🔒 暗号化して保存されます",
                 font=("", 9), foreground="blue").pack(side=tk.LEFT)
        ttk.Button(security_frame, text="📖 詳細",
                  command=self._show_niconico_help).pack(side=tk.RIGHT)

        # ログイン情報入力エリア
        login_frame = ttk.LabelFrame(self.content_frame, text="ログイン情報", padding="8")
        login_frame.pack(fill=tk.X, padx=20, pady=5)

        # メールアドレス
        email_frame = ttk.Frame(login_frame)
        email_frame.pack(fill=tk.X, pady=3)
        ttk.Label(email_frame, text="メールアドレス:", width=14).pack(side=tk.LEFT)
        self.niconico_email_var = tk.StringVar()
        ttk.Entry(email_frame, textvariable=self.niconico_email_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # パスワード
        password_frame = ttk.Frame(login_frame)
        password_frame.pack(fill=tk.X, pady=3)
        ttk.Label(password_frame, text="パスワード:", width=14).pack(side=tk.LEFT)
        self.niconico_password_var = tk.StringVar()
        ttk.Entry(password_frame, textvariable=self.niconico_password_var, width=40, show="●").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 保存ボタン
        ttk.Button(login_frame, text="💾 認証情報を保存", command=self._save_niconico_credentials).pack(pady=(8, 0))

        # ステータス表示
        self.niconico_status_var = tk.StringVar(value="")
        self.niconico_status_label = ttk.Label(login_frame, textvariable=self.niconico_status_var, font=("", 10))
        self.niconico_status_label.pack(pady=(8, 0))

        # 既に認証情報がある場合
        if NICONICO_AUTH_FILE.exists():
            self.niconico_configured = True
            self.niconico_status_var.set("✓ ニコニコ動画の認証情報は既に設定されています")
            self.niconico_status_label.config(foreground="green")

        # 注意事項（コンパクト）
        ttk.Label(
            self.content_frame,
            text="注意: 認証情報はローカルに暗号化保存。一部機能はログイン不要です。",
            font=("", 8),
            foreground="gray"
        ).pack(padx=20, pady=5, anchor=tk.W)

    def _save_niconico_credentials(self):
        """ニコニコ動画の認証情報を保存"""
        email = self.niconico_email_var.get().strip()
        password = self.niconico_password_var.get()

        if not email:
            self.niconico_status_var.set("✗ メールアドレスを入力してください")
            self.niconico_status_label.config(foreground="red")
            return

        if not password:
            self.niconico_status_var.set("✗ パスワードを入力してください")
            self.niconico_status_label.config(foreground="red")
            return

        try:
            from credentials_manager import get_credentials_manager
            manager = get_credentials_manager()

            if manager.save_niconico_credentials(email, password):
                self.niconico_configured = True
                self.niconico_status_var.set("✓ 認証情報を暗号化して保存しました")
                self.niconico_status_label.config(foreground="green")
                # パスワードをクリア
                self.niconico_password_var.set("")
            else:
                self.niconico_status_var.set("✗ 保存に失敗しました")
                self.niconico_status_label.config(foreground="red")
        except Exception as e:
            self.niconico_status_var.set(f"✗ エラー: {str(e)[:30]}")
            self.niconico_status_label.config(foreground="red")

    # ========================================
    # ステップ7: 完了
    # ========================================
    def _show_complete(self):
        """完了画面を表示"""
        # アイコン/タイトル
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(pady=(20, 10))

        icon_label = ttk.Label(
            title_frame,
            text="🎉",
            font=("", 48)
        )
        icon_label.pack()

        title_label = ttk.Label(
            title_frame,
            text="セットアップ完了！",
            font=("", 18, "bold"),
            foreground="green"
        )
        title_label.pack(pady=(8, 0))

        # 説明
        desc_frame = ttk.Frame(self.content_frame)
        desc_frame.pack(fill=tk.X, padx=30, pady=10)

        desc_text = (
            "YouTube Playlist Managerを使用する準備が整いました。\n\n"
            "「アプリを開始」をクリックしてアプリケーションを起動してください。"
        )

        desc_label = ttk.Label(
            desc_frame,
            text=desc_text,
            font=("", 10),
            justify=tk.CENTER
        )
        desc_label.pack()

        # チェックリスト
        check_frame = ttk.LabelFrame(self.content_frame, text="設定状況", padding="10")
        check_frame.pack(fill=tk.X, padx=30, pady=10)

        # YouTube関連
        youtube_checks = [
            ("✓ Google Cloud Console設定", "green"),
            ("✓ 認証情報ファイル配置", "green"),
            ("✓ YouTubeアカウント連携", "green" if self.auth_success else "orange"),
            ("✓ API接続テスト", "green" if self.test_success else "orange"),
        ]

        for text, color in youtube_checks:
            ttk.Label(
                check_frame,
                text=text,
                font=("", 10),
                foreground=color
            ).pack(anchor=tk.W, pady=2)

        # セパレータ
        ttk.Separator(check_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # オプションサービス
        ttk.Label(
            check_frame,
            text="オプションサービス:",
            font=("", 10, "bold")
        ).pack(anchor=tk.W, pady=(5, 2))

        # ニコニコ動画
        niconico_text = "✓ ニコニコ動画" if self.niconico_configured else "- ニコニコ動画（未設定）"
        niconico_color = "green" if self.niconico_configured else "gray"
        ttk.Label(
            check_frame,
            text=niconico_text,
            font=("", 10),
            foreground=niconico_color
        ).pack(anchor=tk.W, pady=2)

        # ヒント
        hint_frame = ttk.Frame(self.content_frame)
        hint_frame.pack(fill=tk.X, padx=30, pady=10)

        ttk.Label(
            hint_frame,
            text="💡 ヒント: 「設定」メニューからいつでもセットアップウィザードを再実行できます",
            font=("", 9),
            foreground="gray"
        ).pack()

    # ========================================
    # ヘルプウィンドウ表示メソッド
    # ========================================
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
        dialog = tk.Toplevel(self.window)
        dialog.title(title)
        dialog.transient(self.window)
        dialog.grab_set()

        # サイズを設定
        dialog_width = 650
        dialog_height = 450

        # 中央に配置
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog_width // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog_height // 2)
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

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
            self.window.clipboard_clear()
            self.window.clipboard_append(content)
            messagebox.showinfo("コピー完了", "内容をクリップボードにコピーしました", parent=dialog)

        def copy_url():
            self._copy_to_clipboard(url)

        ttk.Button(btn_frame, text="内容をコピー", command=copy_content, width=15).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="公式サイトを開く", command=lambda: self._open_url_safely(url), width=15).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(btn_frame, text="📋 URLをコピー", command=copy_url, width=15).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(btn_frame, text="閉じる", command=dialog.destroy, width=10).pack(side=tk.RIGHT)

    def run(self):
        """ウィザードを実行"""
        self.window.mainloop()


def run_setup_wizard(parent: Optional[tk.Tk] = None, on_complete: Optional[Callable] = None) -> bool:
    """セットアップウィザードを実行

    Args:
        parent: 親ウィンドウ
        on_complete: 完了時のコールバック

    Returns:
        セットアップが完了した場合True
    """
    wizard = SetupWizard(parent, on_complete)
    if parent:
        parent.wait_window(wizard.window)
    else:
        wizard.run()
    return SetupStatus.is_setup_complete()


def check_and_run_setup(parent: Optional[tk.Tk] = None) -> bool:
    """セットアップが必要な場合にウィザードを実行

    Returns:
        セットアップが完了している場合True
    """
    if SetupStatus.needs_setup():
        return run_setup_wizard(parent)
    return True


# 直接実行時のテスト
if __name__ == "__main__":
    def on_complete(success):
        print(f"Setup complete: {success}")

    wizard = SetupWizard(on_complete=on_complete)
    wizard.run()
