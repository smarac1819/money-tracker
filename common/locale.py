"""
Money Tracker — i18n Locale System
Supports Chinese (ZH) and English (EN).
Access via:  from common.locale import L, set_lang, get_lang
"""

from PyQt6.QtCore import QSettings

# ── String table ──────────────────────────────────────────────────────────────
STRINGS = {
    # ── App-level ──
    "app_title":            {"zh": "智能财务记账管家",       "en": "Smart Finance Tracker"},
    "app_subtitle":         {"zh": "记账管家专业版",         "en": "Pro Edition"},

    # ── Sidebar ──
    "ledger_list":          {"zh": "账本列表",               "en": "Ledgers"},
    "sort_label":           {"zh": "排序：",                 "en": "Sort:"},
    "sort_bal_desc":        {"zh": "余额从大到小",            "en": "Balance ↓"},
    "sort_bal_asc":         {"zh": "余额从小到大",            "en": "Balance ↑"},
    "sort_created":         {"zh": "创建时间",               "en": "Created"},
    "sort_updated":         {"zh": "最近动态",               "en": "Recent"},
    "btn_search":           {"zh": "全局搜索",               "en": "Search"},
    "btn_stats":            {"zh": "数据分析",               "en": "Analytics"},
    "btn_settings":         {"zh": "系统设置",               "en": "Settings"},
    "btn_add_ledger":       {"zh": "+ 新建账本",             "en": "+ New Ledger"},

    # ── Ledger / Module Panel ──
    "no_ledger":            {"zh": "未选择账本",             "en": "No Ledger Selected"},
    "btn_manage":           {"zh": "☑ 管理",                "en": "☑ Manage"},
    "btn_income":           {"zh": "+  记入收入",            "en": "+  Add Income"},
    "btn_expense":          {"zh": "−  记录支出",            "en": "−  Add Expense"},
    "btn_select_all":       {"zh": "全选",                   "en": "Select All"},
    "btn_delete_selected":  {"zh": "删除选中",               "en": "Delete Selected"},
    "filter_label":         {"zh": "筛选:",                  "en": "Filter:"},
    "filter_all":           {"zh": "全部",                   "en": "All"},
    "filter_income":        {"zh": "收入 ↗",                 "en": "Income ↗"},
    "filter_expense":       {"zh": "支出 ↙",                 "en": "Expense ↙"},
    "sort_bar_label":       {"zh": "排序:",                  "en": "Sort:"},
    "sort_by_date":         {"zh": "按日期",                 "en": "By Date"},
    "sort_by_amount":       {"zh": "按金额",                 "en": "By Amount"},
    "sort_desc":            {"zh": "降序 ↓",                 "en": "Desc ↓"},
    "sort_asc":             {"zh": "升序 ↑",                 "en": "Asc ↑"},
    "income_short":         {"zh": "收 ¥",                   "en": "In ¥"},
    "expense_short":        {"zh": "支 ¥",                   "en": "Out ¥"},
    "currency_unit":        {"zh": "元",                     "en": ""},
    "uncategorized":        {"zh": "未分类",                 "en": "Uncategorized"},
    "confirm_delete":       {"zh": "确认删除",               "en": "Confirm Delete"},
    "confirm_delete_msg":   {"zh": "确定要删除选中的 {n} 条交易记录吗？",
                             "en": "Delete {n} selected transaction(s)?"},

    # ── Analytics Panel ──
    "analytics_title":      {"zh": "数据分析",               "en": "Analytics"},
    "multi_select_btn":     {"zh": "☑  多选统计",            "en": "☑  Multi-Select"},
    "net_worth_label":      {"zh": "NET WORTH  净资产",      "en": "NET WORTH"},
    "live_label":           {"zh": "● LIVE",                 "en": "● LIVE"},
    "total_income_label":   {"zh": "总收入  INCOME",         "en": "TOTAL INCOME"},
    "total_expense_label":  {"zh": "总支出  EXPENSE",        "en": "TOTAL EXPENSE"},
    "ledger_detail":        {"zh": "账本明细",               "en": "Ledger Detail"},

    # ── Transaction Dialog ──
    "tx_income_title":      {"zh": "记笔收入",               "en": "Add Income"},
    "tx_expense_title":     {"zh": "记笔支出",               "en": "Add Expense"},
    "ledger_label":         {"zh": "账本：",                 "en": "Ledger: "},
    "amount_caption":       {"zh": "AMOUNT  交易金额",       "en": "AMOUNT"},
    "amount_placeholder":   {"zh": "0.00",                   "en": "0.00"},
    "category_caption":     {"zh": "CATEGORY  分类备注",     "en": "CATEGORY & NOTE"},
    "category_placeholder": {"zh": "输入备注或选择分类…",   "en": "Enter note or pick category…"},
    "btn_cancel":           {"zh": "取消",                   "en": "Cancel"},
    "btn_confirm":          {"zh": "确认记录 ✓",             "en": "Confirm ✓"},

    # ── Module Dialog ──
    "new_ledger_title":     {"zh": "新建账本",               "en": "New Ledger"},
    "edit_ledger_title":    {"zh": "编辑账本",               "en": "Edit Ledger"},
    "ledger_name_label":    {"zh": "账本名称",               "en": "Ledger Name"},
    "ledger_name_hint":     {"zh": "为账本起个名字…",        "en": "Give your ledger a name…"},
    "btn_save":             {"zh": "保 存  ✓",               "en": "Save  ✓"},
    "btn_delete_ledger":    {"zh": "删除此账本",             "en": "Delete This Ledger"},

    # ── Settings Dialog ──
    "settings_title":       {"zh": "⚙️  系统设置",           "en": "⚙️  Settings"},
    "shortcut_section":     {"zh": "⌨️  快捷键设置",          "en": "⌨️  Keyboard Shortcuts"},
    "shortcut_hint":        {"zh": "点击输入框后按下想要绑定的按键（单个字母推荐）",
                             "en": "Click the box then press a key to bind (single letter recommended)"},
    "shortcut_income":      {"zh": "记入收入快捷键",         "en": "Add Income Shortcut"},
    "shortcut_expense":     {"zh": "记录支出快捷键",         "en": "Add Expense Shortcut"},
    "shortcut_default":     {"zh": "默认 [{k}]",             "en": "Default [{k}]"},
    "password_section":     {"zh": "🔐  密码保护",           "en": "🔐  Password Lock"},
    "pwd_set":              {"zh": "✅  当前已设置密码，启动时需要验证",
                             "en": "✅  Password is set — required on launch"},
    "pwd_not_set":          {"zh": "🔓  当前未设置密码",      "en": "🔓  No password set"},
    "btn_change_pwd":       {"zh": "修改密码",               "en": "Change Password"},
    "btn_remove_pwd":       {"zh": "移除密码",               "en": "Remove Password"},
    "btn_set_pwd":          {"zh": "设置密码",               "en": "Set Password"},
    "language_section":     {"zh": "🌐  语言 / Language",    "en": "🌐  Language"},
    "lang_zh":              {"zh": "中文",                   "en": "中文 (Chinese)"},
    "lang_en":              {"zh": "English",                "en": "English"},
    "lang_restart_hint":    {"zh": "切换语言后请重启应用以生效",
                             "en": "Restart the app after switching language"},
    "btn_save_close":       {"zh": "保存并关闭  ✓",          "en": "Save & Close  ✓"},

    # ── Search Panel ──
    "search_placeholder":   {"zh": "搜索交易记录…",          "en": "Search transactions…"},
    "search_empty":         {"zh": "未找到匹配记录",         "en": "No results found"},

    # ── Export ──
    "export_success":       {"zh": "导出成功！",             "en": "Export Successful!"},
    "btn_open_folder":      {"zh": "📂 打开文件夹",          "en": "📂 Open Folder"},
    "btn_done":             {"zh": "完 成",                  "en": "Done"},

    # ── About / Developer ──
    "about_section":        {"zh": "ℹ️  关于",               "en": "ℹ️  About"},
    "developer_label":      {"zh": "开发人员",               "en": "Developer"},
    "developer_name":       {"zh": "TRYuuu233",              "en": "TRYuuu233"},
    "version_label":        {"zh": "版本",                   "en": "Version"},
    "version_value":        {"zh": "v1.0.0",                 "en": "v1.0.0"},

    # ── Misc ──
    "tooltip_exact":        {"zh": "精确余额: ¥{v}\n收入: ¥{i}\n支出: ¥{e}",
                             "en": "Exact balance: ¥{v}\nIncome: ¥{i}\nExpense: ¥{e}"},
}


# ── Runtime state ─────────────────────────────────────────────────────────────
_current_lang: str = "zh"


def get_lang() -> str:
    """Return the currently active language code ('zh' or 'en')."""
    return _current_lang


def set_lang(lang: str):
    """Set the active language. Saves to QSettings for persistence."""
    global _current_lang
    if lang in ("zh", "en"):
        _current_lang = lang
        s = QSettings("MoneyTracker", "Shortcuts")
        s.setValue("language", lang)
        s.sync()


def load_lang():
    """Load the saved language preference from QSettings (call on startup)."""
    global _current_lang
    s = QSettings("MoneyTracker", "Shortcuts")
    _current_lang = s.value("language", "zh")


def L(key: str, **kwargs) -> str:
    """
    Look up a localized string by key.
    Supports f-string style substitution via kwargs:
        L("confirm_delete_msg", n=3)  →  "Delete 3 selected transaction(s)?"
    """
    entry = STRINGS.get(key)
    if entry is None:
        return key  # fallback: return key name
    text = entry.get(_current_lang, entry.get("zh", key))
    for k, v in kwargs.items():
        text = text.replace("{" + k + "}", str(v))
    return text
