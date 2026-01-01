# YouTube Playlist Manager

<div align="center">

![YouTube Playlist Manager](https://img.shields.io/badge/version-v1.0.1-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Languages](https://img.shields.io/badge/languages-7-orange)

**7言語対応 YouTubeプレイリスト自動生成ツール**

年代・カテゴリ・キーワード・地域を指定して、YouTubeプレイリストを自動生成

[📥 ダウンロード](https://github.com/raou1023-source/youtube-playlist-manager/releases/latest) | [📖 ドキュメント](#使い方) | [🐛 バグ報告](https://github.com/raou1023-source/youtube-playlist-manager/issues)

</div>

---

## 📸 スクリーンショット

### メイン画面
![メイン画面](screenshots/main-screen-ja.png)

### 多言語対応
![言語選択](screenshots/language-selection.png)

---

## ✨ 主な機能

### 🌍 完全多言語対応
7言語にリアルタイム対応。すべてのUI要素が完全翻訳済み。

- 🇯🇵 **日本語** (Japanese)
- 🇬🇧 **English** (英語)
- 🇨🇳 **简体中文** (簡体字中国語)
- 🇹🇼 **繁體中文** (繁体字中国語)
- 🇰🇷 **한국어** (韓国語)
- 🇪🇸 **Español** (スペイン語)
- 🇫🇷 **Français** (フランス語)
- 🇩🇪 **Deutsch** (ドイツ語)

### 🎵 豊富なカテゴリ対応

#### 音楽 (Music)
Rock、Pop、Jazz、Classical、Hip-Hop、EDM、R&B、Country、Metal、Reggae、Blues、Folk、Latin、K-Pop、J-Pop、Anime など **20+ジャンル**

#### 映画 (Movies)
Action、Comedy、Drama、Horror、Sci-Fi、Romance、Thriller、Animation、Documentary、Fantasy、Crime など **11ジャンル**

#### 教育 (Education)
Science、Technology、History、Language、Math、Art、Cooking、Programming、Business、Health、Tutorial、Lecture など **12分野**

#### ニュース (News)
Politics、World News、Economy、Sports、Tech News、Entertainment、Weather、Local News など **10カテゴリ**

### 🗺️ グローバル対応
**30以上の国・地域**に対応

🌏 アジア: Japan、Korea、China、Taiwan、Thailand、Vietnam、Philippines、Indonesia、Singapore、India  
🌎 北米: United States、Canada、Mexico  
🌍 ヨーロッパ: UK、France、Germany、Spain、Italy、Netherlands、Sweden、Norway、Denmark など  
🌏 その他: Australia、New Zealand、Brazil、Argentina、Middle East、Africa

### 📊 高度な機能

- ✅ **年代別検索** - 1950年代～2020年代
- ✅ **検索精度設定** - 標準/高精度/最高精度の3段階
- ✅ **公式チャンネル優先** - 認証済みチャンネルのみ抽出
- ✅ **動画数範囲指定** - スライダーで柔軟に設定
- ✅ **プレイリスト履歴管理** - 作成履歴の保存・管理
- ✅ **エクスポート機能** - CSV/JSON形式で出力
- ✅ **地域キーワード自動追加** - 選択した地域に応じた最適化

---

## 📦 ダウンロード

### 最新版

[![Download](https://img.shields.io/badge/Download-v1.0.1-blue?style=for-the-badge&logo=github)](https://github.com/raou1023-source/youtube-playlist-manager/releases/latest)

**ファイル名**: `YouTubePlaylistManager-v1.0-Windows.zip`

### システム要件

- **OS**: Windows 10/11 (64-bit)
- **メモリ**: 4GB RAM以上推奨
- **ストレージ**: 100MB以上の空き容量
- **インターネット**: 必須（YouTube API接続用）

---

## 🚀 インストール方法

### Step 1: ダウンロード

1. [最新リリース](https://github.com/raou1023-source/youtube-playlist-manager/releases/latest)にアクセス
2. `YouTubePlaylistManager-v1.0-Windows.zip` をダウンロード

### Step 2: 解凍

1. ダウンロードしたZIPファイルを右クリック
2. **"すべて展開"** を選択
3. 任意の場所に解凍

### Step 3: 実行

1. 解凍したフォルダ内の `YouTubePlaylistManager.exe` をダブルクリック
2. Windows Defender SmartScreenの警告が出た場合：
   - **"詳細情報"** をクリック
   - **"実行"** をクリック

---

## 🔑 YouTube API設定

初回起動時にYouTube API認証が必要です。

### Step 1: Google Cloud Projectの作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. **新しいプロジェクト**を作成
   - プロジェクト名: 任意（例: "YouTube Playlist Manager"）
3. プロジェクトを選択

### Step 2: YouTube Data API v3の有効化

1. 左側メニューから **"APIとサービス"** → **"ライブラリ"**
2. "YouTube Data API v3" を検索
3. **"有効にする"** をクリック

### Step 3: OAuth 2.0認証情報の作成

1. **"APIとサービス"** → **"認証情報"**
2. **"認証情報を作成"** → **"OAuth クライアント ID"**
3. **アプリケーションの種類**: **"デスクトップアプリ"**
4. **名前**: 任意（例: "YouTube Playlist Manager Desktop"）
5. **"作成"** をクリック

### Step 4: credentials.jsonのダウンロード

1. 作成した認証情報の右側にある **ダウンロードアイコン** をクリック
2. `credentials.json` という名前で保存
3. このファイルを `YouTubePlaylistManager.exe` と**同じフォルダ**に配置

### Step 5: 初回認証

1. `YouTubePlaylistManager.exe` を起動
2. ブラウザが自動的に開く
3. Googleアカウントでログイン
4. **"許可"** をクリック
5. "認証が完了しました" と表示されたらブラウザを閉じる

---

## 📖 使い方

### 基本的な使い方

#### 1. 言語を選択

メニューバー: **Settings** → **Language** → お好みの言語を選択

#### 2. プレイリスト条件を設定

- **年代**: 1950s～2020sから選択
- **カテゴリ**: Music/Movies/Education/Newsから選択
- **動画数**: スライダーで範囲を指定

#### 3. キーワード・地域を選択

- **キーワード**: カテゴリに応じたキーワードをチェック
- **地域**: 対象地域を選択
- **追加キーワード**: 任意のキーワードを入力

#### 4. 検索オプション（任意）

- **検索精度**: 標準/高精度/最高精度
- **公式チャンネル優先**: オン/オフ
- **プライバシー設定**: Public/Unlisted/Private

#### 5. プレイリスト作成

**"プレイリスト作成"** ボタンをクリック

→ 進行状況が表示され、完成したらURLが表示されます

### 履歴管理

- **更新**: 履歴を最新の状態に更新
- **削除**: 選択した履歴を削除
- **エクスポート**: CSV/JSON形式で保存
- **再作成**: 同じ条件で新しいプレイリストを作成

---

## ⚙️ 高度な設定

### 検索精度の違い

| 精度レベル | 説明 | 用途 |
|----------|------|------|
| **標準** | 適度な検索 + 公式チャンネル優先 | 一般的な使用 |
| **高精度** | 公式チャンネルのみ | 高品質な動画が必要な場合 |
| **最高精度** | チャンネルIDリストから直接検索 | 特定のチャンネルのみ |

### お気に入り機能

よく使う設定を保存できます：

1. **Favorites** → **Save Current Settings**
2. 設定名を入力して保存
3. **Favorites** → **Load Favorite** で呼び出し

---

## ❓ トラブルシューティング

### Q1: アプリが起動しない

**A**: Windows Defender SmartScreenが原因の可能性があります。

**解決方法**:
1. EXEファイルを右クリック
2. **"プロパティ"** を選択
3. **"全般"** タブの下部にある **"許可する"** にチェック
4. **"OK"** をクリック

### Q2: "credentials.json が見つかりません" エラー

**A**: YouTube API認証情報が正しく配置されていません。

**解決方法**:
1. `credentials.json` が `YouTubePlaylistManager.exe` と同じフォルダにあるか確認
2. ファイル名が正確に `credentials.json` か確認（大文字小文字に注意）

### Q3: "YouTube API エラー: quota exceeded"

**A**: YouTube API の1日あたりの割り当て制限（10,000クエリ）に達しました。

**解決方法**:
- 翌日まで待つ（太平洋時間の午前0時にリセット）
- Google Cloud Consoleで割り当てを増やす（有料）

### Q4: プレイリストが作成されない

**A**: 検索条件が厳しすぎる可能性があります。

**解決方法**:
1. 動画数の範囲を広げる
2. キーワードを減らす
3. 検索精度を「標準」に変更

### Q5: 言語が変更されない

**A**: キャッシュの問題の可能性があります。

**解決方法**:
1. アプリを完全に終了
2. `data` フォルダの `settings.json` を削除
3. アプリを再起動

---

## 🤝 貢献

プロジェクトへの貢献を歓迎します！

### バグ報告

[Issues](https://github.com/raou1023-source/youtube-playlist-manager/issues) で報告してください。

含めていただきたい情報：
- 使用環境（Windows バージョン）
- エラーメッセージ
- 再現手順

### 機能要望

[Discussions](https://github.com/raou1023-source/youtube-playlist-manager/discussions) でご提案ください。

---

## 📝 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

---

## 🙏 謝辞

- **YouTube Data API** - Google
- **Tkinter** - Python標準GUIライブラリ
- **PyInstaller** - Python実行ファイル作成
- すべての貢献者とユーザーの皆様

---

## 📞 お問い合わせ

- **Issues**: [GitHub Issues](https://github.com/raou1023-source/youtube-playlist-manager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/raou1023-source/youtube-playlist-manager/discussions)

---

## 🗺️ ロードマップ

### v1.x (現在)
- ✅ Windows実行ファイル版
- ✅ 7言語対応
- ✅ 基本的なプレイリスト生成機能

### v2.0 (計画中)
- 🔄 WEBアプリ版
- 🔄 ニコニコ動画対応
- 🔄 複数プラットフォーム統合

### 将来のアイデア
- 💡 AI自動カテゴリ分類
- 💡 プレイリスト分析機能
- 💡 コラボレーション機能

---

<div align="center">

**Developed with ❤️ by [raou1023-source](https://github.com/raou1023-source)**

⭐ このプロジェクトが役に立ったら、スターをつけていただけると嬉しいです！

</div>
