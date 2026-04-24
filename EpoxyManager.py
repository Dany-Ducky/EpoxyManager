"""環氧樹脂工作站 V6.4.12 """
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv, os, datetime, json, math

import sys as _sys
def _detect_font():
    """Select CJK font by platform."""
    p = _sys.platform
    if p == 'darwin':
        return "PingFang TC"
    elif p == 'win32':
        return "Microsoft JhengHei"
    else:
        return "Noto Sans CJK TC"

_FONT_FAMILY = _detect_font()

class _C:
    """Color constants."""
    BLUE       = "#0071e3"
    BLUE_HOVER = "#0077ED"
    BLUE_DARK  = "#0066cc"
    BLUE_LIGHT = "#2997ff"

    TEXT       = "#1d1d1f"
    TEXT_SEC   = "#48484a"
    TEXT_TER   = "#86868b"
    TEXT_WHITE = "#ffffff"

    BG_LIGHT   = "#f5f5f7"
    BG_WHITE   = "#ffffff"
    BG_BLACK   = "#000000"
    BG_INPUT   = "#ffffff"

    BORDER     = "#d2d2d7"
    BORDER_LT  = "#e8e8ed"

    BTN_LIGHT  = "#c7c7cc"
    BTN_HOVER  = "#aeaeb2"
    BTN_ADD_HV = "#f0f5ff"

    TAB_UNSEL  = "#8e8e93"
    TAB_HOVER  = "#636366"

    GREEN      = "#34C759"
    GREEN_HV   = "#2DB84D"
    RED        = "#FF3B30"
    RED_HV     = "#D32F2F"
    ORANGE     = "#FF9500"
    PINK       = "#FF2D55"
    INDIGO     = "#5856D6"
    PURPLE     = "#AF52DE"

    CARD_A     = "#f0f5ff"
    CARD_B     = "#fff1f2"
    SUBTOTAL   = "#fef3c7"

    SASH       = "#d2d2d7"

LANG_CFG_FILE = "lang_config.json"
SUPPORTED_LANGS = ["zh_TW", "zh_CN", "en", "ja"]
LANG_DISPLAY = {"zh_TW": "正體中文", "zh_CN": "简体中文", "en": "English", "ja": "日本語"}

_CURRENT_LANG = "zh_TW"

_TRANSLATIONS = {
"app_title":                  {"zh_TW":"環氧樹脂工作站", "zh_CN":"环氧树脂工作站", "en":"Epoxy Resin Workstation", "ja":"エポキシ樹脂ワークステーション"},
"tab_calc":                   {"zh_TW":"🧪 1K 單組分設計", "zh_CN":"🧪 1K 单组分设计", "en":"🧪 1K Formulation", "ja":"🧪 1K 配合設計"},
"tab_db":                     {"zh_TW":"🕷 物料資料庫管理", "zh_CN":"🕷 物料数据库管理", "en":"🕷 Material Database", "ja":"🕷 材料データベース管理"},
"tab_recipe":                 {"zh_TW":"📋 配方管理與物性", "zh_CN":"📋 配方管理与物性", "en":"📋 Recipe & Properties", "ja":"📋 配合管理と物性"},
"language":                   {"zh_TW":"語言", "zh_CN":"语言", "en":"Language", "ja":"言語"},
"cat_resins":                 {"zh_TW":"樹脂", "zh_CN":"树脂", "en":"Resins", "ja":"樹脂"},
"cat_hardeners":              {"zh_TW":"固化劑", "zh_CN":"固化剂", "en":"Hardeners", "ja":"硬化剤"},
"cat_additives":              {"zh_TW":"助劑", "zh_CN":"助剂", "en":"Additives", "ja":"添加剤"},
"cat_fillers":                {"zh_TW":"填料", "zh_CN":"填料", "en":"Fillers", "ja":"フィラー"},
"cat_catalysts":              {"zh_TW":"催化劑", "zh_CN":"催化剂", "en":"Catalysts", "ja":"触媒"},
"sec_resin":                  {"zh_TW":"1. 樹脂", "zh_CN":"1. 树脂", "en":"1. Resins", "ja":"1. 樹脂"},
"sec_hardener":               {"zh_TW":"2. 固化劑", "zh_CN":"2. 固化剂", "en":"2. Hardeners", "ja":"2. 硬化剤"},
"sec_additive":               {"zh_TW":"3. 助劑", "zh_CN":"3. 助剂", "en":"3. Additives", "ja":"3. 添加剤"},
"sec_filler":                 {"zh_TW":"4. 填料", "zh_CN":"4. 填料", "en":"4. Fillers", "ja":"4. フィラー"},
"sec_catalyst":               {"zh_TW":"5. 催化劑", "zh_CN":"5. 催化剂", "en":"5. Catalysts", "ja":"5. 触媒"},
"add_resin":                  {"zh_TW":"+ 添加樹脂", "zh_CN":"+ 添加树脂", "en":"+ Add Resin", "ja":"+ 樹脂を追加"},
"add_hardener":               {"zh_TW":"+ 添加固化劑", "zh_CN":"+ 添加固化剂", "en":"+ Add Hardener", "ja":"+ 硬化剤を追加"},
"add_additive":               {"zh_TW":"+ 添加助劑", "zh_CN":"+ 添加助剂", "en":"+ Add Additive", "ja":"+ 添加剤を追加"},
"add_filler":                 {"zh_TW":"+ 添加填料", "zh_CN":"+ 添加填料", "en":"+ Add Filler", "ja":"+ フィラーを追加"},
"add_catalyst":               {"zh_TW":"+ 添加催化劑", "zh_CN":"+ 添加催化剂", "en":"+ Add Catalyst", "ja":"+ 触媒を追加"},
"calc_mode":                  {"zh_TW":"計算模式:", "zh_CN":"计算模式:", "en":"Calc Mode:", "ja":"計算モード:"},
"calc_settings":              {"zh_TW":"計算設定", "zh_CN":"计算设置", "en":"Calculation Settings", "ja":"計算設定"},
"mass_rounding":              {"zh_TW":"質量取整:", "zh_CN":"质量取整:", "en":"Mass Rounding:", "ja":"質量丸め:"},
"opt_100g":                   {"zh_TW":"100g 配平選項", "zh_CN":"100g 配平选项", "en":"100g Balancing Options", "ja":"100gバランスオプション"},
"join_100g_balance":          {"zh_TW":"參與100g配平", "zh_CN":"参与100g配平", "en":"Include in 100g balance", "ja":"100gバランスに含める"},
"hint_100g_extra":            {"zh_TW":"💡 100g模式：僅樹脂+固化劑配平至100g，其他組分按%額外添加", "zh_CN":"💡 100g模式：仅树脂+固化剂配平至100g，其他组分按%额外添加", "en":"💡 100g: Only R+H balanced to 100g; others added as % extra", "ja":"💡 100g：樹脂+硬化剤のみを100gに調整、その他は%で追加"},
"hint_phr100":               {"zh_TW":"💡 百份模式：樹脂配平至100份，固化劑按當量額外計算，助劑/填料/催化劑按(R+H)%額外添加", "zh_CN":"💡 百份模式：树脂配平至100份，固化剂按当量额外计算，助剂/填料/催化剂按(R+H)%额外添加", "en":"💡 phr_100: Resin=100 parts, hardener by equiv (extra), others as %(R+H) extra", "ja":"💡 百部法：樹脂100部、硬化剤は当量で追加、他は(R+H)%で追加"},
"col_phr_result":             {"zh_TW":"phr (基材%)", "zh_CN":"phr (基材%)", "en":"phr (Base%)", "ja":"phr (基材%)"},
"2k_normalize":               {"zh_TW":"⚖ 基材配平至 100g（填料等按 % 額外添加）", "zh_CN":"⚖ 基材配平至 100g（填料等按 % 额外添加）", "en":"⚖ Normalize base (R+H) to 100g", "ja":"⚖ 基材を100gに正規化"},
"btn_calculate":              {"zh_TW":"▶ 開始計算並生成報表", "zh_CN":"▶ 开始计算并生成报表", "en":"▶ Calculate & Generate Report", "ja":"▶ 計算してレポート生成"},
"col_material":               {"zh_TW":"物料", "zh_CN":"物料", "en":"Material", "ja":"材料"},
"col_mass_g":                 {"zh_TW":"質量(g)", "zh_CN":"质量(g)", "en":"Mass(g)", "ja":"質量(g)"},
"col_pct":                    {"zh_TW":"佔比(%)", "zh_CN":"占比(%)", "en":"Ratio(%)", "ja":"配合比(%)"},
"col_eq_info":                {"zh_TW":"當量資訊", "zh_CN":"当量信息", "en":"Eq. Info", "ja":"当量情報"},
"col_cl_ppm":                 {"zh_TW":"氯(ppm)", "zh_CN":"氯(ppm)", "en":"Cl(ppm)", "ja":"塩素(ppm)"},
"btn_copy_excel":             {"zh_TW":"📋 複製到 Excel", "zh_CN":"📋 复制到 Excel", "en":"📋 Copy to Excel", "ja":"📋 Excelにコピー"},
"btn_save_recipe":            {"zh_TW":"💾 儲存配方至資料庫", "zh_CN":"💾 保存配方至数据库", "en":"💾 Save Recipe to Database", "ja":"💾 配合をデータベースに保存"},
"hdr_name_type":              {"zh_TW":"名稱/類型", "zh_CN":"名称/类型", "en":"Name/Type", "ja":"名称/タイプ"},
"hdr_eq_ratio":               {"zh_TW":"當量比例/佔比", "zh_CN":"当量比例/占比", "en":"Eq.Ratio/Pct", "ja":"当量比/配合比"},
"hdr_corr_pct":               {"zh_TW":"校正(C)%", "zh_CN":"校正(C)%", "en":"Correction(C)%", "ja":"補正(C)%"},
"clear_reselect":             {"zh_TW":"清空並重選物料", "zh_CN":"清空并重选物料", "en":"Clear & reselect material", "ja":"クリアして再選択"},
"no_note":                    {"zh_TW":"無備註", "zh_CN":"无备注", "en":"No notes", "ja":"備考なし"},
"fixed_mass":                 {"zh_TW":"固定質量", "zh_CN":"固定质量", "en":"Fixed Mass", "ja":"固定質量"},
"fixed_ratio":                {"zh_TW":"固定比例", "zh_CN":"固定比例", "en":"Fixed Ratio", "ja":"固定比率"},
"dlg_save_recipe":            {"zh_TW":"儲存配方", "zh_CN":"保存配方", "en":"Save Recipe", "ja":"配合を保存"},
"recipe_name_label":          {"zh_TW":"配方名稱：", "zh_CN":"配方名称：", "en":"Recipe Name:", "ja":"配合名："},
"batch_no_label":             {"zh_TW":"批次號：", "zh_CN":"批次号：", "en":"Batch No.:", "ja":"ロット番号："},
"btn_confirm_save":           {"zh_TW":"💾 確認儲存", "zh_CN":"💾 确认保存", "en":"💾 Confirm Save", "ja":"💾 保存確認"},
"warn_enter_name":            {"zh_TW":"請輸入配方名稱", "zh_CN":"请输入配方名称", "en":"Please enter a recipe name", "ja":"配合名を入力してください"},
"warn_calc_first":            {"zh_TW":"請先執行計算", "zh_CN":"请先执行计算", "en":"Please calculate first", "ja":"先に計算を実行してください"},
"save_ok":                    {"zh_TW":"已成功儲存至配方庫", "zh_CN":"已成功保存至配方库", "en":"Successfully saved to recipe database", "ja":"配合データベースに保存しました"},
"copy_ok":                    {"zh_TW":"已複製到剪貼簿，可在 Excel 中貼上", "zh_CN":"已复制到剪贴板，可在 Excel 中粘贴", "en":"Copied to clipboard, paste in Excel", "ja":"クリップボードにコピーしました"},
"data_edit":                  {"zh_TW":"資料編輯", "zh_CN":"数据编辑", "en":"Data Edit", "ja":"データ編集"},
"not_selected":               {"zh_TW":"（未選取資料）", "zh_CN":"（未选中数据）", "en":"(No selection)", "ja":"（未選択）"},
"editing":                    {"zh_TW":"▶ 編輯中：", "zh_CN":"▶ 编辑中：", "en":"▶ Editing: ", "ja":"▶ 編集中："},
"btn_deselect":               {"zh_TW":"✖ 取消選取", "zh_CN":"✖ 取消选中", "en":"✖ Deselect", "ja":"✖ 選択解除"},
"lbl_category":               {"zh_TW":"類別:", "zh_CN":"类别:", "en":"Category:", "ja":"カテゴリー:"},
"lbl_name":                   {"zh_TW":"名稱:", "zh_CN":"名称:", "en":"Name:", "ja":"名称:"},
"lbl_type":                   {"zh_TW":"類型:", "zh_CN":"类型:", "en":"Type:", "ja":"タイプ:"},
"lbl_appearance":             {"zh_TW":"外觀特性:", "zh_CN":"外观特性:", "en":"Appearance:", "ja":"外観特性:"},
"lbl_viscosity":              {"zh_TW":"黏度 cP(25℃):", "zh_CN":"粘度 cP(25℃):", "en":"Viscosity cP(25℃):", "ja":"粘度 cP(25℃):"},
"lbl_dk":                     {"zh_TW":"介電常數:", "zh_CN":"介电常数:", "en":"Dielectric Const.:", "ja":"誘電率:"},
"lbl_surface_energy":         {"zh_TW":"表面能 mN/m(25℃):", "zh_CN":"表面能 mN/m(25℃):", "en":"Surface Energy mN/m(25℃):", "ja":"表面エネルギー mN/m(25℃):"},
"lbl_structure":              {"zh_TW":"分子結構:", "zh_CN":"分子结构:", "en":"Molecular Structure:", "ja":"分子構造:"},
"lbl_source":                 {"zh_TW":"來源:", "zh_CN":"来源:", "en":"Source:", "ja":"入手先:"},
"lbl_cl":                     {"zh_TW":"氯(ppm):", "zh_CN":"氯(ppm):", "en":"Cl(ppm):", "ja":"塩素(ppm):"},
"lbl_cost_per_kg":            {"zh_TW":"成本 ($/kg):", "zh_CN":"成本 ($/kg):", "en":"Cost ($/kg):", "ja":"コスト ($/kg):"},
"lbl_volatile_pct":           {"zh_TW":"揮發分 (%):", "zh_CN":"挥发分 (%):", "en":"Volatiles (%):", "ja":"揮発分 (%):"},
"lbl_tg_dsc":                 {"zh_TW":"Tg-DSC (°C):", "zh_CN":"Tg-DSC (°C):", "en":"Tg-DSC (°C):", "ja":"Tg-DSC (°C):"},
"lbl_shelf_life":             {"zh_TW":"保存期限 (月):", "zh_CN":"保质期 (月):", "en":"Shelf Life (mo):", "ja":"有効期限 (月):"},
"lbl_storage_temp":           {"zh_TW":"儲存溫度 (°C):", "zh_CN":"储存温度 (°C):", "en":"Storage Temp (°C):", "ja":"保管温度 (°C):"},
"cost_summary":               {"zh_TW":"配方成本", "zh_CN":"配方成本", "en":"Formula Cost", "ja":"配合コスト"},
"cost_per_g":                 {"zh_TW":"$/g", "zh_CN":"$/g", "en":"$/g", "ja":"$/g"},
"cost_per_kg_unit":           {"zh_TW":"$/kg", "zh_CN":"$/kg", "en":"$/kg", "ja":"$/kg"},
"cost_incomplete":            {"zh_TW":"⚠ 部分物料缺少成本資料", "zh_CN":"⚠ 部分物料缺少成本数据", "en":"⚠ Some materials are missing cost data", "ja":"⚠ 一部の材料にコストデータなし"},
"lbl_eew":                    {"zh_TW":"EEW直接輸入:", "zh_CN":"EEW直接输入:", "en":"EEW Direct Input:", "ja":"EEW直接入力:"},
"lbl_ahew":                   {"zh_TW":"當量直接輸入:", "zh_CN":"当量直接输入:", "en":"Equivalent Direct Input:", "ja":"当量直接入力:"},
"hardener_calc":              {"zh_TW":"⚙️ 固化劑當量輔助計算", "zh_CN":"⚙️ 固化剂当量辅助计算", "en":"⚙️ Hardener Eq. Calculator", "ja":"⚙️ 硬化剤当量補助計算"},
"lbl_subtype":                {"zh_TW":"子類型:", "zh_CN":"子类型:", "en":"Subtype:", "ja":"サブタイプ:"},
"custom_fields":              {"zh_TW":"📝 自訂欄位", "zh_CN":"📝 自定义栏位", "en":"📝 Custom Fields", "ja":"📝 カスタムフィールド"},
"no_custom_fields":           {"zh_TW":"（無自訂欄位）", "zh_CN":"（无自定义栏位）", "en":"(No custom fields)", "ja":"（カスタムフィールドなし）"},
"lbl_notes":                  {"zh_TW":"備註:", "zh_CN":"备注:", "en":"Notes:", "ja":"備考:"},
"btn_save":                   {"zh_TW":"💾 儲存", "zh_CN":"💾 保存", "en":"💾 Save", "ja":"💾 保存"},
"btn_save_as_new":            {"zh_TW":"📄 另存為新物料", "zh_CN":"📄 另存为新物料", "en":"📄 Save As New", "ja":"📄 新規として保存"},
"btn_delete_sel":             {"zh_TW":"🗑 刪除所選", "zh_CN":"🗑 删除选中", "en":"🗑 Delete Selected", "ja":"🗑 選択削除"},
"btn_col_manager":            {"zh_TW":"⚙ 欄位管理", "zh_CN":"⚙ 栏位管理", "en":"⚙ Column Manager", "ja":"⚙ 列管理"},
"saved_to_db":                {"zh_TW":"已成功儲存至物料庫", "zh_CN":"已成功保存至物料库", "en":"Successfully saved to database", "ja":"保存しました"},
"confirm":                    {"zh_TW":"確認", "zh_CN":"确认", "en":"Confirm", "ja":"確認"},
"hint":                       {"zh_TW":"提示", "zh_CN":"提示", "en":"Notice", "ja":"ヒント"},
"error":                      {"zh_TW":"錯誤", "zh_CN":"错误", "en":"Error", "ja":"エラー"},
"ok":                         {"zh_TW":"OK", "zh_CN":"OK", "en":"OK", "ja":"OK"},
"tab_2k":                    {"zh_TW":"⚗ 2K 雙組分設計", "zh_CN":"⚗ 2K 双组分设计", "en":"⚗ 2K Formulation", "ja":"⚗ 2K 配合設計"},
"2k_resins":                 {"zh_TW":"A 側樹脂（有EEW）", "zh_CN":"A 侧树脂（有EEW）", "en":"A-Side Resins (EEW)", "ja":"A側樹脂（EEW）"},
"2k_a_others":               {"zh_TW":"A 側其他組分", "zh_CN":"A 侧其他组分", "en":"A-Side Others", "ja":"A側その他"},
"2k_hardeners":              {"zh_TW":"B 側固化劑（AHEW）", "zh_CN":"B 侧固化剂（AHEW）", "en":"B-Side Hardeners (AHEW)", "ja":"B側硬化剤（AHEW）"},
"2k_b_others":               {"zh_TW":"B 側其他組分", "zh_CN":"B 侧其他组分", "en":"B-Side Others", "ja":"B側その他"},
"2k_add_resin":              {"zh_TW":"+ 添加 A 側樹脂", "zh_CN":"+ 添加 A 侧树脂", "en":"+ Add A-Side Resin", "ja":"+ A側樹脂追加"},
"2k_add_a_other":            {"zh_TW":"+ 添加 A 側組分", "zh_CN":"+ 添加 A 侧组分", "en":"+ Add A-Side Component", "ja":"+ A側組成追加"},
"2k_add_hardener":           {"zh_TW":"+ 添加 B 側固化劑", "zh_CN":"+ 添加 B 侧固化剂", "en":"+ Add B-Side Hardener", "ja":"+ B側硬化剤追加"},
"2k_add_b_other":            {"zh_TW":"+ 添加 B 側組分", "zh_CN":"+ 添加 B 侧组分", "en":"+ Add B-Side Component", "ja":"+ B側組成追加"},
"2k_settings":               {"zh_TW":"2K 計算設定", "zh_CN":"2K 计算设置", "en":"2K Calc Settings", "ja":"2K 計算設定"},
"2k_global_stoich":          {"zh_TW":"全域當量比 %:", "zh_CN":"全局当量比 %:", "en":"Global Stoich %:", "ja":"グローバル当量比 %:"},
"2k_target_ratio":           {"zh_TW":"目標混合比 A:B:", "zh_CN":"目标混合比 A:B:", "en":"Target Mix Ratio A:B:", "ja":"目標混合比 A:B:"},
"2k_target_none":            {"zh_TW":"不指定（自然比例）", "zh_CN":"不指定（自然比例）", "en":"None (natural ratio)", "ja":"指定なし（自然比率）"},
"2k_btn_calc":               {"zh_TW":"▶ 計算 2K 配方", "zh_CN":"▶ 计算 2K 配方", "en":"▶ Calculate 2K", "ja":"▶ 2K 配合計算"},
"2k_summary":                {"zh_TW":"配方摘要", "zh_CN":"配方摘要", "en":"Summary", "ja":"配合サマリー"},
"2k_result":                 {"zh_TW":"2K 配方報表", "zh_CN":"2K 配方报表", "en":"2K Report", "ja":"2K 配合レポート"},
"2k_save_recipe":            {"zh_TW":"💾 儲存 2K 配方", "zh_CN":"💾 保存 2K 配方", "en":"💾 Save 2K Recipe", "ja":"💾 2K配合を保存"},
"2k_copy_excel":             {"zh_TW":"📋 複製到 Excel", "zh_CN":"📋 复制到 Excel", "en":"📋 Copy to Excel", "ja":"📋 Excelにコピー"},
"tab_recipe_mgr":             {"zh_TW":"📂 配方管理", "zh_CN":"📂 配方管理", "en":"📂 Recipe Manager", "ja":"📂 配合管理"},
"recipe_list_title":          {"zh_TW":"📋 配方清單", "zh_CN":"📋 配方列表", "en":"📋 Recipe List", "ja":"📋 配合リスト"},
"btn_refresh":                {"zh_TW":"🔄 重新整理", "zh_CN":"🔄 刷新", "en":"🔄 Refresh", "ja":"🔄 更新"},
"recipe_composition":         {"zh_TW":"📄 配方組成", "zh_CN":"📄 配方组成", "en":"📄 Recipe Composition", "ja":"📄 配合組成"},
"prop_input":                 {"zh_TW":"🔬 物性資料輸入", "zh_CN":"🔬 物性数据录入", "en":"🔬 Property Data Entry", "ja":"🔬 物性データ入力"},
"custom_prop_mgr":            {"zh_TW":"🔧 自訂物性欄位", "zh_CN":"🔧 自定义物性栏位", "en":"🔧 Custom Property Fields", "ja":"🔧 カスタム物性フィールド"},
"col_recipe_name":            {"zh_TW":"配方名稱", "zh_CN":"配方名称", "en":"Recipe Name", "ja":"配合名"},
"col_batch":                  {"zh_TW":"批次號", "zh_CN":"批次号", "en":"Batch No.", "ja":"ロット番号"},
"col_date":                   {"zh_TW":"建立日期", "zh_CN":"创建日期", "en":"Date Created", "ja":"作成日"},
"col_total_mass":             {"zh_TW":"總質量(g)", "zh_CN":"总质量(g)", "en":"Total Mass(g)", "ja":"総質量(g)"},
"btn_rename":                 {"zh_TW":"✏️ 重新命名", "zh_CN":"✏️ 重命名", "en":"✏️ Rename", "ja":"✏️ 名前変更"},
"btn_delete":                 {"zh_TW":"🗑 刪除", "zh_CN":"🗑 删除", "en":"🗑 Delete", "ja":"🗑 削除"},
"btn_copy_vertical":          {"zh_TW":"📋 複製(垂直Excel)", "zh_CN":"📋 复制(垂直Excel)", "en":"📋 Copy (Vertical Excel)", "ja":"📋 コピー(縦Excel)"},
"btn_save_all_props":         {"zh_TW":"💾 儲存所有已填物性", "zh_CN":"💾 保存所有已填物性数据", "en":"💾 Save All Properties", "ja":"💾 全物性データを保存"},
"btn_clear_all_props":        {"zh_TW":"🗑 清空所有物性欄位", "zh_CN":"🗑 清空所有物性栏位", "en":"🗑 Clear All Properties", "ja":"🗑 全物性フィールドをクリア"},
"btn_toggle_expand":          {"zh_TW":"▲▼ 全部展開/折疊", "zh_CN":"▲▼ 全部展开/折叠", "en":"▲▼ Expand/Collapse All", "ja":"▲▼ 全て展開/折畳"},
"mode_stoich":                {"zh_TW":"stoich (按當量配比)", "zh_CN":"stoich (按当量配比)", "en":"stoich (Stoichiometric)", "ja":"stoich (当量比)"},
"mode_weight":                {"zh_TW":"weight (按樹脂總量百分比)", "zh_CN":"weight (按树脂总量百分比)", "en":"weight (Wt% of Resin)", "ja":"weight (樹脂質量比)"},
"mode_target100":             {"zh_TW":"target_100 (目標總重 100g)", "zh_CN":"target_100 (目标总重 100g)", "en":"target_100 (Target 100g)", "ja":"target_100 (目標100g)"},
"mode_phr100":               {"zh_TW":"phr_100 (樹脂百份計算)", "zh_CN":"phr_100 (树脂百份计算)", "en":"phr_100 (Resin 100-Part)", "ja":"phr_100 (樹脂百部法)"},
"round_none":                 {"zh_TW":"不取整", "zh_CN":"不取整", "en":"No Round", "ja":"丸めなし"},
"round_int":                  {"zh_TW":"整數", "zh_CN":"整数", "en":"Integer", "ja":"整数"},
"round_1dp":                  {"zh_TW":"1位小數", "zh_CN":"1位小数", "en":"1 d.p.", "ja":"小数1桁"},
"round_2dp":                  {"zh_TW":"2位小數", "zh_CN":"2位小数", "en":"2 d.p.", "ja":"小数2桁"},
"col_mat_name":               {"zh_TW":"物料名稱", "zh_CN":"物料名称", "en":"Material Name", "ja":"材料名"},
"col_mass_g_result":          {"zh_TW":"質量 (g)", "zh_CN":"质量 (g)", "en":"Mass (g)", "ja":"質量 (g)"},
"col_pct_result":             {"zh_TW":"佔比 (%)", "zh_CN":"占比 (%)", "en":"Ratio (%)", "ja":"配合比 (%)"},
"col_cl_result":              {"zh_TW":"氯 (ppm)", "zh_CN":"氯 (ppm)", "en":"Cl (ppm)", "ja":"塩素 (ppm)"},
"total":                      {"zh_TW":"總計", "zh_CN":"总计", "en":"Total", "ja":"合計"},
"copy_hdr":                   {"zh_TW":"物料名稱\t質量 (g)\t佔比 (%)\t氯含量 (ppm)", "zh_CN":"物料名称\t质量 (g)\t占比 (%)\t氯含量 (ppm)", "en":"Material\tMass (g)\tRatio (%)\tCl (ppm)", "ja":"材料名\t質量 (g)\t配合比 (%)\t塩素 (ppm)"},
"h_amine":                    {"zh_TW":"胺類", "zh_CN":"胺类", "en":"Amine", "ja":"アミン系"},
"h_polyamide":                {"zh_TW":"聚醯胺", "zh_CN":"聚酰胺", "en":"Polyamide", "ja":"ポリアミド"},
"h_anhydride":                {"zh_TW":"酸酐", "zh_CN":"酸酐", "en":"Anhydride", "ja":"酸無水物"},
"h_mercaptan":                {"zh_TW":"巰基", "zh_CN":"巯基", "en":"Mercaptan", "ja":"メルカプタン"},
"h_hydroxyl":                 {"zh_TW":"羥基", "zh_CN":"羟基", "en":"Hydroxyl", "ja":"水酸基"},
"lbl_amine_value":            {"zh_TW":"胺值:", "zh_CN":"胺值:", "en":"Amine Value:", "ja":"アミン価:"},
"calc_56100_amine":           {"zh_TW":"計算(56100/胺值)", "zh_CN":"计算(56100/胺值)", "en":"Calc (56100/Amine Value)", "ja":"計算(56100/アミン価)"},
"lbl_coeff_f":                {"zh_TW":"係數f:", "zh_CN":"系数f:", "en":"Factor f:", "ja":"係数f:"},
"calc_56100_amine_f":         {"zh_TW":"計算(56100/胺值×f)", "zh_CN":"计算(56100/胺值×f)", "en":"Calc (56100/AV×f)", "ja":"計算(56100/AV×f)"},
"lbl_mw":                     {"zh_TW":"分子量:", "zh_CN":"分子量:", "en":"Mol. Weight:", "ja":"分子量:"},
"lbl_active_h":               {"zh_TW":"活性氫數:", "zh_CN":"活性氢数:", "en":"Active H count:", "ja":"活性水素数:"},
"calc_mw_h":                  {"zh_TW":"計算(MW/活性氫數)", "zh_CN":"计算(MW/活性氢数)", "en":"Calc (MW/Active H)", "ja":"計算(MW/活性水素数)"},
"lbl_acid_value":             {"zh_TW":"酸值:", "zh_CN":"酸值:", "en":"Acid Value:", "ja":"酸価:"},
"calc_56100_acid":            {"zh_TW":"計算(56100/酸值)", "zh_CN":"计算(56100/酸值)", "en":"Calc (56100/AV)", "ja":"計算(56100/酸価)"},
"lbl_anh_groups":             {"zh_TW":"酸酐基數:", "zh_CN":"酸酐基数:", "en":"Anhydride Groups:", "ja":"酸無水物基数:"},
"calc_mw_anh":                {"zh_TW":"計算(MW/酸酐基數)", "zh_CN":"计算(MW/酸酐基数)", "en":"Calc (MW/Anh. Groups)", "ja":"計算(MW/酸無水物基数)"},
"lbl_mercapto_groups":        {"zh_TW":"巰基數:", "zh_CN":"巯基数:", "en":"Mercapto Groups:", "ja":"メルカプト基数:"},
"calc_mw_merc":               {"zh_TW":"計算(MW/巰基數)", "zh_CN":"计算(MW/巯基数)", "en":"Calc (MW/SH Groups)", "ja":"計算(MW/SH基数)"},
"lbl_oh_value":               {"zh_TW":"羥值:", "zh_CN":"羟值:", "en":"Hydroxyl Value:", "ja":"水酸基価:"},
"calc_56100_oh":              {"zh_TW":"計算(56100/羥值)", "zh_CN":"计算(56100/羟值)", "en":"Calc (56100/OHV)", "ja":"計算(56100/OHV)"},
"no_recipe_selected":         {"zh_TW":"（尚未選取配方）", "zh_CN":"（尚未选中配方）", "en":"(No recipe selected)", "ja":"（配合未選択）"},
"current_recipe":             {"zh_TW":"▶ 目前選取：{}", "zh_CN":"▶ 当前选中：{}", "en":"▶ Selected: {}", "ja":"▶ 選択中：{}"},
"search":                     {"zh_TW":"🔍 搜尋:", "zh_CN":"🔍 搜索:", "en":"🔍 Search:", "ja":"🔍 検索:"},
"cat_filter":                 {"zh_TW":"分類過濾:", "zh_CN":"分类过滤:", "en":"Category Filter:", "ja":"カテゴリーフィルター:"},
"all_cats":                   {"zh_TW":"（全部）", "zh_CN":"（全部）", "en":"(All)", "ja":"（全て）"},
"btn_clear_filter":           {"zh_TW":"清除過濾", "zh_CN":"清除过滤", "en":"Clear Filter", "ja":"フィルター解除"},
"total_items":                {"zh_TW":"共 {} 項", "zh_CN":"共 {} 项", "en":"{} items", "ja":"全{}件"},
"add_prop_def":               {"zh_TW":"➕ 新增物性定義", "zh_CN":"➕ 新增物性定义", "en":"➕ Add Property Definition", "ja":"➕ 物性定義を追加"},
"lbl_prop_display":           {"zh_TW":"顯示名稱*:", "zh_CN":"显示名称*:", "en":"Display Name*:", "ja":"表示名*:"},
"lbl_prop_dbkey":             {"zh_TW":"DB Key(英文)*:", "zh_CN":"DB Key(英文)*:", "en":"DB Key*:", "ja":"DBキー(英語)*:"},
"lbl_test_method":            {"zh_TW":"測試方法:", "zh_CN":"测试方法:", "en":"Test Method:", "ja":"試験方法:"},
"lbl_target_cat":             {"zh_TW":"目標分類*:", "zh_CN":"目标分类*:", "en":"Target Category*:", "ja":"対象カテゴリー*:"},
"col_src":                    {"zh_TW":"來源", "zh_CN":"来源", "en":"Source", "ja":"入手先"},
"col_cat":                    {"zh_TW":"分類", "zh_CN":"分类", "en":"Category", "ja":"分類"},
"col_prop_display":           {"zh_TW":"顯示名稱", "zh_CN":"显示名称", "en":"Display Name", "ja":"表示名"},
"col_dbkey":                  {"zh_TW":"DB Key", "zh_CN":"DB Key", "en":"DB Key", "ja":"DBキー"},
"col_method":                 {"zh_TW":"測試方法", "zh_CN":"测试方法", "en":"Test Method", "ja":"試験方法"},
"btn_add_prop":               {"zh_TW":"✅ 新增", "zh_CN":"✅ 新增", "en":"✅ Add", "ja":"✅ 追加"},
"btn_del_prop":               {"zh_TW":"🗑 刪除所選使用者項目", "zh_CN":"🗑 删除选中用户项目", "en":"🗑 Delete Selected User Item", "ja":"🗑 選択ユーザー項目を削除"},
"btn_copy_prop":              {"zh_TW":"📋 複製所選項目到新增欄", "zh_CN":"📋 复制选中项目到新增栏", "en":"📋 Copy Selected to Add Form", "ja":"📋 選択項目を追加欄にコピー"},
"btn_add_cat":               {"zh_TW":"➕ 新增分類", "zh_CN":"➕ 新增分类", "en":"➕ Add Category", "ja":"➕ カテゴリー追加"},
"btn_del_cat":               {"zh_TW":"🗑 刪除自訂分類", "zh_CN":"🗑 删除自定义分类", "en":"🗑 Del Category", "ja":"🗑 カテゴリー削除"},
"lbl_unit":                   {"zh_TW":"單位:", "zh_CN":"单位:", "en":"Unit:", "ja":"単位:"},
"2k_mixed_eew":              {"zh_TW":"A 側混合 EEW:", "zh_CN":"A 侧混合 EEW:", "en":"A-Side Mixed EEW:", "ja":"A側混合EEW:"},
"2k_total_eq":               {"zh_TW":"A 側環氧當量數:", "zh_CN":"A 侧环氧当量数:", "en":"A-Side Epoxy Eq.:", "ja":"A側エポキシ当量:"},
"2k_total_a":                {"zh_TW":"Part A 總質量:", "zh_CN":"Part A 总质量:", "en":"Part A Total:", "ja":"Part A 総質量:"},
"2k_total_b":                {"zh_TW":"Part B 總質量:", "zh_CN":"Part B 总质量:", "en":"Part B Total:", "ja":"Part B 総質量:"},
"2k_ratio_wt":               {"zh_TW":"混合比 A:B (重量):", "zh_CN":"混合比 A:B (重量):", "en":"Mix Ratio A:B (wt):", "ja":"混合比 A:B (重量):"},
"2k_ratio_simple":           {"zh_TW":"簡化比:", "zh_CN":"简化比:", "en":"Simplified:", "ja":"簡略化:"},
"2k_total_mixed":            {"zh_TW":"混合總質量:", "zh_CN":"混合总质量:", "en":"Mixed Total:", "ja":"混合総質量:"},
"2k_total_cl":               {"zh_TW":"混合氯含量:", "zh_CN":"混合氯含量:", "en":"Mixed Cl:", "ja":"混合塩素:"},
"2k_col_side":               {"zh_TW":"側", "zh_CN":"侧", "en":"Side", "ja":"側"},
"2k_col_cat":                {"zh_TW":"類別", "zh_CN":"类别", "en":"Category", "ja":"分類"},
"2k_col_name":               {"zh_TW":"物料名稱", "zh_CN":"物料名称", "en":"Material", "ja":"材料名"},
"2k_col_mass":               {"zh_TW":"質量(g)", "zh_CN":"质量(g)", "en":"Mass(g)", "ja":"質量(g)"},
"2k_col_eq":                 {"zh_TW":"EEW/AHEW", "zh_CN":"EEW/AHEW", "en":"EEW/AHEW", "ja":"EEW/AHEW"},
"2k_col_phr":                {"zh_TW":"phr", "zh_CN":"phr", "en":"phr", "ja":"phr"},
"2k_col_pct_side":           {"zh_TW":"側內%", "zh_CN":"侧内%", "en":"Side%", "ja":"側内%"},
"2k_col_pct_total":          {"zh_TW":"總%", "zh_CN":"总%", "en":"Total%", "ja":"総%"},
"2k_col_cl":                 {"zh_TW":"氯(ppm)", "zh_CN":"氯(ppm)", "en":"Cl(ppm)", "ja":"塩素(ppm)"},
"2k_sub_a":                  {"zh_TW":"小計 Part A", "zh_CN":"小计 Part A", "en":"Subtotal A", "ja":"小計 Part A"},
"2k_sub_b":                  {"zh_TW":"小計 Part B", "zh_CN":"小计 Part B", "en":"Subtotal B", "ja":"小計 Part B"},
"2k_grand_total":            {"zh_TW":"A+B 合計", "zh_CN":"A+B 合计", "en":"A+B Total", "ja":"A+B 合計"},
"detail_recipe_fmt":          {"zh_TW":"配方：{}", "zh_CN":"配方：{}", "en":"Recipe: {}", "ja":"配合：{}"},
"detail_batch_fmt":           {"zh_TW":"批次號：{}", "zh_CN":"批次号：{}", "en":"Batch No.: {}", "ja":"ロット番号：{}"},
"detail_date_mode":           {"zh_TW":"日期：{}   模式：{}", "zh_CN":"日期：{}   模式：{}", "en":"Date: {}   Mode: {}", "ja":"日付：{}   モード：{}"},
"detail_total":               {"zh_TW":"總質量：", "zh_CN":"总质量：", "en":"Total Mass: ", "ja":"総質量："},
"detail_total_cl":            {"zh_TW":"{} g    氯：{} ppm", "zh_CN":"{} g    氯：{} ppm", "en":"{} g    Cl: {} ppm", "ja":"{} g    塩素：{} ppm"},
"2k_detail_hdr":             {"zh_TW":"─── 2K 配方資訊 ───", "zh_CN":"─── 2K 配方信息 ───", "en":"─── 2K Info ───", "ja":"─── 2K 配合情報 ───"},
"2k_detail_meew":            {"zh_TW":"  A 側混合 EEW: {}", "zh_CN":"  A 侧混合 EEW: {}", "en":"  A-Side Mixed EEW: {}", "ja":"  A側混合EEW: {}"},
"2k_detail_stoich":          {"zh_TW":"  當量比: {}%", "zh_CN":"  当量比: {}%", "en":"  Stoich: {}%", "ja":"  当量比: {}%"},
"2k_detail_ratio":           {"zh_TW":"  混合比 A:B = {}", "zh_CN":"  混合比 A:B = {}", "en":"  Mix Ratio A:B = {}", "ja":"  混合比 A:B = {}"},
"2k_detail_side":            {"zh_TW":"[{}側]", "zh_CN":"[{}侧]", "en":"[{} Side]", "ja":"[{}側]"},
"detail_eq":                  {"zh_TW":"  當量={}  {}", "zh_CN":"  当量={}  {}", "en":"  Eq.={}  {}", "ja":"  当量={}  {}"},
"copy_recipe_hdr_name":       {"zh_TW":"配方名稱", "zh_CN":"配方名称", "en":"Recipe Name", "ja":"配合名"},
"copy_recipe_hdr_batch":      {"zh_TW":"批次號", "zh_CN":"批次号", "en":"Batch No.", "ja":"ロット番号"},
"copy_recipe_hdr_mat":        {"zh_TW":"物料名稱\t質量(g)\t佔比(%)", "zh_CN":"物料名称\t质量(g)\t占比(%)", "en":"Material\tMass(g)\tRatio(%)", "ja":"材料名\t質量(g)\t配合比(%)"},
"copy_recipe_hdr_prop":       {"zh_TW":"物性項目\t數值", "zh_CN":"物性项目\t数值", "en":"Property\tValue", "ja":"物性項目\t値"},
"copy_ok_title":              {"zh_TW":"完成", "zh_CN":"完成", "en":"Done", "ja":"完了"},
"ratio_pending":              {"zh_TW":"比例份數", "zh_CN":"比例份数", "en":"Ratio Parts", "ja":"比率パーツ"},
"err_over_100g":              {"zh_TW":"基材總質量超過100g限制或為零", "zh_CN":"基材总质量超过100g限制或为零", "en":"Base mass exceeds 100g limit or is zero", "ja":"基材の総質量が100gの制限を超えるかゼロです"},
"err_ratio_not_100g":         {"zh_TW":"比例模式僅適用於 target_100 計算模式", "zh_CN":"比例模式仅适用于 target_100 计算模式", "en":"Ratio mode is only available in target_100 mode", "ja":"比率モードはtarget_100モードでのみ使用可能です"},
"err_coeff_zero":             {"zh_TW":"比例係數計算結果為零，無法配平", "zh_CN":"比例系数计算结果为零，无法配平", "en":"Ratio coefficient is zero, cannot balance", "ja":"比率係数がゼロのため配合できません"},
"search_placeholder":         {"zh_TW":"輸入關鍵字...", "zh_CN":"输入关键字...", "en":"Enter keyword...", "ja":"キーワードを入力..."},
"warn_name_empty":            {"zh_TW":"名稱不可為空", "zh_CN":"名称不可为空", "en":"Name cannot be empty", "ja":"名称は空にできません"},
"confirm_del_mat":            {"zh_TW":"確定要刪除物料 [{}] 嗎？", "zh_CN":"确定要删除物料 [{}] 吗？", "en":"Delete material [{}]?", "ja":"材料 [{}] を削除しますか？"},
"confirm_del_recipe":         {"zh_TW":"確定要刪除配方 [{}] 嗎？", "zh_CN":"确定要删除配方 [{}] 吗？", "en":"Delete recipe [{}]?", "ja":"配合 [{}] を削除しますか？"},
"col_mgr_hint":               {"zh_TW":"欄位管理功能可透過 JSON 設定檔調整，或在此擴充 UI。", "zh_CN":"栏位管理功能可通过 JSON 配置文件调整，或在此扩展 UI。", "en":"Column management can be configured via JSON config file, or UI can be extended here.", "ja":"列管理はJSON設定ファイルで調整するか、ここでUI拡張が可能です。"},
"save_failed":                {"zh_TW":"儲存失敗", "zh_CN":"保存失败", "en":"Save failed", "ja":"保存に失敗しました"},
"rename_title":               {"zh_TW":"重新命名", "zh_CN":"重命名", "en":"Rename", "ja":"名前変更"},
"rename_prompt":              {"zh_TW":"請輸入 [{}] 的新名稱：", "zh_CN":"请输入 [{}] 的新名称：", "en":"Enter new name for [{}]:", "ja":"[{}] の新しい名前を入力してください："},
"warn_name_exists":           {"zh_TW":"名稱已存在", "zh_CN":"名称已存在", "en":"Name already exists", "ja":"名前は既に存在します"},
"err_part_a_zero":            {"zh_TW":"Part A 樹脂總量必須大於0", "zh_CN":"Part A 树脂总量必须大于0", "en":"Part A resin total must be > 0", "ja":"Part A 樹脂の総量は0より大きい必要があります"},
"add_custom_prefix":          {"zh_TW":"+ 添加", "zh_CN":"+ 添加", "en":"+ Add ", "ja":"+ 追加"},
"btn_tools":                  {"zh_TW":"🔬 工具", "zh_CN":"🔬 工具", "en":"🔬 Tools", "ja":"🔬 ツール"},
"tool_gel_time":              {"zh_TW":"凝膠時間估算", "zh_CN":"凝胶时间估算", "en":"Gel Time Estimator", "ja":"ゲルタイム推定"},
"tool_tg_predict":            {"zh_TW":"DiBenedetto Tg 預測", "zh_CN":"DiBenedetto Tg 预测", "en":"DiBenedetto Tg Prediction", "ja":"DiBenedetto Tg 予測"},
"tool_hardener_type":         {"zh_TW":"固化劑類型:", "zh_CN":"固化剂类型:", "en":"Hardener Type:", "ja":"硬化剤タイプ:"},
"tool_cure_temp":             {"zh_TW":"固化溫度 (°C):", "zh_CN":"固化温度 (°C):", "en":"Cure Temp (°C):", "ja":"硬化温度 (°C):"},
"tool_ea":                    {"zh_TW":"活化能 Ea (kJ/mol):", "zh_CN":"活化能 Ea (kJ/mol):", "en":"Ea (kJ/mol):", "ja":"活性化エネルギー (kJ/mol):"},
"tool_ln_a":                  {"zh_TW":"指前因子 ln(A):", "zh_CN":"指前因子 ln(A):", "en":"ln(A):", "ja":"頻度因子 ln(A):"},
"tool_batch_mass":            {"zh_TW":"批量 (g):", "zh_CN":"批量 (g):", "en":"Batch Mass (g):", "ja":"バッチ量 (g):"},
"tool_tg0":                   {"zh_TW":"Tg₀ 未固化 (°C):", "zh_CN":"Tg₀ 未固化 (°C):", "en":"Tg₀ uncured (°C):", "ja":"Tg₀ 未硬化 (°C):"},
"tool_tg_inf":                {"zh_TW":"Tg∞ 完全固化 (°C):", "zh_CN":"Tg∞ 完全固化 (°C):", "en":"Tg∞ fully cured (°C):", "ja":"Tg∞ 完全硬化 (°C):"},
"tool_lambda":                {"zh_TW":"λ 形狀參數:", "zh_CN":"λ 形状参数:", "en":"λ shape param:", "ja":"λ 形状パラメータ:"},
"tool_alpha":                 {"zh_TW":"轉化率 α:", "zh_CN":"转化率 α:", "en":"Conversion α:", "ja":"転化率 α:"},
"tool_result":                {"zh_TW":"計算結果", "zh_CN":"计算结果", "en":"Result", "ja":"計算結果"},
"tool_dual_cure":             {"zh_TW":"UV-熱雙固化", "zh_CN":"UV-热双固化", "en":"UV-Thermal Dual Cure", "ja":"UV-熱デュアル硬化"},
"tool_dsc_parser":            {"zh_TW":"DSC/TGA 解析", "zh_CN":"DSC/TGA 解析", "en":"DSC/TGA Parser", "ja":"DSC/TGA 解析"},
"tool_uv_pi":                 {"zh_TW":"光起始劑 (phr):", "zh_CN":"光引发剂 (phr):", "en":"Photoinitiator (phr):", "ja":"光開始剤 (phr):"},
"tool_uv_dose":               {"zh_TW":"UV 劑量 (mJ/cm²):", "zh_CN":"UV 剂量 (mJ/cm²):", "en":"UV Dose (mJ/cm²):", "ja":"UV照射量 (mJ/cm²):"},
"tool_thermal_ti":            {"zh_TW":"熱起始劑 (phr):", "zh_CN":"热引发剂 (phr):", "en":"Thermal Initiator (phr):", "ja":"熱開始剤 (phr):"},
"tool_uv_conv":               {"zh_TW":"UV 階段轉化率:", "zh_CN":"UV 阶段转化率:", "en":"UV-stage conversion:", "ja":"UV段階転化率:"},
"tool_thermal_conv":          {"zh_TW":"熱階段轉化率:", "zh_CN":"热阶段转化率:", "en":"Thermal conversion:", "ja":"熱段階転化率:"},
"tool_load_csv":              {"zh_TW":"📂 載入 CSV", "zh_CN":"📂 加载 CSV", "en":"📂 Load CSV", "ja":"📂 CSV読込"},
"tool_dsc_ti":                {"zh_TW":"起始溫度 Ti:", "zh_CN":"起始温度 Ti:", "en":"Onset Ti:", "ja":"開始温度 Ti:"},
"tool_dsc_tp":                {"zh_TW":"峰溫度 Tp:", "zh_CN":"峰温度 Tp:", "en":"Peak Tp:", "ja":"ピーク温度 Tp:"},
"tool_dsc_dh":                {"zh_TW":"反應熱 ΔH:", "zh_CN":"反应热 ΔH:", "en":"ΔH:", "ja":"反応熱 ΔH:"},
"tool_dsc_ea":                {"zh_TW":"活化能 Ea:", "zh_CN":"活化能 Ea:", "en":"Ea:", "ja":"活性化エネルギー:"},
"tool_cat_coeff":             {"zh_TW":"催化均聚係數:", "zh_CN":"催化均聚系数:", "en":"Catalyst Homo. Coeff:", "ja":"触媒ホモ重合係数:"},
"tool_cat_coeff_hint":        {"zh_TW":"酸酐/潛伏性體系的環氧均聚比例 (0~0.3)", "zh_CN":"酸酐/潜伏性体系的环氧均聚比例 (0~0.3)", "en":"Epoxy homopolymerization fraction for anhydride/latent (0~0.3)", "ja":"酸無水物/潜在系のエポキシホモ重合比率 (0~0.3)"},
"tool_cte":                   {"zh_TW":"CTE 預測", "zh_CN":"CTE 预测", "en":"CTE Prediction", "ja":"CTE 予測"},
"tool_thermal_k":             {"zh_TW":"導熱係數預測", "zh_CN":"导热系数预测", "en":"Thermal Conductivity", "ja":"熱伝導率予測"},
"tool_elec":                  {"zh_TW":"導電/絕緣預測", "zh_CN":"导电/绝缘预测", "en":"Electrical Prediction", "ja":"電気特性予測"},
"tool_resin_cte":             {"zh_TW":"樹脂基體 CTE (ppm/°C):", "zh_CN":"树脂基体 CTE (ppm/°C):", "en":"Resin matrix CTE (ppm/°C):", "ja":"樹脂マトリックス CTE (ppm/°C):"},
"tool_filler_cte":            {"zh_TW":"填料 CTE (ppm/°C):", "zh_CN":"填料 CTE (ppm/°C):", "en":"Filler CTE (ppm/°C):", "ja":"フィラー CTE (ppm/°C):"},
"tool_filler_vf":             {"zh_TW":"填料體積分率 φ:", "zh_CN":"填料体积分率 φ:", "en":"Filler vol fraction φ:", "ja":"フィラー体積分率 φ:"},
"tool_resin_k":               {"zh_TW":"樹脂導熱 (W/m·K):", "zh_CN":"树脂导热 (W/m·K):", "en":"Resin k (W/m·K):", "ja":"樹脂熱伝導率 (W/m·K):"},
"tool_filler_k":              {"zh_TW":"填料導熱 (W/m·K):", "zh_CN":"填料导热 (W/m·K):", "en":"Filler k (W/m·K):", "ja":"フィラー熱伝導率 (W/m·K):"},
"tool_resin_rho":             {"zh_TW":"樹脂電阻率 (Ω·cm):", "zh_CN":"树脂电阻率 (Ω·cm):", "en":"Resin ρ (Ω·cm):", "ja":"樹脂抵抗率 (Ω·cm):"},
"tool_filler_rho_e":          {"zh_TW":"填料電阻率 (Ω·cm):", "zh_CN":"填料电阻率 (Ω·cm):", "en":"Filler ρ (Ω·cm):", "ja":"フィラー抵抗率 (Ω·cm):"},
"tool_perc_thresh":           {"zh_TW":"滲流閾值 φc:", "zh_CN":"渗流阈值 φc:", "en":"Percolation threshold φc:", "ja":"パーコレーション閾値 φc:"},
"lbl_cte_ppm":                {"zh_TW":"CTE (ppm/°C):", "zh_CN":"CTE (ppm/°C):", "en":"CTE (ppm/°C):", "ja":"CTE (ppm/°C):"},
"lbl_thermal_cond":           {"zh_TW":"導熱率 (W/m·K):", "zh_CN":"导热率 (W/m·K):", "en":"Thermal Cond. (W/m·K):", "ja":"熱伝導率 (W/m·K):"},
"lbl_elec_resistivity":       {"zh_TW":"電阻率 (Ω·cm):", "zh_CN":"电阻率 (Ω·cm):", "en":"Resistivity (Ω·cm):", "ja":"抵抗率 (Ω·cm):"},
"tool_hdr_arrhenius":         {"zh_TW":"Arrhenius: k = A·exp(-Eₐ/RT)", "zh_CN":"Arrhenius: k = A·exp(-Eₐ/RT)", "en":"Arrhenius: k = A·exp(-Eₐ/RT)", "ja":"Arrhenius: k = A·exp(-Eₐ/RT)"},
"tool_hdr_dibenedetto":       {"zh_TW":"Tg = Tg₀ + (Tg∞−Tg₀)·λα / [1−(1−λ)α]", "zh_CN":"Tg = Tg₀ + (Tg∞−Tg₀)·λα / [1−(1−λ)α]", "en":"Tg = Tg₀ + (Tg∞−Tg₀)·λα / [1−(1−λ)α]", "ja":"Tg = Tg₀ + (Tg∞−Tg₀)·λα / [1−(1−λ)α]"},
"tool_hdr_dualcure":          {"zh_TW":"UV預固化支架 + 熱後固化", "zh_CN":"UV预固化支架 + 热后固化", "en":"UV scaffold + thermal post-cure", "ja":"UVプレ硬化 + 熱ポスト硬化"},
"tool_hdr_dualcure_sub":      {"zh_TW":"UV 階段形成預固化支架，熱階段完成環氧交聯", "zh_CN":"UV 阶段形成预固化支架，热阶段完成环氧交联", "en":"UV stage forms scaffold, thermal stage completes epoxy crosslinking", "ja":"UV段階でスキャフォールドを形成し、熱段階でエポキシ架橋を完了"},
"tool_hdr_dsc":               {"zh_TW":"DSC/TGA CSV 數據 → Ti, Tp, ΔH, Ea", "zh_CN":"DSC/TGA CSV 数据 → Ti, Tp, ΔH, Ea", "en":"DSC/TGA CSV data → Ti, Tp, ΔH, Ea", "ja":"DSC/TGA CSVデータ → Ti, Tp, ΔH, Ea"},
"tool_hdr_cte":               {"zh_TW":"Turner / Schapery / ML", "zh_CN":"Turner / Schapery / ML", "en":"Turner / Schapery / ML", "ja":"Turner / Schapery / ML"},
"tool_hdr_thermal_k":         {"zh_TW":"Maxwell / Bruggeman / Lewis-Nielsen / ML", "zh_CN":"Maxwell / Bruggeman / Lewis-Nielsen / ML", "en":"Maxwell / Bruggeman / Lewis-Nielsen / ML", "ja":"Maxwell / Bruggeman / Lewis-Nielsen / ML"},
"tool_hdr_elec":              {"zh_TW":"滲流 / GEM / ML", "zh_CN":"渗流 / GEM / ML", "en":"Percolation / GEM / ML", "ja":"パーコレーション / GEM / ML"},
"tooltip_eq_ratio":           {"zh_TW":"佔總當量的比例", "zh_CN":"占总当量的比例", "en":"Proportion of total equivalents", "ja":"総当量に対する割合"},
"tooltip_corr_coeff":         {"zh_TW":"固化劑校正係數 (C)", "zh_CN":"固化剂校正系数 (C)", "en":"Hardener correction factor (C)", "ja":"硬化剤補正係数 (C)"},
"2k_copy_hdr":               {"zh_TW":"側\t類別\t物料名稱\t質量(g)\tEEW/AHEW\tphr\t側內%\t總%\t氯(ppm)", "zh_CN":"侧\t类别\t物料名称\t质量(g)\tEEW/AHEW\tphr\t侧内%\t总%\t氯(ppm)", "en":"Side\tCategory\tMaterial\tMass(g)\tEEW/AHEW\tphr\tSide%\tTotal%\tCl(ppm)", "ja":"側\t分類\t材料名\t質量(g)\tEEW/AHEW\tphr\t側内%\t総%\t塩素(ppm)"},
"batch_scale":               {"zh_TW":"投料校正 %:", "zh_CN":"投料校正 %:", "en":"Batch Scale %:", "ja":"仕込み補正 %:"},
"col_scaled":                {"zh_TW":"投料量(g)", "zh_CN":"投料量(g)", "en":"Scaled(g)", "ja":"仕込み量(g)"},
"col_formula":               {"zh_TW":"計算公式", "zh_CN":"计算公式", "en":"Formula", "ja":"計算式"},
"col_eq_val":                {"zh_TW":"EEW/AHEW", "zh_CN":"EEW/AHEW", "en":"EEW/AHEW", "ja":"EEW/AHEW"},
"col_type":                  {"zh_TW":"類型", "zh_CN":"类型", "en":"Type", "ja":"タイプ"},
"col_category":              {"zh_TW":"類別", "zh_CN":"类别", "en":"Category", "ja":"分類"},
"export_title":              {"zh_TW":"📋 匯出預覽", "zh_CN":"📋 导出预览", "en":"📋 Export Preview", "ja":"📋 エクスポートプレビュー"},
"export_cols":               {"zh_TW":"可選欄位:", "zh_CN":"可选列:", "en":"Optional Columns:", "ja":"オプション列:"},
"export_copy":               {"zh_TW":"📋 複製到剪貼簿", "zh_CN":"📋 复制到剪贴板", "en":"📋 Copy to Clipboard", "ja":"📋 クリップボードにコピー"},
"export_drag_hint":          {"zh_TW":"💡 拖動列即可調整排序", "zh_CN":"💡 拖动行即可调整排序", "en":"💡 Drag rows to reorder", "ja":"💡 行をドラッグして並べ替え"},
"formula_direct":            {"zh_TW":"直接輸入", "zh_CN":"直接输入", "en":"Direct input", "ja":"直接入力"},
"formula_stoich":            {"zh_TW":"Σ(樹脂/EEW)×{ratio}×AHEW({eq})×C({corr})={mass}g", "zh_CN":"Σ(树脂/EEW)×{ratio}×AHEW({eq})×C({corr})={mass}g", "en":"Σ(R/EEW)×{ratio}×AHEW({eq})×C({corr})={mass}g", "ja":"Σ(樹脂/EEW)×{ratio}×AHEW({eq})×C({corr})={mass}g"},
"formula_weight":            {"zh_TW":"Σ樹脂({base}g)×{pct}%×C({corr})={mass}g", "zh_CN":"Σ树脂({base}g)×{pct}%×C({corr})={mass}g", "en":"ΣResin({base}g)×{pct}%×C({corr})={mass}g", "ja":"Σ樹脂({base}g)×{pct}%×C({corr})={mass}g"},
"formula_t100_scale":        {"zh_TW":"{orig}g×SF({sf:.4f})={mass}g (配平至100g)", "zh_CN":"{orig}g×SF({sf:.4f})={mass}g (配平至100g)", "en":"{orig}g×SF({sf:.4f})={mass}g (norm to 100g)", "ja":"{orig}g×SF({sf:.4f})={mass}g (100g正規化)"},
"formula_t100_extra":        {"zh_TW":"額外添加 {val}g", "zh_CN":"额外添加 {val}g", "en":"Extra add {val}g", "ja":"追加 {val}g"},
"formula_phr_resin":         {"zh_TW":"{parts}份 (×SF={mass:.4f}g)", "zh_CN":"{parts}份 (×SF={mass:.4f}g)", "en":"{parts} parts (×SF={mass:.4f}g)", "ja":"{parts}部 (×SF={mass:.4f}g)"},
"formula_phr_hardener":      {"zh_TW":"Σ(R/EEW)×{ratio}×AHEW({eq})×C({corr})={mass:.4f}g", "zh_CN":"Σ(R/EEW)×{ratio}×AHEW({eq})×C({corr})={mass:.4f}g", "en":"Σ(R/EEW)×{ratio}×AHEW({eq})×C({corr})={mass:.4f}g", "ja":"Σ(R/EEW)×{ratio}×AHEW({eq})×C({corr})={mass:.4f}g"},
"formula_phr_extra":         {"zh_TW":"(R+H){base:.2f}g×{pct}%={mass:.4f}g", "zh_CN":"(R+H){base:.2f}g×{pct}%={mass:.4f}g", "en":"(R+H){base:.2f}g×{pct}%={mass:.4f}g", "ja":"(R+H){base:.2f}g×{pct}%={mass:.4f}g"},
"2k_mode":                   {"zh_TW":"計算模式:", "zh_CN":"计算模式:", "en":"Calc Mode:", "ja":"計算モード:"},
"2k_mode_free":              {"zh_TW":"自由計算 (直接輸入質量)", "zh_CN":"自由计算 (直接输入质量)", "en":"Free Calc (Direct Mass)", "ja":"自由計算 (直接入力)"},
"2k_mode_ratio":             {"zh_TW":"配比計算 (份數+目標比例)", "zh_CN":"配比计算 (份数+目标比例)", "en":"Ratio Calc (Parts+Target)", "ja":"比率計算 (部数+目標比率)"},
"visc_predict":              {"zh_TW":"📊 黏度預測", "zh_CN":"📊 粘度预测", "en":"📊 Viscosity Prediction", "ja":"📊 粘度予測"},
"visc_result":               {"zh_TW":"預測黏度 (25°C):", "zh_CN":"预测粘度 (25°C):", "en":"Predicted Viscosity (25°C):", "ja":"予測粘度 (25°C):"},
"visc_unit":                 {"zh_TW":"cP", "zh_CN":"cP", "en":"cP", "ja":"cP"},
"visc_confidence":           {"zh_TW":"信心度:", "zh_CN":"信心度:", "en":"Confidence:", "ja":"信頼度:"},
"visc_conf_high":            {"zh_TW":"● 高 — ML集成+物理模型校正", "zh_CN":"● 高 — ML集成+物理模型校正", "en":"● High — ML ensemble + physics calibrated", "ja":"● 高 — MLアンサンブル+物理校正済み"},
"visc_conf_medium":          {"zh_TW":"● 中 — 預測可參考", "zh_CN":"● 中 — 预测可参考", "en":"● Medium — reasonable estimate", "ja":"● 中 — 参考値"},
"visc_conf_low":             {"zh_TW":"● 低 — 部分物料缺數據(已自動推算)", "zh_CN":"● 低 — 部分物料缺数据(已自动推算)", "en":"● Low — some data imputed", "ja":"● 低 — 一部データ推算"},
"visc_conf_none":            {"zh_TW":"● 無法預測 — 無黏度資料", "zh_CN":"● 无法预测 — 无粘度数据", "en":"● N/A — no viscosity data", "ja":"● 予測不可 — データなし"},
"visc_missing":              {"zh_TW":"缺黏度資料:", "zh_CN":"缺粘度数据:", "en":"Missing viscosity:", "ja":"粘度データ不足:"},
"visc_detail":               {"zh_TW":"📝 計算詳情", "zh_CN":"📝 计算详情", "en":"📝 Calculation Detail", "ja":"📝 計算詳細"},
"visc_settings":             {"zh_TW":"⚙ 模型參數", "zh_CN":"⚙ 模型参数", "en":"⚙ Model Parameters", "ja":"⚙ モデルパラメータ"},
"visc_phi_max":              {"zh_TW":"φ_max (最大堆積):", "zh_CN":"φ_max (最大堆积):", "en":"φ_max (Max Packing):", "ja":"φ_max (最大充填):"},
"visc_intrinsic":            {"zh_TW":"[η] (本徵黏度):", "zh_CN":"[η] (本征粘度):", "en":"[η] (Intrinsic Visc.):", "ja":"[η] (固有粘度):"},
"visc_filler_rho":           {"zh_TW":"填料密度 g/cm³:", "zh_CN":"填料密度 g/cm³:", "en":"Filler Density g/cm³:", "ja":"フィラー密度 g/cm³:"},
"visc_liquid_rho":           {"zh_TW":"液相密度 g/cm³:", "zh_CN":"液相密度 g/cm³:", "en":"Liquid Density g/cm³:", "ja":"液相密度 g/cm³:"},
"visc_ti":                   {"zh_TW":"觸變指數 TI:", "zh_CN":"触变指数 TI:", "en":"Thixotropic Index:", "ja":"チクソトロピー指数:"},
"visc_state":                {"zh_TW":"常溫狀態:", "zh_CN":"常温状态:", "en":"RT State:", "ja":"常温状態:"},
"state_liquid":              {"zh_TW":"液態", "zh_CN":"液态", "en":"Liquid", "ja":"液体"},
"state_paste":               {"zh_TW":"膏狀", "zh_CN":"膏状", "en":"Paste", "ja":"ペースト"},
"state_solid":               {"zh_TW":"固態/半固態", "zh_CN":"固态/半固态", "en":"Solid/Semi-solid", "ja":"固体/半固体"},
"state_unknown":             {"zh_TW":"未知", "zh_CN":"未知", "en":"Unknown", "ja":"不明"},
"lbl_density":               {"zh_TW":"密度 g/cm³:", "zh_CN":"密度 g/cm³:", "en":"Density g/cm³:", "ja":"密度 g/cm³:"},
"lbl_particle_size":         {"zh_TW":"粒徑 D50 (μm):", "zh_CN":"粒径 D50 (μm):", "en":"Particle Size D50 (μm):", "ja":"粒径 D50 (μm):"},
"lbl_ssa":                   {"zh_TW":"比表面積 BET (m²/g):", "zh_CN":"比表面积 BET (m²/g):", "en":"SSA BET (m²/g):", "ja":"比表面積 BET (m²/g):"},
"lbl_particle_shape":        {"zh_TW":"粒子形態:", "zh_CN":"粒子形态:", "en":"Particle Shape:", "ja":"粒子形状:"},
"lbl_oil_absorption":        {"zh_TW":"吸油量 (ml/100g):", "zh_CN":"吸油量 (ml/100g):", "en":"Oil Absorption (ml/100g):", "ja":"吸油量 (ml/100g):"},
"lbl_mohs":                  {"zh_TW":"莫氏硬度:", "zh_CN":"莫氏硬度:", "en":"Mohs Hardness:", "ja":"モース硬度:"},
"lbl_refractive_index":      {"zh_TW":"折射率:", "zh_CN":"折射率:", "en":"Refractive Index:", "ja":"屈折率:"},
"shape_sphere":              {"zh_TW":"球形", "zh_CN":"球形", "en":"Spherical", "ja":"球状"},
"shape_irregular":           {"zh_TW":"不規則", "zh_CN":"不规则", "en":"Irregular", "ja":"不定形"},
"shape_platelet":            {"zh_TW":"片狀", "zh_CN":"片状", "en":"Platelet", "ja":"板状"},
"shape_fiber":               {"zh_TW":"纖維狀", "zh_CN":"纤维状", "en":"Fiber", "ja":"繊維状"},
"shape_fumed":               {"zh_TW":"氣相法(鏈狀聚集)", "zh_CN":"气相法(链状聚集)", "en":"Fumed (chain aggregate)", "ja":"フュームド(鎖状凝集)"},
"tab_home":                  {"zh_TW":"🏠 首頁", "zh_CN":"🏠 首页", "en":"🏠 Home", "ja":"🏠 ホーム"},
"home_db_section":           {"zh_TW":"📂 資料庫設定", "zh_CN":"📂 数据库设置", "en":"📂 Database Settings", "ja":"📂 データベース設定"},
"home_mat_db":               {"zh_TW":"物料資料庫:", "zh_CN":"物料数据库:", "en":"Material Database:", "ja":"材料データベース:"},
"home_recipe_db":            {"zh_TW":"配方資料庫:", "zh_CN":"配方数据库:", "en":"Recipe Database:", "ja":"配合データベース:"},
"home_browse":               {"zh_TW":"瀏覽…", "zh_CN":"浏览…", "en":"Browse…", "ja":"参照…"},
"home_reload":               {"zh_TW":"🔄 重新載入資料庫", "zh_CN":"🔄 重新加载数据库", "en":"🔄 Reload Database", "ja":"🔄 データベース再読込"},
"home_appearance":           {"zh_TW":"🎨 外觀設定", "zh_CN":"🎨 外观设置", "en":"🎨 Appearance", "ja":"🎨 外観設定"},
"home_accent_color":         {"zh_TW":"主題色", "zh_CN":"主题色", "en":"Accent Color", "ja":"テーマカラー"},
"home_language":             {"zh_TW":"🌐 語言", "zh_CN":"🌐 语言", "en":"🌐 Language", "ja":"🌐 言語"},
"home_about":                {"zh_TW":"工欲善其事，必先利其器\n專為環氧調校，或能延伸至其他熱固性 / 光固化 / PU 等配方系統", "zh_CN":"工欲善其事，必先利其器\n专为环氧调校，或能延伸至其他热固性 / 光固化 / PU 等配方体系", "en":"Sharpen your axe before you chop wood\nTuned for epoxy; may extend to other thermoset / UV-curable / PU formulation systems", "ja":"良工まずその刀を利くし、能書は必ず好筆を用う\nエポキシ向けに調整；他の熱硬化性 / UV硬化型 / PU 系配合にも応用できる可能性あり"},
"home_motto":                {"zh_TW":"工欲善其事，必先利其器", "zh_CN":"工欲善其事，必先利其器", "en":"Sharpen your axe before you chop wood", "ja":"良工まずその刀を利くし、能書は必ず好筆を用う"},
"home_tagline":              {"zh_TW":"專為環氧調校，或能延伸至其他熱固性 / 光固化 / PU 等配方系統", "zh_CN":"专为环氧调校，或能延伸至其他热固性 / 光固化 / PU 等配方体系", "en":"Tuned for epoxy; may extend to other thermoset / UV-curable / PU formulation systems", "ja":"エポキシ向けに調整；他の熱硬化性 / UV硬化型 / PU 系配合にも応用できる可能性あり"},
"visc_thinking":             {"zh_TW":"分析配方中", "zh_CN":"分析配方中", "en":"Analyzing", "ja":"分析中"},
"visc_temp":                 {"zh_TW":"預測溫度 °C:", "zh_CN":"预测温度 °C:", "en":"Temperature °C:", "ja":"予測温度 °C:"},
"visc_ml_status":            {"zh_TW":"ML 模型:", "zh_CN":"ML 模型:", "en":"ML Model:", "ja":"MLモデル:"},
"visc_ml_active":            {"zh_TW":"✓ 集成ML已啟用 ({n} 筆訓練資料)", "zh_CN":"✓ 集成ML已启用 ({n} 条训练数据)", "en":"✓ Ensemble ML Active ({n} training samples)", "ja":"✓ アンサンブルML有効 ({n}件の学習データ)"},
"visc_ml_inactive":          {"zh_TW":"○ ML待機 (需≥2筆帶黏度的配方)", "zh_CN":"○ ML待机 (需≥2条带粘度的配方)", "en":"○ ML standby (need ≥2 recipes with viscosity)", "ja":"○ ML待機中 (粘度データ付き配合≥2件必要)"},
"col_mgr_add":               {"zh_TW":"+ 新增自訂欄位", "zh_CN":"+ 新增自定义栏位", "en":"+ Add Custom Column", "ja":"+ カスタム列を追加"},
"col_mgr_name":              {"zh_TW":"欄位名稱:", "zh_CN":"栏位名称:", "en":"Column Name:", "ja":"列名:"},
"col_mgr_key":               {"zh_TW":"資料鍵值:", "zh_CN":"数据键值:", "en":"Data Key:", "ja":"データキー:"},
"prop_mgr_add":              {"zh_TW":"+ 新增自訂物性", "zh_CN":"+ 新增自定义物性", "en":"+ Add Custom Property", "ja":"+ カスタム物性を追加"},
"prop_mgr_name":             {"zh_TW":"物性名稱:", "zh_CN":"物性名称:", "en":"Property Name:", "ja":"物性名:"},
"prop_mgr_unit":             {"zh_TW":"單位:", "zh_CN":"单位:", "en":"Unit:", "ja":"単位:"},
"prop_mgr_method":           {"zh_TW":"測試方法:", "zh_CN":"测试方法:", "en":"Test Method:", "ja":"試験方法:"},
"prop_mgr_category":         {"zh_TW":"所屬類別:", "zh_CN":"所属类别:", "en":"Category:", "ja":"カテゴリ:"},
"home_new_db":               {"zh_TW":"📄 新增", "zh_CN":"📄 新建", "en":"📄 New", "ja":"📄 新規"},
"home_rename_db":            {"zh_TW":"✏️ 重命名", "zh_CN":"✏️ 重命名", "en":"✏️ Rename", "ja":"✏️ 名前変更"},
"builtin_col_name":          {"zh_TW":"名稱", "zh_CN":"名称", "en":"Name", "ja":"名称"},
"builtin_col_type":          {"zh_TW":"類型", "zh_CN":"类型", "en":"Type", "ja":"タイプ"},
"builtin_col_eq":            {"zh_TW":"EEW/當量", "zh_CN":"EEW/当量", "en":"EEW/Eq.", "ja":"EEW/当量"},
"builtin_col_cl":            {"zh_TW":"氯", "zh_CN":"氯", "en":"Cl", "ja":"塩素"},
"batch_label":                {"zh_TW":"批次號", "zh_CN":"批次号", "en":"Batch No.", "ja":"ロット番号"},
"date_label":                 {"zh_TW":"建立日期", "zh_CN":"创建日期", "en":"Date Created", "ja":"作成日"},
"mode_label":                 {"zh_TW":"模式", "zh_CN":"模式", "en":"Mode", "ja":"モード"},
"total_mass_label":           {"zh_TW":"總質量", "zh_CN":"总质量", "en":"Total Mass", "ja":"総質量"},
"total_cl_label":             {"zh_TW":"總氯含量", "zh_CN":"总氯含量", "en":"Total Cl", "ja":"総塩素含有量"},
"propcat_1":                  {"zh_TW":"1.未固化屬性", "zh_CN":"1.未固化属性", "en":"1. Uncured Properties", "ja":"1. 未硬化特性"},
"propcat_2":                  {"zh_TW":"2.固化過程", "zh_CN":"2.固化过程", "en":"2. Curing Process", "ja":"2. 硬化プロセス"},
"propcat_3":                  {"zh_TW":"3.機械屬性", "zh_CN":"3.机械属性", "en":"3. Mechanical Properties", "ja":"3. 機械特性"},
"propcat_4":                  {"zh_TW":"4.熱屬性", "zh_CN":"4.热属性", "en":"4. Thermal Properties", "ja":"4. 熱特性"},
"propcat_5":                  {"zh_TW":"5.耐化學性", "zh_CN":"5.耐化学性", "en":"5. Chemical Resistance", "ja":"5. 耐薬品性"},
"propcat_6":                  {"zh_TW":"6.電屬性", "zh_CN":"6.电属性", "en":"6. Electrical Properties", "ja":"6. 電気特性"},
"propcat_7":                  {"zh_TW":"7.可靠性", "zh_CN":"7.可靠性", "en":"7. Reliability", "ja":"7. 信頼性"},
# ========== V6.4.12 cat 4-7 物性/方法翻譯補齊 ==========
"DSC 二次升溫": {"zh_TW":"DSC 二次升溫", "zh_CN":"DSC 二次升温", "en":"DSC 2nd heat scan", "ja":"DSC 2回目昇温"},
"DMA 拉伸/三點彎曲": {"zh_TW":"DMA 拉伸/三點彎曲", "zh_CN":"DMA 拉伸/三点弯曲", "en":"DMA tensile / 3-point bending", "ja":"DMA 引張 / 3点曲げ"},
"DMA 儲存模量轉折": {"zh_TW":"DMA 儲存模量轉折", "zh_CN":"DMA 储存模量转折", "en":"DMA storage-modulus onset", "ja":"DMA 貯蔵弾性率転換点"},
"Tg-TMA (膨脹轉折)": {"zh_TW":"Tg-TMA (膨脹轉折)", "zh_CN":"Tg-TMA (膨胀转折)", "en":"Tg-TMA (expansion onset)", "ja":"Tg-TMA (膨張転換点)"},
"DMA 升溫速率/頻率": {"zh_TW":"DMA 升溫速率/頻率", "zh_CN":"DMA 升温速率/频率", "en":"DMA heating rate / frequency", "ja":"DMA 昇温速度 / 周波数"},
"熱分解溫度 Td5%": {"zh_TW":"熱分解溫度 Td5%", "zh_CN":"热分解温度 Td5%", "en":"Decomposition Temp. Td5%", "ja":"熱分解温度 Td5%"},
"熱分解溫度 Td5% (Air)": {"zh_TW":"熱分解溫度 Td5% (Air)", "zh_CN":"热分解温度 Td5% (Air)", "en":"Decomposition Temp. Td5% (Air)", "ja":"熱分解温度 Td5% (空気中)"},
"殘碳率 @800°C": {"zh_TW":"殘碳率 @800°C", "zh_CN":"残碳率 @800°C", "en":"Char residue @800°C", "ja":"残炭率 @800°C"},
"導熱率": {"zh_TW":"導熱率", "zh_CN":"导热率", "en":"Thermal conductivity", "ja":"熱伝導率"},
"HDT 熱變形溫度": {"zh_TW":"HDT 熱變形溫度", "zh_CN":"HDT 热变形温度", "en":"HDT (Heat Deflection Temp.)", "ja":"HDT 熱変形温度"},
"UL94 阻燃等級": {"zh_TW":"UL94 阻燃等級", "zh_CN":"UL94 阻燃等级", "en":"UL94 flammability rating", "ja":"UL94 難燃性ランク"},
"LOI 極限氧指數": {"zh_TW":"LOI 極限氧指數", "zh_CN":"LOI 极限氧指数", "en":"LOI (Limiting Oxygen Index)", "ja":"LOI 限界酸素指数"},
"回焊耐性 (260°C)": {"zh_TW":"回焊耐性 (260°C)", "zh_CN":"回流焊耐性 (260°C)", "en":"Reflow resistance (260°C)", "ja":"リフロー耐性 (260°C)"},
"回焊耐性 (288°C)": {"zh_TW":"回焊耐性 (288°C)", "zh_CN":"回流焊耐性 (288°C)", "en":"Reflow resistance (288°C)", "ja":"リフロー耐性 (288°C)"},
"回焊裂紋/脫層": {"zh_TW":"回焊裂紋/脫層", "zh_CN":"回流焊裂纹/脱层", "en":"Reflow cracking / delamination", "ja":"リフロークラック / 剥離"},
"Pass/Fail, 次數": {"zh_TW":"Pass/Fail, 次數", "zh_CN":"Pass/Fail, 次数", "en":"Pass/Fail, cycles", "ja":"Pass/Fail, 回数"},
"SAT/X-ray 檢查": {"zh_TW":"SAT/X-ray 檢查", "zh_CN":"SAT/X-ray 检查", "en":"SAT / X-ray inspection", "ja":"SAT / X線検査"},
"氣密性 — 回焊前": {"zh_TW":"氣密性 — 回焊前", "zh_CN":"气密性 — 回流焊前", "en":"Hermeticity — before reflow", "ja":"気密性 — リフロー前"},
"氣密性 — 回焊 1次後": {"zh_TW":"氣密性 — 回焊 1次後", "zh_CN":"气密性 — 回流焊 1次后", "en":"Hermeticity — after 1 reflow", "ja":"気密性 — リフロー 1回後"},
"氣密性 — 回焊 2次後": {"zh_TW":"氣密性 — 回焊 2次後", "zh_CN":"气密性 — 回流焊 2次后", "en":"Hermeticity — after 2 reflows", "ja":"気密性 — リフロー 2回後"},
"氣密性 — 回焊 3次後": {"zh_TW":"氣密性 — 回焊 3次後", "zh_CN":"气密性 — 回流焊 3次后", "en":"Hermeticity — after 3 reflows", "ja":"気密性 — リフロー 3回後"},
"氣密性判定標準": {"zh_TW":"氣密性判定標準", "zh_CN":"气密性判定标准", "en":"Hermeticity acceptance criterion", "ja":"気密性判定基準"},
"氣密性結論": {"zh_TW":"氣密性結論", "zh_CN":"气密性结论", "en":"Hermeticity result", "ja":"気密性判定結果"},
"He 洩漏檢測 (初始值)": {"zh_TW":"He 洩漏檢測 (初始值)", "zh_CN":"He 泄漏检测 (初始值)", "en":"He leak test (initial)", "ja":"Heリークテスト (初期値)"},
"He 洩漏檢測": {"zh_TW":"He 洩漏檢測", "zh_CN":"He 泄漏检测", "en":"He leak test", "ja":"Heリークテスト"},
"吸水率 (24h/25°C)": {"zh_TW":"吸水率 (24h/25°C)", "zh_CN":"吸水率 (24h/25°C)", "en":"Water absorption (24h/25°C)", "ja":"吸水率 (24h/25°C)"},
"吸水率 (煮沸2h)": {"zh_TW":"吸水率 (煮沸2h)", "zh_CN":"吸水率 (煮沸2h)", "en":"Water absorption (2h boil)", "ja":"吸水率 (煮沸2h)"},
"吸濕率 (85°C/85%RH)": {"zh_TW":"吸濕率 (85°C/85%RH)", "zh_CN":"吸湿率 (85°C/85%RH)", "en":"Moisture absorption (85°C/85%RH)", "ja":"吸湿率 (85°C/85%RH)"},
"吸濕飽和時間": {"zh_TW":"吸濕飽和時間", "zh_CN":"吸湿饱和时间", "en":"Moisture saturation time", "ja":"吸湿飽和時間"},
"恆溫恆濕箱": {"zh_TW":"恆溫恆濕箱", "zh_CN":"恒温恒湿箱", "en":"Constant temperature & humidity chamber", "ja":"恒温恒湿槽"},
"耐溶劑性 (IPA)": {"zh_TW":"耐溶劑性 (IPA)", "zh_CN":"耐溶剂性 (IPA)", "en":"Solvent resistance (IPA)", "ja":"耐溶剤性 (IPA)"},
"耐溶劑性 (Acetone)": {"zh_TW":"耐溶劑性 (Acetone)", "zh_CN":"耐溶剂性 (Acetone)", "en":"Solvent resistance (Acetone)", "ja":"耐溶剤性 (アセトン)"},
"耐溶劑性 (NMP)": {"zh_TW":"耐溶劑性 (NMP)", "zh_CN":"耐溶剂性 (NMP)", "en":"Solvent resistance (NMP)", "ja":"耐溶剤性 (NMP)"},
"耐酸性 (5% HCl)": {"zh_TW":"耐酸性 (5% HCl)", "zh_CN":"耐酸性 (5% HCl)", "en":"Acid resistance (5% HCl)", "ja":"耐酸性 (5% HCl)"},
"耐鹼性 (5% NaOH)": {"zh_TW":"耐鹼性 (5% NaOH)", "zh_CN":"耐碱性 (5% NaOH)", "en":"Alkali resistance (5% NaOH)", "ja":"耐アルカリ性 (5% NaOH)"},
"耐助焊劑性": {"zh_TW":"耐助焊劑性", "zh_CN":"耐助焊剂性", "en":"Flux resistance", "ja":"耐フラックス性"},
"浸泡測試 @25°C": {"zh_TW":"浸泡測試 @25°C", "zh_CN":"浸泡测试 @25°C", "en":"Immersion test @25°C", "ja":"浸漬試験 @25°C"},
"浸泡測試": {"zh_TW":"浸泡測試", "zh_CN":"浸泡测试", "en":"Immersion test", "ja":"浸漬試験"},
"浸泡測試 @指定助焊劑": {"zh_TW":"浸泡測試 @指定助焊劑", "zh_CN":"浸泡测试 @指定助焊剂", "en":"Immersion test @specified flux", "ja":"浸漬試験 @指定フラックス"},
"離子純度 Na⁺": {"zh_TW":"離子純度 Na⁺", "zh_CN":"离子纯度 Na⁺", "en":"Ionic purity Na⁺", "ja":"イオン純度 Na⁺"},
"離子純度 Cl⁻": {"zh_TW":"離子純度 Cl⁻", "zh_CN":"离子纯度 Cl⁻", "en":"Ionic purity Cl⁻", "ja":"イオン純度 Cl⁻"},
"離子純度 總萃取離子": {"zh_TW":"離子純度 總萃取離子", "zh_CN":"离子纯度 总萃取离子", "en":"Ionic purity — total extractable", "ja":"イオン純度 — 全抽出イオン"},
"銅鏡腐蝕": {"zh_TW":"銅鏡腐蝕", "zh_CN":"铜镜腐蚀", "en":"Copper mirror corrosion", "ja":"銅鏡腐食"},
"鹽霧試驗": {"zh_TW":"鹽霧試驗", "zh_CN":"盐雾试验", "en":"Salt spray test", "ja":"塩水噴霧試験"},
"離子色譜 IC / IPC-TM-650": {"zh_TW":"離子色譜 IC / IPC-TM-650", "zh_CN":"离子色谱 IC / IPC-TM-650", "en":"Ion chromatography / IPC-TM-650", "ja":"イオンクロマトグラフィー / IPC-TM-650"},
"TML 總質量損失": {"zh_TW":"TML 總質量損失", "zh_CN":"TML 总质量损失", "en":"TML (Total Mass Loss)", "ja":"TML 全質量損失"},
"CVCM 可凝揮發物": {"zh_TW":"CVCM 可凝揮發物", "zh_CN":"CVCM 可凝挥发物", "en":"CVCM (Collected Volatile Condensable Material)", "ja":"CVCM 凝縮性揮発物"},
"揮發分 (TGA)": {"zh_TW":"揮發分 (TGA)", "zh_CN":"挥发分 (TGA)", "en":"Volatiles (TGA)", "ja":"揮発分 (TGA)"},
"ASTM E595 (125°C/24h/真空)": {"zh_TW":"ASTM E595 (125°C/24h/真空)", "zh_CN":"ASTM E595 (125°C/24h/真空)", "en":"ASTM E595 (125°C/24h/vacuum)", "ja":"ASTM E595 (125°C/24h/真空)"},
"TGA @指定溫度": {"zh_TW":"TGA @指定溫度", "zh_CN":"TGA @指定温度", "en":"TGA @specified temperature", "ja":"TGA @指定温度"},
"介電常數 Dk @1MHz": {"zh_TW":"介電常數 Dk @1MHz", "zh_CN":"介电常数 Dk @1MHz", "en":"Dielectric constant Dk @1MHz", "ja":"誘電率 Dk @1MHz"},
"介電常數 Dk @1GHz": {"zh_TW":"介電常數 Dk @1GHz", "zh_CN":"介电常数 Dk @1GHz", "en":"Dielectric constant Dk @1GHz", "ja":"誘電率 Dk @1GHz"},
"介電常數 Dk @10GHz": {"zh_TW":"介電常數 Dk @10GHz", "zh_CN":"介电常数 Dk @10GHz", "en":"Dielectric constant Dk @10GHz", "ja":"誘電率 Dk @10GHz"},
"介電損耗 Df @1MHz": {"zh_TW":"介電損耗 Df @1MHz", "zh_CN":"介电损耗 Df @1MHz", "en":"Dielectric loss Df @1MHz", "ja":"誘電正接 Df @1MHz"},
"介電損耗 Df @1GHz": {"zh_TW":"介電損耗 Df @1GHz", "zh_CN":"介电损耗 Df @1GHz", "en":"Dielectric loss Df @1GHz", "ja":"誘電正接 Df @1GHz"},
"介電損耗 Df @10GHz": {"zh_TW":"介電損耗 Df @10GHz", "zh_CN":"介电损耗 Df @10GHz", "en":"Dielectric loss Df @10GHz", "ja":"誘電正接 Df @10GHz"},
"體積電阻率": {"zh_TW":"體積電阻率", "zh_CN":"体积电阻率", "en":"Volume resistivity", "ja":"体積抵抗率"},
"表面電阻率": {"zh_TW":"表面電阻率", "zh_CN":"表面电阻率", "en":"Surface resistivity", "ja":"表面抵抗率"},
"介電強度": {"zh_TW":"介電強度", "zh_CN":"介电强度", "en":"Dielectric strength", "ja":"絶縁破壊強さ"},
"絕緣電阻 (常態)": {"zh_TW":"絕緣電阻 (常態)", "zh_CN":"绝缘电阻 (常态)", "en":"Insulation resistance (as-is)", "ja":"絶縁抵抗 (常態)"},
"絕緣電阻 (吸濕後)": {"zh_TW":"絕緣電阻 (吸濕後)", "zh_CN":"绝缘电阻 (吸湿后)", "en":"Insulation resistance (after moisture)", "ja":"絶縁抵抗 (吸湿後)"},
"IPC-TM-650 (85/85後)": {"zh_TW":"IPC-TM-650 (85/85後)", "zh_CN":"IPC-TM-650 (85/85后)", "en":"IPC-TM-650 (after 85/85)", "ja":"IPC-TM-650 (85/85後)"},
"CTI 漏電起痕指數": {"zh_TW":"CTI 漏電起痕指數", "zh_CN":"CTI 漏电起痕指数", "en":"CTI (Comparative Tracking Index)", "ja":"CTI 比較トラッキング指数"},
"體積電阻率 (導電)": {"zh_TW":"體積電阻率 (導電)", "zh_CN":"体积电阻率 (导电)", "en":"Volume resistivity (conductive)", "ja":"体積抵抗率 (導電性)"},
"接觸電阻": {"zh_TW":"接觸電阻", "zh_CN":"接触电阻", "en":"Contact resistance", "ja":"接触抵抗"},
"四探針法": {"zh_TW":"四探針法", "zh_CN":"四探针法", "en":"4-probe method", "ja":"四探針法"},
"四線法": {"zh_TW":"四線法", "zh_CN":"四线法", "en":"4-wire method", "ja":"四端子法"},
"PCT 壓力鍋測試": {"zh_TW":"PCT 壓力鍋測試", "zh_CN":"PCT 压力锅测试", "en":"PCT (Pressure Cooker Test)", "ja":"PCT プレッシャークッカー試験"},
"HAST 高加速壽命": {"zh_TW":"HAST 高加速壽命", "zh_CN":"HAST 高加速寿命", "en":"HAST (Highly Accelerated Stress Test)", "ja":"HAST 高加速寿命試験"},
"85/85 恆溫恆濕": {"zh_TW":"85/85 恆溫恆濕", "zh_CN":"85/85 恒温恒湿", "en":"85/85 T&H test", "ja":"85/85 恒温恒湿試験"},
"PCT/HAST 後接著強度": {"zh_TW":"PCT/HAST 後接著強度", "zh_CN":"PCT/HAST 后粘接强度", "en":"Adhesion strength after PCT/HAST", "ja":"PCT/HAST 後の接着強さ"},
"PCT/HAST 後絕緣電阻": {"zh_TW":"PCT/HAST 後絕緣電阻", "zh_CN":"PCT/HAST 后绝缘电阻", "en":"Insulation resistance after PCT/HAST", "ja":"PCT/HAST 後の絶縁抵抗"},
"121°C/2atm/100%RH, 記錄時間": {"zh_TW":"121°C/2atm/100%RH, 記錄時間", "zh_CN":"121°C/2atm/100%RH, 记录时间", "en":"121°C/2atm/100%RH, time-to-fail", "ja":"121°C/2atm/100%RH, 時間記録"},
"130°C/85%RH, 記錄時間": {"zh_TW":"130°C/85%RH, 記錄時間", "zh_CN":"130°C/85%RH, 记录时间", "en":"130°C/85%RH, time-to-fail", "ja":"130°C/85%RH, 時間記録"},
"85°C/85%RH, 記錄通過時間": {"zh_TW":"85°C/85%RH, 記錄通過時間", "zh_CN":"85°C/85%RH, 记录通过时间", "en":"85°C/85%RH, time-to-pass", "ja":"85°C/85%RH, 合格時間記録"},
"可靠性後剪切測試": {"zh_TW":"可靠性後剪切測試", "zh_CN":"可靠性后剪切测试", "en":"Post-reliability shear test", "ja":"信頼性試験後のせん断試験"},
"可靠性後電阻測試": {"zh_TW":"可靠性後電阻測試", "zh_CN":"可靠性后电阻测试", "en":"Post-reliability resistance test", "ja":"信頼性試験後の抵抗測定"},
"TCT 溫度循環": {"zh_TW":"TCT 溫度循環", "zh_CN":"TCT 温度循环", "en":"TCT (Thermal Cycle Test)", "ja":"TCT 温度サイクル試験"},
"TST 冷熱衝擊": {"zh_TW":"TST 冷熱衝擊", "zh_CN":"TST 冷热冲击", "en":"TST (Thermal Shock Test)", "ja":"TST 冷熱衝撃試験"},
"TCT/TST 後外觀": {"zh_TW":"TCT/TST 後外觀", "zh_CN":"TCT/TST 后外观", "en":"Appearance after TCT/TST", "ja":"TCT/TST 後の外観"},
"TCT/TST 後接著強度": {"zh_TW":"TCT/TST 後接著強度", "zh_CN":"TCT/TST 后粘接强度", "en":"Adhesion strength after TCT/TST", "ja":"TCT/TST 後の接着強さ"},
"-40~125°C 或 -55~125°C": {"zh_TW":"-40~125°C 或 -55~125°C", "zh_CN":"-40~125°C 或 -55~125°C", "en":"-40~125°C or -55~125°C", "ja":"-40~125°C または -55~125°C"},
"-40~125°C (液槽/氣槽)": {"zh_TW":"-40~125°C (液槽/氣槽)", "zh_CN":"-40~125°C (液槽/气槽)", "en":"-40~125°C (liquid/gas chamber)", "ja":"-40~125°C (液槽/気槽)"},
"SAT/X-ray/顯微鏡": {"zh_TW":"SAT/X-ray/顯微鏡", "zh_CN":"SAT/X-ray/显微镜", "en":"SAT / X-ray / microscopy", "ja":"SAT / X線 / 顕微鏡"},
"高溫儲存 HTSL": {"zh_TW":"高溫儲存 HTSL", "zh_CN":"高温储存 HTSL", "en":"HTSL (High Temp. Storage Life)", "ja":"HTSL 高温保管試験"},
"低溫儲存 LTSL": {"zh_TW":"低溫儲存 LTSL", "zh_CN":"低温储存 LTSL", "en":"LTSL (Low Temp. Storage Life)", "ja":"LTSL 低温保管試験"},
"UV 耐候性": {"zh_TW":"UV 耐候性", "zh_CN":"UV 耐候性", "en":"UV weathering resistance", "ja":"UV 耐候性"},
"耐黃變 ΔYI": {"zh_TW":"耐黃變 ΔYI", "zh_CN":"耐黄变 ΔYI", "en":"Yellowing resistance ΔYI", "ja":"黄変耐性 ΔYI"},
"MSL 吸濕敏感度等級": {"zh_TW":"MSL 吸濕敏感度等級", "zh_CN":"MSL 吸湿敏感度等级", "en":"MSL (Moisture Sensitivity Level)", "ja":"MSL 吸湿感度レベル"},
"150°C 或 175°C": {"zh_TW":"150°C 或 175°C", "zh_CN":"150°C 或 175°C", "en":"150°C or 175°C", "ja":"150°C または 175°C"},
"ASTM D1925 (UV後)": {"zh_TW":"ASTM D1925 (UV後)", "zh_CN":"ASTM D1925 (UV后)", "en":"ASTM D1925 (after UV)", "ja":"ASTM D1925 (UV後)"},
"打線接合性 Wire Bond": {"zh_TW":"打線接合性 Wire Bond", "zh_CN":"打线接合性 Wire Bond", "en":"Wire bondability", "ja":"ワイヤーボンド性"},
"打線拉力 Wire Pull": {"zh_TW":"打線拉力 Wire Pull", "zh_CN":"打线拉力 Wire Pull", "en":"Wire pull strength", "ja":"ワイヤープル強さ"},
"打線球剪切 Ball Shear": {"zh_TW":"打線球剪切 Ball Shear", "zh_CN":"打线球剪切 Ball Shear", "en":"Ball shear strength", "ja":"ボールシェア強さ"},
"propcat_custom":             {"zh_TW":"8.自訂", "zh_CN":"8.自定义", "en":"8. Custom", "ja":"8. カスタム"},
# ========== V6.4.4 DSC 工具：固化劑類型下拉翻譯 ==========
"htype_DICY": {"zh_TW":"雙氰胺 (DICY)", "zh_CN":"双氰胺 (DICY)", "en":"Dicyandiamide (DICY)", "ja":"ジシアンジアミド (DICY)"},
"htype_amine": {"zh_TW":"胺類", "zh_CN":"胺类", "en":"Amine", "ja":"アミン系"},
"htype_anhydride": {"zh_TW":"酸酐", "zh_CN":"酸酐", "en":"Anhydride", "ja":"酸無水物"},
"htype_imidazole": {"zh_TW":"咪唑", "zh_CN":"咪唑", "en":"Imidazole", "ja":"イミダゾール"},
"htype_mercaptan": {"zh_TW":"巰基 / 硫醇", "zh_CN":"巯基 / 硫醇", "en":"Mercaptan / Thiol", "ja":"メルカプタン / チオール"},
"htype_latent": {"zh_TW":"潛伏型催化", "zh_CN":"潜伏型催化", "en":"Latent Catalyst", "ja":"潜在性触媒"},
"htype_phenolic": {"zh_TW":"酚醛", "zh_CN":"酚醛", "en":"Phenolic", "ja":"フェノール系"},

# ========== V6.4.3 物性/群組/方法多語言翻譯 ==========
# 鍵即為 zh_TW 原字串（與 PREDEFINED_PROPS 對齊）；T_prop/T_group/T_method
# 會查找這裡；未翻譯者自動回退到鍵本身 (即 zh_TW 中文原值)
# 涵蓋範圍：所有 29 groups + 分類 1~7 全部物性/方法翻譯

"外觀與流變": {"zh_TW":"外觀與流變", "zh_CN":"外观与流变", "en":"Appearance & Rheology", "ja":"外観とレオロジー"},
"物理常數": {"zh_TW":"物理常數", "zh_CN":"物理常数", "en":"Physical Constants", "ja":"物理定数"},
"操作性": {"zh_TW":"操作性", "zh_CN":"操作性", "en":"Workability", "ja":"作業性"},
"凝膠測試": {"zh_TW":"凝膠測試", "zh_CN":"凝胶测试", "en":"Gel Test", "ja":"ゲル化試験"},
"DSC 分析": {"zh_TW":"DSC 分析", "zh_CN":"DSC 分析", "en":"DSC Analysis", "ja":"DSC 解析"},
"固化條件": {"zh_TW":"固化條件", "zh_CN":"固化条件", "en":"Cure Conditions", "ja":"硬化条件"},
"硬度": {"zh_TW":"硬度", "zh_CN":"硬度", "en":"Hardness", "ja":"硬度"},
"拉伸性能": {"zh_TW":"拉伸性能", "zh_CN":"拉伸性能", "en":"Tensile Properties", "ja":"引張特性"},
"彎曲性能": {"zh_TW":"彎曲性能", "zh_CN":"弯曲性能", "en":"Flexural Properties", "ja":"曲げ特性"},
"壓縮與衝擊": {"zh_TW":"壓縮與衝擊", "zh_CN":"压缩与冲击", "en":"Compression & Impact", "ja":"圧縮と衝撃"},
"彈性模量": {"zh_TW":"彈性模量", "zh_CN":"弹性模量", "en":"Elastic Modulus", "ja":"弾性率"},
"接著/剪切強度": {"zh_TW":"接著/剪切強度", "zh_CN":"粘接/剪切强度", "en":"Adhesion/Shear Strength", "ja":"接着/せん断強度"},
"剝離與接著": {"zh_TW":"剝離與接著", "zh_CN":"剥离与粘接", "en":"Peel & Adhesion", "ja":"剥離と接着"},
"玻璃轉化溫度 Tg": {"zh_TW":"玻璃轉化溫度 Tg", "zh_CN":"玻璃化转变温度 Tg", "en":"Glass Transition Tg", "ja":"ガラス転移温度 Tg"},
"熱膨脹": {"zh_TW":"熱膨脹", "zh_CN":"热膨胀", "en":"Thermal Expansion", "ja":"熱膨張"},
"耐熱性": {"zh_TW":"耐熱性", "zh_CN":"耐热性", "en":"Heat Resistance", "ja":"耐熱性"},
"回焊耐性": {"zh_TW":"回焊耐性", "zh_CN":"回流焊耐性", "en":"Reflow Resistance", "ja":"リフロー耐性"},
"回焊氣密性": {"zh_TW":"回焊氣密性", "zh_CN":"回流焊气密性", "en":"Reflow Hermeticity", "ja":"リフロー気密性"},
"吸濕性": {"zh_TW":"吸濕性", "zh_CN":"吸湿性", "en":"Moisture Absorption", "ja":"吸湿特性"},
"耐化學品": {"zh_TW":"耐化學品", "zh_CN":"耐化学品", "en":"Chemical Resistance", "ja":"耐薬品性"},
"腐蝕與離子": {"zh_TW":"腐蝕與離子", "zh_CN":"腐蚀与离子", "en":"Corrosion & Ions", "ja":"腐食とイオン"},
"出氣量": {"zh_TW":"出氣量", "zh_CN":"出气量", "en":"Outgassing", "ja":"アウトガス"},
"介電性能": {"zh_TW":"介電性能", "zh_CN":"介电性能", "en":"Dielectric Properties", "ja":"誘電特性"},
"絕緣性能": {"zh_TW":"絕緣性能", "zh_CN":"绝缘性能", "en":"Insulation Properties", "ja":"絶縁特性"},
"導電性 (導電膠適用)": {"zh_TW":"導電性 (導電膠適用)", "zh_CN":"导电性 (导电胶适用)", "en":"Conductivity (Conductive Adhesives)", "ja":"導電性 (導電性接着剤用)"},
"溫濕度可靠性": {"zh_TW":"溫濕度可靠性", "zh_CN":"温湿度可靠性", "en":"Temp/Humidity Reliability", "ja":"温湿度信頼性"},
"溫度循環": {"zh_TW":"溫度循環", "zh_CN":"温度循环", "en":"Temperature Cycling", "ja":"温度サイクル"},
"其他可靠性": {"zh_TW":"其他可靠性", "zh_CN":"其他可靠性", "en":"Other Reliability", "ja":"その他信頼性"},
"打線與焊接": {"zh_TW":"打線與焊接", "zh_CN":"打线与焊接", "en":"Wire Bond & Soldering", "ja":"ワイヤーボンドとはんだ付け"},
"常溫狀態 (25°C)": {"zh_TW":"常溫狀態 (25°C)", "zh_CN":"常温状态 (25°C)", "en":"RT State (25°C)", "ja":"常温状態 (25°C)"},
"顏色": {"zh_TW":"顏色", "zh_CN":"颜色", "en":"Color", "ja":"色"},
"黏度 (cP, 25°C)": {"zh_TW":"黏度 (cP, 25°C)", "zh_CN":"粘度 (cP, 25°C)", "en":"Viscosity (cP, 25°C)", "ja":"粘度 (cP, 25°C)"},
"黏度 (Pa·s, 25°C)": {"zh_TW":"黏度 (Pa·s, 25°C)", "zh_CN":"粘度 (Pa·s, 25°C)", "en":"Viscosity (Pa·s, 25°C)", "ja":"粘度 (Pa·s, 25°C)"},
"觸變指數 TI (η1/η10)": {"zh_TW":"觸變指數 TI (η1/η10)", "zh_CN":"触变指数 TI (η1/η10)", "en":"Thixotropic Index TI (η1/η10)", "ja":"チクソトロピー指数 TI (η1/η10)"},
"流淌性 Slump": {"zh_TW":"流淌性 Slump", "zh_CN":"流淌性 Slump", "en":"Slump", "ja":"スランプ"},
"比重 SG (25°C)": {"zh_TW":"比重 SG (25°C)", "zh_CN":"比重 SG (25°C)", "en":"Specific Gravity (25°C)", "ja":"比重 SG (25°C)"},
"比重 SG (固化後)": {"zh_TW":"比重 SG (固化後)", "zh_CN":"比重 SG (固化后)", "en":"Specific Gravity (cured)", "ja":"比重 SG (硬化後)"},
"折射率 nD (25°C)": {"zh_TW":"折射率 nD (25°C)", "zh_CN":"折射率 nD (25°C)", "en":"Refractive Index nD (25°C)", "ja":"屈折率 nD (25°C)"},
"體積收縮率": {"zh_TW":"體積收縮率", "zh_CN":"体积收缩率", "en":"Volume Shrinkage", "ja":"体積収縮率"},
"適用期 Pot Life (25°C)": {"zh_TW":"適用期 Pot Life (25°C)", "zh_CN":"适用期 Pot Life (25°C)", "en":"Pot Life (25°C)", "ja":"可使用時間 (25°C)"},
"適用期 Pot Life (指定溫度)": {"zh_TW":"適用期 Pot Life (指定溫度)", "zh_CN":"适用期 Pot Life (指定温度)", "en":"Pot Life (specified temp)", "ja":"可使用時間 (指定温度)"},
"保質期 Shelf Life": {"zh_TW":"保存期限 Shelf Life", "zh_CN":"保质期 Shelf Life", "en":"Shelf Life", "ja":"有効期限"},
"擠出性 (卡式管)": {"zh_TW":"擠出性 (卡式管)", "zh_CN":"挤出性 (卡式管)", "en":"Extrudability (cartridge)", "ja":"押出性 (カートリッジ)"},
"目視觀察": {"zh_TW":"目視觀察", "zh_CN":"目视观察", "en":"Visual observation", "ja":"目視観察"},
"目視/Gardner色標": {"zh_TW":"目視/Gardner色標", "zh_CN":"目视/Gardner色标", "en":"Visual / Gardner scale", "ja":"目視 / ガードナー色標"},
"Brookfield旋轉黏度計": {"zh_TW":"Brookfield旋轉黏度計", "zh_CN":"Brookfield旋转粘度计", "en":"Brookfield rotational viscometer", "ja":"ブルックフィールド回転粘度計"},
"流變儀 (錐板/平板)": {"zh_TW":"流變儀 (錐板/平板)", "zh_CN":"流变仪 (锥板/平板)", "en":"Rheometer (cone-plate / parallel-plate)", "ja":"レオメータ (コーンプレート/パラレルプレート)"},
"Brookfield 1rpm/10rpm": {"zh_TW":"Brookfield 1rpm/10rpm", "zh_CN":"Brookfield 1rpm/10rpm", "en":"Brookfield 1rpm/10rpm", "ja":"ブルックフィールド 1rpm/10rpm"},
"垂直掛片法": {"zh_TW":"垂直掛片法", "zh_CN":"垂直挂片法", "en":"Vertical slump method", "ja":"垂直試験片法"},
"比重瓶法/密度計": {"zh_TW":"比重瓶法/密度計", "zh_CN":"比重瓶法/密度计", "en":"Pycnometer / densitometer", "ja":"比重瓶法 / 密度計"},
"阿基米德法": {"zh_TW":"阿基米德法", "zh_CN":"阿基米德法", "en":"Archimedes method", "ja":"アルキメデス法"},
"阿貝折射儀": {"zh_TW":"阿貝折射儀", "zh_CN":"阿贝折射仪", "en":"Abbe refractometer", "ja":"アッベ屈折計"},
"比重法 (固化前後)": {"zh_TW":"比重法 (固化前後)", "zh_CN":"比重法 (固化前后)", "en":"SG method (before/after cure)", "ja":"比重法 (硬化前後)"},
"黏度倍增法 @25°C": {"zh_TW":"黏度倍增法 @25°C", "zh_CN":"粘度倍增法 @25°C", "en":"Viscosity doubling method @25°C", "ja":"粘度倍化法 @25°C"},
"黏度倍增法": {"zh_TW":"黏度倍增法", "zh_CN":"粘度倍增法", "en":"Viscosity doubling method", "ja":"粘度倍化法"},
"≤X°C 儲存": {"zh_TW":"≤X°C 儲存", "zh_CN":"≤X°C 储存", "en":"Storage ≤X°C", "ja":"≤X°C 保管"},
"氣壓擠出 @指定壓力": {"zh_TW":"氣壓擠出 @指定壓力", "zh_CN":"气压挤出 @指定压力", "en":"Pneumatic extrusion @specified pressure", "ja":"空圧押出 @指定圧力"},
"凝膠時間 Gel Time": {"zh_TW":"凝膠時間 Gel Time", "zh_CN":"凝胶时间 Gel Time", "en":"Gel Time", "ja":"ゲル化時間"},
"凝膠測試溫度": {"zh_TW":"凝膠測試溫度", "zh_CN":"凝胶测试温度", "en":"Gel test temperature", "ja":"ゲル化試験温度"},
"凝膠時間 (恆溫 DSC)": {"zh_TW":"凝膠時間 (恆溫 DSC)", "zh_CN":"凝胶时间 (恒温 DSC)", "en":"Gel time (isothermal DSC)", "ja":"ゲル化時間 (等温 DSC)"},
"DSC 起始固化溫度 Ti": {"zh_TW":"DSC 起始固化溫度 Ti", "zh_CN":"DSC 起始固化温度 Ti", "en":"DSC onset cure temp Ti", "ja":"DSC 硬化開始温度 Ti"},
"DSC 放熱峰溫度 Tp": {"zh_TW":"DSC 放熱峰溫度 Tp", "zh_CN":"DSC 放热峰温度 Tp", "en":"DSC exothermic peak Tp", "ja":"DSC 発熱ピーク温度 Tp"},
"DSC 反應熱 ΔH": {"zh_TW":"DSC 反應熱 ΔH", "zh_CN":"DSC 反应热 ΔH", "en":"DSC reaction enthalpy ΔH", "ja":"DSC 反応熱 ΔH"},
"DSC 升溫速率": {"zh_TW":"DSC 升溫速率", "zh_CN":"DSC 升温速率", "en":"DSC heating rate", "ja":"DSC 昇温速度"},
"DSC 殘餘反應熱": {"zh_TW":"DSC 殘餘反應熱", "zh_CN":"DSC 残余反应热", "en":"DSC residual enthalpy", "ja":"DSC 残留反応熱"},
"固化度 α": {"zh_TW":"固化度 α", "zh_CN":"固化度 α", "en":"Degree of cure α", "ja":"硬化度 α"},
"推薦固化條件": {"zh_TW":"推薦固化條件", "zh_CN":"推荐固化条件", "en":"Recommended cure schedule", "ja":"推奨硬化条件"},
"後固化條件": {"zh_TW":"後固化條件", "zh_CN":"后固化条件", "en":"Post-cure schedule", "ja":"ポスト硬化条件"},
"最低固化溫度": {"zh_TW":"最低固化溫度", "zh_CN":"最低固化温度", "en":"Minimum cure temp", "ja":"最低硬化温度"},
"指觸乾燥時間": {"zh_TW":"指觸乾燥時間", "zh_CN":"指触干燥时间", "en":"Touch-dry time", "ja":"指触乾燥時間"},
"熱板法": {"zh_TW":"熱板法", "zh_CN":"热板法", "en":"Hot plate method", "ja":"ホットプレート法"},
"恆溫 DSC": {"zh_TW":"恆溫 DSC", "zh_CN":"恒温 DSC", "en":"Isothermal DSC", "ja":"等温 DSC"},
"DSC 動態掃描 (onset)": {"zh_TW":"DSC 動態掃描 (onset)", "zh_CN":"DSC 动态扫描 (onset)", "en":"DSC dynamic scan (onset)", "ja":"DSC 動的スキャン (onset)"},
"DSC 動態掃描 (peak)": {"zh_TW":"DSC 動態掃描 (peak)", "zh_CN":"DSC 动态扫描 (peak)", "en":"DSC dynamic scan (peak)", "ja":"DSC 動的スキャン (ピーク)"},
"DSC 動態掃描": {"zh_TW":"DSC 動態掃描", "zh_CN":"DSC 动态扫描", "en":"DSC dynamic scan", "ja":"DSC 動的スキャン"},
"DSC (固化後再掃描)": {"zh_TW":"DSC (固化後再掃描)", "zh_CN":"DSC (固化后再扫描)", "en":"DSC (re-scan after cure)", "ja":"DSC (硬化後再スキャン)"},
"1 - ΔH_residual/ΔH_total": {"zh_TW":"1 - ΔH_residual/ΔH_total", "zh_CN":"1 - ΔH_residual/ΔH_total", "en":"1 − ΔH_residual / ΔH_total", "ja":"1 − ΔH残留 / ΔH全"},
"溫度×時間": {"zh_TW":"溫度×時間", "zh_CN":"温度×时间", "en":"Temperature × time", "ja":"温度 × 時間"},
"指觸法 @指定溫度": {"zh_TW":"指觸法 @指定溫度", "zh_CN":"指触法 @指定温度", "en":"Touch method @specified temp", "ja":"指触法 @指定温度"},
"硬度 Shore A": {"zh_TW":"硬度 Shore A", "zh_CN":"硬度 Shore A", "en":"Hardness Shore A", "ja":"硬度 Shore A"},
"硬度 Shore D": {"zh_TW":"硬度 Shore D", "zh_CN":"硬度 Shore D", "en":"Hardness Shore D", "ja":"硬度 Shore D"},
"鉛筆硬度": {"zh_TW":"鉛筆硬度", "zh_CN":"铅笔硬度", "en":"Pencil hardness", "ja":"鉛筆硬度"},
"拉伸強度": {"zh_TW":"拉伸強度", "zh_CN":"拉伸强度", "en":"Tensile strength", "ja":"引張強さ"},
"拉伸模量": {"zh_TW":"拉伸模量", "zh_CN":"拉伸模量", "en":"Tensile modulus", "ja":"引張弾性率"},
"斷裂伸長率": {"zh_TW":"斷裂伸長率", "zh_CN":"断裂伸长率", "en":"Elongation at break", "ja":"破断伸び"},
"彎曲強度": {"zh_TW":"彎曲強度", "zh_CN":"弯曲强度", "en":"Flexural strength", "ja":"曲げ強さ"},
"彎曲模量": {"zh_TW":"彎曲模量", "zh_CN":"弯曲模量", "en":"Flexural modulus", "ja":"曲げ弾性率"},
"壓縮強度": {"zh_TW":"壓縮強度", "zh_CN":"压缩强度", "en":"Compressive strength", "ja":"圧縮強さ"},
"壓縮模量": {"zh_TW":"壓縮模量", "zh_CN":"压缩模量", "en":"Compressive modulus", "ja":"圧縮弾性率"},
"衝擊強度 Charpy": {"zh_TW":"衝擊強度 Charpy", "zh_CN":"冲击强度 Charpy", "en":"Charpy impact strength", "ja":"シャルピー衝撃強さ"},
"衝擊強度 Izod": {"zh_TW":"衝擊強度 Izod", "zh_CN":"冲击强度 Izod", "en":"Izod impact strength", "ja":"アイゾット衝撃強さ"},
"楊氏模量 (拉伸)": {"zh_TW":"楊氏模量 (拉伸)", "zh_CN":"杨氏模量 (拉伸)", "en":"Young's modulus (tensile)", "ja":"ヤング率 (引張)"},
"儲存模量 E' @25°C": {"zh_TW":"儲存模量 E' @25°C", "zh_CN":"储存模量 E' @25°C", "en":"Storage modulus E' @25°C", "ja":"貯蔵弾性率 E' @25°C"},
"儲存模量 E' @260°C": {"zh_TW":"儲存模量 E' @260°C", "zh_CN":"储存模量 E' @260°C", "en":"Storage modulus E' @260°C", "ja":"貯蔵弾性率 E' @260°C"},
"損耗因子 tan δ @25°C": {"zh_TW":"損耗因子 tan δ @25°C", "zh_CN":"损耗因子 tan δ @25°C", "en":"Loss factor tan δ @25°C", "ja":"損失正接 tan δ @25°C"},
"搭接剪切強度 Al-Al": {"zh_TW":"搭接剪切強度 Al-Al", "zh_CN":"搭接剪切强度 Al-Al", "en":"Lap shear strength Al-Al", "ja":"引張せん断強さ Al-Al"},
"搭接剪切強度 Cu-Cu": {"zh_TW":"搭接剪切強度 Cu-Cu", "zh_CN":"搭接剪切强度 Cu-Cu", "en":"Lap shear strength Cu-Cu", "ja":"引張せん断強さ Cu-Cu"},
"搭接剪切強度 SUS-SUS": {"zh_TW":"搭接剪切強度 SUS-SUS", "zh_CN":"搭接剪切强度 SUS-SUS", "en":"Lap shear strength SUS-SUS", "ja":"引張せん断強さ SUS-SUS"},
"搭接剪切強度 FR4-FR4": {"zh_TW":"搭接剪切強度 FR4-FR4", "zh_CN":"搭接剪切强度 FR4-FR4", "en":"Lap shear strength FR4-FR4", "ja":"引張せん断強さ FR4-FR4"},
"搭接剪切強度 Glass-Glass": {"zh_TW":"搭接剪切強度 Glass-Glass", "zh_CN":"搭接剪切强度 Glass-Glass", "en":"Lap shear strength Glass-Glass", "ja":"引張せん断強さ Glass-Glass"},
"搭接剪切溫度": {"zh_TW":"搭接剪切溫度", "zh_CN":"搭接剪切温度", "en":"Lap shear test temperature", "ja":"引張せん断試験温度"},
"Die Shear (晶片剪切) @25°C": {"zh_TW":"Die Shear (晶片剪切) @25°C", "zh_CN":"Die Shear (芯片剪切) @25°C", "en":"Die shear @25°C", "ja":"ダイシェア @25°C"},
"Die Shear @260°C": {"zh_TW":"Die Shear @260°C", "zh_CN":"Die Shear @260°C", "en":"Die shear @260°C", "ja":"ダイシェア @260°C"},
"Die 尺寸": {"zh_TW":"Die 尺寸", "zh_CN":"Die 尺寸", "en":"Die size", "ja":"ダイサイズ"},
"T 型剝離強度": {"zh_TW":"T 型剝離強度", "zh_CN":"T 型剥离强度", "en":"T-peel strength", "ja":"T 型剥離強さ"},
"90° 剝離強度": {"zh_TW":"90° 剝離強度", "zh_CN":"90° 剥离强度", "en":"90° peel strength", "ja":"90° 剥離強さ"},
"180° 剝離強度": {"zh_TW":"180° 剝離強度", "zh_CN":"180° 剥离强度", "en":"180° peel strength", "ja":"180° 剥離強さ"},
"剝離基材": {"zh_TW":"剝離基材", "zh_CN":"剥离基材", "en":"Peel substrate", "ja":"剥離基材"},
"交叉切割附著力": {"zh_TW":"交叉切割附著力", "zh_CN":"交叉切割附着力", "en":"Cross-cut adhesion", "ja":"クロスカット密着性"},
"DMA": {"zh_TW":"DMA", "zh_CN":"DMA", "en":"DMA", "ja":"DMA"},
"MIL-STD-883 / SEMI": {"zh_TW":"MIL-STD-883 / SEMI", "zh_CN":"MIL-STD-883 / SEMI", "en":"MIL-STD-883 / SEMI", "ja":"MIL-STD-883 / SEMI"},
"ASTM D3359 (0B-5B)": {"zh_TW":"ASTM D3359 (0B-5B)", "zh_CN":"ASTM D3359 (0B-5B)", "en":"ASTM D3359 (0B-5B)", "ja":"ASTM D3359 (0B-5B)"},
}

def _load_lang():
    global _CURRENT_LANG
    if os.path.exists(LANG_CFG_FILE):
        try:
            with open(LANG_CFG_FILE, 'r', encoding='utf-8') as f:
                d = json.load(f)
                if d.get('lang') in SUPPORTED_LANGS: _CURRENT_LANG = d['lang']
        except Exception: pass

def _save_lang(lang):
    global _CURRENT_LANG
    _CURRENT_LANG = lang
    try:
        with open(LANG_CFG_FILE, 'w', encoding='utf-8') as f: json.dump({"lang": lang}, f)
    except Exception: pass

def T(key, *args):
    entry = _TRANSLATIONS.get(key)
    if not entry: return key
    text = entry.get(_CURRENT_LANG) or entry.get("zh_TW", key)
    if args:
        try: text = text.format(*args)
        except Exception: pass
    return text

_load_lang()

_PROPCAT_MAP = {
    "1.Uncured": "propcat_1", "2.Curing": "propcat_2",
    "3.Mechanical": "propcat_3", "4.Thermal": "propcat_4",
    "5.Chemical": "propcat_5", "6.Electrical": "propcat_6",
    "7.Reliability": "propcat_7", "8.Custom": "propcat_custom",
}
_LEGACY_PROPCAT = {
    "1.未固化屬性": "1.Uncured", "2.固化過程": "2.Curing",
    "3.機械屬性": "3.Mechanical", "4.熱屬性": "4.Thermal",
    "5.化學環境": "5.Chemical", "6.電屬性": "6.Electrical",
    "7.自定義": "7.Custom", "7.Custom": "8.Custom",
}
def _migrate_propcat_key(key):
    """Migrate legacy prop category keys."""
    return _LEGACY_PROPCAT.get(key, key)

CUSTOM_CAT_CFG_FILE = "custom_categories.json"
_custom_cats = []

def _load_custom_cats():
    global _custom_cats
    if os.path.exists(CUSTOM_CAT_CFG_FILE):
        try:
            with open(CUSTOM_CAT_CFG_FILE, 'r', encoding='utf-8') as f: _custom_cats = json.load(f)
        except Exception: _custom_cats = []

def _save_custom_cats():
    try:
        with open(CUSTOM_CAT_CFG_FILE, 'w', encoding='utf-8') as f: json.dump(_custom_cats, f, ensure_ascii=False, indent=2)
    except Exception: pass

_load_custom_cats()

def T_propcat(cat):
    migrated = _migrate_propcat_key(cat)
    tkey = _PROPCAT_MAP.get(migrated)
    if tkey: return T(tkey)
    for cc in _custom_cats:
        if cc.get("key") == cat: return cc.get(_CURRENT_LANG) or cc.get("zh_TW", cat)
    return cat

def _propcat_reverse(display):
    for internal_key, tkey in _PROPCAT_MAP.items():
        if T(tkey) == display: return internal_key
    for cc in _custom_cats:
        for lang in SUPPORTED_LANGS:
            if cc.get(lang) == display: return cc["key"]
    return display

def get_cat_cn():
    return {"resins": T("cat_resins"), "hardeners": T("cat_hardeners"), "additives": T("cat_additives"), "fillers": T("cat_fillers"), "catalysts": T("cat_catalysts")}

CUSTOM_MAT_CAT_FILE = "custom_mat_cats.json"
_custom_mat_cats = []

def _load_custom_mat_cats():
    global _custom_mat_cats
    if os.path.exists(CUSTOM_MAT_CAT_FILE):
        try:
            with open(CUSTOM_MAT_CAT_FILE, 'r', encoding='utf-8') as f: _custom_mat_cats = json.load(f)
        except Exception: _custom_mat_cats = []

def _save_custom_mat_cats():
    try:
        with open(CUSTOM_MAT_CAT_FILE, 'w', encoding='utf-8') as f: json.dump(_custom_mat_cats, f, ensure_ascii=False, indent=2)
    except Exception: pass

_load_custom_mat_cats()

def get_mat_cat_display(key):
    disp = get_cat_cn()
    if key in disp: return disp[key]
    for mc in _custom_mat_cats:
        if mc['key'] == key: return mc.get(_CURRENT_LANG) or mc.get('zh_TW', key)
    return key

def get_all_cat_display():
    d = dict(get_cat_cn())
    for mc in _custom_mat_cats: d[mc['key']] = mc.get(_CURRENT_LANG) or mc.get('zh_TW', mc['key'])
    return d

def get_all_slot_counts():
    d = dict(SLOT_COUNTS)
    for mc in _custom_mat_cats: d[mc['key']] = 20
    return d

def get_all_slot_fields():
    d = dict(SLOT_FIELDS)
    for mc in _custom_mat_cats:
        fields = ["Name", "Mass_g", "Pct"]
        if mc.get('has_eew'): fields.append("EEW")
        if mc.get('has_type'): fields.append("Type")
        if mc.get('has_appearance'): fields.append("Appearance")
        if mc.get('has_viscosity'): fields.append("Viscosity")
        if mc.get('has_dk'): fields.append("Dk")
        if mc.get('has_surface_energy'): fields.append("SurfEnergy")
        if mc.get('has_structure'): fields.append("Structure")
        if mc.get('has_cl'): fields.append("Cl_ppm")
        if mc.get('has_source'): fields.append("Source")
        d[mc['key']] = fields
    return d

def get_all_cat_cn():
    d = dict(CAT_CN)
    for mc in _custom_mat_cats: d[mc['key']] = mc.get('csv_name', mc.get('zh_TW', mc['key']))
    return d

def _get_custom_mat_cat(key):
    for mc in _custom_mat_cats:
        if mc['key'] == key: return mc
    return None

MAT_DB_FILE      = "epoxy_db.csv"
RECIPE_DB_FILE   = "recipe_database.csv"
CUSTOM_PROP_FILE = "custom_properties.csv"
MAT_COL_CFG_FILE = "mat_col_config.json"

SLOT_COUNTS = {"resins": 4, "hardeners": 4, "additives": 3, "fillers": 3, "catalysts": 3}

SLOT_FIELDS = {
    "resins":    ["Name","Mass_g","Pct","EEW","Type","Structure","Cl_ppm"],
    "hardeners": ["Name","Mass_g","Pct","Eq","Subtype","Corr_pct","Structure","Cl_ppm"],
    "additives": ["Name","Mass_g","Pct","Type","Cl_ppm"],
    "fillers":   ["Name","Mass_g","Pct","Type","Cl_ppm"],
    "catalysts": ["Name","Mass_g","Pct","Type","Cl_ppm"],
}
CAT_CN = {"resins":"Resins","hardeners":"Hardeners","additives":"Additives","fillers":"Fillers","catalysts":"Catalysts"}

_LEGACY_CAT_CN = {"樹脂":"Resins","固化劑":"Hardeners","助劑":"Additives","填料":"Fillers","催化劑":"Catalysts"}
_LEGACY_FIELD = {"名稱":"Name","質量_g":"Mass_g","佔比%":"Pct","EEW":"EEW","類型":"Type",
                 "分子結構":"Structure","氯_ppm":"Cl_ppm","當量":"Eq","子類型":"Subtype",
                 "校正%":"Corr_pct","外觀":"Appearance","黏度":"Viscosity","Dk":"Dk",
                 "表面能":"SurfEnergy","來源":"Source"}
_LEGACY_FIXED = {"配方名稱":"RecipeName","批次號":"BatchNo","建立日期":"DateCreated",
                 "計算模式":"CalcMode","總質量_g":"TotalMass_g","總氯含量_ppm":"TotalCl_ppm"}

_HSUBTYPE_INTERNAL = ["amine","polyamide","anhydride","mercaptan","hydroxyl"]
_HSUBTYPE_DISPLAY  = ["h_amine","h_polyamide","h_anhydride","h_mercaptan","h_hydroxyl"]
_HSUBTYPE_LEGACY   = {"胺類":"amine","聚酰胺":"polyamide","聚醯胺":"polyamide","酸酐":"anhydride","巯基":"mercaptan","巰基":"mercaptan","羥基":"hydroxyl"}
def _norm_hsubtype(val):
    """將舊版中文或翻譯顯示值正規化為內部英文 key"""
    if val in _HSUBTYPE_INTERNAL: return val
    if val in _HSUBTYPE_LEGACY: return _HSUBTYPE_LEGACY[val]
    for i, dk in enumerate(_HSUBTYPE_DISPLAY):
        for lang in SUPPORTED_LANGS:
            tr = _TRANSLATIONS.get(dk, {}).get(lang, "")
            if tr == val: return _HSUBTYPE_INTERNAL[i]
    return val
def _hsubtype_display(internal_key):
    """內部英文 key → 當前語言顯示文字"""
    if internal_key in _HSUBTYPE_INTERNAL:
        idx = _HSUBTYPE_INTERNAL.index(internal_key)
        return T(_HSUBTYPE_DISPLAY[idx])
    return internal_key

def _migrate_col_name(col):
    """Migrate legacy CSV column name."""
    if col in _LEGACY_FIXED: return _LEGACY_FIXED[col]
    migrated = col
    for old, new in _LEGACY_CAT_CN.items():
        if migrated.startswith(old): migrated = new + migrated[len(old):]; break
    for old, new in _LEGACY_FIELD.items():
        if migrated.endswith("_" + old): migrated = migrated[:migrated.rfind("_" + old)] + "_" + new; break
    return migrated

def _migrate_row(row):
    """Migrate recipe row keys."""
    return {_migrate_col_name(k): v for k, v in row.items()}

def _get_builtin_mat_cols():
    return [
        {"db_key":"Name",      "display":T("builtin_col_name"), "unit":"",    "data_key":"_name",  "visible":True, "builtin":True, "locked":True},
        {"db_key":"Type",      "display":T("builtin_col_type"), "unit":"",    "data_key":"type",   "visible":True, "builtin":True},
        {"db_key":"EEW_AHEW", "display":T("builtin_col_eq"),   "unit":"",    "data_key":"_eq",    "visible":True, "builtin":True, "special":True},
        {"db_key":"Cl_ppm",   "display":T("builtin_col_cl"),   "unit":"ppm", "data_key":"cl",     "visible":True, "builtin":True},
    ]

# V6.4.3: 物性/群組/方法多語言查找
# 設計：以中文 (zh_TW) 原字串作為 _TRANSLATIONS 鍵；未翻譯者回退為該中文
# → CSV 欄位名保持向下相容，同時支援任意語言切換
def T_prop(name):
    """Translate property name via _TRANSLATIONS; fallback to original (zh_TW)."""
    if not name: return name
    entry = _TRANSLATIONS.get(name)
    if not entry: return name
    return entry.get(_CURRENT_LANG) or entry.get("zh_TW", name)

def T_group(name):
    """Translate group name via _TRANSLATIONS; fallback to original (zh_TW)."""
    if not name: return name
    entry = _TRANSLATIONS.get(name)
    if not entry: return name
    return entry.get(_CURRENT_LANG) or entry.get("zh_TW", name)

def T_method(name):
    """Translate test method via _TRANSLATIONS; fallback to original.
    For pure ASTM/JIS/ISO codes without Chinese (e.g. 'ASTM D638'),
    look-up will miss and fall back to the code itself — as desired."""
    if not name: return name
    entry = _TRANSLATIONS.get(name)
    if not entry: return name
    return entry.get(_CURRENT_LANG) or entry.get("zh_TW", name)

PREDEFINED_PROPS = {
    "1.Uncured": [
        ("__group__", "外觀與流變", [
            ("常溫狀態 (25°C)", "", "目視觀察"),
            ("顏色", "", "目視/Gardner色標"),
            ("黏度 (cP, 25°C)", "cP", "Brookfield旋轉黏度計"),
            ("黏度 (Pa·s, 25°C)", "Pa·s", "流變儀 (錐板/平板)"),
            ("觸變指數 TI (η1/η10)", "", "Brookfield 1rpm/10rpm"),
            ("流淌性 Slump", "mm", "垂直掛片法"),
        ]),
        ("__group__", "物理常數", [
            ("比重 SG (25°C)", "", "比重瓶法/密度計"),
            ("比重 SG (固化後)", "", "阿基米德法"),
            ("折射率 nD (25°C)", "", "阿貝折射儀"),
            ("體積收縮率", "%", "比重法 (固化前後)"),
        ]),
        ("__group__", "操作性", [
            ("適用期 Pot Life (25°C)", "min", "黏度倍增法 @25°C"),
            ("適用期 Pot Life (指定溫度)", "min", "黏度倍增法"),
            ("保質期 Shelf Life", "月", "≤X°C 儲存"),
            ("擠出性 (卡式管)", "g/min", "氣壓擠出 @指定壓力"),
        ]),
    ],
    "2.Curing": [
        ("__group__", "凝膠測試", [
            ("凝膠時間 Gel Time", "sec", "熱板法"),
            ("凝膠測試溫度", "°C", ""),
            ("凝膠時間 (恆溫 DSC)", "min", "恆溫 DSC"),
        ]),
        ("__group__", "DSC 分析", [
            ("DSC 起始固化溫度 Ti", "°C", "DSC 動態掃描 (onset)"),
            ("DSC 放熱峰溫度 Tp", "°C", "DSC 動態掃描 (peak)"),
            ("DSC 反應熱 ΔH", "J/g", "DSC 動態掃描"),
            ("DSC 升溫速率", "°C/min", ""),
            ("DSC 殘餘反應熱", "J/g", "DSC (固化後再掃描)"),
            ("固化度 α", "%", "1 - ΔH_residual/ΔH_total"),
        ]),
        ("__group__", "固化條件", [
            ("推薦固化條件", "", "溫度×時間"),
            ("後固化條件", "", "溫度×時間"),
            ("最低固化溫度", "°C", ""),
            ("指觸乾燥時間", "min", "指觸法 @指定溫度"),
        ]),
    ],
    "3.Mechanical": [
        ("__group__", "硬度", [
            ("硬度 Shore A", "", "ASTM D2240 / JIS K6253"),
            ("硬度 Shore D", "", "ASTM D2240 / JIS K6253"),
            ("鉛筆硬度", "", "JIS K5600-5-4"),
        ]),
        ("__group__", "拉伸性能", [
            ("拉伸強度", "MPa", "ASTM D638 / JIS K7161"),
            ("拉伸模量", "GPa", "ASTM D638 / JIS K7161"),
            ("斷裂伸長率", "%", "ASTM D638 / JIS K7161"),
        ]),
        ("__group__", "彎曲性能", [
            ("彎曲強度", "MPa", "ASTM D790 / JIS K7171"),
            ("彎曲模量", "GPa", "ASTM D790 / JIS K7171"),
        ]),
        ("__group__", "壓縮與衝擊", [
            ("壓縮強度", "MPa", "ASTM D695"),
            ("壓縮模量", "GPa", "ASTM D695"),
            ("衝擊強度 Charpy", "kJ/m²", "ISO 179"),
            ("衝擊強度 Izod", "J/m", "ASTM D256"),
        ]),
        ("__group__", "彈性模量", [
            ("楊氏模量 (拉伸)", "GPa", "ASTM D638 / JIS K7161"),
            ("儲存模量 E' @25°C", "GPa", "DMA"),
            ("儲存模量 E' @260°C", "MPa", "DMA"),
            ("損耗因子 tan δ @25°C", "", "DMA"),
        ]),
        ("__group__", "接著/剪切強度", [
            ("搭接剪切強度 Al-Al", "MPa", "ASTM D1002 / JIS K6850"),
            ("搭接剪切強度 Cu-Cu", "MPa", "ASTM D1002 / JIS K6850"),
            ("搭接剪切強度 SUS-SUS", "MPa", "ASTM D1002"),
            ("搭接剪切強度 FR4-FR4", "MPa", "ASTM D1002"),
            ("搭接剪切強度 Glass-Glass", "MPa", "ASTM D1002"),
            ("搭接剪切溫度", "°C", ""),
            ("Die Shear (晶片剪切) @25°C", "kgf", "MIL-STD-883 / SEMI"),
            ("Die Shear @260°C", "kgf", "MIL-STD-883 / SEMI"),
            ("Die 尺寸", "mm", ""),
        ]),
        ("__group__", "剝離與接著", [
            ("T 型剝離強度", "N/mm", "ASTM D1876 / JIS K6854"),
            ("90° 剝離強度", "N/mm", "JIS K6854"),
            ("180° 剝離強度", "N/mm", "ASTM D903"),
            ("剝離基材", "", ""),
            ("交叉切割附著力", "級", "ASTM D3359 (0B-5B)"),
        ]),
    ],
    "4.Thermal": [
        ("__group__", "玻璃轉化溫度 Tg", [
            ("Tg-DSC (ΔCp midpoint)", "°C", "DSC 二次升溫"),
            ("Tg-DMA (tan δ peak)", "°C", "DMA 拉伸/三點彎曲"),
            ("Tg-DMA (E' onset)", "°C", "DMA 儲存模量轉折"),
            ("Tg-TMA (膨脹轉折)", "°C", "TMA"),
            ("DMA 升溫速率/頻率", "", "e.g. 3°C/min, 1Hz"),
        ]),
        ("__group__", "熱膨脹", [
            ("CTE α1 (<Tg)", "ppm/°C", "TMA"),
            ("CTE α2 (>Tg)", "ppm/°C", "TMA"),
        ]),
        ("__group__", "耐熱性", [
            ("熱分解溫度 Td5%", "°C", "TGA (5% wt loss, N₂)"),
            ("熱分解溫度 Td5% (Air)", "°C", "TGA (5% wt loss, Air)"),
            ("殘碳率 @800°C", "%", "TGA (N₂)"),
            ("導熱率", "W/(m·K)", "Hot Disk / Laser Flash"),
            ("HDT 熱變形溫度", "°C", "ASTM D648 (0.45/1.8MPa)"),
            ("UL94 阻燃等級", "", "UL94 V-0/V-1/V-2/HB"),
            ("LOI 極限氧指數", "%", "ASTM D2863"),
        ]),
        ("__group__", "回焊耐性", [
            ("回焊耐性 (260°C)", "", "Pass/Fail, 次數"),
            ("回焊耐性 (288°C)", "", "Pass/Fail, 次數"),
            ("回焊裂紋/脫層", "", "SAT/X-ray 檢查"),
        ]),
        ("__group__", "回焊氣密性", [
            ("氣密性 — 回焊前", "Pa·cm³/s", "He 洩漏檢測 (初始值)"),
            ("氣密性 — 回焊 1次後", "Pa·cm³/s", "He 洩漏檢測"),
            ("氣密性 — 回焊 2次後", "Pa·cm³/s", "He 洩漏檢測"),
            ("氣密性 — 回焊 3次後", "Pa·cm³/s", "He 洩漏檢測"),
            ("氣密性判定標準", "", "e.g. ≤1×10⁻⁸ Pa·cm³/s"),
            ("氣密性結論", "", "Pass/Fail"),
        ]),
    ],
    "5.Chemical": [
        ("__group__", "吸濕性", [
            ("吸水率 (24h/25°C)", "%", "ASTM D570"),
            ("吸水率 (煮沸2h)", "%", "ASTM D570"),
            ("吸濕率 (85°C/85%RH)", "%", "恆溫恆濕箱"),
            ("吸濕飽和時間", "h", "85°C/85%RH"),
        ]),
        ("__group__", "耐化學品", [
            ("耐溶劑性 (IPA)", "", "浸泡測試 @25°C"),
            ("耐溶劑性 (Acetone)", "", "浸泡測試 @25°C"),
            ("耐溶劑性 (NMP)", "", "浸泡測試 @25°C"),
            ("耐酸性 (5% HCl)", "", "浸泡測試"),
            ("耐鹼性 (5% NaOH)", "", "浸泡測試"),
            ("耐助焊劑性", "", "浸泡測試 @指定助焊劑"),
        ]),
        ("__group__", "腐蝕與離子", [
            ("離子純度 Na⁺", "ppm", "離子色譜 IC / IPC-TM-650"),
            ("離子純度 Cl⁻", "ppm", "離子色譜 IC / IPC-TM-650"),
            ("離子純度 總萃取離子", "ppm", "IPC-TM-650 2.3.28"),
            ("銅鏡腐蝕", "", "IPC-TM-650 2.6.15"),
            ("鹽霧試驗", "h", "ASTM B117"),
        ]),
        ("__group__", "出氣量", [
            ("TML 總質量損失", "%", "ASTM E595 (125°C/24h/真空)"),
            ("CVCM 可凝揮發物", "%", "ASTM E595"),
            ("揮發分 (TGA)", "%", "TGA @指定溫度"),
        ]),
    ],
    "6.Electrical": [
        ("__group__", "介電性能", [
            ("介電常數 Dk @1MHz", "", "ASTM D150 / IPC-TM-650"),
            ("介電常數 Dk @1GHz", "", "IPC-TM-650 / Split-post"),
            ("介電常數 Dk @10GHz", "", "Split-post / Cavity"),
            ("介電損耗 Df @1MHz", "", "ASTM D150 / IPC-TM-650"),
            ("介電損耗 Df @1GHz", "", "IPC-TM-650 / Split-post"),
            ("介電損耗 Df @10GHz", "", "Split-post / Cavity"),
        ]),
        ("__group__", "絕緣性能", [
            ("體積電阻率", "Ω·cm", "ASTM D257 / JIS K6911"),
            ("表面電阻率", "Ω", "ASTM D257"),
            ("介電強度", "kV/mm", "ASTM D149 / IPC-TM-650"),
            ("絕緣電阻 (常態)", "Ω", "IPC-TM-650"),
            ("絕緣電阻 (吸濕後)", "Ω", "IPC-TM-650 (85/85後)"),
            ("CTI 漏電起痕指數", "V", "IEC 60112"),
        ]),
        ("__group__", "導電性 (導電膠適用)", [
            ("體積電阻率 (導電)", "Ω·cm", "四探針法"),
            ("接觸電阻", "mΩ", "四線法"),
        ]),
    ],
    "7.Reliability": [
        ("__group__", "溫濕度可靠性", [
            ("PCT 壓力鍋測試", "", "121°C/2atm/100%RH, 記錄時間"),
            ("HAST 高加速壽命", "", "130°C/85%RH, 記錄時間"),
            ("85/85 恆溫恆濕", "h", "85°C/85%RH, 記錄通過時間"),
            ("PCT/HAST 後接著強度", "MPa", "可靠性後剪切測試"),
            ("PCT/HAST 後絕緣電阻", "Ω", "可靠性後電阻測試"),
        ]),
        ("__group__", "溫度循環", [
            ("TCT 溫度循環", "cycles", "-40~125°C 或 -55~125°C"),
            ("TST 冷熱衝擊", "cycles", "-40~125°C (液槽/氣槽)"),
            ("TCT/TST 後外觀", "", "SAT/X-ray/顯微鏡"),
            ("TCT/TST 後接著強度", "MPa", ""),
        ]),
        ("__group__", "其他可靠性", [
            ("高溫儲存 HTSL", "h", "150°C 或 175°C"),
            ("低溫儲存 LTSL", "h", "-40°C"),
            ("UV 耐候性", "h", "ASTM G154 / QUV"),
            ("耐黃變 ΔYI", "", "ASTM D1925 (UV後)"),
            ("MSL 吸濕敏感度等級", "", "IPC/JEDEC J-STD-020 (1~6)"),
        ]),
        ("__group__", "打線與焊接", [
            ("打線接合性 Wire Bond", "", "Au/Cu wire, Pull/Shear test"),
            ("打線拉力 Wire Pull", "gf", "MIL-STD-883"),
            ("打線球剪切 Ball Shear", "gf", "JEDEC JESD22-B116"),
        ]),
    ],
    "8.Custom": [],
}
USER_PROP_FILE = "user_prop_definitions.csv"

def _build_fixed_columns():
    cols = ["RecipeName", "BatchNo", "DateCreated", "CalcMode", "TotalMass_g", "TotalCl_ppm"]
    sc = get_all_slot_counts(); sf = get_all_slot_fields(); cc = get_all_cat_cn()
    for cat, n in sc.items():
        cn = cc.get(cat, cat)
        for i in range(1, n + 1):
            for field in sf.get(cat, ["Name","Mass_g","Pct"]): cols.append(f"{cn}{i}_{field}")
    return cols

def get_fixed_columns(): return _build_fixed_columns()

def _setup_modern_styles(accent=_C.BLUE):
    """Configure ttk styles."""
    s = ttk.Style()
    s.theme_use("default")

    s.configure("Treeview",
                rowheight=30,
                font=(_FONT_FAMILY, 10),
                background="white",
                fieldbackground="white",
                foreground=_C.TEXT,
                borderwidth=0,
                relief="flat")
    s.configure("Treeview.Heading",
                font=(_FONT_FAMILY, 10, "bold"),
                background=_C.BG_LIGHT,
                foreground=_C.TEXT,
                borderwidth=0,
                relief="flat",
                padding=(8, 6))
    s.map("Treeview",
          background=[("selected", accent)],
          foreground=[("selected", "white")])
    s.map("Treeview.Heading",
          background=[("active", _C.BORDER_LT)])
    s.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    s.configure("TCombobox",
                fieldbackground="white",
                background="white",
                foreground=_C.TEXT,
                arrowsize=14,
                arrowcolor=_C.TEXT_TER,
                borderwidth=1,
                relief="flat",
                padding=(6, 5),
                font=(_FONT_FAMILY, 10))
    s.map("TCombobox",
          fieldbackground=[("readonly", "white"), ("disabled", _C.BG_LIGHT),
                           ("focus", "white"), ("!focus", "white")],
          background=[("readonly", "white"), ("active", "#fafafc"), ("!focus", "white")],
          foreground=[("disabled", _C.TEXT_TER)],
          selectbackground=[("focus", accent)],
          selectforeground=[("focus", "white")],
          bordercolor=[("focus", accent), ("!focus", _C.BORDER)])
    try:
        root = tk._default_root
        if root:
            root.option_add("*TCombobox*Listbox.font", f"{{{_FONT_FAMILY}}} 10")
            root.option_add("*TCombobox*Listbox.selectBackground", accent)
            root.option_add("*TCombobox*Listbox.selectForeground", "white")
    except Exception: pass

    s.configure("TScrollbar",
                troughcolor=_C.BG_LIGHT,
                background=_C.BTN_LIGHT,
                borderwidth=0,
                arrowsize=0,
                relief="flat",
                width=8)
    s.map("TScrollbar",
          background=[("active", _C.TAB_UNSEL), ("pressed", _C.TAB_HOVER)])

    s.configure("DbTree.Treeview", rowheight=28)
    s.configure("Recipe.Treeview", rowheight=30)

def _update_ttk_accent(accent):
    """Update ttk accent."""
    try:
        s = ttk.Style()
        s.map("Treeview", background=[("selected", accent)], foreground=[("selected", "white")])
        s.map("TCombobox", selectbackground=[("focus", accent)],
              selectforeground=[("focus", "white")],
              bordercolor=[("focus", accent), ("!focus", _C.BORDER)])
        root = tk._default_root
        if root:
            root.option_add("*TCombobox*Listbox.selectBackground", accent)
            root.option_add("*TCombobox*Listbox.selectForeground", "white")
            root.option_add("*TCombobox*Listbox.background", "white")
    except Exception: pass

class ToolTip:
    """Tooltip widget."""
    def __init__(self, widget, text="", delay=350):
        self.widget = widget; self.text = text; self._delay = delay
        self.tipwindow = None; self._id = None
        widget.bind('<Enter>', self._enter); widget.bind('<Leave>', self._leave)
    def set_text(self, t): self.text = t
    def _enter(self, _=None): self._id = self.widget.after(self._delay, self._show)
    def _leave(self, _=None):
        if self._id: self.widget.after_cancel(self._id); self._id = None
        if self.tipwindow: self.tipwindow.destroy(); self.tipwindow = None
    def _show(self, _=None):
        txt = self.text() if callable(self.text) else self.text
        if not txt: return
        try: x, y, _, _ = self.widget.bbox("insert")
        except Exception: x = y = 0
        x += self.widget.winfo_rootx() + 20; y += self.widget.winfo_rooty() + 28
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True); tw.wm_geometry(f"+{x}+{y}")
        try: tw.wm_attributes('-alpha', 0.95)
        except Exception: pass
        frame = ctk.CTkFrame(tw, corner_radius=8, fg_color=_C.TEXT, border_width=0)
        frame.pack(fill='both', expand=True)
        tk.Label(frame, text=txt, justify='left', wraplength=360,
                 background="#1d1d1f", foreground=_C.BG_LIGHT,
                 font=(_FONT_FAMILY, 9),
                 padx=10, pady=6, relief='flat', borderwidth=0).pack()

def _build_mat_tooltip(dm, cat, name):
    """Build material tooltip text."""
    info = dm.materials.get(cat, {}).get(name, {})
    if not info: return ""
    parts = [f"【{name}】"]
    if info.get('type'): parts.append(f"類型: {info['type']}")
    if info.get('appearance'): parts.append(f"外觀: {info['appearance']}")
    visc = info.get('viscosity', '')
    if visc: parts.append(f"粘度: {visc} cP (25°C)")
    eew = info.get('eew', 0)
    if eew: parts.append(f"EEW: {eew}")
    ahew = info.get('ahew', 0)
    if ahew: parts.append(f"AHEW: {ahew}")
    cl = info.get('cl', 0)
    if cl: parts.append(f"氯: {cl} ppm")
    dk = info.get('dk', '')
    if dk: parts.append(f"Dk: {dk}")
    se = info.get('surface_energy', '')
    if se: parts.append(f"表面能: {se} mN/m")
    density = info.get('density', '')
    if density: parts.append(f"密度: {density} g/cm³")
    ps = info.get('particle_size', '')
    if ps: parts.append(f"D50: {ps} μm")
    cte = info.get('cte_ppm', '')
    if cte: parts.append(f"CTE: {cte} ppm/°C")
    tk_val = info.get('thermal_cond', '')
    if tk_val: parts.append(f"導熱: {tk_val} W/(m·K)")
    er = info.get('elec_resistivity', '')
    if er: parts.append(f"電阻率: {er} Ω·cm")
    tg = info.get('tg_dsc', '')
    if tg: parts.append(f"Tg(DSC): {tg}°C")
    cost = info.get('cost_per_kg', '')
    if cost: parts.append(f"成本: ${cost}/kg")
    vol = info.get('volatile_pct', '')
    if vol: parts.append(f"揮發分: {vol}%")
    shelf = info.get('shelf_life', '')
    stor = info.get('storage_temp', '')
    if shelf or stor:
        sl_str = f"{shelf}個月" if shelf else ""
        st_str = f" @{stor}°C" if stor else ""
        parts.append(f"保質期: {sl_str}{st_str}")
    src = info.get('source', '')
    if src: parts.append(f"來源: {src}")
    desc = info.get('desc', '')
    if desc: parts.append(f"─────────\n{desc}")
    return "\n".join(parts) if len(parts) > 1 else ""

class RoundedTreeFrame(ctk.CTkFrame):
    """Apple-style rounded container for ttk.Treeview.
    Creates an inner clip frame so the rectangular Treeview
    doesn't overflow the rounded corners."""

    def __init__(self, parent, corner_radius=8, border_width=1,
                 border_color=_C.BORDER, fg_color=None, **kwargs):
        super().__init__(parent, corner_radius=corner_radius,
                         border_width=border_width, border_color=border_color,
                         fg_color=fg_color, **kwargs)
        self._inner = tk.Frame(self, bg="white", bd=0, highlightthickness=0)
        self._inner.pack(fill='both', expand=True, padx=5, pady=5)

    @property
    def inner(self):
        """Use this as parent for Treeview + Scrollbar."""
        return self._inner

class RoundedPopup:
    """Autocomplete popup."""
    _TRANS_COLOR = '#f0f1f0'

    def __init__(self, parent, accent=_C.BLUE):
        self.parent = parent; self.accent = accent
        self.win = None; self.items_frame = None; self._cb = None; self._buttons = []
        self._global_bind_id = None; self._click_token = None

    def show(self, cb, items, on_select):
        self.close()
        if not items: return
        self._cb = cb; self._on_select = on_select
        cb.update_idletasks()

        self.win = tk.Toplevel(cb)
        self.win.wm_overrideredirect(True)
        self.win.wm_attributes('-topmost', True)
        self.win.configure(bg=self._TRANS_COLOR)
        try: self.win.wm_attributes('-transparentcolor', self._TRANS_COLOR)
        except Exception: self.win.configure(bg='white')

        w = max(cb.winfo_width(), 300)
        n = min(8, len(items))
        h = n * 30 + 12
        x = cb.winfo_rootx(); y = cb.winfo_rooty() + cb.winfo_height() + 2
        self.win.geometry(f'{w}x{h}+{x}+{y}')

        container = ctk.CTkFrame(self.win, corner_radius=8, fg_color="white",
                                  border_width=1, border_color=_C.BORDER)
        container.pack(fill='both', expand=True, padx=2, pady=2)

        self.items_frame = ctk.CTkScrollableFrame(container, fg_color="white",
                                                    corner_radius=8, height=h-16)
        self.items_frame.pack(fill='both', expand=True, padx=2, pady=2)
        try: self.items_frame._scrollbar.configure(width=0)
        except Exception: pass

        self._buttons = []
        for item in items[:50]:
            btn = ctk.CTkButton(self.items_frame, text=item, anchor='w',
                                 fg_color="transparent", text_color=_C.TEXT,
                                 hover_color=_C.BG_LIGHT, corner_radius=6,
                                 font=ctk.CTkFont(family=_FONT_FAMILY, size=11),
                                 height=28, command=lambda v=item: self._pick(v))
            btn.pack(fill='x', padx=2, pady=1)
            self._buttons.append(btn)

        self._click_token = object()
        token = self._click_token
        root = cb.winfo_toplevel()
        def _handler(event, _token=token):
            if self._click_token is not _token:
                return
            self._on_global_click(event)
        self._global_bind_id = root.bind_all('<Button-1>', _handler, '+')

    def _on_global_click(self, event):
        """Close popup if user clicks outside of it."""
        if not self.win:
            return
        try:
            click_x = event.x_root
            click_y = event.y_root
            wx = self.win.winfo_rootx()
            wy = self.win.winfo_rooty()
            ww = self.win.winfo_width()
            wh = self.win.winfo_height()
            if wx <= click_x <= wx + ww and wy <= click_y <= wy + wh:
                return
            if self._cb:
                cx = self._cb.winfo_rootx()
                cy = self._cb.winfo_rooty()
                cw = self._cb.winfo_width()
                ch = self._cb.winfo_height()
                if cx <= click_x <= cx + cw and cy <= click_y <= cy + ch:
                    return
        except Exception:
            pass
        self.close()

    def _pick(self, value):
        cb = self._cb
        if cb:
            if hasattr(cb, 'set'):
                cb.set(value)
            else:
                cb.delete(0, tk.END)
                cb.insert(0, value)
            try: cb.event_generate('<<ComboboxSelected>>')
            except Exception: pass
        self.close()
        if cb:
            cb.focus_set()
            try: cb.icursor(tk.END)
            except Exception: pass
        if hasattr(self, '_on_select'): self._on_select()

    def close(self):
        self._click_token = None
        self._global_bind_id = None
        if self.win:
            try: self.win.destroy()
            except Exception: pass
            self.win = None; self.items_frame = None; self._cb = None; self._buttons = []

class AppleDropdown(ctk.CTkButton):
    """Rounded dropdown (CTkButton subclass)."""

    def __init__(self, parent, values=None, variable=None, command=None,
                 width=180, font=None, corner_radius=8,
                 fg_color=_C.BLUE, button_color=None, text_color="white",
                 dropdown_fg_color="white", dropdown_text_color=_C.TEXT,
                 dropdown_hover_color=_C.BG_LIGHT, **kwargs):

        self._values = values or []
        self._variable = variable
        # V6.4.7 CRITICAL FIX: 改名為 _user_command 避免與 CTkButton._command 衝突。
        # super().__init__(command=self._toggle) 呼叫 CTkButton.__init__，後者內部會
        # 執行 self._command = self._toggle 將我們這裡存的 command 覆蓋掉 —— 這是
        # V6.4.1~V6.4.5 語言切換完全失效的真正原因（_on_pick 呼叫 self._command(value)
        # 實際上是呼叫 self._toggle(value)，因參數數量不符而拋 TypeError 被吞掉，
        # 導致 _on_lang_change 從未被觸發）。
        self._user_command = command
        self._fg_color = fg_color
        self._button_color = button_color or fg_color
        self._text_color = text_color
        self._dd_fg = dropdown_fg_color
        self._dd_text = dropdown_text_color
        self._dd_hover = dropdown_hover_color
        self._corner_radius = corner_radius
        self._popup = None
        self._global_bind_id = None
        self._click_token = None

        init_text = ""
        if self._variable:
            init_text = self._variable.get()
        elif self._values:
            init_text = self._values[0]
        self._current = init_text

        super().__init__(
            parent, text=f"{init_text}  ▾", anchor='w',
            fg_color=self._fg_color, hover_color=self._button_color,
            text_color=self._text_color,
            corner_radius=self._corner_radius,
            font=font or ctk.CTkFont(family=_FONT_FAMILY, size=12),
            command=self._toggle, width=width, height=30,
        )

        self._last_toggle_ts = 0
        self.bind('<Button-1>', self._on_click_fallback, add='+')

        if self._variable:
            self._variable.trace_add('write', self._on_var_change)

    def _on_var_change(self, *args):
        val = self._variable.get()
        if val != self._current:
            self._current = val
            super().configure(text=f"{val}  ▾")

    def _on_click_fallback(self, event):
        """Click fallback for ScrollableFrame compatibility."""
        self.after(100, self._fallback_check)

    def _fallback_check(self):
        import time
        if time.monotonic() - self._last_toggle_ts > 0.15:
            self._toggle()

    def _toggle(self):
        import time
        self._last_toggle_ts = time.monotonic()
        if self._popup and self._popup.win:
            self._popup.close()
            self._unbind_global()
            self._popup = None
            return
        self._show_dropdown()

    def _show_dropdown(self):
        if not self._values:
            return
        self._close_dropdown()

        self._popup = _AppleDropdownPopup(self)
        self.update_idletasks()

        w = max(self.winfo_width(), 160)
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 2

        self._popup.show(x, y, w, self._values, self._current, self._on_pick)

        self._click_token = object()
        token = self._click_token
        root = self.winfo_toplevel()
        def _handler(event, _token=token):
            if self._click_token is not _token:
                return
            self._on_global_click(event)
        self._global_bind_id = root.bind_all('<Button-1>', _handler, '+')

    def _on_global_click(self, event):
        if not self._popup or not self._popup.win:
            self._unbind_global()
            return
        try:
            cx, cy = event.x_root, event.y_root
            pw = self._popup.win
            if (pw.winfo_rootx() <= cx <= pw.winfo_rootx() + pw.winfo_width() and
                pw.winfo_rooty() <= cy <= pw.winfo_rooty() + pw.winfo_height()):
                return
            bx, by = self.winfo_rootx(), self.winfo_rooty()
            if (bx <= cx <= bx + self.winfo_width() and
                by <= cy <= by + self.winfo_height()):
                return
        except Exception:
            pass
        self._close_dropdown()

    def _on_pick(self, value):
        self._current = value
        super().configure(text=f"{value}  ▾")
        if self._variable:
            self._variable.set(value)
        self._close_dropdown()
        if self._user_command:
            self._user_command(value)

    def _close_dropdown(self):
        self._unbind_global()
        if self._popup:
            self._popup.close()
            self._popup = None

    def _unbind_global(self):
        self._click_token = None
        self._global_bind_id = None

    def get(self):
        return self._current

    def set(self, value):
        self._current = value
        super().configure(text=f"{value}  ▾")
        if self._variable:
            self._variable.set(value)

    def configure(self, **kwargs):
        if 'values' in kwargs:
            self._values = kwargs.pop('values')
        if 'fg_color' in kwargs:
            self._fg_color = kwargs['fg_color']
            super().configure(fg_color=kwargs.pop('fg_color'))
        if 'button_color' in kwargs:
            self._button_color = kwargs.pop('button_color')
            super().configure(hover_color=self._button_color)
        if 'text_color' in kwargs:
            self._text_color = kwargs.pop('text_color')
            super().configure(text_color=self._text_color)
        if 'command' in kwargs:
            self._user_command = kwargs.pop('command')
        if 'variable' in kwargs:
            self._variable = kwargs.pop('variable')
        if 'font' in kwargs:
            super().configure(font=kwargs.pop('font'))
        if 'width' in kwargs:
            w = kwargs.pop('width')
            super().configure(width=w)
        if kwargs:
            super().configure(**kwargs)

class _AppleDropdownPopup:
    """Dropdown popup window."""
    _TRANS_COLOR = '#f0f1f0'

    def __init__(self, owner):
        self.owner = owner
        self.win = None

    def show(self, x, y, w, values, current, on_pick):
        self.close()
        self.win = tk.Toplevel(self.owner)
        self.win.wm_overrideredirect(True)
        self.win.wm_attributes('-topmost', True)
        self.win.configure(bg=self._TRANS_COLOR)
        try:
            self.win.wm_attributes('-transparentcolor', self._TRANS_COLOR)
        except Exception:
            self.win.configure(bg='white')

        n = min(10, len(values))
        h = n * 32 + 12
        self.win.geometry(f'{w}x{h}+{x}+{y}')

        container = ctk.CTkFrame(self.win, corner_radius=8, fg_color="white",
                                  border_width=1, border_color=_C.BORDER)
        container.pack(fill='both', expand=True, padx=2, pady=2)

        sf = ctk.CTkScrollableFrame(container, fg_color="white",
                                     corner_radius=6, height=h - 16)
        sf.pack(fill='both', expand=True, padx=2, pady=2)
        try:
            sf._scrollbar.configure(width=0)
        except Exception:
            pass

        for val in values:
            is_sel = (val == current)
            btn = ctk.CTkButton(
                sf, text=f"  {val}" + ("  ✓" if is_sel else ""),
                anchor='w',
                fg_color=self.owner._fg_color if is_sel else "transparent",
                text_color="white" if is_sel else _C.TEXT,
                hover_color=_C.BG_LIGHT if not is_sel else self.owner._fg_color,
                corner_radius=6,
                font=ctk.CTkFont(family=_FONT_FAMILY, size=11),
                height=28,
                command=lambda v=val: on_pick(v),
            )
            btn.pack(fill='x', padx=2, pady=1)

    def close(self):
        if self.win:
            try:
                self.win.destroy()
            except Exception:
                pass
            self.win = None

class DataManager:
    CAT_MAP     = CAT_CN
    CAT_MAP_REV = {v: k for k, v in CAT_CN.items()}
    def __init__(self):
        self.mat_columns   = self._load_mat_col_config()
        self.materials     = self._load_materials()
        self.custom_props  = self._load_custom_props()

    def _load_mat_col_config(self):
        cols = [dict(c) for c in _get_builtin_mat_cols()]
        if os.path.exists(MAT_COL_CFG_FILE):
            try:
                with open(MAT_COL_CFG_FILE, 'r', encoding='utf-8') as f: saved = json.load(f)
                vis_map = {c['db_key']: c.get('visible', True) for c in saved}
                for c in cols:
                    if c['db_key'] in vis_map: c['visible'] = vis_map[c['db_key']]
                builtin_keys = {c['db_key'] for c in cols}
                for c in saved:
                    if c['db_key'] not in builtin_keys:
                        c['builtin'] = False
                        c.setdefault('data_key', c['db_key'].lower())
                        c.setdefault('visible', True)
                        cols.append(c)
            except Exception: pass
        return cols

    def _save_mat_col_config(self):
        try:
            save_list = [{"db_key": c['db_key'], "display": c['display'], "unit": c.get('unit',''), "visible": c.get('visible',True), "builtin": c.get('builtin',True), "data_key": c.get('data_key','')} for c in self.mat_columns]
            with open(MAT_COL_CFG_FILE, 'w', encoding='utf-8') as f: json.dump(save_list, f, ensure_ascii=False, indent=2)
        except Exception as e: pass

    def get_visible_mat_cols(self): return [c for c in self.mat_columns if c.get('visible', True)]
    def get_custom_mat_cols(self): return [c for c in self.mat_columns if not c.get('builtin', True)]

    def add_mat_column(self, db_key, display, unit=""):
        if any(c['db_key'] == db_key for c in self.mat_columns): return False
        self.mat_columns.append({"db_key": db_key, "display": display, "unit": unit, "data_key": db_key.lower(), "visible": True, "builtin": False})
        self._save_mat_col_config(); return True

    def remove_mat_column(self, db_key):
        self.mat_columns = [c for c in self.mat_columns if c['db_key'] != db_key or c.get('builtin')]
        self._save_mat_col_config()

    _MAT_FIELDS = ['Category','Name','Type','Appearance','Viscosity_cP25','Dk','Surface_Energy','Hardener_Subtype','EEW','AHEW','Polyamide_Eq','Anhydride_Eq','Mercapto_Eq','Hydroxyl_Eq','Amine_Value','Acid_Value','Hydroxyl_Value','MW','Func_Group_Num','f_factor','C_factor','Cl_ppm','Molecular_Structure','Source','Description','Density_gcm3','Particle_Size_D50_um','Specific_Surface_Area_m2g','Particle_Shape','Oil_Absorption_ml100g','Mohs_Hardness','Refractive_Index','Cost_per_kg','Volatile_pct','Tg_DSC','Shelf_Life_months','Storage_Temp_C','CTE_ppm','Thermal_Cond_WmK','Elec_Resistivity_Ohm_cm']

    def _load_materials(self):
        data = {k: {} for k in get_all_slot_counts()}
        if not os.path.exists(MAT_DB_FILE): return data
        try:
            with open(MAT_DB_FILE, 'r', encoding='utf-8-sig', newline='') as f:
                for row in csv.DictReader(f):
                    cat = row.get('Category','')
                    if cat in data and row.get('Name'):
                        info = {'type': row.get('Type',''), 'appearance': row.get('Appearance',''), 'viscosity': row.get('Viscosity_cP25','') or row.get('Viscosity',''), 'dk': row.get('Dk',''), 'surface_energy': row.get('Surface_Energy',''), 'h_subtype': _norm_hsubtype(row.get('Hardener_Subtype','')), 'eew': float(row.get('EEW',0) or 0), 'ahew': float(row.get('AHEW',0) or 0), 'polyamide_eq': float(row.get('Polyamide_Eq',0) or 0), 'anhydride_eq': float(row.get('Anhydride_Eq',0) or 0), 'mercapto_eq': float(row.get('Mercapto_Eq',0) or 0), 'hydroxyl_eq': float(row.get('Hydroxyl_Eq',0) or 0), 'amine_value': float(row.get('Amine_Value',0) or 0), 'acid_value': float(row.get('Acid_Value',0) or 0), 'hydroxyl_value': float(row.get('Hydroxyl_Value',0) or 0), 'mw': float(row.get('MW',0) or 0), 'func_group_num': float(row.get('Func_Group_Num',0) or 0), 'f_factor': float(row.get('f_factor',1.0) or 1.0), 'c_factor': float(row.get('C_factor',1.0) or 1.0), 'cl': float(row.get('Cl_ppm',0) or 0), 'structure': row.get('Molecular_Structure',''), 'source': row.get('Source',''), 'desc': row.get('Description',''),
                                'density': row.get('Density_gcm3',''), 'particle_size': row.get('Particle_Size_D50_um',''), 'ssa': row.get('Specific_Surface_Area_m2g',''), 'particle_shape': row.get('Particle_Shape',''), 'oil_absorption': row.get('Oil_Absorption_ml100g',''), 'mohs': row.get('Mohs_Hardness',''), 'refractive_index': row.get('Refractive_Index',''),
                                'cost_per_kg': row.get('Cost_per_kg',''), 'volatile_pct': row.get('Volatile_pct',''), 'tg_dsc': row.get('Tg_DSC',''), 'shelf_life': row.get('Shelf_Life_months',''), 'storage_temp': row.get('Storage_Temp_C',''),
                                'cte_ppm': row.get('CTE_ppm',''), 'thermal_cond': row.get('Thermal_Cond_WmK',''), 'elec_resistivity': row.get('Elec_Resistivity_Ohm_cm','')}
                        for col in self.get_custom_mat_cols(): info[col['data_key']] = row.get(col['db_key'], '')
                        data[cat][row['Name']] = info
        except Exception as e: pass
        return data

    def save_materials(self):
        try:
            extra_keys = [c['db_key'] for c in self.get_custom_mat_cols()]
            fields = self._MAT_FIELDS + extra_keys
            with open(MAT_DB_FILE, 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
                for cat, items in self.materials.items():
                    for name, info in items.items():
                        rd = {'Category':cat,'Name':name, 'Type':info.get('type',''), 'Appearance':info.get('appearance',''), 'Viscosity_cP25':info.get('viscosity',''), 'Dk':info.get('dk',''), 'Surface_Energy':info.get('surface_energy',''), 'Hardener_Subtype':info.get('h_subtype',''), 'EEW':info.get('eew',0),'AHEW':info.get('ahew',0), 'Polyamide_Eq':info.get('polyamide_eq',0),'Anhydride_Eq':info.get('anhydride_eq',0), 'Mercapto_Eq':info.get('mercapto_eq',0),'Hydroxyl_Eq':info.get('hydroxyl_eq',0), 'Amine_Value':info.get('amine_value',0),'Acid_Value':info.get('acid_value',0), 'Hydroxyl_Value':info.get('hydroxyl_value',0),'MW':info.get('mw',0), 'Func_Group_Num':info.get('func_group_num',0),'f_factor':info.get('f_factor',1.0), 'C_factor':info.get('c_factor',1.0),'Cl_ppm':info.get('cl',0), 'Molecular_Structure':info.get('structure',''), 'Source':info.get('source',''),'Description':info.get('desc',''),
                               'Density_gcm3':info.get('density',''), 'Particle_Size_D50_um':info.get('particle_size',''), 'Specific_Surface_Area_m2g':info.get('ssa',''), 'Particle_Shape':info.get('particle_shape',''), 'Oil_Absorption_ml100g':info.get('oil_absorption',''), 'Mohs_Hardness':info.get('mohs',''), 'Refractive_Index':info.get('refractive_index',''),
                               'Cost_per_kg':info.get('cost_per_kg',''), 'Volatile_pct':info.get('volatile_pct',''), 'Tg_DSC':info.get('tg_dsc',''), 'Shelf_Life_months':info.get('shelf_life',''), 'Storage_Temp_C':info.get('storage_temp',''),
                               'CTE_ppm':info.get('cte_ppm',''), 'Thermal_Cond_WmK':info.get('thermal_cond',''), 'Elec_Resistivity_Ohm_cm':info.get('elec_resistivity','')}
                        for col in self.get_custom_mat_cols(): rd[col['db_key']] = info.get(col['data_key'], '')
                        w.writerow(rd)
        except Exception as e: messagebox.showerror(T("error"), str(e))

    def get_active_eq(self, info):
        st = _norm_hsubtype(info.get('h_subtype', ''))
        eq_map = {'polyamide':'polyamide_eq','anhydride':'anhydride_eq','mercaptan':'mercapto_eq','hydroxyl':'hydroxyl_eq'}
        return info.get(eq_map.get(st, 'ahew'), 1) or 1

    def _read_recipe_rows(self):
        rows = []
        if not os.path.exists(RECIPE_DB_FILE): return rows
        try:
            with open(RECIPE_DB_FILE, 'r', encoding='utf-8-sig', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader: rows.append(_migrate_row(dict(row)))
        except Exception as e: pass
        return rows

    def _write_recipe_rows(self, rows):
        if not rows:
            if os.path.exists(RECIPE_DB_FILE): os.remove(RECIPE_DB_FILE)
            return
        seen_extra = []
        for row in rows:
            for k in row.keys():
                if k not in get_fixed_columns() and k not in seen_extra: seen_extra.append(k)
        all_cols = get_fixed_columns() + seen_extra
        try:
            with open(RECIPE_DB_FILE, 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.DictWriter(f, fieldnames=all_cols, extrasaction='ignore'); w.writeheader()
                for row in rows: w.writerow({c: row.get(c, '') for c in all_cols})
        except Exception as e: messagebox.showerror(T("error"), str(e))

    def get_recipe_names(self): return [r.get("RecipeName","") for r in self._read_recipe_rows()]
    def get_recipe_row(self, name):
        for r in self._read_recipe_rows():
            if r.get("RecipeName") == name: return r
        return {}

    def get_prop_columns(self):
        if not os.path.exists(RECIPE_DB_FILE): return []
        try:
            with open(RECIPE_DB_FILE, 'r', encoding='utf-8-sig', newline='') as f: headers = next(csv.reader(f), [])
            return [h for h in headers if h not in get_fixed_columns()]
        except Exception: return []

    def build_recipe_row(self, recipe_name, batch_no, calc_mode, materials_list, total_mass, total_cl):
        row = {c: "" for c in get_fixed_columns()}
        row["RecipeName"] = recipe_name; row["BatchNo"] = batch_no; row["DateCreated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row["CalcMode"] = calc_mode; row["TotalMass_g"] = f"{total_mass:.4f}"; row["TotalCl_ppm"] = f"{total_cl:.2f}"
        all_sc = get_all_slot_counts(); all_sf = get_all_slot_fields(); all_cn = get_all_cat_cn()
        counters = {c: 0 for c in all_sc}
        for m in materials_list:
            cat = m.get("orig_cat")
            if cat not in counters: continue
            counters[cat] += 1; idx = counters[cat]
            if idx > all_sc.get(cat, 3): continue
            cn = all_cn.get(cat, cat); name = m["name"]; info = self.materials.get(cat,{}).get(name, {})
            mass = m.get("rounded_mass", 0); pct = m.get("pct", 0)
            fields = all_sf.get(cat, ["Name","Mass_g","Pct"])
            row[f"{cn}{idx}_Name"] = name; row[f"{cn}{idx}_Mass_g"] = str(mass); row[f"{cn}{idx}_Pct"] = f"{pct:.4f}"
            if cat == "resins":
                row[f"{cn}{idx}_EEW"] = str(info.get("eew","")); row[f"{cn}{idx}_Type"] = info.get("type",""); row[f"{cn}{idx}_Structure"] = info.get("structure","")
            elif cat == "hardeners":
                row[f"{cn}{idx}_Eq"] = str(self.get_active_eq(info)); row[f"{cn}{idx}_Subtype"] = info.get("h_subtype",""); row[f"{cn}{idx}_Corr_pct"] = str(m.get("corr_pct","")); row[f"{cn}{idx}_Structure"] = info.get("structure","")
            else:
                if "EEW" in fields: row[f"{cn}{idx}_EEW"] = str(info.get("eew",""))
                if "Type" in fields: row[f"{cn}{idx}_Type"] = info.get("type","")
                if "Appearance" in fields: row[f"{cn}{idx}_Appearance"] = info.get("appearance","")
                if "Viscosity" in fields: row[f"{cn}{idx}_Viscosity"] = info.get("viscosity","")
                if "Dk" in fields: row[f"{cn}{idx}_Dk"] = info.get("dk","")
                if "SurfEnergy" in fields: row[f"{cn}{idx}_SurfEnergy"] = info.get("surface_energy","")
                if "Structure" in fields: row[f"{cn}{idx}_Structure"] = info.get("structure","")
                if "Cl_ppm" in fields: row[f"{cn}{idx}_Cl_ppm"] = str(info.get("cl",""))
                if "Source" in fields: row[f"{cn}{idx}_Source"] = info.get("source","")
        return row

    def save_new_recipe(self, row_dict):
        rows = self._read_recipe_rows()
        for existing in rows:
            if existing.get("RecipeName") == row_dict.get("RecipeName"):
                for col in self.get_prop_columns(): row_dict.setdefault(col, existing.get(col, ""))
                existing.update(row_dict); self._write_recipe_rows(rows); return
        rows.append(row_dict); self._write_recipe_rows(rows)

    def update_recipe_props(self, recipe_name, props_dict):
        rows = self._read_recipe_rows()
        found = False
        for row in rows:
            if row.get("RecipeName") == recipe_name: row.update(props_dict); found = True; break
        if not found: return False
        self._write_recipe_rows(rows); return True

    def delete_recipe(self, recipe_name):
        rows = [r for r in self._read_recipe_rows() if r.get("RecipeName") != recipe_name]
        self._write_recipe_rows(rows)

    def rename_recipe(self, old_name, new_name):
        rows = self._read_recipe_rows()
        for r in rows:
            if r.get("RecipeName") == old_name: r["RecipeName"] = new_name
        self._write_recipe_rows(rows)

    def _load_custom_props(self):
        props = []
        if os.path.exists(CUSTOM_PROP_FILE):
            try:
                with open(CUSTOM_PROP_FILE, 'r', encoding='utf-8-sig', newline='') as f:
                    for row in csv.DictReader(f): props.append(dict(row))
                os.rename(CUSTOM_PROP_FILE, CUSTOM_PROP_FILE + ".bak"); self._save_user_props_to_file(props)
            except Exception: pass
        if not os.path.exists(USER_PROP_FILE): return props
        try:
            with open(USER_PROP_FILE, 'r', encoding='utf-8-sig', newline='') as f:
                for row in csv.DictReader(f): props.append(dict(row))
        except Exception: pass
        return props

    def _save_user_props_to_file(self, props):
        fields = ["category", "name", "db_key", "unit", "method"]
        try:
            with open(USER_PROP_FILE, 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore'); w.writeheader(); w.writerows(props)
        except Exception as e: messagebox.showerror(T("error"), str(e))

    def save_custom_props(self): self._save_user_props_to_file(self.custom_props)

    def get_prop_csv_key(self, display_name):
        for p in self.custom_props:
            if p.get('name') == display_name and p.get('db_key'): return p['db_key']
        return display_name

    def get_all_builtin_names(self):
        names = set()
        for items in PREDEFINED_PROPS.values():
            for n, u, m in self._flat_iter(items): names.add(n)
        return names

    @staticmethod
    def _flat_iter(items):
        for item in items:
            if isinstance(item, tuple) and len(item) == 3 and item[0] == '__group__':
                for sub in item[2]: yield sub
            else: yield item

    def get_prop_defs_flat(self):
        deleted = {p['name'] for p in self.custom_props if p.get('category') == '_deleted'}
        result = {}
        for cat, items in PREDEFINED_PROPS.items():
            flat = [(n,u,m) for n,u,m in self._flat_iter(items) if n not in deleted]
            if flat: result[cat] = flat
        for p in self.custom_props:
            cat = _migrate_propcat_key(p.get("category") or "8.Custom")
            if cat == '_deleted': continue
            tup = (p["name"], p.get("unit",""), p.get("method",""))
            if tup not in result.setdefault(cat, []): result[cat].append(tup)
        return result

    def get_prop_defs_structured(self):
        deleted = {p['name'] for p in self.custom_props if p.get('category') == '_deleted'}
        result = {}
        for cat, items in PREDEFINED_PROPS.items():
            filtered = []
            for item in items:
                if isinstance(item, tuple) and len(item) == 3 and item[0] == '__group__':
                    _, grp_name, grp_items = item
                    kept = [(n,u,m) for n,u,m in grp_items if n not in deleted]
                    if kept: filtered.append(("__group__", grp_name, kept))
                else:
                    n, u, m = item
                    if n not in deleted: filtered.append(item)
            if filtered: result[cat] = filtered
        for p in self.custom_props:
            cat = _migrate_propcat_key(p.get("category") or "8.Custom")
            if cat == '_deleted': continue
            tup = (p["name"], p.get("unit",""), p.get("method",""))
            existing_flat = list(self._flat_iter(result.get(cat, [])))
            if tup not in existing_flat: result.setdefault(cat, []).append(tup)
        return result

    def get_all_prop_defs(self): return self.get_prop_defs_flat()
    def get_all_categories(self):
        cats = list(PREDEFINED_PROPS.keys())
        for cc in _custom_cats:
            k = cc.get("key","")
            if k and k not in cats: cats.append(k)
        for p in self.custom_props:
            c = _migrate_propcat_key(p.get("category") or "8.Custom")
            if c not in cats and c != '_deleted': cats.append(c)
        return cats
    
class ViscosityPredictor:
    DEFAULT_FILLER_DENSITY = 2.2
    DEFAULT_LIQUID_DENSITY = 1.15
    DEFAULT_PHI_MAX = 0.64
    DEFAULT_INTRINSIC_ETA = 2.5
    R_GAS = 8.314

    _SHAPE_ETA = {"Spherical":2.5,"球形":2.5,"Irregular":3.8,"不規則":3.8,"不规则":3.8,"不定形":3.8,
                  "Platelet":6.0,"片狀":6.0,"片状":6.0,"板状":6.0,
                  "Fiber":10.0,"纖維狀":10.0,"纤维状":10.0,"繊維状":10.0,
                  "Fumed (chain aggregate)":12.0,"氣相法(鏈狀聚集)":12.0,"气相法(链状聚集)":12.0,"フュームド(鎖状凝集)":12.0}
    _SHAPE_TI_K = {"Spherical":5.0,"球形":5.0,"Irregular":8.0,"不規則":8.0,"不规则":8.0,"不定形":8.0,
                   "Platelet":15.0,"片狀":15.0,"片状":15.0,"板状":15.0,
                   "Fiber":18.0,"纖維狀":18.0,"纤维状":18.0,"繊維状":18.0,
                   "Fumed (chain aggregate)":25.0,"氣相法(鏈狀聚集)":25.0,"气相法(链状聚集)":25.0,"フュームド(鎖状凝集)":25.0}
    _CSR_KW = ['csr','core-shell','core shell','mx-','kaneka mx','コアシェル']
    _DILUENT_KW = ['reactive diluent','monofunctional','mono-functional','diluent',
                    'bge','pge','c12-c14 glycidyl','agex','反応性希釈剤','反應性稀釋劑']

    _TYPE_VISC_DEFAULTS = {
        'bisphenol a': 12000, 'bpa': 12000, 'dgeba': 12000, 'yd-128': 12000,
        'bisphenol f': 3000, 'bpf': 3000, 'dgebf': 3000,
        'novolac': 30000, 'ecn': 25000, 'phenol novolac': 25000, 'cresol novolac': 50000,
        'cycloaliphatic': 350, 'alicyclic': 350,
        'reactive diluent': 15, 'monofunctional': 8,
        'dabpa': 2500, 'diallyl bisphenol a': 2500,
        'dicy': 0, 'dicyandiamide': 0,  # solid
        'amine': 20, 'aliphatic amine': 15, 'aromatic amine': 0,
        'anhydride': 50, 'acid anhydride': 50,
        'polyamide': 5000, 'amidoamine': 1000,
        'mercaptan': 200, 'thiol': 200,
        'latent': 0, 'latent catalyst': 0, 'imidazole': 0,
        'silica': 0, 'alumina': 0, 'calcium carbonate': 0,
    }

    def __init__(self, dm, phi_max=None, intrinsic_eta=None,
                 filler_density=None, liquid_density=None, temperature=25.0):
        self.dm = dm
        self.phi_max = phi_max or self.DEFAULT_PHI_MAX
        self.intrinsic_eta = intrinsic_eta or self.DEFAULT_INTRINSIC_ETA
        self.filler_density = filler_density or self.DEFAULT_FILLER_DENSITY
        self.liquid_density = liquid_density or self.DEFAULT_LIQUID_DENSITY
        self.temperature = temperature
        self._train_cache = None
        self._cache_hash = None

    def predict(self, mats):
        liq = []; fillers = []; total_mass = 0.0; missing = []; imputed = []
        detail = []
        for m in mats:
            cat=m.get('orig_cat',''); name=m.get('name',''); mass=m.get('rounded_mass',0)
            if mass<=0: continue
            total_mass += mass
            info = self.dm.materials.get(cat,{}).get(name,{})
            if cat=='fillers':
                rho=self._pf(info.get('density',''),self.filler_density)
                shape=str(info.get('particle_shape','')).strip()
                oa=self._pf(info.get('oil_absorption',''),0)
                is_csr=any(kw in name.lower() or kw in str(info.get('type','')).lower() for kw in self._CSR_KW)
                fillers.append((mass,rho,shape,oa,name,is_csr)); continue
            visc=self._pf(info.get('viscosity',''),0)
            eew=info.get('eew',0) or 0; mw=info.get('mw',0) or 0
            if visc>0:
                liq.append((mass,visc,eew,mw,cat,name))
            else:
                est = self._estimate_missing_visc(name, cat, info)
                if est > 0:
                    liq.append((mass, est, eew, mw, cat, name))
                    imputed.append(f"{name}→{est:.0f}cP(est)")
                    detail.append(f"  ⚠ {name}: visc imputed → {est:.0f} cP")
                else:
                    missing.append(name)

        if not liq:
            feat = self._features_v2(mats, 0, 0, total_mass)
            ml_result = self._ensemble_predict(feat)
            if ml_result['prediction'] > 0:
                detail.append("[ML-only] No liquid viscosity data, using pure ML prediction")
                detail.append(f"  → {ml_result['prediction']:.0f} cP (n={ml_result['n_train']})")
                return self._build_result(ml_result['prediction'], 0, 0, 0, 1.0,
                                         detail, "ml_only", missing, imputed, 0, 1.0, ml_result)
            return self._empty(missing, imputed)

        tl=sum(m for m,*_ in liq)
        fracs=[(m/tl,v,eew,mw,c,n) for m,v,eew,mw,c,n in liq]

        dil_fracs = []; base_fracs = []
        for w, v, eew, mw, c, n in fracs:
            info = self.dm.materials.get(c, {}).get(n, {})
            fg = float(info.get('func_group_num', 0) or 0)
            typ = str(info.get('type', '')).lower()
            nm_l = n.lower()
            is_dil = (fg == 1) or any(kw in typ or kw in nm_l for kw in self._DILUENT_KW)
            if is_dil and v > 0 and v < 200:
                dil_fracs.append((w, v, n))
            else:
                base_fracs.append((w, v, eew, mw, c, n))

        if dil_fracs and base_fracs:
            tw_base = sum(w for w, *_ in base_fracs)
            tw_dil = sum(w for w, *_ in dil_fracs)
            if tw_base > 0:
                norm_base = [(w/tw_base, v, eew, mw, c, n) for w, v, eew, mw, c, n in base_fracs]
            else:
                norm_base = base_fracs
            ln_base = sum(w * math.log(v) for w, v, *_ in norm_base if v > 0)
            eta_base = math.exp(ln_base)
            k_dil = 4.5
            eta_l1 = eta_base * math.exp(-k_dil * tw_dil)
            dil_names = ", ".join(n for _, _, n in dil_fracs)
            detail.append(f"[L1] Diluent model: base={eta_base:.0f}cP × exp(-{k_dil}×{tw_dil:.3f}) → {eta_l1:.1f} cP")
            detail.append(f"  Diluents: {dil_names} ({tw_dil*100:.1f}%)")
        else:
            ln_e=sum(w*math.log(v) for w,v,*_ in fracs if v > 0)
            inter=0.0
            for i in range(len(fracs)):
                for j in range(i+1,len(fracs)):
                    wi,vi,_,mwi,ci,_=fracs[i]; wj,vj,_,mwj,cj,_=fracs[j]
                    if vi > 0 and vj > 0:
                        d=self._dij(vi,vj,mwi,mwj,ci,cj)
                        inter+=wi*wj*d
            ln_e+=inter
            eta_l1=math.exp(ln_e)
            detail.append(f"[L1] Grunberg-Nissan → {eta_l1:.1f} cP (d_ij={inter:+.3f})")

        eta_T=eta_l1
        if abs(self.temperature-25.0)>0.5:
            avg_eew=0; n_eew=0
            for w,_,eew,*_ in fracs:
                if eew>0: avg_eew+=w*eew; n_eew+=1
            if n_eew==0: avg_eew=190
            else: avg_eew/=sum(w for w,_,eew,*_ in fracs if eew>0)
            Ea=max(30000,min(100000,35000+80*avg_eew))
            tf=math.exp(Ea/self.R_GAS*(1/(self.temperature+273.15)-1/298.15))
            eta_T=eta_l1*tf
            detail.append(f"[L1.5] T={self.temperature}°C Ea={Ea/1000:.1f}kJ/mol → ×{tf:.3f} = {eta_T:.1f} cP")
        else:
            detail.append("[L1.5] T=25°C → skip")

        eta_kd=eta_T; phi=0.0; fm_total=sum(fm for fm,*_ in fillers)
        if fillers and total_mass>0:
            tvf=sum(fm/rho for fm,rho,*_ in fillers)
            vl=(total_mass-fm_total)/self.liquid_density
            phi=tvf/(tvf+vl)
            ie_sum=0.0
            for fm,rho,sh,oa,fn,csr in fillers:
                vi=fm/rho; wi=vi/tvf if tvf>0 else 1.0
                ei=1.5 if csr else self._SHAPE_ETA.get(sh,self.intrinsic_eta)
                ie_sum+=wi*ei
                tag="CSR" if csr else sh or "?"
                detail.append(f"  [{fn}] {tag} [η]={ei}")
            eff_ie=ie_sum if ie_sum>0 else self.intrinsic_eta

            avg_ssa = sum(self._pf(self.dm.materials.get('fillers',{}).get(fn,{}).get('ssa',''),0)
                         for _,_,_,_,fn,_ in fillers) / max(len(fillers),1)
            avg_d50 = sum(self._pf(self.dm.materials.get('fillers',{}).get(fn,{}).get('particle_size',''),0)
                         for _,_,_,_,fn,_ in fillers) / max(len(fillers),1)

            woa=sum(fm*oa for fm,_,_,oa,_,_ in fillers if oa>0)
            woa_m=sum(fm for fm,_,_,oa,_,_ in fillers if oa>0)
            if woa_m > 0:
                pm_oa = max(0.3, min(0.74, 1/(1+woa/woa_m*(fm_total/tvf)/100)))
            else:
                pm_oa = self.phi_max
            pm_adj = 0.0
            if avg_ssa > 0 and avg_d50 > 0:
                pm_adj = -0.02 * math.log(max(avg_ssa, 1)) + 0.01 * math.log(max(avg_d50, 0.1))
            pm = max(0.30, min(0.74, pm_oa + pm_adj))
            detail.append(f"  φ_max calc: OA→{pm_oa:.3f} SSA/D50adj→{pm_adj:+.3f} → {pm:.3f}")
            if phi<pm:
                kd=(1-phi/pm)**(-eff_ie*pm)
                eta_kd=eta_T*kd
                detail.append(f"[L2] K-D: φ={phi:.3f} φ_max={pm:.3f} [η]={eff_ie:.2f} → ×{kd:.2f} = {eta_kd:.1f} cP")
            else:
                eta_kd=float('inf')
                detail.append(f"[L2] JAMMED φ={phi:.3f}≥φ_max={pm:.3f}")
        else:
            detail.append("[L2] No fillers → skip")

        feat = self._features_v2(mats, eta_l1, phi, total_mass)
        ml_result = self._ensemble_predict(feat)
        ml_pred = ml_result['prediction']
        ml_n = ml_result['n_train']
        ml_std = ml_result.get('std', 0)

        physics = eta_kd if eta_kd != float('inf') else 0
        if ml_pred > 0 and ml_n >= 2:
            ml_cv = ml_result.get('cv_score', 0)
            if ml_n >= 15 and ml_cv > 0.6:
                mw_ = 0.70
            elif ml_n >= 8 and ml_cv > 0.4:
                mw_ = 0.55
            elif ml_n >= 5:
                mw_ = 0.40
            elif ml_n >= 3:
                mw_ = 0.30
            else:
                mw_ = 0.20

            if missing or imputed:
                mw_ = min(0.85, mw_ + 0.15)

            if physics > 0:
                eta_final = math.exp((1 - mw_) * math.log(physics) + mw_ * math.log(ml_pred))
            else:
                eta_final = ml_pred

            models_used = ", ".join(f"{k}:{v:.0f}" for k, v in ml_result.get('model_preds', {}).items())
            detail.append(f"[ML] Ensemble (n={ml_n} CV={ml_cv:.2f}): {ml_pred:.0f}±{ml_std:.0f}cP")
            detail.append(f"  Models: {models_used}")
            detail.append(f"  Blend: physics×{1-mw_:.0%} + ML×{mw_:.0%} → {eta_final:.0f} cP")
        else:
            eta_final = physics if physics > 0 else eta_kd
            detail.append(f"[ML] Inactive (n={ml_n}) → physics only")

        conf = self._calc_confidence(missing, imputed, ml_n, ml_result.get('cv_score', 0), ml_std, eta_final)

        ti=1.0
        if fillers and phi>0.01:
            tvf=sum(fm/rho for fm,rho,*_ in fillers)
            tk=sum((fm/rho)/tvf*self._SHAPE_TI_K.get(sh,8.0) for fm,rho,sh,_,_,_ in fillers) if tvf>0 else 8.0
            ti=1.0+tk*phi*phi
            detail.append(f"[TI] k={tk:.1f} TI={ti:.2f}")
        else: detail.append("[TI] ≈1.0")

        if eta_final==float('inf') or phi>=self.phi_max: st="solid"
        elif eta_final>100000: st="solid"
        elif eta_final>5000: st="paste"
        elif eta_final>0: st="liquid"
        else: st="unknown"
        detail.append(f"[State] → {st}")

        return self._build_result(eta_final, eta_l1, eta_T, eta_kd, 1.0,
                                 detail, conf, missing, imputed, phi, ti, ml_result)

    def _build_result(self, eta_final, eta_l1, eta_T, eta_kd, corr,
                     detail, conf, missing, imputed, phi, ti, ml_result):
        st = "unknown"
        if eta_final == float('inf'): st = "solid"
        elif eta_final > 100000: st = "solid"
        elif eta_final > 5000: st = "paste"
        elif eta_final > 0: st = "liquid"
        return {"eta_liquid": eta_l1, "eta_at_T": eta_T, "eta_filled": eta_kd,
                "eta_final": eta_final, "correction_factor": corr,
                "detail": "\n".join(detail) if isinstance(detail, list) else detail,
                "confidence": conf, "missing": missing, "imputed": imputed,
                "phi": phi, "thixotropic_index": ti, "rt_state": st,
                "ml_n": ml_result.get('n_train', 0),
                "ml_cv_score": ml_result.get('cv_score', 0),
                "ml_std": ml_result.get('std', 0),
                "ml_models": ml_result.get('model_preds', {})}

    def _empty(self, missing, imputed=None):
        return {"eta_liquid":0,"eta_at_T":0,"eta_filled":0,"eta_final":0,
                "correction_factor":1.0,"detail":"No viscosity data available","confidence":"no_data",
                "missing":missing,"imputed":imputed or [],"phi":0,"thixotropic_index":1.0,"rt_state":"unknown",
                "ml_n":0,"ml_cv_score":0,"ml_std":0,"ml_models":{}}

    def _estimate_missing_visc(self, name, cat, info):
        """Auto-impute missing viscosity."""
        type_str = str(info.get('type', '')).lower().strip()
        eew = info.get('eew', 0) or 0
        mw = info.get('mw', 0) or 0

        same_type_viscs = []
        all_cat_viscs = []
        for n, inf in self.dm.materials.get(cat, {}).items():
            v = self._pf(inf.get('viscosity', ''), 0)
            if v <= 0: continue
            all_cat_viscs.append(v)
            t = str(inf.get('type', '')).lower().strip()
            if t and type_str and t == type_str:
                same_type_viscs.append(v)
            elif eew > 0 and (inf.get('eew', 0) or 0) > 0:
                ie = inf.get('eew', 0) or 0
                if 0.7 * eew <= ie <= 1.3 * eew:
                    same_type_viscs.append(v)

        if same_type_viscs:
            same_type_viscs.sort()
            mid = len(same_type_viscs) // 2
            est = same_type_viscs[mid]
            return est

        if cat == 'resins' and eew > 0:
            eew_visc_pairs = []
            for n, inf in self.dm.materials.get('resins', {}).items():
                v = self._pf(inf.get('viscosity', ''), 0)
                ie = inf.get('eew', 0) or 0
                if v > 0 and ie > 0:
                    eew_visc_pairs.append((ie, v))
            if len(eew_visc_pairs) >= 2:
                est = self._eew_regression(eew_visc_pairs, eew)
                if est > 0:
                    return est

        name_lower = name.lower()
        for kw, default_v in self._TYPE_VISC_DEFAULTS.items():
            if kw in name_lower or kw in type_str:
                if default_v > 0:
                    return default_v
                break

        if all_cat_viscs:
            return math.exp(sum(math.log(v) for v in all_cat_viscs) / len(all_cat_viscs))

        return 0

    def _eew_regression(self, pairs, target_eew):
        """EEW-based viscosity regression."""
        n = len(pairs)
        if n < 2: return 0
        sx = sum(eew for eew, _ in pairs)
        sy = sum(math.log(v) for _, v in pairs)
        sxx = sum(eew * eew for eew, _ in pairs)
        sxy = sum(eew * math.log(v) for eew, v in pairs)
        denom = n * sxx - sx * sx
        if abs(denom) < 1e-10: return 0
        b = (n * sxy - sx * sy) / denom
        a = (sy - b * sx) / n
        est = math.exp(a + b * target_eew)
        return max(1, min(est, 1e6))

    def _features_v2(self, mats, eta_l1, phi, total_mass):
        """Build 28-dim ML feature vector."""
        cm = {}; eews = []; mws = []; n_comp = 0
        for m in mats:
            c = m.get('orig_cat', ''); mass = m.get('rounded_mass', 0)
            if mass <= 0: continue
            n_comp += 1
            cm[c] = cm.get(c, 0) + mass
            info = self.dm.materials.get(c, {}).get(m.get('name', ''), {})
            if (info.get('eew', 0) or 0) > 0: eews.append(info['eew'])
            if (info.get('mw', 0) or 0) > 0: mws.append(info['mw'])

        t = max(total_mass, 1)
        r_frac = cm.get('resins', 0) / t
        h_frac = cm.get('hardeners', 0) / t
        f_frac = cm.get('fillers', 0) / t
        a_frac = cm.get('additives', 0) / t
        c_frac = cm.get('catalysts', 0) / t

        custom_frac = sum(v / t for k, v in cm.items()
                         if k not in ('resins', 'hardeners', 'fillers', 'additives', 'catalysts'))

        avg_eew = sum(eews) / len(eews) if eews else 190.0
        max_eew = max(eews) if eews else 190.0
        min_eew = min(eews) if eews else 190.0
        avg_mw = sum(mws) / len(mws) if mws else 380.0

        filler_info = self._filler_features(mats, total_mass)

        ln_eta = math.log(max(eta_l1, 1)) if eta_l1 > 0 else 0

        rh_ratio = cm.get('resins', 0) / max(cm.get('hardeners', 0), 0.01)

        return [
            r_frac,
            h_frac,
            f_frac,
            a_frac,
            c_frac,
            custom_frac,
            phi,
            ln_eta,
            n_comp,
            self.temperature,
            avg_eew,
            max_eew,
            min_eew,
            avg_mw,
            rh_ratio,
            total_mass,
            r_frac * h_frac,
            r_frac * f_frac,
            phi ** 2,
            ln_eta * phi,
            filler_info.get('avg_d50', 0),
            filler_info.get('avg_ssa', 0),
            filler_info.get('n_fillers', 0),
            filler_info.get('csr_frac', 0),
            filler_info.get('avg_oa', 0),
            len(eews) / max(n_comp, 1),
            math.log(max(avg_eew, 1)),
            math.log(max(avg_mw, 1)),
        ]

    def _filler_features(self, mats, total_mass):
        """Filler feature extraction."""
        d50s = []; ssas = []; oas = []; n_f = 0; csr_mass = 0; filler_mass = 0
        for m in mats:
            if m.get('orig_cat') != 'fillers' or m.get('rounded_mass', 0) <= 0: continue
            n_f += 1
            mass = m['rounded_mass']
            filler_mass += mass
            info = self.dm.materials.get('fillers', {}).get(m.get('name', ''), {})
            d = self._pf(info.get('particle_size', ''), 0)
            if d > 0: d50s.append(d)
            s = self._pf(info.get('ssa', ''), 0)
            if s > 0: ssas.append(s)
            o = self._pf(info.get('oil_absorption', ''), 0)
            if o > 0: oas.append(o)
            if any(kw in m.get('name', '').lower() for kw in self._CSR_KW):
                csr_mass += mass
        return {
            'avg_d50': sum(d50s) / len(d50s) if d50s else 0,
            'avg_ssa': sum(ssas) / len(ssas) if ssas else 0,
            'avg_oa': sum(oas) / len(oas) if oas else 0,
            'n_fillers': n_f,
            'csr_frac': csr_mass / max(filler_mass, 0.01),
        }

    def _ensemble_predict(self, feat):
        """GPR+Ridge+kNN ensemble prediction."""
        train = self._build_training_set()
        n = len(train)
        if n < 2:
            return {'prediction': 0, 'n_train': n, 'std': 0, 'cv_score': 0, 'model_preds': {}}

        X = [t[0] for t in train]
        y = [t[1] for t in train]

        nf = len(feat)
        mins = [min(X[j][i] for j in range(n)) for i in range(nf)]
        maxs = [max(X[j][i] for j in range(n)) for i in range(nf)]
        rng = [maxs[i] - mins[i] if maxs[i] != mins[i] else 1.0 for i in range(nf)]
        Xn = [[(X[j][i] - mins[i]) / rng[i] for i in range(nf)] for j in range(n)]
        qn = [(feat[i] - mins[i]) / rng[i] for i in range(nf)]

        gpr_pred, gpr_std = self._gpr_predict(Xn, y, qn)

        ridge_pred = self._ridge_predict(Xn, y, qn)

        knn_pred = self._adaptive_knn(Xn, y, qn, n)

        cv_scores = self._loo_cv(Xn, y, n)

        preds = {}
        weights = {}
        total_w = 0

        if gpr_pred > 0:
            preds['GPR'] = math.exp(gpr_pred)
            w = max(cv_scores.get('gpr', 0.1), 0.05)
            weights['GPR'] = w; total_w += w

        if ridge_pred != 0:
            preds['Ridge'] = math.exp(ridge_pred)
            w = max(cv_scores.get('ridge', 0.1), 0.05)
            weights['Ridge'] = w; total_w += w

        if knn_pred != 0:
            preds['k-NN'] = math.exp(knn_pred)
            w = max(cv_scores.get('knn', 0.1), 0.05)
            weights['k-NN'] = w; total_w += w

        if not preds:
            return {'prediction': 0, 'n_train': n, 'std': 0, 'cv_score': 0, 'model_preds': {}}

        ln_ensemble = 0
        for model, pred in preds.items():
            ln_ensemble += (weights[model] / total_w) * math.log(max(pred, 1))
        ensemble_pred = math.exp(ln_ensemble)

        pred_values = list(preds.values())
        if len(pred_values) > 1:
            mean_ln = sum(math.log(max(v, 1)) for v in pred_values) / len(pred_values)
            std_ln = math.sqrt(sum((math.log(max(v, 1)) - mean_ln) ** 2 for v in pred_values) / len(pred_values))
            std_pred = ensemble_pred * std_ln
        else:
            std_pred = ensemble_pred * (math.exp(gpr_std) - 1) if gpr_std > 0 else 0

        overall_cv = sum(cv_scores.values()) / max(len(cv_scores), 1)

        return {
            'prediction': ensemble_pred,
            'n_train': n,
            'std': std_pred,
            'cv_score': overall_cv,
            'model_preds': preds,
        }

    def _gpr_predict(self, X, y, q):
        """GPR prediction (log-space)."""
        n = len(X); nf = len(q)
        if n < 2: return 0, 0

        l = max(0.3, math.sqrt(nf) * 0.5)
        sigma_f = 1.0
        sigma_n = 0.1

        K = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                d2 = sum((X[i][f] - X[j][f]) ** 2 for f in range(nf))
                K[i][j] = sigma_f * math.exp(-d2 / (2 * l * l))
            K[i][i] += sigma_n * sigma_n

        try:
            alpha = self._solve_linear(K, y)
        except Exception:
            return 0, 0

        k_star = [sigma_f * math.exp(-sum((q[f] - X[i][f]) ** 2 for f in range(nf)) / (2 * l * l))
                  for i in range(n)]

        mean = sum(k_star[i] * alpha[i] for i in range(n))

        k_qq = sigma_f + sigma_n * sigma_n
        try:
            v = self._solve_linear(K, k_star)
            var = k_qq - sum(k_star[i] * v[i] for i in range(n))
            std = math.sqrt(max(var, 0))
        except Exception:
            std = 0.5

        return mean, std

    def _ridge_predict(self, X, y, q):
        """Ridge regression."""
        n = len(X); nf = len(q)
        if n < 2: return 0

        def augment(x):
            base = [1.0] + list(x)
            for i in [0, 1, 2, 6, 7]:
                if i < len(x):
                    base.append(x[i] ** 2)
            return base

        Xa = [augment(X[i]) for i in range(n)]
        qa = augment(q)
        p = len(qa)

        lam = max(n * 0.1, 1.0)

        XtX = [[0.0] * p for _ in range(p)]
        Xty = [0.0] * p
        for i in range(n):
            for j in range(p):
                Xty[j] += Xa[i][j] * y[i]
                for k in range(p):
                    XtX[j][k] += Xa[i][j] * Xa[i][k]
        for j in range(p):
            XtX[j][j] += lam

        try:
            beta = self._solve_linear(XtX, Xty)
            return sum(qa[j] * beta[j] for j in range(p))
        except Exception:
            return 0

    def _adaptive_knn(self, X, y, q, n):
        """Adaptive k-NN."""
        nf = len(q)
        ds = []
        for i in range(n):
            d = math.sqrt(sum((q[f] - X[i][f]) ** 2 for f in range(nf)))
            ds.append((d, y[i]))
        ds.sort(key=lambda x: x[0])

        k = max(3, min(int(math.sqrt(n) + 0.5), min(15, n)))
        nb = ds[:k]

        sigma_d = max(nb[-1][0] * 0.5, 0.01)
        tw = 0; ws = 0
        for d, ly in nb:
            w = math.exp(-d * d / (2 * sigma_d * sigma_d))
            ws += w * ly; tw += w
        return ws / tw if tw > 0 else 0

    def _loo_cv(self, X, y, n):
        """LOO cross-validation scores."""
        if n < 4:
            return {'gpr': 0.3, 'ridge': 0.3, 'knn': 0.3}

        indices = list(range(n)) if n <= 30 else list(range(0, n, max(1, n // 20)))

        errs = {'gpr': [], 'ridge': [], 'knn': []}
        y_vals = []

        for i in indices:
            Xi = X[:i] + X[i+1:]
            yi = y[:i] + y[i+1:]
            y_vals.append(y[i])

            try:
                p, _ = self._gpr_predict(Xi, yi, X[i])
                errs['gpr'].append((y[i] - p) ** 2)
            except Exception:
                errs['gpr'].append(10.0)

            try:
                p = self._ridge_predict(Xi, yi, X[i])
                errs['ridge'].append((y[i] - p) ** 2)
            except Exception:
                errs['ridge'].append(10.0)

            try:
                p = self._adaptive_knn(Xi, yi, X[i], len(Xi))
                errs['knn'].append((y[i] - p) ** 2)
            except Exception:
                errs['knn'].append(10.0)

        if not y_vals:
            return {'gpr': 0.3, 'ridge': 0.3, 'knn': 0.3}
        y_mean = sum(y_vals) / len(y_vals)
        ss_tot = sum((yv - y_mean) ** 2 for yv in y_vals)
        if ss_tot < 1e-10:
            return {'gpr': 0.5, 'ridge': 0.5, 'knn': 0.5}

        scores = {}
        for model, err_list in errs.items():
            ss_res = sum(err_list) / len(err_list) * len(y_vals) if err_list else ss_tot
            r2 = max(0, 1 - ss_res / ss_tot)
            scores[model] = r2
        return scores

    def _build_training_set(self):
        """Build training data from recipe database. Uses caching."""
        try:
            rows = self.dm._read_recipe_rows()
        except Exception:
            return []

        train = []
        for row in rows:
            y = self._meas_visc(row)
            if y <= 0: continue
            rm = self._recipe_mats(row)
            if not rm: continue
            tm = sum(m['rounded_mass'] for m in rm)
            eta_h = self._calc_l1(rm)
            phi_h = self._calc_phi(rm)
            if eta_h <= 0: eta_h = 1
            feat = self._features_v2(rm, eta_h, phi_h, tm)
            train.append((feat, math.log(y)))
        return train

    def _calc_confidence(self, missing, imputed, ml_n, cv_score, ml_std, eta_final):
        if eta_final <= 0 or eta_final == float('inf'):
            return "no_data"
        if ml_n >= 10 and cv_score > 0.6 and not missing:
            return "high"
        if ml_n >= 5 and cv_score > 0.3 and len(missing) <= 1:
            return "high" if not missing else "medium"
        if ml_n >= 3 or (not missing and not imputed):
            return "medium"
        if imputed and not missing:
            return "medium"
        if missing:
            return "low"
        return "medium"

    @staticmethod
    def _solve_linear(A, b):
        """Solve Ax = b via Gaussian elimination with partial pivoting."""
        n = len(b)
        M = [list(A[i]) + [b[i]] for i in range(n)]

        for col in range(n):
            max_row = col
            max_val = abs(M[col][col])
            for row in range(col + 1, n):
                if abs(M[row][col]) > max_val:
                    max_val = abs(M[row][col])
                    max_row = row
            M[col], M[max_row] = M[max_row], M[col]

            if abs(M[col][col]) < 1e-12:
                continue

            for row in range(col + 1, n):
                factor = M[row][col] / M[col][col]
                for j in range(col, n + 1):
                    M[row][j] -= factor * M[col][j]

        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            if abs(M[i][i]) < 1e-12:
                x[i] = 0
                continue
            x[i] = M[i][n]
            for j in range(i + 1, n):
                x[i] -= M[i][j] * x[j]
            x[i] /= M[i][i]
        return x

    @staticmethod
    def _dij(vi,vj,mwi,mwj,ci,cj):
        if vi<=0 or vj<=0: return 0.0
        vr=abs(math.log(vi/vj))
        cross=(ci=='resins' and cj=='hardeners') or (cj=='resins' and ci=='hardeners')
        if cross: return -0.4*vr
        if mwi>0 and mwj>0: return -0.15*abs(math.log(mwi/mwj))
        return -0.05*vr

    def _meas_visc(self,row):
        for k in ['粘度 (cP, 25°C)','Viscosity_cP25','viscosity']:
            v=str(row.get(k,'') or '').strip()
            if v:
                try: r=float(v.replace(',','').split('-')[0]); return r if r>0 else 0
                except Exception: pass
        return 0

    def _recipe_mats(self,row):
        mats=[]
        for cat,n in get_all_slot_counts().items():
            cn=get_all_cat_cn().get(cat,cat)
            for i in range(1,n+1):
                nm=row.get(f"{cn}{i}_Name","")
                ms=row.get(f"{cn}{i}_Mass_g","0")
                if nm:
                    try: mass=float(ms)
                    except Exception: mass=0
                    if mass>0: mats.append({"name":nm,"orig_cat":cat,"rounded_mass":mass})
        return mats

    def _physics_only(self,mats):
        eta=self._calc_l1(mats)
        if eta<=0: return 0
        phi=self._calc_phi(mats)
        if phi>0:
            finfo=[(m,self.dm.materials.get(m['orig_cat'],{}).get(m['name'],{})) for m in mats if m['orig_cat']=='fillers']
            ie=self.intrinsic_eta
            if finfo:
                tvf=sum(m['rounded_mass']/self._pf(info.get('density',''),self.filler_density) for m,info in finfo)
                if tvf>0:
                    ie=sum((m['rounded_mass']/self._pf(info.get('density',''),self.filler_density))/tvf*
                           (1.5 if any(kw in m['name'].lower() for kw in self._CSR_KW) else
                            self._SHAPE_ETA.get(str(info.get('particle_shape','')).strip(),self.intrinsic_eta))
                           for m,info in finfo)
            if phi<self.phi_max: return eta*(1-phi/self.phi_max)**(-ie*self.phi_max)
            return float('inf')
        return eta

    def _calc_l1(self,mats):
        lq=[]
        for m in mats:
            if m['orig_cat']=='fillers': continue
            info=self.dm.materials.get(m['orig_cat'],{}).get(m['name'],{})
            v=self._pf(info.get('viscosity',''),0)
            if v>0: lq.append((m['rounded_mass'],v))
        if not lq: return 0
        tl=sum(m for m,_ in lq)
        return math.exp(sum((m/tl)*math.log(v) for m,v in lq))

    def _calc_phi(self,mats):
        fm=0;total=0
        for m in mats:
            mass=m['rounded_mass']; total+=mass
            if m['orig_cat']=='fillers':
                info=self.dm.materials.get('fillers',{}).get(m['name'],{})
                fm+=mass/self._pf(info.get('density',''),self.filler_density)
        if fm<=0 or total<=0: return 0
        vl=(total-sum(m['rounded_mass'] for m in mats if m['orig_cat']=='fillers'))/self.liquid_density
        return fm/(fm+vl)

    @staticmethod
    def _pf(val,default=0.0):
        try: return float(str(val).replace(',','').split('-')[0].split('~')[0]) if str(val).strip() else default
        except Exception: return default

class PropertyMLPredictor:
    """ML ensemble predictor for any recipe property (Tg, gel time, CTE, etc).
    Reuses ViscosityPredictor's 28-dim feature engineering + GPR/Ridge/kNN ensemble.
    Training data: recipes in DB that have the target property filled in."""

    _PROP_KEYS = {
        'tg': ['Prop_Tg-DSC (ΔCp midpoint)', 'Prop_Tg-DSC', 'Prop_Tg_DSC'],
        'gel_time': ['Prop_凝膠時間 Gel Time', 'Prop_Gel_Time', 'Prop_gel_time'],
        'cte1': ['Prop_CTE α1 (<Tg)', 'Prop_CTE_a1', 'Prop_CTE1'],
        'dh': ['Prop_DSC 反應熱 ΔH', 'Prop_DSC_dH', 'Prop_dH'],
        'shore_d': ['Prop_硬度 Shore D', 'Prop_Shore_D'],
        'tensile': ['Prop_拉伸強度', 'Prop_Tensile_Strength'],
        'flexural': ['Prop_彎曲強度', 'Prop_Flexural_Strength'],
        'shear_al': ['Prop_搭接剪切強度 Al-Al', 'Prop_Lap_Shear_Al'],
        'dk_1mhz': ['Prop_介電常數 Dk @1MHz', 'Prop_Dk_1MHz'],
        'water_abs': ['Prop_吸水率 (24h/25°C)', 'Prop_Water_Abs_24h'],
        'thermal_k': ['Prop_導熱率', 'Prop_Thermal_Conductivity'],
        'elec_rho': ['Prop_體積電阻率', 'Prop_Volume_Resistivity'],
    }

    def __init__(self, dm, prop_key='tg'):
        self.dm = dm
        self.prop_key = prop_key
        self._vp = ViscosityPredictor(dm)

    def _find_prop_value(self, row):
        keys = self._PROP_KEYS.get(self.prop_key, [self.prop_key])
        for k in keys:
            v = row.get(k, '')
            if v:
                try:
                    val = float(str(v).replace(',','').split('~')[0].split('-')[0].strip())
                    if val != 0: return val
                except Exception: pass
        return 0

    def _build_training(self):
        try: rows = self.dm._read_recipe_rows()
        except Exception: return []
        train = []
        for row in rows:
            y = self._find_prop_value(row)
            if y == 0: continue
            rm = self._vp._recipe_mats(row)
            if not rm: continue
            tm = sum(m.get('rounded_mass', 0) for m in rm)
            eta_h = self._vp._calc_l1(rm)
            phi_h = self._vp._calc_phi(rm)
            if eta_h <= 0: eta_h = 1
            feat = self._vp._features_v2(rm, eta_h, phi_h, tm)
            train.append((feat, y))
        return train

    def predict(self, mats, analytical_value=0):
        """Predict property using ML ensemble, blended with analytical estimate.
        Returns dict: prediction, confidence, n_train, analytical, ml_pred, blend_weight."""
        train = self._build_training()
        n = len(train)
        if n < 2:
            return {'prediction': analytical_value, 'confidence': 'analytical',
                    'n_train': n, 'analytical': analytical_value, 'ml_pred': 0, 'blend_weight': 0}

        X = [t[0] for t in train]; y = [t[1] for t in train]
        tm = sum(m.get('rounded_mass', 0) for m in mats)
        eta_h = self._vp._calc_l1(mats)
        phi_h = self._vp._calc_phi(mats)
        if eta_h <= 0: eta_h = 1
        feat = self._vp._features_v2(mats, eta_h, phi_h, tm)

        preds = {}
        try:
            p, _ = self._vp._gpr_predict(X, y, feat)
            preds['gpr'] = p
        except Exception: pass
        try:
            preds['ridge'] = self._vp._ridge_predict(X, y, feat)
        except Exception: pass
        try:
            preds['knn'] = self._vp._adaptive_knn(X, y, feat, n)
        except Exception: pass

        if not preds:
            return {'prediction': analytical_value, 'confidence': 'analytical',
                    'n_train': n, 'analytical': analytical_value, 'ml_pred': 0, 'blend_weight': 0}

        scores = self._vp._loo_cv(X, y, n) if n >= 4 else {'gpr': 0.3, 'ridge': 0.3, 'knn': 0.3}
        total_w = sum(scores.get(m, 0) for m in preds)
        if total_w > 0:
            ml_pred = sum(preds[m] * scores.get(m, 0) for m in preds) / total_w
        else:
            ml_pred = sum(preds.values()) / len(preds)

        cv_avg = sum(scores.values()) / max(len(scores), 1)
        if n >= 10 and cv_avg > 0.5: mw = 0.70
        elif n >= 5 and cv_avg > 0.3: mw = 0.50
        elif n >= 3: mw = 0.30
        else: mw = 0.15

        if analytical_value and analytical_value != 0:
            blended = (1 - mw) * analytical_value + mw * ml_pred
        else:
            blended = ml_pred; mw = 1.0

        conf = 'high' if n >= 8 and cv_avg > 0.5 else 'medium' if n >= 4 else 'low'
        return {
            'prediction': blended, 'confidence': conf, 'n_train': n,
            'analytical': analytical_value, 'ml_pred': ml_pred,
            'blend_weight': mw, 'cv_score': cv_avg,
            'model_preds': preds, 'model_scores': scores,
        }

def dibenedetto_tg(tg0, tg_inf, lam, alpha):
    """DiBenedetto equation: predict Tg at conversion α.
    tg0: Tg of uncured resin (°C), tg_inf: Tg of fully cured (°C),
    lam: shape parameter (typically 0.4–0.6), alpha: conversion 0–1."""
    if alpha < 0 or alpha > 1: return tg0
    return tg0 + (tg_inf - tg0) * lam * alpha / (1 - (1 - lam) * alpha)

def arrhenius_gel_time(ea_kj, ln_a, temp_c, total_mass_g=100, cp=1.5, rho=1.15, h_rxn=350):
    """Simplified Arrhenius gel time & adiabatic ΔT estimator.
    ea_kj: activation energy (kJ/mol), ln_a: ln(pre-exp factor s⁻¹),
    temp_c: cure temperature (°C), total_mass_g: batch mass (g),
    cp: specific heat (J/g·K), h_rxn: reaction enthalpy (J/g).
    Returns dict with gel_time_min, rate_constant, delta_T_adiabatic."""
    R = 8.314
    T = temp_c + 273.15
    k = math.exp(ln_a - ea_kj * 1000 / (R * T))
    gel_time_s = 1.0 / k if k > 0 else float('inf')
    dt_ad = h_rxn / cp if cp > 0 else 0
    return {
        'rate_constant': k,
        'gel_time_min': gel_time_s / 60.0,
        'delta_T_adiabatic': dt_ad,
        'peak_temp': temp_c + dt_ad,
    }

_COMMON_EA = {
    'DICY': (110, 25.0), 'amine': (55, 14.0), 'anhydride': (70, 17.0),
    'imidazole': (85, 20.0), 'mercaptan': (45, 12.0), 'latent': (100, 23.0),
    'phenolic': (90, 21.0),
}

_FILLER_DEFAULTS = {
    'silica': {'cte': 0.5, 'k': 1.4, 'rho_e': 1e16},
    'fused silica': {'cte': 0.5, 'k': 1.4, 'rho_e': 1e16},
    'alumina': {'cte': 7.0, 'k': 30.0, 'rho_e': 1e14},
    'aln': {'cte': 4.5, 'k': 170.0, 'rho_e': 1e13},
    'bn': {'cte': 1.0, 'k': 60.0, 'rho_e': 1e15},
    'silver': {'cte': 19.0, 'k': 429.0, 'rho_e': 1.6e-6},
    'copper': {'cte': 17.0, 'k': 400.0, 'rho_e': 1.7e-6},
    'carbon black': {'cte': 5.0, 'k': 6.0, 'rho_e': 0.1},
    'graphite': {'cte': 1.0, 'k': 100.0, 'rho_e': 1e-3},
    'diamond': {'cte': 1.0, 'k': 1000.0, 'rho_e': 1e16},
    'csr': {'cte': 150.0, 'k': 0.15, 'rho_e': 1e16},
}

def predict_cte(cte_resin, cte_filler, phi, k_resin=3.5, k_filler=30.0):
    """Turner model + Schapery bounds for composite CTE.
    k = bulk modulus (GPa). Returns dict with cte_turner, cte_rom, cte_schapery_lower."""
    if phi <= 0: return {'turner': cte_resin, 'rom': cte_resin, 'schapery_lo': cte_resin}
    phi = min(phi, 0.95)
    vr = 1 - phi
    cte_rom = vr * cte_resin + phi * cte_filler
    denom = vr * k_resin + phi * k_filler
    cte_turner = (vr * cte_resin * k_resin + phi * cte_filler * k_filler) / denom if denom > 0 else cte_rom
    k_upper = vr * k_resin + phi * k_filler
    k_lower = 1.0 / (vr / k_resin + phi / k_filler) if (k_resin > 0 and k_filler > 0) else k_upper
    cte_schapery = cte_rom - (cte_resin - cte_filler) * (1/k_lower - 1/k_upper) / (1/k_filler - 1/k_resin) if abs(1/k_filler - 1/k_resin) > 1e-12 else cte_rom
    return {'turner': cte_turner, 'rom': cte_rom, 'schapery_lo': cte_schapery}

def predict_thermal_k(k_resin, k_filler, phi):
    """Maxwell + Bruggeman + Lewis-Nielsen models for thermal conductivity.
    Returns dict with maxwell, bruggeman, lewis_nielsen values (W/m·K)."""
    if phi <= 0: return {'maxwell': k_resin, 'bruggeman': k_resin, 'lewis_nielsen': k_resin}
    phi = min(phi, 0.95)
    L = (k_filler - k_resin) / (k_filler + 2 * k_resin) if (k_filler + 2 * k_resin) > 0 else 0
    k_maxwell = k_resin * (1 + 2 * L * phi) / (1 - L * phi) if (1 - L * phi) > 0 else k_resin
    k_brug = k_resin
    for _ in range(50):
        if k_brug <= 0: break
        f_val = (1 - phi) * (k_resin - k_brug) / (k_resin + 2 * k_brug) + phi * (k_filler - k_brug) / (k_filler + 2 * k_brug)
        df = -(1 - phi) * (k_resin + 2 * k_brug + 2 * (k_resin - k_brug)) / (k_resin + 2 * k_brug)**2 \
             - phi * (k_filler + 2 * k_brug + 2 * (k_filler - k_brug)) / (k_filler + 2 * k_brug)**2
        if abs(df) < 1e-20: break
        k_brug -= f_val / df
        k_brug = max(k_brug, 0.001)
    phi_max = 0.637
    A = 1.5
    psi = 1 + (1 - phi_max) / phi_max**2 * phi
    k_ln = k_resin * (1 + A * L * phi) / (1 - L * psi * phi) if (1 - L * psi * phi) > 0 else k_resin
    return {'maxwell': max(k_maxwell, 0), 'bruggeman': max(k_brug, 0), 'lewis_nielsen': max(k_ln, 0)}

def predict_elec(rho_resin, rho_filler, phi, phi_c=0.15, t_exp=2.0, s_exp=0.87):
    """Percolation + GEM model for electrical resistivity.
    phi_c: percolation threshold, t_exp/s_exp: critical exponents.
    Returns dict with log_rho_eff (Ω·cm), is_conductive flag."""
    if phi <= 0: return {'log_rho': math.log10(max(rho_resin, 1e-10)), 'rho': rho_resin, 'conductive': False}
    phi = min(phi, 0.95)
    log_rr = math.log10(max(rho_resin, 1e-10))
    log_rf = math.log10(max(rho_filler, 1e-10))
    if rho_filler > 1e6:
        log_rho = (1 - phi) * log_rr + phi * log_rf
        return {'log_rho': log_rho, 'rho': 10**log_rho, 'conductive': False}
    if phi < phi_c:
        log_rho = log_rr - (log_rr - log_rf) * 0.05 * (phi / phi_c)**2
        return {'log_rho': log_rho, 'rho': 10**log_rho, 'conductive': False}
    else:
        sigma_f = 1.0 / max(rho_filler, 1e-20)
        sigma_eff = sigma_f * ((phi - phi_c) / (1 - phi_c))**t_exp
        rho_eff = 1.0 / max(sigma_eff, 1e-20)
        return {'log_rho': math.log10(max(rho_eff, 1e-10)), 'rho': rho_eff, 'conductive': True}

class ExportPreviewDialog:
    """Shows a preview window where the user can reorder rows, toggle columns,
    set a batch scaling %, and then copy everything to clipboard."""

    OPT_COLS = [
        ("category",  "col_category",  False),
        ("eq_val",    "col_eq_val",    True),
        ("type",      "col_type",      False),
        ("formula",   "col_formula",   True),
    ]

    def __init__(self, parent, mats, base_mass, total_mass, total_cl, app, raw_mats=None, dm=None):
        """mats: list of dicts with keys name,category,calc_mass,phr,pct,cl_ppm,eq_val,type,formula
           raw_mats: original mats list from calculate() for viscosity prediction
           dm: DataManager instance"""
        self.mats = list(mats)
        self.app = app
        self.base_mass = base_mass
        self.total_mass = total_mass
        self.dm = dm
        self.raw_mats = raw_mats or []

        self.top = ctk.CTkToplevel(parent)
        self.top.title(T("export_title"))
        self.top.geometry("1000x640")
        self.top.grab_set()

        hdr = ctk.CTkFrame(self.top, fg_color="transparent")
        hdr.pack(fill='x', padx=12, pady=(10, 4))

        ctk.CTkLabel(hdr, text=T("batch_scale"), font=app.font_bold).pack(side='left')
        self.scale_var = ctk.CTkEntry(hdr, width=60, corner_radius=6, border_width=1, border_color=_C.BORDER); self.scale_var.insert(0, "100")
        self.scale_var.pack(side='left', padx=5)
        ctk.CTkLabel(hdr, text="%", font=app.font_std).pack(side='left')
        self.scale_var.bind('<KeyRelease>', lambda e: self._refresh())

        ctk.CTkLabel(hdr, text="   " + T("export_cols"), font=app.font_bold).pack(side='left', padx=(20,0))
        self.col_vars = {}
        for key, tkey, default in self.OPT_COLS:
            var = tk.BooleanVar(value=default)
            cb = ctk.CTkCheckBox(hdr, text=T(tkey), variable=var, font=app.font_std,
                                 command=self._refresh, checkbox_width=18, checkbox_height=18)
            cb.pack(side='left', padx=4)
            self.col_vars[key] = var

        ctk.CTkLabel(self.top, text=T("export_drag_hint"), font=app.font_std, text_color="gray"
                     ).pack(anchor='w', padx=14)

        mid = ctk.CTkFrame(self.top, fg_color="transparent")
        mid.pack(fill='both', expand=True, padx=12, pady=4)

        tf = RoundedTreeFrame(mid)
        tf.pack(side='left', fill='both', expand=True)
        self.tree = ttk.Treeview(tf.inner, show='headings', height=16)
        vsb = ttk.Scrollbar(tf.inner, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self._drag_item = None
        self.tree.bind("<ButtonPress-1>", self._drag_start)
        self.tree.bind("<B1-Motion>", self._drag_move)
        self.tree.bind("<ButtonRelease-1>", self._drag_end)
        self.tree.tag_configure('total', font=(_FONT_FAMILY, 10, "bold"), background=_C.BG_LIGHT)

        vp = ctk.CTkFrame(mid, width=280, corner_radius=8)
        vp.pack(side='right', fill='y', padx=(8, 0))
        vp.pack_propagate(False)

        ctk.CTkLabel(vp, text=T("visc_predict"), font=app.font_bold).pack(anchor='w', padx=10, pady=(8, 4))

        self.lbl_visc_result = ctk.CTkLabel(vp, text="—", font=ctk.CTkFont(family=_FONT_FAMILY, size=22, weight="bold"),
                                             text_color=app.current_accent)
        self.lbl_visc_result.pack(anchor='w', padx=10)
        self.lbl_visc_conf = ctk.CTkLabel(vp, text="", font=app.font_std, text_color="gray")
        self.lbl_visc_conf.pack(anchor='w', padx=10, pady=(0, 4))
        self.lbl_visc_missing = ctk.CTkLabel(vp, text="", font=ctk.CTkFont(family=_FONT_FAMILY, size=10),
                                              text_color=_C.RED, wraplength=250, justify="left")
        self.lbl_visc_missing.pack(anchor='w', padx=10)

        sep = ctk.CTkFrame(vp, height=1, fg_color="gray70")
        sep.pack(fill='x', padx=10, pady=6)
        self.lbl_visc_ti = ctk.CTkLabel(vp, text=T("visc_ti") + " —", font=app.font_std)
        self.lbl_visc_ti.pack(anchor='w', padx=10)
        self.lbl_visc_state = ctk.CTkLabel(vp, text=T("visc_state") + " —", font=app.font_std)
        self.lbl_visc_state.pack(anchor='w', padx=10, pady=(0, 4))

        ctk.CTkLabel(vp, text=T("visc_settings"), font=app.font_bold).pack(anchor='w', padx=10, pady=(10, 2))

        rf_t = ctk.CTkFrame(vp, fg_color="transparent")
        rf_t.pack(fill='x', padx=10, pady=1)
        ctk.CTkLabel(rf_t, text=T("visc_temp"), font=ctk.CTkFont(family=_FONT_FAMILY, size=11), anchor='w').pack(side='left')
        self.temp_entry = ctk.CTkEntry(rf_t, width=50, corner_radius=6, border_width=1, border_color=_C.BORDER); self.temp_entry.insert(0, "25")
        self.temp_entry.pack(side='right')
        self.temp_entry.bind('<KeyRelease>', lambda e: self._run_visc())

        params = [("phi_max", T("visc_phi_max"), "0.64"),
                  ("intr_eta", T("visc_intrinsic"), "2.5"),
                  ("filler_rho", T("visc_filler_rho"), "2.2"),
                  ("liquid_rho", T("visc_liquid_rho"), "1.15")]
        self.visc_params = {}
        for key, label, default in params:
            rf = ctk.CTkFrame(vp, fg_color="transparent")
            rf.pack(fill='x', padx=10, pady=1)
            ctk.CTkLabel(rf, text=label, font=ctk.CTkFont(family=_FONT_FAMILY, size=11), anchor='w').pack(side='left')
            ent = ctk.CTkEntry(rf, width=50, corner_radius=6, border_width=1, border_color=_C.BORDER); ent.insert(0, default)
            ent.pack(side='right')
            ent.bind('<KeyRelease>', lambda e: self._run_visc())
            self.visc_params[key] = ent

        self.lbl_ml_status = ctk.CTkLabel(vp, text=T("visc_ml_status") + " ...", 
                                           font=ctk.CTkFont(family=_FONT_FAMILY, size=10),
                                           text_color="gray")
        self.lbl_ml_status.pack(anchor='w', padx=10, pady=(4, 0))

        ctk.CTkButton(vp, text=T("visc_detail"), font=app.font_std, fg_color=_C.BTN_LIGHT, text_color=_C.TEXT_SEC, corner_radius=8,
                       command=self._show_visc_detail, height=28).pack(fill='x', padx=10, pady=(8, 4))

        self._visc_detail_text = ""
        self._l3_cache = None
        self._think_dots = 0
        self._think_job = None

        bf = ctk.CTkFrame(self.top, fg_color="transparent")
        bf.pack(fill='x', padx=12, pady=10)
        ctk.CTkButton(bf, text=T("export_copy"), fg_color=app.current_accent, corner_radius=8,
                       font=app.font_bold, command=self._do_copy).pack(side='right')

        self._refresh()

    def _col_defs(self):
        """Return list of (key, header, width)."""
        cols = [("name", T("col_mat_name"), 160), ("calc_mass", T("col_mass_g_result"), 85),
                ("scaled", T("col_scaled"), 85), ("phr", T("col_phr_result"), 70),
                ("pct", T("col_pct_result"), 70), ("cl", T("col_cl_result"), 75)]
        for key, tkey, _ in self.OPT_COLS:
            if self.col_vars.get(key, tk.BooleanVar(value=False)).get():
                w = 200 if key == "formula" else 90
                cols.append((key, T(tkey), w))
        return cols

    def _refresh(self, _=None):
        try: scale = max(0, float(self.scale_var.get() or 100)) / 100.0
        except Exception: scale = 1.0

        order = [self.tree.item(iid, 'values')[0] for iid in self.tree.get_children()
                 if 'total' not in self.tree.item(iid, 'tags')]
        if order:
            idx_map = {name: i for i, name in enumerate(order)}
            self.mats.sort(key=lambda m: idx_map.get(m['name'], 999))

        cols = self._col_defs()
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = [c[0] for c in cols]
        for cid, hdr, w in cols:
            self.tree.heading(cid, text=hdr)
            self.tree.column(cid, width=w, anchor='center' if cid != 'formula' else 'w')

        for m in self.mats:
            vals = [m['name'], f"{m['calc_mass']:.2f}", f"{m['calc_mass']*scale:.2f}",
                    f"{m['phr']:.2f}", f"{m['pct']:.2f}", f"{m['cl_ppm']:.0f}"]
            for key, _, _ in self.OPT_COLS:
                if self.col_vars.get(key, tk.BooleanVar(value=False)).get():
                    vals.append(str(m.get(key, '')))
            self.tree.insert("", "end", values=vals)

        tot_calc = sum(m['calc_mass'] for m in self.mats)
        tot_scaled = tot_calc * scale
        tot_cl = (sum(m['calc_mass']*(m['cl_ppm']/1e6) for m in self.mats)/tot_calc*1e6) if tot_calc>0 else 0
        tot_vals = [T("total"), f"{tot_calc:.2f}", f"{tot_scaled:.2f}", "—", "100.00", f"{tot_cl:.0f}"]
        for key, _, _ in self.OPT_COLS:
            if self.col_vars.get(key, tk.BooleanVar(value=False)).get():
                tot_vals.append("")
        self.tree.insert("", "end", values=tot_vals, tags=('total',))
        self._start_visc_thinking()

    def _start_visc_thinking(self):
        """Show a 'thinking' pulse animation, then compute prediction."""
        if self._think_job:
            try: self.top.after_cancel(self._think_job)
            except Exception: pass
        self._think_dots = 0
        self.lbl_visc_result.configure(text=T("visc_thinking"), text_color="gray")
        self.lbl_visc_conf.configure(text="")
        self.lbl_visc_missing.configure(text="")
        self.lbl_visc_ti.configure(text="")
        self.lbl_visc_state.configure(text="")
        self._animate_thinking()

    def _animate_thinking(self):
        """Pulse dots: 分析中. → 分析中.. → 分析中..."""
        self._think_dots = (self._think_dots % 3) + 1
        dots = "·" * self._think_dots + "  " * (3 - self._think_dots)
        self.lbl_visc_result.configure(text=f"{T('visc_thinking')} {dots}")
        if self._think_dots < 3:
            self._think_job = self.top.after(280, self._animate_thinking)
        else:
            self._think_job = self.top.after(200, self._run_visc_actual)

    def _run_visc(self, _=None):
        """Triggered by param changes — restart thinking animation."""
        self._l3_cache = None
        self._start_visc_thinking()

    def _run_visc_actual(self):
        """Execute the actual prediction (called after thinking animation)."""
        self._think_job = None
        if not self.dm or not self.raw_mats:
            self.lbl_visc_result.configure(text="—", text_color=self.app.current_accent)
            self.lbl_visc_conf.configure(text=T("visc_conf_none"))
            self.lbl_visc_missing.configure(text="")
            self.lbl_visc_ti.configure(text=T("visc_ti") + " —")
            self.lbl_visc_state.configure(text=T("visc_state") + " —")
            self.lbl_ml_status.configure(text=T("visc_ml_status") + " —")
            self._visc_detail_text = ""
            return
        try:
            phi_max = float(self.visc_params['phi_max'].get() or 0.64)
            intr_eta = float(self.visc_params['intr_eta'].get() or 2.5)
            filler_rho = float(self.visc_params['filler_rho'].get() or 2.2)
            liquid_rho = float(self.visc_params['liquid_rho'].get() or 1.15)
            temp = float(self.temp_entry.get() or 25)
        except Exception:
            phi_max, intr_eta, filler_rho, liquid_rho, temp = 0.64, 2.5, 2.2, 1.15, 25.0

        vp = ViscosityPredictor(self.dm, phi_max=phi_max, intrinsic_eta=intr_eta,
                                 filler_density=filler_rho, liquid_density=liquid_rho,
                                 temperature=temp)
        result = vp.predict(self.raw_mats)

        eta = result.get('eta_final', 0)
        conf = result.get('confidence', 'no_data')
        missing = result.get('missing', [])
        imputed = result.get('imputed', [])
        ti = result.get('thixotropic_index', 1.0)
        rt_state = result.get('rt_state', 'unknown')
        ml_n = result.get('ml_n', 0)
        ml_cv = result.get('ml_cv_score', 0)
        ml_models = result.get('ml_models', {})
        self._visc_detail_text = result.get('detail', '')

        if eta and eta != float('inf') and eta > 0:
            self.lbl_visc_result.configure(text=f"{eta:,.0f} {T('visc_unit')}",
                                            text_color=self.app.current_accent)
        else:
            self.lbl_visc_result.configure(text="—", text_color=self.app.current_accent)

        conf_map = {"high": T("visc_conf_high"), "medium": T("visc_conf_medium"),
                    "low": T("visc_conf_low"), "no_data": T("visc_conf_none"),
                    "ml_only": "● ML-only prediction"}
        color_map = {"high": _C.GREEN, "medium": _C.ORANGE, "low": _C.RED,
                     "no_data": _C.TEXT_TER, "ml_only": _C.INDIGO}
        self.lbl_visc_conf.configure(text=conf_map.get(conf, ""), text_color=color_map.get(conf, _C.TEXT_TER))

        info_parts = []
        if missing:
            info_parts.append(T("visc_missing") + " " + ", ".join(missing[:5]))
        if imputed:
            info_parts.append("⚠ Auto-estimated: " + ", ".join(imputed[:3]))
        self.lbl_visc_missing.configure(text="\n".join(info_parts) if info_parts else "")

        self.lbl_visc_ti.configure(text=f"{T('visc_ti')} {ti:.2f}")
        state_disp = {"liquid": T("state_liquid"), "paste": T("state_paste"),
                      "solid": T("state_solid"), "unknown": T("state_unknown")}
        state_color = {"liquid": _C.BLUE, "paste": _C.ORANGE, "solid": _C.TEXT_TER, "unknown": _C.TEXT_TER}
        self.lbl_visc_state.configure(text=f"{T('visc_state')} {state_disp.get(rt_state, rt_state)}",
                                       text_color=state_color.get(rt_state, _C.TEXT_TER))

        if ml_n >= 2:
            cv_str = f"CV={ml_cv:.2f}" if ml_cv > 0 else ""
            models_str = " | ".join(f"{k}:{v:.0f}" for k, v in ml_models.items()) if ml_models else ""
            status_text = f"✓ Ensemble n={ml_n} {cv_str}"
            if models_str:
                status_text += f"\n  {models_str}"
            self.lbl_ml_status.configure(text=status_text, text_color=_C.GREEN)
        else:
            self.lbl_ml_status.configure(text=T("visc_ml_inactive"), text_color=_C.TEXT_TER)

    def _show_visc_detail(self):
        if not self._visc_detail_text:
            messagebox.showinfo(T("visc_detail"), "N/A")
            return
        dtop = ctk.CTkToplevel(self.top)
        dtop.title(T("visc_detail")); dtop.geometry("520x320")
        tb = ctk.CTkTextbox(dtop, font=ctk.CTkFont(family="Consolas", size=11), wrap="word", corner_radius=8, border_width=1, border_color=_C.BORDER)
        tb.pack(fill='both', expand=True, padx=10, pady=10)
        tb.insert("1.0", self._visc_detail_text)
        tb.configure(state="disabled")

    def _drag_start(self, e):
        item = self.tree.identify_row(e.y)
        if item and 'total' not in self.tree.item(item, 'tags'): self._drag_item = item
    def _drag_move(self, e):
        if not self._drag_item: return
        tgt = self.tree.identify_row(e.y)
        if tgt and tgt != self._drag_item and 'total' not in self.tree.item(tgt, 'tags'):
            self.tree.move(self._drag_item, self.tree.parent(tgt), self.tree.index(tgt))
    def _drag_end(self, e): self._drag_item = None

    def _do_copy(self):
        cols = self._col_defs()
        header = "\t".join(c[1] for c in cols)
        lines = [header]
        for iid in self.tree.get_children():
            vals = self.tree.item(iid, 'values')
            lines.append("\t".join(str(v) for v in vals))
        lines.append("")
        eta_text = self.lbl_visc_result.cget("text")
        ti_text = self.lbl_visc_ti.cget("text")
        state_text = self.lbl_visc_state.cget("text")
        conf_text = self.lbl_visc_conf.cget("text")
        lines.append(f"{T('visc_predict')}\t{eta_text}")
        lines.append(f"{ti_text}")
        lines.append(f"{state_text}")
        lines.append(f"{T('visc_confidence')}\t{conf_text}")
        text = "\n".join(lines) + "\n"
        self.top.clipboard_clear(); self.top.clipboard_append(text); self.top.update()
        messagebox.showinfo(T("copy_ok_title"), T("copy_ok"))

def _open_tools_dialog(_parent, _dm, _app, _fs, _fb, _last_mats):
    _dsc_data_holder = [None]
    top = ctk.CTkToplevel(_parent.winfo_toplevel())
    top.title(T("btn_tools")); top.geometry("700x650"); top.grab_set()
    nb = ctk.CTkTabview(top, corner_radius=8, segmented_button_selected_color=_app.current_accent)
    nb.pack(fill='both', expand=True, padx=10, pady=10)

    t1 = nb.add(T("tool_gel_time"))
    t2 = nb.add(T("tool_tg_predict"))
    t3 = nb.add(T("tool_dual_cure"))
    t4 = nb.add(T("tool_dsc_parser"))
    t5 = nb.add(T("tool_cte"))
    t6 = nb.add(T("tool_thermal_k"))
    t7 = nb.add(T("tool_elec"))

    fs = _fs; fb = _fb

    def _mk_row(parent, label, default="", width=120):
        r = ctk.CTkFrame(parent, fg_color="transparent"); r.pack(fill='x', pady=4, padx=10)
        ctk.CTkLabel(r, text=label, width=180, anchor='e', font=fs).pack(side='left', padx=5)
        e = ctk.CTkEntry(r, width=width, corner_radius=6, border_width=1, border_color=_C.BORDER)
        e.pack(side='left', padx=5)
        if default: e.insert(0, str(default))
        return e

    ctk.CTkLabel(t1, text=T("tool_hdr_arrhenius"), font=fb).pack(anchor='w', padx=10, pady=(10,5))
    # 固化劑類型下拉選單：display 用 T() 翻譯，internal key 保持英文
    _htype_display_map = {k: T(f"htype_{k}") for k in _COMMON_EA.keys()}  # internal -> display
    _htype_reverse_map = {v: k for k, v in _htype_display_map.items()}    # display -> internal
    htype_var = tk.StringVar(value=_htype_display_map["DICY"])
    r_ht = ctk.CTkFrame(t1, fg_color="transparent"); r_ht.pack(fill='x', pady=4, padx=10)
    ctk.CTkLabel(r_ht, text=T("tool_hardener_type"), width=180, anchor='e', font=fs).pack(side='left', padx=5)
    ht_cb = AppleDropdown(r_ht, variable=htype_var, values=list(_htype_display_map.values()), width=150, font=fs,
                          corner_radius=8, fg_color=_app.current_accent, button_color=_app.current_accent,
                          command=lambda v: _fill_ea(_htype_reverse_map.get(v, "DICY")))
    ht_cb.pack(side='left', padx=5)

    e_ea = _mk_row(t1, T("tool_ea"), "110")
    e_lna = _mk_row(t1, T("tool_ln_a"), "25.0")
    e_temp = _mk_row(t1, T("tool_cure_temp"), "150")
    e_mass = _mk_row(t1, T("tool_batch_mass"), "100")

    def _fill_ea(htype):
        ea_val, lna_val = _COMMON_EA.get(htype, (80, 18.0))
        e_ea.delete(0, 'end'); e_ea.insert(0, str(ea_val))
        e_lna.delete(0, 'end'); e_lna.insert(0, str(lna_val))

    lbl_gel = ctk.CTkLabel(t1, text="", font=fb, justify='left', wraplength=450)
    lbl_gel.pack(anchor='w', padx=15, pady=10)

    def _calc_gel():
        try:
            r = arrhenius_gel_time(float(e_ea.get()), float(e_lna.get()),
                                   float(e_temp.get()), float(e_mass.get()))
            analytical = r['gel_time_min']
            txt = f"━━ Arrhenius ━━\n"
            txt += f"k = {r['rate_constant']:.4e} s⁻¹\n"
            txt += f"Gel Time ≈ {analytical:.1f} min\n"
            txt += f"ΔT (adiabatic) ≈ {r['delta_T_adiabatic']:.0f}°C\n"
            txt += f"Peak Temp ≈ {r['peak_temp']:.0f}°C\n"
            mats = _last_mats
            if mats:
                ml = PropertyMLPredictor(_dm, 'gel_time')
                res = ml.predict(mats, analytical)
                if res['n_train'] >= 2:
                    txt += f"\n━━ ML Ensemble (n={res['n_train']}) ━━\n"
                    txt += f"ML predict: {res['ml_pred']:.1f} min\n"
                    txt += f"Blended ({res['blend_weight']*100:.0f}% ML): {res['prediction']:.1f} min\n"
                    txt += f"Confidence: {res['confidence']} (CV={res.get('cv_score',0):.2f})"
                else:
                    txt += f"\n⚠ ML: insufficient data (n={res['n_train']})"
            else:
                txt += "\n💡 先計算配方再開啟工具，可啟用ML預測"
            lbl_gel.configure(text=txt)
        except Exception as ex:
            lbl_gel.configure(text=str(ex))

    ctk.CTkButton(t1, text="▶ " + T("tool_result"), fg_color=_app.current_accent,
                   command=_calc_gel, corner_radius=8).pack(fill='x', padx=10, pady=5)

    ctk.CTkLabel(t2, text=T("tool_hdr_dibenedetto"), font=fb).pack(anchor='w', padx=10, pady=(10,5))
    e_tg0 = _mk_row(t2, T("tool_tg0"), "-20")
    e_tginf = _mk_row(t2, T("tool_tg_inf"), "150")
    e_lam = _mk_row(t2, T("tool_lambda"), "0.50")
    e_alpha = _mk_row(t2, T("tool_alpha"), "0.95")

    lbl_tg = ctk.CTkLabel(t2, text="", font=fb, justify='left', wraplength=450)
    lbl_tg.pack(anchor='w', padx=15, pady=10)

    def _calc_tg():
        try:
            tg0 = float(e_tg0.get()); tginf = float(e_tginf.get())
            lam = float(e_lam.get()); alpha = float(e_alpha.get())
            tg_analytical = dibenedetto_tg(tg0, tginf, lam, alpha)
            txt = f"━━ DiBenedetto ━━\n"
            txt += f"Tg(@α={alpha:.2f}) = {tg_analytical:.1f}°C\n"
            for a in [0.5, 0.7, 0.85, 0.95, 1.0]:
                t = dibenedetto_tg(tg0, tginf, lam, a)
                txt += f"  α={a:.2f} → Tg={t:.1f}°C\n"
            mats = _last_mats
            if mats:
                ml = PropertyMLPredictor(_dm, 'tg')
                res = ml.predict(mats, tg_analytical)
                if res['n_train'] >= 2:
                    txt += f"\n━━ ML Ensemble (n={res['n_train']}) ━━\n"
                    txt += f"ML predict: {res['ml_pred']:.1f}°C\n"
                    txt += f"Blended ({res['blend_weight']*100:.0f}% ML): {res['prediction']:.1f}°C\n"
                    txt += f"Confidence: {res['confidence']} (CV={res.get('cv_score',0):.2f})"
                else:
                    txt += f"\n⚠ ML: insufficient data (n={res['n_train']})"
            else:
                txt += "\n💡 先計算配方再開啟工具，可啟用ML預測"
            lbl_tg.configure(text=txt)
        except Exception as ex:
            lbl_tg.configure(text=str(ex))

    ctk.CTkButton(t2, text="▶ " + T("tool_result"), fg_color=_app.current_accent,
                   command=_calc_tg, corner_radius=8).pack(fill='x', padx=10, pady=5)

    ctk.CTkLabel(t3, text=T("tool_hdr_dualcure"), font=fb).pack(anchor='w', padx=10, pady=(10,2))
    ctk.CTkLabel(t3, text=T("tool_hdr_dualcure_sub"), font=fs, text_color=_C.TEXT_SEC).pack(anchor='w', padx=10, pady=(0,5))
    e_pi = _mk_row(t3, T("tool_uv_pi"), "3.0")
    e_dose = _mk_row(t3, T("tool_uv_dose"), "3000")
    e_ti = _mk_row(t3, T("tool_thermal_ti"), "1.0")
    e_tcure = _mk_row(t3, T("tool_cure_temp"), "150")
    e_cat = _mk_row(t3, T("tool_cat_coeff"), "0.05")
    ctk.CTkLabel(t3, text=T("tool_cat_coeff_hint"), font=ctk.CTkFont(family=_FONT_FAMILY, size=10),
                 text_color=_C.TEXT_SEC, wraplength=400).pack(anchor='w', padx=15)

    lbl_dc = ctk.CTkLabel(t3, text="", font=fb, justify='left', wraplength=450)
    lbl_dc.pack(anchor='w', padx=15, pady=10)

    def _calc_dc():
        try:
            pi = float(e_pi.get()); dose = float(e_dose.get())
            ti = float(e_ti.get()); tc = float(e_tcure.get()); cat_c = float(e_cat.get())
            uv_eff = min(0.95, 0.1 * math.log(1 + dose / 500) * (pi / 3.0) ** 0.5)
            R = 8.314; T = tc + 273.15
            ea_th, lna_th = 85, 20.0
            k_th = math.exp(lna_th - ea_th * 1000 / (R * T))
            remain = 1.0 - uv_eff
            thermal_conv = remain * (1 - math.exp(-k_th * 30 * 60)) * (1 + cat_c)
            total_conv = min(1.0, uv_eff + thermal_conv)
            txt = f"━━ Analytical ━━\n"
            txt += f"UV stage:     α_uv  = {uv_eff:.3f} ({uv_eff*100:.1f}%)\n"
            txt += f"Thermal stage: α_th  = {thermal_conv:.3f} ({thermal_conv*100:.1f}%)\n"
            txt += f"Homo-poly:    coeff = {cat_c:.2f}\n"
            txt += f"Total α       = {total_conv:.3f} ({total_conv*100:.1f}%)\n"
            tg_analytical = dibenedetto_tg(-20, 150, 0.5, total_conv) if total_conv > 0 else -20
            txt += f"DiBenedetto Tg ≈ {tg_analytical:.0f}°C\n"
            mats = _last_mats
            if mats:
                ml_tg = PropertyMLPredictor(_dm, 'tg')
                res = ml_tg.predict(mats, tg_analytical)
                if res['n_train'] >= 2:
                    txt += f"\n━━ ML Tg (n={res['n_train']}) ━━\n"
                    txt += f"ML Tg: {res['ml_pred']:.1f}°C\n"
                    txt += f"Blended: {res['prediction']:.1f}°C ({res['confidence']})"
            lbl_dc.configure(text=txt)
        except Exception as ex:
            lbl_dc.configure(text=str(ex))

    ctk.CTkButton(t3, text="▶ " + T("tool_result"), fg_color=_app.current_accent,
                   command=_calc_dc, corner_radius=8).pack(fill='x', padx=10, pady=5)

    ctk.CTkLabel(t4, text=T("tool_hdr_dsc"), font=fb).pack(anchor='w', padx=10, pady=(10,5))

    _dsc_data_holder[0] = None
    lbl_dsc = ctk.CTkLabel(t4, text="", font=fs, justify='left', wraplength=450)
    lbl_dsc.pack(anchor='w', padx=15, pady=10)

    def _load_dsc():
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=[("CSV/TXT", "*.csv *.txt"), ("All", "*.*")], parent=top)
        if not path: return
        try:
            temps = []; heats = []
            with open(path, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    parts = line.strip().replace(',', '\t').split('\t')
                    if len(parts) >= 2:
                        try:
                            t = float(parts[0]); h = float(parts[1])
                            temps.append(t); heats.append(h)
                        except ValueError:
                            continue
            if len(temps) < 10:
                lbl_dsc.configure(text=f"Data too short ({len(temps)} points). Need col1=Temp, col2=HeatFlow.")
                return
            _dsc_data_holder[0] = (temps, heats)
            _analyze_dsc(temps, heats)
        except Exception as ex:
            lbl_dsc.configure(text=f"Error: {ex}")

    def _analyze_dsc(temps, heats):
        n = len(temps)
        peak_idx = 0; peak_val = heats[0]
        for i in range(n):
            if heats[i] > peak_val:
                peak_val = heats[i]; peak_idx = i
        tp = temps[peak_idx]

        ti = temps[0]
        threshold = peak_val * 0.05
        for i in range(peak_idx):
            if heats[i] > threshold:
                ti = temps[i]; break

        dt = abs(temps[1] - temps[0]) if n > 1 else 1.0
        dh = sum(heats) * dt
        dh_abs = abs(dh)

        ea_analytical = 0.47 * (tp + 273.15) - 50 if tp > 100 else 0

        txt = f"━━ DSC Curve Analysis ━━\n"
        txt += f"Data: {n} points ({temps[0]:.0f}°C ~ {temps[-1]:.0f}°C)\n"
        txt += f"{T('tool_dsc_ti')} {ti:.1f}°C\n"
        txt += f"{T('tool_dsc_tp')} {tp:.1f}°C\n"
        txt += f"{T('tool_dsc_dh')} {dh_abs:.1f} J/g\n"
        txt += f"{T('tool_dsc_ea')} ~{ea_analytical:.0f} kJ/mol (Kissinger)\n"

        mats = _last_mats
        if mats:
            ml_tg = PropertyMLPredictor(_dm, 'tg')
            res_tg = ml_tg.predict(mats, tp * 0.7)
            ml_dh = PropertyMLPredictor(_dm, 'dh')
            res_dh = ml_dh.predict(mats, dh_abs)
            txt += f"\n━━ ML Enhancement ━━\n"
            if res_tg['n_train'] >= 2:
                txt += f"ML Tg predict: {res_tg['ml_pred']:.1f}°C (n={res_tg['n_train']})\n"
            if res_dh['n_train'] >= 2:
                txt += f"ML ΔH predict: {res_dh['ml_pred']:.1f} J/g (n={res_dh['n_train']})\n"
                if res_dh['ml_pred'] > 0 and dh_abs > 0:
                    cure_degree = min(1.0, dh_abs / res_dh['ml_pred'])
                    txt += f"Est. cure degree: α ≈ {cure_degree:.2f} ({cure_degree*100:.0f}%)"
            if res_tg['n_train'] < 2 and res_dh['n_train'] < 2:
                txt += "⚠ Insufficient recipe data for ML"
        else:
            txt += "\n💡 先計算配方再開啟工具，可啟用ML預測"

        lbl_dsc.configure(text=txt)

    ctk.CTkButton(t4, text=T("tool_load_csv"), fg_color=_app.current_accent,
                   command=_load_dsc, corner_radius=8).pack(fill='x', padx=10, pady=5)

    # ── CTE Prediction ──
    ctk.CTkLabel(t5, text=T("tool_hdr_cte"), font=fb).pack(anchor='w', padx=10, pady=(10,5))
    e_cte_r = _mk_row(t5, T("tool_resin_cte"), "65")
    e_cte_f = _mk_row(t5, T("tool_filler_cte"), "0.5")
    e_cte_phi = _mk_row(t5, T("tool_filler_vf"), "0.30")
    lbl_cte = ctk.CTkLabel(t5, text="", font=fb, justify='left', wraplength=450)
    lbl_cte.pack(anchor='w', padx=15, pady=10)

    def _calc_cte():
        try:
            cr = float(e_cte_r.get()); cf = float(e_cte_f.get()); phi = float(e_cte_phi.get())
            r = predict_cte(cr, cf, phi)
            txt = f"━━ Physics Models ━━\n"
            txt += f"Rule of Mixtures: {r['rom']:.1f} ppm/°C\n"
            txt += f"Turner model:     {r['turner']:.1f} ppm/°C\n"
            txt += f"Schapery lower:   {r['schapery_lo']:.1f} ppm/°C\n"
            analytical = r['turner']
            mats = _last_mats
            if mats:
                ml = PropertyMLPredictor(_dm, 'cte1')
                res = ml.predict(mats, analytical)
                if res['n_train'] >= 2:
                    txt += f"\n━━ ML Ensemble (n={res['n_train']}) ━━\n"
                    txt += f"ML: {res['ml_pred']:.1f} ppm/°C\n"
                    txt += f"Blended ({res['blend_weight']*100:.0f}% ML): {res['prediction']:.1f} ppm/°C\n"
                    txt += f"Confidence: {res['confidence']}"
                else:
                    txt += f"\n⚠ ML: n={res['n_train']}, need ≥2"
            else:
                txt += "\n💡 先計算配方再開啟工具，可啟用ML預測"
            lbl_cte.configure(text=txt)
        except Exception as ex: lbl_cte.configure(text=str(ex))

    ctk.CTkButton(t5, text="▶ " + T("tool_result"), fg_color=_app.current_accent,
                   command=_calc_cte, corner_radius=8).pack(fill='x', padx=10, pady=5)

    # ── Thermal Conductivity ──
    ctk.CTkLabel(t6, text=T("tool_hdr_thermal_k"), font=fb).pack(anchor='w', padx=10, pady=(10,5))
    e_kr = _mk_row(t6, T("tool_resin_k"), "0.20")
    e_kf = _mk_row(t6, T("tool_filler_k"), "30.0")
    e_k_phi = _mk_row(t6, T("tool_filler_vf"), "0.30")
    lbl_k = ctk.CTkLabel(t6, text="", font=fb, justify='left', wraplength=450)
    lbl_k.pack(anchor='w', padx=15, pady=10)

    def _calc_k():
        try:
            kr = float(e_kr.get()); kf = float(e_kf.get()); phi = float(e_k_phi.get())
            r = predict_thermal_k(kr, kf, phi)
            txt = f"━━ Physics Models ━━\n"
            txt += f"Maxwell:       {r['maxwell']:.3f} W/(m·K)\n"
            txt += f"Bruggeman:     {r['bruggeman']:.3f} W/(m·K)\n"
            txt += f"Lewis-Nielsen: {r['lewis_nielsen']:.3f} W/(m·K)\n"
            avg_phys = (r['maxwell'] + r['bruggeman'] + r['lewis_nielsen']) / 3
            mats = _last_mats
            if mats:
                ml = PropertyMLPredictor(_dm, 'thermal_k')
                res = ml.predict(mats, avg_phys)
                if res['n_train'] >= 2:
                    txt += f"\n━━ ML Ensemble (n={res['n_train']}) ━━\n"
                    txt += f"ML: {res['ml_pred']:.3f} W/(m·K)\n"
                    txt += f"Blended: {res['prediction']:.3f} W/(m·K) ({res['confidence']})"
                else:
                    txt += f"\n⚠ ML: n={res['n_train']}, need ≥2"
            else:
                txt += "\n💡 先計算配方再開啟工具，可啟用ML預測"
            lbl_k.configure(text=txt)
        except Exception as ex: lbl_k.configure(text=str(ex))

    ctk.CTkButton(t6, text="▶ " + T("tool_result"), fg_color=_app.current_accent,
                   command=_calc_k, corner_radius=8).pack(fill='x', padx=10, pady=5)

    # ── Electrical Conductivity/Resistivity ──
    ctk.CTkLabel(t7, text=T("tool_hdr_elec"), font=fb).pack(anchor='w', padx=10, pady=(10,5))
    e_rho_r = _mk_row(t7, T("tool_resin_rho"), "1e15")
    e_rho_f = _mk_row(t7, T("tool_filler_rho_e"), "1e-5")
    e_e_phi = _mk_row(t7, T("tool_filler_vf"), "0.30")
    e_phic = _mk_row(t7, T("tool_perc_thresh"), "0.15")
    lbl_e = ctk.CTkLabel(t7, text="", font=fb, justify='left', wraplength=450)
    lbl_e.pack(anchor='w', padx=15, pady=10)

    def _calc_elec():
        try:
            rr = float(e_rho_r.get()); rf = float(e_rho_f.get())
            phi = float(e_e_phi.get()); phic = float(e_phic.get())
            r = predict_elec(rr, rf, phi, phi_c=phic)
            txt = f"━━ Percolation Model ━━\n"
            txt += f"φ = {phi:.3f}   φc = {phic:.3f}\n"
            if r['conductive']:
                txt += f"⚡ ABOVE percolation threshold\n"
            else:
                txt += f"🔒 Below percolation threshold (insulating)\n"
            txt += f"log(ρ) = {r['log_rho']:.2f}\n"
            txt += f"ρ ≈ {r['rho']:.2e} Ω·cm\n"
            if r['rho'] > 0:
                sigma = 1.0 / r['rho']
                txt += f"σ ≈ {sigma:.2e} S/cm"
            mats = _last_mats
            if mats:
                ml = PropertyMLPredictor(_dm, 'dk_1mhz')
                res = ml.predict(mats, r['log_rho'])
                if res['n_train'] >= 2:
                    txt += f"\n\n━━ ML (Dk proxy, n={res['n_train']}) ━━\n"
                    txt += f"ML Dk@1MHz: {res['ml_pred']:.2f} ({res['confidence']})"
            lbl_e.configure(text=txt)
        except Exception as ex: lbl_e.configure(text=str(ex))

    ctk.CTkButton(t7, text="▶ " + T("tool_result"), fg_color=_app.current_accent,
                   command=_calc_elec, corner_radius=8).pack(fill='x', padx=10, pady=5)


class CalcTab:
    @staticmethod
    def _mode_map():
        return {
            T("mode_stoich"):  "stoich",
            T("mode_weight"):  "weight",
            T("mode_target100"): "target_100",
            T("mode_phr100"): "phr_100",
        }

    def __init__(self, parent_frame, dm: DataManager, font_std, font_bold, app_instance):
        self.dm = dm; self.fs = font_std; self.fb = font_bold
        self.app = app_instance
        self.frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.frame.pack(fill='both', expand=True)
        
        self.calc_rows = {c: [] for c in get_all_slot_counts()}
        self._drag_item = None
        self._build()

    def _build(self):
        self.paned = tk.PanedWindow(self.frame, orient=tk.HORIZONTAL, sashwidth=8,
                                     sashcursor='sb_h_double_arrow', showhandle=False,
                                     sashrelief='flat', bg=_C.SASH, bd=0)
        self.paned.pack(fill='both', expand=True, pady=5)

        left_tk = tk.Frame(self.paned, bg='#f5f5f7')
        self.sf = ctk.CTkScrollableFrame(left_tk, corner_radius=8)
        self.sf.pack(fill="both", expand=True)
        self.paned.add(left_tk, minsize=250, width=600)

        rf = ctk.CTkFrame(self.sf, corner_radius=8, border_width=1, border_color=_C.BORDER)
        rf.pack(fill='x', pady=5, padx=5)
        ctk.CTkLabel(rf, text=T("sec_resin"), font=self.fb).pack(anchor='w', padx=10, pady=(5,0))
        self.resin_box = ctk.CTkFrame(rf, fg_color="transparent")
        self.resin_box.pack(fill='both', expand=True, padx=5, pady=5)
        self.btn_add_resin = ctk.CTkButton(rf, text=T("add_resin"), fg_color="transparent", text_color=self.app.current_accent, border_width=1, border_color=self.app.current_accent, hover_color=_C.BTN_ADD_HV, command=lambda: self.add_row('resins', self.resin_box), corner_radius=8)
        self.btn_add_resin.pack(anchor='w', padx=10, pady=(0, 10))

        hf = ctk.CTkFrame(self.sf, corner_radius=8, border_width=1, border_color=_C.BORDER)
        hf.pack(fill='x', pady=5, padx=5)
        ctk.CTkLabel(hf, text=T("sec_hardener"), font=self.fb).pack(anchor='w', padx=10, pady=(5,0))
        
        mf = ctk.CTkFrame(hf, fg_color="transparent")
        mf.pack(fill='x', padx=10, pady=2)
        ctk.CTkLabel(mf, text=T("calc_mode"), font=self.fs).pack(side='left')
        self.calc_mode = tk.StringVar(value=T("mode_phr100"))
        self.mcb = AppleDropdown(mf, variable=self.calc_mode, width=220, font=self.fs, corner_radius=8, fg_color=self.app.current_accent, button_color=self.app.current_accent,
                                values=list(self._mode_map().keys()), command=self._update_ui)
        self.mcb.pack(side='left', padx=10)
        
        self.h_header = ctk.CTkFrame(hf, fg_color="transparent")
        self.h_header.pack(fill='x', padx=10)
        self.hardener_box = ctk.CTkFrame(hf, fg_color="transparent")
        self.hardener_box.pack(fill='both', expand=True, padx=5, pady=5)
        self.btn_add_hardener = ctk.CTkButton(hf, text=T("add_hardener"), fg_color="transparent", text_color=self.app.current_accent, border_width=1, border_color=self.app.current_accent, hover_color=_C.BTN_ADD_HV, command=lambda: self.add_row('hardeners', self.hardener_box), corner_radius=8)
        self.btn_add_hardener.pack(anchor='w', padx=10, pady=(0, 10))

        self.other_btns = []
        for cat, title_key in [('additives','sec_additive'),('fillers','sec_filler'),('catalysts','sec_catalyst')]:
            f = ctk.CTkFrame(self.sf, corner_radius=8, border_width=1, border_color=_C.BORDER)
            f.pack(fill='x', pady=5, padx=5)
            ctk.CTkLabel(f, text=T(title_key), font=self.fb).pack(anchor='w', padx=10, pady=(5,0))
            box = ctk.CTkFrame(f, fg_color="transparent")
            box.pack(fill='both', expand=True, padx=5, pady=5)
            setattr(self, f"{cat}_box", box)
            btn_text = T({"additives":"add_additive","fillers":"add_filler","catalysts":"add_catalyst"}[cat])
            btn = ctk.CTkButton(f, text=btn_text, fg_color="transparent", text_color=self.app.current_accent,
                                border_width=1, border_color=self.app.current_accent, hover_color=_C.BTN_ADD_HV,
                                command=lambda c=cat, b=box: self.add_row(c, b), corner_radius=8)
            btn.pack(anchor='w', padx=10, pady=(0, 10))
            self.other_btns.append(btn)

        self._custom_mat_boxes = {}
        self.custom_btns = []
        for mc in _custom_mat_cats:
            ckey = mc['key']; disp = get_mat_cat_display(ckey)
            f = ctk.CTkFrame(self.sf, corner_radius=8, border_width=1, border_color=_C.BORDER)
            f.pack(fill='x', pady=5, padx=5)
            ctk.CTkLabel(f, text=disp, font=self.fb).pack(anchor='w', padx=10, pady=(5,0))
            box = ctk.CTkFrame(f, fg_color="transparent")
            box.pack(fill='both', expand=True, padx=5, pady=5)
            self._custom_mat_boxes[ckey] = box
            if ckey not in self.calc_rows: self.calc_rows[ckey] = []
            btn = ctk.CTkButton(f, text=f"{T('add_custom_prefix')}{disp}", fg_color="transparent", text_color=self.app.current_accent,
                                border_width=1, border_color=self.app.current_accent, hover_color=_C.BTN_ADD_HV,
                                command=lambda c=ckey, b=box: self.add_row(c, b), corner_radius=8)
            btn.pack(anchor='w', padx=10, pady=(0, 10))
            self.custom_btns.append(btn)

        right_tk = tk.Frame(self.paned, bg='#f5f5f7')
        self.paned.add(right_tk, minsize=200)
        ra = ctk.CTkScrollableFrame(right_tk, corner_radius=8)
        ra.pack(fill='both', expand=True)
        
        cf = ctk.CTkFrame(ra, corner_radius=8, border_width=1, border_color=_C.BORDER)
        cf.pack(fill='x', padx=10, pady=10)
        ctk.CTkLabel(cf, text=T("calc_settings"), font=self.fb).pack(anchor='w', padx=10, pady=(5,0))
        
        row1 = ctk.CTkFrame(cf, fg_color="transparent")
        row1.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(row1, text=T("mass_rounding"), font=self.fs).pack(side='left', padx=5)
        self.round_opt = tk.StringVar(value=T("round_2dp"))
        self.round_cb = AppleDropdown(row1, variable=self.round_opt, font=self.fs, width=120, corner_radius=8, fg_color=self.app.current_accent, button_color=self.app.current_accent,
                          values=[T("round_none"),T("round_int"),T("round_1dp"),T("round_2dp")])
        self.round_cb.pack(side='left')

        ctk.CTkLabel(row1, text="    " + T("batch_scale"), font=self.fs).pack(side='left', padx=(10,0))
        self.batch_scale_var = ctk.CTkEntry(row1, width=55, corner_radius=6, border_width=1, border_color=_C.BORDER)
        self.batch_scale_var.insert(0, "100")
        self.batch_scale_var.pack(side='left', padx=3)
        ctk.CTkLabel(row1, text="%", font=self.fs).pack(side='left')

        self.t100_frame = ctk.CTkFrame(cf, fg_color="transparent")
        self.lbl_100g_hint = ctk.CTkLabel(self.t100_frame, text=T("hint_100g_extra"), font=self.fs, text_color=self.app.current_accent)
        self.lbl_100g_hint.pack(anchor='w', padx=5, pady=3)

        self.btn_calc = ctk.CTkButton(cf, text=T("btn_calculate"), font=self.fb, fg_color=self.app.current_accent, command=self.calculate, corner_radius=8)
        self.btn_calc.pack(fill='x', padx=10, pady=(5, 10))

        tf = RoundedTreeFrame(ra)
        tf.pack(fill="x", padx=10, pady=(0,5))
        cols = [("name",T("col_mat_name"),160),("mass",T("col_mass_g_result"),80),
                ("scaled",T("col_scaled"),80),("phr",T("col_phr_result"),70),
                ("percent",T("col_pct_result"),70),("eq",T("col_eq_val"),75),("cl",T("col_cl_result"),75)]
        self.tree = ttk.Treeview(tf.inner, columns=[c[0] for c in cols], show='headings', height=10)
        for cid, hdr, w in cols: 
            self.tree.heading(cid, text=hdr)
            self.tree.column(cid, width=w, anchor='center')
        vsbt = ttk.Scrollbar(tf.inner, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsbt.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsbt.pack(side='right', fill='y')
        self.tree.tag_configure('total', font=(_FONT_FAMILY, 11, "bold"), background=_C.BG_LIGHT)
        self.tree.bind("<ButtonPress-1>",   self._ds)
        self.tree.bind("<B1-Motion>", self._dm)
        self.tree.bind("<ButtonRelease-1>", self._dr)

        bf = ctk.CTkFrame(ra, fg_color="transparent")
        bf.pack(fill='x', padx=10, pady=10)
        ctk.CTkButton(bf, text=T("btn_copy_excel"), fg_color=_C.GREEN, hover_color=_C.GREEN_HV, corner_radius=8, command=self._copy).pack(side='left', fill='x', expand=True, padx=(0,5))
        self.btn_save = ctk.CTkButton(bf, text=T("btn_save_recipe"), fg_color=self.app.current_accent, command=self._save, corner_radius=8)
        self.btn_save.pack(side='left', fill='x', expand=True, padx=(5,5))
        self.btn_tools = ctk.CTkButton(bf, text=T("btn_tools"), fg_color=_C.BTN_LIGHT, text_color=_C.TEXT, hover_color=_C.BTN_HOVER, corner_radius=8, command=self._open_tools, width=80)
        self.btn_tools.pack(side='left', padx=(5,0))

        self.add_row('resins', self.resin_box)
        self.add_row('hardeners', self.hardener_box)
        self.add_row('additives', self.additives_box)
        self.add_row('fillers', self.fillers_box)
        self.add_row('catalysts', self.catalysts_box)
        for mc in _custom_mat_cats:
            ckey = mc['key']
            if ckey in self._custom_mat_boxes:
                self.add_row(ckey, self._custom_mat_boxes[ckey])
        self._update_ui()

    def update_accent_color(self, hex_color):
        self.btn_add_resin.configure(text_color=hex_color, border_color=hex_color)
        self.btn_add_hardener.configure(text_color=hex_color, border_color=hex_color)
        for btn in self.other_btns: btn.configure(text_color=hex_color, border_color=hex_color)
        for btn in self.custom_btns: btn.configure(text_color=hex_color, border_color=hex_color)
        self.btn_calc.configure(fg_color=hex_color)
        self.btn_save.configure(fg_color=hex_color)
        self.lbl_100g_hint.configure(text_color=hex_color)
        self.mcb.configure(fg_color=hex_color, button_color=hex_color)
        self.round_cb.configure(fg_color=hex_color, button_color=hex_color)

    def _ds(self, e):
        item = self.tree.identify_row(e.y)
        if not item or any(t in self.tree.item(item,"tags") for t in ('total','divider')): return
        self._drag_item = item
    def _dm(self, e):
        if not self._drag_item: return
        tgt = self.tree.identify_row(e.y)
        if not tgt or tgt == self._drag_item or any(t in self.tree.item(tgt,"tags") for t in ('total','divider')): return
        self.tree.move(self._drag_item, self.tree.parent(tgt), self.tree.index(tgt))
    def _dr(self, e): self._drag_item = None

    def _update_ui(self, _=None):
        mode = self._mode_map().get(self.calc_mode.get(), "stoich")
        self._sync_resin_modes()
        self._sync_hardener_header()
        if mode == "target_100":
            self.t100_frame.pack(fill='x', pady=5)
            self.lbl_100g_hint.configure(text=T("hint_100g_extra"))
        elif mode == "phr_100":
            self.t100_frame.pack(fill='x', pady=5)
            self.lbl_100g_hint.configure(text=T("hint_phr100"))
        else:
            self.t100_frame.pack_forget()
        is_pct = mode in ("target_100", "phr_100")
        for cat in list(SLOT_COUNTS.keys()):
            if cat in ('resins','hardeners'): continue
            for rd in self.calc_rows.get(cat, []):
                if rd.get('lbl_unit'): rd['lbl_unit'].configure(text="%" if is_pct else "g")
        for mc in _custom_mat_cats:
            if not mc.get('has_eew'):
                for rd in self.calc_rows.get(mc['key'], []):
                    if rd.get('lbl_unit'): rd['lbl_unit'].configure(text="%" if is_pct else "g")

    def _sync_resin_modes(self, _=None):
        mode = self._mode_map().get(self.calc_mode.get(), "stoich")
        allow = mode in ("target_100", "phr_100")
        avail = [T("fixed_mass"), T("ratio_pending")] if allow else [T("fixed_mass")]
        for rd in self.calc_rows['resins']:
            if rd.get('cb_mode'):
                rd['cb_mode'].configure(values=avail)
                if allow:
                    entry_empty = not rd.get('entry') or not rd['entry'].get().strip()
                    if rd['mode_var'].get() == T("fixed_mass") and entry_empty:
                        rd['mode_var'].set(T("ratio_pending"))
                        rd['cb_mode'].set(T("ratio_pending"))
                        if rd.get('lbl_unit'): rd['lbl_unit'].configure(text="R-parts")
                elif rd['mode_var'].get() == T("ratio_pending"):
                    rd['mode_var'].set(T('fixed_mass'))
                    rd['cb_mode'].set(T('fixed_mass'))
                    if rd.get('lbl_unit'): rd['lbl_unit'].configure(text="g")

    def _sync_hardener_header(self):
        n = len(self.calc_rows['hardeners'])
        for w in self.h_header.winfo_children(): w.destroy()
        ctk.CTkLabel(self.h_header, text=T("hdr_name_type"), width=200, anchor='w').pack(side='left')
        if n > 1: ctk.CTkLabel(self.h_header, text=T("hdr_eq_ratio"), width=80).pack(side='left', padx=5)
        ctk.CTkLabel(self.h_header, text=T("hdr_corr_pct"), width=80).pack(side='left', padx=5)
        for rd in self.calc_rows['hardeners']:
            if n > 1:
                rd['eq_ratio'].pack(side='left', padx=5, before=rd['corr'])
                rd['lbl_ru'].pack(side='left', before=rd['corr'])
            else:
                rd['eq_ratio'].pack_forget()
                rd['lbl_ru'].pack_forget()

    def add_row(self, cat, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill='x', pady=2)
        cb = ctk.CTkEntry(row, width=220, corner_radius=6, border_width=1, border_color=_C.BORDER, font=ctk.CTkFont(family=_FONT_FAMILY, size=11),
                           placeholder_text=T("search_placeholder"))
        cb.pack(side='left')
        cb.bind('<KeyRelease>', lambda e: self._filter(e, cb, cat))
        cb.bind('<FocusOut>', lambda e: cb.after(200, self._ac_close))
        ctk.CTkButton(row, text="▾", width=26, height=26, corner_radius=6,
                       fg_color=_C.BTN_LIGHT, text_color=_C.TEXT_SEC, hover_color=_C.BTN_HOVER,
                       command=lambda: self._show_all(None, cb, cat)).pack(side='left', padx=(2,0))
        
        ctk.CTkButton(row, text="↺", width=26, height=26, corner_radius=6,
                       fg_color=_C.BTN_LIGHT, text_color=_C.TEXT_SEC, hover_color=_C.BTN_HOVER,
                       command=lambda: self._clear_cb(cb, cat)).pack(side='left', padx=(4,0))
        rd = {"frame": row, "cb": cb}

        tip = ToolTip(cb, lambda _c=cat, _cb=cb: _build_mat_tooltip(
            self.dm, _c, _cb.get().split("  [")[0].strip()))
        rd["tooltip"] = tip

        if cat == 'resins':
            cur_mode = self._mode_map().get(self.calc_mode.get(), "stoich")
            is_parts = cur_mode in ("target_100", "phr_100")
            avail = [T("fixed_mass"), T("ratio_pending")] if is_parts else [T("fixed_mass")]
            default_mode = T("ratio_pending") if is_parts else T("fixed_mass")
            mv = tk.StringVar(value=default_mode)
            cbm = AppleDropdown(row, variable=mv, width=100, values=avail, corner_radius=6,
                                    fg_color=_C.BTN_LIGHT, button_color="#aeaeb2", text_color=_C.TEXT,
                                    command=lambda v: lbl.configure(text="g" if v==T("fixed_mass") else "R-parts"))
            cbm.pack(side='left', padx=5)
            ent = ctk.CTkEntry(row, width=60, corner_radius=6, border_width=1, border_color=_C.BORDER)
            ent.pack(side='left', padx=5)
            lbl = ctk.CTkLabel(row, text="R-parts" if is_parts else "g", font=self.fs)
            lbl.pack(side='left')
            rd.update({"entry": ent, "mode_var": mv, "cb_mode": cbm, "lbl_unit": lbl})
            self._sync_resin_modes()
        elif cat == 'hardeners':
            eq = ctk.CTkEntry(row, width=60, corner_radius=6, border_width=1, border_color=_C.BORDER); eq.insert(0,"100"); eq.pack(side='left', padx=5)
            lru = ctk.CTkLabel(row, text="%", font=self.fs); lru.pack(side='left')
            corr = ctk.CTkEntry(row, width=60, corner_radius=6, border_width=1, border_color=_C.BORDER); corr.insert(0,"100"); corr.pack(side='left', padx=5)
            ctk.CTkLabel(row, text="%", font=self.fs).pack(side='left')
            rd.update({"eq_ratio": eq, "lbl_ru": lru, "corr": corr})
        else:
            ent = ctk.CTkEntry(row, width=70, corner_radius=6, border_width=1, border_color=_C.BORDER); ent.pack(side='left', padx=5)
            cur_mode = self._mode_map().get(self.calc_mode.get(), "stoich")
            lbl_u = ctk.CTkLabel(row, text="%" if cur_mode == "target_100" else "g", font=self.fs)
            lbl_u.pack(side='left')
            rd.update({"entry": ent, "lbl_unit": lbl_u})

        ctk.CTkButton(row, text="✕", width=26, height=26, corner_radius=6, fg_color=_C.BTN_LIGHT, text_color=_C.TEXT_SEC, hover_color=_C.RED,
                      command=lambda: self._del_row(row, cat)).pack(side='right', padx=5)
        self.calc_rows[cat].append(rd)
        if cat == 'hardeners': self._sync_hardener_header()

    def _del_row(self, frame, cat):
        self._ac_close()
        frame.destroy()
        self.calc_rows[cat] = [r for r in self.calc_rows[cat] if r['frame'] != frame]
        if cat == 'hardeners': self._sync_hardener_header()
        elif cat == 'resins': self._sync_resin_modes()

    def _opts(self, cat): return [f"{n}  [{i.get('type','')}]" for n, i in sorted(self.dm.materials.get(cat,{}).items())]

    def _filter(self, e, cb, cat):
        if e.keysym in ['Escape','Return','Up']: self._ac_close(); return
        txt = cb.get().split("  [")[0].lower().strip()
        filtered = [o for o in self._opts(cat) if txt in o.lower()] if txt else self._opts(cat)
        if filtered and txt: self._ac_show(cb, filtered)
        else: self._ac_close()

    def _show_all(self, e, cb, cat): self._ac_close(); self._ac_show(cb, self._opts(cat))
    def _clear_cb(self, cb, cat): self._ac_close(); cb.delete(0, 'end'); cb.focus_set()

    def _ac_show(self, cb, items):
        if not hasattr(self, '_popup') or self._popup is None:
            self._popup = RoundedPopup(self.frame, self.app.current_accent)
        self._popup.accent = self.app.current_accent
        self._popup.show(cb, items, lambda: None)

    def _ac_select(self): pass

    def _ac_close(self):
        if hasattr(self, '_popup') and self._popup:
            self._popup.close()

    def calculate(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            mode = self._mode_map().get(self.calc_mode.get(), "stoich")
            mats = []; fixed_r_mass = 0.0; fixed_r_eq = 0.0
            ratio_r = []; total_r_parts = 0.0

            for rd in self.calc_rows['resins']:
                nm = rd['cb'].get().split("  [")[0]; vs = rd['entry'].get()
                if not nm or not vs: continue
                v = float(vs); info = self.dm.materials['resins'].get(nm,{})
                eew = info.get('eew',0)
                if rd['mode_var'].get() == T("fixed_mass"):
                    fixed_r_mass += v
                    if eew > 0: fixed_r_eq += v/eew
                    mats.append({"orig_cat":"resins","name":nm,"mass":v,"cl_ppm":info.get('cl',0),
                                 "type":info.get('type',''),"is_base":True,"eq_val":str(eew) if eew else "",
                                 "formula":T("formula_direct")+" "+str(v)+"g","cat_disp":T("cat_resins"),"_sort_cat":"Resin"})
                else:
                    ratio_r.append({"orig_cat":"resins","name":nm,"parts":v,"eew":eew,"cl_ppm":info.get('cl',0),
                                    "type":info.get('type',''),"eq_val":str(eew) if eew else "","cat_disp":T("cat_resins"),"_sort_cat":"Resin"})
                    total_r_parts += v

            others_mats = []
            for cat in ['additives','fillers','catalysts']:
                for rd in self.calc_rows[cat]:
                    nm = rd['cb'].get().split("  [")[0]; vs = rd['entry'].get()
                    if not nm or not vs: continue
                    val = float(vs); info = self.dm.materials.get(cat,{}).get(nm,{})
                    others_mats.append({"orig_cat":cat,"name":nm,"input_val":val,"cl_ppm":info.get('cl',0),
                                        "type":info.get('type',''),"is_base":False,"eq_val":"",
                                        "cat_disp":get_mat_cat_display(cat),"_sort_cat":cat.capitalize()})

            for mc in _custom_mat_cats:
                ckey = mc['key']
                for rd in self.calc_rows.get(ckey, []):
                    nm = rd['cb'].get().split("  [")[0]; vs = rd['entry'].get()
                    if not nm or not vs: continue
                    val = float(vs); info = self.dm.materials.get(ckey,{}).get(nm,{})
                    cl = info.get('cl',0); cat_d = get_mat_cat_display(ckey)
                    if mc.get('has_eew'):
                        eew = info.get('eew',0)
                        if eew > 0: fixed_r_eq += val/eew
                        fixed_r_mass += val
                        mats.append({"orig_cat":ckey,"name":nm,"mass":val,"cl_ppm":cl,"type":info.get('type',''),
                                     "is_base":True,"eq_val":str(eew) if eew else "","formula":T("formula_direct")+" "+str(val)+"g","cat_disp":cat_d,"_sort_cat":cat_d})
                    else:
                        others_mats.append({"orig_cat":ckey,"name":nm,"input_val":val,"cl_ppm":cl,"type":info.get('type',''),
                                            "is_base":False,"eq_val":"","cat_disp":cat_d,"_sort_cat":cat_d})

            h_cfgs = []; total_hr = 0.0
            hc = len(self.calc_rows['hardeners'])
            for rd in self.calc_rows['hardeners']:
                nm = rd['cb'].get().split("  [")[0]
                if not nm: continue
                ir = float(rd['eq_ratio'].get() or (100 if hc==1 else 0))
                corr = float(rd['corr'].get() or 100)/100.0
                info = self.dm.materials['hardeners'].get(nm,{})
                aeq = self.dm.get_active_eq(info)
                h_cfgs.append({"name":nm,"input_val":ir,"corr":corr,"eq":aeq,"cl_ppm":info.get('cl',0),
                               "corr_pct":float(rd['corr'].get() or 100),"type":info.get('type',''),
                               "eq_val":str(aeq),"cat_disp":T("cat_hardeners")})
                total_hr += ir

            if not ratio_r:
                for h in h_cfgs:
                    hm = 0; formula = ""
                    if mode in ["stoich","target_100"] and total_hr > 0:
                        ratio_s = f"{h['input_val']:.0f}/{total_hr:.0f}"
                        hm = (fixed_r_eq*(h['input_val']/total_hr))*h['eq']*h['corr']
                        formula = f"Eq({fixed_r_eq:.4f})×{ratio_s}×AHEW({h['eq']})×C({h['corr']:.2f})={hm:.4f}g"
                    elif mode == "weight":
                        hm = fixed_r_mass*(h['input_val']/100.0)*h['corr']
                        formula = f"R({fixed_r_mass:.2f}g)×{h['input_val']:.1f}%×C({h['corr']:.2f})={hm:.4f}g"
                    elif mode == "phr_100" and total_hr > 0:
                        ratio_s = f"{h['input_val']:.0f}/{total_hr:.0f}"
                        hm = (fixed_r_eq*(h['input_val']/total_hr))*h['eq']*h['corr']
                        formula = f"Eq({fixed_r_eq:.4f})×{ratio_s}×AHEW({h['eq']})×C({h['corr']:.2f})={hm:.4f}g"
                    mats.append({"orig_cat":"hardeners","name":h['name'],"mass":hm,"cl_ppm":h['cl_ppm'],
                                 "type":h['type'],"corr_pct":h['corr_pct'],"is_base":True,
                                 "eq_val":h['eq_val'],"formula":formula,"cat_disp":h['cat_disp'],"_sort_cat":"Hardener"})

                if mode == "phr_100":
                    resin_total = sum(m['mass'] for m in mats if m['orig_cat'] == 'resins')
                    if resin_total <= 0: raise ValueError(T("err_over_100g"))
                    sf = 100.0 / resin_total
                    scaled_r_eq = 0.0
                    for m in mats:
                        if m['orig_cat'] == 'resins':
                            orig = m['mass']; m['mass'] *= sf
                            info = self.dm.materials.get('resins',{}).get(m['name'],{})
                            eew = info.get('eew',0)
                            if eew > 0: scaled_r_eq += m['mass'] / eew
                            parts = orig
                            m['formula'] = T("formula_phr_resin").format(parts=parts, mass=m['mass'])
                    for m in mats:
                        if m['orig_cat'] == 'hardeners':
                            h_cfg = next((h for h in h_cfgs if h['name'] == m['name']), None)
                            if h_cfg and total_hr > 0:
                                ratio_s = f"{h_cfg['input_val']:.0f}/{total_hr:.0f}"
                                hm = (scaled_r_eq * (h_cfg['input_val']/total_hr)) * h_cfg['eq'] * h_cfg['corr']
                                m['mass'] = hm
                                m['formula'] = T("formula_phr_hardener").format(
                                    ratio=ratio_s, eq=h_cfg['eq'], corr=f"{h_cfg['corr']:.2f}", mass=hm)
                    rh_base = sum(m['mass'] for m in mats if m.get('is_base'))
                    for om in others_mats:
                        pct_val = om['input_val']
                        om['mass'] = rh_base * pct_val / 100.0
                        om['formula'] = T("formula_phr_extra").format(base=rh_base, pct=pct_val, mass=om['mass'])
                        om["_sort_cat"] = om["orig_cat"].capitalize()
                        mats.append({**om})

                elif mode == "target_100":
                    base = sum(m['mass'] for m in mats if m.get('is_base'))
                    if base <= 0: raise ValueError(T("err_over_100g"))
                    sc = 100.0 / base
                    for m in mats:
                        if m.get('is_base'):
                            orig = m['mass']; m['mass'] *= sc
                            m['formula'] = f"{orig:.4f}g×SF({sc:.4f})={m['mass']:.4f}g"
                    for om in others_mats:
                        om['mass'] = om['input_val']
                        om['formula'] = T("formula_t100_extra").format(val=om['input_val']); om["_sort_cat"]=om["orig_cat"].capitalize()
                        mats.append({**om})
                else:
                    for om in others_mats:
                        om['mass'] = om['input_val']
                        om['formula'] = T("formula_direct")+" "+str(om['input_val'])+"g"; om["_sort_cat"]=om["orig_cat"].capitalize()
                        mats.append({**om})
            else:
                if mode not in ("target_100", "phr_100"): raise ValueError(T("err_ratio_not_100g"))

                if mode == "phr_100":
                    remaining = 100.0 - fixed_r_mass
                    if remaining <= 0 or total_r_parts <= 0: raise ValueError(T("err_over_100g"))
                    u = remaining / total_r_parts
                    scaled_r_eq = fixed_r_eq
                    for r in ratio_r:
                        rm = u * r['parts']
                        if r['eew'] > 0: scaled_r_eq += rm / r['eew']
                        mats.append({"orig_cat":"resins","name":r['name'],"mass":rm,"cl_ppm":r['cl_ppm'],
                                     "type":r['type'],"is_base":True,"eq_val":r['eq_val'],
                                     "formula":T("formula_phr_resin").format(parts=r['parts'], mass=rm),
                                     "cat_disp":r['cat_disp'],"_sort_cat":"Resin"})
                    for h in h_cfgs:
                        if total_hr > 0:
                            ratio_s = f"{h['input_val']:.0f}/{total_hr:.0f}"
                            hm = (scaled_r_eq * (h['input_val']/total_hr)) * h['eq'] * h['corr']
                        else: hm = 0; ratio_s = "0"
                        mats.append({"orig_cat":"hardeners","name":h['name'],"mass":hm,"cl_ppm":h['cl_ppm'],
                                     "type":h['type'],"corr_pct":h.get('corr_pct',100),"is_base":True,
                                     "_sort_cat":"Hardener","eq_val":h['eq_val'],
                                     "formula":T("formula_phr_hardener").format(ratio=ratio_s, eq=h['eq'], corr=f"{h['corr']:.2f}", mass=hm),
                                     "cat_disp":h['cat_disp']})
                    rh_base = sum(m['mass'] for m in mats if m.get('is_base'))
                    for om in others_mats:
                        pct_val = om['input_val']
                        om['mass'] = rh_base * pct_val / 100.0
                        om['formula'] = T("formula_phr_extra").format(base=rh_base, pct=pct_val, mass=om['mass'])
                        om["_sort_cat"] = om["orig_cat"].capitalize()
                        mats.append({**om})

                else:
                    A = total_r_parts; B = C = 0.0
                    veq = sum(r['parts']/r['eew'] for r in ratio_r if r['eew']>0)
                    for h in h_cfgs:
                        if total_hr > 0:
                            sh = h['input_val']/total_hr
                            B += veq*sh*h['eq']*h['corr']; C += fixed_r_eq*sh*h['eq']*h['corr']
                    cf_ = fixed_r_mass + C; vc = A + B
                    if vc == 0: raise ValueError(T("err_coeff_zero"))
                    u = (100.0-cf_)/vc
                    if u < 0: raise ValueError(T("err_over_100g"))
                    tfe = fixed_r_eq + u*veq
                    for r in ratio_r:
                        rm = u*r['parts']
                        mats.append({"orig_cat":"resins","name":r['name'],"mass":rm,"cl_ppm":r['cl_ppm'],
                                     "type":r['type'],"is_base":True,"eq_val":r['eq_val'],
                                     "formula":f"u({u:.4f})×{r['parts']}parts={rm:.4f}g","cat_disp":r['cat_disp'],"_sort_cat":"Resin"})
                    for h in h_cfgs:
                        hm = (tfe*(h['input_val']/total_hr)*h['eq']*h['corr']) if total_hr>0 else 0
                        mats.append({"orig_cat":"hardeners","name":h['name'],"mass":hm,"cl_ppm":h['cl_ppm'],
                                     "type":h['type'],"corr_pct":h['corr_pct'],"is_base":True,
                                     "_sort_cat":"Hardener","eq_val":h['eq_val'],"formula":f"Eq({tfe:.4f})×({h['input_val']}/{total_hr})×{h['eq']}×{h['corr']:.2f}={hm:.4f}g","cat_disp":h['cat_disp']})
                    for om in others_mats:
                        om['mass'] = om['input_val']
                        om['formula'] = T("formula_t100_extra").format(val=om['input_val']); om["_sort_cat"]=om["orig_cat"].capitalize()
                        mats.append({**om})

            sp = {'Resin':2,'Hardener':3,'Additives':4,'Fillers':5,'Catalysts':6}
            for ii, mc in enumerate(_custom_mat_cats): sp[get_mat_cat_display(mc['key'])] = 6 + ii
            mats.sort(key=lambda m: sp.get(m.get('_sort_cat',''),99))

            opt = self.round_opt.get()
            pl = {T("round_int"):0,T("round_1dp"):1,T("round_2dp"):2}.get(opt, None)
            rt = 0.0; base_mass = 0.0
            for m in mats:
                m['rounded_mass'] = round(m['mass'], pl) if pl is not None else m['mass']
                rt += m['rounded_mass']
                if m.get('is_base'): base_mass += m['rounded_mass']
            for m in mats:
                m['pct'] = (m['rounded_mass']/rt*100.0) if rt > 0 else 0
                m['phr'] = (m['rounded_mass']/base_mass*100.0) if base_mass > 0 else 0

            try: bscale = max(0, float(self.batch_scale_var.get() or 100)) / 100.0
            except Exception: bscale = 1.0

            fcl = (sum(m['rounded_mass']*(m['cl_ppm']/1e6) for m in mats)/rt*1e6) if rt > 0 else 0
            
            total_cost = 0.0; cost_incomplete = False
            for m in mats:
                mat_info = self.dm.materials.get(m['orig_cat'], {}).get(m['name'], {})
                cpk = mat_info.get('cost_per_kg', '')
                try:
                    cpk_f = float(cpk)
                    m['cost'] = m['rounded_mass'] * cpk_f / 1000.0
                    total_cost += m['cost']
                except (ValueError, TypeError):
                    m['cost'] = None
                    if m['rounded_mass'] > 0: cost_incomplete = True

            fmt = f"{{:.{pl}f}}" if pl is not None else "{:.2f}"
            for m in mats:
                sm = m['rounded_mass'] * bscale
                self.tree.insert("","end", values=(m['name'], fmt.format(m['rounded_mass']),
                    fmt.format(sm), f"{m['phr']:.2f}", f"{m['pct']:.2f}", m.get('eq_val',''),
                    f"{m['cl_ppm']:.0f}"), tags=(m['orig_cat'],'item'))
            self.tree.insert("","end", values=("---","---","---","---","---","---","---"), tags=('divider',))
            self.tree.insert("","end", values=(T("total"), fmt.format(rt), fmt.format(rt*bscale),
                f"{rt/base_mass*100:.2f}" if base_mass>0 else "—", "100.00", "", f"{fcl:.0f}"), tags=('total',))
            
            if total_cost > 0:
                cost_per_g = total_cost / rt * 1000 if rt > 0 else 0
                cost_label = f"{T('cost_summary')}: ${total_cost:.4f} ({T('cost_per_kg_unit')} {cost_per_g:.2f})"
                if cost_incomplete: cost_label += f"  {T('cost_incomplete')}"
                self.tree.insert("","end", values=(cost_label,"","","","","",""), tags=('cost_info',))
            self.tree.tag_configure('cost_info', font=(_FONT_FAMILY, 9), foreground=_C.TEXT_TER)

            self._last_mats = mats; self._last_total = rt; self._last_cl = fcl
            self._last_base_mass = base_mass
            self._last_mode = self._mode_map().get(self.calc_mode.get(),"stoich")
        except Exception as e: messagebox.showerror(T("error"), str(e))

    def _copy(self):
        if not hasattr(self,'_last_mats') or not self._last_mats:
            messagebox.showwarning(T("hint"),T("warn_calc_first")); return
        export_mats = []
        for m in self._last_mats:
            export_mats.append({"name":m['name'], "category":m.get('cat_disp',''), "calc_mass":m['rounded_mass'],
                                "phr":m['phr'], "pct":m['pct'], "cl_ppm":m['cl_ppm'],
                                "eq_val":m.get('eq_val',''), "type":m.get('type',''), "formula":m.get('formula','')})
        ExportPreviewDialog(self.frame.winfo_toplevel(), export_mats, self._last_base_mass,
                            self._last_total, self._last_cl, self.app,
                            raw_mats=self._last_mats, dm=self.dm)

    def _save(self):
        if not hasattr(self,'_last_mats') or not self._last_mats:
            messagebox.showwarning(T("hint"),T("warn_calc_first")); return
        top = ctk.CTkToplevel(self.frame.winfo_toplevel())
        top.title(T("dlg_save_recipe")); top.geometry("380x180"); top.resizable(False, False); top.grab_set()
        ctk.CTkLabel(top, text=T("recipe_name_label"), font=self.fb).grid(row=0, column=0, padx=10, pady=(15,5), sticky='e')
        e_name = ctk.CTkEntry(top, width=200, corner_radius=6, border_width=1, border_color=_C.BORDER); e_name.grid(row=0, column=1, padx=10, pady=(15,5))
        ctk.CTkLabel(top, text=T("batch_no_label"), font=self.fb).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        e_batch = ctk.CTkEntry(top, width=200, corner_radius=6, border_width=1, border_color=_C.BORDER); e_batch.grid(row=1, column=1, padx=10, pady=5)
        def do_save():
            name = e_name.get().strip()
            if not name: messagebox.showwarning(T("hint"),T("warn_enter_name"), parent=top); return
            row = self.dm.build_recipe_row(name, e_batch.get().strip(), self._last_mode, self._last_mats, self._last_total, self._last_cl)
            self.dm.save_new_recipe(row)
            top.destroy(); messagebox.showinfo(T("ok"), T("save_ok"))
        ctk.CTkButton(top, text=T("btn_confirm_save"), fg_color=self.app.current_accent, command=do_save, corner_radius=8).grid(row=2, column=0, columnspan=2, pady=15)

    def _open_tools(self):
        _open_tools_dialog(self.frame, self.dm, self.app, self.fs, self.fb,
                           getattr(self, '_last_mats', None))

class TwoKCalcTab:
    def __init__(self, parent_frame, dm: DataManager, font_std, font_bold, app_instance):
        self.dm = dm; self.fs = font_std; self.fb = font_bold
        self.app = app_instance
        self.frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.frame.pack(fill='both', expand=True)
        
        self.calc_rows = {'2k_a_resins':[], '2k_a_others':[], '2k_b_hardeners':[], '2k_b_others':[]}
        self._build()

    def _build(self):
        self.paned = tk.PanedWindow(self.frame, orient=tk.HORIZONTAL, sashwidth=4, showhandle=False,
                                     sashrelief='flat', bg=_C.SASH, bd=0)
        self.paned.pack(fill='both', expand=True, pady=5)

        left_tk = tk.Frame(self.paned, bg='#f5f5f7')
        self.sf = ctk.CTkScrollableFrame(left_tk, corner_radius=8)
        self.sf.pack(fill="both", expand=True)
        self.paned.add(left_tk, minsize=250, width=600)

        fa = ctk.CTkFrame(self.sf, corner_radius=8, fg_color=_C.CARD_A, border_width=1, border_color=_C.BORDER)
        if ctk.get_appearance_mode() == "Dark": fa.configure(fg_color="#2b2b2b")
        fa.pack(fill='x', pady=5, padx=5)
        ctk.CTkLabel(fa, text="[ Part A ]", font=self.fb, text_color=self.app.current_accent).pack(anchor='w', padx=10, pady=(5,0))
        
        self.box_a_resins = ctk.CTkFrame(fa, fg_color="transparent")
        self.box_a_resins.pack(fill='x', padx=5, pady=2)
        self.btn_a_resin = ctk.CTkButton(fa, text=T("2k_add_resin"), fg_color="transparent", text_color=self.app.current_accent, border_width=1, border_color=self.app.current_accent, hover_color=_C.BTN_ADD_HV, command=lambda: self.add_row('2k_a_resins', self.box_a_resins), corner_radius=8)
        self.btn_a_resin.pack(anchor='w', padx=10, pady=(0, 5))

        self.box_a_others = ctk.CTkFrame(fa, fg_color="transparent")
        self.box_a_others.pack(fill='x', padx=5, pady=2)
        self.btn_a_other = ctk.CTkButton(fa, text=T("2k_add_a_other"), fg_color="transparent", text_color=self.app.current_accent, border_width=1, border_color=self.app.current_accent, hover_color=_C.BTN_ADD_HV, command=lambda: self.add_row('2k_a_others', self.box_a_others), corner_radius=8)
        self.btn_a_other.pack(anchor='w', padx=10, pady=(0, 10))

        fb = ctk.CTkFrame(self.sf, corner_radius=8, fg_color=_C.CARD_B, border_width=1, border_color=_C.BORDER)
        if ctk.get_appearance_mode() == "Dark": fb.configure(fg_color="#332a2e")
        fb.pack(fill='x', pady=5, padx=5)
        ctk.CTkLabel(fb, text="[ Part B ]", font=self.fb, text_color=_C.PINK).pack(anchor='w', padx=10, pady=(5,0))

        self.box_b_hardeners = ctk.CTkFrame(fb, fg_color="transparent")
        self.box_b_hardeners.pack(fill='x', padx=5, pady=2)
        self.btn_b_hardener = ctk.CTkButton(fb, text=T("2k_add_hardener"), fg_color="transparent", text_color=self.app.current_accent, border_width=1, border_color=self.app.current_accent, hover_color=_C.BTN_ADD_HV, command=lambda: self.add_row('2k_b_hardeners', self.box_b_hardeners), corner_radius=8)
        self.btn_b_hardener.pack(anchor='w', padx=10, pady=(0, 5))

        self.box_b_others = ctk.CTkFrame(fb, fg_color="transparent")
        self.box_b_others.pack(fill='x', padx=5, pady=2)
        self.btn_b_other = ctk.CTkButton(fb, text=T("2k_add_b_other"), fg_color="transparent", text_color=self.app.current_accent, border_width=1, border_color=self.app.current_accent, hover_color=_C.BTN_ADD_HV, command=lambda: self.add_row('2k_b_others', self.box_b_others), corner_radius=8)
        self.btn_b_other.pack(anchor='w', padx=10, pady=(0, 10))

        right_tk = tk.Frame(self.paned, bg='#f5f5f7')
        self.paned.add(right_tk, minsize=200)
        ra = ctk.CTkScrollableFrame(right_tk, corner_radius=8)
        ra.pack(fill='both', expand=True)
        
        cf = ctk.CTkFrame(ra, corner_radius=8, border_width=1, border_color=_C.BORDER)
        cf.pack(fill='x', padx=10, pady=10)
        ctk.CTkLabel(cf, text=T("2k_settings"), font=self.fb).pack(anchor='w', padx=10, pady=(5,0))

        row0 = ctk.CTkFrame(cf, fg_color="transparent")
        row0.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(row0, text=T("2k_mode"), font=self.fs).pack(side='left')
        self.mode_2k = tk.StringVar(value=T("2k_mode_ratio"))
        self.mode_2k_cb = AppleDropdown(row0, variable=self.mode_2k, width=240, font=self.fs, corner_radius=8, fg_color=self.app.current_accent, button_color=self.app.current_accent,
                          values=[T("2k_mode_free"), T("2k_mode_ratio")],
                          command=self._on_2k_mode_change)
        self.mode_2k_cb.pack(side='left', padx=5)

        row1 = ctk.CTkFrame(cf, fg_color="transparent")
        row1.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(row1, text=T("2k_global_stoich"), font=self.fs).pack(side='left')
        self.stoich_var = ctk.CTkEntry(row1, width=60, corner_radius=6, border_width=1, border_color=_C.BORDER)
        self.stoich_var.insert(0, "100")
        self.stoich_var.pack(side='left', padx=5)

        self.row_ratio = ctk.CTkFrame(cf, fg_color="transparent")
        self.row_ratio.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(self.row_ratio, text=T("2k_target_ratio"), font=self.fs).pack(side='left')
        ctk.CTkLabel(self.row_ratio, text="A:", font=self.fs, text_color="gray").pack(side='left', padx=(8,0))
        self.ratio_a_entry = ctk.CTkEntry(self.row_ratio, width=70, corner_radius=6, border_width=1, border_color=_C.BORDER, placeholder_text="100")
        self.ratio_a_entry.pack(side='left', padx=2)
        ctk.CTkLabel(self.row_ratio, text=":", font=self.fb).pack(side='left', padx=4)
        ctk.CTkLabel(self.row_ratio, text="B:", font=self.fs, text_color="gray").pack(side='left')
        self.ratio_b_entry = ctk.CTkEntry(self.row_ratio, width=70, corner_radius=6, border_width=1, border_color=_C.BORDER, placeholder_text="50")
        self.ratio_b_entry.pack(side='left', padx=2)

        row_cat = ctk.CTkFrame(cf, fg_color="transparent")
        row_cat.pack(fill='x', padx=10, pady=2)
        ctk.CTkLabel(row_cat, text=T("tool_cat_coeff"), font=self.fs).pack(side='left')
        self.cat_homo_var = ctk.CTkEntry(row_cat, width=60, corner_radius=6, border_width=1, border_color=_C.BORDER)
        self.cat_homo_var.insert(0, "0")
        self.cat_homo_var.pack(side='left', padx=5)
        ctk.CTkLabel(row_cat, text=T("tool_cat_coeff_hint"), font=ctk.CTkFont(family=_FONT_FAMILY, size=9),
                     text_color=_C.TEXT_SEC, wraplength=300).pack(side='left', padx=5)

        self.btn_calc = ctk.CTkButton(cf, text=T("2k_btn_calc"), font=self.fb, fg_color=self.app.current_accent, command=self.calculate, corner_radius=8)
        self.btn_calc.pack(fill='x', padx=10, pady=(5, 10))

        self.lbl_summary = ctk.CTkLabel(ra, text=T("2k_summary"), font=self.fb, justify="left")
        self.lbl_summary.pack(anchor='w', padx=10, pady=5)

        tf = RoundedTreeFrame(ra)
        tf.pack(fill="x", padx=10, pady=(0,5))
        cols = [("side",T("2k_col_side"),60),("cat",T("2k_col_cat"),90),("name",T("2k_col_name"),150),
                ("mass",T("2k_col_mass"),70),("eq",T("2k_col_eq"),70),("phr",T("2k_col_phr"),60),
                ("pct_side",T("2k_col_pct_side"),60),("pct_total",T("2k_col_pct_total"),60),("cl",T("2k_col_cl"),70)]
        self.tree = ttk.Treeview(tf.inner, columns=[c[0] for c in cols], show='headings', height=8)
        for cid, hdr, w in cols: self.tree.heading(cid, text=hdr); self.tree.column(cid, width=w, anchor='center')
        vsbt = ttk.Scrollbar(tf.inner, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsbt.set)
        self.tree.pack(side='left', fill='both', expand=True); vsbt.pack(side='right', fill='y')
        
        self.tree.tag_configure('subtotal', font=(_FONT_FAMILY, 10, "bold"), background=_C.SUBTOTAL)
        self.tree.tag_configure('total', font=(_FONT_FAMILY, 11, "bold"), background=_C.BG_LIGHT)
        self.tree.tag_configure('Part A', background=_C.CARD_A)
        self.tree.tag_configure('Part B', background=_C.CARD_B)

        bf = ctk.CTkFrame(ra, fg_color="transparent")
        bf.pack(fill='x', padx=10, pady=10)
        ctk.CTkButton(bf, text=T("2k_copy_excel"), fg_color=_C.GREEN, hover_color=_C.GREEN_HV, corner_radius=8, command=self._copy).pack(side='left', fill='x', expand=True, padx=(0,5))
        self.btn_save = ctk.CTkButton(bf, text=T("2k_save_recipe"), fg_color=self.app.current_accent, command=self._save, corner_radius=8)
        self.btn_save.pack(side='left', fill='x', expand=True, padx=(5,5))
        self.btn_tools = ctk.CTkButton(bf, text=T("btn_tools"), fg_color=_C.BTN_LIGHT, text_color=_C.TEXT, hover_color=_C.BTN_HOVER, corner_radius=8, command=self._open_tools, width=80)
        self.btn_tools.pack(side='left', padx=(5,0))

        self.add_row('2k_a_resins', self.box_a_resins)
        self.add_row('2k_a_others', self.box_a_others)
        self.add_row('2k_b_hardeners', self.box_b_hardeners)
        self.add_row('2k_b_others', self.box_b_others)

    def update_accent_color(self, hex_color):
        self.btn_a_resin.configure(text_color=hex_color, border_color=hex_color)
        self.btn_a_other.configure(text_color=hex_color, border_color=hex_color)
        self.btn_b_hardener.configure(text_color=hex_color, border_color=hex_color)
        self.btn_b_other.configure(text_color=hex_color, border_color=hex_color)
        self.btn_calc.configure(fg_color=hex_color)
        self.btn_save.configure(fg_color=hex_color)
        self.mode_2k_cb.configure(fg_color=hex_color, button_color=hex_color)
        
    def _is_free_mode(self):
        return self.mode_2k.get() == T("2k_mode_free")

    def _on_2k_mode_change(self, _=None):
        if self._is_free_mode():
            self.row_ratio.pack_forget()
            self.ratio_a_entry.delete(0, "end"); self.ratio_b_entry.delete(0, "end")
        else:
            self.row_ratio.pack(fill='x', padx=10, pady=5)
        for rd in list(self.calc_rows['2k_b_hardeners']):
            rd['frame'].destroy()
        self.calc_rows['2k_b_hardeners'] = []
        self.add_row('2k_b_hardeners', self.box_b_hardeners)

    def add_row(self, cat, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill='x', pady=2)
        
        cb = ctk.CTkEntry(row, width=200, corner_radius=6, border_width=1, border_color=_C.BORDER, font=ctk.CTkFont(family=_FONT_FAMILY, size=11),
                           placeholder_text=T("search_placeholder"))
        cb.pack(side='left')
        cb.bind('<KeyRelease>', lambda e: self._filter(e, cb, cat))
        cb.bind('<FocusOut>',   lambda e: cb.after(200, self._ac_close))
        ctk.CTkButton(row, text="▾", width=26, height=26, corner_radius=6,
                       fg_color=_C.BTN_LIGHT, text_color=_C.TEXT_SEC, hover_color=_C.BTN_HOVER,
                       command=lambda: self._show_all(None, cb, cat)).pack(side='left', padx=(2,0))
        
        ctk.CTkButton(row, text="↺", width=26, height=26, corner_radius=6,
                       fg_color=_C.BTN_LIGHT, text_color=_C.TEXT_SEC, hover_color=_C.BTN_HOVER,
                       command=lambda: self._clear_cb(cb, cat)).pack(side='left', padx=(4,0))
        
        rd = {"frame": row, "cb": cb}

        def _2k_tooltip(_cb=cb, _cat=cat):
            raw = _cb.get(); nm = raw.split("  [")[0].strip()
            if not nm: return ""
            for rc in self._get_cats_for_2k(_cat):
                if nm in self.dm.materials.get(rc, {}):
                    return _build_mat_tooltip(self.dm, rc, nm)
            return ""
        rd["tooltip"] = ToolTip(cb, _2k_tooltip)

        if cat in ('2k_a_resins', '2k_a_others', '2k_b_others'):
            ent = ctk.CTkEntry(row, width=60, corner_radius=6, border_width=1, border_color=_C.BORDER)
            ent.pack(side='left', padx=5)
            ctk.CTkLabel(row, text="g" if self._is_free_mode() else "parts", font=self.fs).pack(side='left')
            rd["entry"] = ent
        elif cat == '2k_b_hardeners':
            if self._is_free_mode():
                ent = ctk.CTkEntry(row, width=60, corner_radius=6, border_width=1, border_color=_C.BORDER); ent.pack(side='left', padx=5)
                ctk.CTkLabel(row, text="g", font=self.fs).pack(side='left')
                rd["entry"] = ent
            else:
                eq = ctk.CTkEntry(row, width=50, corner_radius=6, border_width=1, border_color=_C.BORDER); eq.insert(0,"100"); eq.pack(side='left', padx=5)
                ctk.CTkLabel(row, text="%", font=self.fs).pack(side='left')
                corr = ctk.CTkEntry(row, width=50, corner_radius=6, border_width=1, border_color=_C.BORDER); corr.insert(0,"100"); corr.pack(side='left', padx=5)
                ctk.CTkLabel(row, text="% (C)", font=self.fs).pack(side='left')
                rd.update({"eq_ratio": eq, "corr": corr})
                ToolTip(eq, T("tooltip_eq_ratio"))
                ToolTip(corr, T("tooltip_corr_coeff"))

        ctk.CTkButton(row, text="✕", width=26, height=26, corner_radius=6, fg_color=_C.BTN_LIGHT, text_color=_C.TEXT_SEC, hover_color=_C.RED,
                      command=lambda: self._del_row(row, cat)).pack(side='right', padx=5)
        self.calc_rows[cat].append(rd)

    def _del_row(self, frame, cat):
        self._ac_close()
        frame.destroy()
        self.calc_rows[cat] = [r for r in self.calc_rows[cat] if r['frame'] != frame]

    def _get_cats_for_2k(self, cat2k):
        if cat2k == '2k_a_resins': return ['resins']
        if cat2k == '2k_b_hardeners': return ['hardeners']
        return list(SLOT_COUNTS.keys()) + [mc['key'] for mc in _custom_mat_cats]

    def _opts(self, cat):
        opts = []
        for rc in self._get_cats_for_2k(cat):
            for n, i in sorted(self.dm.materials.get(rc,{}).items()):
                opts.append(f"{n}  [{i.get('type','')}]  ({get_mat_cat_display(rc)})")
        return opts

    def _filter(self, e, cb, cat):
        if e.keysym in ['Escape','Return','Up']: self._ac_close(); return
        txt = cb.get().split("  [")[0].lower().strip()
        filtered = [o for o in self._opts(cat) if txt in o.lower()] if txt else self._opts(cat)
        if filtered and txt: self._ac_show(cb, filtered)
        else: self._ac_close()

    def _show_all(self, e, cb, cat): self._ac_close(); self._ac_show(cb, self._opts(cat))
    def _clear_cb(self, cb, cat): self._ac_close(); cb.delete(0, 'end'); cb.focus_set()

    def _ac_show(self, cb, items):
        if not hasattr(self, '_popup') or self._popup is None:
            self._popup = RoundedPopup(self.frame, self.app.current_accent)
        self._popup.accent = self.app.current_accent
        self._popup.show(cb, items, lambda: None)

    def _ac_select(self): pass

    def _ac_close(self):
        if hasattr(self, '_popup') and self._popup:
            self._popup.close()

    def calculate(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            mats_A = []; mats_B = []
            A_epoxy_eq = 0.0; A_base_mass = 0.0
            
            for rd in self.calc_rows['2k_a_resins']:
                nm = rd['cb'].get().split("  [")[0]; vs = rd['entry'].get()
                if not nm or not vs: continue
                v = float(vs); info = self.dm.materials.get('resins',{}).get(nm,{})
                eew = info.get('eew',0)
                if eew > 0: A_epoxy_eq += v/eew
                A_base_mass += v
                mats_A.append({"name":nm, "orig_cat":"resins", "cat_disp":T("cat_resins"), "parts":v, "cl_ppm":info.get('cl',0), "eq":eew, "is_base":True})
            
            if A_base_mass <= 0: raise ValueError(T("err_part_a_zero"))
            mixed_eew = A_base_mass / A_epoxy_eq if A_epoxy_eq > 0 else 0

            for rd in self.calc_rows['2k_a_others']:
                raw = rd['cb'].get(); nm = raw.split("  [")[0]; vs = rd['entry'].get()
                if not nm or not vs: continue
                v = float(vs)
                orig_cat = "additives"
                if ") " in raw:
                    cdisp = raw.split("  (")[-1].strip(")")
                    for k, cv in get_all_cat_cn().items():
                        if cv == cdisp or k == cdisp: orig_cat = k; break
                info = self.dm.materials.get(orig_cat,{}).get(nm,{})
                mats_A.append({"name":nm, "orig_cat":orig_cat, "cat_disp":get_mat_cat_display(orig_cat), "parts":v, "cl_ppm":info.get('cl',0), "eq":"-", "is_base":False})

            is_free = self._is_free_mode()
            st_val = float(self.stoich_var.get() or 100) / 100.0
            try: cat_homo = max(0, min(0.5, float(self.cat_homo_var.get() or 0)))
            except Exception: cat_homo = 0
            eff_epoxy_eq = A_epoxy_eq * (1.0 - cat_homo)
            total_hr_parts = 0.0
            hc_count = len(self.calc_rows['2k_b_hardeners'])
            for rd in self.calc_rows['2k_b_hardeners']:
                nm = rd['cb'].get().split("  [")[0]
                if not nm: continue
                info = self.dm.materials.get('hardeners',{}).get(nm,{})
                aeq = self.dm.get_active_eq(info)
                if is_free:
                    vs = rd.get('entry')
                    if not vs: continue
                    hmass = float(vs.get() or 0)
                else:
                    ir = float(rd['eq_ratio'].get() or (100 if hc_count==1 else 0)) / 100.0
                    cr = float(rd['corr'].get() or 100) / 100.0
                    hmass = (eff_epoxy_eq * st_val * ir) * aeq * cr
                mats_B.append({"name":nm, "orig_cat":"hardeners", "cat_disp":T("cat_hardeners"), "parts":hmass, "cl_ppm":info.get('cl',0), "eq":aeq, "is_base":True})
                total_hr_parts += hmass

            for rd in self.calc_rows['2k_b_others']:
                raw = rd['cb'].get(); nm = raw.split("  [")[0]; vs = rd['entry'].get()
                if not nm or not vs: continue
                v = float(vs)
                orig_cat = "additives"
                if ") " in raw:
                    cdisp = raw.split("  (")[-1].strip(")")
                    for k, cv in get_all_cat_cn().items():
                        if cv == cdisp or k == cdisp: orig_cat = k; break
                info = self.dm.materials.get(orig_cat,{}).get(nm,{})
                mats_B.append({"name":nm, "orig_cat":orig_cat, "cat_disp":get_mat_cat_display(orig_cat), "parts":v, "cl_ppm":info.get('cl',0), "eq":"-", "is_base":False})

            sum_A = sum(m['parts'] for m in mats_A)
            sum_B = sum(m['parts'] for m in mats_B)
            tgt_mode = f"{self.ratio_a_entry.get().strip()}:{self.ratio_b_entry.get().strip()}" if self.ratio_a_entry.get().strip() and self.ratio_b_entry.get().strip() else ""
            
            sc_A = 1.0; sc_B = 1.0
            if tgt_mode and ':' in tgt_mode:
                ratio_str = tgt_mode.split()[0]
                ta, tb = map(float, ratio_str.split(':'))
                if sum_A > 0 and sum_B > 0:
                    sc_A = ta / sum_A; sc_B = tb / sum_B

            for m in mats_A: m['mass'] = m['parts'] * sc_A
            for m in mats_B: m['mass'] = m['parts'] * sc_B

            final_A = sum(m['mass'] for m in mats_A)
            final_B = sum(m['mass'] for m in mats_B)
            grand_total = final_A + final_B
            total_cl_mass = sum(m['mass']*(m['cl_ppm']/1e6) for m in mats_A+mats_B)
            mixed_cl = (total_cl_mass / grand_total * 1e6) if grand_total > 0 else 0

            self.tree.delete(*self.tree.get_children())
            
            def insert_side(side_name, mats, total_side):
                for m in mats:
                    pct_s = (m['mass']/total_side*100) if total_side>0 else 0
                    pct_t = (m['mass']/grand_total*100) if grand_total>0 else 0
                    phr_base = final_A if side_name=="Part B" else A_base_mass
                    phr = (m['mass']/phr_base*100) if phr_base>0 else 0
                    self.tree.insert("","end", values=(side_name, m['cat_disp'], m['name'], f"{m['mass']:.2f}",
                        m['eq'] if m['eq']!="-" else "-", f"{phr:.2f}", f"{pct_s:.2f}", f"{pct_t:.2f}", f"{m['cl_ppm']:.0f}"), tags=(side_name,))
                
                scl = sum(m['mass']*(m['cl_ppm']/1e6) for m in mats)/total_side*1e6 if total_side>0 else 0
                self.tree.insert("","end", values=("---", "---", T('2k_sub_a') if side_name=="Part A" else T('2k_sub_b'), 
                                                   f"{total_side:.2f}", "-", "-", "100.00", f"{total_side/grand_total*100:.2f}", f"{scl:.0f}"), tags=('subtotal', side_name))

            if mats_A: insert_side("Part A", mats_A, final_A)
            if mats_B: insert_side("Part B", mats_B, final_B)

            self.tree.insert("","end", values=("---","---","---","---","---","---","---","---","---"), tags=('divider',))
            self.tree.insert("","end", values=("A+B", "-", T("2k_grand_total"), f"{grand_total:.2f}", "-", "-", "-", "100.00", f"{mixed_cl:.0f}"), tags=('total',))

            ratio_w_b = (final_B/final_A*100) if final_A>0 else 0
            gcd_val = math.gcd(int(final_A), int(final_B)) if final_A.is_integer() and final_B.is_integer() else 1
            simp = f"{int(final_A/gcd_val)}:{int(final_B/gcd_val)}" if gcd_val>1 else f"100 : {ratio_w_b:.2f}"
            
            sum_text = f"{T('2k_mixed_eew')} {mixed_eew:.1f}   |   {T('2k_total_eq')} {A_epoxy_eq:.4f}\n"
            if cat_homo > 0:
                sum_text += f"Homo-poly: {cat_homo*100:.0f}%   →   Eff.Eq: {eff_epoxy_eq:.4f}\n"
            sum_text += f"{T('2k_total_a')} {final_A:.2f}g   |   {T('2k_total_b')} {final_B:.2f}g\n"
            sum_text += f"{T('2k_ratio_wt')} {final_A:.2f} : {final_B:.2f}   ({T('2k_ratio_simple')} {simp})\n"
            sum_text += f"{T('2k_total_mixed')} {grand_total:.2f}g   |   {T('2k_total_cl')} {mixed_cl:.0f} ppm"
            self.lbl_summary.configure(text=sum_text)

            self._last_mats_2k = mats_A + mats_B
            self._last_total_2k = grand_total
            self._last_cl_2k = mixed_cl
            self._last_meew = mixed_eew
            self._last_stoich = st_val * 100
            self._last_ratio_str = f"{final_A:.2f}:{final_B:.2f}"

        except Exception as e: messagebox.showerror(T("error"), str(e))

    def _open_tools(self):
        _open_tools_dialog(self.frame, self.dm, self.app, self.fs, self.fb,
                           getattr(self, '_last_mats_2k', None))

    def _copy(self):
        try:
            text = T("2k_copy_hdr") + "\n"
            for item in self.tree.get_children():
                vals = self.tree.item(item,"values")
                if vals[0] == "---": continue
                text += "\t".join(map(str,vals)) + "\n"
            self.frame.clipboard_clear(); self.frame.clipboard_append(text); self.frame.update()
            messagebox.showinfo(T("copy_ok_title"),T("copy_ok"))
        except Exception as e: messagebox.showerror(T("error"),str(e))

    def _save(self):
        if not hasattr(self,'_last_mats_2k') or not self._last_mats_2k:
            messagebox.showwarning(T("hint"),T("warn_calc_first")); return
        top = ctk.CTkToplevel(self.frame.winfo_toplevel())
        top.title(T("2k_save_recipe")); top.geometry("380x180"); top.resizable(False, False); top.grab_set()
        ctk.CTkLabel(top, text=T("recipe_name_label"), font=self.fb).grid(row=0, column=0, padx=10, pady=(15,5), sticky='e')
        e_name = ctk.CTkEntry(top, width=200, corner_radius=6, border_width=1, border_color=_C.BORDER); e_name.grid(row=0, column=1, padx=10, pady=(15,5))
        ctk.CTkLabel(top, text=T("batch_no_label"), font=self.fb).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        e_batch = ctk.CTkEntry(top, width=200, corner_radius=6, border_width=1, border_color=_C.BORDER); e_batch.grid(row=1, column=1, padx=10, pady=5)
        def do_save():
            name = e_name.get().strip()
            if not name: messagebox.showwarning(T("hint"),T("warn_enter_name"), parent=top); return
            mode_str = f"2K | MEEW:{self._last_meew:.1f} | St:{self._last_stoich:.0f}% | R:{self._last_ratio_str}"
            row = self.dm.build_recipe_row(name, e_batch.get().strip(), mode_str, self._last_mats_2k, self._last_total_2k, self._last_cl_2k)
            self.dm.save_new_recipe(row)
            top.destroy(); messagebox.showinfo(T("ok"), T("save_ok"))
        ctk.CTkButton(top, text=T("btn_confirm_save"), fg_color=self.app.current_accent, command=do_save, corner_radius=8).grid(row=2, column=0, columnspan=2, pady=15)

class DatabaseTab:
    def __init__(self, parent_frame, dm: DataManager, font_std, font_bold, app_instance, rebuild_cb=None):
        self.dm = dm; self.fs = font_std; self.fb = font_bold
        self.app = app_instance; self.rebuild_cb = rebuild_cb
        self.frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.frame.pack(fill='both', expand=True)
        self.current_sel = None
        self._build()

    def _build(self):
        lf = ctk.CTkFrame(self.frame, width=320, corner_radius=8)
        lf.pack(side="left", fill="y", padx=(0, 5), pady=5)
        lf.pack_propagate(False)

        top_lf = ctk.CTkFrame(lf, fg_color="transparent")
        top_lf.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(top_lf, text=T("search"), font=self.fb).pack(anchor='w')
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_tree)
        ctk.CTkEntry(top_lf, corner_radius=6, border_width=1, border_color=_C.BORDER, textvariable=self.search_var, placeholder_text=T("search_placeholder")).pack(fill='x', pady=(2, 10))

        ctk.CTkLabel(top_lf, text=T("cat_filter"), font=self.fb).pack(anchor='w')
        self.cat_var = tk.StringVar(value=T("all_cats"))
        cat_opts = [T("all_cats")] + list(get_all_cat_display().values())
        self.cat_cb = AppleDropdown(top_lf, variable=self.cat_var, values=cat_opts, command=self._filter_tree, font=self.fs, corner_radius=8, fg_color=self.app.current_accent, button_color=self.app.current_accent)
        self.cat_cb.pack(fill='x', pady=(2, 10))

        self.lbl_count = ctk.CTkLabel(top_lf, text=T("total_items", 0), font=self.fs, text_color="gray")
        self.lbl_count.pack(anchor='w')

        tree_f = RoundedTreeFrame(lf)
        tree_f.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.tree = ttk.Treeview(tree_f.inner, columns=("cat", "name"), show='headings', style="DbTree.Treeview")
        self.tree.heading("cat", text=T("lbl_category")); self.tree.column("cat", width=80, anchor='center')
        self.tree.heading("name", text=T("lbl_name")); self.tree.column("name", width=180, anchor='w')
        vsb = ttk.Scrollbar(tree_f.inner, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True); vsb.pack(side='right', fill='y')
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        self.rf = ctk.CTkScrollableFrame(self.frame, corner_radius=8)
        self.rf.pack(side="right", fill='both', expand=True, padx=(5,0), pady=5)
        
        hdr_f = ctk.CTkFrame(self.rf, fg_color="transparent")
        hdr_f.pack(fill='x', padx=10, pady=(10, 5))
        self.lbl_edit_title = ctk.CTkLabel(hdr_f, text=T("data_edit") + " " + T("not_selected"), font=self.fb, text_color=self.app.current_accent)
        self.lbl_edit_title.pack(side='left')
        
        btn_f = ctk.CTkFrame(hdr_f, fg_color="transparent")
        btn_f.pack(side='right')
        ctk.CTkButton(btn_f, text=T("btn_deselect"), width=80, fg_color=_C.BTN_LIGHT, text_color=_C.TEXT_SEC, corner_radius=8, command=self._clear_form).pack(side='left', padx=5)
        self.btn_col_mgr = ctk.CTkButton(btn_f, text=T("btn_col_manager"), width=100, fg_color=self.app.current_accent, command=self._open_col_manager)
        self.btn_col_mgr.pack(side='left', padx=5)

        self.form_f = ctk.CTkFrame(self.rf, fg_color="transparent")
        self.form_f.pack(fill='both', expand=True, padx=10, pady=5)
        self.entries = {}

        self._add_field("category", T("lbl_category"), is_combo=True, opts=list(get_all_cat_display().values()))
        self.entries['category'].configure(command=lambda v: self._update_form_vis())
        self._add_field("name", T("lbl_name"))
        self._add_field("type", T("lbl_type"))
        self._add_field("appearance", T("lbl_appearance"))
        self._add_field("viscosity", T("lbl_viscosity"))
        self._add_field("dk", T("lbl_dk"))
        self._add_field("surface_energy", T("lbl_surface_energy"))
        self._add_field("structure", T("lbl_structure"))
        self._add_field("source", T("lbl_source"))
        self._add_field("cl", T("lbl_cl"))
        self._add_field("cost_per_kg", T("lbl_cost_per_kg"))
        self._add_field("volatile_pct", T("lbl_volatile_pct"))
        self._add_field("tg_dsc", T("lbl_tg_dsc"))
        self._add_field("shelf_life", T("lbl_shelf_life"))
        self._add_field("storage_temp", T("lbl_storage_temp"))

        self.eq_f = ctk.CTkFrame(self.form_f, corner_radius=8, border_width=1, border_color=_C.BORDER)
        self.eq_f.pack(fill='x', pady=10, ipady=5)
        
        self.eew_f = ctk.CTkFrame(self.eq_f, fg_color="transparent")
        ctk.CTkLabel(self.eew_f, text=T("lbl_eew"), width=120, anchor='e', font=self.fs).pack(side='left', padx=5)
        self.entries['eew'] = ctk.CTkEntry(self.eew_f, width=200, corner_radius=6, border_width=1, border_color=_C.BORDER); self.entries['eew'].pack(side='left', padx=5)

        self.ahew_f = ctk.CTkFrame(self.eq_f, fg_color="transparent")
        ctk.CTkLabel(self.ahew_f, text=T("lbl_ahew"), width=120, anchor='e', font=self.fs).pack(side='left', padx=5)
        self.entries['ahew'] = ctk.CTkEntry(self.ahew_f, width=200, corner_radius=6, border_width=1, border_color=_C.BORDER); self.entries['ahew'].pack(side='left', padx=5)

        self.hsub_f = ctk.CTkFrame(self.eq_f, fg_color="transparent")
        ctk.CTkLabel(self.hsub_f, text=T("lbl_subtype"), width=120, anchor='e', font=self.fs).pack(side='left', padx=5)
        self.entries['h_subtype'] = AppleDropdown(self.hsub_f, width=200,
            values=[T("h_amine"), T("h_polyamide"), T("h_anhydride"), T("h_mercaptan"), T("h_hydroxyl")],
            font=ctk.CTkFont(family=_FONT_FAMILY, size=11), corner_radius=8,
            fg_color=self.app.current_accent, button_color=self.app.current_accent)
        self.entries['h_subtype'].pack(side='left', padx=5)

        self.calc_tools_f = ctk.CTkFrame(self.eq_f, fg_color="transparent")
        
        self.calc_widgets = {}
        for key in ['amine_value', 'f_factor', 'mw', 'func_group_num', 'acid_value', 'hydroxyl_value']:
            self.calc_widgets[key] = ctk.CTkEntry(self.calc_tools_f, width=80, corner_radius=6, border_width=1, border_color=_C.BORDER)

        self.filler_f = ctk.CTkFrame(self.eq_f, fg_color="transparent")
        filler_fields = [
            ("density", T("lbl_density")),
            ("particle_size", T("lbl_particle_size")),
            ("ssa", T("lbl_ssa")),
            ("oil_absorption", T("lbl_oil_absorption")),
            ("mohs", T("lbl_mohs")),
            ("refractive_index", T("lbl_refractive_index")),
            ("cte_ppm", T("lbl_cte_ppm")),
            ("thermal_cond", T("lbl_thermal_cond")),
            ("elec_resistivity", T("lbl_elec_resistivity")),
        ]
        for key, label in filler_fields:
            rf = ctk.CTkFrame(self.filler_f, fg_color="transparent")
            rf.pack(fill='x', pady=1)
            ctk.CTkLabel(rf, text=label, width=160, anchor='e', font=self.fs).pack(side='left', padx=5)
            ent = ctk.CTkEntry(rf, width=200, corner_radius=6, border_width=1, border_color=_C.BORDER); ent.pack(side='left', padx=5)
            self.entries[key] = ent
        rf_shape = ctk.CTkFrame(self.filler_f, fg_color="transparent")
        rf_shape.pack(fill='x', pady=1)
        ctk.CTkLabel(rf_shape, text=T("lbl_particle_shape"), width=160, anchor='e', font=self.fs).pack(side='left', padx=5)
        shape_vals = [T("shape_sphere"), T("shape_irregular"), T("shape_platelet"), T("shape_fiber"), T("shape_fumed")]
        self.entries['particle_shape'] = AppleDropdown(rf_shape, width=200, values=shape_vals,
            font=ctk.CTkFont(family=_FONT_FAMILY, size=11), corner_radius=8,
            fg_color=self.app.current_accent, button_color=self.app.current_accent)
        self.entries['particle_shape'].pack(side='left', padx=5)

        self.custom_f = ctk.CTkFrame(self.form_f, corner_radius=8, fg_color=_C.BG_LIGHT if ctk.get_appearance_mode()=="Light" else "#2b2b2b")
        self.custom_f.pack(fill='x', pady=10)
        ctk.CTkLabel(self.custom_f, text=T("custom_fields"), font=self.fb).pack(anchor='w', padx=10, pady=(5,0))
        self.custom_inner = ctk.CTkFrame(self.custom_f, fg_color="transparent")
        self.custom_inner.pack(fill='x', padx=10, pady=5)
        self._build_custom_fields()

        notes_f = ctk.CTkFrame(self.form_f, fg_color="transparent")
        notes_f.pack(fill='x', pady=5)
        ctk.CTkLabel(notes_f, text=T("lbl_notes"), width=120, anchor='ne', font=self.fs).pack(side='left', padx=5, anchor='n')
        self.entries['desc'] = ctk.CTkTextbox(notes_f, height=80, width=400, corner_radius=6, border_width=1, border_color=_C.BORDER)
        self.entries['desc'].pack(side='left', fill='x', expand=True, padx=5)

        bf = ctk.CTkFrame(self.rf, fg_color="transparent")
        bf.pack(fill='x', padx=10, pady=20)
        
        self.btn_del = ctk.CTkButton(bf, text=T("btn_delete_sel"), fg_color="transparent", text_color=_C.RED, border_width=1, border_color=_C.RED, hover_color=_C.RED, command=self._delete, corner_radius=8)
        self.btn_del.pack(side='left', padx=(0,10))
        
        self.btn_save = ctk.CTkButton(bf, text=T("btn_save"), fg_color=self.app.current_accent, font=self.fb, command=lambda: self._save(is_new=False), corner_radius=8)
        self.btn_save.pack(side='right', padx=(10,0))
        
        self.btn_save_new = ctk.CTkButton(bf, text=T("btn_save_as_new"), fg_color=self.app.current_accent, font=self.fb, command=lambda: self._save(is_new=True), corner_radius=8)
        self.btn_save_new.pack(side='right')

        self._refresh_tree()
        self._clear_form()

    def update_accent_color(self, hex_color):
        self.lbl_edit_title.configure(text_color=hex_color)
        self.btn_save.configure(fg_color=hex_color)
        self.btn_save_new.configure(fg_color=hex_color)
        self.btn_col_mgr.configure(fg_color=hex_color)
        self.cat_cb.configure(fg_color=hex_color, button_color=hex_color)
        cat_w = self.entries.get('category')
        if cat_w and isinstance(cat_w, (ctk.CTkOptionMenu, AppleDropdown)):
            cat_w.configure(fg_color=hex_color, button_color=hex_color)

    def _add_field(self, key, label_text, is_combo=False, opts=None):
        row = ctk.CTkFrame(self.form_f, fg_color="transparent")
        row.pack(fill='x', pady=3)
        ctk.CTkLabel(row, text=label_text, width=120, anchor='e', font=self.fs).pack(side='left', padx=5)
        if is_combo:
            cb = AppleDropdown(row, width=400, values=opts or [], font=self.fs, corner_radius=8, fg_color=self.app.current_accent, button_color=self.app.current_accent)
            cb.pack(side='left', fill='x', expand=True, padx=5)
            self.entries[key] = cb
        else:
            ent = ctk.CTkEntry(row, width=400, corner_radius=6, border_width=1, border_color=_C.BORDER)
            ent.pack(side='left', fill='x', expand=True, padx=5)
            self.entries[key] = ent

    def _build_custom_fields(self):
        for w in self.custom_inner.winfo_children(): w.destroy()
        custom_cols = self.dm.get_custom_mat_cols()
        if not custom_cols:
            ctk.CTkLabel(self.custom_inner, text=T("no_custom_fields"), text_color="gray", font=self.fs).pack(pady=5)
            return
        for col in custom_cols:
            row = ctk.CTkFrame(self.custom_inner, fg_color="transparent")
            row.pack(fill='x', pady=2)
            disp = col['display'] + (f" ({col['unit']})" if col.get('unit') else "") + ":"
            ctk.CTkLabel(row, text=disp, width=120, anchor='e', font=self.fs).pack(side='left', padx=5)
            ent = ctk.CTkEntry(row, width=400, corner_radius=6, border_width=1, border_color=_C.BORDER)
            ent.pack(side='left', fill='x', expand=True, padx=5)
            self.entries[col['data_key']] = ent

    def _refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.tree_data = []
        for internal_cat, items in self.dm.materials.items():
            disp_cat = get_mat_cat_display(internal_cat)
            for name in items.keys():
                self.tree_data.append((disp_cat, name, internal_cat))
        self.tree_data.sort(key=lambda x: (x[0], x[1]))
        self._filter_tree()

    def _filter_tree(self, *args):
        kw = self.search_var.get().lower()
        fc = self.cat_var.get()
        self.tree.delete(*self.tree.get_children())
        count = 0
        for disp_cat, name, internal_cat in self.tree_data:
            if fc != T("all_cats") and disp_cat != fc: continue
            if kw and kw not in name.lower() and kw not in disp_cat.lower(): continue
            self.tree.insert("", "end", values=(disp_cat, name), tags=(internal_cat,))
            count += 1
        self.lbl_count.configure(text=T("total_items", count))

    def _clear_form(self):
        self.current_sel = None
        self.lbl_edit_title.configure(text=T("data_edit") + " " + T("not_selected"))
        for k, w in self.entries.items():
            if isinstance(w, ctk.CTkEntry): w.delete(0, 'end')
            elif isinstance(w, ctk.CTkTextbox): w.delete("1.0", 'end')
            elif isinstance(w, (ctk.CTkOptionMenu, AppleDropdown)) and k != 'category': w.set('')
        self.btn_del.configure(state="disabled")
        self._update_form_vis()

    def _on_select(self, e):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0], 'values')
        tags = self.tree.item(sel[0], 'tags')
        if not vals or not tags: return
        
        disp_cat, name = vals[0], vals[1]
        internal_cat = tags[0]
        info = self.dm.materials.get(internal_cat, {}).get(name)
        if not info: return
        
        self._clear_form()
        self.current_sel = (internal_cat, name)
        self.lbl_edit_title.configure(text=T("editing") + name)
        self.btn_del.configure(state="normal")
        
        self.entries['category'].set(disp_cat)
        self.entries['name'].insert(0, name)
        
        for k in ['type', 'appearance', 'viscosity', 'dk', 'surface_energy', 'structure', 'source']:
            if k in self.entries: self.entries[k].insert(0, str(info.get(k, '')))
        
        if 'cl' in self.entries: self.entries['cl'].insert(0, str(info.get('cl', '')))
        for fk in ['cost_per_kg', 'volatile_pct', 'tg_dsc', 'shelf_life', 'storage_temp']:
            if fk in self.entries: self.entries[fk].insert(0, str(info.get(fk, '')))
        if 'eew' in self.entries and info.get('eew'): self.entries['eew'].insert(0, str(info.get('eew')))
        if 'ahew' in self.entries and info.get('ahew'): self.entries['ahew'].insert(0, str(info.get('ahew')))
        if 'h_subtype' in self.entries: self.entries['h_subtype'].set(_hsubtype_display(info.get('h_subtype', '')))
        
        for fk in ['density', 'particle_size', 'ssa', 'oil_absorption', 'mohs', 'refractive_index', 'cte_ppm', 'thermal_cond', 'elec_resistivity']:
            if fk in self.entries: self.entries[fk].insert(0, str(info.get(fk, '')))
        if 'particle_shape' in self.entries: self.entries['particle_shape'].set(str(info.get('particle_shape', '')))
        
        for col in self.dm.get_custom_mat_cols():
            dk = col['data_key']
            if dk in self.entries: self.entries[dk].insert(0, str(info.get(dk, '')))
            
        if 'desc' in self.entries: self.entries['desc'].insert("1.0", str(info.get('desc', '')))
        self._update_form_vis()

    def _on_hsub_change(self, e=None): pass 

    def _update_form_vis(self, e=None):
        cat_disp = self.entries['category'].get()
        internal_cat = None
        for k, v in get_all_cat_display().items():
            if v == cat_disp: internal_cat = k; break
            
        self.eew_f.pack_forget(); self.ahew_f.pack_forget(); self.hsub_f.pack_forget(); self.calc_tools_f.pack_forget(); self.filler_f.pack_forget()
        
        if internal_cat == 'resins':
            self.eew_f.pack(fill='x', pady=2)
        elif internal_cat == 'hardeners':
            self.ahew_f.pack(fill='x', pady=2)
            self.hsub_f.pack(fill='x', pady=2)
        elif internal_cat == 'fillers':
            self.filler_f.pack(fill='x', pady=2)
        else:
            mc = _get_custom_mat_cat(internal_cat)
            if mc and mc.get('has_eew'): self.eew_f.pack(fill='x', pady=2)

    def _save(self, is_new=False):
        cat_disp = self.entries['category'].get()
        name = self.entries['name'].get().strip()
        if not name: messagebox.showwarning(T("hint"), T("warn_name_empty")); return
        
        internal_cat = None
        for k, v in get_all_cat_display().items():
            if v == cat_disp: internal_cat = k; break
        if not internal_cat: return

        if not is_new and self.current_sel and self.current_sel != (internal_cat, name):
            old_c, old_n = self.current_sel
            if old_c in self.dm.materials and old_n in self.dm.materials[old_c]:
                del self.dm.materials[old_c][old_n]

        def get_float(k):
            try: return float(self.entries[k].get())
            except Exception: return 0.0

        def get_str(k):
            w = self.entries.get(k)
            if w is None: return ''
            try: return w.get().strip()
            except Exception: return ''

        info = {
            'type': self.entries['type'].get(), 'appearance': self.entries['appearance'].get(),
            'viscosity': self.entries['viscosity'].get(), 'dk': self.entries['dk'].get(),
            'surface_energy': self.entries['surface_energy'].get(), 'structure': self.entries['structure'].get(),
            'source': self.entries['source'].get(), 'cl': get_float('cl'),
            'desc': self.entries['desc'].get("1.0", "end").strip(),
            'cost_per_kg': get_str('cost_per_kg'), 'volatile_pct': get_str('volatile_pct'),
            'tg_dsc': get_str('tg_dsc'), 'shelf_life': get_str('shelf_life'),
            'storage_temp': get_str('storage_temp'),
        }
        
        if internal_cat == 'resins' or (_get_custom_mat_cat(internal_cat) or {}).get('has_eew'):
            info['eew'] = get_float('eew')
        elif internal_cat == 'hardeners':
            info['ahew'] = get_float('ahew')
            hsub_w = self.entries.get('h_subtype')
            info['h_subtype'] = _norm_hsubtype(hsub_w.get() if hsub_w else '')
        elif internal_cat == 'fillers':
            for fk in ['density', 'particle_size', 'ssa', 'oil_absorption', 'mohs', 'refractive_index', 'cte_ppm', 'thermal_cond', 'elec_resistivity']:
                if fk in self.entries: info[fk] = self.entries[fk].get()
            if 'particle_shape' in self.entries: info['particle_shape'] = self.entries['particle_shape'].get()

        for col in self.dm.get_custom_mat_cols():
            dk = col['data_key']
            if dk in self.entries: info[dk] = self.entries[dk].get()

        if internal_cat not in self.dm.materials: self.dm.materials[internal_cat] = {}
        self.dm.materials[internal_cat][name] = info
        self.dm.save_materials()
        
        self._refresh_tree()
        self._clear_form()
        messagebox.showinfo(T("ok"), T("saved_to_db"))

    def _delete(self):
        if not self.current_sel: return
        cat, name = self.current_sel
        if messagebox.askyesno(T("confirm"), T("confirm_del_mat", name)):
            if cat in self.dm.materials and name in self.dm.materials[cat]:
                del self.dm.materials[cat][name]
                self.dm.save_materials()
                self._refresh_tree()
                self._clear_form()

    def _open_col_manager(self):
        """Column manager: toggle visibility + add custom columns."""
        top = ctk.CTkToplevel(self.frame.winfo_toplevel())
        top.title(T("btn_col_manager")); top.geometry("420x550"); top.grab_set()
        ctk.CTkLabel(top, text=T("btn_col_manager"), font=self.fb).pack(pady=(10, 5))

        scroll = ctk.CTkScrollableFrame(top, corner_radius=8)
        scroll.pack(fill='both', expand=True, padx=10, pady=5)

        col_mgr_vars = {}
        for col in self.dm.mat_columns:
            var = tk.BooleanVar(value=col.get('visible', True))
            rf = ctk.CTkFrame(scroll, fg_color="transparent")
            rf.pack(fill='x', pady=2)
            cb = ctk.CTkCheckBox(rf, text=col.get('display', col.get('db_key', '')),
                                  variable=var, font=self.fs, corner_radius=4)
            cb.pack(side='left', padx=10)
            if not col.get('builtin', False):
                def _del(dk=col['db_key'], frame=rf):
                    self.dm.mat_columns = [c for c in self.dm.mat_columns if c['db_key'] != dk]
                    frame.destroy()
                ctk.CTkButton(rf, text="✕", width=26, height=26, corner_radius=6, fg_color=_C.BTN_LIGHT, text_color=_C.TEXT_SEC, hover_color=_C.RED,
                               command=_del).pack(side='right', padx=5)
            col_mgr_vars[col['db_key']] = var

        sep = ctk.CTkFrame(top, height=1, fg_color=_C.BORDER)
        sep.pack(fill='x', padx=10, pady=6)
        add_f = ctk.CTkFrame(top, fg_color="transparent")
        add_f.pack(fill='x', padx=10)
        ctk.CTkLabel(add_f, text=T("col_mgr_add"), font=self.fb).pack(anchor='w', pady=(0, 4))
        r1 = ctk.CTkFrame(add_f, fg_color="transparent"); r1.pack(fill='x', pady=2)
        ctk.CTkLabel(r1, text=T("col_mgr_name"), font=self.fs, width=80).pack(side='left')
        new_name = ctk.CTkEntry(r1, corner_radius=6, border_width=1, border_color=_C.BORDER); new_name.pack(side='left', fill='x', expand=True, padx=5)
        r2 = ctk.CTkFrame(add_f, fg_color="transparent"); r2.pack(fill='x', pady=2)
        ctk.CTkLabel(r2, text=T("col_mgr_key"), font=self.fs, width=80).pack(side='left')
        new_key = ctk.CTkEntry(r2, corner_radius=6, border_width=1, border_color=_C.BORDER, placeholder_text="e.g. Tg_DMA"); new_key.pack(side='left', fill='x', expand=True, padx=5)

        def _add_col():
            nm = new_name.get().strip(); dk = new_key.get().strip()
            if not nm or not dk: return
            if any(c['db_key'] == dk for c in self.dm.mat_columns): return
            col = {"db_key": dk, "display": nm, "unit": "", "data_key": dk.lower(), "visible": True, "builtin": False}
            self.dm.mat_columns.append(col)
            var = tk.BooleanVar(value=True)
            rf = ctk.CTkFrame(scroll, fg_color="transparent"); rf.pack(fill='x', pady=2)
            ctk.CTkCheckBox(rf, text=nm, variable=var, font=self.fs, corner_radius=4).pack(side='left', padx=10)
            col_mgr_vars[dk] = var
            new_name.delete(0, 'end'); new_key.delete(0, 'end')

        ctk.CTkButton(add_f, text=T("col_mgr_add"), fg_color=self.app.current_accent, corner_radius=8,
                       command=_add_col).pack(anchor='w', pady=6)

        def _save_cols():
            for col in self.dm.mat_columns:
                key = col['db_key']
                if key in col_mgr_vars:
                    col['visible'] = col_mgr_vars[key].get()
            self.dm._save_mat_col_config()
            self._refresh_tree()
            top.destroy()

        ctk.CTkButton(top, text=T("btn_save"), fg_color=self.app.current_accent, corner_radius=8,
                       command=_save_cols).pack(pady=10)

class RecipeTab:
    def __init__(self, parent_frame, dm: DataManager, font_std, font_bold, app_instance):
        self.dm = dm; self.fs = font_std; self.fb = font_bold
        self.app = app_instance
        self.frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.frame.pack(fill='both', expand=True)
        self.current_recipe = None
        self._build()

    def _build(self):
        lf = ctk.CTkFrame(self.frame, width=320, corner_radius=8)
        lf.pack(side="left", fill="y", padx=(0, 5), pady=5)
        lf.pack_propagate(False)

        top_lf = ctk.CTkFrame(lf, fg_color="transparent")
        top_lf.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkLabel(top_lf, text=T("recipe_list_title"), font=self.fb).pack(side='left')
        self.btn_refresh = ctk.CTkButton(top_lf, text=T("btn_refresh"), width=80, fg_color=self.app.current_accent, command=self._refresh_list, corner_radius=8)
        self.btn_refresh.pack(side='right')

        tree_f = RoundedTreeFrame(lf)
        tree_f.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.tree_list = ttk.Treeview(tree_f.inner, columns=("name",), show='headings', style="Recipe.Treeview")
        self.tree_list.heading("name", text=T("col_recipe_name")); self.tree_list.column("name", anchor='w')
        vsb_list = ttk.Scrollbar(tree_f.inner, orient="vertical", command=self.tree_list.yview)
        self.tree_list.configure(yscrollcommand=vsb_list.set)
        self.tree_list.pack(side='left', fill='both', expand=True); vsb_list.pack(side='right', fill='y')
        self.tree_list.bind("<<TreeviewSelect>>", self._on_select)

        bf_list = ctk.CTkFrame(lf, fg_color="transparent")
        bf_list.pack(fill='x', padx=10, pady=10)
        self.btn_rename = ctk.CTkButton(bf_list, text=T("btn_rename"), fg_color=self.app.current_accent, corner_radius=8, command=self._rename)
        self.btn_rename.pack(fill='x', pady=2)
        self.btn_del = ctk.CTkButton(bf_list, text=T("btn_delete"), fg_color="transparent", text_color=_C.RED, border_width=1, border_color=_C.RED, hover_color=_C.RED, command=self._delete, corner_radius=8)
        self.btn_del.pack(fill='x', pady=2)

        self.rf = ctk.CTkScrollableFrame(self.frame, corner_radius=8)
        self.rf.pack(side="right", fill='both', expand=True, padx=(5,0), pady=5)

        self.lbl_title = ctk.CTkLabel(self.rf, text=T("current_recipe").format(T("no_recipe_selected")), font=self.fb, text_color=self.app.current_accent)
        self.lbl_title.pack(anchor='w', padx=10, pady=10)

        comp_f = ctk.CTkFrame(self.rf, corner_radius=8)
        comp_f.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(comp_f, text=T("recipe_composition"), font=self.fb).pack(anchor='w', padx=10, pady=(5,0))
        
        self.lbl_comp_info = ctk.CTkLabel(comp_f, text="", font=self.fs, justify="left")
        self.lbl_comp_info.pack(anchor='w', padx=10, pady=2)
        
        tf_comp = RoundedTreeFrame(comp_f)
        tf_comp.pack(fill='x', padx=10, pady=5)
        cols_comp = [("mat", T("col_mat_name"), 200), ("mass", T("col_mass_g_result"), 100), ("pct", T("col_pct_result"), 100)]
        self.tree_comp = ttk.Treeview(tf_comp.inner, columns=[c[0] for c in cols_comp], show='headings', height=6)
        for cid, hdr, w in cols_comp:
            self.tree_comp.heading(cid, text=hdr); self.tree_comp.column(cid, width=w, anchor='center')
        self.tree_comp.pack(fill='x')
        
        ctk.CTkButton(comp_f, text=T("btn_copy_vertical"), fg_color=_C.GREEN, hover_color=_C.GREEN_HV, corner_radius=8, command=self._copy_vertical).pack(anchor='e', padx=10, pady=10)

        prop_f = ctk.CTkFrame(self.rf, corner_radius=8)
        prop_f.pack(fill='x', padx=10, pady=10)
        
        hdr_prop = ctk.CTkFrame(prop_f, fg_color="transparent")
        hdr_prop.pack(fill='x', padx=10, pady=10)
        ctk.CTkLabel(hdr_prop, text=T("prop_input"), font=self.fb).pack(side='left')
        self.btn_save_prop = ctk.CTkButton(hdr_prop, text=T("btn_save_all_props"), fg_color=self.app.current_accent, command=self._save_props, corner_radius=8)
        self.btn_save_prop.pack(side='right')
        self.btn_prop_mgr = ctk.CTkButton(hdr_prop, text=T("prop_mgr_add"), fg_color=self.app.current_accent,
                       width=140, command=self._open_prop_manager, corner_radius=8)
        self.btn_prop_mgr.pack(side='right', padx=5)
        self.btn_dsc_import = ctk.CTkButton(hdr_prop, text="📊 DSC/TGA", fg_color=_C.BTN_LIGHT,
                       text_color=_C.TEXT, hover_color=_C.BTN_HOVER, width=100,
                       command=self._import_dsc, corner_radius=8)
        self.btn_dsc_import.pack(side='right', padx=5)

        self.prop_container = ctk.CTkFrame(prop_f, fg_color="transparent")
        self.prop_container.pack(fill='x', padx=10, pady=5)
        self.prop_entries = {}
        self._prop_cat_labels = []

        self._refresh_list()

    def update_accent_color(self, hex_color):
        self.btn_refresh.configure(fg_color=hex_color)
        self.lbl_title.configure(text_color=hex_color)
        self.btn_save_prop.configure(fg_color=hex_color)
        self.btn_prop_mgr.configure(fg_color=hex_color)
        self.btn_rename.configure(fg_color=hex_color)
        for lbl in getattr(self, '_prop_cat_labels', []):
            try: lbl.configure(text_color=hex_color)
            except Exception: pass

    def _refresh_list(self):
        self.tree_list.delete(*self.tree_list.get_children())
        names = self.dm.get_recipe_names()
        for nm in names: self.tree_list.insert("", "end", values=(nm,))
        self._clear_detail()

    def _clear_detail(self):
        self.current_recipe = None
        self.lbl_title.configure(text=T("current_recipe").format(T("no_recipe_selected")))
        self.lbl_comp_info.configure(text="")
        self.tree_comp.delete(*self.tree_comp.get_children())
        for w in self.prop_container.winfo_children(): w.destroy()
        self.prop_entries.clear()
        self._prop_cat_labels = []

    def _on_select(self, e):
        sel = self.tree_list.selection()
        if not sel: return
        name = self.tree_list.item(sel[0], 'values')[0]
        row = self.dm.get_recipe_row(name)
        if not row: return
        self.current_recipe = name
        self.lbl_title.configure(text=T("current_recipe").format(name))
        
        info_str = f"{T('batch_label')}: {row.get('BatchNo','')}   |   {T('date_label')}: {row.get('DateCreated','')}   |   {T('mode_label')}: {row.get('CalcMode','')}\n"
        info_str += f"{T('total_mass_label')}: {row.get('TotalMass_g','0')} g   |   {T('total_cl_label')}: {row.get('TotalCl_ppm','0')} ppm"
        self.lbl_comp_info.configure(text=info_str)

        self.tree_comp.delete(*self.tree_comp.get_children())
        all_sc = get_all_slot_counts()
        all_cn = get_all_cat_cn()
        for cat, n in all_sc.items():
            cn = all_cn.get(cat, cat)
            for i in range(1, n+1):
                mat = row.get(f"{cn}{i}_Name", "")
                if mat:
                    mass = row.get(f"{cn}{i}_Mass_g", "0")
                    pct = row.get(f"{cn}{i}_Pct", "0")
                    self.tree_comp.insert("", "end", values=(mat, mass, pct))

        if not self.prop_entries:
            self._build_prop_form(row)
        else:
            self._update_prop_values(row)

    def _build_prop_form(self, row):
        """首次構建物性表單 UI（一次性，後續切換配方只更新值）。"""
        for w in self.prop_container.winfo_children(): w.destroy()
        self.prop_entries.clear()
        self._prop_cat_labels = []
        
        prop_defs = self.dm.get_prop_defs_structured()
        for cat, items in prop_defs.items():
            cf = ctk.CTkFrame(self.prop_container, fg_color="transparent")
            cf.pack(fill='x', pady=5)
            cat_lbl = ctk.CTkLabel(cf, text=T_propcat(cat), font=self.fb, text_color=self.app.current_accent)
            cat_lbl.pack(anchor='w', pady=(0, 2))
            self._prop_cat_labels.append(cat_lbl)
            
            for item in items:
                if isinstance(item, tuple) and len(item) == 3 and item[0] == '__group__':
                    _, grp_name, grp_items = item
                    ctk.CTkLabel(cf, text=f"  ▸ {T_group(grp_name)}", font=ctk.CTkFont(family=_FONT_FAMILY, size=11, weight="bold"),
                                 text_color=_C.TEXT_SEC).pack(anchor='w', padx=8, pady=(6, 1))
                    for p_name, p_unit, p_method in grp_items:
                        self._add_prop_row(cf, p_name, p_unit, p_method, row)
                else:
                    p_name, p_unit, p_method = item
                    self._add_prop_row(cf, p_name, p_unit, p_method, row)

    def _update_prop_values(self, row):
        """快速更新已有表單中的值（不重建 UI）。"""
        for csv_key, ent in self.prop_entries.items():
            ent.delete(0, 'end')
            val = row.get(csv_key, "")
            if val: ent.insert(0, str(val))

    def _add_prop_row(self, parent, p_name, p_unit, p_method, row):
        """Add a single property input row."""
        rf = ctk.CTkFrame(parent, fg_color="transparent")
        rf.pack(fill='x', pady=1)
        disp = f"{T_prop(p_name)}" + (f" ({p_unit})" if p_unit else "")
        ctk.CTkLabel(rf, text=disp, width=200, anchor='e', font=self.fs).pack(side='left', padx=5)
        ent = ctk.CTkEntry(rf, width=150, corner_radius=6, border_width=1, border_color=_C.BORDER)
        ent.pack(side='left', padx=5)
        csv_key = self.dm.get_prop_csv_key(p_name)
        val = row.get(csv_key, "")
        ent.insert(0, str(val))
        self.prop_entries[csv_key] = ent
        if p_method:
            ctk.CTkLabel(rf, text=f"[{T_method(p_method)}]", text_color=_C.TEXT_SEC,
                         font=ctk.CTkFont(family=_FONT_FAMILY, size=11)).pack(side='left', padx=2)

    def _copy_vertical(self):
        if not self.current_recipe: return
        try:
            row = self.dm.get_recipe_row(self.current_recipe)
            text = f"{T('copy_recipe_hdr_name')}\t{self.current_recipe}\n"
            text += f"{T('copy_recipe_hdr_batch')}\t{row.get('BatchNo','')}\n\n"
            text += T("copy_recipe_hdr_mat") + "\n"
            for item in self.tree_comp.get_children():
                vals = self.tree_comp.item(item,"values")
                text += f"{vals[0]}\t{vals[1]}\t{vals[2]}\n"
            text += "\n" + T("copy_recipe_hdr_prop") + "\n"
            for k, ent in self.prop_entries.items():
                v = ent.get().strip()
                if v: text += f"{k}\t{v}\n"
            self.frame.clipboard_clear(); self.frame.clipboard_append(text); self.frame.update()
            messagebox.showinfo(T("ok"), T("copy_ok"))
        except Exception as e: messagebox.showerror(T("error"), str(e))

    def _import_dsc(self):
        """Import DSC/TGA CSV and auto-fill property fields."""
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            filetypes=[("CSV/TXT", "*.csv *.txt"), ("All", "*.*")])
        if not path: return

        try:
            temps = []; heats = []
            with open(path, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    parts = line.strip().replace(',', '\t').split('\t')
                    if len(parts) >= 2:
                        try:
                            t = float(parts[0]); h = float(parts[1])
                            temps.append(t); heats.append(h)
                        except ValueError: continue
            if len(temps) < 10:
                messagebox.showwarning(T("hint"), f"Data too short ({len(temps)} points)")
                return

            n = len(temps)
            peak_idx = max(range(n), key=lambda i: heats[i])
            tp = temps[peak_idx]; peak_val = heats[peak_idx]
            ti = temps[0]
            threshold = peak_val * 0.05
            for i in range(peak_idx):
                if heats[i] > threshold: ti = temps[i]; break
            dt = abs(temps[1] - temps[0]) if n > 1 else 1.0
            dh_abs = abs(sum(heats) * dt)
            ea_est = 0.47 * (tp + 273.15) - 50 if tp > 100 else 0

            filled = 0
            prop_map = {
                'Prop_DSC 起始固化溫度 Ti': f"{ti:.1f}",
                'Prop_DSC_Ti': f"{ti:.1f}",
                'Prop_DSC 放熱峰溫度 Tp': f"{tp:.1f}",
                'Prop_DSC_Tp': f"{tp:.1f}",
                'Prop_DSC 反應熱 ΔH': f"{dh_abs:.1f}",
                'Prop_DSC_dH': f"{dh_abs:.1f}",
            }
            for csv_key, val in prop_map.items():
                if csv_key in self.prop_entries:
                    self.prop_entries[csv_key].delete(0, 'end')
                    self.prop_entries[csv_key].insert(0, val)
                    filled += 1

            ml_info = ""
            mats = None
            if hasattr(self, 'current_recipe') and self.current_recipe:
                row = self.dm.get_recipe_row(self.current_recipe)
                if row:
                    try:
                        vp = ViscosityPredictor(self.dm)
                        mats = vp._recipe_mats(row)
                    except Exception: pass
            if mats:
                ml_dh = PropertyMLPredictor(self.dm, 'dh')
                res = ml_dh.predict(mats, dh_abs)
                if res['n_train'] >= 2 and res['ml_pred'] > 0:
                    cure_deg = min(1.0, dh_abs / res['ml_pred'])
                    ml_info = f"\nML ΔH={res['ml_pred']:.0f} J/g → α≈{cure_deg:.0%}"

            messagebox.showinfo("DSC Import",
                f"Ti={ti:.1f}°C  Tp={tp:.1f}°C\nΔH={dh_abs:.1f} J/g  Ea≈{ea_est:.0f} kJ/mol\n"
                f"Auto-filled {filled} fields{ml_info}")
        except Exception as e:
            messagebox.showerror(T("error"), str(e))

    def _save_props(self):
        if not self.current_recipe: return
        pd = {k: ent.get() for k, ent in self.prop_entries.items()}
        if self.dm.update_recipe_props(self.current_recipe, pd): messagebox.showinfo(T("ok"), T("save_ok"))
        else: messagebox.showerror(T("error"), T("save_failed"))

    def _rename(self):
        if not self.current_recipe: return
        new_name = simpledialog.askstring(T("rename_title"), T("rename_prompt", self.current_recipe), initialvalue=self.current_recipe)
        if new_name and new_name != self.current_recipe:
            if new_name in self.dm.get_recipe_names(): messagebox.showwarning(T("hint"), T("warn_name_exists")); return
            self.dm.rename_recipe(self.current_recipe, new_name)
            self._refresh_list()

    def _delete(self):
        if not self.current_recipe: return
        if messagebox.askyesno(T("confirm"), T("confirm_del_recipe", self.current_recipe)):
            self.dm.delete_recipe(self.current_recipe)
            self._refresh_list()

    def _open_prop_manager(self):
        """Add/manage custom property definitions."""
        top = ctk.CTkToplevel(self.frame.winfo_toplevel())
        top.title(T("prop_mgr_add")); top.geometry("480x520"); top.grab_set()
        ctk.CTkLabel(top, text=T("prop_mgr_add"), font=self.fb).pack(pady=(10, 5))

        scroll = ctk.CTkScrollableFrame(top, corner_radius=8, height=200)
        scroll.pack(fill='both', expand=True, padx=10, pady=5)

        for p in self.dm.custom_props:
            if p.get('category') == '_deleted': continue
            rf = ctk.CTkFrame(scroll, fg_color="transparent")
            rf.pack(fill='x', pady=2)
            ctk.CTkLabel(rf, text=f"{p['name']}  ({p.get('unit','')})  [{p.get('category','')}]",
                          font=self.fs).pack(side='left', padx=10)
            def _del_prop(pname=p['name'], frame=rf):
                for pp in self.dm.custom_props:
                    if pp['name'] == pname: pp['category'] = '_deleted'; break
                self.dm.save_custom_props()
                frame.destroy()
            ctk.CTkButton(rf, text="✕", width=26, height=26, corner_radius=6, fg_color=_C.BTN_LIGHT, text_color=_C.TEXT_SEC, hover_color=_C.RED,
                           command=_del_prop).pack(side='right', padx=5)

        sep = ctk.CTkFrame(top, height=1, fg_color=_C.BORDER); sep.pack(fill='x', padx=10, pady=6)
        add_f = ctk.CTkFrame(top, fg_color="transparent"); add_f.pack(fill='x', padx=10)

        fields = {}
        for key, label in [("name", T("prop_mgr_name")), ("unit", T("prop_mgr_unit")),
                            ("method", T("prop_mgr_method"))]:
            r = ctk.CTkFrame(add_f, fg_color="transparent"); r.pack(fill='x', pady=2)
            ctk.CTkLabel(r, text=label, font=self.fs, width=80).pack(side='left')
            ent = ctk.CTkEntry(r, corner_radius=6, border_width=1, border_color=_C.BORDER); ent.pack(side='left', fill='x', expand=True, padx=5)
            fields[key] = ent

        r_cat = ctk.CTkFrame(add_f, fg_color="transparent"); r_cat.pack(fill='x', pady=2)
        ctk.CTkLabel(r_cat, text=T("prop_mgr_category"), font=self.fs, width=80).pack(side='left')
        cat_opts = list(PREDEFINED_PROPS.keys())
        cat_cb = AppleDropdown(r_cat, values=cat_opts, font=self.fs, width=200,
                                    corner_radius=8, fg_color=self.app.current_accent,
                                    button_color=self.app.current_accent)
        cat_cb.set("8.Custom")
        cat_cb.pack(side='left', padx=5)

        def _add():
            nm = fields["name"].get().strip()
            if not nm: return
            new_prop = {"name": nm, "unit": fields["unit"].get().strip(),
                        "method": fields["method"].get().strip(), "category": cat_cb.get()}
            self.dm.custom_props.append(new_prop)
            self.dm.save_custom_props()
            rf = ctk.CTkFrame(scroll, fg_color="transparent"); rf.pack(fill='x', pady=2)
            ctk.CTkLabel(rf, text=f"{nm}  ({new_prop['unit']})  [{new_prop['category']}]",
                          font=self.fs).pack(side='left', padx=10)
            for ent in fields.values(): ent.delete(0, 'end')

        ctk.CTkButton(add_f, text=T("prop_mgr_add"), fg_color=self.app.current_accent, corner_radius=8,
                       command=_add).pack(anchor='w', pady=8)
        ctk.CTkButton(top, text=T("btn_save"), fg_color=self.app.current_accent,
                       command=top.destroy).pack(pady=10)
PREFS_FILE = "epoxy_prefs.json"

def _load_prefs():
    defaults = {"accent": _C.BLUE, "mat_db": MAT_DB_FILE, "recipe_db": RECIPE_DB_FILE}
    if os.path.exists(PREFS_FILE):
        try:
            with open(PREFS_FILE, 'r', encoding='utf-8') as f:
                d = json.load(f)
                defaults.update(d)
        except Exception: pass
    return defaults

def _save_prefs(prefs):
    try:
        with open(PREFS_FILE, 'w', encoding='utf-8') as f:
            json.dump(prefs, f, ensure_ascii=False, indent=2)
    except Exception: pass

class ColorDot(tk.Canvas):
    SIZE = 20
    def __init__(self, parent, color, on_click, selected=False, **kw):
        super().__init__(parent, width=self.SIZE+6, height=self.SIZE+6,
                         highlightthickness=0, bd=0, **kw)
        self.color = color; self._on_click = on_click; self._selected = selected
        self._draw()
        self.bind("<Button-1>", lambda e: self._on_click(self.color))
        self.bind("<Enter>", lambda e: self.config(cursor="hand2"))
    def _draw(self):
        self.delete("all")
        cx, cy, r = (self.SIZE+6)//2, (self.SIZE+6)//2, self.SIZE//2
        if self._selected:
            self.create_oval(cx-r-2, cy-r-2, cx+r+2, cy+r+2, outline=self.color, width=2, fill="")
        self.create_oval(cx-r+1, cy-r+1, cx+r-1, cy+r-1, fill=self.color, outline="")
    def set_selected(self, sel):
        self._selected = sel; self._draw()

class HomeTab:
    def __init__(self, parent_frame, app):
        self.app = app
        self.frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.frame.pack(fill='both', expand=True)
        self._build()

    def _build(self):
        outer = ctk.CTkFrame(self.frame, fg_color="transparent")
        outer.pack(expand=True, fill='both', padx=40, pady=20)

        # banner 分為上方諺語（大字粗體）+ 下方 tagline（小字細體）
        self.banner_frame = ctk.CTkFrame(outer, corner_radius=8, fg_color=self.app.current_accent, height=100)
        self.banner_frame.pack(fill='x', pady=(0, 20))
        self.banner_frame.pack_propagate(False)
        inner = ctk.CTkFrame(self.banner_frame, fg_color="transparent")
        inner.pack(expand=True)
        self.lbl_motto = ctk.CTkLabel(inner, text=T("home_motto"),
                                       font=ctk.CTkFont(family=_FONT_FAMILY, size=16, weight="bold"),
                                       text_color="white", justify="center")
        self.lbl_motto.pack(pady=(2, 2))
        self.lbl_tagline = ctk.CTkLabel(inner, text=T("home_tagline"),
                                         font=ctk.CTkFont(family=_FONT_FAMILY, size=11),
                                         text_color="white", justify="center")
        self.lbl_tagline.pack(pady=(0, 2))
        # 向下相容舊引用
        self.lbl_banner = self.lbl_motto

        cols = ctk.CTkFrame(outer, fg_color="transparent")
        cols.pack(fill='both', expand=True)

        left = ctk.CTkFrame(cols, corner_radius=8)
        left.pack(side='left', fill='both', expand=True, padx=(0, 10))

        ctk.CTkLabel(left, text=T("home_db_section"), font=self.app.font_bold).pack(anchor='w', padx=16, pady=(16, 8))

        for db_key, label_key, attr in [("mat_db", "home_mat_db", "mat_db_path"),
                                         ("recipe_db", "home_recipe_db", "recipe_db_path")]:
            rf = ctk.CTkFrame(left, fg_color="transparent")
            rf.pack(fill='x', padx=16, pady=4)
            ctk.CTkLabel(rf, text=T(label_key), font=self.app.font_std, width=120, anchor='e').pack(side='left')
            ent = ctk.CTkEntry(rf, font=self.app.font_std, corner_radius=6, border_width=1, border_color=_C.BORDER)
            ent.insert(0, self.app.prefs.get(db_key, ""))
            ent.pack(side='left', fill='x', expand=True, padx=4)
            setattr(self, attr, ent)
            ctk.CTkButton(rf, text=T("home_browse"), width=56, corner_radius=8,
                          fg_color=self.app.current_accent,
                          command=lambda e=ent: self._browse(e)).pack(side='right', padx=1)
            ctk.CTkButton(rf, text=T("home_new_db"), width=52,
                          fg_color=self.app.current_accent,
                          command=lambda e=ent: self._new_db(e)).pack(side='right', padx=1)
            ctk.CTkButton(rf, text=T("home_rename_db"), width=64,
                          fg_color=self.app.current_accent,
                          command=lambda e=ent: self._rename_db(e)).pack(side='right', padx=1)

        self.btn_reload = ctk.CTkButton(left, text=T("home_reload"), fg_color=self.app.current_accent, corner_radius=8,
                                         command=self._reload_db)
        self.btn_reload.pack(anchor='w', padx=16, pady=(12, 16))

        right = ctk.CTkFrame(cols, corner_radius=8)
        right.pack(side='right', fill='both', expand=True, padx=(10, 0))

        ctk.CTkLabel(right, text=T("home_appearance"), font=self.app.font_bold).pack(anchor='w', padx=16, pady=(16, 8))

        self.color_frame = ctk.CTkFrame(right, fg_color="transparent")
        self.color_frame.pack(fill='x', padx=16, pady=4)

        color_hdr = ctk.CTkFrame(self.color_frame, fg_color="transparent")
        color_hdr.pack(fill='x')
        ctk.CTkLabel(color_hdr, text=T("home_accent_color"), font=self.app.font_std).pack(side='left')

        self._color_expanded = False
        self.selected_dot = ColorDot(color_hdr, self.app.current_accent, lambda c: self._toggle_palette(), selected=True)
        self.selected_dot.pack(side='left', padx=8)

        self.palette_frame = ctk.CTkFrame(self.color_frame, fg_color="transparent")
        self._color_dots = []
        for hex_c in EpoxyApp.ACCENT_PALETTE:
            dot = ColorDot(self.palette_frame, hex_c, self._pick_color,
                           selected=(hex_c == self.app.current_accent))
            dot.pack(side='left', padx=3, pady=6)
            self._color_dots.append(dot)

        ctk.CTkLabel(right, text=T("home_language"), font=self.app.font_bold).pack(anchor='w', padx=16, pady=(16, 4))
        self.lang_cb = AppleDropdown(right, values=[LANG_DISPLAY[l] for l in SUPPORTED_LANGS],
                                          command=self.app._on_lang_change, font=self.app.font_std,
                                          width=180, corner_radius=8, fg_color=self.app.current_accent,
                                          button_color=self.app.current_accent)
        self.lang_cb.set(LANG_DISPLAY.get(_CURRENT_LANG, "正體中文"))
        self.lang_cb.pack(anchor='w', padx=16, pady=(0, 16))

    def _toggle_palette(self):
        if self._color_expanded:
            self.palette_frame.pack_forget()
        else:
            self.palette_frame.pack(fill='x', pady=(4, 0))
        self._color_expanded = not self._color_expanded

    def _pick_color(self, hex_color):
        self.app._apply_accent(hex_color)
        self.selected_dot.color = hex_color
        self.selected_dot._selected = True
        self.selected_dot._draw()
        for dot in self._color_dots:
            dot.set_selected(dot.color == hex_color)
        self.banner_frame.configure(fg_color=hex_color)
        self.lang_cb.configure(fg_color=hex_color, button_color=hex_color)
        self.btn_reload.configure(fg_color=hex_color)
        for attr in ['mat_db_path','recipe_db_path']:
            ent = getattr(self, attr, None)
            if ent:
                for w in ent.master.winfo_children():
                    if isinstance(w, ctk.CTkButton):
                        w.configure(fg_color=hex_color)

    def _browse(self, entry_widget):
        from tkinter import filedialog
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("All", "*.*")])
        if path:
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, path)

    def _new_db(self, entry_widget):
        """Create a new empty CSV database."""
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV", "*.csv")])
        if path:
            try:
                with open(path, 'w', encoding='utf-8-sig', newline='') as f:
                    f.write("")
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, path)
            except Exception as e:
                messagebox.showerror(T("error"), str(e))

    def _rename_db(self, entry_widget):
        """Rename an existing database file."""
        old_path = entry_widget.get().strip()
        if not old_path or not os.path.exists(old_path):
            messagebox.showwarning(T("hint"), T("warn_name_empty")); return
        new_name = simpledialog.askstring(T("home_rename_db"), T("rename_prompt", old_path),
                                           initialvalue=os.path.basename(old_path))
        if new_name and new_name != os.path.basename(old_path):
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, new_path)
            except Exception as e:
                messagebox.showerror(T("error"), str(e))

    def _reload_db(self):
        global MAT_DB_FILE, RECIPE_DB_FILE
        new_mat = self.mat_db_path.get().strip()
        new_rec = self.recipe_db_path.get().strip()
        if new_mat: MAT_DB_FILE = new_mat
        if new_rec: RECIPE_DB_FILE = new_rec
        self.app.prefs["mat_db"] = MAT_DB_FILE
        self.app.prefs["recipe_db"] = RECIPE_DB_FILE
        _save_prefs(self.app.prefs)
        self.app.dm = DataManager()
        self.app._rebuild_tabs()
        messagebox.showinfo(T("ok"), T("home_reload"))

    def update_accent_color(self, hex_color):
        self.selected_dot.color = hex_color
        self.selected_dot._selected = True
        self.selected_dot._draw()
        for dot in self._color_dots:
            dot.set_selected(dot.color == hex_color)
        self.banner_frame.configure(fg_color=hex_color)
        self.lang_cb.configure(fg_color=hex_color, button_color=hex_color)
        self.btn_reload.configure(fg_color=hex_color)
        for attr in ['mat_db_path', 'recipe_db_path']:
            ent = getattr(self, attr, None)
            if ent:
                for w in ent.master.winfo_children():
                    if isinstance(w, ctk.CTkButton):
                        w.configure(fg_color=hex_color)

class EpoxyApp:
    ACCENT_PALETTE = [
        _C.BLUE,
        _C.INDIGO,
        "#AF52DE",   # Purple
        "#FF2D55",   # Pink
        _C.RED,
        _C.ORANGE,
        _C.GREEN,
        "#5AC8FA",   # Teal Blue
        "#607D8B",   # Slate (淺色系白底黑字主題)
        "#1d1d1f",   # Near Black
    ]

    def __init__(self, root):
        self.root = root
        self.prefs = _load_prefs()
        self.current_accent = self.prefs.get("accent", self.ACCENT_PALETTE[0])
        if self.current_accent not in self.ACCENT_PALETTE:
            self.current_accent = self.ACCENT_PALETTE[0]

        global MAT_DB_FILE, RECIPE_DB_FILE
        MAT_DB_FILE = self.prefs.get("mat_db", MAT_DB_FILE)
        RECIPE_DB_FILE = self.prefs.get("recipe_db", RECIPE_DB_FILE)

        self.root.minsize(900, 600)

        self.font_std   = ctk.CTkFont(family=_FONT_FAMILY, size=13)
        self.font_bold  = ctk.CTkFont(family=_FONT_FAMILY, size=13, weight="bold")
        self.font_title = ctk.CTkFont(family=_FONT_FAMILY, size=22, weight="bold")
        self.font_ver   = ctk.CTkFont(family=_FONT_FAMILY, size=10)

        self.dm = DataManager()
        _setup_modern_styles(self.current_accent)

        self._build_window()

        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w = min(max(self.root.winfo_reqwidth(), 1280), int(sw * 0.88))
        h = min(max(self.root.winfo_reqheight(), 720), int(sh * 0.88))
        x = (sw - w) // 2
        y = max(0, (sh - h) // 2 - 30)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _draw_indicator(self):
        c = self.accent_indicator
        c.delete("all")
        c.create_oval(2, 2, 12, 12, fill=self.current_accent, outline="")

    def _build_window(self):
        """建立 (或重建) 主視窗的全部 widgets。
        此方法設計為可以被重複呼叫 — 呼叫前需先 destroy root 的所有 children。"""
        self.root.title(f"{T('app_title')} V6.4.12")

        self.top_bar = ctk.CTkFrame(self.root, height=48, corner_radius=0, fg_color="transparent")
        self.top_bar.pack(fill='x', padx=24, pady=(12, 0))

        self.lbl_title = ctk.CTkLabel(self.top_bar, text=T('app_title'), font=self.font_title,
                                       text_color=_C.TEXT)
        self.lbl_title.pack(side='left')
        ctk.CTkLabel(self.top_bar, text="v6.4.12", font=self.font_ver, text_color=_C.TEXT_TER).pack(side='left', padx=(6,0), pady=(6,0))

        self.accent_indicator = tk.Canvas(self.top_bar, width=14, height=14, highlightthickness=0, bd=0)
        self.accent_indicator.pack(side='right', padx=8, pady=2)
        self._draw_indicator()
        self.accent_indicator.bind("<Button-1>", lambda e: self.tabview.set(T("tab_home")))
        self.accent_indicator.bind("<Enter>", lambda e: self.accent_indicator.config(cursor="hand2"))

        self.tabview = ctk.CTkTabview(self.root, corner_radius=8,
                                       segmented_button_selected_color=self.current_accent,
                                       segmented_button_unselected_color=_C.TAB_UNSEL,
                                       segmented_button_selected_hover_color=self.current_accent,
                                       segmented_button_unselected_hover_color=_C.TAB_HOVER,
                                       text_color="white",
                                       text_color_disabled="white")
        self.tabview.pack(pady=(6, 12), padx=24, expand=True, fill='both')
        self._build_tabs()

    def _build_tabs(self):
        self.tab_names = [T("tab_home"), T("tab_calc"), T("tab_2k"), T("tab_db"), T("tab_recipe")]
        for name in self.tab_names:
            self.tabview.add(name)

        self.home_tab   = HomeTab(self.tabview.tab(T("tab_home")), self)
        self.calc_tab   = CalcTab(self.tabview.tab(T("tab_calc")),   self.dm, self.font_std, self.font_bold, self)
        self.twok_tab   = TwoKCalcTab(self.tabview.tab(T("tab_2k")),self.dm, self.font_std, self.font_bold, self)
        self.db_tab     = DatabaseTab(self.tabview.tab(T("tab_db")), self.dm, self.font_std, self.font_bold, self)
        self.recipe_tab = RecipeTab(self.tabview.tab(T("tab_recipe")),self.dm, self.font_std, self.font_bold, self)

    def _full_rebuild(self):
        """徹底重建視窗內容 — destroy 所有 root children 並從頭 build。
        這避免只重建 tabview 時 tkinter segmented button 的狀態殘留問題。"""
        for child in list(self.root.winfo_children()):
            try:
                child.destroy()
            except Exception:
                pass
        self.root.update_idletasks()  # 強制 flush 所有 pending destroy
        self._build_window()

    def _rebuild_tabs(self):
        """Redirect to _full_rebuild (保留此方法以相容 HomeTab._reload_db)"""
        self._full_rebuild()

    def _apply_accent(self, hex_color):
        self.current_accent = hex_color
        self.prefs["accent"] = hex_color
        _save_prefs(self.prefs)
        _update_ttk_accent(hex_color)
        self.tabview.configure(segmented_button_selected_color=hex_color,
                               segmented_button_selected_hover_color=hex_color)
        self._draw_indicator()
        for tab_name in ['home_tab', 'calc_tab', 'twok_tab', 'db_tab', 'recipe_tab']:
            tab = getattr(self, tab_name, None)
            if tab and hasattr(tab, 'update_accent_color'):
                tab.update_accent_color(hex_color)

    def _on_lang_change(self, choice):
        rev = {v: k for k, v in LANG_DISPLAY.items()}
        lang = rev.get(choice, "zh_TW")
        _save_lang(lang)
        self.dm.mat_columns = self.dm._load_mat_col_config()
        # 延遲 + 完整重建。延遲讓 AppleDropdown._on_pick 完整返回，
        # 完整重建確保沒有任何 widget 持有舊語言的 reference。
        self.root.after(50, self._full_rebuild)

    def _rebuild_ui(self):
        """Legacy alias — redirect 到 _full_rebuild"""
        self._full_rebuild()

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    _setup_modern_styles()
    app = EpoxyApp(root)
    root.mainloop()