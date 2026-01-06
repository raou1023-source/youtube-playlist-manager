"""
YouTube Playlist Manager - Streamlit Web Application (Full Version)
7言語対応 YouTubeプレイリスト自動生成ツール
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import time

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from youtube_helper import get_youtube_helper

# ページ設定
st.set_page_config(
    page_title="YouTube Playlist Manager",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF0000;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF0000;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #CC0000;
    }
</style>
""", unsafe_allow_html=True)

# 年代から日付範囲を取得
def get_date_range(era):
    """年代から検索用の日付範囲を取得"""
    if era == "すべて":
        return None, None
    
    era_map = {
        "1950s": ("1950-01-01T00:00:00Z", "1959-12-31T23:59:59Z"),
        "1960s": ("1960-01-01T00:00:00Z", "1969-12-31T23:59:59Z"),
        "1970s": ("1970-01-01T00:00:00Z", "1979-12-31T23:59:59Z"),
        "1980s": ("1980-01-01T00:00:00Z", "1989-12-31T23:59:59Z"),
        "1990s": ("1990-01-01T00:00:00Z", "1999-12-31T23:59:59Z"),
        "2000s": ("2000-01-01T00:00:00Z", "2009-12-31T23:59:59Z"),
        "2010s": ("2010-01-01T00:00:00Z", "2019-12-31T23:59:59Z"),
        "2020s": ("2020-01-01T00:00:00Z", "2029-12-31T23:59:59Z"),
    }
    
    return era_map.get(era, (None, None))

def create_playlist_with_progress(youtube_helper, settings):
    """プレイリストを作成（進行状況付き）"""
    
    # プレイリストタイトル生成
    title_parts = []
    if settings['era'] != "すべて":
        title_parts.append(settings['era'])
    title_parts.append(settings['category'])
    if settings['keywords']:
        title_parts.extend(settings['keywords'].split(',')[:2])
    
    playlist_title = " ".join(title_parts).strip()
    
    # プレイリスト作成
    st.info(f"📝 プレイリストを作成中: {playlist_title}")
    playlist_response = youtube_helper.create_playlist(
        title=playlist_title,
        description=f"Created by YouTube Playlist Manager\n{datetime.now().strftime('%Y-%m-%d')}",
        privacy_status="public"
    )
    
    if not playlist_response:
        return None
    
    playlist_id = playlist_response['id']
    st.success(f"✅ プレイリスト作成完了: {playlist_title}")
    
    # 検索クエリ生成
    query_parts = [settings['category']]
    if settings['keywords']:
        query_parts.extend([k.strip() for k in settings['keywords'].split(',')])
    search_query = " ".join(query_parts)
    
    # 日付範囲取得
    published_after, published_before = get_date_range(settings['era'])
    
    # 動画検索
    st.info(f"🔍 動画を検索中: {search_query}")
    region_code_map = {
        "Global": "US",
        "Japan": "JP",
        "United States": "US",
        "Korea": "KR",
        "China": "CN",
        "United Kingdom": "GB"
    }
    region_code = region_code_map.get(settings['region'], "US")
    
    videos = youtube_helper.search_videos(
        query=search_query,
        max_results=settings['video_count'],
        region_code=region_code,
        published_after=published_after,
        published_before=published_before
    )
    
    if not videos:
        st.warning("⚠️ 検索結果が見つかりませんでした")
        return None
    
    st.success(f"✅ {len(videos)}個の動画が見つかりました")
    
    # 動画をプレイリストに追加
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    added_count = 0
    for i, video in enumerate(videos):
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']
        
        status_text.text(f"📹 追加中 ({i+1}/{len(videos)}): {video_title[:50]}...")
        
        if youtube_helper.add_video_to_playlist(playlist_id, video_id):
            added_count += 1
        
        progress_bar.progress((i + 1) / len(videos))
        time.sleep(0.1)  # API制限対策
    
    status_text.empty()
    progress_bar.empty()
    
    return {
        'playlist_id': playlist_id,
        'title': playlist_title,
        'video_count': added_count,
        'url': youtube_helper.get_playlist_url(playlist_id)
    }

