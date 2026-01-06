"""
YouTube Playlist Manager - Streamlit Web Application
7言語対応 YouTubeプレイリスト自動生成ツール
"""

import streamlit as st
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

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
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
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
    
    # メインコンテンツ
    tab1, tab2, tab3 = st.tabs(["🎵 プレイリスト作成", "📊 履歴", "ℹ️ About"])
    
    with tab1:
        st.header("プレイリスト作成")
        
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
        if st.button("🎵 プレイリスト作成", use_container_width=True):
            with st.spinner("プレイリストを作成中..."):
                # TODO: 実際のプレイリスト作成処理を実装
                st.success("✅ プレイリストが作成されました！")
                st.info("🔗 プレイリストURL: https://youtube.com/playlist?list=...")
    
    with tab2:
        st.header("📊 プレイリスト履歴")
        st.info("履歴機能は開発中です")
        
        # ダミーデータ
        if st.button("履歴を表示"):
            st.write("最近作成されたプレイリスト:")
            st.write("1. 2020s Rock Music - 50 videos")
            st.write("2. Japanese Pop 1990s - 30 videos")
            st.write("3. Classical Music Masterpieces - 40 videos")
    
    with tab3:
        st.header("ℹ️ About")
        
        st.markdown("""
        ### YouTube Playlist Manager
        
        **7言語対応 YouTubeプレイリスト自動生成ツール**
        
        #### 主な機能
        - 🌍 7言語完全対応（日本語、English、简体中文、繁體中文、한국어、Español、Français、Deutsch）
        - 🎵 年代・カテゴリ別プレイリスト自動生成
        - 🗺️ 30以上の国・地域対応
        - 📊 履歴管理機能
        - 🔍 高度な検索オプション
        
        #### バージョン
        - Web版: v1.0.0
        - Desktop版: [v1.0.1](https://github.com/raou1023-source/youtube-playlist-manager/releases)
        
        #### リンク
        - [GitHub Repository](https://github.com/raou1023-source/youtube-playlist-manager)
        - [Issues](https://github.com/raou1023-source/youtube-playlist-manager/issues)
        - [Discussions](https://github.com/raou1023-source/youtube-playlist-manager/discussions)
        
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
