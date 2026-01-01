# -*- coding: utf-8 -*-
"""
Multi-language translation system for YouTube Playlist Manager
Supports: Japanese, English, Chinese (Simplified & Traditional), Korean, Spanish, French, German
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
        
        # News keywords
        'keyword_politics': '政治',
        'keyword_world_news': '国際ニュース',
        'keyword_economy': '経済',
        'keyword_sports': 'スポーツ',
        'keyword_tech_news': 'IT・技術',
        'keyword_entertainment_news': '芸能',
        'keyword_weather': '天気',
        'keyword_local_news': '地域ニュース',
        
        # Search precision
        'search_precision_label': '検索精度:',
        'precision_standard': '標準（デフォルト）',
        'precision_standard_desc': '適度な検索＋公式チャンネル優先',
        'precision_high': '高精度',
        'precision_high_desc': '全録画が公式チャンネルのみ',
        'precision_highest': '最高精度',
        'precision_highest_desc': 'チャンネルIDリストから直接検索',
        
        # Official channel options
        'option_official_channel': '公式チャンネル優先',
        'option_verified_badge': '認証済みバッジ必須',
        'option_subscriber_100k': 'チャンネル登録者数: 100万人以上',
        'option_video_views_100k': '再生回数: 100万回以上',
        'option_vevo_only': 'VEVO/公式のみ',
        'option_add_detailed_to_weak': '詳細な説明を追加',
        
        # Privacy settings
        'privacy_unlisted': '非公開（自分のみ閲覧可能）',
        'privacy_unlisted_url': '限定公開（URLを知っている人のみ閲覧可能）',
        'privacy_public': '公開（誰でも検索・閲覧可能）',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'ニコニコ動画',
        
        # Progress
        'progress_waiting': '待機中...',
        'status_waiting': '待機中...',
        
        # Region selection
        'region_selected': '選択中:',

        # UI Section labels
        'section_preset': 'プリセット',
        'section_result': '結果',
        
        # Additional labels
        'label_preset': 'プリセット:',
        
        # Buttons
        'btn_load': '読み込み',
        'btn_save': '保存',
        'btn_edit': '編集',
        
        # Privacy descriptions
        'privacy_private_desc': '自分のみ閲覧可能',
        'privacy_unlisted_desc': '自分のみ閲覧可能',
        'privacy_public_desc': '誰でも検索・閲覧可能',
        
        # Additional options
        'option_add_detailed_desc': '詳細な説明を追加',
        # Setup and Auth menu items
        'setup_wizard': 'セットアップウィザード',
        'youtube_auth': 'YouTube認証',
        'niconico_auth': 'ニコニコ動画認証',
        'check_auth_status': '認証状態を確認',
        
        # History menu items
        'export_history': '履歴をエクスポート',
        'import_history': '履歴をインポート',
        
        # Help menu items
        'youtube_api_help': 'YouTube API ヘルプ',
        'niconico_help': 'ニコニコ動画ヘルプ',
        'usage_guide': '使い方ガイド',
        'troubleshooting': 'トラブルシューティング',
        
        # Education keywords - additional
        'keyword_lecture': '講義',
        'keyword_tutorial': 'チュートリアル',
        
        # News keywords - additional  
        'keyword_world_news': '国際ニュース',
        'keyword_sports_news': 'スポーツニュース',
        'keyword_technology_news': 'IT・技術ニュース',
        'option_add_region_keywords': '地域キーワードを自動追加',
        'region_code_none': '(regionCode: なし)',
        
        # Additional keywords
        'label_additional_keywords': '追加キーワード:',
        'additional_keyword': '追加キーワード',
        'label_playlist_url': 'プレイリスト URL:',
        'label_progress': '進行状況',
        
        # Buttons
        'btn_create_playlist': '再生リスト作成',
        'btn_refresh': '更新',
        'btn_delete_all': '全削除',
        'btn_export': 'エクスポート',
        'btn_import': 'インポート',
        'btn_recreate_same': '同条件で再作成',
        'btn_open_url': 'URLを開く',
        'btn_video_confirm': '動画確認',
        'btn_delete_history': '履歴を削除',
        'btn_csv_export': 'CSV出力',
        'btn_create_new': '新規作成',
        'btn_json_export': 'JSON出力',
        'btn_html_export': 'HTML出力',
        'btn_delete': '削除',
        'btn_ok': 'OK',
        'btn_cancel': 'キャンセル',
        'btn_close': '閉じる',
        
        # Table columns
        'col_created_date': '作成日時',
        'col_title': 'タイトル',
        'col_video_count': '動画数',
        'col_platform': 'Platform',
        'col_category': 'カテゴリ',
        'col_era': '年代',
        'col_total': '合計',
        'col_youtube': 'YouTube',
        'col_niconico': 'ニコニコ',
        
        # Messages
        'language_changed': '言語を変更しました',
        'selected_keywords': '選択されたキーワード',
        'section_history': '履歴',
        'section_integrated_viewer': '統合プレイリストビューワー',
        
        # Region names
        'region_worldwide': '全世界',
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
        'region_brazil': 'ブラジル',
        'region_mexico': 'メキシコ',
        'region_canada': 'カナダ',
        'region_australia': 'オーストラリア',
        'region_india': 'インド',
        'region_russia': 'ロシア',
        'region_asia': 'アジア',
        'region_europe': 'ヨーロッパ',
        'region_americas': '北米・南米',
        'region_others': 'その他'
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
        'export_txt': 'Text Format',
        'backup_create': 'Create Backup',
        'backup_restore': 'Restore from Backup',
        'backup_manage': 'Manage Backups',
        'menu_exit': 'Exit',
        'favorites_save': 'Save Current Settings',
        'favorites_load': 'Load Favorite',
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
        'section_keywords': 'Keywords & Region',
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
        'tab_playlist': 'Playlist',
        
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
        
        # News keywords
        'keyword_politics': 'Politics',
        'keyword_world_news': 'World News',
        'keyword_economy': 'Economy',
        'keyword_sports': 'Sports',
        'keyword_tech_news': 'Tech News',
        'keyword_entertainment_news': 'Entertainment',
        'keyword_weather': 'Weather',
        'keyword_local_news': 'Local News',
        
        # Search precision
        'search_precision_label': 'Search Precision:',
        'precision_standard': 'Standard (Default)',
        'precision_standard_desc': 'Moderate search + Official channel priority',
        'precision_high': 'High Precision',
        'precision_high_desc': 'Official channels only',
        'precision_highest': 'Highest Precision',
        'precision_highest_desc': 'Direct search from channel ID list',
        
        # Official channel options
        'option_official_channel': 'Official Channel Priority',
        'option_verified_badge': 'Verified Badge Required',
        'option_subscriber_100k': 'Subscribers: 1M+',
        'option_video_views_100k': 'Views: 1M+',
        'option_vevo_only': 'VEVO/Official Only',
        'option_add_detailed_to_weak': 'Add Detailed Description',
        
        # Privacy settings
        'privacy_unlisted': 'Private (Only you can view)',
        'privacy_unlisted_url': 'Unlisted (Anyone with link can view)',
        'privacy_public': 'Public (Anyone can search & view)',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Progress
        'progress_waiting': 'Waiting...',
        'status_waiting': 'Waiting...',
        
        # Region selection
        'region_selected': 'Selected:',

        # UI Section labels
        'section_preset': 'Preset',
        'section_result': 'Result',
        
        # Additional labels
        'label_preset': 'Preset:',
        
        # Buttons
        'btn_load': 'Load',
        'btn_save': 'Save',
        'btn_edit': 'Edit',
        
        # Privacy descriptions
        'privacy_private_desc': 'Only you can view',
        'privacy_unlisted_desc': 'Only you can view',
        'privacy_public_desc': 'Anyone can search and view',
        
        # Additional options
        'option_add_detailed_desc': 'Add detailed description',
        # Setup and Auth menu items
        'setup_wizard': 'Setup Wizard',
        'youtube_auth': 'YouTube Authentication',
        'niconico_auth': 'Niconico Authentication',
        'check_auth_status': 'Check Auth Status',
        
        # History menu items
        'export_history': 'Export History',
        'import_history': 'Import History',
        
        # Help menu items
        'youtube_api_help': 'YouTube API Help',
        'niconico_help': 'Niconico Help',
        'usage_guide': 'Usage Guide',
        'troubleshooting': 'Troubleshooting',
        
        # Education keywords - additional
        'keyword_lecture': 'Lecture',
        'keyword_tutorial': 'Tutorial',
        
        # News keywords - additional
        'keyword_world_news': 'World News',
        'keyword_sports_news': 'Sports News',
        'keyword_technology_news': 'Technology News',
        'option_add_region_keywords': 'Auto-add region keywords',
        'region_code_none': '(regionCode: None)',
        
        # Additional keywords
        'label_additional_keywords': 'Additional Keywords:',
        'additional_keyword': 'Additional Keywords',
        'label_playlist_url': 'Playlist URL:',
        'label_progress': 'Progress',
        
        # Buttons
        'btn_create_playlist': 'Create Playlist',
        'btn_refresh': 'Refresh',
        'btn_delete_all': 'Delete All',
        'btn_export': 'Export',
        'btn_import': 'Import',
        'btn_recreate_same': 'Recreate with Same Settings',
        'btn_open_url': 'Open URL',
        'btn_video_confirm': 'Video Confirmation',
        'btn_delete_history': 'Delete History',
        'btn_csv_export': 'Export CSV',
        'btn_create_new': 'Create New',
        'btn_json_export': 'Export JSON',
        'btn_html_export': 'Export HTML',
        'btn_delete': 'Delete',
        'btn_ok': 'OK',
        'btn_cancel': 'Cancel',
        'btn_close': 'Close',
        
        # Table columns
        'col_created_date': 'Created',
        'col_title': 'Title',
        'col_video_count': 'Videos',
        'col_platform': 'Platform',
        'col_category': 'Category',
        'col_era': 'Era',
        'col_total': 'Total',
        'col_youtube': 'YouTube',
        'col_niconico': 'Niconico',
        
        # Messages
        'language_changed': 'Language changed',
        'selected_keywords': 'Selected Keywords',
        'section_history': 'History',
        'section_integrated_viewer': 'Integrated Playlist Viewer',
        
        # Region names
        'region_worldwide': 'Worldwide',
        'region_japan': 'Japan',
        'region_korea': 'Korea',
        'region_china': 'China',
        'region_taiwan': 'Taiwan',
        'region_usa': 'USA',
        'region_uk': 'UK',
        'region_france': 'France',
        'region_germany': 'Germany',
        'region_spain': 'Spain',
        'region_italy': 'Italy',
        'region_brazil': 'Brazil',
        'region_mexico': 'Mexico',
        'region_canada': 'Canada',
        'region_australia': 'Australia',
        'region_india': 'India',
        'region_russia': 'Russia',
        'region_asia': 'Asia',
        'region_europe': 'Europe',
        'region_americas': 'Americas',
        'region_others': 'Others'
    },
    'zh-CN': {
        # Menu bar
        'menu_file': '文件',
        'menu_favorites': '收藏夹',
        'menu_settings': '设置',
        'menu_help': '帮助',
        'menu_export': '导出',
        'export_csv': 'CSV格式',
        'export_json': 'JSON格式',
        'export_txt': '文本格式',
        'backup_create': '创建备份',
        'backup_restore': '从备份还原',
        'backup_manage': '管理备份',
        'menu_exit': '退出',
        'favorites_save': '保存当前设置',
        'favorites_load': '加载收藏',
        'favorites_manage': '管理收藏',
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
        'section_official_channel': '官方频道优先:',
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
        'tab_integrated_viewer': '整合播放列表查看器',
        'tab_playlist': '播放列表',
        
        # Music keywords
        'keyword_rock': '摇滚',
        'keyword_pop': '流行',
        'keyword_jazz': '爵士',
        'keyword_classical': '古典',
        'keyword_hip-hop': '嘻哈',
        'keyword_edm': '电子舞曲',
        'keyword_metal': '金属',
        'keyword_country': '乡村',
        'keyword_reggae': '雷鬼',
        'keyword_electronic': '电子',
        'keyword_blues': '布鲁斯',
        
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
        
        # News keywords
        'keyword_politics': '政治',
        'keyword_world_news': '国际新闻',
        'keyword_economy': '经济',
        'keyword_sports': '体育',
        'keyword_tech_news': '科技新闻',
        'keyword_entertainment_news': '娱乐',
        'keyword_weather': '天气',
        'keyword_local_news': '本地新闻',
        
        # Search precision
        'search_precision_label': '搜索精度:',
        'precision_standard': '标准（默认）',
        'precision_standard_desc': '适度搜索 + 官方频道优先',
        'precision_high': '高精度',
        'precision_high_desc': '仅官方频道',
        'precision_highest': '最高精度',
        'precision_highest_desc': '从频道ID列表直接搜索',
        
        # Official channel options
        'option_official_channel': '官方频道优先',
        'option_verified_badge': '需要认证徽章',
        'option_subscriber_100k': '订阅者: 100万+',
        'option_video_views_100k': '观看次数: 100万+',
        'option_vevo_only': '仅VEVO/官方',
        'option_add_detailed_to_weak': '添加详细说明',
        
        # Privacy settings
        'privacy_unlisted': '私人（仅您可以查看）',
        'privacy_unlisted_url': '不公开（知道链接的人可以查看）',
        'privacy_public': '公开（任何人都可以搜索和查看）',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Progress
        'progress_waiting': '等待中...',
        'status_waiting': '等待中...',
        
        # Region selection
        'region_selected': '已选择:',

        # UI Section labels
        'section_preset': '预设',
        'section_result': '结果',
        
        # Additional labels
        'label_preset': '预设:',
        
        # Buttons
        'btn_load': '加载',
        'btn_save': '保存',
        'btn_edit': '编辑',
        
        # Privacy descriptions
        'privacy_private_desc': '仅自己可见',
        'privacy_unlisted_desc': '仅自己可见',
        'privacy_public_desc': '任何人都可以搜索和查看',
        
        # Additional options
        'option_add_detailed_desc': '添加详细说明',
        # Setup and Auth menu items
        'setup_wizard': '设置向导',
        'youtube_auth': 'YouTube认证',
        'niconico_auth': 'Niconico认证',
        'check_auth_status': '检查认证状态',
        
        # History menu items
        'export_history': '导出历史',
        'import_history': '导入历史',
        
        # Help menu items
        'youtube_api_help': 'YouTube API帮助',
        'niconico_help': 'Niconico帮助',
        'usage_guide': '使用指南',
        'troubleshooting': '故障排除',
        
        # Education keywords - additional
        'keyword_lecture': '讲座',
        'keyword_tutorial': '教程',
        
        # News keywords - additional
        'keyword_world_news': '国际新闻',
        'keyword_sports_news': '体育新闻',
        'keyword_technology_news': '科技新闻',
        'option_add_region_keywords': '自动添加地区关键字',
        'region_code_none': '(regionCode: 无)',
        
        # Additional keywords
        'label_additional_keywords': '附加关键字:',
        'additional_keyword': '附加关键字',
        'label_playlist_url': '播放列表 URL:',
        'label_progress': '进度',
        
        # Buttons
        'btn_create_playlist': '创建播放列表',
        'btn_refresh': '刷新',
        'btn_delete_all': '全部删除',
        'btn_export': '导出',
        'btn_import': '导入',
        'btn_recreate_same': '使用相同设置重新创建',
        'btn_open_url': '打开 URL',
        'btn_video_confirm': '视频确认',
        'btn_delete_history': '删除历史记录',
        'btn_csv_export': '导出 CSV',
        'btn_create_new': '新建',
        'btn_json_export': '导出 JSON',
        'btn_html_export': '导出 HTML',
        'btn_delete': '删除',
        'btn_ok': '确定',
        'btn_cancel': '取消',
        'btn_close': '关闭',
        
        # Table columns
        'col_created_date': '创建日期',
        'col_title': '标题',
        'col_video_count': '视频',
        'col_platform': '平台',
        'col_category': '类别',
        'col_era': '年代',
        'col_total': '总计',
        'col_youtube': 'YouTube',
        'col_niconico': 'Niconico',
        
        # Messages
        'language_changed': '语言已更改',
        'selected_keywords': '选择的关键字',
        'section_history': '历史记录',
        'section_integrated_viewer': '整合播放列表查看器',
        
        # Region names
        'region_worldwide': '全球',
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
        'region_brazil': '巴西',
        'region_mexico': '墨西哥',
        'region_canada': '加拿大',
        'region_australia': '澳洲',
        'region_india': '印度',
        'region_russia': '俄罗斯',
        'region_asia': '亚洲',
        'region_europe': '欧洲',
        'region_americas': '美洲',
        'region_others': '其他'
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
        'favorites_manage': '管理我的最愛',
        'menu_language': '語言',
        'update_check': '檢查更新',
        'about': '版本資訊',
        
        # Main UI labels
        'label_era': '年代:',
        'label_category': '類別:',
        'label_video_count': '影片數量:',
        
        # Sections
        'section_basic': '基本設定',
        'section_keywords': '關鍵字・地區',
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
        'tab_integrated_viewer': '整合播放清單檢視器',
        'tab_playlist': '影片播放清單',
        
        # Music keywords
        'keyword_rock': '搖滾',
        'keyword_pop': '流行',
        'keyword_jazz': '爵士',
        'keyword_classical': '古典',
        'keyword_hip-hop': '嘻哈',
        'keyword_electronic': '電子',
        'keyword_metal': '金屬',
        'keyword_country': '鄉村',
        'keyword_reggae': '雷鬼',
        'keyword_blues': '藍調',
        
        # Movie keywords
        'keyword_action': '動作',
        'keyword_comedy': '喜劇',
        'keyword_drama': '劇情',
        'keyword_horror': '恐怖',
        'keyword_sci-fi': '科幻',
        'keyword_animation': '動畫',
        'keyword_documentary': '紀錄片',
        'keyword_thriller': '驚悚',
        
        # Education keywords
        'keyword_science': '科學',
        'keyword_technology': '技術',
        'keyword_history': '歷史',
        'keyword_math': '數學',
        'keyword_language': '語言',
        
        # News keywords
        'keyword_politics': '政治',
        'keyword_world_news': '國際新聞',
        'keyword_economy': '經濟',
        'keyword_sports': '體育',
        
        # Regions
        'region_selected': '已選擇:',

        # UI Section labels
        'section_preset': '預設',
        'section_result': '結果',
        
        # Additional labels
        'label_preset': '預設:',
        
        # Buttons
        'btn_load': '載入',
        'btn_save': '儲存',
        'btn_edit': '編輯',
        
        # Privacy descriptions
        'privacy_private_desc': '僅自己可見',
        'privacy_unlisted_desc': '僅自己可見',
        'privacy_public_desc': '任何人都可以搜尋和檢視',
        
        # Additional options
        'option_add_detailed_desc': '新增詳細說明',
        # Setup and Auth menu items
        'setup_wizard': '設定精靈',
        'youtube_auth': 'YouTube驗證',
        'niconico_auth': 'Niconico驗證',
        'check_auth_status': '檢查驗證狀態',
        
        # History menu items
        'export_history': '匯出歷史',
        'import_history': '匯入歷史',
        
        # Help menu items
        'youtube_api_help': 'YouTube API說明',
        'niconico_help': 'Niconico說明',
        'usage_guide': '使用指南',
        'troubleshooting': '疑難排解',
        
        # Education keywords - additional
        'keyword_lecture': '講座',
        'keyword_tutorial': '教學',
        
        # News keywords - additional
        'keyword_world_news': '國際新聞',
        'keyword_sports_news': '體育新聞',
        'keyword_technology_news': '科技新聞',
        'region_japan': '日本',
        'region_korea': '韓國',
        'region_china': '中國',
        'region_usa': '美國',
        'region_uk': '英國',
        'region_france': '法國',
        'region_germany': '德國',
        
        # Buttons
        'button_create': '建立播放清單',
        'button_search': '搜尋',
        'button_cancel': '取消',
        'button_save': '儲存',
        'button_delete': '刪除',
        'button_close': '關閉',
        
        # Messages
        'message_success': '成功',
        'message_error': '錯誤',
        'message_creating': '建立中...',
        'message_searching': '搜尋中...',
        
        # Privacy
        'privacy_private': '私人',
        'privacy_unlisted': '不公開',
        'privacy_public': '公開',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Search precision
        'precision_standard': '標準',
        'precision_high': '高精度',
        'precision_highest': '最高精度',
        
        # Status
        'status_ready': '就緒',
        'status_authenticated': '已驗證',
        'setup_wizard': '設定精靈',
        'youtube_auth': 'YouTube驗證',
        'niconico_auth': 'Niconico驗證',
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
        'backup_create': '백업 생성',
        'backup_restore': '백업에서 복원',
        'backup_manage': '백업 관리',
        'menu_exit': '종료',
        'favorites_save': '현재 설정 저장',
        'favorites_load': '즐겨찾기 불러오기',
        'favorites_manage': '즐겨찾기 관리',
        'menu_language': '언어',
        'update_check': '업데이트 확인',
        'about': '버전 정보',
        
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
        'tab_playlist': '동영상 재생목록',
        
        # Music keywords
        'keyword_rock': '록',
        'keyword_pop': '팝',
        'keyword_jazz': '재즈',
        'keyword_classical': '클래식',
        'keyword_hip-hop': '힙합',
        'keyword_electronic': '일렉트로닉',
        'keyword_metal': '메탈',
        'keyword_country': '컨트리',
        'keyword_reggae': '레게',
        'keyword_blues': '블루스',
        
        # Movie keywords
        'keyword_action': '액션',
        'keyword_comedy': '코미디',
        'keyword_drama': '드라마',
        'keyword_horror': '공포',
        'keyword_sci-fi': 'SF',
        'keyword_animation': '애니메이션',
        'keyword_documentary': '다큐멘터리',
        'keyword_thriller': '스릴러',
        
        # Education keywords
        'keyword_science': '과학',
        'keyword_technology': '기술',
        'keyword_history': '역사',
        'keyword_math': '수학',
        'keyword_language': '언어',
        
        # News keywords
        'keyword_politics': '정치',
        'keyword_world_news': '국제 뉴스',
        'keyword_economy': '경제',
        'keyword_sports': '스포츠',
        
        # Regions
        'region_selected': '선택됨:',

        # UI Section labels
        'section_preset': '프리셋',
        'section_result': '결과',
        
        # Additional labels
        'label_preset': '프리셋:',
        
        # Buttons
        'btn_load': '불러오기',
        'btn_save': '저장',
        'btn_edit': '편집',
        
        # Privacy descriptions
        'privacy_private_desc': '본인만 볼 수 있음',
        'privacy_unlisted_desc': '본인만 볼 수 있음',
        'privacy_public_desc': '누구나 검색하고 볼 수 있음',
        
        # Additional options
        'option_add_detailed_desc': '상세 설명 추가',
        # Setup and Auth menu items
        'setup_wizard': '설정 마법사',
        'youtube_auth': 'YouTube 인증',
        'niconico_auth': 'Niconico 인증',
        'check_auth_status': '인증 상태 확인',
        
        # History menu items
        'export_history': '기록 내보내기',
        'import_history': '기록 가져오기',
        
        # Help menu items
        'youtube_api_help': 'YouTube API 도움말',
        'niconico_help': 'Niconico 도움말',
        'usage_guide': '사용 가이드',
        'troubleshooting': '문제 해결',
        
        # Education keywords - additional
        'keyword_lecture': '강의',
        'keyword_tutorial': '튜토리얼',
        
        # News keywords - additional
        'keyword_world_news': '국제 뉴스',
        'keyword_sports_news': '스포츠 뉴스',
        'keyword_technology_news': '기술 뉴스',
        'region_japan': '일본',
        'region_korea': '한국',
        'region_china': '중국',
        'region_usa': '미국',
        'region_uk': '영국',
        'region_france': '프랑스',
        'region_germany': '독일',
        
        # Buttons
        'button_create': '재생목록 생성',
        'button_search': '검색',
        'button_cancel': '취소',
        'button_save': '저장',
        'button_delete': '삭제',
        'button_close': '닫기',
        
        # Messages
        'message_success': '성공',
        'message_error': '오류',
        'message_creating': '생성 중...',
        'message_searching': '검색 중...',
        
        # Privacy
        'privacy_private': '비공개',
        'privacy_unlisted': '일부 공개',
        'privacy_public': '공개',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Search precision
        'precision_standard': '표준',
        'precision_high': '고정밀',
        'precision_highest': '최고정밀',
        
        # Status
        'status_ready': '준비',
        'status_authenticated': '인증됨',
        'setup_wizard': '설정 마법사',
        'youtube_auth': 'YouTube 인증',
        'niconico_auth': 'Niconico 인증',
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
        'tab_playlist': 'Lista de reproducción',
        
        # Music keywords
        'keyword_rock': 'Rock',
        'keyword_pop': 'Pop',
        'keyword_jazz': 'Jazz',
        'keyword_classical': 'Clásica',
        'keyword_hip-hop': 'Hip-Hop',
        'keyword_electronic': 'Electrónica',
        'keyword_metal': 'Metal',
        'keyword_country': 'Country',
        'keyword_reggae': 'Reggae',
        'keyword_blues': 'Blues',
        
        # Movie keywords
        'keyword_action': 'Acción',
        'keyword_comedy': 'Comedia',
        'keyword_drama': 'Drama',
        'keyword_horror': 'Terror',
        'keyword_sci-fi': 'Ciencia ficción',
        'keyword_animation': 'Animación',
        'keyword_documentary': 'Documental',
        'keyword_thriller': 'Suspense',
        
        # Education keywords
        'keyword_science': 'Ciencia',
        'keyword_technology': 'Tecnología',
        'keyword_history': 'Historia',
        'keyword_math': 'Matemáticas',
        'keyword_language': 'Idiomas',
        
        # News keywords
        'keyword_politics': 'Política',
        'keyword_world_news': 'Noticias internacionales',
        'keyword_economy': 'Economía',
        'keyword_sports': 'Deportes',
        
        # Regions
        'region_selected': 'Seleccionado:',

        # UI Section labels
        'section_preset': 'Preajuste',
        'section_result': 'Resultado',
        
        # Additional labels
        'label_preset': 'Preajuste:',
        
        # Buttons
        'btn_load': 'Cargar',
        'btn_save': 'Guardar',
        'btn_edit': 'Editar',
        
        # Privacy descriptions
        'privacy_private_desc': 'Solo tú puedes ver',
        'privacy_unlisted_desc': 'Solo tú puedes ver',
        'privacy_public_desc': 'Cualquiera puede buscar y ver',
        
        # Additional options
        'option_add_detailed_desc': 'Agregar descripción detallada',
        # Setup and Auth menu items
        'setup_wizard': 'Asistente de configuración',
        'youtube_auth': 'Autenticación de YouTube',
        'niconico_auth': 'Autenticación de Niconico',
        'check_auth_status': 'Verificar estado de autenticación',
        
        # History menu items
        'export_history': 'Exportar historial',
        'import_history': 'Importar historial',
        
        # Help menu items
        'youtube_api_help': 'Ayuda de API de YouTube',
        'niconico_help': 'Ayuda de Niconico',
        'usage_guide': 'Guía de uso',
        'troubleshooting': 'Solución de problemas',
        
        # Education keywords - additional
        'keyword_lecture': 'Conferencia',
        'keyword_tutorial': 'Tutorial',
        
        # News keywords - additional
        'keyword_world_news': 'Noticias mundiales',
        'keyword_sports_news': 'Noticias deportivas',
        'keyword_technology_news': 'Noticias tecnológicas',
        'region_japan': 'Japón',
        'region_korea': 'Corea',
        'region_china': 'China',
        'region_usa': 'EE.UU.',
        'region_uk': 'Reino Unido',
        'region_france': 'Francia',
        'region_germany': 'Alemania',
        
        # Buttons
        'button_create': 'Crear lista',
        'button_search': 'Buscar',
        'button_cancel': 'Cancelar',
        'button_save': 'Guardar',
        'button_delete': 'Eliminar',
        'button_close': 'Cerrar',
        
        # Messages
        'message_success': 'Éxito',
        'message_error': 'Error',
        'message_creating': 'Creando...',
        'message_searching': 'Buscando...',
        
        # Privacy
        'privacy_private': 'Privado',
        'privacy_unlisted': 'No listado',
        'privacy_public': 'Público',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Search precision
        'precision_standard': 'Estándar',
        'precision_high': 'Alta precisión',
        'precision_highest': 'Máxima precisión',
        
        # Status
        'status_ready': 'Listo',
        'status_authenticated': 'Autenticado',
        'setup_wizard': 'Asistente de configuración',
        'youtube_auth': 'Autenticación YouTube',
        'niconico_auth': 'Autenticación Niconico',
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
        'backup_restore': 'Restaurer la sauvegarde',
        'backup_manage': 'Gérer les sauvegardes',
        'menu_exit': 'Quitter',
        'favorites_save': 'Sauvegarder la configuration',
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
        'section_basic': 'Configuration de base',
        'section_keywords': 'Mots-clés et région',
        'section_search_options': 'Options de recherche',
        'section_official_channel': 'Prioriser les chaînes officielles:',
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
        'tab_playlist': 'Playlist vidéo',
        
        # Music keywords
        'keyword_rock': 'Rock',
        'keyword_pop': 'Pop',
        'keyword_jazz': 'Jazz',
        'keyword_classical': 'Classique',
        'keyword_hip-hop': 'Hip-Hop',
        'keyword_electronic': 'Électronique',
        'keyword_metal': 'Metal',
        'keyword_country': 'Country',
        'keyword_reggae': 'Reggae',
        'keyword_blues': 'Blues',
        
        # Movie keywords
        'keyword_action': 'Action',
        'keyword_comedy': 'Comédie',
        'keyword_drama': 'Drame',
        'keyword_horror': 'Horreur',
        'keyword_sci-fi': 'Science-fiction',
        'keyword_animation': 'Animation',
        'keyword_documentary': 'Documentaire',
        'keyword_thriller': 'Thriller',
        
        # Education keywords
        'keyword_science': 'Science',
        'keyword_technology': 'Technologie',
        'keyword_history': 'Histoire',
        'keyword_math': 'Mathématiques',
        'keyword_language': 'Langues',
        
        # News keywords
        'keyword_politics': 'Politique',
        'keyword_world_news': 'Actualités internationales',
        'keyword_economy': 'Économie',
        'keyword_sports': 'Sports',
        
        # Regions
        'region_selected': 'Sélectionné:',

        # UI Section labels
        'section_preset': 'Préréglage',
        'section_result': 'Résultat',
        
        # Additional labels
        'label_preset': 'Préréglage:',
        
        # Buttons
        'btn_load': 'Charger',
        'btn_save': 'Enregistrer',
        'btn_edit': 'Modifier',
        
        # Privacy descriptions
        'privacy_private_desc': 'Vous seul pouvez voir',
        'privacy_unlisted_desc': 'Vous seul pouvez voir',
        'privacy_public_desc': 'Tout le monde peut rechercher et voir',
        
        # Additional options
        'option_add_detailed_desc': 'Ajouter une description détaillée',
        # Setup and Auth menu items
        'setup_wizard': 'Assistant de configuration',
        'youtube_auth': 'Authentification YouTube',
        'niconico_auth': 'Authentification Niconico',
        'check_auth_status': "Vérifier l'état d'authentification",
        
        # History menu items
        'export_history': "Exporter l'historique",
        'import_history': "Importer l'historique",
        
        # Help menu items
        'youtube_api_help': 'Aide API YouTube',
        'niconico_help': 'Aide Niconico',
        'usage_guide': "Guide d'utilisation",
        'troubleshooting': 'Dépannage',
        
        # Education keywords - additional
        'keyword_lecture': 'Cours',
        'keyword_tutorial': 'Tutoriel',
        
        # News keywords - additional
        'keyword_world_news': 'Actualités mondiales',
        'keyword_sports_news': 'Actualités sportives',
        'keyword_technology_news': 'Actualités technologiques',
        'region_japan': 'Japon',
        'region_korea': 'Corée',
        'region_china': 'Chine',
        'region_usa': 'États-Unis',
        'region_uk': 'Royaume-Uni',
        'region_france': 'France',
        'region_germany': 'Allemagne',
        
        # Buttons
        'button_create': 'Créer la playlist',
        'button_search': 'Rechercher',
        'button_cancel': 'Annuler',
        'button_save': 'Sauvegarder',
        'button_delete': 'Supprimer',
        'button_close': 'Fermer',
        
        # Messages
        'message_success': 'Succès',
        'message_error': 'Erreur',
        'message_creating': 'Création...',
        'message_searching': 'Recherche...',
        
        # Privacy
        'privacy_private': 'Privé',
        'privacy_unlisted': 'Non répertorié',
        'privacy_public': 'Public',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Search precision
        'precision_standard': 'Standard',
        'precision_high': 'Haute précision',
        'precision_highest': 'Précision maximale',
        
        # Status
        'status_ready': 'Prêt',
        'status_authenticated': 'Authentifié',
        'setup_wizard': 'Assistant de configuration',
        'youtube_auth': 'Authentification YouTube',
        'niconico_auth': 'Authentification Niconico',
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
        'backup_create': 'Backup erstellen',
        'backup_restore': 'Aus Backup wiederherstellen',
        'backup_manage': 'Backups verwalten',
        'menu_exit': 'Beenden',
        'favorites_save': 'Aktuelle Einstellungen speichern',
        'favorites_load': 'Favoriten laden',
        'favorites_manage': 'Favoriten verwalten',
        'menu_language': 'Sprache',
        'update_check': 'Nach Updates suchen',
        'about': 'Über',
        
        # Main UI labels
        'label_era': 'Ära:',
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
        'tab_playlist': 'Video-Wiedergabeliste',
        
        # Music keywords
        'keyword_rock': 'Rock',
        'keyword_pop': 'Pop',
        'keyword_jazz': 'Jazz',
        'keyword_classical': 'Klassik',
        'keyword_hip-hop': 'Hip-Hop',
        'keyword_electronic': 'Elektronisch',
        'keyword_metal': 'Metal',
        'keyword_country': 'Country',
        'keyword_reggae': 'Reggae',
        'keyword_blues': 'Blues',
        
        # Movie keywords
        'keyword_action': 'Action',
        'keyword_comedy': 'Komödie',
        'keyword_drama': 'Drama',
        'keyword_horror': 'Horror',
        'keyword_sci-fi': 'Science-Fiction',
        'keyword_animation': 'Animation',
        'keyword_documentary': 'Dokumentarfilm',
        'keyword_thriller': 'Thriller',
        
        # Education keywords
        'keyword_science': 'Wissenschaft',
        'keyword_technology': 'Technologie',
        'keyword_history': 'Geschichte',
        'keyword_math': 'Mathematik',
        'keyword_language': 'Sprachen',
        
        # News keywords
        'keyword_politics': 'Politik',
        'keyword_world_news': 'Weltnachrichten',
        'keyword_economy': 'Wirtschaft',
        'keyword_sports': 'Sport',
        
        # Regions
        'region_selected': 'Ausgewählt:',

        # UI Section labels
        'section_preset': 'Voreinstellung',
        'section_result': 'Ergebnis',
        
        # Additional labels
        'label_preset': 'Voreinstellung:',
        
        # Buttons
        'btn_load': 'Laden',
        'btn_save': 'Speichern',
        'btn_edit': 'Bearbeiten',
        
        # Privacy descriptions
        'privacy_private_desc': 'Nur Sie können ansehen',
        'privacy_unlisted_desc': 'Nur Sie können ansehen',
        'privacy_public_desc': 'Jeder kann suchen und ansehen',
        
        # Additional options
        'option_add_detailed_desc': 'Detaillierte Beschreibung hinzufügen',
        # Setup and Auth menu items
        'setup_wizard': 'Einrichtungsassistent',
        'youtube_auth': 'YouTube-Authentifizierung',
        'niconico_auth': 'Niconico-Authentifizierung',
        'check_auth_status': 'Authentifizierungsstatus prüfen',
        
        # History menu items
        'export_history': 'Verlauf exportieren',
        'import_history': 'Verlauf importieren',
        
        # Help menu items
        'youtube_api_help': 'YouTube-API-Hilfe',
        'niconico_help': 'Niconico-Hilfe',
        'usage_guide': 'Benutzerhandbuch',
        'troubleshooting': 'Fehlerbehebung',
        
        # Education keywords - additional
        'keyword_lecture': 'Vorlesung',
        'keyword_tutorial': 'Tutorial',
        
        # News keywords - additional
        'keyword_world_news': 'Weltnachrichten',
        'keyword_sports_news': 'Sportnachrichten',
        'keyword_technology_news': 'Technologienachrichten',
        'region_japan': 'Japan',
        'region_korea': 'Korea',
        'region_china': 'China',
        'region_usa': 'USA',
        'region_uk': 'Vereinigtes Königreich',
        'region_france': 'Frankreich',
        'region_germany': 'Deutschland',
        
        # Buttons
        'button_create': 'Wiedergabeliste erstellen',
        'button_search': 'Suchen',
        'button_cancel': 'Abbrechen',
        'button_save': 'Speichern',
        'button_delete': 'Löschen',
        'button_close': 'Schließen',
        
        # Messages
        'message_success': 'Erfolg',
        'message_error': 'Fehler',
        'message_creating': 'Wird erstellt...',
        'message_searching': 'Suche läuft...',
        
        # Privacy
        'privacy_private': 'Privat',
        'privacy_unlisted': 'Nicht gelistet',
        'privacy_public': 'Öffentlich',
        
        # Platform
        'platform_youtube': 'YouTube',
        'platform_niconico': 'Niconico',
        
        # Search precision
        'precision_standard': 'Standard',
        'precision_high': 'Hohe Präzision',
        'precision_highest': 'Höchste Präzision',
        
        # Status
        'status_ready': 'Bereit',
        'status_authenticated': 'Authentifiziert',
        'setup_wizard': 'Einrichtungsassistent',
        'youtube_auth': 'YouTube-Authentifizierung',
        'niconico_auth': 'Niconico-Authentifizierung',
    }

}

# Current language (default: Japanese)
_current_lang = 'ja'

def set_language(lang_code):
    """Set current language"""
    global _current_lang
    if lang_code in TRANSLATIONS:
        _current_lang = lang_code
        return True
    return False

def get_current_language():
    """Get current language code"""
    return _current_lang

def t(key):
    """Get translation for key"""
    return TRANSLATIONS.get(_current_lang, TRANSLATIONS['ja']).get(key, key)

def t_keyword(keyword):
    """Translate keyword - convenience wrapper for t('keyword_xxx')"""
    if keyword.startswith('keyword_'):
        return t(keyword)
    return t(f'keyword_{keyword}')

def t_region(region):
    """Translate region - convenience wrapper for t('region_xxx')"""
    if region.startswith('region_'):
        return t(region)
    return t(f'region_{region}')

# Keyword to API mapping
KEYWORD_TO_API = {
    # Japanese
    'ロック': 'rock', 'ポップ': 'pop', 'ジャズ': 'jazz', 'クラシック': 'classical',
    'ヒップホップ': 'hip-hop', 'EDM': 'EDM', 'メタル': 'metal', 'カントリー': 'country',
    'レゲエ': 'reggae', 'エレクトロニック': 'electronic', 'ブルース': 'blues',
    'アクション': 'action', 'コメディ': 'comedy', 'ドラマ': 'drama', 'ホラー': 'horror',
    'SF': 'sci-fi', 'ロマンス': 'romance', 'スリラー': 'thriller', 'アニメーション': 'animation',
    'ドキュメンタリー': 'documentary', 'ファンタジー': 'fantasy', '犯罪': 'crime',
    '科学': 'science', '技術': 'technology', '歴史': 'history', '語学': 'language learning',
    '数学': 'math', '芸術': 'art', '料理': 'cooking', 'プログラミング': 'programming',
    'ビジネス': 'business', '健康': 'health',
    '政治': 'politics', '国際ニュース': 'world news', '経済': 'economy', 'スポーツ': 'sports',
    'IT・技術': 'tech news', '芸能': 'entertainment news', '天気': 'weather', '地域ニュース': 'local news',
    
    # English
    'Rock': 'rock', 'Pop': 'pop', 'Jazz': 'jazz', 'Classical': 'classical',
    'Hip-Hop': 'hip-hop', 'EDM': 'EDM', 'Metal': 'metal', 'Country': 'country',
    'Reggae': 'reggae', 'Electronic': 'electronic', 'Blues': 'blues',
    'Action': 'action', 'Comedy': 'comedy', 'Drama': 'drama', 'Horror': 'horror',
    'Sci-Fi': 'sci-fi', 'Romance': 'romance', 'Thriller': 'thriller', 'Animation': 'animation',
    'Documentary': 'documentary', 'Fantasy': 'fantasy', 'Crime': 'crime',
    'Science': 'science', 'Technology': 'technology', 'History': 'history', 'Language': 'language learning',
    'Math': 'math', 'Art': 'art', 'Cooking': 'cooking', 'Programming': 'programming',
    'Business': 'business', 'Health': 'health',
    'Politics': 'politics', 'World News': 'world news', 'Economy': 'economy', 'Sports': 'sports',
    'Tech News': 'tech news', 'Entertainment': 'entertainment news', 'Weather': 'weather', 'Local News': 'local news',
    
    # Chinese Simplified
    '摇滚': 'rock', '流行': 'pop', '爵士': 'jazz', '古典': 'classical',
    '嘻哈': 'hip-hop', '电子舞曲': 'EDM', '金属': 'metal', '乡村': 'country',
    '雷鬼': 'reggae', '电子': 'electronic', '布鲁斯': 'blues',
    '动作': 'action', '喜剧': 'comedy', '剧情': 'drama', '恐怖': 'horror',
    '科幻': 'sci-fi', '爱情': 'romance', '惊悚': 'thriller', '动画': 'animation',
    '纪录片': 'documentary', '奇幻': 'fantasy', '犯罪': 'crime',
    '科学': 'science', '技术': 'technology', '历史': 'history', '语言': 'language learning',
    '数学': 'math', '艺术': 'art', '烹饪': 'cooking', '编程': 'programming',
    '商业': 'business', '健康': 'health',
    '政治': 'politics', '国际新闻': 'world news', '经济': 'economy', '体育': 'sports',
    '科技新闻': 'tech news', '娱乐': 'entertainment news', '天气': 'weather', '本地新闻': 'local news'
}

def get_api_keyword(display_keyword):
    """Convert display keyword to API search keyword (English)"""
    return KEYWORD_TO_API.get(display_keyword, display_keyword)


def get_current_language():
    return current_language

def get_available_languages():
    return list(TRANSLATIONS.keys())
