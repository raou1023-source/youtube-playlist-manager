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
