# README.mdに追加するセクション

## 🌐 Web版（Streamlit Cloud）

### オンラインで使用

Web版を使用するには：
1. [こちら](https://あなたのアプリ名.streamlit.app) にアクセス
2. Googleアカウントで認証
3. すぐに使い始められます！

### 自分でデプロイする

詳細な手順は [DEPLOY.md](DEPLOY.md) を参照してください。

簡易手順：
1. このリポジトリをフォーク
2. [Streamlit Cloud](https://streamlit.io/cloud) でアカウント作成
3. リポジトリを接続してデプロイ
4. Secrets を設定
5. Google Cloud Console でリダイレクト URI を更新

## 🖥️ デスクトップ版

従来のデスクトップアプリケーションも引き続き利用可能です。

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/raou1023-source/youtube-playlist-manager.git
cd youtube-playlist-manager

# 依存関係をインストール
pip install -r requirements.txt

# デスクトップ版を起動
python src/main.py
```

### Web版をローカルで実行

```bash
# Streamlit版を起動
streamlit run webapp/streamlit_app.py
```

## 📊 機能比較

| 機能 | デスクトップ版 | Web版 |
|------|--------------|-------|
| プレイリスト作成 | ✅ | ✅ |
| 年代・カテゴリフィルタ | ✅ | ✅ |
| 地域選択 | ✅ | ✅ |
| 多言語対応（8言語） | ✅ | ✅ |
| インストール不要 | ❌ | ✅ |
| オフライン使用 | ✅ | ❌ |
| 自動更新 | ✅ | N/A |

## 🔐 セキュリティ

- OAuth 2.0による安全な認証
- 認証情報は暗号化して保存
- YouTube APIの公式ライブラリを使用
- HTTPS通信でデータを保護

## 🛠️ 技術スタック

### デスクトップ版
- Python 3.8+
- Tkinter (GUI)
- Google API Client
- Auto-update機能

### Web版
- Streamlit
- Google API Client
- OAuth 2.0認証
- クラウドホスティング

## 📝 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照してください。

## 🤝 コントリビューション

プルリクエストを歓迎します！詳細は [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

## 📞 サポート

- バグ報告: [Issues](https://github.com/raou1023-source/youtube-playlist-manager/issues)
- 機能リクエスト: [Discussions](https://github.com/raou1023-source/youtube-playlist-manager/discussions)
- ドキュメント: [Wiki](https://github.com/raou1023-source/youtube-playlist-manager/wiki)

---

⭐ このプロジェクトが役に立ったら、スターをつけてください！
