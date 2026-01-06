# Streamlit Cloud デプロイ チェックリスト

デプロイ前に以下の項目を確認してください。

## ✅ ファイル準備

- [ ] `requirements.txt` が存在する
- [ ] `.streamlit/config.toml` が存在する
- [ ] `.streamlit/secrets.toml.sample` が存在する（参考用）
- [ ] `DEPLOY.md` が存在する
- [ ] `.gitignore` に機密情報が含まれている
- [ ] `README.md` にデプロイ情報が記載されている

## ✅ コード確認

- [ ] `webapp/streamlit_app.py` が正常に動作する
- [ ] `webapp/youtube_helper.py` が存在する
- [ ] ローカルで `streamlit run webapp/streamlit_app.py` が成功する
- [ ] エラーハンドリングが適切に実装されている
- [ ] 日本語を含む全言語が正常に表示される

## ✅ 認証情報

- [ ] Google Cloud Platform プロジェクトが作成されている
- [ ] YouTube Data API v3 が有効化されている
- [ ] OAuth 2.0 クライアント ID が作成されている（ウェブアプリケーション）
- [ ] `credentials.json` がリポジトリに **含まれていない**
- [ ] `token.pickle` がリポジトリに **含まれていない**

## ✅ GitHub リポジトリ

- [ ] すべての変更がコミットされている
- [ ] リモートリポジトリにプッシュされている
- [ ] リポジトリが公開されている（または Streamlit Cloud から見える）
- [ ] README.md が適切に表示される
- [ ] ライセンスファイルが存在する

## ✅ Streamlit Cloud 設定

- [ ] Streamlit Cloud アカウントが作成されている
- [ ] GitHub アカウントと連携されている
- [ ] デプロイするリポジトリが選択できる

## 🚀 デプロイ手順

### 1. Streamlit Cloud でアプリを作成

```
Repository: raou1023-source/youtube-playlist-manager
Branch: main
Main file path: webapp/streamlit_app.py
```

### 2. Secrets を設定

Streamlit Cloud のアプリ設定 > Secrets タブで以下を設定：

```toml
[google_oauth]
client_id = "YOUR_CLIENT_ID.apps.googleusercontent.com"
project_id = "YOUR_PROJECT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uris = ["https://YOUR_APP_NAME.streamlit.app"]
```

### 3. Google Cloud Console でリダイレクト URI を更新

1. Google Cloud Console > APIs & Services > Credentials
2. OAuth 2.0 クライアント ID を選択
3. 承認済みのリダイレクト URI に追加：
   - `https://YOUR_APP_NAME.streamlit.app`
   - `https://YOUR_APP_NAME.streamlit.app/`

### 4. デプロイ実行

- "Deploy!" ボタンをクリック
- ログを確認してエラーがないことを確認

### 5. 動作確認

- [ ] アプリが正常に起動する
- [ ] Google 認証が成功する
- [ ] YouTube API 接続が確認できる
- [ ] プレイリスト作成が動作する
- [ ] 言語切り替えが動作する

## 🐛 トラブルシューティング

### デプロイが失敗する

- ログを確認
- requirements.txt の内容を確認
- Python バージョンを確認（3.8以上）

### 認証エラー

- Secrets の設定を確認
- Google Cloud Console のリダイレクト URI を確認
- OAuth 2.0 クライアントのタイプを確認（ウェブアプリケーション）

### API エラー

- YouTube Data API v3 が有効化されているか確認
- API クォータ制限を確認
- 認証情報が正しいか確認

## 📝 デプロイ後のタスク

- [ ] README.md にデプロイ済みアプリの URL を追加
- [ ] リリースノートを作成
- [ ] ユーザーガイドを更新
- [ ] バグ報告用の Issue テンプレートを作成
- [ ] 機能リクエスト用の Discussion を開始

---

すべてのチェック項目が完了したら、デプロイの準備が整っています！
