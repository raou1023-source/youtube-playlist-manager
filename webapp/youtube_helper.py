"""
YouTube API Helper for Streamlit
Streamlit用YouTube API連携モジュール
"""

import os
import sys
from pathlib import Path
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

class YouTubeAPIHelper:
    """Streamlit用YouTube APIヘルパークラス"""
    
    def __init__(self):
        self.youtube = None
        self.credentials = None
        
    def authenticate(self):
        """YouTube API認証"""
        creds = None
        token_path = project_root / "credentials" / "token.pickle"
        credentials_path = project_root / "credentials" / "credentials.json"
        
        # トークンが存在する場合は読み込む
        if token_path.exists():
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # 認証情報が無効または存在しない場合
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not credentials_path.exists():
                    st.error("❌ credentials.json が見つかりません")
                    st.info("""
                    ### 認証情報の設定手順
                    
                    1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
                    2. プロジェクトを作成
                    3. YouTube Data API v3 を有効化
                    4. OAuth 2.0 認証情報を作成（デスクトップアプリ）
                    5. `credentials.json` をダウンロード
                    6. プロジェクトの `credentials` フォルダに配置
                    """)
                    return False
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(credentials_path), SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    st.error(f"❌ 認証エラー: {str(e)}")
                    return False
            
            # トークンを保存
            token_path.parent.mkdir(exist_ok=True)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
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
