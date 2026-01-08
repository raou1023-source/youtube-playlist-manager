"""
YouTube API Helper for Streamlit
Streamlit用YouTube API連携モジュール (Streamlit Secrets対応版)
"""

import os
import sys
import json
import tempfile
from pathlib import Path
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

class YouTubeAPIHelper:
    """Streamlit用YouTube APIヘルパークラス (Streamlit Secrets対応)"""

    def __init__(self):
        self.youtube = None
        self.credentials = None

    def get_credentials_from_secrets(self):
        """Streamlit Secretsから認証情報を取得"""
        try:
            # Streamlit Secretsから認証情報を取得
            if "google_oauth" not in st.secrets:
                st.error("❌ Streamlit Secretsに認証情報が設定されていません")
                st.info("""
                ### Streamlit Secrets の設定方法
                
                1. Streamlit Cloud の管理画面で、アプリの **Settings** を開く
                2. **Secrets** タブを選択
                3. 以下の形式で認証情報を貼り付け:
                
                ```toml
                [google_oauth]
                client_id = "your-client-id.apps.googleusercontent.com"
                project_id = "your-project-id"
                auth_uri = "https://accounts.google.com/o/oauth2/auth"
                token_uri = "https://oauth2.googleapis.com/token"
                auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
                client_secret = "your-client-secret"
                redirect_uris = ["https://your-app-url.streamlit.app"]
                ```
                
                4. **Save changes** をクリック
                """)
                return None

            # Secrets から認証情報を構築
            oauth_config = {
                "installed": {
                    "client_id": st.secrets["google_oauth"]["client_id"],
                    "project_id": st.secrets["google_oauth"]["project_id"],
                    "auth_uri": st.secrets["google_oauth"]["auth_uri"],
                    "token_uri": st.secrets["google_oauth"]["token_uri"],
                    "auth_provider_x509_cert_url": st.secrets["google_oauth"]["auth_provider_x509_cert_url"],
                    "client_secret": st.secrets["google_oauth"]["client_secret"],
                    "redirect_uris": st.secrets["google_oauth"]["redirect_uris"]
                }
            }
            
            return oauth_config

        except Exception as e:
            st.error(f"❌ Secrets読み込みエラー: {str(e)}")
            return None

    def authenticate(self):
        """YouTube API認証 (Streamlit Secrets対応)"""
        creds = None
        
        # セッションステートにトークンがあれば使用
        if "youtube_token" in st.session_state:
            try:
                creds = pickle.loads(st.session_state["youtube_token"])
            except:
                pass

        # 認証情報が無効または存在しない場合
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except:
                    creds = None

            if not creds:
                # Streamlit Secretsから認証情報を取得
                oauth_config = self.get_credentials_from_secrets()
                if not oauth_config:
                    return False

                try:
                    # 一時ファイルに認証情報を書き込み
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                        json.dump(oauth_config, f)
                        temp_credentials_path = f.name

                    # OAuth フローを実行
                    flow = Flow.from_client_secrets_file(
                        temp_credentials_path,
                        scopes=SCOPES,
                        redirect_uri=oauth_config["installed"]["redirect_uris"][0]
                    )

                    # 認証URLを生成
                    auth_url, _ = flow.authorization_url(prompt='consent')

                    st.info("🔐 YouTube APIに接続するには、以下のリンクをクリックしてGoogleアカウントで認証してください:")
                    st.markdown(f"[Google認証ページを開く]({auth_url})")
                    
                    # 認証コード入力欄
                    auth_code = st.text_input(
                        "認証後に表示されるコードを入力してください:",
                        type="password",
                        key="auth_code_input"
                    )

                    if auth_code:
                        try:
                            flow.fetch_token(code=auth_code)
                            creds = flow.credentials
                            
                            # セッションステートに保存
                            st.session_state["youtube_token"] = pickle.dumps(creds)
                            st.success("✅ 認証に成功しました！")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ 認証エラー: {str(e)}")
                            return False
                    else:
                        return False

                    # 一時ファイルを削除
                    os.unlink(temp_credentials_path)

                except Exception as e:
                    st.error(f"❌ 認証エラー: {str(e)}")
                    return False

            # トークンをセッションステートに保存
            if creds:
                st.session_state["youtube_token"] = pickle.dumps(creds)

        self.credentials = creds
        self.youtube = build('youtube', 'v3', credentials=creds)
        return True

    def search_videos(self, query, max_results=50, region_code="JP",
                     published_after=None, published_before=None):
        """動画を検索"""
        try:
            search_params = {
                'part': 'snippet',
                'q': query,
                'maxResults': min(max_results, 50),
                'type': 'video',
                'regionCode': region_code,
                'relevanceLanguage': region_code.lower()
            }

            if published_after:
                search_params['publishedAfter'] = published_after
            if published_before:
                search_params['publishedBefore'] = published_before

            request = self.youtube.search().list(**search_params)
            response = request.execute()

            return response.get('items', [])
        except Exception as e:
            st.error(f"❌ 検索エラー: {str(e)}")
            return []

    def create_playlist(self, title, description="", privacy_status="public"):
        """プレイリストを作成"""
        try:
            request = self.youtube.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description
                    },
                    "status": {
                        "privacyStatus": privacy_status
                    }
                }
            )
            response = request.execute()
            return response
        except Exception as e:
            st.error(f"❌ プレイリスト作成エラー: {str(e)}")
            return None

    def add_video_to_playlist(self, playlist_id, video_id):
        """プレイリストに動画を追加"""
        try:
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            response = request.execute()
            return True
        except Exception as e:
            st.warning(f"⚠️ 動画追加エラー: {str(e)}")
            return False

    def get_playlist_url(self, playlist_id):
        """プレイリストURLを取得"""
        return f"https://www.youtube.com/playlist?list={playlist_id}"

# グローバルインスタンス
@st.cache_resource
def get_youtube_helper():
    """YouTubeヘルパーのシングルトンインスタンスを取得"""
    return YouTubeAPIHelper()
