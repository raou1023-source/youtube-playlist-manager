# Streamlit Cloud デプロイガイド

このガイドでは、YouTube Playlist Manager を Streamlit Cloud にデプロイする手順を説明します。

## 前提条件

- GitHubアカウント
- Google Cloud Platform アカウント
- YouTube Data API v3 が有効化されたプロジェト

## デプロイ手順

### 1. Streamlit Cloud アカウントの作成

1. https://streamlit.io/cloud にアクセス
2. "Sign up" をクリック
3. GitHubアカウントで認証

### 2. アプリのデプロイ

1. Streamlit Cloud ダッシュボードで "New app" をクリック
2. リポジトリを選択: `raou1023-source/youtube-playlist-manager`
3. ブランチ: `main`
4. メインファイルパス: `webapp/streamlit_app.py`
5. "Deploy!" をクリック

### 3. Secrets の設定

デプロイ後、以下の手順でシークレットを設定します：

1. アプリの設定画面で "Secrets" タブを開く
2. `.streamlit/secrets.toml.sample` の内容を参考に、以下の形式で設定：

```toml
[google_oauth]
client_id = "あなたのクライアントID.apps.googleusercontent.com"
project_id = "あなたのプロジェクトID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_secret = "あなたのクライアントシークレット"
redirect_uris = ["https://あなたのアプリ名.streamlit.app"]
```

3. "Save" をクリック

### 4. Google Cloud Console での設定

デプロイ後、OAuth 2.0 のリダイレクト URI を更新する必要があります：

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. プロジェクトを選択
3. "APIs & Services" > "Credentials" に移動
4. OAuth 2.0 クライアント ID をクリック
5. "承認済みのリダイレクト URI" に以下を追加：
   - `https://あなたのアプリ名.streamlit.app`
   - `https://あなたのアプリ名.streamlit.app/`
6. "保存" をクリック

### 5. アプリの確認

1. デプロイが完了したら、提供された URL にアクセス
2. Google アカウントで認証
3. プレイリスト作成機能をテスト

## トラブルシューティング

### 認証エラーが発生する場合

- Google Cloud Console でリダイレクト URI が正しく設定されているか確認
- Streamlit Cloud の Secrets が正しく設定されているか確認
- OAuth 2.0 クライアント ID のタイプが "ウェブアプリケーション" になっているか確認

### アプリが起動しない場合

- ログを確認（Streamlit Cloud のダッシュボードから）
- requirements.txt に記載されているパッケージがすべてインストールされているか確認
- Python のバージョンが互換性があるか確認（Python 3.8以上推奨）

### API クォータエラーが発生する場合

- YouTube Data API v3 のクォータ制限を確認
- Google Cloud Console で API の使用状況を確認
- 必要に応じてクォータの増加をリクエスト

## セキュリティに関する注意事項

1. **絶対に** credentials.json や token.pickle をリポジトリにコミットしないでください
2. `.gitignore` に以下が含まれていることを確認してください：
   ```
   credentials/
   *.pickle
   .streamlit/secrets.toml
   ```
3. Streamlit Cloud の Secrets 機能を使用して機密情報を管理してください

## サポート

問題が発生した場合は、以下のリソースを参照してください：

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)

または、GitHubリポジトリで Issue を作成してください。
