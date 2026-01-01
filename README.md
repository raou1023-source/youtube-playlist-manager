# YouTube Playlist Manager

**多言語対応 YouTubeプレイリスト自動生成ツール**

7言語完全対応（日本語、English、简体中文、繁體中文、한국어、Español、Français、Deutsch）

---

## 🌟 主な機能

### ✨ プレイリスト自動生成
- 年代・カテゴリ・キーワード・地域を指定して自動生成
- YouTube APIを使用した高度な検索
- 動画数の範囲指定が可能

### 🌍 多言語対応
- 7言語に完全対応
- リアルタイム言語切り替え
- すべてのUI要素が翻訳済み

### 🎵 豊富なカテゴリ
- **音楽**: Rock、Pop、Jazz、Classical、Hip-Hop、EDM、K-Pop、J-Pop など
- **映画**: Action、Comedy、Drama、Horror、Sci-Fi など
- **教育**: Science、Technology、History、Programming など
- **ニュース**: Politics、Economy、Sports など

### 🗺️ グローバル対応
- 30以上の国・地域に対応
- 地域キーワード自動追加機能

### 📊 履歴管理
- 作成したプレイリストの履歴保存
- CSV/JSONエクスポート機能
- 同じ条件での再作成機能

---

## 💾 ダウンロード

### Windows版

[最新リリースをダウンロード](https://github.com/YOUR_USERNAME/youtube-playlist-manager/releases/latest)

**システム要件:**
- Windows 10/11
- YouTube API認証情報（初回のみ）

---

## 🚀 使い方

### 初回起動時

1. `YouTubePlaylistManager.exe` をダブルクリック
2. セットアップウィザードが起動
3. YouTube API認証を完了

### プレイリスト作成

1. 言語を選択（Settings > Language）
2. 年代とカテゴリを選択
3. キーワード・地域を選択
4. 「プレイリスト作成」をクリック

### 言語切り替え

メニュー: **Settings > Language** から選択
- 🇯🇵 日本語
- 🇬🇧 English
- 🇨🇳 简体中文
- 🇹🇼 繁體中文
- 🇰🇷 한국어
- 🇪🇸 Español
- 🇫🇷 Français
- 🇩🇪 Deutsch

---

## 🔧 YouTube API設定

### 1. Google Cloud Consoleでプロジェクト作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成
3. YouTube Data API v3 を有効化
4. 認証情報を作成（OAuth 2.0 クライアント ID）
5. `credentials.json` をダウンロード

### 2. 認証情報の配置

`credentials.json` をアプリケーションと同じフォルダに配置

---

## 📂 ファイル構成

```
YouTubePlaylistManager/
├── YouTubePlaylistManager.exe  # メインアプリケーション
├── credentials.json            # YouTube API認証情報（要配置）
└── (その他の依存ファイル)
```

---

## ❓ トラブルシューティング

### Q: アプリが起動しない
A: Windows Defender SmartScreenが警告を出す場合があります。「詳細情報」→「実行」をクリックしてください。

### Q: YouTube APIエラーが出る
A: `credentials.json` が正しく配置されているか確認してください。

### Q: プレイリストが作成できない
A: YouTube API の割り当て制限を確認してください（1日あたり10,000クエリ）。

---

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

---

## 🤝 貢献

バグ報告や機能要望は [Issues](https://github.com/YOUR_USERNAME/youtube-playlist-manager/issues) までお願いします。

---

## 📧 お問い合わせ

質問やフィードバックは [Discussions](https://github.com/YOUR_USERNAME/youtube-playlist-manager/discussions) でお気軽にどうぞ。

---

## 🎉 更新履歴

### v1.0.0 (2025-12-30)
- 🎉 初回リリース
- ✅ 7言語完全対応
- ✅ プレイリスト自動生成機能
- ✅ 履歴管理機能
- ✅ Windows EXE版配布開始

---

**Developed with ❤️ by [YOUR_NAME]**