def main():
    # ヘッダー
    st.markdown('<div class="main-header">🎵 YouTube Playlist Manager</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">7言語対応 YouTubeプレイリスト自動生成ツール</div>', unsafe_allow_html=True)
    
    # サイドバー：言語選択
    st.sidebar.title("⚙️ Settings")
    language = st.sidebar.selectbox(
        "Language / 言語",
        options=[
            "🇯🇵 日本語",
            "🇬🇧 English",
            "🇨🇳 简体中文",
            "🇹🇼 繁體中文",
            "🇰🇷 한국어",
            "🇪🇸 Español",
            "🇫🇷 Français",
            "🇩🇪 Deutsch"
        ]
    )
    
    # YouTube API認証状態
    youtube_helper = get_youtube_helper()
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # メインコンテンツ
    tab1, tab2, tab3 = st.tabs(["🎵 プレイリスト作成", "📊 履歴", "ℹ️ About"])
    
    with tab1:
        st.header("プレイリスト作成")
        
        # 認証チェック
        if not st.session_state.authenticated:
            st.warning("⚠️ YouTube APIに接続していません")
            if st.button("🔐 YouTube APIに接続", use_container_width=True):
                with st.spinner("認証中..."):
                    if youtube_helper.authenticate():
                        st.session_state.authenticated = True
                        st.success("✅ 認証完了！")
                        st.rerun()
        else:
            st.success("✅ YouTube API接続済み")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("基本設定")
            
            # 年代選択
            era = st.selectbox(
                "年代",
                options=["すべて", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
            )
            
            # カテゴリ選択
            category = st.selectbox(
                "カテゴリ",
                options=["Music", "Movies", "Education", "News"]
            )
            
            # 動画数
            video_count = st.slider(
                "動画数",
                min_value=10,
                max_value=100,
                value=50,
                step=5
            )
        
        with col2:
            st.subheader("詳細設定")
            
            # 地域選択
            region = st.selectbox(
                "地域",
                options=["Global", "Japan", "United States", "Korea", "China", "United Kingdom"]
            )
            
            # 検索精度
            precision = st.select_slider(
                "検索精度",
                options=["標準", "高精度", "最高精度"],
                value="標準"
            )
            
            # 公式チャンネル優先
            official_only = st.checkbox("公式チャンネル優先", value=False)
        
        # キーワード入力
        st.subheader("キーワード")
        keywords = st.text_input(
            "追加キーワード（カンマ区切り）",
            placeholder="例: rock, jazz, classical"
        )
        
        # プレイリスト作成ボタン
        if st.button("🎵 プレイリスト作成", use_container_width=True, disabled=not st.session_state.authenticated):
            settings = {
                'era': era,
                'category': category,
                'video_count': video_count,
                'region': region,
                'precision': precision,
                'official_only': official_only,
                'keywords': keywords
            }
            
            with st.spinner("プレイリストを作成中..."):
                result = create_playlist_with_progress(youtube_helper, settings)
                
                if result:
                    st.balloons()
                    st.success(f"🎉 プレイリスト作成完了！")
                    
                    st.markdown(f"""
                    ### ✅ 作成されたプレイリスト
                    
                    **タイトル**: {result['title']}  
                    **動画数**: {result['video_count']}個  
                    **URL**: [{result['url']}]({result['url']})
                    """)
                    
                    # 履歴に保存
                    if 'history' not in st.session_state:
                        st.session_state.history = []
                    st.session_state.history.append({
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'title': result['title'],
                        'video_count': result['video_count'],
                        'url': result['url']
                    })
    
    with tab2:
        st.header("📊 プレイリスト履歴")
        
        if 'history' in st.session_state and st.session_state.history:
            for i, item in enumerate(reversed(st.session_state.history)):
                with st.expander(f"{i+1}. {item['title']} - {item['timestamp']}"):
                    st.write(f"**動画数**: {item['video_count']}個")
                    st.write(f"**URL**: [{item['url']}]({item['url']})")
        else:
            st.info("まだプレイリストが作成されていません")
    
    with tab3:
        st.header("ℹ️ About")
        
        st.markdown("""
        ### YouTube Playlist Manager
        
        **7言語対応 YouTubeプレイリスト自動生成ツール**
        
        #### 主な機能
        - 🌍 7言語完全対応
        - 🎵 年代・カテゴリ別プレイリスト自動生成
        - 🗺️ 30以上の国・地域対応
        - 📊 履歴管理機能
        
        #### バージョン
        - Web版: v1.0.0
        - Desktop版: [v1.0.1](https://github.com/raou1023-source/youtube-playlist-manager/releases)
        
        #### リンク
        - [GitHub Repository](https://github.com/raou1023-source/youtube-playlist-manager)
        
        ---
        
        Developed with ❤️ by [raou1023-source](https://github.com/raou1023-source)
        """)

    # フッター
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📌 Quick Links")
    st.sidebar.markdown("- [Desktop版ダウンロード](https://github.com/raou1023-source/youtube-playlist-manager/releases)")
    st.sidebar.markdown("- [ドキュメント](https://github.com/raou1023-source/youtube-playlist-manager)")
    st.sidebar.markdown("- [バグ報告](https://github.com/raou1023-source/youtube-playlist-manager/issues)")

if __name__ == "__main__":
    main()
