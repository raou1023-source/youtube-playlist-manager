# 🎉 Streamlit Cloud デプロイ準備完了！

## ✅ 作成したファイル

### 1. **requirements.txt**
Streamlit Cloud で必要な Python パッケージを定義
- streamlit
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client

### 2. **.streamlit/config.toml**
Streamlit アプリの設定ファイル
- テーマ設定（YouTube風のダークテーマ）
- サーバー設定
- ブラウザ設定

### 3. **.streamlit/secrets.toml.sample**
Secrets 管理のサンプルファイル
- Google OAuth 2.0 認証情報の形式を示す
- デプロイ時の参考用

### 4. **DEPLOY.md**
詳細なデプロイガイド
- 前提条件
- ステップバイステップの手順
- トラブルシューティング
- セキュリティに関する注意事項

### 5. **DEPLOY_CHECKLIST.md**
デプロイ前のチェックリスト
- ファイル準備の確認項目
- コード確認の確認項目
- 認証情報の確認項目
- デプロイ後のタスク

### 6. **README_DEPLOY_SECTION.md**
README.md に追加するセクション
- Web版とデスクトップ版の説明
- 機能比較表
- 技術スタック
- サポート情報

### 7. **.gitignore.streamlit**
Streamlit 用の .gitignore 追加項目
- 既存の .gitignore にマージして使用

## 🚀 次のステップ

### Phase 4: Streamlit Cloud へのデプロイ

#### 1. ローカルで最終確認
```bash
cd C:\Users\raou_\Desktop\youtube-playlist-manager
streamlit run webapp/streamlit_app.py
```

#### 2. GitHub にプッシュ
```bash
# 新しいファイルを追加
git add requirements.txt
git add .streamlit/
git add DEPLOY.md
git add DEPLOY_CHECKLIST.md
git add README_DEPLOY_SECTION.md

# コミット
git commit -m "Add Streamlit Cloud deployment configuration"

# プッシュ
git push origin main
```

#### 3. Streamlit Cloud でデプロイ

1. https://streamlit.io/cloud にアクセス
2. "Sign up" または "Log in" で GitHub アカウントと連携
3. "New app" をクリック
4. 以下を設定：
   - Repository: `raou1023-source/youtube-playlist-manager`
   - Branch: `main`
   - Main file path: `webapp/streamlit_app.py`
5. "Deploy!" をクリック

#### 4. Secrets を設定

デプロイ後、アプリの設定画面で：
1. "Secrets" タブを開く
2. `credentials.json` の内容を以下の形式で貼り付け：

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

3. "Save" をクリック

#### 5. Google Cloud Console を更新

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. プロジェクトを選択
3. "APIs & Services" > "Credentials"
4. OAuth 2.0 クライアント ID を選択
5. "承認済みのリダイレクト URI" に追加：
   - `https://YOUR_APP_NAME.streamlit.app`
   - `https://YOUR_APP_NAME.streamlit.app/`
6. "保存"

#### 6. 動作確認

- デプロイされたアプリにアクセス
- Google アカウントで認証
- プレイリスト作成をテスト

## 📋 重要な注意事項

### セキュリティ
- **絶対に** `credentials.json` や `token.pickle` をリポジトリにコミットしないでください
- Streamlit Cloud の Secrets 機能を必ず使用してください
- `.gitignore` に機密情報が含まれていることを確認してください

### OAuth リダイレクト URI
デプロイ後、必ず以下の2つの URI を Google Cloud Console に追加してください：
1. `https://YOUR_APP_NAME.streamlit.app`
2. `https://YOUR_APP_NAME.streamlit.app/` （末尾のスラッシュ付き）

### API クォータ
- YouTube Data API v3 には1日あたりのクォータ制限があります
- 大量のユーザーが使用する場合は、クォータの増加をリクエストする必要があります

## 🎯 完了予定タスク

- [x] requirements.txt 作成
- [x] .streamlit/config.toml 作成
- [x] secrets.toml.sample 作成
- [x] DEPLOY.md 作成
- [x] DEPLOY_CHECKLIST.md 作成
- [x] README 追加セクション作成
- [x] .gitignore 更新項目作成
- [ ] GitHub へプッシュ
- [ ] Streamlit Cloud でデプロイ
- [ ] Secrets 設定
- [ ] Google Cloud Console 更新
- [ ] 動作確認
- [ ] README.md を更新してデプロイ URL を追加

## 💡 おすすめの改善案

デプロイ後に検討できる機能：
1. ユーザー統計ダッシュボード
2. プレイリスト履歴の保存
3. お気に入り設定の保存
4. ソーシャルシェア機能
5. プレミアム機能（より多くの動画数など）

---

準備完了です！次は GitHub へプッシュしてデプロイしましょう！🚀
