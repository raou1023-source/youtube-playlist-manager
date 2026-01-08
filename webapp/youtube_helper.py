"""
YouTube API Helper for Streamlit
Streamlit用YouTube API連携モジュール (サービスアカウント認証対応)
"""

import os
import sys
from pathlib import Path
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

class YouTubeAPIHelper:
    """Streamlit用YouTube APIヘルパークラス (サービスアカウント認証)"""

    def __init__(self):
        self.youtube = None
        self.credentials = None

    def authenticate(self):
        """YouTube API認証 (サービスアカウント)"""
        try:
            # Streamlit Secretsからサービスアカウント情報を取得
            if "service_account" not in st.secrets:
                st.error("❌ Streamlit Secretsにサービスアカウント情報が設定されていません")
                st.info("""
                ### Streamlit Secrets の設定方法
                
                1. Streamlit Cloud の管理画面で、アプリの **Settings** を開く
                2. **Secrets** タブを選択
                3. サービスアカウントのJSON情報をTOML形式で貼り付け
                4. **Save changes** をクリック
                """)
                return False

            # サービスアカウント認証情報を構築
            credentials = service_account.Credentials.from_service_account_info(
                st.secrets["service_account"],
                scopes=SCOPES
            )

            self.credentials = credentials
            self.youtube = build('youtube', 'v3', credentials=credentials)
            
            st.success("✅ YouTube APIに接続しました")
            return True

        except Exception as e:
            st.error(f"❌ 認証エラー: {str(e)}")
            st.info("💡 Streamlit Secretsの設定を確認してください")
            return False

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
