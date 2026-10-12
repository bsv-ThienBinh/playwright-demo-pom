class LoginPageLocators:
    INPUT_USERNAME = "ID"  # ID   lấy theo label
    INPUT_PASSWORD = "パスワード"  # パスワード lấy theo label
    BUTTON_LOGIN = "ログイン"  # ログイン lấy theo label
    LOGIN_ERROR = "#login_error" # lấy theo id

class TicketPageLocators:
    PANEL = "#panel_tickets"
    SEARCH_INPUT = "件名または担当者で検索"  # 件名または担当者で検索
    BUTTON_SEARCH = "検索"  # 検索
    BUTTON_NEW_TICKET = "新規チケット作成"  # 新規チケット作成
    TICKET_ROWS = "#ticket_tbody tr"
    DRAWER_TITLE = "新規チケット作成"  # 新規チケット作成
    STEP1 = "1. 基本情報"  # 1. 基本情報
    NAV_NOTIFICATIONS = "#nav_tab_notifications"
    SELECT_ALL = "全て選択"  # 全て選択
    ROW_CHECKBOX = "#ticket_tbody input.row-checkbox"
    BULK_BAR = "#bulk_action_bar"
    SELECT_ALL = "全て選択"  # 全て選択
    PRIORITY_FILTER = "優先度で絞り込み"  # 優先度で絞り込み
    BUTTON_DELETE = "削除"  # 削除
    CREATED_DATE_HELP = "#th_created .tooltip-wrap"
    CREATED_DATE_TOOLTIP = "#th_created .tooltip-content" 
    BUTTON_DETAIL = "詳細"  # 詳細
    BUTTON_DELETE = "削除"  # 削除
    DETAIL_TITLE = "チケット詳細"  # チケット詳細
    FILE_INPUT = "#detail_file_input"
    FILE_NAME = "#detail_file_name"
    BUTTON_REMOVE_FILE = "ファイルを削除"  # ファイルを削除
    BUTTON_CLOSE_DETAIL = "#detail_close_btn"
    BUTTON_MANUAL = "外部マニュアルを開く（新しいタブ）"  # 外部マニュアルを開く（新しいタブ）
    PREVIEW_FRAME = "#preview_iframe"
    FRAME_STATUS = "#frame_status"
    BUTTON_APPLY = "適用"  # 適用
    FRAME_RESULT = "#frame_result"
    HEADER = "#app_header"
    TICKET_TABLE = "#ticket_table"

class NotificationPageLocators:
    TITLE = "通知一覧"  # 通知一覧
    ROWS = "#notification_tbody tr"
    PANEL = "#panel_notifications"