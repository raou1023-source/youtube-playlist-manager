# -*- coding: utf-8 -*-
"""
Multi-language translation system for YouTube Playlist Manager - PERFECT VERSION
Supports: Japanese, English, Chinese (Simplified & Traditional), Korean, Spanish, French, German

修正内容:
- 全7言語に region_worldwide を追加
- region_selected の統一確認済み
- 全キーワード（keyword_hip-hop, keyword_sci-fi等）の統一確認済み
- 言語管理機能を追加（set_language, get_current_language, t, t_keyword, t_region）
"""

# Translation dictionaries
TRANSLATIONS = {
    'ja': {
        # Menu bar
        'menu_file': 'ファイル',
        'menu_favorites': 'お気に入り',
        'menu_settings': '設定',
        'menu_help': 'ヘルプ',
        'menu_export': 'エクスポート',
        'export_csv': 'CSV形式',
        'export_json': 'JSON形式',
        'export_txt': 'TXT形式',
        'backup_create': 'バックアップを作成',
        'backup_restore': 'バックアップから復元',
        'backup_manage': 'バックアップ管理',
        'menu_exit': '終了',
        'favorites_save': '現在の設定を保存',
        'favorites_load': 'お気に入りを読み込み',
        'favorites_manage': 'お気に入り管理',
        'menu_language': '言語',
        'update_check': '更新を確認',
        'about': 'バージョン情報',
        
        # Main UI labels
        'label_era': '年代:',
        'label_category': 'カテゴリ:',
        'label_video_count': '動画数:',
        
        # Sections
        'section_basic': '基本設定',
        'section_keywords': 'キーワード・地域',
        'section_search_options': '検索オプション',
        'section_official_channel': '公式チャンネル優先設定:',
        'section_privacy': 'プライバシー設定',
        'section_platform': 'プラットフォーム',
        'section_progress': '進行状況',
        
        # Tab names
        'tab_music': '音楽',
        'tab_movies': '映画',
        'tab_education': '教育',
        'tab_news': 'ニュース',
        'tab_region': '地域',
        'tab_history': '履歴',
        'tab_integrated_viewer': '統合プレイリストビューワー',
        'tab_playlist': '動画再生リスト',
        
        # Music keywords
        'keyword_rock': 'ロック',
        'keyword_pop': 'ポップ',
        'keyword_jazz': 'ジャズ',
        'keyword_classical': 'クラシック',
        'keyword_hip-hop': 'ヒップホップ',
        'keyword_edm': 'EDM',
        'keyword_metal': 'メタル',
        'keyword_country': 'カントリー',
        'keyword_reggae': 'レゲエ',
        'keyword_electronic': 'エレクトロニック',
        'keyword_blues': 'ブルース',
        
        # Movie keywords
        'keyword_action': 'アクション',
        'keyword_comedy': 'コメディ',
        'keyword_drama': 'ドラマ',
        'keyword_horror': 'ホラー',
        'keyword_sci-fi': 'SF',
        'keyword_romance': 'ロマンス',
        'keyword_thriller': 'スリラー',
        'keyword_animation': 'アニメーション',
        'keyword_documentary': 'ドキュメンタリー',
        'keyword_fantasy': 'ファンタジー',
        'keyword_crime': '犯罪',
        
        # Education keywords
        'keyword_science': '科学',
        'keyword_technology': '技術',
        'keyword_history': '歴史',
        'keyword_language': '語学',
        'keyword_math': '数学',
        'keyword_art': '芸術',
        'keyword_cooking': '料理',
        'keyword_programming': 'プログラミング',
        'keyword_business': 'ビジネス',
        'keyword_health': '健康',
        'keyword_tutorial': 'チュートリアル',
        'keyword_lecture': '講義',
        
        # News keywords
        'keyword_politics': '政治',
        'keyword_world_news': '国際ニュース',
        'keyword_economy': '経済',
        'keyword_sports': 'スポーツ',
        'keyword_tech_news': 'IT・技術',
        'keyword_entertainment_news': '芸能',
        'keyword_weather': '天気',
        'keyword_local_news': '地域ニュース',
        'keyword_sports_news': 'スポーツニュース',
        'keyword_technology_news': 'テクノロジーニュース',
        
        # Search precision
        'search_precision_label': '検索精度:',
        'precision_standard': '標準（デフォルト）',
        'precision_standard_desc': '適度な検索＋公式チャンネル優先',
        'precision_high': '高精度',
        'precision_high_desc': '仅官方频道',
        'precision_highest': '最高精度',
        'precision_highest_desc': 'チャンネルIDリストから直接検索',
        
        # Official channel options
        'option_official_channel': '公式チャンネル優先',
        'option_verified_badge': '認証済みバッジ必須',
        'option_subscriber_100k': 'チャンネル登録者数: 100万人以上',
        'option_video_views_100k': '再生回数: 100万回以上',
        'option_vevo_only': 'VEVO/公式のみ',
        'option_add_detailed_to_desc': '詳細な説明を追加',
        
        # Privacy settings
        'privacy_private': '非公開（自分のみ閲覧可能）',
        'privacy_unlisted': '限定公開（URLを知っている人のみ閲覧可能）',
        'privacy_public': '公開（誰でも検索・閲覧可能）',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'ニコニコ動画',
        
        # Progress
        'progress_waiting': '待機中...',
        'status_waiting': '待機中...',
        
        # Region selection
        'region_selected': '選択中:',
        'region_none': 'なし',
        'region_worldwide': '全世界',
        
        # Regions
        'region_japan': '日本',
        'region_korea': '韓国',
        'region_china': '中国',
        'region_taiwan': '台湾',
        'region_usa': 'アメリカ',
        'region_uk': 'イギリス',
        'region_france': 'フランス',
        'region_germany': 'ドイツ',
        'region_spain': 'スペイン',
        'region_italy': 'イタリア',
        'region_canada': 'カナダ',
        'region_australia': 'オーストラリア',
        'region_brazil': 'ブラジル',
        'region_mexico': 'メキシコ',
        'region_india': 'インド',
        'region_thailand': 'タイ',
        'region_vietnam': 'ベトナム',
        'region_philippines': 'フィリピン',
        'region_indonesia': 'インドネシア',
        'region_singapore': 'シンガポール',
        'region_russia': 'ロシア',
        'region_poland': 'ポーランド',
        'region_netherlands': 'オランダ',
        'region_sweden': 'スウェーデン',
        'region_norway': 'ノルウェー',
        'region_denmark': 'デンマーク',
        'region_argentina': 'アルゼンチン',
        'region_africa': 'アフリカ',
        'region_middle_east': '中東',
        'region_new_zealand': 'ニュージーランド',
        
        # Buttons
        'button_create_playlist': 'プレイリスト作成',
        'button_refresh': '更新',
        'button_delete': '削除',
        'button_cancel': 'キャンセル',
        'button_export': 'エクスポート',
        'button_import': 'インポート',
        'button_open_url': 'URLを開く',
        'button_recreate_sampler': 'サンプラーを再作成',
        'button_video_info': '動画情報',
        'button_delete_history': '履歴削除',
        'button_csv_export': 'CSV出力',
        
        # Labels
        'label_playlist_url': 'プレイリストURL:',
        'label_created_date': '作成日時',
        'label_title': 'タイトル',
        'label_video_count': '動画数',
        'label_platform': 'プラットフォーム',
        'label_category_short': 'カテゴリ',
        'label_era_short': '年代',
        'label_total': '合計',
        
        # Section headers
        'section_preset': 'プリセット',
        'section_result': '結果',
        'section_history': '履歴',
        'section_integrated_playlists': '統合プレイリストビューワー',
        
        # Additional options
        'option_add_region_keywords': '地域キーワードを追加',
        'option_add_detailed_desc': '詳細な説明を追加',
        
        # Additional keyword
        'label_additional_keyword': '追加キーワード',
        'additional_keyword': '追加キーワード',
        'selected_keywords': '選択されたキーワード',
        'region_keyword_auto': '地域キーワードを自動追加',
        
        # Buttons
        'btn_create_playlist': 'プレイリスト作成',
        'btn_cancel': 'キャンセル',
        'btn_save': '保存',
        'btn_copy_url': 'URLをコピー',
        'btn_open': '開く',
        'btn_refresh': '更新',
        'btn_delete': '削除',
        'btn_delete_all': 'すべて削除',
        'btn_export': 'エクスポート',
        'btn_import': 'インポート',
        'btn_recreate_same': '同じ条件で再作成',
        'btn_open_url': 'URLを開く',
        'btn_video_confirm': '動画確認',
        'btn_delete_history': '履歴削除',
        'btn_csv_export': 'CSV出力',
        'btn_create_new': '新規作成',
        'btn_json_export': 'JSON出力',
        'btn_html_export': 'HTML出力',
        'btn_edit': '編集',
        
        # Column headers
        'col_created_date': '作成日時',
        'col_title': 'タイトル',
        'col_video_count': '動画数',
        'col_platform': 'プラットフォーム',
        'col_category': 'カテゴリ',
        'col_era': '年代',
        'col_total': '合計',
        'col_youtube': 'YouTube',
        'col_niconico': 'ニコニコ動画',
        
        # Labels
        'label_video_range': '動画数範囲',
        
        # Section headers (additional)
        'section_integrated_viewer': '統合プレイリストビューワー',
        
        # Privacy descriptions
        'privacy_private_desc': '自分のみ閲覧可能',
        'privacy_unlisted_desc': '自分のみ閲覧可能',
        'privacy_public_desc': '誰でも検索・閲覧可能',
        
        # Messages
        'message_success': '成功',
        'message_error': 'エラー',
        'message_creating': '作成中...',
        'message_searching': '検索中...',
        
        # Setup and Auth
        'setup_wizard': 'セットアップウィザード',
        'youtube_auth': 'YouTube認証',
        'niconico_auth': 'ニコニコ動画認証',
        'check_auth_status': '認証状態確認',
        
        # Help
        'youtube_api_help': 'YouTube API ヘルプ',
        'niconico_help': 'ニコニコ動画ヘルプ',
        'usage_guide': '使い方ガイド',
        'troubleshooting': 'トラブルシューティング',
    },
    
    'en': {
        # Menu bar
        'menu_file': 'File',
        'menu_favorites': 'Favorites',
        'menu_settings': 'Settings',
        'menu_help': 'Help',
        'menu_export': 'Export',
        'export_csv': 'CSV Format',
        'export_json': 'JSON Format',
        'export_txt': 'TXT Format',
        'backup_create': 'Create Backup',
        'backup_restore': 'Restore from Backup',
        'backup_manage': 'Manage Backups',
        'menu_exit': 'Exit',
        'favorites_save': 'Save Current Settings',
        'favorites_load': 'Load Favorites',
        'favorites_manage': 'Manage Favorites',
        'menu_language': 'Language',
        'update_check': 'Check for Updates',
        'about': 'About',
        
        # Main UI labels
        'label_era': 'Era:',
        'label_category': 'Category:',
        'label_video_count': 'Video Count:',
        
        # Sections
        'section_basic': 'Basic Settings',
        'section_keywords': 'Keywords and Region',
        'section_search_options': 'Search Options',
        'section_official_channel': 'Official Channel Priority:',
        'section_privacy': 'Privacy Settings',
        'section_platform': 'Platform',
        'section_progress': 'Progress',
        
        # Tab names
        'tab_music': 'Music',
        'tab_movies': 'Movies',
        'tab_education': 'Education',
        'tab_news': 'News',
        'tab_region': 'Region',
        'tab_history': 'History',
        'tab_integrated_viewer': 'Integrated Playlist Viewer',
        'tab_playlist': 'Playlist URL',
        
        # Music keywords
        'keyword_rock': 'Rock',
        'keyword_pop': 'Pop',
        'keyword_jazz': 'Jazz',
        'keyword_classical': 'Classical',
        'keyword_hip-hop': 'Hip-Hop',
        'keyword_edm': 'EDM',
        'keyword_metal': 'Metal',
        'keyword_country': 'Country',
        'keyword_reggae': 'Reggae',
        'keyword_electronic': 'Electronic',
        'keyword_blues': 'Blues',
        
        # Movie keywords
        'keyword_action': 'Action',
        'keyword_comedy': 'Comedy',
        'keyword_drama': 'Drama',
        'keyword_horror': 'Horror',
        'keyword_sci-fi': 'Sci-Fi',
        'keyword_romance': 'Romance',
        'keyword_thriller': 'Thriller',
        'keyword_animation': 'Animation',
        'keyword_documentary': 'Documentary',
        'keyword_fantasy': 'Fantasy',
        'keyword_crime': 'Crime',
        
        # Education keywords
        'keyword_science': 'Science',
        'keyword_technology': 'Technology',
        'keyword_history': 'History',
        'keyword_language': 'Language',
        'keyword_math': 'Math',
        'keyword_art': 'Art',
        'keyword_cooking': 'Cooking',
        'keyword_programming': 'Programming',
        'keyword_business': 'Business',
        'keyword_health': 'Health',
        'keyword_tutorial': 'Tutorial',
        'keyword_lecture': 'Lecture',
        
        # News keywords
        'keyword_politics': 'Politics',
        'keyword_world_news': 'World News',
        'keyword_economy': 'Economy',
        'keyword_sports': 'Sports',
        'keyword_tech_news': 'Tech News',
        'keyword_entertainment_news': 'Entertainment',
        'keyword_weather': 'Weather',
        'keyword_local_news': 'Local News',
        'keyword_sports_news': 'Sports News',
        'keyword_technology_news': 'Technology News',
        
        # Search precision
        'search_precision_label': 'Search Precision:',
        'precision_standard': 'Standard (Default)',
        'precision_standard_desc': 'Moderate search + official channel priority',
        'precision_high': 'High Precision',
        'precision_high_desc': 'Official channels only',
        'precision_highest': 'Highest Precision',
        'precision_highest_desc': 'Direct search from channel ID list',
        
        # Official channel options
        'option_official_channel': 'Prioritize Official Channels',
        'option_verified_badge': 'Require Verified Badge',
        'option_subscriber_100k': 'Subscribers: 100K+',
        'option_video_views_100k': 'Views: 100K+',
        'option_vevo_only': 'VEVO/Official Only',
        'option_add_detailed_to_desc': 'Add Detailed Description',
        
        # Privacy settings
        'privacy_private': 'Private (Only you can view)',
        'privacy_unlisted': 'Unlisted (Anyone with link can view)',
        'privacy_public': 'Public (Anyone can search and view)',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Progress
        'progress_waiting': 'Waiting...',
        'status_waiting': 'Waiting...',
        
        # Region selection
        'region_selected': 'Selected:',
        'region_none': 'None',
        'region_worldwide': 'Worldwide',
        
        # Regions
        'region_japan': 'Japan',
        'region_korea': 'South Korea',
        'region_china': 'China',
        'region_taiwan': 'Taiwan',
        'region_usa': 'USA',
        'region_uk': 'United Kingdom',
        'region_france': 'France',
        'region_germany': 'Germany',
        'region_spain': 'Spain',
        'region_italy': 'Italy',
        'region_canada': 'Canada',
        'region_australia': 'Australia',
        'region_brazil': 'Brazil',
        'region_mexico': 'Mexico',
        'region_india': 'India',
        'region_thailand': 'Thailand',
        'region_vietnam': 'Vietnam',
        'region_philippines': 'Philippines',
        'region_indonesia': 'Indonesia',
        'region_singapore': 'Singapore',
        'region_russia': 'Russia',
        'region_poland': 'Poland',
        'region_netherlands': 'Netherlands',
        'region_sweden': 'Sweden',
        'region_norway': 'Norway',
        'region_denmark': 'Denmark',
        'region_argentina': 'Argentina',
        'region_africa': 'Africa',
        'region_middle_east': 'Middle East',
        'region_new_zealand': 'New Zealand',
        
        # Buttons
        'button_create_playlist': 'Create Playlist',
        'button_refresh': 'Refresh',
        'button_delete': 'Delete',
        'button_cancel': 'Cancel',
        'button_export': 'Export',
        'button_import': 'Import',
        'button_open_url': 'Open URL',
        'button_recreate_sampler': 'Recreate Sampler',
        'button_video_info': 'Video Info',
        'button_delete_history': 'Delete History',
        'button_csv_export': 'Export CSV',
        
        # Labels
        'label_playlist_url': 'Playlist URL:',
        'label_created_date': 'Creation Date',
        'label_title': 'Title',
        'label_video_count': 'Video Count',
        'label_platform': 'Platform',
        'label_category_short': 'Category',
        'label_era_short': 'Era',
        'label_total': 'Total',
        
        # Section headers
        'section_preset': 'Preset',
        'section_result': 'Result',
        'section_history': 'History',
        'section_integrated_playlists': 'Integrated Playlist Viewer',
        
        # Additional options
        'option_add_region_keywords': 'Add Region Keywords',
        'option_add_detailed_desc': 'Add Detailed Description',
        
        # Additional keyword
        'label_additional_keyword': 'Additional Keyword',
        'additional_keyword': 'Additional Keyword',
        'selected_keywords': 'Selected Keywords',
        'region_keyword_auto': 'Auto-add Region Keywords',
        
        # Buttons (complete set)
        'btn_create_playlist': 'Create Playlist',
        'btn_cancel': 'Cancel',
        'btn_save': 'Save',
        'btn_copy_url': 'Copy URL',
        'btn_open': 'Open',
        'btn_refresh': 'Refresh',
        'btn_delete': 'Delete',
        'btn_delete_all': 'Delete All',
        'btn_export': 'Export',
        'btn_import': 'Import',
        'btn_recreate_same': 'Recreate Same',
        'btn_open_url': 'Open URL',
        'btn_video_confirm': 'Video Confirm',
        'btn_delete_history': 'Delete History',
        'btn_csv_export': 'CSV Export',
        'btn_create_new': 'Create New',
        'btn_json_export': 'JSON Export',
        'btn_html_export': 'HTML Export',
        'btn_edit': 'Edit',
        
        # Column headers
        'col_created_date': 'Created Date',
        'col_title': 'Title',
        'col_video_count': 'Video Count',
        'col_platform': 'Platform',
        'col_category': 'Category',
        'col_era': 'Era',
        'col_total': 'Total',
        'col_youtube': 'YouTube',
        'col_niconico': 'Niconico',
        
        # Labels
        'label_video_range': 'Video Range',
        
        # Section headers (additional)
        'section_integrated_viewer': 'Integrated Playlist Viewer',
        
        # Privacy descriptions
        'privacy_private_desc': 'Only you can view',
        'privacy_unlisted_desc': 'Only you can view',
        'privacy_public_desc': 'Anyone can search and view',
        
        # Messages
        'message_success': 'Success',
        'message_error': 'Error',
        'message_creating': 'Creating...',
        'message_searching': 'Searching...',
        
        # Setup and Auth
        'setup_wizard': 'Setup Wizard',
        'youtube_auth': 'YouTube Authentication',
        'niconico_auth': 'Niconico Authentication',
        'check_auth_status': 'Check Auth Status',
        
        # Help
        'youtube_api_help': 'YouTube API Help',
        'niconico_help': 'Niconico Help',
        'usage_guide': 'Usage Guide',
        'troubleshooting': 'Troubleshooting',
    },
    
    'zh-CN': {
        # Menu bar
        'menu_file': '文件',
        'menu_favorites': '我的言葉',
        'menu_settings': '设置',
        'menu_help': '帮助',
        'menu_export': '导出',
        'export_csv': 'CSV格式',
        'export_json': 'JSON格式',
        'export_txt': 'TXT格式',
        'backup_create': '创建备份',
        'backup_restore': '从备份恢复',
        'backup_manage': '备份管理',
        'menu_exit': '退出',
        'favorites_save': '保存当前设置',
        'favorites_load': '加载收藏',
        'favorites_manage': '收藏管理',
        'menu_language': '语言',
        'update_check': '检查更新',
        'about': '关于',
        
        # Main UI labels
        'label_era': '年代:',
        'label_category': '类别:',
        'label_video_count': '视频数量:',
        
        # Sections
        'section_basic': '基本设置',
        'section_keywords': '关键字和地区',
        'section_search_options': '搜索选项',
        'section_official_channel': '官方频道优先设定:',
        'section_privacy': '隐私设置',
        'section_platform': '平台',
        'section_progress': '进度',
        
        # Tab names
        'tab_music': '音乐',
        'tab_movies': '电影',
        'tab_education': '教育',
        'tab_news': '新闻',
        'tab_region': '地区',
        'tab_history': '历史记录',
        'tab_integrated_viewer': '统合播放清单查看器',
        'tab_playlist': '播放清单URL',
        
        # Music keywords
        'keyword_rock': '摇滚',
        'keyword_pop': '流行',
        'keyword_jazz': '爵士',
        'keyword_classical': '古典',
        'keyword_hip-hop': '嘻哈',
        'keyword_edm': 'EDM',
        'keyword_metal': '金属',
        'keyword_country': '乡村',
        'keyword_reggae': '雷鬼',
        'keyword_electronic': '电子',
        'keyword_blues': '蓝调',
        
        # Movie keywords
        'keyword_action': '动作',
        'keyword_comedy': '喜剧',
        'keyword_drama': '剧情',
        'keyword_horror': '恐怖',
        'keyword_sci-fi': '科幻',
        'keyword_romance': '爱情',
        'keyword_thriller': '惊悚',
        'keyword_animation': '动画',
        'keyword_documentary': '纪录片',
        'keyword_fantasy': '奇幻',
        'keyword_crime': '犯罪',
        
        # Education keywords
        'keyword_science': '科学',
        'keyword_technology': '技术',
        'keyword_history': '历史',
        'keyword_language': '语言',
        'keyword_math': '数学',
        'keyword_art': '艺术',
        'keyword_cooking': '烹饪',
        'keyword_programming': '编程',
        'keyword_business': '商业',
        'keyword_health': '健康',
        'keyword_tutorial': '教程',
        'keyword_lecture': '讲座',
        
        # News keywords
        'keyword_politics': '政治',
        'keyword_world_news': '国际新闻',
        'keyword_economy': '经济',
        'keyword_sports': '体育',
        'keyword_tech_news': '科技新闻',
        'keyword_entertainment_news': '娱乐',
        'keyword_weather': '天气',
        'keyword_local_news': '本地新闻',
        'keyword_sports_news': '体育新闻',
        'keyword_technology_news': '科技新闻',
        
        # Search precision
        'search_precision_label': '搜索精度:',
        'precision_standard': '标准（默认）',
        'precision_standard_desc': '适度搜索＋官方频道优先',
        'precision_high': '高精度',
        'precision_high_desc': '仅官方频道',
        'precision_highest': '最高精度',
        'precision_highest_desc': '从频道ID列表直接搜索',
        
        # Official channel options
        'option_official_channel': '官方频道优先',
        'option_verified_badge': '需要认证徽章',
        'option_subscriber_100k': '订阅者: 10万人以上',
        'option_video_views_100k': '观看次数: 10万次以上',
        'option_vevo_only': '仅VEVO/官方',
        'option_add_detailed_to_desc': '新增详细说明',
        
        # Privacy settings
        'privacy_private': '私人（仅自己可以看）',
        'privacy_unlisted': '不公开（仅自己可看）',
        'privacy_public': '公开（任何人都可以搜索和查看）',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Progress
        'progress_waiting': '等待中...',
        'status_waiting': '等待中...',
        
        # Region selection
        'region_selected': '已选择:',
        'region_none': '无',
        'region_worldwide': '全球',
        
        # Regions
        'region_japan': '日本',
        'region_korea': '韩国',
        'region_china': '中国',
        'region_taiwan': '台湾',
        'region_usa': '美国',
        'region_uk': '英国',
        'region_france': '法国',
        'region_germany': '德国',
        'region_spain': '西班牙',
        'region_italy': '意大利',
        'region_canada': '加拿大',
        'region_australia': '澳大利亚',
        'region_brazil': '巴西',
        'region_mexico': '墨西哥',
        'region_india': '印度',
        'region_thailand': '泰国',
        'region_vietnam': '越南',
        'region_philippines': '菲律宾',
        'region_indonesia': '印度尼西亚',
        'region_singapore': '新加坡',
        'region_russia': '俄罗斯',
        'region_poland': '波兰',
        'region_netherlands': '荷兰',
        'region_sweden': '瑞典',
        'region_norway': '挪威',
        'region_denmark': '丹麦',
        'region_argentina': '阿根廷',
        'region_africa': '非洲',
        'region_middle_east': '中东',
        'region_new_zealand': '新西兰',
        
        # Buttons
        'button_create_playlist': '创建播放列表',
        'button_refresh': '刷新',
        'button_delete': '删除',
        'button_cancel': '取消',
        'button_export': '导出',
        'button_import': '导入',
        'button_open_url': '打开URL',
        'button_recreate_sampler': '重新创建取样器',
        'button_video_info': '视频信息',
        'button_delete_history': '删除历史',
        'button_csv_export': '导出CSV',
        
        # Labels
        'label_playlist_url': '播放列表URL:',
        'label_created_date': '创建日期',
        'label_title': '标题',
        'label_video_count': '视频数量',
        'label_platform': '平台',
        'label_category_short': '类别',
        'label_era_short': '年代',
        'label_total': '总计',
        
        # Section headers
        'section_preset': '预设',
        'section_result': '结果',
        'section_history': '历史记录',
        'section_integrated_playlists': '统合播放清单查看器',
        
        # Additional options
        'option_add_region_keywords': '添加地区关键字',
        'option_add_detailed_desc': '添加详细说明',
        
        # Additional keyword
        'label_additional_keyword': '附加关键字',
        'additional_keyword': '附加关键字',
        'selected_keywords': '已选关键字',
        'region_keyword_auto': '自动添加地区关键字',
        
        # Buttons (complete set)
        'btn_create_playlist': '创建播放列表',
        'btn_cancel': '取消',
        'btn_save': '保存',
        'btn_copy_url': '复制URL',
        'btn_open': '打开',
        'btn_refresh': '刷新',
        'btn_delete': '删除',
        'btn_delete_all': '全部删除',
        'btn_export': '导出',
        'btn_import': '导入',
        'btn_recreate_same': '相同条件重建',
        'btn_open_url': '打开URL',
        'btn_video_confirm': '确认视频',
        'btn_delete_history': '删除历史',
        'btn_csv_export': 'CSV导出',
        'btn_create_new': '新建',
        'btn_json_export': 'JSON导出',
        'btn_html_export': 'HTML导出',
        'btn_edit': '编辑',
        
        # Column headers
        'col_created_date': '创建日期',
        'col_title': '标题',
        'col_video_count': '视频数',
        'col_platform': '平台',
        'col_category': '类别',
        'col_era': '年代',
        'col_total': '总计',
        'col_youtube': 'YouTube',
        'col_niconico': 'Niconico',
        
        # Labels
        'label_video_range': '视频范围',
        
        # Section headers (additional)
        'section_integrated_viewer': '统合播放列表查看器',
        
        # Privacy descriptions
        'privacy_private_desc': '仅自己可看',
        'privacy_unlisted_desc': '仅自己可看',
        'privacy_public_desc': '任何人都可以搜索和查看',
        
        # Messages
        'message_success': '成功',
        'message_error': '错误',
        'message_creating': '创建中...',
        'message_searching': '搜索中...',
        
        # Setup and Auth
        'setup_wizard': '设置向导',
        'youtube_auth': 'YouTube认证',
        'niconico_auth': 'Niconico认证',
        'check_auth_status': '检查认证状态',
        
        # Help
        'youtube_api_help': 'YouTube API帮助',
        'niconico_help': 'Niconico帮助',
        'usage_guide': '使用指南',
        'troubleshooting': '故障排除',
    },
    
    'zh-TW': {
        # Menu bar
        'menu_file': '檔案',
        'menu_favorites': '我的最愛',
        'menu_settings': '設定',
        'menu_help': '說明',
        'menu_export': '匯出',
        'export_csv': 'CSV格式',
        'export_json': 'JSON格式',
        'export_txt': 'TXT格式',
        'backup_create': '建立備份',
        'backup_restore': '從備份還原',
        'backup_manage': '備份管理',
        'menu_exit': '結束',
        'favorites_save': '儲存目前設定',
        'favorites_load': '載入我的最愛',
        'favorites_manage': '我的最愛管理',
        'menu_language': '語言',
        'update_check': '檢查更新',
        'about': '關於',
        
        # Main UI labels
        'label_era': '年代:',
        'label_category': '類別:',
        'label_video_count': '影片數量:',
        
        # Sections
        'section_basic': '基本設定',
        'section_keywords': '關鍵字和地區',
        'section_search_options': '搜尋選項',
        'section_official_channel': '官方頻道優先設定:',
        'section_privacy': '隱私設定',
        'section_platform': '平台',
        'section_progress': '進度',
        
        # Tab names
        'tab_music': '音樂',
        'tab_movies': '電影',
        'tab_education': '教育',
        'tab_news': '新聞',
        'tab_region': '地區',
        'tab_history': '歷史記錄',
        'tab_integrated_viewer': '統合播放清單檢視器',
        'tab_playlist': '播放清單URL',
        
        # Music keywords
        'keyword_rock': '搖滾',
        'keyword_pop': '流行',
        'keyword_jazz': '爵士',
        'keyword_classical': '古典',
        'keyword_hip-hop': '嘻哈',
        'keyword_edm': 'EDM',
        'keyword_metal': '金屬',
        'keyword_country': '鄉村',
        'keyword_reggae': '雷鬼',
        'keyword_electronic': '電子',
        'keyword_blues': '藍調',
        
        # Movie keywords
        'keyword_action': '動作',
        'keyword_comedy': '喜劇',
        'keyword_drama': '劇情',
        'keyword_horror': '恐怖',
        'keyword_sci-fi': '科幻',
        'keyword_romance': '愛情',
        'keyword_thriller': '驚悚',
        'keyword_animation': '動畫',
        'keyword_documentary': '紀錄片',
        'keyword_fantasy': '奇幻',
        'keyword_crime': '犯罪',
        
        # Education keywords
        'keyword_science': '科學',
        'keyword_technology': '技術',
        'keyword_history': '歷史',
        'keyword_language': '語言',
        'keyword_math': '數學',
        'keyword_art': '藝術',
        'keyword_cooking': '烹飪',
        'keyword_programming': '程式設計',
        'keyword_business': '商業',
        'keyword_health': '健康',
        'keyword_tutorial': '教學',
        'keyword_lecture': '講座',
        
        # News keywords
        'keyword_politics': '政治',
        'keyword_world_news': '國際新聞',
        'keyword_economy': '經濟',
        'keyword_sports': '體育',
        'keyword_tech_news': '科技新聞',
        'keyword_entertainment_news': '娛樂',
        'keyword_weather': '天氣',
        'keyword_local_news': '本地新聞',
        'keyword_sports_news': '體育新聞',
        'keyword_technology_news': '科技新聞',
        
        # Search precision
        'search_precision_label': '搜尋精度:',
        'precision_standard': '標準（預設）',
        'precision_standard_desc': '適度搜尋＋官方頻道優先',
        'precision_high': '高精度',
        'precision_high_desc': '僅官方頻道',
        'precision_highest': '最高精度',
        'precision_highest_desc': '從頻道ID清單直接搜尋',
        
        # Official channel options
        'option_official_channel': '官方頻道優先',
        'option_verified_badge': '需要認證徽章',
        'option_subscriber_100k': '訂閱者: 10萬人以上',
        'option_video_views_100k': '觀看次數: 10萬次以上',
        'option_vevo_only': '僅VEVO/官方',
        'option_add_detailed_to_desc': '新增詳細說明',
        
        # Privacy settings
        'privacy_private': '私人（僅自己可以看）',
        'privacy_unlisted': '不公開（僅自己可看）',
        'privacy_public': '公開（任何人都可以搜尋和查看）',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Progress
        'progress_waiting': '等待中...',
        'status_waiting': '等待中...',
        
        # Region selection
        'region_selected': '已選擇:',
        'region_none': '無',
        'region_worldwide': '全球',
        
        # Regions
        'region_japan': '日本',
        'region_korea': '韓國',
        'region_china': '中國',
        'region_taiwan': '台灣',
        'region_usa': '美國',
        'region_uk': '英國',
        'region_france': '法國',
        'region_germany': '德國',
        'region_spain': '西班牙',
        'region_italy': '義大利',
        'region_canada': '加拿大',
        'region_australia': '澳洲',
        'region_brazil': '巴西',
        'region_mexico': '墨西哥',
        'region_india': '印度',
        'region_thailand': '泰國',
        'region_vietnam': '越南',
        'region_philippines': '菲律賓',
        'region_indonesia': '印尼',
        'region_singapore': '新加坡',
        'region_russia': '俄羅斯',
        'region_poland': '波蘭',
        'region_netherlands': '荷蘭',
        'region_sweden': '瑞典',
        'region_norway': '挪威',
        'region_denmark': '丹麥',
        'region_argentina': '阿根廷',
        'region_africa': '非洲',
        'region_middle_east': '中東',
        'region_new_zealand': '紐西蘭',
        
        # Buttons
        'button_create_playlist': '建立播放清單',
        'button_refresh': '重新整理',
        'button_delete': '刪除',
        'button_cancel': '取消',
        'button_export': '匯出',
        'button_import': '匯入',
        'button_open_url': '開啟URL',
        'button_recreate_sampler': '重新建立取樣器',
        'button_video_info': '影片資訊',
        'button_delete_history': '刪除歷史',
        'button_csv_export': '匯出CSV',
        
        # Labels
        'label_playlist_url': '播放清單URL:',
        'label_created_date': '建立日期',
        'label_title': '標題',
        'label_video_count': '影片數量',
        'label_platform': '平台',
        'label_category_short': '類別',
        'label_era_short': '年代',
        'label_total': '總計',
        
        # Section headers
        'section_preset': '預設',
        'section_result': '結果',
        'section_history': '歷史記錄',
        'section_integrated_playlists': '統合播放清單檢視器',
        
        # Additional options
        'option_add_region_keywords': '新增地區關鍵字',
        'option_add_detailed_desc': '新增詳細說明',
        
        # Additional keyword
        'label_additional_keyword': '附加關鍵字',
        'additional_keyword': '附加關鍵字',
        'selected_keywords': '已選關鍵字',
        'region_keyword_auto': '自動添加地區關鍵字',
        
        # Buttons (complete set)
        'btn_create_playlist': '建立播放清單',
        'btn_cancel': '取消',
        'btn_save': '儲存',
        'btn_copy_url': '複製URL',
        'btn_open': '開啟',
        'btn_refresh': '重新整理',
        'btn_delete': '刪除',
        'btn_delete_all': '全部刪除',
        'btn_export': '匯出',
        'btn_import': '匯入',
        'btn_recreate_same': '相同條件重建',
        'btn_open_url': '開啟URL',
        'btn_video_confirm': '確認影片',
        'btn_delete_history': '刪除歷史',
        'btn_csv_export': 'CSV匯出',
        'btn_create_new': '新建',
        'btn_json_export': 'JSON匯出',
        'btn_html_export': 'HTML匯出',
        'btn_edit': '編輯',
        
        # Column headers
        'col_created_date': '建立日期',
        'col_title': '標題',
        'col_video_count': '影片數',
        'col_platform': '平台',
        'col_category': '類別',
        'col_era': '年代',
        'col_total': '總計',
        'col_youtube': 'YouTube',
        'col_niconico': 'Niconico',
        
        # Labels
        'label_video_range': '影片範圍',
        
        # Section headers (additional)
        'section_integrated_viewer': '統合播放清單查看器',
        
        # Privacy descriptions
        'privacy_private_desc': '僅自己可看',
        'privacy_unlisted_desc': '僅自己可看',
        'privacy_public_desc': '任何人都可以搜尋和查看',
        
        # Messages
        'message_success': '成功',
        'message_error': '錯誤',
        'message_creating': '建立中...',
        'message_searching': '搜尋中...',
        
        # Setup and Auth
        'setup_wizard': '設定精靈',
        'youtube_auth': 'YouTube認證',
        'niconico_auth': 'Niconico認證',
        'check_auth_status': '檢查認證狀態',
        
        # Help
        'youtube_api_help': 'YouTube API說明',
        'niconico_help': 'Niconico說明',
        'usage_guide': '使用指南',
        'troubleshooting': '故障排除',
    },
    
    'ko': {
        # Menu bar
        'menu_file': '파일',
        'menu_favorites': '즐겨찾기',
        'menu_settings': '설정',
        'menu_help': '도움말',
        'menu_export': '내보내기',
        'export_csv': 'CSV 형식',
        'export_json': 'JSON 형식',
        'export_txt': 'TXT 형식',
        'backup_create': '백업 만들기',
        'backup_restore': '백업에서 복원',
        'backup_manage': '백업 관리',
        'menu_exit': '종료',
        'favorites_save': '현재 설정 저장',
        'favorites_load': '즐겨찾기 불러오기',
        'favorites_manage': '즐겨찾기 관리',
        'menu_language': '언어',
        'update_check': '업데이트 확인',
        'about': '정보',
        
        # Main UI labels
        'label_era': '연대:',
        'label_category': '카테고리:',
        'label_video_count': '동영상 수:',
        
        # Sections
        'section_basic': '기본 설정',
        'section_keywords': '키워드·지역',
        'section_search_options': '검색 옵션',
        'section_official_channel': '공식 채널 우선 설정:',
        'section_privacy': '공개 설정',
        'section_platform': '플랫폼',
        'section_progress': '진행 상황',
        
        # Tab names
        'tab_music': '음악',
        'tab_movies': '영화',
        'tab_education': '교육',
        'tab_news': '뉴스',
        'tab_region': '지역',
        'tab_history': '기록',
        'tab_integrated_viewer': '통합 재생목록 뷰어',
        'tab_playlist': '재생목록 URL',
        
        # Music keywords
        'keyword_rock': '록',
        'keyword_pop': '팝',
        'keyword_jazz': '재즈',
        'keyword_classical': '클래식',
        'keyword_hip-hop': '힙합',
        'keyword_edm': 'EDM',
        'keyword_metal': '메탈',
        'keyword_country': '컨트리',
        'keyword_reggae': '레게',
        'keyword_electronic': '일렉트로닉',
        'keyword_blues': '블루스',
        
        # Movie keywords
        'keyword_action': '액션',
        'keyword_comedy': '코미디',
        'keyword_drama': '드라마',
        'keyword_horror': '공포',
        'keyword_sci-fi': 'SF',
        'keyword_romance': '로맨스',
        'keyword_thriller': '스릴러',
        'keyword_animation': '애니메이션',
        'keyword_documentary': '다큐멘터리',
        'keyword_fantasy': '판타지',
        'keyword_crime': '범죄',
        
        # Education keywords
        'keyword_science': '과학',
        'keyword_technology': '기술',
        'keyword_history': '역사',
        'keyword_language': '언어',
        'keyword_math': '수학',
        'keyword_art': '예술',
        'keyword_cooking': '요리',
        'keyword_programming': '프로그래밍',
        'keyword_business': '비즈니스',
        'keyword_health': '건강',
        'keyword_tutorial': '튜토리얼',
        'keyword_lecture': '강의',
        
        # News keywords
        'keyword_politics': '정치',
        'keyword_world_news': '국제 뉴스',
        'keyword_economy': '경제',
        'keyword_sports': '스포츠',
        'keyword_tech_news': '기술 뉴스',
        'keyword_entertainment_news': '연예',
        'keyword_weather': '날씨',
        'keyword_local_news': '지역 뉴스',
        'keyword_sports_news': '스포츠 뉴스',
        'keyword_technology_news': '기술 뉴스',
        
        # Search precision
        'search_precision_label': '검색 정확도:',
        'precision_standard': '표준（기본）',
        'precision_standard_desc': '적당한 검색＋공식 채널 우선',
        'precision_high': '고정밀',
        'precision_high_desc': '공식 채널만',
        'precision_highest': '최고정밀',
        'precision_highest_desc': '채널 ID 목록에서 직접 검색',
        
        # Official channel options
        'option_official_channel': '공식 채널 우선',
        'option_verified_badge': '인증 배지 필수',
        'option_subscriber_100k': '구독자: 10만 명 이상',
        'option_video_views_100k': '조회수: 10만 회 이상',
        'option_vevo_only': 'VEVO/공식만',
        'option_add_detailed_to_desc': '상세 설명 추가',
        
        # Privacy settings
        'privacy_private': '비공개（본인만 볼 수 있음）',
        'privacy_unlisted': '일부 공개（본인만 볼 수 있음）',
        'privacy_public': '공개（누구나 검색하고 볼 수 있음）',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Progress
        'progress_waiting': '대기 중...',
        'status_waiting': '대기 중...',
        
        # Region selection
        'region_selected': '선택됨:',
        'region_none': '없음',
        'region_worldwide': '전 세계',
        
        # Regions
        'region_japan': '일본',
        'region_korea': '영국',
        'region_china': '중국',
        'region_taiwan': '대만',
        'region_usa': '미국',
        'region_uk': '영국',
        'region_france': '프랑스',
        'region_germany': '독일',
        'region_spain': '스페인',
        'region_italy': '이탈리아',
        'region_canada': '캐나다',
        'region_australia': '호주',
        'region_brazil': '브라질',
        'region_mexico': '멕시코',
        'region_india': '인도',
        'region_thailand': '태국',
        'region_vietnam': '베트남',
        'region_philippines': '필리핀',
        'region_indonesia': '인도네시아',
        'region_singapore': '싱가포르',
        'region_russia': '러시아',
        'region_poland': '폴란드',
        'region_netherlands': '네덜란드',
        'region_sweden': '스웨덴',
        'region_norway': '노르웨이',
        'region_denmark': '덴마크',
        'region_argentina': '아르헨티나',
        'region_africa': '아프리카',
        'region_middle_east': '중동',
        'region_new_zealand': '뉴질랜드',
        
        # Buttons
        'button_create_playlist': '재생목록 만들기',
        'button_refresh': '새로 고침',
        'button_delete': '삭제',
        'button_cancel': '취소',
        'button_export': '내보내기',
        'button_import': '가져오기',
        'button_open_url': 'URL 열기',
        'button_recreate_sampler': '샘플러 다시 만들기',
        'button_video_info': '동영상 정보',
        'button_delete_history': '기록 삭제',
        'button_csv_export': 'CSV 내보내기',
        
        # Labels
        'label_playlist_url': '재생목록 URL:',
        'label_created_date': '생성 날짜',
        'label_title': '제목',
        'label_video_count': '동영상 수',
        'label_platform': '플랫폼',
        'label_category_short': '카테고리',
        'label_era_short': '연대',
        'label_total': '합계',
        
        # Section headers
        'section_preset': '프리셋',
        'section_result': '결과',
        'section_history': '기록',
        'section_integrated_playlists': '통합 재생목록 뷰어',
        
        # Additional options
        'option_add_region_keywords': '지역 키워드 추가',
        'option_add_detailed_desc': '상세 설명 추가',
        
        # Additional keyword
        'label_additional_keyword': '추가 키워드',
        'additional_keyword': '추가 키워드',
        'selected_keywords': '선택된 키워드',
        'region_keyword_auto': '지역 키워드 자동 추가',
        
        # Buttons (complete set)
        'btn_create_playlist': '재생목록 만들기',
        'btn_cancel': '취소',
        'btn_save': '저장',
        'btn_copy_url': 'URL 복사',
        'btn_open': '열기',
        'btn_refresh': '새로고침',
        'btn_delete': '삭제',
        'btn_delete_all': '전체 삭제',
        'btn_export': '내보내기',
        'btn_import': '가져오기',
        'btn_recreate_same': '동일 조건으로 재생성',
        'btn_open_url': 'URL 열기',
        'btn_video_confirm': '동영상 확인',
        'btn_delete_history': '기록 삭제',
        'btn_csv_export': 'CSV 내보내기',
        'btn_create_new': '새로 만들기',
        'btn_json_export': 'JSON 내보내기',
        'btn_html_export': 'HTML 내보내기',
        'btn_edit': '편집',
        
        # Column headers
        'col_created_date': '생성 날짜',
        'col_title': '제목',
        'col_video_count': '동영상 수',
        'col_platform': '플랫폼',
        'col_category': '카테고리',
        'col_era': '연대',
        'col_total': '합계',
        'col_youtube': 'YouTube',
        'col_niconico': 'Niconico',
        
        # Labels
        'label_video_range': '동영상 범위',
        
        # Section headers (additional)
        'section_integrated_viewer': '통합 재생목록 뷰어',
        
        # Privacy descriptions
        'privacy_private_desc': '본인만 볼 수 있음',
        'privacy_unlisted_desc': '본인만 볼 수 있음',
        'privacy_public_desc': '누구나 검색하고 볼 수 있음',
        
        # Messages
        'message_success': '성공',
        'message_error': '오류',
        'message_creating': '생성 중...',
        'message_searching': '검색 중...',
        
        # Setup and Auth
        'setup_wizard': '설정 마법사',
        'youtube_auth': 'YouTube 인증',
        'niconico_auth': 'Niconico 인증',
        'check_auth_status': '인증 상태 확인',
        
        # Help
        'youtube_api_help': 'YouTube API 도움말',
        'niconico_help': 'Niconico 도움말',
        'usage_guide': '사용 가이드',
        'troubleshooting': '문제 해결',
    },
    
    'es': {
        # Menu bar
        'menu_file': 'Archivo',
        'menu_favorites': 'Favoritos',
        'menu_settings': 'Configuración',
        'menu_help': 'Ayuda',
        'menu_export': 'Exportar',
        'export_csv': 'Formato CSV',
        'export_json': 'Formato JSON',
        'export_txt': 'Formato TXT',
        'backup_create': 'Crear copia de seguridad',
        'backup_restore': 'Restaurar desde copia',
        'backup_manage': 'Gestionar copias',
        'menu_exit': 'Salir',
        'favorites_save': 'Guardar configuración actual',
        'favorites_load': 'Cargar favoritos',
        'favorites_manage': 'Gestionar favoritos',
        'menu_language': 'Idioma',
        'update_check': 'Buscar actualizaciones',
        'about': 'Acerca de',
        
        # Main UI labels
        'label_era': 'Época:',
        'label_category': 'Categoría:',
        'label_video_count': 'Número de videos:',
        
        # Sections
        'section_basic': 'Configuración básica',
        'section_keywords': 'Palabras clave y región',
        'section_search_options': 'Opciones de búsqueda',
        'section_official_channel': 'Priorizar canales oficiales:',
        'section_privacy': 'Configuración de privacidad',
        'section_platform': 'Plataforma',
        'section_progress': 'Progreso',
        
        # Tab names
        'tab_music': 'Música',
        'tab_movies': 'Películas',
        'tab_education': 'Educación',
        'tab_news': 'Noticias',
        'tab_region': 'Región',
        'tab_history': 'Historial',
        'tab_integrated_viewer': 'Visor de listas integradas',
        'tab_playlist': 'URL de lista de reproducción',
        
        # Music keywords
        'keyword_rock': 'Rock',
        'keyword_pop': 'Pop',
        'keyword_jazz': 'Jazz',
        'keyword_classical': 'Clásica',
        'keyword_hip-hop': 'Hip-Hop',
        'keyword_edm': 'EDM',
        'keyword_metal': 'Metal',
        'keyword_country': 'Country',
        'keyword_reggae': 'Reggae',
        'keyword_electronic': 'Electrónica',
        'keyword_blues': 'Blues',
        
        # Movie keywords
        'keyword_action': 'Acción',
        'keyword_comedy': 'Comedia',
        'keyword_drama': 'Drama',
        'keyword_horror': 'Terror',
        'keyword_sci-fi': 'Ciencia ficción',
        'keyword_romance': 'Romance',
        'keyword_thriller': 'Thriller',
        'keyword_animation': 'Animación',
        'keyword_documentary': 'Documental',
        'keyword_fantasy': 'Fantasía',
        'keyword_crime': 'Crimen',
        
        # Education keywords
        'keyword_science': 'Ciencia',
        'keyword_technology': 'Tecnología',
        'keyword_history': 'Historia',
        'keyword_language': 'Idioma',
        'keyword_math': 'Matemáticas',
        'keyword_art': 'Arte',
        'keyword_cooking': 'Cocina',
        'keyword_programming': 'Programación',
        'keyword_business': 'Negocios',
        'keyword_health': 'Salud',
        'keyword_tutorial': 'Tutorial',
        'keyword_lecture': 'Conferencia',
        
        # News keywords
        'keyword_politics': 'Política',
        'keyword_world_news': 'Noticias mundiales',
        'keyword_economy': 'Economía',
        'keyword_sports': 'Deportes',
        'keyword_tech_news': 'Noticias de tecnología',
        'keyword_entertainment_news': 'Entretenimiento',
        'keyword_weather': 'Clima',
        'keyword_local_news': 'Noticias locales',
        'keyword_sports_news': 'Noticias deportivas',
        'keyword_technology_news': 'Noticias de tecnología',
        
        # Search precision
        'search_precision_label': 'Precisión de búsqueda:',
        'precision_standard': 'Estándar（predeterminado）',
        'precision_standard_desc': 'Búsqueda moderada＋prioridad canal oficial',
        'precision_high': 'Alta precisión',
        'precision_high_desc': 'Solo canales oficiales',
        'precision_highest': 'Máxima precisión',
        'precision_highest_desc': 'Búsqueda directa desde lista de ID de canal',
        
        # Official channel options
        'option_official_channel': 'Priorizar canales oficiales',
        'option_verified_badge': 'Requiere insignia verificada',
        'option_subscriber_100k': 'Suscriptores: 100K+',
        'option_video_views_100k': 'Visualizaciones: 100K+',
        'option_vevo_only': 'Solo VEVO/Oficial',
        'option_add_detailed_to_desc': 'Agregar descripción detallada',
        
        # Privacy settings
        'privacy_private': 'Privado（solo tú puedes ver）',
        'privacy_unlisted': 'No listado（solo tú puedes ver）',
        'privacy_public': 'Público（cualquiera puede buscar y ver）',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Progress
        'progress_waiting': 'Esperando...',
        'status_waiting': 'Esperando...',
        
        # Region selection
        'region_selected': 'Seleccionado:',
        'region_none': 'Ninguno',
        'region_worldwide': 'Mundial',
        
        # Regions
        'region_japan': 'Japón',
        'region_korea': 'Corea del Sur',
        'region_china': 'China',
        'region_taiwan': 'Taiwán',
        'region_usa': 'EE.UU.',
        'region_uk': 'Reino Unido',
        'region_france': 'Francia',
        'region_germany': 'Alemania',
        'region_spain': 'España',
        'region_italy': 'Italia',
        'region_canada': 'Canadá',
        'region_australia': 'Australia',
        'region_brazil': 'Brasil',
        'region_mexico': 'México',
        'region_india': 'India',
        'region_thailand': 'Tailandia',
        'region_vietnam': 'Vietnam',
        'region_philippines': 'Filipinas',
        'region_indonesia': 'Indonesia',
        'region_singapore': 'Singapur',
        'region_russia': 'Rusia',
        'region_poland': 'Polonia',
        'region_netherlands': 'Países Bajos',
        'region_sweden': 'Suecia',
        'region_norway': 'Noruega',
        'region_denmark': 'Dinamarca',
        'region_argentina': 'Argentina',
        'region_africa': 'África',
        'region_middle_east': 'Oriente Medio',
        'region_new_zealand': 'Nueva Zelanda',
        
        # Buttons
        'button_create_playlist': 'Crear lista de reproducción',
        'button_refresh': 'Actualizar',
        'button_delete': 'Eliminar',
        'button_cancel': 'Cancelar',
        'button_export': 'Exportar',
        'button_import': 'Importar',
        'button_open_url': 'Abrir URL',
        'button_recreate_sampler': 'Recrear muestreador',
        'button_video_info': 'Información de video',
        'button_delete_history': 'Eliminar historial',
        'button_csv_export': 'Exportar CSV',
        
        # Labels
        'label_playlist_url': 'URL de lista de reproducción:',
        'label_created_date': 'Fecha de creación',
        'label_title': 'Título',
        'label_video_count': 'Número de videos',
        'label_platform': 'Plataforma',
        'label_category_short': 'Categoría',
        'label_era_short': 'Época',
        'label_total': 'Total',
        
        # Section headers
        'section_preset': 'Preajuste',
        'section_result': 'Resultado',
        'section_history': 'Historial',
        'section_integrated_playlists': 'Visor de listas integradas',
        
        # Additional options
        'option_add_region_keywords': 'Agregar palabras clave de región',
        'option_add_detailed_desc': 'Agregar descripción detallada',
        
        # Additional keyword
        'label_additional_keyword': 'Palabra clave adicional',
        'additional_keyword': 'Palabra clave adicional',
        'selected_keywords': 'Palabras clave seleccionadas',
        'region_keyword_auto': 'Agregar automáticamente palabras clave regionales',
        
        # Buttons (complete set)
        'btn_create_playlist': 'Crear lista de reproducción',
        'btn_cancel': 'Cancelar',
        'btn_save': 'Guardar',
        'btn_copy_url': 'Copiar URL',
        'btn_open': 'Abrir',
        'btn_refresh': 'Actualizar',
        'btn_delete': 'Eliminar',
        'btn_delete_all': 'Eliminar todo',
        'btn_export': 'Exportar',
        'btn_import': 'Importar',
        'btn_recreate_same': 'Recrear con mismas condiciones',
        'btn_open_url': 'Abrir URL',
        'btn_video_confirm': 'Confirmar video',
        'btn_delete_history': 'Eliminar historial',
        'btn_csv_export': 'Exportar CSV',
        'btn_create_new': 'Crear nuevo',
        'btn_json_export': 'Exportar JSON',
        'btn_html_export': 'Exportar HTML',
        'btn_edit': 'Editar',
        
        # Column headers
        'col_created_date': 'Fecha de creación',
        'col_title': 'Título',
        'col_video_count': 'Número de videos',
        'col_platform': 'Plataforma',
        'col_category': 'Categoría',
        'col_era': 'Época',
        'col_total': 'Total',
        'col_youtube': 'YouTube',
        'col_niconico': 'Niconico',
        
        # Labels
        'label_video_range': 'Rango de videos',
        
        # Section headers (additional)
        'section_integrated_viewer': 'Visor de listas integradas',
        
        # Privacy descriptions
        'privacy_private_desc': 'Solo tú puedes ver',
        'privacy_unlisted_desc': 'Solo tú puedes ver',
        'privacy_public_desc': 'Cualquiera puede buscar y ver',
        
        # Messages
        'message_success': 'Éxito',
        'message_error': 'Error',
        'message_creating': 'Creando...',
        'message_searching': 'Buscando...',
        
        # Setup and Auth
        'setup_wizard': 'Asistente de configuración',
        'youtube_auth': 'Autenticación de YouTube',
        'niconico_auth': 'Autenticación de Niconico',
        'check_auth_status': 'Verificar estado de autenticación',
        
        # Help
        'youtube_api_help': 'Ayuda de API de YouTube',
        'niconico_help': 'Ayuda de Niconico',
        'usage_guide': 'Guía de uso',
        'troubleshooting': 'Solución de problemas',
    },
    
    'fr': {
        # Menu bar
        'menu_file': 'Fichier',
        'menu_favorites': 'Favoris',
        'menu_settings': 'Paramètres',
        'menu_help': 'Aide',
        'menu_export': 'Exporter',
        'export_csv': 'Format CSV',
        'export_json': 'Format JSON',
        'export_txt': 'Format TXT',
        'backup_create': 'Créer une sauvegarde',
        'backup_restore': 'Restaurer depuis une sauvegarde',
        'backup_manage': 'Gérer les sauvegardes',
        'menu_exit': 'Quitter',
        'favorites_save': 'Enregistrer la configuration actuelle',
        'favorites_load': 'Charger les favoris',
        'favorites_manage': 'Gérer les favoris',
        'menu_language': 'Langue',
        'update_check': 'Vérifier les mises à jour',
        'about': 'À propos',
        
        # Main UI labels
        'label_era': 'Époque:',
        'label_category': 'Catégorie:',
        'label_video_count': 'Nombre de vidéos:',
        
        # Sections
        'section_basic': 'Paramètres de base',
        'section_keywords': 'Mots-clés et région',
        'section_search_options': 'Options de recherche',
        'section_official_channel': 'Priorité aux chaînes officielles:',
        'section_privacy': 'Paramètres de confidentialité',
        'section_platform': 'Plateforme',
        'section_progress': 'Progression',
        
        # Tab names
        'tab_music': 'Musique',
        'tab_movies': 'Films',
        'tab_education': 'Éducation',
        'tab_news': 'Actualités',
        'tab_region': 'Région',
        'tab_history': 'Historique',
        'tab_integrated_viewer': 'Visionneuse de playlists intégrées',
        'tab_playlist': 'URL de la playlist',
        
        # Music keywords
        'keyword_rock': 'Rock',
        'keyword_pop': 'Pop',
        'keyword_jazz': 'Jazz',
        'keyword_classical': 'Classique',
        'keyword_hip-hop': 'Hip-Hop',
        'keyword_edm': 'EDM',
        'keyword_metal': 'Metal',
        'keyword_country': 'Country',
        'keyword_reggae': 'Reggae',
        'keyword_electronic': 'Électronique',
        'keyword_blues': 'Blues',
        
        # Movie keywords
        'keyword_action': 'Action',
        'keyword_comedy': 'Comédie',
        'keyword_drama': 'Drame',
        'keyword_horror': 'Horreur',
        'keyword_sci-fi': 'Science-fiction',
        'keyword_romance': 'Romance',
        'keyword_thriller': 'Thriller',
        'keyword_animation': 'Animation',
        'keyword_documentary': 'Documentaire',
        'keyword_fantasy': 'Fantastique',
        'keyword_crime': 'Crime',
        
        # Education keywords
        'keyword_science': 'Science',
        'keyword_technology': 'Technologie',
        'keyword_history': 'Histoire',
        'keyword_language': 'Langue',
        'keyword_math': 'Mathématiques',
        'keyword_art': 'Art',
        'keyword_cooking': 'Cuisine',
        'keyword_programming': 'Programmation',
        'keyword_business': 'Affaires',
        'keyword_health': 'Santé',
        'keyword_tutorial': 'Tutoriel',
        'keyword_lecture': 'Conférence',
        
        # News keywords
        'keyword_politics': 'Politique',
        'keyword_world_news': 'Actualités mondiales',
        'keyword_economy': 'Économie',
        'keyword_sports': 'Sports',
        'keyword_tech_news': 'Actualités technologiques',
        'keyword_entertainment_news': 'Divertissement',
        'keyword_weather': 'Météo',
        'keyword_local_news': 'Actualités locales',
        'keyword_sports_news': 'Actualités sportives',
        'keyword_technology_news': 'Actualités technologiques',
        
        # Search precision
        'search_precision_label': 'Précision de recherche:',
        'precision_standard': 'Standard（par défaut）',
        'precision_standard_desc': 'Recherche modérée＋priorité chaîne officielle',
        'precision_high': 'Haute précision',
        'precision_high_desc': 'Chaînes officielles uniquement',
        'precision_highest': 'Précision maximale',
        'precision_highest_desc': 'Recherche directe depuis liste ID chaîne',
        
        # Official channel options
        'option_official_channel': 'Priorité aux chaînes officielles',
        'option_verified_badge': 'Badge vérifié requis',
        'option_subscriber_100k': 'Abonnés: 100K+',
        'option_video_views_100k': 'Vues: 100K+',
        'option_vevo_only': 'VEVO/Officiel uniquement',
        'option_add_detailed_to_desc': 'Ajouter une description détaillée',
        
        # Privacy settings
        'privacy_private': 'Privé（vous seul pouvez voir）',
        'privacy_unlisted': 'Non répertorié（vous seul pouvez voir）',
        'privacy_public': 'Public（tout le monde peut rechercher et voir）',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Progress
        'progress_waiting': 'En attente...',
        'status_waiting': 'En attente...',
        
        # Region selection
        'region_selected': 'Sélectionné:',
        'region_none': 'Aucun',
        'region_worldwide': 'Mondial',
        
        # Regions
        'region_japan': 'Japon',
        'region_korea': 'Corée du Sud',
        'region_china': 'Chine',
        'region_taiwan': 'Taïwan',
        'region_usa': 'États-Unis',
        'region_uk': 'Royaume-Uni',
        'region_france': 'France',
        'region_germany': 'Allemagne',
        'region_spain': 'Espagne',
        'region_italy': 'Italie',
        'region_canada': 'Canada',
        'region_australia': 'Australie',
        'region_brazil': 'Brésil',
        'region_mexico': 'Mexique',
        'region_india': 'Inde',
        'region_thailand': 'Thaïlande',
        'region_vietnam': 'Vietnam',
        'region_philippines': 'Philippines',
        'region_indonesia': 'Indonésie',
        'region_singapore': 'Singapour',
        'region_russia': 'Russie',
        'region_poland': 'Pologne',
        'region_netherlands': 'Pays-Bas',
        'region_sweden': 'Suède',
        'region_norway': 'Norvège',
        'region_denmark': 'Danemark',
        'region_argentina': 'Argentine',
        'region_africa': 'Afrique',
        'region_middle_east': 'Moyen-Orient',
        'region_new_zealand': 'Nouvelle-Zélande',
        
        # Buttons
        'button_create_playlist': 'Créer une playlist',
        'button_refresh': 'Actualiser',
        'button_delete': 'Supprimer',
        'button_cancel': 'Annuler',
        'button_export': 'Exporter',
        'button_import': 'Importer',
        'button_open_url': 'Ouvrir URL',
        'button_recreate_sampler': 'Recréer échantillonneur',
        'button_video_info': 'Info vidéo',
        'button_delete_history': 'Supprimer historique',
        'button_csv_export': 'Exporter CSV',
        
        # Labels
        'label_playlist_url': 'URL de la playlist:',
        'label_created_date': 'Date de création',
        'label_title': 'Titre',
        'label_video_count': 'Nombre de vidéos',
        'label_platform': 'Plateforme',
        'label_category_short': 'Catégorie',
        'label_era_short': 'Époque',
        'label_total': 'Total',
        
        # Section headers
        'section_preset': 'Préréglage',
        'section_result': 'Résultat',
        'section_history': 'Historique',
        'section_integrated_playlists': 'Visionneuse de playlists intégrées',
        
        # Additional options
        'option_add_region_keywords': 'Ajouter mots-clés de région',
        'option_add_detailed_desc': 'Ajouter description détaillée',
        
        # Additional keyword
        'label_additional_keyword': 'Mot-clé supplémentaire',
        'additional_keyword': 'Mot-clé supplémentaire',
        'selected_keywords': 'Mots-clés sélectionnés',
        'region_keyword_auto': 'Ajouter automatiquement les mots-clés régionaux',
        
        # Buttons (complete set)
        'btn_create_playlist': 'Créer liste de lecture',
        'btn_cancel': 'Annuler',
        'btn_save': 'Enregistrer',
        'btn_copy_url': 'Copier URL',
        'btn_open': 'Ouvrir',
        'btn_refresh': 'Actualiser',
        'btn_delete': 'Supprimer',
        'btn_delete_all': 'Tout supprimer',
        'btn_export': 'Exporter',
        'btn_import': 'Importer',
        'btn_recreate_same': 'Recréer avec mêmes conditions',
        'btn_open_url': 'Ouvrir URL',
        'btn_video_confirm': 'Confirmer vidéo',
        'btn_delete_history': 'Supprimer historique',
        'btn_csv_export': 'Exporter CSV',
        'btn_create_new': 'Créer nouveau',
        'btn_json_export': 'Exporter JSON',
        'btn_html_export': 'Exporter HTML',
        'btn_edit': 'Modifier',
        
        # Column headers
        'col_created_date': 'Date de création',
        'col_title': 'Titre',
        'col_video_count': 'Nombre de vidéos',
        'col_platform': 'Plateforme',
        'col_category': 'Catégorie',
        'col_era': 'Époque',
        'col_total': 'Total',
        'col_youtube': 'YouTube',
        'col_niconico': 'Niconico',
        
        # Labels
        'label_video_range': 'Plage de vidéos',
        
        # Section headers (additional)
        'section_integrated_viewer': 'Visionneuse de listes intégrées',
        
        # Privacy descriptions
        'privacy_private_desc': 'Vous seul pouvez voir',
        'privacy_unlisted_desc': 'Vous seul pouvez voir',
        'privacy_public_desc': 'Tout le monde peut rechercher et voir',
        
        # Messages
        'message_success': 'Succès',
        'message_error': 'Erreur',
        'message_creating': 'Création...',
        'message_searching': 'Recherche...',
        
        # Setup and Auth
        'setup_wizard': 'Assistant de configuration',
        'youtube_auth': 'Authentification YouTube',
        'niconico_auth': 'Authentification Niconico',
        'check_auth_status': 'Vérifier état authentification',
        
        # Help
        'youtube_api_help': 'Aide API YouTube',
        'niconico_help': 'Aide Niconico',
        'usage_guide': 'Guide d\'utilisation',
        'troubleshooting': 'Dépannage',
    },
    
    'de': {
        # Menu bar
        'menu_file': 'Datei',
        'menu_favorites': 'Favoriten',
        'menu_settings': 'Einstellungen',
        'menu_help': 'Hilfe',
        'menu_export': 'Exportieren',
        'export_csv': 'CSV-Format',
        'export_json': 'JSON-Format',
        'export_txt': 'TXT-Format',
        'backup_create': 'Sicherung erstellen',
        'backup_restore': 'Von Sicherung wiederherstellen',
        'backup_manage': 'Sicherungen verwalten',
        'menu_exit': 'Beenden',
        'favorites_save': 'Aktuelle Einstellungen speichern',
        'favorites_load': 'Favoriten laden',
        'favorites_manage': 'Favoriten verwalten',
        'menu_language': 'Sprache',
        'update_check': 'Nach Updates suchen',
        'about': 'Über',
        
        # Main UI labels
        'label_era': 'Epoche:',
        'label_category': 'Kategorie:',
        'label_video_count': 'Anzahl der Videos:',
        
        # Sections
        'section_basic': 'Grundeinstellungen',
        'section_keywords': 'Schlüsselwörter und Region',
        'section_search_options': 'Suchoptionen',
        'section_official_channel': 'Offizielle Kanäle priorisieren:',
        'section_privacy': 'Datenschutzeinstellungen',
        'section_platform': 'Plattform',
        'section_progress': 'Fortschritt',
        
        # Tab names
        'tab_music': 'Musik',
        'tab_movies': 'Filme',
        'tab_education': 'Bildung',
        'tab_news': 'Nachrichten',
        'tab_region': 'Region',
        'tab_history': 'Verlauf',
        'tab_integrated_viewer': 'Integrierter Playlist-Viewer',
        'tab_playlist': 'Playlist-URL',
        
        # Music keywords
        'keyword_rock': 'Rock',
        'keyword_pop': 'Pop',
        'keyword_jazz': 'Jazz',
        'keyword_classical': 'Klassisch',
        'keyword_hip-hop': 'Hip-Hop',
        'keyword_edm': 'EDM',
        'keyword_metal': 'Metal',
        'keyword_country': 'Country',
        'keyword_reggae': 'Reggae',
        'keyword_electronic': 'Elektronisch',
        'keyword_blues': 'Blues',
        
        # Movie keywords
        'keyword_action': 'Action',
        'keyword_comedy': 'Komödie',
        'keyword_drama': 'Drama',
        'keyword_horror': 'Horror',
        'keyword_sci-fi': 'Science-Fiction',
        'keyword_romance': 'Romantik',
        'keyword_thriller': 'Thriller',
        'keyword_animation': 'Animation',
        'keyword_documentary': 'Dokumentation',
        'keyword_fantasy': 'Fantasy',
        'keyword_crime': 'Krimi',
        
        # Education keywords
        'keyword_science': 'Wissenschaft',
        'keyword_technology': 'Technologie',
        'keyword_history': 'Geschichte',
        'keyword_language': 'Sprache',
        'keyword_math': 'Mathematik',
        'keyword_art': 'Kunst',
        'keyword_cooking': 'Kochen',
        'keyword_programming': 'Programmierung',
        'keyword_business': 'Geschäft',
        'keyword_health': 'Gesundheit',
        'keyword_tutorial': 'Tutorial',
        'keyword_lecture': 'Vorlesung',
        
        # News keywords
        'keyword_politics': 'Politik',
        'keyword_world_news': 'Weltnachrichten',
        'keyword_economy': 'Wirtschaft',
        'keyword_sports': 'Sport',
        'keyword_tech_news': 'Technologie-Nachrichten',
        'keyword_entertainment_news': 'Unterhaltung',
        'keyword_weather': 'Wetter',
        'keyword_local_news': 'Lokale Nachrichten',
        'keyword_sports_news': 'Sport-Nachrichten',
        'keyword_technology_news': 'Technologie-Nachrichten',
        
        # Search precision
        'search_precision_label': 'Suchgenauigkeit:',
        'precision_standard': 'Standard（Standard）',
        'precision_standard_desc': 'Moderate Suche＋Priorität offizieller Kanal',
        'precision_high': 'Hohe Präzision',
        'precision_high_desc': 'Nur offizielle Kanäle',
        'precision_highest': 'Höchste Präzision',
        'precision_highest_desc': 'Direkte Suche aus Kanal-ID-Liste',
        
        # Official channel options
        'option_official_channel': 'Offizielle Kanäle priorisieren',
        'option_verified_badge': 'Verifiziertes Abzeichen erforderlich',
        'option_subscriber_100k': 'Abonnenten: 100K+',
        'option_video_views_100k': 'Aufrufe: 100K+',
        'option_vevo_only': 'Nur VEVO/Offiziell',
        'option_add_detailed_to_desc': 'Detaillierte Beschreibung hinzufügen',
        
        # Privacy settings
        'privacy_private': 'Privat（nur Sie können sehen）',
        'privacy_unlisted': 'Nicht gelistet（nur Sie können sehen）',
        'privacy_public': 'Öffentlich（jeder kann suchen und sehen）',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Progress
        'progress_waiting': 'Warten...',
        'status_waiting': 'Warten...',
        
        # Region selection
        'region_selected': 'Ausgewählt:',
        'region_none': 'Keine',
        'region_worldwide': 'Weltweit',
        
        # Regions
        'region_japan': 'Japan',
        'region_korea': 'Südkorea',
        'region_china': 'China',
        'region_taiwan': 'Taiwan',
        'region_usa': 'USA',
        'region_uk': 'Vereinigtes Königreich',
        'region_france': 'Frankreich',
        'region_germany': 'Deutschland',
        'region_spain': 'Spanien',
        'region_italy': 'Italien',
        'region_canada': 'Kanada',
        'region_australia': 'Australien',
        'region_brazil': 'Brasilien',
        'region_mexico': 'Mexiko',
        'region_india': 'Indien',
        'region_thailand': 'Thailand',
        'region_vietnam': 'Vietnam',
        'region_philippines': 'Philippinen',
        'region_indonesia': 'Indonesien',
        'region_singapore': 'Singapur',
        'region_russia': 'Russland',
        'region_poland': 'Polen',
        'region_netherlands': 'Niederlande',
        'region_sweden': 'Schweden',
        'region_norway': 'Norwegen',
        'region_denmark': 'Dänemark',
        'region_argentina': 'Argentinien',
        'region_africa': 'Afrika',
        'region_middle_east': 'Naher Osten',
        'region_new_zealand': 'Neuseeland',
        
        # Buttons
        'button_create_playlist': 'Playlist erstellen',
        'button_refresh': 'Aktualisieren',
        'button_delete': 'Löschen',
        'button_cancel': 'Abbrechen',
        'button_export': 'Exportieren',
        'button_import': 'Importieren',
        'button_open_url': 'URL öffnen',
        'button_recreate_sampler': 'Sampler neu erstellen',
        'button_video_info': 'Videoinfo',
        'button_delete_history': 'Verlauf löschen',
        'button_csv_export': 'CSV exportieren',
        
        # Labels
        'label_playlist_url': 'Playlist-URL:',
        'label_created_date': 'Erstellungsdatum',
        'label_title': 'Titel',
        'label_video_count': 'Anzahl der Videos',
        'label_platform': 'Plattform',
        'label_category_short': 'Kategorie',
        'label_era_short': 'Epoche',
        'label_total': 'Gesamt',
        
        # Section headers
        'section_preset': 'Voreinstellung',
        'section_result': 'Ergebnis',
        'section_history': 'Verlauf',
        'section_integrated_playlists': 'Integrierter Playlist-Viewer',
        
        # Additional options
        'option_add_region_keywords': 'Regions-Schlüsselwörter hinzufügen',
        'option_add_detailed_desc': 'Detaillierte Beschreibung hinzufügen',
        
        # Additional keyword
        'label_additional_keyword': 'Zusätzliches Schlüsselwort',
        'additional_keyword': 'Zusätzliches Schlüsselwort',
        'selected_keywords': 'Ausgewählte Schlüsselwörter',
        'region_keyword_auto': 'Regions-Schlüsselwörter automatisch hinzufügen',
        
        # Buttons (complete set)
        'btn_create_playlist': 'Playlist erstellen',
        'btn_cancel': 'Abbrechen',
        'btn_save': 'Speichern',
        'btn_copy_url': 'URL kopieren',
        'btn_open': 'Öffnen',
        'btn_refresh': 'Aktualisieren',
        'btn_delete': 'Löschen',
        'btn_delete_all': 'Alle löschen',
        'btn_export': 'Exportieren',
        'btn_import': 'Importieren',
        'btn_recreate_same': 'Mit gleichen Bedingungen neu erstellen',
        'btn_open_url': 'URL öffnen',
        'btn_video_confirm': 'Video bestätigen',
        'btn_delete_history': 'Verlauf löschen',
        'btn_csv_export': 'CSV exportieren',
        'btn_create_new': 'Neu erstellen',
        'btn_json_export': 'JSON exportieren',
        'btn_html_export': 'HTML exportieren',
        'btn_edit': 'Bearbeiten',
        
        # Column headers
        'col_created_date': 'Erstellungsdatum',
        'col_title': 'Titel',
        'col_video_count': 'Anzahl der Videos',
        'col_platform': 'Plattform',
        'col_category': 'Kategorie',
        'col_era': 'Epoche',
        'col_total': 'Gesamt',
        'col_youtube': 'YouTube',
        'col_niconico': 'Niconico',
        
        # Labels
        'label_video_range': 'Video-Bereich',
        
        # Section headers (additional)
        'section_integrated_viewer': 'Integrierter Playlist-Viewer',
        
        # Privacy descriptions
        'privacy_private_desc': 'Nur Sie können sehen',
        'privacy_unlisted_desc': 'Nur Sie können sehen',
        'privacy_public_desc': 'Jeder kann suchen und sehen',
        
        # Messages
        'message_success': 'Erfolg',
        'message_error': 'Fehler',
        'message_creating': 'Erstellen...',
        'message_searching': 'Suchen...',
        
        # Setup and Auth
        'setup_wizard': 'Einrichtungsassistent',
        'youtube_auth': 'YouTube-Authentifizierung',
        'niconico_auth': 'Niconico-Authentifizierung',
        'check_auth_status': 'Authentifizierungsstatus prüfen',
        
        # Help
        'youtube_api_help': 'YouTube-API-Hilfe',
        'niconico_help': 'Niconico-Hilfe',
        'usage_guide': 'Benutzerhandbuch',
        'troubleshooting': 'Fehlerbehebung',
    },
}

def get_available_languages():
    """利用可能な言語のリストを取得"""
    return list(TRANSLATIONS.keys())


# ========================================
# 言語管理機能
# ========================================

# 現在の言語（グローバル変数）
_current_language = 'ja'


def set_language(language_code: str) -> bool:
    """言語を設定する
    
    Args:
        language_code: 言語コード ('ja', 'en', 'zh-CN', 'zh-TW', 'ko', 'es', 'fr', 'de')
    
    Returns:
        設定に成功した場合True
    """
    global _current_language
    if language_code in TRANSLATIONS:
        _current_language = language_code
        return True
    return False


def get_current_language() -> str:
    """現在の言語コードを取得する
    
    Returns:
        現在の言語コード
    """
    return _current_language


def t(key: str, default: str = None) -> str:
    """翻訳テキストを取得する
    
    Args:
        key: 翻訳キー
        default: キーが見つからない場合のデフォルト値
    
    Returns:
        翻訳されたテキスト
    """
    lang = get_current_language()
    if lang in TRANSLATIONS:
        return TRANSLATIONS[lang].get(key, default or key)
    return default or key


def t_keyword(keyword: str) -> str:
    """キーワードの翻訳を取得する（便利関数）
    
    Args:
        keyword: キーワード（例: 'rock', 'hip-hop'）
    
    Returns:
        翻訳されたキーワード
    """
    if keyword.startswith('keyword_'):
        return t(keyword)
    return t(f'keyword_{keyword}')


def t_region(region: str) -> str:
    """地域名の翻訳を取得する（便利関数）
    
    Args:
        region: 地域コード（例: 'japan', 'worldwide'）
    
    Returns:
        翻訳された地域名
    """
    if region.startswith('region_'):
        return t(region)
    return t(f'region_{region}')
