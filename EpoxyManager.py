import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv, os, datetime, json

# ─────────────── 多語言系統 ───────────────
LANG_CFG_FILE = "lang_config.json"
SUPPORTED_LANGS = ["zh_TW", "zh_CN", "en", "ja"]
LANG_DISPLAY = {"zh_TW": "正體中文", "zh_CN": "简体中文", "en": "English", "ja": "日本語"}

_CURRENT_LANG = "zh_TW"

_TRANSLATIONS = {
# ── 全局 / 應用標題 ──
"app_title":                  {"zh_TW":"環氧樹脂工作站", "zh_CN":"环氧树脂工作站", "en":"Epoxy Resin Workstation", "ja":"エポキシ樹脂ワークステーション"},
"tab_calc":                   {"zh_TW":"🗡 配方設計與計算", "zh_CN":"🗡 配方设计与计算", "en":"🗡 Formulation Design", "ja":"🗡 配合設計と計算"},
"tab_db":                     {"zh_TW":"🕷 物料數據庫管理", "zh_CN":"🕷 物料数据库管理", "en":"🕷 Material Database", "ja":"🕷 材料データベース管理"},
"tab_recipe":                 {"zh_TW":"📋 配方管理與物性", "zh_CN":"📋 配方管理与物性", "en":"📋 Recipe & Properties", "ja":"📋 配合管理と物性"},
"language":                   {"zh_TW":"語言", "zh_CN":"语言", "en":"Language", "ja":"言語"},
# ── 類別名 ──
"cat_resins":                 {"zh_TW":"樹脂", "zh_CN":"树脂", "en":"Resins", "ja":"樹脂"},
"cat_hardeners":              {"zh_TW":"固化劑", "zh_CN":"固化剂", "en":"Hardeners", "ja":"硬化剤"},
"cat_additives":              {"zh_TW":"助劑", "zh_CN":"助剂", "en":"Additives", "ja":"添加剤"},
"cat_fillers":                {"zh_TW":"填料", "zh_CN":"填料", "en":"Fillers", "ja":"フィラー"},
"cat_catalysts":              {"zh_TW":"催化劑", "zh_CN":"催化剂", "en":"Catalysts", "ja":"触媒"},
# ── CalcTab 配方設計 ──
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
"opt_100g":                   {"zh_TW":"100g 配平選項", "zh_CN":"100g 配平选项", "en":"100g Balancing Options", "ja":"100g配合オプション"},
"join_100g_balance":          {"zh_TW":"參與100g配平", "zh_CN":"参与100g配平", "en":"Include in 100g balance", "ja":"100g配合に参加"},
"btn_calculate":              {"zh_TW":"▶ 開始計算並生成報表", "zh_CN":"▶ 开始计算并生成报表", "en":"▶ Calculate & Generate Report", "ja":"▶ 計算してレポート生成"},
"col_material":               {"zh_TW":"物料", "zh_CN":"物料", "en":"Material", "ja":"材料"},
"col_mass_g":                 {"zh_TW":"質量(g)", "zh_CN":"质量(g)", "en":"Mass(g)", "ja":"質量(g)"},
"col_pct":                    {"zh_TW":"佔比(%)", "zh_CN":"占比(%)", "en":"Ratio(%)", "ja":"配合比(%)"},
"col_eq_info":                {"zh_TW":"當量資訊", "zh_CN":"当量信息", "en":"Eq. Info", "ja":"当量情報"},
"col_cl_ppm":                 {"zh_TW":"氯(ppm)", "zh_CN":"氯(ppm)", "en":"Cl(ppm)", "ja":"塩素(ppm)"},
"btn_copy_excel":             {"zh_TW":"📋 複製到 Excel", "zh_CN":"📋 复制到 Excel", "en":"📋 Copy to Excel", "ja":"📋 Excelにコピー"},
"btn_save_recipe":            {"zh_TW":"💾 儲存配方至數據庫", "zh_CN":"💾 保存配方至数据库", "en":"💾 Save Recipe to Database", "ja":"💾 配合をデータベースに保存"},
"hdr_name_type":              {"zh_TW":"名稱/類型", "zh_CN":"名称/类型", "en":"Name/Type", "ja":"名称/タイプ"},
"hdr_eq_ratio":               {"zh_TW":"當量比例/佔比", "zh_CN":"当量比例/占比", "en":"Eq.Ratio/Pct", "ja":"当量比/配合比"},
"hdr_corr_pct":               {"zh_TW":"校正(C)%", "zh_CN":"校正(C)%", "en":"Correction(C)%", "ja":"補正(C)%"},
"clear_reselect":             {"zh_TW":"清空並重選物料", "zh_CN":"清空并重选物料", "en":"Clear & reselect material", "ja":"クリアして再選択"},
"no_note":                    {"zh_TW":"無備註", "zh_CN":"无备注", "en":"No notes", "ja":"備考なし"},
"fixed_mass":                 {"zh_TW":"固定質量", "zh_CN":"固定质量", "en":"Fixed Mass", "ja":"固定質量"},
"fixed_ratio":                {"zh_TW":"固定比例", "zh_CN":"固定比例", "en":"Fixed Ratio", "ja":"固定比率"},
# ── CalcTab 儲存對話框 ──
"dlg_save_recipe":            {"zh_TW":"儲存配方", "zh_CN":"保存配方", "en":"Save Recipe", "ja":"配合を保存"},
"recipe_name_label":          {"zh_TW":"配方名稱：", "zh_CN":"配方名称：", "en":"Recipe Name:", "ja":"配合名："},
"batch_no_label":             {"zh_TW":"批次號：", "zh_CN":"批次号：", "en":"Batch No.:", "ja":"ロット番号："},
"btn_confirm_save":           {"zh_TW":"💾 確認儲存", "zh_CN":"💾 确认保存", "en":"💾 Confirm Save", "ja":"💾 保存確認"},
"warn_enter_name":            {"zh_TW":"請輸入配方名稱", "zh_CN":"请输入配方名称", "en":"Please enter recipe name", "ja":"配合名を入力してください"},
"warn_calc_first":            {"zh_TW":"請先執行計算", "zh_CN":"请先执行计算", "en":"Please calculate first", "ja":"先に計算を実行してください"},
"save_ok":                    {"zh_TW":"已成功儲存至配方庫", "zh_CN":"已成功保存至配方库", "en":"Successfully saved to recipe database", "ja":"配合データベースに保存しました"},
"copy_ok":                    {"zh_TW":"已複製到剪貼板，可在 Excel 中貼上", "zh_CN":"已复制到剪贴板，可在 Excel 中粘贴", "en":"Copied to clipboard, paste in Excel", "ja":"クリップボードにコピーしました。Excelに貼り付けできます"},
# ── DatabaseTab ──
"data_edit":                  {"zh_TW":"數據編輯", "zh_CN":"数据编辑", "en":"Data Edit", "ja":"データ編集"},
"not_selected":               {"zh_TW":"（未選中數據）", "zh_CN":"（未选中数据）", "en":"(No selection)", "ja":"（未選択）"},
"editing":                    {"zh_TW":"▶ 編輯中：", "zh_CN":"▶ 编辑中：", "en":"▶ Editing: ", "ja":"▶ 編集中："},
"btn_deselect":               {"zh_TW":"✖ 取消選中", "zh_CN":"✖ 取消选中", "en":"✖ Deselect", "ja":"✖ 選択解除"},
"lbl_category":               {"zh_TW":"類別:", "zh_CN":"类别:", "en":"Category:", "ja":"カテゴリー:"},
"lbl_name":                   {"zh_TW":"名稱:", "zh_CN":"名称:", "en":"Name:", "ja":"名称:"},
"lbl_type":                   {"zh_TW":"類型:", "zh_CN":"类型:", "en":"Type:", "ja":"タイプ:"},
"lbl_appearance":             {"zh_TW":"外觀特性:", "zh_CN":"外观特性:", "en":"Appearance:", "ja":"外観特性:"},
"lbl_viscosity":              {"zh_TW":"粘度 cP(25℃):", "zh_CN":"粘度 cP(25℃):", "en":"Viscosity cP(25℃):", "ja":"粘度 cP(25℃):"},
"lbl_dk":                     {"zh_TW":"介電常數:", "zh_CN":"介电常数:", "en":"Dielectric Const.:", "ja":"誘電率:"},
"lbl_surface_energy":         {"zh_TW":"表面能 mN/m(25℃):", "zh_CN":"表面能 mN/m(25℃):", "en":"Surface Energy mN/m(25℃):", "ja":"表面エネルギー mN/m(25℃):"},
"lbl_structure":              {"zh_TW":"分子結構:", "zh_CN":"分子结构:", "en":"Molecular Structure:", "ja":"分子構造:"},
"lbl_source":                 {"zh_TW":"來源:", "zh_CN":"来源:", "en":"Source:", "ja":"出典:"},
"lbl_cl":                     {"zh_TW":"氯(ppm):", "zh_CN":"氯(ppm):", "en":"Cl(ppm):", "ja":"塩素(ppm):"},
"lbl_eew":                    {"zh_TW":"EEW直接輸入:", "zh_CN":"EEW直接输入:", "en":"EEW Direct Input:", "ja":"EEW直接入力:"},
"lbl_ahew":                   {"zh_TW":"當量直接輸入:", "zh_CN":"当量直接输入:", "en":"Equivalent Direct Input:", "ja":"当量直接入力:"},
"hardener_calc":              {"zh_TW":"⚙️ 固化劑當量輔助計算", "zh_CN":"⚙️ 固化剂当量辅助计算", "en":"⚙️ Hardener Eq. Calculator", "ja":"⚙️ 硬化剤当量補助計算"},
"lbl_subtype":                {"zh_TW":"子類型:", "zh_CN":"子类型:", "en":"Subtype:", "ja":"サブタイプ:"},
"custom_fields":              {"zh_TW":"📝 自定義欄位", "zh_CN":"📝 自定义字段", "en":"📝 Custom Fields", "ja":"📝 カスタムフィールド"},
"no_custom_fields":           {"zh_TW":"（無自定義欄位，可在「欄位管理」中新增）", "zh_CN":"（无自定义字段，可在「字段管理」中新增）", "en":"(No custom fields. Add in Column Manager)", "ja":"（カスタムフィールドなし。列管理で追加可能）"},
"lbl_notes":                  {"zh_TW":"備註:", "zh_CN":"备注:", "en":"Notes:", "ja":"備考:"},
"btn_save":                   {"zh_TW":"💾 儲存", "zh_CN":"💾 保存", "en":"💾 Save", "ja":"💾 保存"},
"btn_save_as_new":            {"zh_TW":"📄 另存為新物料", "zh_CN":"📄 另存为新物料", "en":"📄 Save As New", "ja":"📄 新規として保存"},
"btn_delete_sel":             {"zh_TW":"🗑 刪除選中", "zh_CN":"🗑 删除选中", "en":"🗑 Delete Selected", "ja":"🗑 選択削除"},
"btn_col_manager":            {"zh_TW":"⚙ 欄位管理", "zh_CN":"⚙ 字段管理", "en":"⚙ Column Manager", "ja":"⚙ 列管理"},
"col_mgr_hint":               {"zh_TW":"(新增/刪除/顯示隱藏欄位)", "zh_CN":"(新增/删除/显示隐藏字段)", "en":"(Add/Delete/Show/Hide columns)", "ja":"(追加/削除/表示切替)"},
"saved_to_db":                {"zh_TW":"已成功儲存至物料庫", "zh_CN":"已成功保存至物料库", "en":"Successfully saved to material database", "ja":"材料データベースに保存しました"},
"saved_as_new":               {"zh_TW":"已另存「{}」至物料庫", "zh_CN":"已另存「{}」至物料库", "en":"Saved '{}' as new material", "ja":"「{}」を新規保存しました"},
"name_exists_overwrite":      {"zh_TW":"物料「{}」已存在於 {} 類別中。\n\n確定要覆蓋嗎？如不要覆蓋，請先修改名稱欄。", "zh_CN":"物料「{}」已存在于 {} 类别中。\n\n确定要覆盖吗？如不要覆盖，请先修改名称栏。", "en":"Material '{}' already exists in {} category.\n\nOverwrite? If not, change the name first.", "ja":"材料「{}」は{}カテゴリーに既に存在します。\n\n上書きしますか？上書きしない場合は名前を変更してください。"},
"name_exists_title":          {"zh_TW":"名稱已存在", "zh_CN":"名称已存在", "en":"Name Exists", "ja":"名前が既に存在"},
"warn_enter_mat_name":        {"zh_TW":"請輸入物料名稱", "zh_CN":"请输入物料名称", "en":"Please enter material name", "ja":"材料名を入力してください"},
"warn_eq_format":             {"zh_TW":"EEW/當量值格式錯誤", "zh_CN":"EEW/当量值格式错误", "en":"Invalid EEW/Equivalent format", "ja":"EEW/当量値のフォーマットが無効です"},
"confirm_delete":             {"zh_TW":"確定刪除「{}」？", "zh_CN":"确定删除「{}」？", "en":"Delete '{}'?", "ja":"「{}」を削除しますか？"},
"confirm":                    {"zh_TW":"確認", "zh_CN":"确认", "en":"Confirm", "ja":"確認"},
"hint":                       {"zh_TW":"提示", "zh_CN":"提示", "en":"Notice", "ja":"通知"},
"error":                      {"zh_TW":"錯誤", "zh_CN":"错误", "en":"Error", "ja":"エラー"},
"ok":                         {"zh_TW":"OK", "zh_CN":"OK", "en":"OK", "ja":"OK"},
"warn_select_delete":         {"zh_TW":"請選擇要刪除的物料", "zh_CN":"请选择要删除的物料", "en":"Please select a material to delete", "ja":"削除する材料を選択してください"},
# ── 固化劑輔助計算 ──
"h_amine":                    {"zh_TW":"胺類", "zh_CN":"胺类", "en":"Amine", "ja":"アミン系"},
"h_polyamide":                {"zh_TW":"聚酰胺", "zh_CN":"聚酰胺", "en":"Polyamide", "ja":"ポリアミド"},
"h_anhydride":                {"zh_TW":"酸酐", "zh_CN":"酸酐", "en":"Anhydride", "ja":"酸無水物"},
"h_mercaptan":                {"zh_TW":"巯基", "zh_CN":"巯基", "en":"Mercaptan", "ja":"メルカプタン"},
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
"lbl_mercapto_groups":        {"zh_TW":"巯基數:", "zh_CN":"巯基数:", "en":"Mercapto Groups:", "ja":"メルカプト基数:"},
"calc_mw_merc":               {"zh_TW":"計算(MW/巯基數)", "zh_CN":"计算(MW/巯基数)", "en":"Calc (MW/SH Groups)", "ja":"計算(MW/SH基数)"},
"lbl_oh_value":               {"zh_TW":"羥值:", "zh_CN":"羟值:", "en":"Hydroxyl Value:", "ja":"水酸基価:"},
"calc_56100_oh":              {"zh_TW":"計算(56100/羥值)", "zh_CN":"计算(56100/羟值)", "en":"Calc (56100/OHV)", "ja":"計算(56100/OHV)"},
# ── 欄位管理對話框 ──
"col_mgr_title":              {"zh_TW":"欄位管理", "zh_CN":"字段管理", "en":"Column Manager", "ja":"列管理"},
"col_mgr_check_hint":         {"zh_TW":"勾選要在列表中顯示的欄位：", "zh_CN":"勾选要在列表中显示的字段：", "en":"Check columns to display in the list:", "ja":"リストに表示する列にチェック:"},
"builtin":                    {"zh_TW":"內建", "zh_CN":"内置", "en":"Built-in", "ja":"ビルトイン"},
"custom":                     {"zh_TW":"自定義", "zh_CN":"自定义", "en":"Custom", "ja":"カスタム"},
"add_custom_col":             {"zh_TW":"➕ 新增自定義欄位", "zh_CN":"➕ 新增自定义字段", "en":"➕ Add Custom Column", "ja":"➕ カスタム列追加"},
"lbl_display_name":           {"zh_TW":"顯示名稱*:", "zh_CN":"显示名称*:", "en":"Display Name*:", "ja":"表示名*:"},
"lbl_db_key":                 {"zh_TW":"DB Key(英文)*:", "zh_CN":"DB Key(英文)*:", "en":"DB Key*:", "ja":"DBキー(英語)*:"},
"lbl_unit":                   {"zh_TW":"單位:", "zh_CN":"单位:", "en":"Unit:", "ja":"単位:"},
"btn_add_col":                {"zh_TW":"✅ 新增欄位", "zh_CN":"✅ 新增字段", "en":"✅ Add Column", "ja":"✅ 列を追加"},
"btn_del_custom_col":         {"zh_TW":"🗑 刪除自定義欄位", "zh_CN":"🗑 删除自定义字段", "en":"🗑 Delete Custom Column", "ja":"🗑 カスタム列削除"},
"del_custom_col_title":       {"zh_TW":"刪除自定義欄位", "zh_CN":"删除自定义字段", "en":"Delete Custom Column", "ja":"カスタム列を削除"},
"no_custom_col_del":          {"zh_TW":"目前無自定義欄位可刪除", "zh_CN":"目前无自定义字段可删除", "en":"No custom columns to delete", "ja":"削除可能なカスタム列がありません"},
"confirm_del_col":            {"zh_TW":"確定刪除欄位「{}」？", "zh_CN":"确定删除字段「{}」？", "en":"Delete column '{}'?", "ja":"列「{}」を削除しますか？"},
"warn_fill_disp_key":         {"zh_TW":"請填寫顯示名稱和DB Key", "zh_CN":"请填写显示名称和DB Key", "en":"Please fill Display Name and DB Key", "ja":"表示名とDBキーを入力してください"},
"warn_key_format":            {"zh_TW":"DB Key 只能包含英文字母、數字和底線，且不能以數字開頭", "zh_CN":"DB Key 只能包含英文字母、数字和下划线，且不能以数字开头", "en":"DB Key must be a valid identifier (letters, digits, underscore)", "ja":"DBキーは英字・数字・アンダースコアのみ使用可能"},
"warn_key_exists":            {"zh_TW":"DB Key「{}」已存在", "zh_CN":"DB Key「{}」已存在", "en":"DB Key '{}' already exists", "ja":"DBキー「{}」は既に存在します"},
"col_added":                  {"zh_TW":"已新增欄位「{}」", "zh_CN":"已新增字段「{}」", "en":"Column '{}' added", "ja":"列「{}」を追加しました"},
"btn_ok":                     {"zh_TW":"確定", "zh_CN":"确定", "en":"OK", "ja":"OK"},
# ── RecipeTab ──
"recipe_list":                {"zh_TW":"配方清單", "zh_CN":"配方列表", "en":"Recipe List", "ja":"配合リスト"},
"col_recipe_name":            {"zh_TW":"配方名稱", "zh_CN":"配方名称", "en":"Recipe Name", "ja":"配合名"},
"col_batch":                  {"zh_TW":"批次號", "zh_CN":"批次号", "en":"Batch No.", "ja":"ロット番号"},
"col_date":                   {"zh_TW":"建立日期", "zh_CN":"创建日期", "en":"Date Created", "ja":"作成日"},
"col_total_mass":             {"zh_TW":"總質量(g)", "zh_CN":"总质量(g)", "en":"Total Mass(g)", "ja":"総質量(g)"},
"btn_rename":                 {"zh_TW":"✏️ 重命名", "zh_CN":"✏️ 重命名", "en":"✏️ Rename", "ja":"✏️ 名前変更"},
"btn_delete":                 {"zh_TW":"🗑 刪除", "zh_CN":"🗑 删除", "en":"🗑 Delete", "ja":"🗑 削除"},
"btn_copy_vertical":          {"zh_TW":"📋 複製(垂直Excel)", "zh_CN":"📋 复制(垂直Excel)", "en":"📋 Copy (Vertical Excel)", "ja":"📋 コピー(縦Excel)"},
"no_recipe_selected":         {"zh_TW":"（尚未選中配方）", "zh_CN":"（尚未选中配方）", "en":"(No recipe selected)", "ja":"（配合未選択）"},
"current_recipe":             {"zh_TW":"▶ 當前選中：{}", "zh_CN":"▶ 当前选中：{}", "en":"▶ Selected: {}", "ja":"▶ 選択中：{}"},
"detail_view":                {"zh_TW":"配方詳情", "zh_CN":"配方详情", "en":"Recipe Details", "ja":"配合詳細"},
"properties":                 {"zh_TW":"物性數據", "zh_CN":"物性数据", "en":"Properties", "ja":"物性データ"},
"btn_save_props":             {"zh_TW":"💾 儲存物性", "zh_CN":"💾 保存物性", "en":"💾 Save Properties", "ja":"💾 物性を保存"},
"btn_clear_props":            {"zh_TW":"🗑 清空表單", "zh_CN":"🗑 清空表单", "en":"🗑 Clear Form", "ja":"🗑 フォームをクリア"},
"btn_toggle_all":             {"zh_TW":"📂 全部展開/折疊", "zh_CN":"📂 全部展开/折叠", "en":"📂 Expand/Collapse All", "ja":"📂 すべて展開/折畳"},
"custom_prop_mgr":            {"zh_TW":"🔧 自定義物性欄位", "zh_CN":"🔧 自定义物性字段", "en":"🔧 Custom Property Fields", "ja":"🔧 カスタム物性フィールド"},
"prop_info_hint":             {"zh_TW":"💡 所有項目均可刪除。內建項目（灰色）刪除後可點「恢復內建預設」還原。", "zh_CN":"💡 所有项目均可删除。内置项目（灰色）删除后可点「恢复内置预设」还原。", "en":"💡 All items deletable. Built-in (gray) can be restored.", "ja":"💡 全項目削除可能。ビルトイン（灰色）は復元可能。"},
"btn_restore_builtin":        {"zh_TW":"🔄 恢復內建預設", "zh_CN":"🔄 恢复内置预设", "en":"🔄 Restore Defaults", "ja":"🔄 ビルトインを復元"},
"search":                     {"zh_TW":"🔍 搜尋:", "zh_CN":"🔍 搜索:", "en":"🔍 Search:", "ja":"🔍 検索:"},
"cat_filter":                 {"zh_TW":"分類過濾:", "zh_CN":"分类过滤:", "en":"Category Filter:", "ja":"カテゴリーフィルター:"},
"all_cats":                   {"zh_TW":"（全部）", "zh_CN":"（全部）", "en":"(All)", "ja":"（全て）"},
"btn_clear_filter":           {"zh_TW":"清除過濾", "zh_CN":"清除过滤", "en":"Clear Filter", "ja":"フィルター解除"},
"total_items":                {"zh_TW":"共 {} 項", "zh_CN":"共 {} 项", "en":"{} items", "ja":"全{}件"},
"col_src":                    {"zh_TW":"來源", "zh_CN":"来源", "en":"Source", "ja":"ソース"},
"col_cat":                    {"zh_TW":"分類", "zh_CN":"分类", "en":"Category", "ja":"分類"},
"col_prop_display":           {"zh_TW":"顯示名稱", "zh_CN":"显示名称", "en":"Display Name", "ja":"表示名"},
"col_dbkey":                  {"zh_TW":"DB Key", "zh_CN":"DB Key", "en":"DB Key", "ja":"DBキー"},
"col_method":                 {"zh_TW":"測試方法", "zh_CN":"测试方法", "en":"Test Method", "ja":"試験方法"},
"src_builtin":                {"zh_TW":"📌內建", "zh_CN":"📌内置", "en":"📌Built-in", "ja":"📌ビルトイン"},
"src_user":                   {"zh_TW":"✏️用戶", "zh_CN":"✏️用户", "en":"✏️User", "ja":"✏️ユーザー"},
"eq_display_name":            {"zh_TW":"(=顯示名稱)", "zh_CN":"(=显示名称)", "en":"(=Display Name)", "ja":"(=表示名)"},
"add_prop_def":               {"zh_TW":"➕ 新增物性定義", "zh_CN":"➕ 新增物性定义", "en":"➕ Add Property Definition", "ja":"➕ 物性定義を追加"},
"lbl_prop_display":           {"zh_TW":"顯示名稱*:", "zh_CN":"显示名称*:", "en":"Display Name*:", "ja":"表示名*:"},
"lbl_prop_dbkey":             {"zh_TW":"DB Key(英文)*:", "zh_CN":"DB Key(英文)*:", "en":"DB Key*:", "ja":"DBキー(英語)*:"},
"lbl_test_method":            {"zh_TW":"測試方法:", "zh_CN":"测试方法:", "en":"Test Method:", "ja":"試験方法:"},
"lbl_target_cat":             {"zh_TW":"目標分類*:", "zh_CN":"目标分类*:", "en":"Target Category*:", "ja":"対象カテゴリー*:"},
"btn_add_mat_cat":           {"zh_TW":"➕ 新增物料種類", "zh_CN":"➕ 新增物料种类", "en":"➕ Add Material Category", "ja":"➕ 材料カテゴリー追加"},
"btn_del_mat_cat":           {"zh_TW":"🗑 刪除自定義種類", "zh_CN":"🗑 删除自定义种类", "en":"🗑 Del Material Category", "ja":"🗑 カテゴリー削除"},
"dlg_add_mat_cat":           {"zh_TW":"新增自定義物料種類", "zh_CN":"新增自定义物料种类", "en":"Add Material Category", "ja":"材料カテゴリー追加"},
"dlg_del_mat_cat":           {"zh_TW":"刪除自定義物料種類", "zh_CN":"删除自定义物料种类", "en":"Delete Material Category", "ja":"材料カテゴリー削除"},
"lbl_mat_cat_key":           {"zh_TW":"內部鍵名*:", "zh_CN":"内部键名*:", "en":"Internal Key*:", "ja":"内部キー*:"},
"lbl_mat_cat_csv":           {"zh_TW":"CSV欄位前綴*:", "zh_CN":"CSV栏位前缀*:", "en":"CSV Column Prefix*:", "ja":"CSVカラム接頭辞*:"},
"lbl_mat_cat_csv_hint":      {"zh_TW":"配方存檔欄位名，如：稀釋劑", "zh_CN":"配方存档栏位名，如：稀释剂", "en":"Recipe save column name", "ja":"レシピ保存カラム名"},
"lbl_mat_cat_key_hint":      {"zh_TW":"程式識別用，如：diluent", "zh_CN":"程序识别用，如：diluent", "en":"For program ID, e.g. diluent", "ja":"プログラム識別用"},
"lbl_basic_info":            {"zh_TW":"基本資訊", "zh_CN":"基本信息", "en":"Basic Info", "ja":"基本情報"},
"lbl_lang_names":            {"zh_TW":"多語言顯示名稱", "zh_CN":"多语言显示名称", "en":"Multilingual Display Names", "ja":"多言語表示名"},
"field_appearance":          {"zh_TW":"外觀", "zh_CN":"外观", "en":"Appearance", "ja":"外観"},
"field_viscosity":           {"zh_TW":"黏度 (cP@25°C)", "zh_CN":"粘度 (cP@25°C)", "en":"Viscosity (cP@25°C)", "ja":"粘度 (cP@25°C)"},
"field_dk":                  {"zh_TW":"介電常數 (Dk)", "zh_CN":"介电常数 (Dk)", "en":"Dielectric Constant (Dk)", "ja":"誘電率 (Dk)"},
"field_surface_energy":      {"zh_TW":"表面能", "zh_CN":"表面能", "en":"Surface Energy", "ja":"表面エネルギー"},
"field_source":              {"zh_TW":"來源/供應商", "zh_CN":"来源/供应商", "en":"Source/Supplier", "ja":"ソース/サプライヤー"},
"lbl_field_select":          {"zh_TW":"選擇此種類包含的欄位:", "zh_CN":"选择此种类包含的栏位:", "en":"Select fields for this category:", "ja":"このカテゴリーのフィールドを選択:"},
"field_eew":                 {"zh_TW":"EEW（參與當量計算）", "zh_CN":"EEW（参与当量计算）", "en":"EEW (stoichiometric calc)", "ja":"EEW（当量計算に参加）"},
"field_type":                {"zh_TW":"類型", "zh_CN":"类型", "en":"Type", "ja":"タイプ"},
"field_structure":           {"zh_TW":"分子結構", "zh_CN":"分子结构", "en":"Molecular Structure", "ja":"分子構造"},
"field_cl":                  {"zh_TW":"氯含量 (ppm)", "zh_CN":"氯含量 (ppm)", "en":"Cl Content (ppm)", "ja":"塩素含有量 (ppm)"},
"warn_mat_cat_key_empty":    {"zh_TW":"請填寫鍵名、CSV前綴及當前語言的顯示名稱", "zh_CN":"请填写键名、CSV前缀及当前语言的显示名称", "en":"Please fill in key, CSV prefix and display name for current language", "ja":"キー、CSVプレフィクス、現在の言語の表示名を入力してください"},
"warn_mat_cat_key_exists":   {"zh_TW":"種類鍵名「{}」已存在", "zh_CN":"种类键名「{}」已存在", "en":"Category key '{}' already exists", "ja":"カテゴリーキー「{}」は既に存在します"},
"mat_cat_added":             {"zh_TW":"已新增物料種類「{}」", "zh_CN":"已新增物料种类「{}」", "en":"Material category '{}' added", "ja":"材料カテゴリー「{}」を追加しました"},
"mat_cat_deleted":           {"zh_TW":"已刪除物料種類「{}」", "zh_CN":"已删除物料种类「{}」", "en":"Material category '{}' deleted", "ja":"材料カテゴリー「{}」を削除しました"},
"no_custom_mat_cat":         {"zh_TW":"目前無自定義物料種類", "zh_CN":"目前无自定义物料种类", "en":"No custom material categories", "ja":"カスタム材料カテゴリーなし"},
"confirm_del_mat_cat":       {"zh_TW":"確定刪除物料種類「{}」？\n（該種類下的所有物料數據將被清除）", "zh_CN":"确定删除物料种类「{}」？\n（该种类下的所有物料数据将被清除）", "en":"Delete category '{}'?\n(All materials in this category will be removed)", "ja":"カテゴリー「{}」を削除しますか？\n（すべての材料データが削除されます）"},
"sec_custom_mat":            {"zh_TW":"{}", "zh_CN":"{}", "en":"{}", "ja":"{}"},
"add_custom_mat":            {"zh_TW":"+ 添加 {}", "zh_CN":"+ 添加 {}", "en":"+ Add {}", "ja":"+ {} 追加"},
"cat_input_hint":             {"zh_TW":"（可選已有分類，或直接輸入新分類名）", "zh_CN":"（可选已有分类，或直接输入新分类名）", "en":"(Select existing or enter new category)", "ja":"（既存カテゴリーを選択または新規入力）"},
"btn_add_cat":               {"zh_TW":"➕ 新增分類", "zh_CN":"➕ 新增分类", "en":"➕ Add Category", "ja":"➕ カテゴリー追加"},
"btn_del_cat":               {"zh_TW":"🗑 刪除自定義分類", "zh_CN":"🗑 删除自定义分类", "en":"🗑 Del Category", "ja":"🗑 カテゴリー削除"},
"dlg_add_cat":               {"zh_TW":"新增自定義分類", "zh_CN":"新增自定义分类", "en":"Add Custom Category", "ja":"カスタムカテゴリー追加"},
"lbl_cat_key":               {"zh_TW":"內部鍵名*:", "zh_CN":"内部键名*:", "en":"Internal Key*:", "ja":"内部キー*:"},
"lbl_cat_key_hint":          {"zh_TW":"（如 8.散熱屬性，建議數字開頭以排序）", "zh_CN":"（如 8.散热属性，建议数字开头以排序）", "en":"(e.g. 8.Heat Dissipation, number prefix for sorting)", "ja":"（例: 8.放熱特性, ソート用に数字で開始推奨）"},
"lbl_lang_zh_tw":            {"zh_TW":"正體中文:", "zh_CN":"正体中文:", "en":"Trad. Chinese:", "ja":"繁体中文:"},
"lbl_lang_zh_cn":            {"zh_TW":"簡體中文:", "zh_CN":"简体中文:", "en":"Simp. Chinese:", "ja":"簡体中文:"},
"lbl_lang_en":               {"zh_TW":"English:", "zh_CN":"English:", "en":"English:", "ja":"English:"},
"lbl_lang_ja":               {"zh_TW":"日本語:", "zh_CN":"日本语:", "en":"Japanese:", "ja":"日本語:"},
"warn_cat_key_empty":        {"zh_TW":"請輸入內部鍵名和當前語言的顯示名稱", "zh_CN":"请输入内部键名和当前语言的显示名称", "en":"Please enter internal key and display name for current language", "ja":"内部キーと現在の言語の表示名を入力してください"},
"warn_cat_key_exists":       {"zh_TW":"分類鍵名「{}」已存在", "zh_CN":"分类键名「{}」已存在", "en":"Category key '{}' already exists", "ja":"カテゴリーキー「{}」は既に存在します"},
"cat_added":                 {"zh_TW":"已新增分類「{}」", "zh_CN":"已新增分类「{}」", "en":"Category '{}' added", "ja":"カテゴリー「{}」を追加しました"},
"no_custom_cat_del":         {"zh_TW":"目前無自定義分類可刪除", "zh_CN":"目前无自定义分类可删除", "en":"No custom categories to delete", "ja":"削除可能なカスタムカテゴリーなし"},
"dlg_del_cat":               {"zh_TW":"刪除自定義分類", "zh_CN":"删除自定义分类", "en":"Delete Custom Category", "ja":"カスタムカテゴリー削除"},
"confirm_del_cat":           {"zh_TW":"確定刪除分類「{}」？\n（該分類下的物性定義不會被刪除，但會歸入「7.自定義」）", "zh_CN":"确定删除分类「{}」？\n（该分类下的物性定义不会被删除，但会归入「7.自定义」）", "en":"Delete category '{}'?\n(Properties won't be deleted, moved to '7.Custom')", "ja":"カテゴリー「{}」を削除しますか？\n（物性定義は削除されず「7.カスタム」に移動）"},
"cat_deleted":               {"zh_TW":"已刪除分類「{}」", "zh_CN":"已删除分类「{}」", "en":"Category '{}' deleted", "ja":"カテゴリー「{}」を削除しました"},
"btn_add_prop":               {"zh_TW":"✅ 新增", "zh_CN":"✅ 新增", "en":"✅ Add", "ja":"✅ 追加"},
"btn_del_prop":               {"zh_TW":"🗑 刪除選中使用者項目", "zh_CN":"🗑 删除选中用户项目", "en":"🗑 Delete Selected User Item", "ja":"🗑 選択ユーザー項目を削除"},
"btn_copy_prop":              {"zh_TW":"📋 複製選中項目到新增欄", "zh_CN":"📋 复制选中项目到新增栏", "en":"📋 Copy Selected to Add Form", "ja":"📋 選択項目を追加欄にコピー"},
"warn_enter_disp_name":       {"zh_TW":"請輸入顯示名稱", "zh_CN":"请输入显示名称", "en":"Please enter display name", "ja":"表示名を入力してください"},
"warn_enter_cat":             {"zh_TW":"請選擇或輸入目標分類", "zh_CN":"请选择或输入目标分类", "en":"Please select or enter target category", "ja":"対象カテゴリーを選択または入力してください"},
"warn_enter_dbkey":           {"zh_TW":"請輸入DB Key（英文鍵名，用於數據庫存儲）", "zh_CN":"请输入DB Key（英文键名，用于数据库存储）", "en":"Please enter DB Key (English key for database storage)", "ja":"DBキーを入力してください（データベース保存用の英語キー）"},
"warn_dbkey_format":          {"zh_TW":"DB Key 只能包含英文字母、數字、底線和連字號", "zh_CN":"DB Key 只能包含英文字母、数字、下划线和连字号", "en":"DB Key: only letters, digits, underscore, hyphen", "ja":"DBキーは英字・数字・アンダースコア・ハイフンのみ"},
"warn_name_exists":           {"zh_TW":"顯示名稱「{}」已存在，請使用不同名稱", "zh_CN":"显示名称「{}」已存在，请使用不同名称", "en":"Display name '{}' already exists", "ja":"表示名「{}」は既に存在します"},
"warn_dbkey_exists":          {"zh_TW":"DB Key「{}」已存在，請使用不同鍵名", "zh_CN":"DB Key「{}」已存在，请使用不同键名", "en":"DB Key '{}' already exists", "ja":"DBキー「{}」は既に存在します"},
"prop_added":                 {"zh_TW":"已將「{}」(DB: {}) 新增至「{}」，物性表單已更新", "zh_CN":"已将「{}」(DB: {}) 新增至「{}」，物性表单已更新", "en":"Added '{}' (DB: {}) to '{}'. Form updated.", "ja":"「{}」(DB: {})を「{}」に追加しました。フォーム更新済み"},
"add_ok":                     {"zh_TW":"新增成功", "zh_CN":"新增成功", "en":"Added Successfully", "ja":"追加成功"},
"warn_select_item":           {"zh_TW":"請先選擇要刪除的項目", "zh_CN":"请先选择要删除的项目", "en":"Please select an item to delete", "ja":"削除する項目を選択してください"},
"confirm_del_builtin":        {"zh_TW":"確定刪除內建屬性「{}」？\n可點「恢復內建預設」還原。", "zh_CN":"确定删除内置属性「{}」？\n可点「恢复内置预设」还原。", "en":"Delete built-in '{}' ?\nCan be restored later.", "ja":"ビルトイン「{}」を削除しますか？\n後で復元可能です。"},
"confirm_del_user":           {"zh_TW":"確定刪除使用者屬性「{}」？\n（已填入此屬性的配方數據不受影響）", "zh_CN":"确定删除用户属性「{}」？\n（已填入此属性的配方数据不受影响）", "en":"Delete user property '{}' ?\n(Existing recipe data unaffected)", "ja":"ユーザー物性「{}」を削除しますか？\n（既存データに影響なし）"},
"confirm_delete_title":       {"zh_TW":"確認刪除", "zh_CN":"确认删除", "en":"Confirm Delete", "ja":"削除確認"},
"deleted":                    {"zh_TW":"已刪除「{}」", "zh_CN":"已删除「{}」", "en":"Deleted '{}'", "ja":"「{}」を削除しました"},
"no_deleted_builtins":        {"zh_TW":"目前沒有被刪除的內建項目", "zh_CN":"目前没有被删除的内置项目", "en":"No deleted built-in items", "ja":"削除されたビルトイン項目なし"},
"restored_builtins":          {"zh_TW":"已恢復 {} 個內建物性定義", "zh_CN":"已恢复 {} 个内置物性定义", "en":"Restored {} built-in property definitions", "ja":"{}件のビルトイン物性定義を復元しました"},
"restore_ok":                 {"zh_TW":"恢復完成", "zh_CN":"恢复完成", "en":"Restore Complete", "ja":"復元完了"},
# ── RecipeTab 其他操作 ──
"warn_select_recipe":         {"zh_TW":"請先選擇配方", "zh_CN":"请先选择配方", "en":"Please select a recipe first", "ja":"配合を選択してください"},
"warn_select_recipe_first":   {"zh_TW":"請先選擇一個配方", "zh_CN":"请先选择一个配方", "en":"Please select a recipe first", "ja":"配合を選択してください"},
"warn_no_props":              {"zh_TW":"尚未填寫任何物性數值", "zh_CN":"尚未填写任何物性数值", "en":"No property values entered", "ja":"物性値が未入力です"},
"props_saved":                {"zh_TW":"已儲存 {} 項物性數據至配方行", "zh_CN":"已保存 {} 项物性数据至配方行", "en":"Saved {} property values to recipe", "ja":"{}件の物性データを配合に保存しました"},
"props_save_ok":              {"zh_TW":"成功", "zh_CN":"成功", "en":"Success", "ja":"成功"},
"props_save_err":             {"zh_TW":"找不到對應配方行，請確認配方已存在於數據庫", "zh_CN":"找不到对应配方行，请确认配方已存在于数据库", "en":"Recipe not found in database", "ja":"データベースに配合が見つかりません"},
"rename_title":               {"zh_TW":"重命名", "zh_CN":"重命名", "en":"Rename", "ja":"名前変更"},
"rename_prompt":              {"zh_TW":"將「{}」重命名為：", "zh_CN":"将「{}」重命名为：", "en":"Rename '{}' to:", "ja":"「{}」の新しい名前:"},
"name_already_exists":        {"zh_TW":"名稱「{}」已存在", "zh_CN":"名称「{}」已存在", "en":"Name '{}' already exists", "ja":"名前「{}」は既に存在します"},
"renamed_ok":                 {"zh_TW":"已重命名為「{}」", "zh_CN":"已重命名为「{}」", "en":"Renamed to '{}'", "ja":"「{}」に名前変更しました"},
"confirm_del_recipe":         {"zh_TW":"確定刪除配方「{}」？\n（包含所有已錄入的物性數據）", "zh_CN":"确定删除配方「{}」？\n（包含所有已录入的物性数据）", "en":"Delete recipe '{}' ?\n(All property data will be lost)", "ja":"配合「{}」を削除しますか？\n（全物性データも削除されます）"},
"deleted_recipe":             {"zh_TW":"已刪除「{}」", "zh_CN":"已删除「{}」", "en":"Deleted '{}'", "ja":"「{}」を削除しました"},
"copy_recipe_ok":             {"zh_TW":"已複製「{}」配方數據（垂直表格格式）\n可在 Excel 中 Ctrl+V 貼上。", "zh_CN":"已复制「{}」配方数据（垂直表格格式）\n可在 Excel 中 Ctrl+V 粘贴。", "en":"Copied '{}' recipe data (vertical format)\nPaste in Excel with Ctrl+V.", "ja":"「{}」の配合データをコピーしました（縦書きExcel形式）\nExcelでCtrl+Vで貼り付け可能"},
"copy_ok_title":              {"zh_TW":"複製成功", "zh_CN":"复制成功", "en":"Copy Success", "ja":"コピー成功"},

# ── CalcTab 計算模式 ──
"mode_stoich":                {"zh_TW":"stoich (按當量配比)", "zh_CN":"stoich (按当量配比)", "en":"stoich (Stoichiometric)", "ja":"stoich (当量比)"},
"mode_weight":                {"zh_TW":"weight (按樹脂總量百分比)", "zh_CN":"weight (按树脂总量百分比)", "en":"weight (Wt% of Resin)", "ja":"weight (樹脂質量比)"},
"mode_target100":             {"zh_TW":"target_100 (目標總重 100g)", "zh_CN":"target_100 (目标总重 100g)", "en":"target_100 (Target 100g)", "ja":"target_100 (目標100g)"},
# ── CalcTab 取整選項 ──
"round_none":                 {"zh_TW":"不取整", "zh_CN":"不取整", "en":"No Round", "ja":"丸めなし"},
"round_int":                  {"zh_TW":"整數", "zh_CN":"整数", "en":"Integer", "ja":"整数"},
"round_1dp":                  {"zh_TW":"1位小數", "zh_CN":"1位小数", "en":"1 d.p.", "ja":"小数1桁"},
"round_2dp":                  {"zh_TW":"2位小數", "zh_CN":"2位小数", "en":"2 d.p.", "ja":"小数2桁"},
# ── CalcTab 結果表 ──
"col_mat_name":               {"zh_TW":"物料名稱", "zh_CN":"物料名称", "en":"Material Name", "ja":"材料名"},
"col_mass_g_result":          {"zh_TW":"質量 (g)", "zh_CN":"质量 (g)", "en":"Mass (g)", "ja":"質量 (g)"},
"col_pct_result":             {"zh_TW":"佔比 (%)", "zh_CN":"占比 (%)", "en":"Ratio (%)", "ja":"配合比 (%)"},
"col_cl_result":              {"zh_TW":"氯 (ppm)", "zh_CN":"氯 (ppm)", "en":"Cl (ppm)", "ja":"塩素 (ppm)"},
"total":                      {"zh_TW":"總計", "zh_CN":"总计", "en":"Total", "ja":"合計"},
"err_ratio_not_100g":         {"zh_TW":"非 '目標100g' 模式不允許使用樹脂比例(待算)", "zh_CN":"非 '目标100g' 模式不允许使用树脂比例(待算)", "en":"Ratio resins only allowed in Target 100g mode", "ja":"比率樹脂は目標100gモードでのみ使用可能"},
"err_coeff_zero":             {"zh_TW":"無法計算：變動部分係數為0", "zh_CN":"无法计算：变动部分系数为0", "en":"Cannot calculate: variable coefficient is 0", "ja":"計算不可：変動係数が0"},
"err_over_100g":              {"zh_TW":"無法配平至100g：固定質量已超過目標", "zh_CN":"无法配平至100g：固定质量已超过目标", "en":"Cannot balance to 100g: fixed mass exceeds target", "ja":"100g配合不可：固定質量が目標を超過"},
# ── CalcTab 複製表頭 ──
"copy_hdr":                   {"zh_TW":"物料名稱\t質量 (g)\t佔比 (%)\t氯含量 (ppm)", "zh_CN":"物料名称\t质量 (g)\t占比 (%)\t氯含量 (ppm)", "en":"Material\tMass (g)\tRatio (%)\tCl (ppm)", "ja":"材料名\t質量 (g)\t配合比 (%)\t塩素 (ppm)"},
# ── RecipeTab 複製表頭 ──
"copy_recipe_hdr_name":       {"zh_TW":"配方名稱", "zh_CN":"配方名称", "en":"Recipe Name", "ja":"配合名"},
"copy_recipe_hdr_batch":      {"zh_TW":"批次號", "zh_CN":"批次号", "en":"Batch No.", "ja":"ロット番号"},
"copy_recipe_hdr_mat":        {"zh_TW":"物料名稱\t質量(g)\t佔比(%)", "zh_CN":"物料名称\t质量(g)\t占比(%)", "en":"Material\tMass(g)\tRatio(%)", "ja":"材料名\t質量(g)\t配合比(%)"},
"copy_recipe_hdr_prop":       {"zh_TW":"物性項目\t數值", "zh_CN":"物性项目\t数值", "en":"Property\tValue", "ja":"物性項目\t値"},
# ── 物料DB欄位顯示名 ──
"matcol_name":                {"zh_TW":"名稱", "zh_CN":"名称", "en":"Name", "ja":"名称"},
"matcol_type":                {"zh_TW":"類型", "zh_CN":"类型", "en":"Type", "ja":"タイプ"},
"matcol_appearance":          {"zh_TW":"外觀特性", "zh_CN":"外观特性", "en":"Appearance", "ja":"外観特性"},
"matcol_viscosity":           {"zh_TW":"粘度", "zh_CN":"粘度", "en":"Viscosity", "ja":"粘度"},
"matcol_dk":                  {"zh_TW":"介電常數", "zh_CN":"介电常数", "en":"Dielectric Const.", "ja":"誘電率"},
"matcol_surface_energy":      {"zh_TW":"表面能", "zh_CN":"表面能", "en":"Surface Energy", "ja":"表面エネルギー"},
"matcol_structure":           {"zh_TW":"分子結構", "zh_CN":"分子结构", "en":"Molecular Structure", "ja":"分子構造"},
"matcol_eew_ahew":            {"zh_TW":"EEW/當量", "zh_CN":"EEW/当量", "en":"EEW/AHEW", "ja":"EEW/当量"},
"matcol_cl":                  {"zh_TW":"氯", "zh_CN":"氯", "en":"Cl", "ja":"塩素"},
"matcol_source":              {"zh_TW":"來源", "zh_CN":"来源", "en":"Source", "ja":"出典"},
"matcol_desc":                {"zh_TW":"備註", "zh_CN":"备注", "en":"Notes", "ja":"備考"},
# ── 物性分類名 ──
"propcat_1":                  {"zh_TW":"1.未固化屬性", "zh_CN":"1.未固化属性", "en":"1.Uncured Properties", "ja":"1.未硬化特性"},
"propcat_2":                  {"zh_TW":"2.固化過程", "zh_CN":"2.固化过程", "en":"2.Curing Process", "ja":"2.硬化プロセス"},
"propcat_3":                  {"zh_TW":"3.機械屬性", "zh_CN":"3.机械属性", "en":"3.Mechanical Properties", "ja":"3.機械的特性"},
"propcat_4":                  {"zh_TW":"4.熱屬性", "zh_CN":"4.热属性", "en":"4.Thermal Properties", "ja":"4.熱的特性"},
"propcat_5":                  {"zh_TW":"5.化學環境", "zh_CN":"5.化学环境", "en":"5.Chemical Resistance", "ja":"5.耐薬品性"},
"propcat_6":                  {"zh_TW":"6.電屬性", "zh_CN":"6.电属性", "en":"6.Electrical Properties", "ja":"6.電気的特性"},
"propcat_custom":             {"zh_TW":"7.自定義", "zh_CN":"7.自定义", "en":"7.Custom", "ja":"7.カスタム"},
# ── 配方詳情 ──
"detail_recipe":              {"zh_TW":"配方：", "zh_CN":"配方：", "en":"Recipe: ", "ja":"配合："},
"detail_batch":               {"zh_TW":"批次號：", "zh_CN":"批次号：", "en":"Batch No.: ", "ja":"ロット番号："},
"detail_date":                {"zh_TW":"建立日期：", "zh_CN":"创建日期：", "en":"Date: ", "ja":"作成日："},
"detail_mode":                {"zh_TW":"計算模式：", "zh_CN":"计算模式：", "en":"Calc Mode: ", "ja":"計算モード："},
"detail_total":               {"zh_TW":"總質量：", "zh_CN":"总质量：", "en":"Total Mass: ", "ja":"総質量："},
"detail_cl":                  {"zh_TW":"總氯：", "zh_CN":"总氯：", "en":"Total Cl: ", "ja":"総塩素："},
"detail_materials":           {"zh_TW":"─── 物料明細 ───", "zh_CN":"─── 物料明细 ───", "en":"─── Material Detail ───", "ja":"─── 材料明細 ───"},
"lang_restart":               {"zh_TW":"語言已切換，正在重建介面…", "zh_CN":"语言已切换，正在重建界面…", "en":"Language changed. Rebuilding UI…", "ja":"言語を変更しました。UIを再構築中…"},

"ratio_pending":              {"zh_TW":"比例(待算)", "zh_CN":"比例(待算)", "en":"Ratio(Calc)", "ja":"比率(計算)"},
"tab_recipe_mgr":             {"zh_TW":"📂 配方管理", "zh_CN":"📂 配方管理", "en":"📂 Recipe Manager", "ja":"📂 配合管理"},
"recipe_list_title":          {"zh_TW":"📋 配方清單", "zh_CN":"📋 配方列表", "en":"📋 Recipe List", "ja":"📋 配合リスト"},
"btn_refresh":                {"zh_TW":"🔄 刷新", "zh_CN":"🔄 刷新", "en":"🔄 Refresh", "ja":"🔄 更新"},
"recipe_composition":         {"zh_TW":"📄 配方組成", "zh_CN":"📄 配方组成", "en":"📄 Recipe Composition", "ja":"📄 配合組成"},
"prop_input":                 {"zh_TW":"🔬 物性數據錄入", "zh_CN":"🔬 物性数据录入", "en":"🔬 Property Data Entry", "ja":"🔬 物性データ入力"},
"btn_save_all_props":         {"zh_TW":"💾 儲存所有已填物性數據", "zh_CN":"💾 保存所有已填物性数据", "en":"💾 Save All Properties", "ja":"💾 全物性データを保存"},
"btn_clear_all_props":        {"zh_TW":"🗑 清空所有物性欄位", "zh_CN":"🗑 清空所有物性字段", "en":"🗑 Clear All Properties", "ja":"🗑 全物性フィールドをクリア"},
"btn_toggle_expand":          {"zh_TW":"▲▼ 全部展開/折疊", "zh_CN":"▲▼ 全部展开/折叠", "en":"▲▼ Expand/Collapse All", "ja":"▲▼ 全て展開/折畳"},
"col_mgr_ok":                 {"zh_TW":"確定", "zh_CN":"确定", "en":"OK", "ja":"OK"},
"confirm_restore":            {"zh_TW":"確認恢復", "zh_CN":"确认恢复", "en":"Confirm Restore", "ja":"復元確認"},
"restore_msg":                {"zh_TW":"將恢復以下 {} 個內建項目：", "zh_CN":"将恢复以下 {} 个内置项目：", "en":"Restore {} built-in items:", "ja":"以下{}件のビルトイン項目を復元:"},
"restored_n":                 {"zh_TW":"已恢復 {} 個內建項目", "zh_CN":"已恢复 {} 个内置项目", "en":"Restored {} built-in items", "ja":"{}件のビルトイン項目を復元しました"},
"detail_date_mode":           {"zh_TW":"日期：{}   模式：{}", "zh_CN":"日期：{}   模式：{}", "en":"Date: {}   Mode: {}", "ja":"日付：{}   モード：{}"},
"detail_total_cl":            {"zh_TW":"{} g    氯：{} ppm", "zh_CN":"{} g    氯：{} ppm", "en":"{} g    Cl: {} ppm", "ja":"{} g    塩素：{} ppm"},
"detail_eq":                  {"zh_TW":"  當量={}  {}", "zh_CN":"  当量={}  {}", "en":"  Eq.={}  {}", "ja":"  当量={}  {}"},
"deleted_fmt":                {"zh_TW":"已刪除「{}」", "zh_CN":"已删除「{}」", "en":"Deleted '{}'", "ja":"「{}」を削除しました"},
"confirm_delete_title2":      {"zh_TW":"確認刪除", "zh_CN":"确认删除", "en":"Confirm Delete", "ja":"削除確認"},
"col_custom_tag":             {"zh_TW":"自定義", "zh_CN":"自定义", "en":"Custom", "ja":"カスタム"},
"detail_recipe_fmt":          {"zh_TW":"配方：{}", "zh_CN":"配方：{}", "en":"Recipe: {}", "ja":"配合：{}"},
"detail_batch_fmt":           {"zh_TW":"批次號：{}", "zh_CN":"批次号：{}", "en":"Batch No.: {}", "ja":"ロット番号：{}"},
"unit_tooltip":               {"zh_TW":"單位: {}\n方法: {}", "zh_CN":"单位: {}\n方法: {}", "en":"Unit: {}\nMethod: {}", "ja":"単位: {}\n方法: {}"},
}

def _load_lang():
    global _CURRENT_LANG
    if os.path.exists(LANG_CFG_FILE):
        try:
            with open(LANG_CFG_FILE, 'r', encoding='utf-8') as f:
                d = json.load(f)
                if d.get('lang') in SUPPORTED_LANGS:
                    _CURRENT_LANG = d['lang']
        except: pass

def _save_lang(lang):
    global _CURRENT_LANG
    _CURRENT_LANG = lang
    try:
        with open(LANG_CFG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"lang": lang}, f)
    except: pass

def T(key, *args):
    entry = _TRANSLATIONS.get(key)
    if not entry: return key
    text = entry.get(_CURRENT_LANG) or entry.get("zh_TW", key)
    if args:
        try: text = text.format(*args)
        except: pass
    return text

_load_lang()

_PROPCAT_MAP = {
    "1.未固化屬性": "propcat_1", "2.固化過程": "propcat_2",
    "3.機械屬性": "propcat_3", "4.熱屬性": "propcat_4",
    "5.化學環境": "propcat_5", "6.電屬性": "propcat_6",
    "7.自定義": "propcat_custom",
}

# ── 自定義分類系統 ──
CUSTOM_CAT_CFG_FILE = "custom_categories.json"
# 每條: {"key":"8.xxx", "zh_TW":"…", "zh_CN":"…", "en":"…", "ja":"…"}
_custom_cats = []

def _load_custom_cats():
    global _custom_cats
    if os.path.exists(CUSTOM_CAT_CFG_FILE):
        try:
            with open(CUSTOM_CAT_CFG_FILE, 'r', encoding='utf-8') as f:
                _custom_cats = json.load(f)
        except: _custom_cats = []

def _save_custom_cats():
    try:
        with open(CUSTOM_CAT_CFG_FILE, 'w', encoding='utf-8') as f:
            json.dump(_custom_cats, f, ensure_ascii=False, indent=2)
    except: pass

_load_custom_cats()

def T_propcat(cat):
    """Translate a category internal key to display name."""
    # Check builtin mapping first
    tkey = _PROPCAT_MAP.get(cat)
    if tkey: return T(tkey)
    # Check custom categories
    for cc in _custom_cats:
        if cc.get("key") == cat:
            return cc.get(_CURRENT_LANG) or cc.get("zh_TW", cat)
    return cat

def _propcat_reverse(display):
    """Reverse map a displayed category name back to internal key."""
    # Check builtin
    for internal_key, tkey in _PROPCAT_MAP.items():
        if T(tkey) == display: return internal_key
    # Check custom
    for cc in _custom_cats:
        for lang in SUPPORTED_LANGS:
            if cc.get(lang) == display: return cc["key"]
    # If not found, it IS the key (user typed raw text)
    return display

def _get_all_cat_display():
    """Return list of (internal_key, display_name) for all categories."""
    result = []
    for k in PREDEFINED_PROPS.keys():
        result.append((k, T_propcat(k)))
    for cc in _custom_cats:
        key = cc["key"]
        if key not in [r[0] for r in result]:
            result.append((key, T_propcat(key)))
    return result

def get_cat_cn():
    return {
        "resins": T("cat_resins"), "hardeners": T("cat_hardeners"),
        "additives": T("cat_additives"), "fillers": T("cat_fillers"),
        "catalysts": T("cat_catalysts")
    }


# ── 自定義物料種類系統 ──
CUSTOM_MAT_CAT_FILE = "custom_mat_cats.json"
_custom_mat_cats = []

def _load_custom_mat_cats():
    global _custom_mat_cats
    if os.path.exists(CUSTOM_MAT_CAT_FILE):
        try:
            with open(CUSTOM_MAT_CAT_FILE, 'r', encoding='utf-8') as f:
                _custom_mat_cats = json.load(f)
        except: _custom_mat_cats = []

def _save_custom_mat_cats():
    try:
        with open(CUSTOM_MAT_CAT_FILE, 'w', encoding='utf-8') as f:
            json.dump(_custom_mat_cats, f, ensure_ascii=False, indent=2)
    except: pass

_load_custom_mat_cats()

def get_mat_cat_display(key):
    """Translate a material category key to current language display name."""
    disp = get_cat_cn()
    if key in disp: return disp[key]
    for mc in _custom_mat_cats:
        if mc['key'] == key:
            return mc.get(_CURRENT_LANG) or mc.get('zh_TW', key)
    return key

def get_all_cat_display():
    """Return dict of ALL material categories: key → translated display name."""
    d = dict(get_cat_cn())
    for mc in _custom_mat_cats:
        d[mc['key']] = mc.get(_CURRENT_LANG) or mc.get('zh_TW', mc['key'])
    return d

def get_all_slot_counts():
    """Merged builtin + custom slot counts. Custom cats use 20 (virtually unlimited)."""
    d = dict(SLOT_COUNTS)
    for mc in _custom_mat_cats:
        d[mc['key']] = 20
    return d

def get_all_slot_fields():
    """Merged builtin + custom slot fields."""
    d = dict(SLOT_FIELDS)
    for mc in _custom_mat_cats:
        fields = ["名稱", "質量_g", "佔比%"]
        if mc.get('has_eew'):            fields.append("EEW")
        if mc.get('has_type'):           fields.append("類型")
        if mc.get('has_appearance'):     fields.append("外觀")
        if mc.get('has_viscosity'):      fields.append("黏度")
        if mc.get('has_dk'):             fields.append("Dk")
        if mc.get('has_surface_energy'): fields.append("表面能")
        if mc.get('has_structure'):      fields.append("分子結構")
        if mc.get('has_cl'):             fields.append("氯_ppm")
        if mc.get('has_source'):         fields.append("來源")
        d[mc['key']] = fields
    return d

def get_all_cat_cn():
    """Merged builtin + custom cat→csv_prefix mapping."""
    d = dict(CAT_CN)
    for mc in _custom_mat_cats:
        d[mc['key']] = mc.get('csv_name', mc.get('zh_TW', mc['key']))
    return d

def _get_custom_mat_cat(key):
    """Return custom mat cat config dict or None."""
    for mc in _custom_mat_cats:
        if mc['key'] == key: return mc
    return None


# ─────────────── 檔案常數 ───────────────
MAT_DB_FILE      = "epoxy_db.csv"
RECIPE_DB_FILE   = "recipe_database.csv"
CUSTOM_PROP_FILE = "custom_properties.csv"
MAT_COL_CFG_FILE = "mat_col_config.json"

SLOT_COUNTS = {"resins": 4, "hardeners": 4, "additives": 3,
               "fillers": 3, "catalysts": 3}

SLOT_FIELDS = {
    "resins":    ["名稱","質量_g","佔比%","EEW","類型","分子結構","氯_ppm"],
    "hardeners": ["名稱","質量_g","佔比%","當量","子類型","校正%","分子結構","氯_ppm"],
    "additives": ["名稱","質量_g","佔比%","類型","氯_ppm"],
    "fillers":   ["名稱","質量_g","佔比%","類型","氯_ppm"],
    "catalysts": ["名稱","質量_g","佔比%","類型","氯_ppm"],
}
CAT_CN = {"resins":"樹脂","hardeners":"固化劑",
          "additives":"助劑","fillers":"填料","catalysts":"催化劑"}

# ─────────────── 物料數據庫欄位定義 ───────────────
# db_key: CSV/內部鍵名(英文), display: 界面顯示名, unit: 單位, data_key: 材料dict中的鍵
# special欄位有特殊處理邏輯(EEW/當量按類別切換)，不參與通用存取
def _get_builtin_mat_cols():
    return [
        {"db_key":"Name",       "display":T("matcol_name"),  "unit":"",          "data_key":"_name",     "visible":True, "builtin":True, "locked":True},
        {"db_key":"Type",       "display":T("matcol_type"),  "unit":"",          "data_key":"type",      "visible":True, "builtin":True},
        {"db_key":"Appearance", "display":T("matcol_appearance"),"unit":"",      "data_key":"appearance","visible":True, "builtin":True},
        {"db_key":"Viscosity_cP25","display":T("matcol_viscosity"),"unit":"cP(25℃)","data_key":"viscosity","visible":True,"builtin":True},
        {"db_key":"Dk",         "display":T("matcol_dk"),    "unit":"",          "data_key":"dk",        "visible":True, "builtin":True},
        {"db_key":"Surface_Energy","display":T("matcol_surface_energy"),"unit":"mN/m(25℃)","data_key":"surface_energy","visible":True,"builtin":True},
        {"db_key":"Molecular_Structure","display":T("matcol_structure"),"unit":"","data_key":"structure","visible":True,"builtin":True},
        {"db_key":"EEW_AHEW",  "display":T("matcol_eew_ahew"),"unit":"",        "data_key":"_eq",       "visible":True, "builtin":True, "special":True},
        {"db_key":"Cl_ppm",    "display":T("matcol_cl"),     "unit":"ppm",       "data_key":"cl",        "visible":True, "builtin":True},
        {"db_key":"Source",     "display":T("matcol_source"), "unit":"",          "data_key":"source",    "visible":False,"builtin":True},
        {"db_key":"Description","display":T("matcol_desc"),   "unit":"",          "data_key":"desc",      "visible":False,"builtin":True},
    ]


_PROP_DISPLAY = {
"粘度 (cP, 25°C)":{"zh_CN":"粘度 (cP, 25°C)","en":"Viscosity (cP, 25°C)","ja":"粘度 (cP, 25°C)"},
"蒸氣壓 (Pa)":{"zh_CN":"蒸气压 (Pa)","en":"Vapor Pressure (Pa)","ja":"蒸気圧 (Pa)"},
"接觸角 (°)":{"zh_CN":"接触角 (°)","en":"Contact Angle (°)","ja":"接触角 (°)"},
"反應放熱峰 (J/g)":{"zh_CN":"反应放热峰 (J/g)","en":"Exotherm Peak (J/g)","ja":"反応発熱ピーク (J/g)"},
"保質期 (D)":{"zh_CN":"保质期 (D)","en":"Shelf Life (D)","ja":"保存期間 (D)"},
"固含量 (%)":{"zh_CN":"固含量 (%)","en":"Solid Content (%)","ja":"固形分 (%)"},
"比重 (g/cm³)":{"zh_CN":"比重 (g/cm³)","en":"Specific Gravity (g/cm³)","ja":"比重 (g/cm³)"},
"顏色 (Gardner)":{"zh_CN":"颜色 (Gardner)","en":"Color (Gardner)","ja":"色調 (Gardner)"},
"VOC含量 (g/L)":{"zh_CN":"VOC含量 (g/L)","en":"VOC Content (g/L)","ja":"VOC含有量 (g/L)"},
"軟化點 (°C)":{"zh_CN":"软化点 (°C)","en":"Softening Point (°C)","ja":"軟化点 (°C)"},
"適用期 Pot Life (d)":{"zh_CN":"适用期 Pot Life (d)","en":"Pot Life (d)","ja":"ポットライフ (d)"},
"保質期 Shelf Life (h)":{"zh_CN":"保质期 Shelf Life (h)","en":"Shelf Life (h)","ja":"シェルフライフ (h)"},
"固化時間-室溫 (h)":{"zh_CN":"固化时间-室温 (h)","en":"Cure Time-RT (h)","ja":"硬化時間-室温 (h)"},
"固化時間-高溫 (h)":{"zh_CN":"固化时间-高温 (h)","en":"Cure Time-Elevated (h)","ja":"硬化時間-高温 (h)"},
"峰值放熱溫度 (°C)":{"zh_CN":"峰值放热温度 (°C)","en":"Peak Exotherm (°C)","ja":"発熱ピーク温度 (°C)"},
"收縮率 (%)":{"zh_CN":"收缩率 (%)","en":"Shrinkage (%)","ja":"収縮率 (%)"},
"高溫凝膠-測試溫度 (°C)":{"zh_CN":"高温凝胶-测试温度 (°C)","en":"HT Gel-Test Temp (°C)","ja":"高温ゲル-試験温度 (°C)"},
"高溫凝膠-拉絲時間":{"zh_CN":"高温凝胶-拉丝时间","en":"HT Gel-String Time","ja":"高温ゲル-糸引き時間"},
"高溫凝膠-固化時間":{"zh_CN":"高温凝胶-固化时间","en":"HT Gel-Cure Time","ja":"高温ゲル-硬化時間"},
"拉伸強度 (MPa)":{"zh_CN":"拉伸强度 (MPa)","en":"Tensile Strength (MPa)","ja":"引張強度 (MPa)"},
"斷裂伸長率 (%)":{"zh_CN":"断裂伸长率 (%)","en":"Elongation at Break (%)","ja":"破断伸び (%)"},
"剪切強度-鋁 (MPa)":{"zh_CN":"剪切强度-铝 (MPa)","en":"Lap Shear-Al (MPa)","ja":"せん断強度-Al (MPa)"},
"剪切強度-鋼 (MPa)":{"zh_CN":"剪切强度-钢 (MPa)","en":"Lap Shear-Steel (MPa)","ja":"せん断強度-鋼 (MPa)"},
"壓縮強度 (MPa)":{"zh_CN":"压缩强度 (MPa)","en":"Compressive Str. (MPa)","ja":"圧縮強度 (MPa)"},
"彎曲強度 (MPa)":{"zh_CN":"弯曲强度 (MPa)","en":"Flexural Str. (MPa)","ja":"曲げ強度 (MPa)"},
"剝離強度 (N/mm)":{"zh_CN":"剥离强度 (N/mm)","en":"Peel Strength (N/mm)","ja":"剥離強度 (N/mm)"},
"衝擊強度 (J/m)":{"zh_CN":"冲击强度 (J/m)","en":"Impact Strength (J/m)","ja":"衝撃強度 (J/m)"},
"拉伸模量 (GPa)":{"zh_CN":"拉伸模量 (GPa)","en":"Tensile Modulus (GPa)","ja":"引張弾性率 (GPa)"},
"彎曲模量 (GPa)":{"zh_CN":"弯曲模量 (GPa)","en":"Flexural Modulus (GPa)","ja":"曲げ弾性率 (GPa)"},
"附著力-鋼 (MPa)":{"zh_CN":"附着力-钢 (MPa)","en":"Adhesion-Steel (MPa)","ja":"付着力-鋼 (MPa)"},
"硬度 Rockwell M (HRM)":{"zh_CN":"硬度 Rockwell M (HRM)","en":"Rockwell M (HRM)","ja":"ロックウェル硬度 M"},
"邵氏硬度 Shore A":{"zh_CN":"邵氏硬度 Shore A","en":"Shore A Hardness","ja":"ショア硬度 A"},
"邵氏硬度 Shore D":{"zh_CN":"邵氏硬度 Shore D","en":"Shore D Hardness","ja":"ショア硬度 D"},
"熱畸變溫度 HDT (°C)":{"zh_CN":"热畸变温度 HDT (°C)","en":"HDT (°C)","ja":"荷重たわみ温度 HDT (°C)"},
"玻璃轉移溫度 Tg (°C)":{"zh_CN":"玻璃转变温度 Tg (°C)","en":"Tg (°C)","ja":"ガラス転移温度 Tg (°C)"},
"熱分解溫度 Td (°C)":{"zh_CN":"热分解温度 Td (°C)","en":"Td (°C)","ja":"熱分解温度 Td (°C)"},
"熱膨脹係數 CTE (ppm/°C)":{"zh_CN":"热膨胀系数 CTE (ppm/°C)","en":"CTE (ppm/°C)","ja":"線膨張係数 CTE (ppm/°C)"},
"熱穩定性-性能保留 (%)":{"zh_CN":"热稳定性-性能保留 (%)","en":"Thermal Stability (%)","ja":"熱安定性 (%)"},
"冷熱衝擊-高溫極限 (°C)":{"zh_CN":"冷热冲击-高温极限 (°C)","en":"T-Shock High (°C)","ja":"冷熱衝撃-高温 (°C)"},
"冷熱衝擊-低溫極限 (°C)":{"zh_CN":"冷热冲击-低温极限 (°C)","en":"T-Shock Low (°C)","ja":"冷熱衝撃-低温 (°C)"},
"冷熱衝擊-駐留時間 (min)":{"zh_CN":"冷热冲击-驻留时间 (min)","en":"T-Shock Dwell (min)","ja":"冷熱衝撃-滞留 (min)"},
"冷熱衝擊-失效循環數":{"zh_CN":"冷热冲击-失效循环数","en":"T-Shock Cycles to Fail","ja":"冷熱衝撃-破壊サイクル数"},
"導熱係數@室溫 (W/m·K)":{"zh_CN":"导热系数@室温 (W/m·K)","en":"λ @RT (W/m·K)","ja":"λ@室温 (W/m·K)"},
"導熱係數@-40°C (W/m·K)":{"zh_CN":"导热系数@-40°C (W/m·K)","en":"λ @-40°C (W/m·K)","ja":"λ@-40°C (W/m·K)"},
"導熱係數@80°C (W/m·K)":{"zh_CN":"导热系数@80°C (W/m·K)","en":"λ @80°C (W/m·K)","ja":"λ@80°C (W/m·K)"},
"導熱係數@150°C (W/m·K)":{"zh_CN":"导热系数@150°C (W/m·K)","en":"λ @150°C (W/m·K)","ja":"λ@150°C (W/m·K)"},
"導熱係數@200°C (W/m·K)":{"zh_CN":"导热系数@200°C (W/m·K)","en":"λ @200°C (W/m·K)","ja":"λ@200°C (W/m·K)"},
"熱擴散率 (mm²/s)":{"zh_CN":"热扩散率 (mm²/s)","en":"Thermal Diffusivity (mm²/s)","ja":"熱拡散率 (mm²/s)"},
"體積比熱容 ρCp (MJ/m³·K)":{"zh_CN":"体积比热容 ρCp (MJ/m³·K)","en":"ρCp (MJ/m³·K)","ja":"ρCp (MJ/m³·K)"},
"熱阻 (°C·cm²/W)":{"zh_CN":"热阻 (°C·cm²/W)","en":"Thermal Resist. (°C·cm²/W)","ja":"熱抵抗 (°C·cm²/W)"},
"界面接觸熱阻 (°C·cm²/W)":{"zh_CN":"界面接触热阻 (°C·cm²/W)","en":"Interface Resist. (°C·cm²/W)","ja":"界面熱抵抗 (°C·cm²/W)"},
"化學耐性-酸 (%重量變化)":{"zh_CN":"化学耐性-酸 (%重量变化)","en":"Acid Resist. (%wt)","ja":"耐酸性 (%質量変化)"},
"化學耐性-鹼 (%重量變化)":{"zh_CN":"化学耐性-碱 (%重量变化)","en":"Base Resist. (%wt)","ja":"耐アルカリ性 (%質量変化)"},
"吸水率 (%)":{"zh_CN":"吸水率 (%)","en":"Water Absorption (%)","ja":"吸水率 (%)"},
"耐老化-性能保留 (%)":{"zh_CN":"耐老化-性能保留 (%)","en":"Aging Retention (%)","ja":"耐老化性 (%)"},
"化學耐性-溶劑 (%重量變化)":{"zh_CN":"化学耐性-溶剂 (%重量变化)","en":"Solvent Resist. (%wt)","ja":"耐溶剤性 (%質量変化)"},
"化學耐性-乙醇 (%重量變化)":{"zh_CN":"化学耐性-乙醇 (%重量变化)","en":"Ethanol Resist. (%wt)","ja":"耐エタノール性 (%質量変化)"},
"化學耐性-丙酮 (%重量變化)":{"zh_CN":"化学耐性-丙酮 (%重量变化)","en":"Acetone Resist. (%wt)","ja":"耐アセトン性 (%質量変化)"},
"介電常數 (1kHz)":{"zh_CN":"介电常数 (1kHz)","en":"Dk (1kHz)","ja":"誘電率 (1kHz)"},
"耗散因子 (1kHz)":{"zh_CN":"耗散因子 (1kHz)","en":"Df (1kHz)","ja":"誘電正接 (1kHz)"},
"體積電阻率 (Ω·cm)":{"zh_CN":"体积电阻率 (Ω·cm)","en":"Vol. Resistivity (Ω·cm)","ja":"体積抵抗率 (Ω·cm)"},
"表面電阻率 (Ω)":{"zh_CN":"表面电阻率 (Ω)","en":"Surface Resistivity (Ω)","ja":"表面抵抗率 (Ω)"},
"DSC Tmax (°C)":{"zh_CN":"DSC Tmax (°C)","en":"DSC Tmax (°C)","ja":"DSC Tmax (°C)"},
"DSC onset (°C)":{"zh_CN":"DSC onset (°C)","en":"DSC Onset (°C)","ja":"DSC onset (°C)"},
"DSC t50 (min)":{"zh_CN":"DSC t50 (min)","en":"DSC t50 (min)","ja":"DSC t50 (min)"},
}
_GROUP_DISPLAY = {
"高溫凝膠":{"zh_CN":"高温凝胶","en":"High-Temp Gelation","ja":"高温ゲル化"},
"硬度":{"zh_CN":"硬度","en":"Hardness","ja":"硬度"},
"冷熱衝擊":{"zh_CN":"冷热冲击","en":"Thermal Shock","ja":"冷熱衝撃"},
"導熱性":{"zh_CN":"导热性","en":"Thermal Conductivity","ja":"熱伝導性"},
"化學溶劑耐性":{"zh_CN":"化学溶剂耐性","en":"Solvent Resistance","ja":"耐溶剤性"},
}
_METHOD_DISPLAY = {
"Brookfield旋轉粘度計":{"zh_CN":"Brookfield旋转粘度计","en":"Brookfield Viscometer","ja":"ブルックフィールド粘度計"},
"蒸氣壓測試儀":{"zh_CN":"蒸气压测试仪","en":"Vapor Pressure Tester","ja":"蒸気圧試験機"},
"接觸角測量儀":{"zh_CN":"接触角测量仪","en":"Contact Angle Goniometer","ja":"接触角計"},
"儲存穩定性測試":{"zh_CN":"储存稳定性测试","en":"Storage Stability Test","ja":"貯蔵安定性試験"},
"烘箱乾燥法":{"zh_CN":"烘箱干燥法","en":"Oven Dry Method","ja":"乾燥炉法"},
"比重計":{"zh_CN":"比重计","en":"Hydrometer","ja":"比重計"},
"色差儀":{"zh_CN":"色差仪","en":"Colorimeter","ja":"色差計"},
"氣相色譜":{"zh_CN":"气相色谱","en":"Gas Chromatography","ja":"ガスクロマトグラフィー"},
"環球法":{"zh_CN":"环球法","en":"Ring & Ball Method","ja":"環球法"},
"膠凝時間測試 @25°C/500g":{"zh_CN":"胶凝时间测试 @25°C/500g","en":"Gel Time @25°C/500g","ja":"ゲル化時間 @25°C/500g"},
"膠凝測試":{"zh_CN":"胶凝测试","en":"Gel Test","ja":"ゲル化試験"},
"密度比較法":{"zh_CN":"密度比较法","en":"Density Comparison","ja":"密度比較法"},
"烘箱老化測試":{"zh_CN":"烘箱老化测试","en":"Oven Aging Test","ja":"乾燥炉老化試験"},
"乾/濕循環測試":{"zh_CN":"干/湿循环测试","en":"Dry/Wet Cycling","ja":"乾湿繰返し試験"},
"熱阻測試":{"zh_CN":"热阻测试","en":"Thermal Resist. Test","ja":"熱抵抗試験"},
"接觸熱阻測試":{"zh_CN":"接触热阻测试","en":"Contact Thermal Resist. Test","ja":"接触熱抵抗試験"},
"量熱儀":{"zh_CN":"量热仪","en":"Calorimeter","ja":"熱量計"},
"熱電偶 @500g":{"zh_CN":"热电偶 @500g","en":"Thermocouple @500g","ja":"熱電対 @500g"},
"高溫凝膠時間測試":{"zh_CN":"高温凝胶时间测试","en":"HT Gel Time Test","ja":"高温ゲル時間試験"},
"冷熱衝擊測試":{"zh_CN":"冷热冲击测试","en":"Thermal Shock Test","ja":"冷熱衝撃試験"},
"導熱分析儀（閃光法）":{"zh_CN":"导热分析仪（闪光法）","en":"Flash Method Analyzer","ja":"フラッシュ法分析装置"},
"高溫凝膠測試，格式: 2'12''":{"zh_CN":"高温凝胶测试，格式: 2'12''","en":"HT Gel Test, fmt: 2'12''","ja":"高温ゲル試験, 形式: 2'12''"},
"高溫凝膠測試，格式: 12'24''":{"zh_CN":"高温凝胶测试，格式: 12'24''","en":"HT Gel Test, fmt: 12'24''","ja":"高温ゲル試験, 形式: 12'24''"},
"冷熱衝擊測試，每端駐留時間":{"zh_CN":"冷热冲击测试，每端驻留时间","en":"Thermal Shock, dwell time per side","ja":"冷熱衝撃試験, 各端滞留時間"},
"導熱測試 @23-25°C":{"zh_CN":"导热测试 @23-25°C","en":"Thermal Cond. Test @23-25°C","ja":"熱伝導率試験 @23-25°C"},
"導熱測試 @-40°C":{"zh_CN":"导热测试 @-40°C","en":"Thermal Cond. Test @-40°C","ja":"熱伝導率試験 @-40°C"},
"導熱測試 @80°C":{"zh_CN":"导热测试 @80°C","en":"Thermal Cond. Test @80°C","ja":"熱伝導率試験 @80°C"},
"導熱測試 @150°C":{"zh_CN":"导热测试 @150°C","en":"Thermal Cond. Test @150°C","ja":"熱伝導率試験 @150°C"},
"導熱測試 @200°C":{"zh_CN":"导热测试 @200°C","en":"Thermal Cond. Test @200°C","ja":"熱伝導率試験 @200°C"},
"DSC":{"zh_CN":"DSC","en":"DSC","ja":"DSC"},
"DSC/DMA":{"zh_CN":"DSC/DMA","en":"DSC/DMA","ja":"DSC/DMA"},
"TGA":{"zh_CN":"TGA","en":"TGA","ja":"TGA"},
"ASTM D638":{"zh_CN":"ASTM D638","en":"ASTM D638","ja":"ASTM D638"},
"ASTM D1002":{"zh_CN":"ASTM D1002","en":"ASTM D1002","ja":"ASTM D1002"},
"ASTM D695":{"zh_CN":"ASTM D695","en":"ASTM D695","ja":"ASTM D695"},
"ASTM D790":{"zh_CN":"ASTM D790","en":"ASTM D790","ja":"ASTM D790"},
"ASTM D1876":{"zh_CN":"ASTM D1876","en":"ASTM D1876","ja":"ASTM D1876"},
"ASTM D256 Izod":{"zh_CN":"ASTM D256 Izod","en":"ASTM D256 Izod","ja":"ASTM D256 Izod"},
"ASTM C882 斜剪":{"zh_CN":"ASTM C882 斜剪","en":"ASTM C882 Slant Shear","ja":"ASTM C882 斜めせん断"},
"ASTM D785":{"zh_CN":"ASTM D785","en":"ASTM D785","ja":"ASTM D785"},
"ASTM D2240 Type A":{"zh_CN":"ASTM D2240 Type A","en":"ASTM D2240 Type A","ja":"ASTM D2240 Type A"},
"ASTM D2240 Type D":{"zh_CN":"ASTM D2240 Type D","en":"ASTM D2240 Type D","ja":"ASTM D2240 Type D"},
"ASTM D648 @455kPa":{"zh_CN":"ASTM D648 @455kPa","en":"ASTM D648 @455kPa","ja":"ASTM D648 @455kPa"},
"ASTM E831":{"zh_CN":"ASTM E831","en":"ASTM E831","ja":"ASTM E831"},
"ASTM D543":{"zh_CN":"ASTM D543","en":"ASTM D543","ja":"ASTM D543"},
"ASTM D543 乙醇浸泡":{"zh_CN":"ASTM D543 乙醇浸泡","en":"ASTM D543 Ethanol Immersion","ja":"ASTM D543 エタノール浸漬"},
"ASTM D543 丙酮浸泡":{"zh_CN":"ASTM D543 丙酮浸泡","en":"ASTM D543 Acetone Immersion","ja":"ASTM D543 アセトン浸漬"},
"ASTM D570 24h":{"zh_CN":"ASTM D570 24h","en":"ASTM D570 24h","ja":"ASTM D570 24h"},
"ASTM D150":{"zh_CN":"ASTM D150","en":"ASTM D150","ja":"ASTM D150"},
"ASTM D257":{"zh_CN":"ASTM D257","en":"ASTM D257","ja":"ASTM D257"},
}

def T_prop(name):
    if _CURRENT_LANG == "zh_TW": return name
    e = _PROP_DISPLAY.get(name)
    return e.get(_CURRENT_LANG, name) if e else name

def T_group(name):
    if _CURRENT_LANG == "zh_TW": return name
    e = _GROUP_DISPLAY.get(name)
    return e.get(_CURRENT_LANG, name) if e else name

def T_method(name):
    if _CURRENT_LANG == "zh_TW": return name
    e = _METHOD_DISPLAY.get(name)
    return e.get(_CURRENT_LANG, name) if e else name

# ─────────────── 預設物性模板 ───────────────
PREDEFINED_PROPS = {
    "1.未固化屬性": [
        ("粘度 (cP, 25°C)",            "cP",       "Brookfield旋轉粘度計"),
        ("蒸氣壓 (Pa)",                "Pa",       "蒸氣壓測試儀"),
        ("接觸角 (°)",                 "°",        "接觸角測量儀"),
        ("反應放熱峰 (J/g)",           "J/g",      "DSC"),
        ("保質期 (D)",                  "D",        "儲存穩定性測試"),
        ("固含量 (%)",                 "%",        "烘箱乾燥法"),
        ("比重 (g/cm³)",               "g/cm³",    "比重計"),
        ("顏色 (Gardner)",             "Gardner",  "色差儀"),
        ("VOC含量 (g/L)",              "g/L",      "氣相色譜"),
        ("軟化點 (°C)",                "°C",       "環球法"),
    ],
    "2.固化過程": [
        ("適用期 Pot Life (d)",         "d",        "膠凝時間測試 @25°C/500g"),
        ("保質期 Shelf Life (h)",       "h",        "儲存穩定性測試"),
        ("固化時間-室溫 (h)",          "h",        "膠凝測試"),
        ("固化時間-高溫 (h)",          "h",        "膠凝測試"),
        ("峰值放熱溫度 (°C)",          "°C",       "熱電偶 @500g"),
        ("收縮率 (%)",                 "%",        "密度比較法"),
        ("DSC Tmax (°C)",              "°C",       "DSC"),
        ("DSC t50 (min)",              "min",      "DSC"),
        ("DSC onset (°C)",             "°C",       "DSC"),
        ("__group__", "高溫凝膠", [
            ("高溫凝膠-測試溫度 (°C)", "°C",        "高溫凝膠時間測試"),
            ("高溫凝膠-拉絲時間",      "m'ss''",    "高溫凝膠測試，格式: 2'12''"),
            ("高溫凝膠-固化時間",      "m'ss''",    "高溫凝膠測試，格式: 12'24''"),
        ]),
    ],
    "3.機械屬性": [
        ("拉伸強度 (MPa)",             "MPa",      "ASTM D638"),
        ("斷裂伸長率 (%)",             "%",        "ASTM D638"),
        ("剪切強度-鋁 (MPa)",          "MPa",      "ASTM D1002"),
        ("剪切強度-鋼 (MPa)",          "MPa",      "ASTM D1002"),
        ("壓縮強度 (MPa)",             "MPa",      "ASTM D695"),
        ("彎曲強度 (MPa)",             "MPa",      "ASTM D790"),
        ("剝離強度 (N/mm)",            "N/mm",     "ASTM D1876"),
        ("衝擊強度 (J/m)",             "J/m",      "ASTM D256 Izod"),
        ("拉伸模量 (GPa)",             "GPa",      "ASTM D638"),
        ("彎曲模量 (GPa)",             "GPa",      "ASTM D790"),
        ("附著力-鋼 (MPa)",            "MPa",      "ASTM C882 斜剪"),
        ("__group__", "硬度", [
            ("硬度 Rockwell M (HRM)",  "HRM",      "ASTM D785"),
            ("邵氏硬度 Shore A",       "Shore A",  "ASTM D2240 Type A"),
            ("邵氏硬度 Shore D",       "Shore D",  "ASTM D2240 Type D"),
        ]),
    ],
    "4.熱屬性": [
        ("熱畸變溫度 HDT (°C)",        "°C",       "ASTM D648 @455kPa"),
        ("玻璃轉移溫度 Tg (°C)",       "°C",       "DSC/DMA"),
        ("熱分解溫度 Td (°C)",         "°C",       "TGA"),
        ("熱膨脹係數 CTE (ppm/°C)",   "ppm/°C",   "ASTM E831"),
        ("熱穩定性-性能保留 (%)",      "%",        "烘箱老化測試"),
        ("__group__", "冷熱衝擊", [
            ("冷熱衝擊-高溫極限 (°C)", "°C",       "冷熱衝擊測試"),
            ("冷熱衝擊-低溫極限 (°C)", "°C",       "冷熱衝擊測試"),
            ("冷熱衝擊-駐留時間 (min)","min",      "冷熱衝擊測試，每端駐留時間"),
            ("冷熱衝擊-失效循環數",    "cycles",   "冷熱衝擊測試"),
        ]),
        ("__group__", "導熱性", [
            ("導熱係數@室溫 (W/m·K)",  "W/m·K",    "導熱測試 @23-25°C"),
            ("導熱係數@-40°C (W/m·K)", "W/m·K",    "導熱測試 @-40°C"),
            ("導熱係數@80°C (W/m·K)",  "W/m·K",    "導熱測試 @80°C"),
            ("導熱係數@150°C (W/m·K)", "W/m·K",    "導熱測試 @150°C"),
            ("導熱係數@200°C (W/m·K)", "W/m·K",    "導熱測試 @200°C"),
            ("熱擴散率 (mm²/s)",       "mm²/s",    "導熱分析儀（閃光法）"),
            ("體積比熱容 ρCp (MJ/m³·K)","MJ/m³·K", "量熱儀"),
            ("熱阻 (°C·cm²/W)",        "°C·cm²/W", "熱阻測試"),
            ("界面接觸熱阻 (°C·cm²/W)","°C·cm²/W", "接觸熱阻測試"),
        ]),
    ],
    "5.化學環境": [
        ("化學耐性-酸 (%重量變化)",    "%",        "ASTM D543"),
        ("化學耐性-鹼 (%重量變化)",    "%",        "ASTM D543"),
        ("吸水率 (%)",                 "%",        "ASTM D570 24h"),
        ("耐老化-性能保留 (%)",        "%",        "乾/濕循環測試"),
        ("__group__", "化學溶劑耐性", [
            ("化學耐性-溶劑 (%重量變化)",  "%",    "ASTM D543"),
            ("化學耐性-乙醇 (%重量變化)",  "%",    "ASTM D543 乙醇浸泡"),
            ("化學耐性-丙酮 (%重量變化)",  "%",    "ASTM D543 丙酮浸泡"),
        ]),
    ],
    "6.電屬性": [
        ("介電常數 (1kHz)",            "-",        "ASTM D150"),
        ("耗散因子 (1kHz)",            "-",        "ASTM D150"),
        ("體積電阻率 (Ω·cm)",          "Ω·cm",     "ASTM D257"),
        ("表面電阻率 (Ω)",             "Ω",        "ASTM D257"),
    ],
}

USER_PROP_FILE = "user_prop_definitions.csv"

def _build_fixed_columns():
    cols = ["配方名稱", "批次號", "建立日期", "計算模式", "總質量_g", "總氯含量_ppm"]
    sc = get_all_slot_counts(); sf = get_all_slot_fields(); cc = get_all_cat_cn()
    for cat, n in sc.items():
        cn = cc.get(cat, cat)
        for i in range(1, n + 1):
            for field in sf.get(cat, ["名稱","質量_g","佔比%"]):
                cols.append(f"{cn}{i}_{field}")
    return cols

def get_fixed_columns():
    return _build_fixed_columns()



# ═══════════════════════════════════════════
#  ToolTip
# ═══════════════════════════════════════════
class ToolTip:
    def __init__(self, widget, text=""):
        self.widget = widget; self.text = text
        self.tipwindow = None; self._id = None
        widget.bind('<Enter>', self._enter); widget.bind('<Leave>', self._leave)

    def set_text(self, t): self.text = t

    def _enter(self, _=None): self._id = self.widget.after(500, self._show)
    def _leave(self, _=None):
        if self._id: self.widget.after_cancel(self._id)
        if self.tipwindow: self.tipwindow.destroy(); self.tipwindow = None

    def _show(self, _=None):
        if not self.text: return
        try: x, y, _, _ = self.widget.bbox("insert")
        except: x = y = 0
        x += self.widget.winfo_rootx() + 25; y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True); tw.wm_geometry(f"+{x}+{y}")
        tk.Label(tw, text=self.text, justify='left', background="#ffffe0",
                 relief='solid', borderwidth=1, font=("Microsoft JhengHei", 9)).pack(ipadx=4, ipady=2)


# ═══════════════════════════════════════════
#  DataManager
# ═══════════════════════════════════════════
class DataManager:
    CAT_MAP     = CAT_CN
    CAT_MAP_REV = {v: k for k, v in CAT_CN.items()}

    def __init__(self):
        self.mat_columns   = self._load_mat_col_config()
        self.materials     = self._load_materials()
        self.custom_props  = self._load_custom_props()

    # ── 物料欄位配置 ──
    def _load_mat_col_config(self):
        cols = [dict(c) for c in _get_builtin_mat_cols()]
        if os.path.exists(MAT_COL_CFG_FILE):
            try:
                with open(MAT_COL_CFG_FILE, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
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
            except: pass
        return cols

    def _save_mat_col_config(self):
        try:
            save_list = []
            for c in self.mat_columns:
                save_list.append({
                    "db_key": c['db_key'], "display": c['display'],
                    "unit": c.get('unit',''), "visible": c.get('visible',True),
                    "builtin": c.get('builtin',True),
                    "data_key": c.get('data_key',''),
                })
            with open(MAT_COL_CFG_FILE, 'w', encoding='utf-8') as f:
                json.dump(save_list, f, ensure_ascii=False, indent=2)
        except Exception as e: print(f"欄位配置儲存失敗: {e}")

    def get_visible_mat_cols(self):
        return [c for c in self.mat_columns if c.get('visible', True)]

    def get_custom_mat_cols(self):
        return [c for c in self.mat_columns if not c.get('builtin', True)]

    def add_mat_column(self, db_key, display, unit=""):
        if any(c['db_key'] == db_key for c in self.mat_columns): return False
        self.mat_columns.append({
            "db_key": db_key, "display": display, "unit": unit,
            "data_key": db_key.lower(), "visible": True, "builtin": False
        })
        self._save_mat_col_config(); return True

    def remove_mat_column(self, db_key):
        self.mat_columns = [c for c in self.mat_columns if c['db_key'] != db_key or c.get('builtin')]
        self._save_mat_col_config()

    # ── 物料庫 I/O ──
    _MAT_FIELDS = [
        'Category','Name','Type','Appearance','Viscosity_cP25','Dk','Surface_Energy',
        'Hardener_Subtype','EEW','AHEW','Polyamide_Eq',
        'Anhydride_Eq','Mercapto_Eq','Hydroxyl_Eq','Amine_Value','Acid_Value',
        'Hydroxyl_Value','MW','Func_Group_Num','f_factor','C_factor','Cl_ppm',
        'Molecular_Structure','Source','Description'
    ]

    def _load_materials(self):
        data = {k: {} for k in get_all_slot_counts()}
        if not os.path.exists(MAT_DB_FILE): return data
        try:
            with open(MAT_DB_FILE, 'r', encoding='utf-8-sig', newline='') as f:
                for row in csv.DictReader(f):
                    cat = row.get('Category','')
                    if cat in data and row.get('Name'):
                        info = {
                            'type': row.get('Type',''),
                            'appearance': row.get('Appearance',''),
                            'viscosity': row.get('Viscosity_cP25','') or row.get('Viscosity',''),
                            'dk': row.get('Dk',''),
                            'surface_energy': row.get('Surface_Energy',''),
                            'h_subtype': row.get('Hardener_Subtype',''),
                            'eew':   float(row.get('EEW',0)  or 0),
                            'ahew':  float(row.get('AHEW',0) or 0),
                            'polyamide_eq':  float(row.get('Polyamide_Eq',0)  or 0),
                            'anhydride_eq':  float(row.get('Anhydride_Eq',0) or 0),
                            'mercapto_eq':   float(row.get('Mercapto_Eq',0)  or 0),
                            'hydroxyl_eq':   float(row.get('Hydroxyl_Eq',0)  or 0),
                            'amine_value':   float(row.get('Amine_Value',0)  or 0),
                            'acid_value':    float(row.get('Acid_Value',0)   or 0),
                            'hydroxyl_value':float(row.get('Hydroxyl_Value',0)or 0),
                            'mw':            float(row.get('MW',0)           or 0),
                            'func_group_num':float(row.get('Func_Group_Num',0)or 0),
                            'f_factor':      float(row.get('f_factor',1.0)   or 1.0),
                            'c_factor':      float(row.get('C_factor',1.0)   or 1.0),
                            'cl':            float(row.get('Cl_ppm',0)       or 0),
                            'structure': row.get('Molecular_Structure',''),
                            'source':    row.get('Source',''),
                            'desc':      row.get('Description',''),
                        }
                        for col in self.get_custom_mat_cols():
                            info[col['data_key']] = row.get(col['db_key'], '')
                        data[cat][row['Name']] = info
        except Exception as e: print(f"物料庫讀取錯誤: {e}")
        return data

    def save_materials(self):
        try:
            extra_keys = [c['db_key'] for c in self.get_custom_mat_cols()]
            fields = self._MAT_FIELDS + extra_keys
            with open(MAT_DB_FILE, 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
                for cat, items in self.materials.items():
                    for name, info in items.items():
                        rd = {'Category':cat,'Name':name,
                            'Type':info.get('type',''),
                            'Appearance':info.get('appearance',''),
                            'Viscosity_cP25':info.get('viscosity',''),
                            'Dk':info.get('dk',''),
                            'Surface_Energy':info.get('surface_energy',''),
                            'Hardener_Subtype':info.get('h_subtype',''),
                            'EEW':info.get('eew',0),'AHEW':info.get('ahew',0),
                            'Polyamide_Eq':info.get('polyamide_eq',0),'Anhydride_Eq':info.get('anhydride_eq',0),
                            'Mercapto_Eq':info.get('mercapto_eq',0),'Hydroxyl_Eq':info.get('hydroxyl_eq',0),
                            'Amine_Value':info.get('amine_value',0),'Acid_Value':info.get('acid_value',0),
                            'Hydroxyl_Value':info.get('hydroxyl_value',0),'MW':info.get('mw',0),
                            'Func_Group_Num':info.get('func_group_num',0),'f_factor':info.get('f_factor',1.0),
                            'C_factor':info.get('c_factor',1.0),'Cl_ppm':info.get('cl',0),
                            'Molecular_Structure':info.get('structure',''),
                            'Source':info.get('source',''),'Description':info.get('desc','')}
                        for col in self.get_custom_mat_cols():
                            rd[col['db_key']] = info.get(col['data_key'], '')
                        w.writerow(rd)
        except Exception as e: messagebox.showerror(T("error"), str(e))

    def get_active_eq(self, info):
        _d2k = {"胺類":"amine","聚酰胺":"polyamide","酸酐":"anhydride","巯基":"mercaptan","羥基":"hydroxyl"}
        st = _d2k.get(info.get('h_subtype',''), info.get('h_subtype',''))
        return info.get({'polyamide':'polyamide_eq','anhydride':'anhydride_eq',
                         'mercaptan':'mercapto_eq','hydroxyl':'hydroxyl_eq'}.get(st,'ahew'), 1) or 1

    # ── 配方數據庫 I/O ──
    def _read_recipe_rows(self):
        rows = []
        if not os.path.exists(RECIPE_DB_FILE): return rows
        try:
            with open(RECIPE_DB_FILE, 'r', encoding='utf-8-sig', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader: rows.append(dict(row))
        except Exception as e: print(f"配方庫讀取錯誤: {e}")
        return rows

    def _write_recipe_rows(self, rows):
        if not rows:
            if os.path.exists(RECIPE_DB_FILE): os.remove(RECIPE_DB_FILE)
            return
        # 合集所有列：先固定列，再已出現的非固定列（保持追加順序）
        seen_extra = []
        for row in rows:
            for k in row.keys():
                if k not in get_fixed_columns() and k not in seen_extra:
                    seen_extra.append(k)
        all_cols = get_fixed_columns() + seen_extra
        try:
            with open(RECIPE_DB_FILE, 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.DictWriter(f, fieldnames=all_cols, extrasaction='ignore')
                w.writeheader()
                for row in rows:
                    w.writerow({c: row.get(c, '') for c in all_cols})
        except Exception as e: messagebox.showerror(T("error"), str(e))

    def get_recipe_names(self):
        return [r.get("配方名稱","") for r in self._read_recipe_rows()]

    def get_recipe_row(self, name):
        for r in self._read_recipe_rows():
            if r.get("配方名稱") == name: return r
        return {}

    def get_prop_columns(self):
        if not os.path.exists(RECIPE_DB_FILE): return []
        try:
            with open(RECIPE_DB_FILE, 'r', encoding='utf-8-sig', newline='') as f:
                reader = csv.reader(f)
                headers = next(reader, [])
            return [h for h in headers if h not in get_fixed_columns()]
        except: return []

    def build_recipe_row(self, recipe_name, batch_no, calc_mode, materials_list, total_mass, total_cl):
        row = {c: "" for c in get_fixed_columns()}
        row["配方名稱"]   = recipe_name
        row["批次號"]     = batch_no
        row["建立日期"]   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row["計算模式"]   = calc_mode
        row["總質量_g"]   = f"{total_mass:.4f}"
        row["總氯含量_ppm"] = f"{total_cl:.2f}"

        all_sc = get_all_slot_counts(); all_sf = get_all_slot_fields(); all_cn = get_all_cat_cn()
        counters = {c: 0 for c in all_sc}
        for m in materials_list:
            cat = m.get("orig_cat")
            if cat not in counters: continue
            counters[cat] += 1
            idx = counters[cat]
            if idx > all_sc.get(cat, 3): continue
            cn   = all_cn.get(cat, cat)
            name = m["name"]
            info = self.materials.get(cat,{}).get(name, {})
            mass = m.get("rounded_mass", 0)
            pct  = m.get("pct", 0)
            fields = all_sf.get(cat, ["名稱","質量_g","佔比%"])

            row[f"{cn}{idx}_名稱"]   = name
            row[f"{cn}{idx}_質量_g"] = str(mass)
            row[f"{cn}{idx}_佔比%"]  = f"{pct:.4f}"

            if cat == "resins":
                row[f"{cn}{idx}_EEW"]    = str(info.get("eew",""))
                row[f"{cn}{idx}_類型"]   = info.get("type","")
                row[f"{cn}{idx}_分子結構"] = info.get("structure","")
            elif cat == "hardeners":
                row[f"{cn}{idx}_當量"]   = str(self.get_active_eq(info))
                row[f"{cn}{idx}_子類型"] = info.get("h_subtype","")
                row[f"{cn}{idx}_校正%"]  = str(m.get("corr_pct",""))
                row[f"{cn}{idx}_分子結構"] = info.get("structure","")
            else:
                # Builtin others + custom cats: write fields present
                if "EEW" in fields:       row[f"{cn}{idx}_EEW"]    = str(info.get("eew",""))
                if "類型" in fields:      row[f"{cn}{idx}_類型"]   = info.get("type","")
                if "外觀" in fields:      row[f"{cn}{idx}_外觀"]   = info.get("appearance","")
                if "黏度" in fields:      row[f"{cn}{idx}_黏度"]   = info.get("viscosity","")
                if "Dk" in fields:        row[f"{cn}{idx}_Dk"]     = info.get("dk","")
                if "表面能" in fields:    row[f"{cn}{idx}_表面能"] = info.get("surface_energy","")
                if "分子結構" in fields:  row[f"{cn}{idx}_分子結構"] = info.get("structure","")
                if "氯_ppm" in fields:    row[f"{cn}{idx}_氯_ppm"] = str(info.get("cl",""))
                if "來源" in fields:      row[f"{cn}{idx}_來源"]   = info.get("source","")

        return row

    def save_new_recipe(self, row_dict):
        rows = self._read_recipe_rows()
        # 防重複名稱：舊記錄存在就覆蓋固定列，保留物性列
        for existing in rows:
            if existing.get("配方名稱") == row_dict.get("配方名稱"):
                # 保留已有物性數據
                prop_cols = self.get_prop_columns()
                for col in prop_cols:
                    row_dict.setdefault(col, existing.get(col, ""))
                existing.update(row_dict)
                self._write_recipe_rows(rows)
                return
        rows.append(row_dict)
        self._write_recipe_rows(rows)

    def update_recipe_props(self, recipe_name, props_dict):
        rows = self._read_recipe_rows()
        found = False
        for row in rows:
            if row.get("配方名稱") == recipe_name:
                row.update(props_dict); found = True; break
        if not found: return False
        self._write_recipe_rows(rows); return True

    def delete_recipe(self, recipe_name):
        rows = [r for r in self._read_recipe_rows() if r.get("配方名稱") != recipe_name]
        self._write_recipe_rows(rows)

    def rename_recipe(self, old_name, new_name):
        rows = self._read_recipe_rows()
        for r in rows:
            if r.get("配方名稱") == old_name: r["配方名稱"] = new_name
        self._write_recipe_rows(rows)

    # ── 使用者物性定義 I/O ──
    def _load_custom_props(self):
        props = []
        # 向後相容：若舊 CUSTOM_PROP_FILE 存在，遷移後刪除
        if os.path.exists(CUSTOM_PROP_FILE):
            try:
                with open(CUSTOM_PROP_FILE, 'r', encoding='utf-8-sig', newline='') as f:
                    for row in csv.DictReader(f): props.append(dict(row))
                os.rename(CUSTOM_PROP_FILE, CUSTOM_PROP_FILE + ".bak")
                self._save_user_props_to_file(props)
            except: pass
        if not os.path.exists(USER_PROP_FILE): return props
        try:
            with open(USER_PROP_FILE, 'r', encoding='utf-8-sig', newline='') as f:
                for row in csv.DictReader(f): props.append(dict(row))
        except: pass
        return props

    def _save_user_props_to_file(self, props):
        fields = ["category", "name", "db_key", "unit", "method"]
        try:
            with open(USER_PROP_FILE, 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
                w.writeheader(); w.writerows(props)
        except Exception as e: messagebox.showerror(T("error"), str(e))

    def save_custom_props(self):
        self._save_user_props_to_file(self.custom_props)

    def get_prop_csv_key(self, display_name):
        for p in self.custom_props:
            if p.get('name') == display_name and p.get('db_key'):
                return p['db_key']
        return display_name

    def get_prop_display_from_csv_key(self, csv_key):
        for p in self.custom_props:
            if p.get('db_key') == csv_key:
                return p.get('name', csv_key)
        return csv_key

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
            else:
                yield item

    def get_prop_defs_flat(self):
        deleted = {p['name'] for p in self.custom_props if p.get('category') == '_deleted'}
        result = {}
        for cat, items in PREDEFINED_PROPS.items():
            flat = [(n,u,m) for n,u,m in self._flat_iter(items) if n not in deleted]
            if flat: result[cat] = flat
        for p in self.custom_props:
            cat = p.get("category") or "7.自定義"
            if cat == '_deleted': continue
            tup = (p["name"], p.get("unit",""), p.get("method",""))
            if tup not in result.setdefault(cat, []):
                result[cat].append(tup)
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
            cat = p.get("category") or "7.自定義"
            if cat == '_deleted': continue
            tup = (p["name"], p.get("unit",""), p.get("method",""))
            existing_flat = list(self._flat_iter(result.get(cat, [])))
            if tup not in existing_flat:
                result.setdefault(cat, []).append(tup)
        return result

    def get_all_prop_defs(self):
        return self.get_prop_defs_flat()

    def get_all_categories(self):
        cats = list(PREDEFINED_PROPS.keys())
        # Add custom categories from config
        for cc in _custom_cats:
            k = cc.get("key","")
            if k and k not in cats: cats.append(k)
        # Add categories from custom props that may not be predefined
        for p in self.custom_props:
            c = p.get("category") or "7.自定義"
            if c not in cats and c != '_deleted': cats.append(c)
        return cats


# ═══════════════════════════════════════════
#  CalcTab  配方設計與計算
# ═══════════════════════════════════════════
class CalcTab:
    @staticmethod
    def _mode_map():
        return {
            T("mode_stoich"):  "stoich",
            T("mode_weight"):  "weight",
            T("mode_target100"): "target_100",
        }

    def __init__(self, nb, dm: DataManager, font_std, font_bold):
        self.dm = dm; self.fs = font_std; self.fb = font_bold
        self.frame = ttk.Frame(nb)
        nb.add(self.frame, text=T("tab_calc"))
        self.calc_rows = {c: [] for c in get_all_slot_counts()}
        self._drag_item = None
        self._ac_win = None
        self._ac_lb = None
        self._ac_cb = None
        self._build()

    # ── UI ──
    def _build(self):
        pw = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        pw.pack(fill='both', expand=True, padx=5, pady=5)

        # 左側可滾動輸入
        lf = ttk.Frame(pw); pw.add(lf, weight=1)
        cvs = tk.Canvas(lf, highlightthickness=0)
        vsb = ttk.Scrollbar(lf, orient="vertical", command=cvs.yview)
        self.sf = ttk.Frame(cvs)
        self.sf.bind("<Configure>", lambda e: cvs.configure(scrollregion=cvs.bbox("all")))
        cvs.create_window((0,0), window=self.sf, anchor="nw")
        cvs.configure(yscrollcommand=vsb.set)
        cvs.pack(side="left", fill="both", expand=True); vsb.pack(side="right", fill="y")

        # 樹脂
        rf = ttk.LabelFrame(self.sf, text=T("sec_resin"), padding=5); rf.pack(fill='x', pady=5, padx=5)
        self.resin_box = ttk.Frame(rf); self.resin_box.pack(fill='both', expand=True)
        ttk.Button(rf, text=T("add_resin"), command=lambda: self.add_row('resins', self.resin_box)).pack(anchor='w')

        # 固化劑
        hf = ttk.LabelFrame(self.sf, text=T("sec_hardener"), padding=5); hf.pack(fill='x', pady=5, padx=5)
        mf = ttk.Frame(hf); mf.pack(fill='x', pady=2)
        ttk.Label(mf, text=T("calc_mode")).pack(side='left')
        self.calc_mode = tk.StringVar(value=T("mode_stoich"))
        mcb = ttk.Combobox(mf, textvariable=self.calc_mode, state="readonly", width=28,
                           values=list(self._mode_map().keys()))
        mcb.bind("<<ComboboxSelected>>", self._update_ui); mcb.pack(side='left', padx=5)
        self.h_header = ttk.Frame(hf); self.h_header.pack(fill='x')
        self.hardener_box = ttk.Frame(hf); self.hardener_box.pack(fill='both', expand=True)
        ttk.Button(hf, text=T("add_hardener"), command=lambda: self.add_row('hardeners', self.hardener_box)).pack(anchor='w')

        # 助劑/填料/催化劑
        for cat, title_key in [('additives','sec_additive'),('fillers','sec_filler'),('catalysts','sec_catalyst')]:
            f = ttk.LabelFrame(self.sf, text=T(title_key), padding=5); f.pack(fill='x', pady=5, padx=5)
            box = ttk.Frame(f); box.pack(fill='both', expand=True)
            setattr(self, f"{cat}_box", box)
            ttk.Button(f, text=T({"additives":"add_additive","fillers":"add_filler","catalysts":"add_catalyst"}[cat]), command=lambda c=cat, b=box: self.add_row(c, b)).pack(anchor='w')

        # 自定義物料種類
        self._custom_mat_boxes = {}
        for mc in _custom_mat_cats:
            ckey = mc['key']
            disp = get_mat_cat_display(ckey)
            f = ttk.LabelFrame(self.sf, text=disp, padding=5); f.pack(fill='x', pady=5, padx=5)
            box = ttk.Frame(f); box.pack(fill='both', expand=True)
            self._custom_mat_boxes[ckey] = box
            if ckey not in self.calc_rows: self.calc_rows[ckey] = []
            ttk.Button(f, text=T("add_custom_mat", disp), command=lambda c=ckey, b=box: self.add_row(c, b)).pack(anchor='w')

        # 右側結果
        ra = ttk.Frame(pw, padding=10); pw.add(ra, weight=2)
        cf = ttk.LabelFrame(ra, text=T("calc_settings"), padding=5); cf.pack(fill='x', pady=5)

        row1 = ttk.Frame(cf); row1.pack(fill='x', pady=2)
        ttk.Label(row1, text=T("mass_rounding")).pack(side='left', padx=5)
        self.round_opt = tk.StringVar(value=T("round_2dp"))
        ttk.Combobox(row1, textvariable=self.round_opt,
                     values=[T("round_none"),T("round_int"),T("round_1dp"),T("round_2dp")], width=10, state="readonly").pack(side='left')

        self.t100_frame = ttk.LabelFrame(cf, text=T("opt_100g"), padding=5)
        self.inc_add = tk.BooleanVar(value=True); self.inc_fil = tk.BooleanVar(value=True); self.inc_cat = tk.BooleanVar(value=True)
        for var, cat_k in [(self.inc_add,"cat_additives"),(self.inc_fil,"cat_fillers"),(self.inc_cat,"cat_catalysts")]:
            ttk.Checkbutton(self.t100_frame, text=f"{T(cat_k)} {T('join_100g_balance')}", variable=var).pack(anchor='w')
        self._custom_inc_vars = {}
        for mc in _custom_mat_cats:
            if not mc.get('has_eew'):
                v = tk.BooleanVar(value=True)
                self._custom_inc_vars[mc['key']] = v
                ttk.Checkbutton(self.t100_frame, text=f"{get_mat_cat_display(mc['key'])} {T('join_100g_balance')}", variable=v).pack(anchor='w')

        ttk.Button(cf, text=T("btn_calculate"), command=self.calculate).pack(fill='x', pady=5)

        tf = ttk.Frame(ra); tf.pack(fill='both', expand=True)
        cols = [("name",T("col_mat_name"),200),("mass",T("col_mass_g_result"),100),("percent",T("col_pct_result"),100),("cl",T("col_cl_result"),110)]
        self.tree = ttk.Treeview(tf, columns=[c[0] for c in cols], show='headings', height=20)
        for cid, hdr, w in cols: self.tree.heading(cid, text=hdr); self.tree.column(cid, width=w, anchor='center')
        vsbt = ttk.Scrollbar(tf, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsbt.set)
        self.tree.pack(side='left', fill='both', expand=True); vsbt.pack(side='right', fill='y')
        self.tree.tag_configure('total', font=self.fb, background="#e1f5fe")
        self.tree.bind("<ButtonPress-1>",   self._ds); self.tree.bind("<B1-Motion>", self._dm)
        self.tree.bind("<ButtonRelease-1>", self._dr)

        bf = ttk.Frame(ra); bf.pack(fill='x', pady=10)
        ttk.Button(bf, text=T("btn_copy_excel"),  command=self._copy).pack(side='left', fill='x', expand=True, padx=(0,5))
        ttk.Button(bf, text=T("btn_save_recipe"), command=self._save).pack(side='left', fill='x', expand=True, padx=(5,0))

        self.add_row('resins', self.resin_box); self.add_row('hardeners', self.hardener_box)
        self._update_ui()

    # ── 拖曳 ─────────────────────────────────────────────────────────
    def _ds(self, e):
        item = self.tree.identify_row(e.y)
        if not item: return
        if any(t in self.tree.item(item,"tags") for t in ('total','divider')): return
        self._drag_item = item
    def _dm(self, e):
        if not self._drag_item: return
        tgt = self.tree.identify_row(e.y)
        if not tgt or tgt == self._drag_item: return
        if any(t in self.tree.item(tgt,"tags") for t in ('total','divider')): return
        self.tree.move(self._drag_item, self.tree.parent(tgt), self.tree.index(tgt))
    def _dr(self, e): self._drag_item = None

    # ── UI 更新 ───────────────────────────────────────────────────────
    def _update_ui(self, _=None):
        mode = self._mode_map().get(self.calc_mode.get(), "stoich")
        self._sync_resin_modes()
        self._sync_hardener_header()
        if mode == "target_100": self.t100_frame.pack(fill='x', pady=5)
        else: self.t100_frame.pack_forget()

    def _sync_resin_modes(self, _=None):
        mode = self._mode_map().get(self.calc_mode.get(), "stoich")
        allow = (mode == "target_100")
        avail = [T("fixed_mass")] + ([T("ratio_pending")] if allow else [])
        for rd in self.calc_rows['resins']:
            if rd.get('cb_mode'):
                rd['cb_mode']['values'] = avail
                if not allow and rd['mode_var'].get() == T("ratio_pending"):
                    rd['mode_var'].set(T('fixed_mass'))
                    if rd.get('lbl_unit'): rd['lbl_unit'].config(text="g")

    def _sync_hardener_header(self):
        n = len(self.calc_rows['hardeners'])
        for w in self.h_header.winfo_children(): w.destroy()
        ttk.Label(self.h_header, text=T("hdr_name_type"), width=25).pack(side='left')
        if n > 1: ttk.Label(self.h_header, text=T("hdr_eq_ratio"), width=12).pack(side='left', padx=5)
        ttk.Label(self.h_header, text=T("hdr_corr_pct"), width=10).pack(side='left', padx=5)
        for rd in self.calc_rows['hardeners']:
            if n > 1:
                rd['eq_ratio'].pack(side='left', padx=5, before=rd['corr']); rd['lbl_ru'].pack(side='left', before=rd['corr'])
            else:
                rd['eq_ratio'].pack_forget(); rd['lbl_ru'].pack_forget()

    # ── 物料行增刪 ───────────────────────────────────────────────────
    def add_row(self, cat, parent):
        row = ttk.Frame(parent); row.pack(fill='x', pady=2)
        cb = ttk.Combobox(row, width=25); cb.pack(side='left')
        cb.bind('<KeyRelease>', lambda e: self._filter(e, cb, cat))
        cb.bind('<Button-1>',   lambda e: self._show_all(e, cb, cat))
        cb.bind('<FocusOut>',   lambda e: cb.after(150, self._ac_close))
        cb['values'] = self._opts(cat)
        btn_clear = ttk.Button(row, text="↺", width=2,
                               command=lambda: self._clear_cb(cb, cat))
        btn_clear.pack(side='left', padx=(2,0))
        ToolTip(btn_clear, T("clear_reselect"))
        rd = {"frame": row, "cb": cb}

        if cat == 'resins':
            mv = tk.StringVar(value=T("fixed_mass"))
            cbm = ttk.Combobox(row, textvariable=mv, width=8, state="readonly"); cbm.pack(side='left', padx=5)
            ent = ttk.Entry(row, width=8); ent.pack(side='left', padx=5)
            lbl = ttk.Label(row, text="g", font=("Arial",8)); lbl.pack(side='left')
            cbm.bind("<<ComboboxSelected>>", lambda e: lbl.config(text="g" if mv.get()==T("fixed_mass") else "R-parts"))
            rd.update({"entry": ent, "mode_var": mv, "cb_mode": cbm, "lbl_unit": lbl})
            self._sync_resin_modes()
        elif cat == 'hardeners':
            eq = ttk.Entry(row, width=8); eq.insert(0,"100"); eq.pack(side='left', padx=5)
            lru = ttk.Label(row, text="%", font=("Arial",8)); lru.pack(side='left')
            corr = ttk.Entry(row, width=6); corr.insert(0,"100"); corr.pack(side='left', padx=5)
            ttk.Label(row, text="%", font=("Arial",8)).pack(side='left')
            rd.update({"eq_ratio": eq, "lbl_ru": lru, "corr": corr})
        else:
            ent = ttk.Entry(row, width=10); ent.pack(side='left', padx=5)
            ttk.Label(row, text="g", font=("Arial",8)).pack(side='left')
            rd.update({"entry": ent})

        tip = ToolTip(ttk.Button(row, text=" i ", width=3, takefocus=False), "")
        tip.widget.pack(side='left', padx=5)
        cb.bind("<<ComboboxSelected>>", lambda e: (self._ac_close(), tip.set_text(
            self.dm.materials.get(cat,{}).get(cb.get().split("  [")[0], {}).get('desc','').strip() or T("no_note"))))
        ttk.Button(row, text="X", width=3, command=lambda: self._del_row(row, cat)).pack(side='left')
        self.calc_rows[cat].append(rd)
        if cat == 'hardeners': self._sync_hardener_header()

    def _del_row(self, frame, cat):
        self._ac_close()
        frame.destroy()
        self.calc_rows[cat] = [r for r in self.calc_rows[cat] if r['frame'] != frame]
        if cat == 'hardeners': self._sync_hardener_header()
        elif cat == 'resins': self._sync_resin_modes()

    def _opts(self, cat):
        return [f"{n}  [{i.get('type','')}]" for n, i in sorted(self.dm.materials.get(cat,{}).items())]

    def _filter(self, e, cb, cat):
        if e.keysym == 'Escape':
            self._ac_close(); return
        if e.keysym == 'Down':
            if self._ac_lb and self._ac_lb.size() > 0:
                self._ac_lb.focus_set()
                self._ac_lb.selection_clear(0, tk.END)
                self._ac_lb.selection_set(0)
                self._ac_lb.see(0)
            return
        if e.keysym in ['Return','Up']: return
        txt = cb.get().split("  [")[0].lower().strip()
        filtered = [o for o in self._opts(cat) if txt in o.lower()] if txt else self._opts(cat)
        cb['values'] = filtered
        if filtered and txt:
            self._ac_show(cb, filtered)
        else:
            self._ac_close()

    def _show_all(self, e, cb, cat):
        self._ac_close()
        cb['values'] = self._opts(cat)

    def _clear_cb(self, cb, cat):
        self._ac_close()
        cb.set('')
        cb['values'] = self._opts(cat)
        cb.focus_set()

    # ── 自動完成浮動列表 ──
    def _ac_show(self, cb, items):
        max_show = 8
        if self._ac_win is None:
            self._ac_win = tk.Toplevel(cb)
            self._ac_win.wm_overrideredirect(True)
            self._ac_win.wm_attributes('-topmost', True)
            self._ac_lb = tk.Listbox(self._ac_win, font=("Microsoft JhengHei", 9),
                                      activestyle='dotbox', selectmode='browse',
                                      exportselection=False)
            self._ac_lb.pack(fill='both', expand=True)
            self._ac_lb.bind('<ButtonRelease-1>', lambda e: self._ac_select())
            self._ac_lb.bind('<Return>', lambda e: self._ac_select())
            self._ac_lb.bind('<Escape>', lambda e: (self._ac_close(), cb.focus_set()))
            self._ac_cb = cb

        if self._ac_cb != cb:
            self._ac_close()
            self._ac_show(cb, items)
            return

        cb.update_idletasks()
        x = cb.winfo_rootx()
        y = cb.winfo_rooty() + cb.winfo_height()
        w = max(cb.winfo_width(), 250)
        n = min(max_show, len(items))
        self._ac_lb.delete(0, tk.END)
        for item in items:
            self._ac_lb.insert(tk.END, item)
        self._ac_lb.config(height=n)
        self._ac_win.geometry(f'{w}x{n * 20}+{x}+{y}')
        self._ac_win.deiconify()

    def _ac_select(self):
        if not self._ac_lb or not self._ac_cb: return
        sel = self._ac_lb.curselection()
        if sel:
            val = self._ac_lb.get(sel[0])
            self._ac_cb.set(val)
            self._ac_cb.event_generate('<<ComboboxSelected>>')
        cb = self._ac_cb
        self._ac_close()
        if cb:
            cb.focus_set()
            cb.icursor(tk.END)

    def _ac_close(self):
        if self._ac_win:
            try: self._ac_win.destroy()
            except: pass
            self._ac_win = None
            self._ac_lb = None
            self._ac_cb = None

    # ── 計算核心 ─────────────────────────────────────────────────────
    def calculate(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            mode = self._mode_map().get(self.calc_mode.get(), "stoich")
            mats = []; fixed_r_mass = 0.0; fixed_r_eq = 0.0
            ratio_r = []; total_r_parts = 0.0
            inc = {'additives': self.inc_add.get(), 'fillers': self.inc_fil.get(), 'catalysts': self.inc_cat.get()}
            for mk, mv in getattr(self, '_custom_inc_vars', {}).items(): inc[mk] = mv.get()

            for rd in self.calc_rows['resins']:
                nm = rd['cb'].get().split("  [")[0]; vs = rd['entry'].get()
                if not nm or not vs: continue
                v = float(vs); info = self.dm.materials['resins'].get(nm,{})
                eew = info.get('eew',0)
                if rd['mode_var'].get() == T("fixed_mass"):
                    fixed_r_mass += v
                    if eew > 0: fixed_r_eq += v/eew
                    mats.append({"orig_cat":"resins","name":nm,"mass":v,"cl_ppm":info.get('cl',0),"type":"Resin(Fixed)"})
                else:
                    ratio_r.append({"orig_cat":"resins","name":nm,"parts":v,"eew":eew,"cl_ppm":info.get('cl',0),"type":"Resin(Ratio)"})
                    total_r_parts += v

            others = 0.0
            for cat in ['additives','fillers','catalysts']:
                for rd in self.calc_rows[cat]:
                    nm = rd['cb'].get().split("  [")[0]; vs = rd['entry'].get()
                    if not nm or not vs: continue
                    mass = float(vs)
                    if inc.get(cat) and mode == "target_100": others += mass
                    info = self.dm.materials.get(cat,{}).get(nm,{})
                    mats.append({"orig_cat":cat,"name":nm,"mass":mass,"cl_ppm":info.get('cl',0),"type":cat.capitalize()})

            # 自定義物料種類
            for mc in _custom_mat_cats:
                ckey = mc['key']
                for rd in self.calc_rows.get(ckey, []):
                    nm = rd['cb'].get().split("  [")[0]; vs = rd['entry'].get()
                    if not nm or not vs: continue
                    mass = float(vs)
                    info = self.dm.materials.get(ckey,{}).get(nm,{})
                    cl = info.get('cl',0)
                    if mc.get('has_eew'):
                        eew = info.get('eew',0)
                        if eew > 0: fixed_r_eq += mass/eew
                        fixed_r_mass += mass
                    else:
                        if inc.get(ckey) and mode == "target_100": others += mass
                    mats.append({"orig_cat":ckey,"name":nm,"mass":mass,"cl_ppm":cl,"type":get_mat_cat_display(ckey)})

            h_cfgs = []; total_hr = 0.0
            hc = len(self.calc_rows['hardeners'])
            for rd in self.calc_rows['hardeners']:
                nm = rd['cb'].get().split("  [")[0]
                if not nm: continue
                ir = float(rd['eq_ratio'].get() or (100 if hc==1 else 0))
                corr = float(rd['corr'].get() or 100)/100.0
                info = self.dm.materials['hardeners'].get(nm,{})
                aeq = self.dm.get_active_eq(info)
                h_cfgs.append({"name":nm,"input_val":ir,"corr":corr,"eq":aeq,
                                "cl_ppm":info.get('cl',0),"corr_pct":float(rd['corr'].get() or 100)})
                total_hr += ir

            if not ratio_r:
                ft = fixed_r_mass + others
                for h in h_cfgs:
                    hm = 0
                    if mode in ["stoich","target_100"] and total_hr > 0:
                        hm = (fixed_r_eq*(h['input_val']/total_hr))*h['eq']*h['corr']
                    elif mode == "weight":
                        hm = fixed_r_mass*(h['input_val']/100.0)*h['corr']
                    mats.append({"orig_cat":"hardeners","name":h['name'],"mass":hm,"cl_ppm":h['cl_ppm'],
                                 "type":"Hardener","corr_pct":h['corr_pct']})
                    ft += hm
                if mode == "target_100" and ft > 0:
                    sc = 100.0/ft
                    for m in mats:
                        oc = m['orig_cat']
                        if m['type'] in ['Additives','Fillers','Catalysts'] and inc.get(oc,False): m['mass'] *= sc
                        elif m['type'] in ['Resin(Fixed)','Hardener']: m['mass'] *= sc
                        elif _get_custom_mat_cat(oc):
                            cmc = _get_custom_mat_cat(oc)
                            if cmc.get('has_eew'): m['mass'] *= sc  # EEW cats always scale
                            elif inc.get(oc, False): m['mass'] *= sc
            else:
                if mode != "target_100": raise ValueError(T("err_ratio_not_100g"))
                A = total_r_parts; B = C = 0.0
                veq = sum(r['parts']/r['eew'] for r in ratio_r if r['eew']>0)
                for h in h_cfgs:
                    if total_hr > 0:
                        sh = h['input_val']/total_hr
                        B += veq*sh*h['eq']*h['corr']; C += fixed_r_eq*sh*h['eq']*h['corr']
                cf = fixed_r_mass + others + C; vc = A + B
                if vc == 0: raise ValueError(T("err_coeff_zero"))
                u = (100.0-cf)/vc
                if u < 0: raise ValueError(T("err_over_100g"))
                tfe = fixed_r_eq + u*veq
                for r in ratio_r: mats.append({"orig_cat":"resins","name":r['name'],"mass":u*r['parts'],"cl_ppm":r['cl_ppm'],"type":"Resin(Calc)"})
                for h in h_cfgs:
                    hm = (tfe*(h['input_val']/total_hr)*h['eq']*h['corr']) if total_hr>0 else 0
                    mats.append({"orig_cat":"hardeners","name":h['name'],"mass":hm,"cl_ppm":h['cl_ppm'],
                                 "type":"Hardener","corr_pct":h['corr_pct']})

            sp = {'Additives':1,'Resin(Fixed)':2,'Resin(Ratio)':2,'Resin(Calc)':2,'Hardener':3,'Fillers':4,'Catalysts':5}
            for ii, mc in enumerate(_custom_mat_cats):
                sp[get_mat_cat_display(mc['key'])] = 6 + ii
            mats.sort(key=lambda m: sp.get(m['type'],99))

            opt = self.round_opt.get()
            pl = {T("round_int"):0,T("round_1dp"):1,T("round_2dp"):2}.get(opt, None)
            rt = 0.0
            for m in mats:
                m['rounded_mass'] = round(m['mass'], pl) if pl is not None else m['mass']
                rt += m['rounded_mass']
            for m in mats: m['pct'] = (m['rounded_mass']/rt*100.0) if rt > 0 else 0

            fcl = (sum(m['rounded_mass']*(m['cl_ppm']/1e6) for m in mats)/rt*1e6) if rt > 0 else 0
            fmt = f"{{:.{pl}f}}" if pl is not None else "{:.2f}"
            for m in mats:
                self.tree.insert("","end", values=(m['name'],fmt.format(m['rounded_mass']),f"{m['pct']:.2f}",m['cl_ppm']),
                                 tags=(m['orig_cat'],'item'))
            self.tree.insert("","end", values=("---","---","---","---"), tags=('divider',))
            self.tree.insert("","end", values=(T("total"),fmt.format(rt),"100.00",f"{fcl:.0f}"), tags=('total',))

            # 快取供儲存使用
            self._last_mats = mats; self._last_total = rt; self._last_cl = fcl
            self._last_mode = self._mode_map().get(self.calc_mode.get(),"stoich")
        except ValueError as ve: messagebox.showerror(T("error"), str(ve))
        except Exception as e: messagebox.showerror(T("error"), str(e))

    # ── 匯出 / 儲存 ──────────────────────────────────────────────────
    def _copy(self):
        try:
            text = T("copy_hdr") + "\n"
            for item in self.tree.get_children():
                vals = self.tree.item(item,"values")
                if vals[0] == "---": continue
                text += "\t".join(map(str,vals)) + "\n"
            self.frame.clipboard_clear(); self.frame.clipboard_append(text); self.frame.update()
            messagebox.showinfo(T("copy_ok_title"),T("copy_ok"))
        except Exception as e: messagebox.showerror(T("error"),str(e))

    def _save(self):
        if not hasattr(self,'_last_mats') or not self._last_mats:
            messagebox.showwarning(T("hint"),T("warn_calc_first")); return
        top = tk.Toplevel(self.frame.winfo_toplevel())
        top.title(T("dlg_save_recipe")); top.geometry("360x160"); top.resizable(False, False)
        top.grab_set()
        ttk.Label(top, text=T("recipe_name_label")).grid(row=0, column=0, padx=10, pady=(15,5), sticky='e')
        e_name = ttk.Entry(top, width=28); e_name.grid(row=0, column=1, padx=10, pady=(15,5))
        ttk.Label(top, text=T("batch_no_label")).grid(row=1, column=0, padx=10, pady=5, sticky='e')
        e_batch = ttk.Entry(top, width=28); e_batch.grid(row=1, column=1, padx=10, pady=5)
        def do_save():
            name = e_name.get().strip()
            if not name:
                messagebox.showwarning(T("hint"),T("warn_enter_name"), parent=top); return
            batch = e_batch.get().strip()
            row = self.dm.build_recipe_row(name, batch, self._last_mode, self._last_mats,
                                           self._last_total, self._last_cl)
            self.dm.save_new_recipe(row)
            top.destroy()
            messagebox.showinfo(T("ok"), T("save_ok"))
        ttk.Button(top, text=T("btn_confirm_save"), command=do_save).grid(row=2, column=0, columnspan=2, pady=15)


# ═══════════════════════════════════════════
#  DatabaseTab  物料數據庫管理
# ═══════════════════════════════════════════
class DatabaseTab:
    H_SUBTYPES_KEYS = ["h_amine","h_polyamide","h_anhydride","h_mercaptan","h_hydroxyl"]
    H_SUBTYPES_DATA = ["胺類","聚酰胺","酸酐","巯基","羥基"]  # CSV data values
    _HST_DATA_TO_KEY = {"胺類":"amine","聚酰胺":"polyamide","酸酐":"anhydride","巯基":"mercaptan","羥基":"hydroxyl"}
    _HST_KEY_TO_DATA = {v:k for k,v in _HST_DATA_TO_KEY.items()}
    _HST_KEY_MAP = {"h_amine":"amine","h_polyamide":"polyamide","h_anhydride":"anhydride","h_mercaptan":"mercaptan","h_hydroxyl":"hydroxyl"}

    def __init__(self, nb, dm: DataManager, font_std, font_bold, rebuild_cb=None):
        self.dm = dm; self.fs = font_std; self.fb = font_bold
        self._rebuild_cb = rebuild_cb
        self.frame = ttk.Frame(nb)
        nb.add(self.frame, text=T("tab_db"))
        self._edit_name = None
        self._build()

    def _build(self):
        f = ttk.Frame(self.frame, padding=10); f.pack(fill='both', expand=True)
        left = ttk.LabelFrame(f, text=T("data_edit"), padding=10); left.pack(side='left', fill='y', padx=5)

        sel_f = ttk.Frame(left); sel_f.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0,5))
        self.lbl_sel_mat = ttk.Label(sel_f, text=T("not_selected"),
                                      font=("Microsoft JhengHei", 9, "bold"), foreground="#999")
        self.lbl_sel_mat.pack(side='left')
        ttk.Button(sel_f, text=T("btn_deselect"), command=self._deselect).pack(side='right')

        ttk.Label(left, text=T("lbl_category")).grid(row=1, column=0, sticky='w')
        self.db_cat = tk.StringVar(value=T("cat_resins"))
        self.db_cat_cb = ttk.Combobox(left, textvariable=self.db_cat, values=list(get_all_cat_display().values()), state="readonly", width=18)
        self.db_cat_cb.grid(row=1, column=1, sticky='ew', pady=2); self.db_cat_cb.bind("<<ComboboxSelected>>", self._refresh)

        # 固定編輯欄位
        for r, lbl, attr in [(2,T("lbl_name"),"e_name"),(3,T("lbl_type"),"e_type"),
                              (4,T("lbl_appearance"),"e_appear"),(5,T("lbl_viscosity"),"e_visc"),
                              (6,T("lbl_dk"),"e_dk"),(7,T("lbl_surface_energy"),"e_se"),
                              (8,T("lbl_structure"),"e_struct"),
                              (9,T("lbl_source"),"e_src"),(10,T("lbl_cl"),"e_cl")]:
            ttk.Label(left, text=lbl).grid(row=r, column=0, sticky='w')
            e = ttk.Entry(left); e.grid(row=r, column=1, sticky='ew', pady=2); setattr(self, attr, e)

        self.row_val = ttk.Frame(left); self.row_val.grid(row=11, column=0, columnspan=2, pady=5, sticky='ew')
        self.lbl_eq = ttk.Label(self.row_val, text=T("lbl_eew"), width=14); self.lbl_eq.pack(side='left')
        self.e_eq = ttk.Entry(self.row_val, font=self.fb); self.e_eq.pack(side='left', fill='x', expand=True)

        self.frm_h = ttk.LabelFrame(left, text=T("hardener_calc"), padding=5)
        ttk.Label(self.frm_h, text=T("lbl_subtype")).pack(anchor='w')
        self.cb_hst = ttk.Combobox(self.frm_h, values=[T(k) for k in self.H_SUBTYPES_KEYS], state="readonly")
        self.cb_hst.pack(fill='x', pady=2); self.cb_hst.bind("<<ComboboxSelected>>", self._on_hst)
        self.sub_frms = {}; self._build_hst_frames()

        # 自定義欄位區域
        self._custom_row_start = 15
        self.frm_custom = ttk.LabelFrame(left, text=T("custom_fields"), padding=5)
        self.frm_custom.grid(row=self._custom_row_start, column=0, columnspan=2, sticky='ew', pady=5)
        self._custom_entries = {}
        self._build_custom_entries()

        ttk.Label(left, text=T("lbl_notes")).grid(row=16, column=0, sticky='w', pady=(10,0))
        self.e_info = tk.Text(left, height=4, width=30); self.e_info.grid(row=17, column=0, columnspan=2, sticky='ew')

        btn_row = ttk.Frame(left); btn_row.grid(row=18, column=0, columnspan=2, pady=8, sticky='ew')
        ttk.Button(btn_row, text=T("btn_save"),       command=self._save).pack(side='left', fill='x', expand=True, padx=(0,3))
        ttk.Button(btn_row, text=T("btn_save_as_new"), command=self._save_as_new).pack(side='left', fill='x', expand=True, padx=3)
        ttk.Button(btn_row, text=T("btn_delete_sel"),   command=self._delete).pack(side='left', fill='x', expand=True, padx=(3,0))

        # 右側列表
        right = ttk.Frame(f); right.pack(side='right', fill='both', expand=True)
        # 管理按鈕列
        col_mgr_f = ttk.Frame(right); col_mgr_f.pack(fill='x', pady=(0,3))
        ttk.Button(col_mgr_f, text=T("btn_col_manager"), command=self._open_col_manager).pack(side='left', padx=5)
        ttk.Separator(col_mgr_f, orient='vertical').pack(side='left', fill='y', padx=4)
        ttk.Button(col_mgr_f, text=T("btn_add_mat_cat"), command=self._add_mat_cat_dialog).pack(side='left', padx=3)
        ttk.Button(col_mgr_f, text=T("btn_del_mat_cat"), command=self._del_mat_cat_dialog).pack(side='left', padx=3)
        # 樹形列表
        self._tree_frame = ttk.Frame(right)
        self._tree_frame.pack(fill='both', expand=True)
        self._build_tree()
        self._refresh()

    def _build_hst_frames(self):
        # 胺類
        f = ttk.Frame(self.frm_h)
        ttk.Label(f,text=T("lbl_amine_value")).grid(row=0,column=0,sticky='w')
        self.e_amine_av = ttk.Entry(f,width=10); self.e_amine_av.grid(row=0,column=1)
        ttk.Button(f,text=T("calc_56100_amine"),command=lambda:self._cs(self.e_amine_av,56100)).grid(row=1,column=0,columnspan=2,sticky='ew')
        self.sub_frms["amine"] = f
        # 聚酰胺
        f = ttk.Frame(self.frm_h)
        ttk.Label(f,text=T("lbl_amine_value")).grid(row=0,column=0,sticky='w'); self.e_poly_av=ttk.Entry(f,width=10); self.e_poly_av.grid(row=0,column=1)
        ttk.Label(f,text=T("lbl_coeff_f")).grid(row=1,column=0,sticky='w'); self.e_poly_f=ttk.Entry(f,width=10); self.e_poly_f.grid(row=1,column=1)
        ttk.Button(f,text=T("calc_56100_amine_f"),command=self._calc_poly).grid(row=2,column=0,columnspan=2,sticky='ew')
        ttk.Separator(f,orient='horizontal').grid(row=3,column=0,columnspan=2,sticky='ew',pady=4)
        ttk.Label(f,text=T("lbl_mw")).grid(row=4,column=0,sticky='w'); self.e_poly_mw=ttk.Entry(f,width=10); self.e_poly_mw.grid(row=4,column=1)
        ttk.Label(f,text=T("lbl_active_h")).grid(row=5,column=0,sticky='w'); self.e_poly_hn=ttk.Entry(f,width=10); self.e_poly_hn.grid(row=5,column=1)
        ttk.Button(f,text=T("calc_mw_h"),command=lambda:self._cd(self.e_poly_mw,self.e_poly_hn)).grid(row=6,column=0,columnspan=2,sticky='ew')
        self.sub_frms["polyamide"] = f
        # 酸酐
        f = ttk.Frame(self.frm_h)
        ttk.Label(f,text=T("lbl_acid_value")).grid(row=0,column=0,sticky='w'); self.e_anh_ac=ttk.Entry(f,width=10); self.e_anh_ac.grid(row=0,column=1)
        ttk.Button(f,text=T("calc_56100_acid"),command=lambda:self._cs(self.e_anh_ac,56100)).grid(row=1,column=0,columnspan=2,sticky='ew')
        ttk.Separator(f,orient='horizontal').grid(row=2,column=0,columnspan=2,sticky='ew',pady=4)
        ttk.Label(f,text=T("lbl_mw")).grid(row=3,column=0,sticky='w'); self.e_anh_mw=ttk.Entry(f,width=10); self.e_anh_mw.grid(row=3,column=1)
        ttk.Label(f,text=T("lbl_anh_groups")).grid(row=4,column=0,sticky='w'); self.e_anh_gp=ttk.Entry(f,width=10); self.e_anh_gp.grid(row=4,column=1)
        ttk.Button(f,text=T("calc_mw_anh"),command=lambda:self._cd(self.e_anh_mw,self.e_anh_gp)).grid(row=5,column=0,columnspan=2,sticky='ew')
        self.sub_frms["anhydride"] = f
        # 巯基
        f = ttk.Frame(self.frm_h)
        ttk.Label(f,text=T("lbl_mw")).grid(row=0,column=0,sticky='w'); self.e_mer_mw=ttk.Entry(f,width=10); self.e_mer_mw.grid(row=0,column=1)
        ttk.Label(f,text=T("lbl_mercapto_groups")).grid(row=1,column=0,sticky='w'); self.e_mer_gp=ttk.Entry(f,width=10); self.e_mer_gp.grid(row=1,column=1)
        ttk.Button(f,text=T("calc_mw_merc"),command=lambda:self._cd(self.e_mer_mw,self.e_mer_gp)).grid(row=2,column=0,columnspan=2,sticky='ew')
        self.sub_frms["mercaptan"] = f
        # 羥基
        f = ttk.Frame(self.frm_h)
        ttk.Label(f,text=T("lbl_oh_value")).grid(row=0,column=0,sticky='w'); self.e_hyd_oh=ttk.Entry(f,width=10); self.e_hyd_oh.grid(row=0,column=1)
        ttk.Button(f,text=T("calc_56100_oh"),command=lambda:self._cs(self.e_hyd_oh,56100)).grid(row=1,column=0,columnspan=2,sticky='ew')
        self.sub_frms["hydroxyl"] = f

    def _cs(self, ent, k):
        try:
            v = float(ent.get() or 0)
            if v > 0: self.e_eq.delete(0,tk.END); self.e_eq.insert(0,f"{k/v:.2f}")
        except: pass
    def _cd(self, emw, egp):
        try:
            mw=float(emw.get() or 0); gp=float(egp.get() or 0)
            if mw>0 and gp>0: self.e_eq.delete(0,tk.END); self.e_eq.insert(0,f"{mw/gp:.2f}")
        except: pass
    def _calc_poly(self):
        try:
            av=float(self.e_poly_av.get() or 0); f=float(self.e_poly_f.get() or 1.0)
            if av>0: self.e_eq.delete(0,tk.END); self.e_eq.insert(0,f"{56100/av*f:.2f}")
        except: pass

    def _on_hst(self, _=None):
        for frm in self.sub_frms.values(): frm.pack_forget()
        st_display = self.cb_hst.get()
        # Map display name -> internal key
        _disp_to_key = {T(k):self._HST_KEY_MAP[k] for k in self.H_SUBTYPES_KEYS}
        st = _disp_to_key.get(st_display, "")
        if st in self.sub_frms: self.sub_frms[st].pack(fill='x', pady=5)

    def _build_tree(self):
        for w in self._tree_frame.winfo_children(): w.destroy()
        vis_cols = self.dm.get_visible_mat_cols()
        col_ids = [c['db_key'] for c in vis_cols]
        self.tree = ttk.Treeview(self._tree_frame, columns=col_ids, show='headings')
        for c in vis_cols:
            hdr = f"{c['display']} ({c['unit']})" if c.get('unit') else c['display']
            self.tree.heading(c['db_key'], text=hdr)
            self.tree.column(c['db_key'], width=80, minwidth=40, stretch=False)
        vsb = ttk.Scrollbar(self._tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self._tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        self._tree_frame.grid_rowconfigure(0, weight=1)
        self._tree_frame.grid_columnconfigure(0, weight=1)
        self.tree.bind("<ButtonRelease-1>", self._on_sel)

    def _build_custom_entries(self):
        for w in self.frm_custom.winfo_children(): w.destroy()
        self._custom_entries.clear()
        custom_cols = self.dm.get_custom_mat_cols()
        if not custom_cols:
            ttk.Label(self.frm_custom, text=T("no_custom_fields"),
                      foreground="#999", font=("Arial",8)).pack(anchor='w')
            return
        for i, col in enumerate(custom_cols):
            lbl = f"{col['display']}:" if not col.get('unit') else f"{col['display']} ({col['unit']}):"
            ttk.Label(self.frm_custom, text=lbl).grid(row=i, column=0, sticky='w', pady=1)
            e = ttk.Entry(self.frm_custom)
            e.grid(row=i, column=1, sticky='ew', pady=1, padx=2)
            self._custom_entries[col['data_key']] = e
        self.frm_custom.grid_columnconfigure(1, weight=1)

    def _open_col_manager(self):
        dlg = tk.Toplevel(self.frame.winfo_toplevel())
        dlg.title(T("col_mgr_title")); dlg.geometry("520x480"); dlg.resizable(True, True)
        dlg.transient(self.frame.winfo_toplevel()); dlg.grab_set()

        ttk.Label(dlg, text=T("col_mgr_check_hint"), font=("Microsoft JhengHei",10,"bold")).pack(anchor='w', padx=10, pady=(10,5))

        # 欄位列表
        chk_frame = ttk.Frame(dlg); chk_frame.pack(fill='both', expand=True, padx=10)
        canvas = tk.Canvas(chk_frame, highlightthickness=0)
        vsb = ttk.Scrollbar(chk_frame, orient='vertical', command=canvas.yview)
        inner = ttk.Frame(canvas)
        inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0,0), window=inner, anchor='nw')
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side='left', fill='both', expand=True); vsb.pack(side='right', fill='y')

        chk_vars = {}
        for i, col in enumerate(self.dm.mat_columns):
            var = tk.BooleanVar(value=col.get('visible', True))
            locked = col.get('locked', False)
            display = col['display']
            if col.get('unit'): display += f" ({col['unit']})"
            tag = T("builtin") if col.get('builtin') else T("custom")
            txt = f"{display}   [DB: {col['db_key']}]   ({tag})"
            chk = ttk.Checkbutton(inner, text=txt, variable=var)
            if locked: chk.config(state='disabled')
            chk.grid(row=i, column=0, sticky='w', pady=1)
            chk_vars[col['db_key']] = var

        # 新增自定義欄位區
        add_f = ttk.LabelFrame(dlg, text=T("add_custom_col"), padding=8)
        add_f.pack(fill='x', padx=10, pady=5)
        r1 = ttk.Frame(add_f); r1.pack(fill='x', pady=2)
        ttk.Label(r1, text=T("lbl_display_name")).pack(side='left')
        e_disp = ttk.Entry(r1, width=14); e_disp.pack(side='left', padx=(2,8))
        ttk.Label(r1, text=T("lbl_db_key")).pack(side='left')
        e_key = ttk.Entry(r1, width=14); e_key.pack(side='left', padx=(2,8))
        ttk.Label(r1, text=T("lbl_unit")).pack(side='left')
        e_unit = ttk.Entry(r1, width=10); e_unit.pack(side='left', padx=2)

        def do_add():
            dk = e_key.get().strip(); dd = e_disp.get().strip(); du = e_unit.get().strip()
            if not dk or not dd:
                messagebox.showwarning(T("hint"),T("warn_fill_disp_key"), parent=dlg); return
            if not dk.isidentifier():
                messagebox.showwarning(T("hint"),T("warn_key_format"), parent=dlg); return
            if not self.dm.add_mat_column(dk, dd, du):
                messagebox.showwarning(T("hint"),T("warn_key_exists",dk), parent=dlg); return
            var = tk.BooleanVar(value=True); chk_vars[dk] = var
            idx = len(self.dm.mat_columns) - 1
            _ctag = T("col_custom_tag")
            txt = f"{dd}   [DB: {dk}]   ({_ctag})"
            if du: txt = f"{dd} ({du})   [DB: {dk}]   ({_ctag})"
            ttk.Checkbutton(inner, text=txt, variable=var).grid(row=idx, column=0, sticky='w', pady=1)
            for ew in [e_disp, e_key, e_unit]: ew.delete(0, tk.END)
            messagebox.showinfo(T("ok"), T("col_added",dd), parent=dlg)

        def do_del():
            custom = self.dm.get_custom_mat_cols()
            if not custom:
                messagebox.showinfo(T("hint"),T("no_custom_col_del"), parent=dlg); return
            names = [f"{c['display']} [{c['db_key']}]" for c in custom]
            del_dlg = tk.Toplevel(dlg); del_dlg.title(T("del_custom_col_title")); del_dlg.geometry("300x200")
            del_dlg.transient(dlg); del_dlg.grab_set()
            lb = tk.Listbox(del_dlg, selectmode='browse')
            for n in names: lb.insert(tk.END, n)
            lb.pack(fill='both', expand=True, padx=10, pady=5)
            def confirm_del():
                sel = lb.curselection()
                if not sel: return
                col = custom[sel[0]]
                if messagebox.askyesno(T("confirm"), T("confirm_del_col",col["display"]), parent=del_dlg):
                    self.dm.remove_mat_column(col['db_key'])
                    del_dlg.destroy()
                    dlg.destroy()
                    self._open_col_manager()
            ttk.Button(del_dlg, text=T("btn_delete_sel"), command=confirm_del).pack(pady=5)

        r2 = ttk.Frame(add_f); r2.pack(fill='x', pady=2)
        ttk.Button(r2, text=T("btn_add_col"), command=do_add).pack(side='left', padx=(0,8))
        ttk.Button(r2, text=T("btn_del_custom_col"), command=do_del).pack(side='left')

        def on_close():
            for col in self.dm.mat_columns:
                if col['db_key'] in chk_vars:
                    col['visible'] = chk_vars[col['db_key']].get()
            self.dm._save_mat_col_config()
            self._build_tree()
            self._build_custom_entries()
            self._refresh()
            dlg.destroy()

        ttk.Button(dlg, text=T("col_mgr_ok"), command=on_close).pack(pady=8)
        dlg.protocol("WM_DELETE_WINDOW", on_close)


    # ── 自定義物料種類管理 ─────────────────────────────────────────
    def _add_mat_cat_dialog(self):
        top = tk.Toplevel(self.frame.winfo_toplevel())
        top.title(T("dlg_add_mat_cat")); top.geometry("520x500"); top.resizable(False, False)
        top.grab_set()

        # ── 基本資訊 ──
        info_f = ttk.LabelFrame(top, text=T("lbl_basic_info"), padding=8)
        info_f.pack(fill='x', padx=12, pady=(10,5))

        r = 0
        ttk.Label(info_f, text=T("lbl_mat_cat_key")).grid(row=r, column=0, padx=5, pady=3, sticky='e')
        e_key = ttk.Entry(info_f, width=20); e_key.grid(row=r, column=1, padx=5, pady=3, sticky='w')
        ttk.Label(info_f, text=T("lbl_mat_cat_key_hint"), foreground="#888",
                  font=("Arial",8)).grid(row=r, column=2, padx=5, sticky='w')
        r += 1
        ttk.Label(info_f, text=T("lbl_mat_cat_csv")).grid(row=r, column=0, padx=5, pady=3, sticky='e')
        e_csv = ttk.Entry(info_f, width=20); e_csv.grid(row=r, column=1, padx=5, pady=3, sticky='w')
        ttk.Label(info_f, text=T("lbl_mat_cat_csv_hint"), foreground="#888",
                  font=("Arial",8)).grid(row=r, column=2, padx=5, sticky='w')

        # ── 多語言名稱 ──
        lang_f = ttk.LabelFrame(top, text=T("lbl_lang_names"), padding=8)
        lang_f.pack(fill='x', padx=12, pady=5)

        entries_lang = {}
        lang_labels = {"zh_TW":"lbl_lang_zh_tw","zh_CN":"lbl_lang_zh_cn","en":"lbl_lang_en","ja":"lbl_lang_ja"}
        for i, (lang_code, lbl_key) in enumerate(lang_labels.items()):
            lbl_txt = T(lbl_key)
            if lang_code == _CURRENT_LANG: lbl_txt = "★ " + lbl_txt
            ttk.Label(lang_f, text=lbl_txt).grid(row=i, column=0, padx=5, pady=2, sticky='e')
            e = ttk.Entry(lang_f, width=22); e.grid(row=i, column=1, padx=5, pady=2, sticky='w')
            entries_lang[lang_code] = e

        # ── 欄位選擇 ──
        field_f = ttk.LabelFrame(top, text=T("lbl_field_select"), padding=8)
        field_f.pack(fill='x', padx=12, pady=5)

        v_eew    = tk.BooleanVar(value=False)
        v_type   = tk.BooleanVar(value=True)
        v_appear = tk.BooleanVar(value=False)
        v_visc   = tk.BooleanVar(value=False)
        v_dk     = tk.BooleanVar(value=False)
        v_se     = tk.BooleanVar(value=False)
        v_struct = tk.BooleanVar(value=False)
        v_cl     = tk.BooleanVar(value=True)
        v_src    = tk.BooleanVar(value=False)

        field_items = [
            (v_eew,    "field_eew"),
            (v_type,   "field_type"),
            (v_appear, "field_appearance"),
            (v_visc,   "field_viscosity"),
            (v_dk,     "field_dk"),
            (v_se,     "field_surface_energy"),
            (v_struct, "field_structure"),
            (v_cl,     "field_cl"),
            (v_src,    "field_source"),
        ]
        for i, (var, lbl_k) in enumerate(field_items):
            row_i = i // 2; col_i = (i % 2) * 2
            ttk.Checkbutton(field_f, text=T(lbl_k), variable=var).grid(
                row=row_i, column=col_i, padx=(10,20), pady=1, sticky='w')

        def do_add():
            key = e_key.get().strip(); csv_nm = e_csv.get().strip()
            cur_name = entries_lang[_CURRENT_LANG].get().strip()
            if not key or not csv_nm or not cur_name:
                messagebox.showwarning(T("hint"), T("warn_mat_cat_key_empty"), parent=top); return
            all_keys = set(SLOT_COUNTS.keys()) | {mc['key'] for mc in _custom_mat_cats}
            if key in all_keys:
                messagebox.showwarning(T("hint"), T("warn_mat_cat_key_exists", key), parent=top); return
            new_mc = {
                "key": key, "csv_name": csv_nm,
                "zh_TW": entries_lang["zh_TW"].get().strip() or cur_name,
                "zh_CN": entries_lang["zh_CN"].get().strip() or cur_name,
                "en":    entries_lang["en"].get().strip() or cur_name,
                "ja":    entries_lang["ja"].get().strip() or cur_name,
                "has_eew": v_eew.get(), "has_type": v_type.get(),
                "has_appearance": v_appear.get(), "has_viscosity": v_visc.get(),
                "has_dk": v_dk.get(), "has_surface_energy": v_se.get(),
                "has_structure": v_struct.get(), "has_cl": v_cl.get(),
                "has_source": v_src.get()
            }
            _custom_mat_cats.append(new_mc)
            _save_custom_mat_cats()
            self.dm.materials[key] = {}  # Init empty material dict
            top.destroy()
            if self._rebuild_cb: self._rebuild_cb()
            else:
                self.db_cat_cb['values'] = list(get_all_cat_display().values())
                messagebox.showinfo(T("ok"), T("mat_cat_added", cur_name))

        ttk.Button(top, text=T("btn_add_mat_cat"), command=do_add).pack(pady=10)

    def _del_mat_cat_dialog(self):
        if not _custom_mat_cats:
            messagebox.showinfo(T("hint"), T("no_custom_mat_cat")); return
        top = tk.Toplevel(self.frame.winfo_toplevel())
        top.title(T("dlg_del_mat_cat")); top.geometry("400x300"); top.resizable(False, False)
        top.grab_set()

        ttk.Label(top, text=T("dlg_del_mat_cat"), font=("Arial",10,"bold")).pack(pady=(10,5))
        lb = tk.Listbox(top, height=8, font=("Arial",10))
        lb.pack(fill='both', expand=True, padx=15, pady=5)
        for mc in _custom_mat_cats:
            lb.insert(tk.END, f"{mc['key']}  —  {get_mat_cat_display(mc['key'])}")

        def do_del():
            sel = lb.curselection()
            if not sel: return
            idx = sel[0]; mc = _custom_mat_cats[idx]
            key = mc['key']; disp = get_mat_cat_display(key)
            if not messagebox.askyesno(T("confirm_delete_title"),
                                       T("confirm_del_mat_cat", disp), parent=top): return
            if key in self.dm.materials: del self.dm.materials[key]
            self.dm.save_materials()
            _custom_mat_cats.pop(idx)
            _save_custom_mat_cats()
            top.destroy()
            if self._rebuild_cb: self._rebuild_cb()
            else:
                self.db_cat_cb['values'] = list(get_all_cat_display().values())
                if self._cat_key() == key: self.db_cat.set(T("cat_resins"))
                self._refresh()
                messagebox.showinfo(T("ok"), T("mat_cat_deleted", disp))

        ttk.Button(top, text=T("btn_del_mat_cat"), command=do_del).pack(pady=10)

    def _cat_key(self): return {v:k for k,v in get_all_cat_display().items()}.get(self.db_cat.get(),"resins")

    def _clear(self):
        for attr in ['e_name','e_type','e_appear','e_visc','e_dk','e_se','e_struct','e_src','e_cl','e_eq',
                     'e_amine_av','e_poly_av','e_poly_mw','e_poly_hn',
                     'e_anh_ac','e_anh_mw','e_anh_gp','e_mer_mw','e_mer_gp','e_hyd_oh']:
            getattr(self,attr).delete(0,tk.END)
        if hasattr(self,'e_poly_f'): self.e_poly_f.delete(0,tk.END); self.e_poly_f.insert(0,"1.0")
        self.e_info.delete("1.0",tk.END); self.cb_hst.set(''); self._edit_name = None
        self.lbl_sel_mat.config(text=T("not_selected"), foreground="#999")
        for ent in self._custom_entries.values(): ent.delete(0,tk.END)

    def _refresh(self, _=None):
        self.tree.delete(*self.tree.get_children()); self._clear()
        cat = self._cat_key(); data = self.dm.materials.get(cat,{})
        cmc = _get_custom_mat_cat(cat)
        if cat == "resins": self.row_val.grid(); self.lbl_eq.config(text=T("lbl_eew")); self.frm_h.grid_remove()
        elif cat == "hardeners": self.row_val.grid(); self.lbl_eq.config(text=T("lbl_ahew")); self.frm_h.grid(row=12,column=0,columnspan=2,pady=5,sticky='ew')
        elif cmc and cmc.get('has_eew'): self.row_val.grid(); self.lbl_eq.config(text=T("lbl_eew")); self.frm_h.grid_remove()
        else: self.row_val.grid_remove(); self.frm_h.grid_remove()
        vis_cols = self.dm.get_visible_mat_cols()
        for name, info in sorted(data.items()):
            vals = []
            for c in vis_cols:
                dk = c.get('data_key','')
                if dk == '_name': vals.append(name)
                elif dk == '_eq':
                    _cmc = _get_custom_mat_cat(cat)
                    if cat=="resins" or (_cmc and _cmc.get('has_eew')):
                        eq = f"{info.get('eew',0):.2f}"
                    elif cat=="hardeners":
                        eq = f"{self.dm.get_active_eq(info):.2f}"
                    else:
                        eq = "—"
                    vals.append(eq)
                elif dk == 'cl': vals.append(info.get('cl',0))
                else: vals.append(info.get(dk, ''))
            self.tree.insert("","end", values=vals)
        self._autofit_columns()

    def _autofit_columns(self):
        import tkinter.font as tkfont
        ft = tkfont.Font(family="Microsoft JhengHei", size=9)
        pad = 16
        vis_cols = self.dm.get_visible_mat_cols()
        for c in vis_cols:
            cid = c['db_key']
            hdr = f"{c['display']} ({c['unit']})" if c.get('unit') else c['display']
            max_w = ft.measure(hdr) + pad
            for item in self.tree.get_children():
                vals = self.tree.item(item)['values']
                idx = [cc['db_key'] for cc in vis_cols].index(cid)
                txt = str(vals[idx]) if idx < len(vals) else ""
                w = ft.measure(txt) + pad
                if w > max_w: max_w = w
            self.tree.column(cid, width=max(max_w, 50))

    def _on_sel(self, _):
        sel = self.tree.selection()
        if not sel: return
        name = self.tree.item(sel[0])['values'][0]; cat = self._cat_key(); info = self.dm.materials[cat].get(name,{})
        self._clear(); self._edit_name = name
        self.lbl_sel_mat.config(text=T("editing")+name, foreground="#0066cc")
        self.e_name.insert(0,name); self.e_type.insert(0,info.get('type',''))
        self.e_appear.insert(0,info.get('appearance','')); self.e_visc.insert(0,info.get('viscosity',''))
        self.e_dk.insert(0,info.get('dk','')); self.e_se.insert(0,info.get('surface_energy',''))
        self.e_struct.insert(0,info.get('structure','')); self.e_src.insert(0,info.get('source',''))
        self.e_cl.insert(0,str(info.get('cl',0))); self.e_info.insert("1.0",info.get('desc',''))
        for dk, ent in self._custom_entries.items():
            ent.insert(0, str(info.get(dk, '')))
        cmc_sel = _get_custom_mat_cat(cat)
        if cat=="resins" or (cmc_sel and cmc_sel.get('has_eew')):
            self.e_eq.insert(0,str(info.get('eew',0)))
        elif cat=="hardeners":
            st_data=info.get('h_subtype','')
            _hst_data_to_disp = {d:T(k) for k,d in zip(self.H_SUBTYPES_KEYS, self.H_SUBTYPES_DATA)}
            self.cb_hst.set(_hst_data_to_disp.get(st_data, st_data)); self._on_hst()
            self.e_eq.insert(0,f"{self.dm.get_active_eq(info):.2f}")
            st = self._HST_DATA_TO_KEY.get(st_data, st_data)
            if st=="amine": self.e_amine_av.insert(0,str(info.get('amine_value','')))
            elif st=="polyamide":
                self.e_poly_av.insert(0,str(info.get('amine_value','')))
                self.e_poly_f.delete(0,tk.END); self.e_poly_f.insert(0,str(info.get('f_factor',1.0)))
                self.e_poly_mw.insert(0,str(info.get('mw',''))); self.e_poly_hn.insert(0,str(info.get('func_group_num','')))
            elif st=="anhydride":
                self.e_anh_ac.insert(0,str(info.get('acid_value',''))); self.e_anh_mw.insert(0,str(info.get('mw',''))); self.e_anh_gp.insert(0,str(info.get('func_group_num','')))
            elif st=="mercaptan": self.e_mer_mw.insert(0,str(info.get('mw',''))); self.e_mer_gp.insert(0,str(info.get('func_group_num','')))
            elif st=="hydroxyl": self.e_hyd_oh.insert(0,str(info.get('hydroxyl_value','')))

    def _save(self):
        cat=self._cat_key(); name=self.e_name.get().strip()
        if not name: messagebox.showwarning(T("hint"),T("warn_enter_mat_name")); return
        if self._edit_name and self._edit_name!=name: del self.dm.materials[cat][self._edit_name]
        nd = self._collect_form_data(cat)
        if nd is None: return
        self.dm.materials[cat][name]=nd; self.dm.save_materials(); self._refresh()
        self._on_sel_by_name(name)
        messagebox.showinfo(T("ok"),T("saved_to_db"))

    def _save_as_new(self):
        cat=self._cat_key(); name=self.e_name.get().strip()
        if not name: messagebox.showwarning(T("hint"),T("warn_enter_mat_name")); return
        if name in self.dm.materials.get(cat,{}):
            if not messagebox.askyesno(T("name_exists_title"),
                T("name_exists_overwrite", name, self.db_cat.get())):
                return
        nd = self._collect_form_data(cat)
        if nd is None: return
        self.dm.materials[cat][name]=nd; self.dm.save_materials(); self._refresh()
        self._on_sel_by_name(name)
        messagebox.showinfo(T("ok"),T("saved_as_new", name))

    def _collect_form_data(self, cat):
        try:
            eq_val = float(self.e_eq.get() or 0)
        except ValueError:
            messagebox.showwarning(T("hint"),T("warn_eq_format")); return None
        nd={"type":self.e_type.get().strip(),
            "appearance":self.e_appear.get().strip(),
            "viscosity":self.e_visc.get().strip(),
            "dk":self.e_dk.get().strip(),
            "surface_energy":self.e_se.get().strip(),
            "structure":self.e_struct.get().strip(),
            "source":self.e_src.get().strip(),"desc":self.e_info.get("1.0",tk.END).strip(),
            "cl":float(self.e_cl.get() or 0)}
        for dk, ent in self._custom_entries.items():
            nd[dk] = ent.get().strip()
        cmc_col = _get_custom_mat_cat(cat)
        if cat=="resins" or (cmc_col and cmc_col.get('has_eew')): nd["eew"]=eq_val
        elif cat=="hardeners":
            _hst_map = {T(k):d for k,d in zip(self.H_SUBTYPES_KEYS, self.H_SUBTYPES_DATA)}
            st_data=_hst_map.get(self.cb_hst.get(), self.cb_hst.get()); nd["h_subtype"]=st_data
            st = self._HST_DATA_TO_KEY.get(st_data, st_data)
            nd["ahew"]=eq_val
            if st=="amine": nd["amine_value"]=float(self.e_amine_av.get() or 0)
            elif st=="polyamide": nd["polyamide_eq"]=eq_val; nd["amine_value"]=float(self.e_poly_av.get() or 0); nd["f_factor"]=float(self.e_poly_f.get() or 1.0); nd["mw"]=float(self.e_poly_mw.get() or 0); nd["func_group_num"]=float(self.e_poly_hn.get() or 0)
            elif st=="anhydride": nd["anhydride_eq"]=eq_val; nd["acid_value"]=float(self.e_anh_ac.get() or 0); nd["mw"]=float(self.e_anh_mw.get() or 0); nd["func_group_num"]=float(self.e_anh_gp.get() or 0)
            elif st=="mercaptan": nd["mercapto_eq"]=eq_val; nd["mw"]=float(self.e_mer_mw.get() or 0); nd["func_group_num"]=float(self.e_mer_gp.get() or 0)
            elif st=="hydroxyl": nd["hydroxyl_eq"]=eq_val; nd["hydroxyl_value"]=float(self.e_hyd_oh.get() or 0)
        return nd

    def _on_sel_by_name(self, name):
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == name:
                self.tree.selection_set(item)
                self.tree.see(item)
                self._edit_name = name
                self.lbl_sel_mat.config(text=T("editing")+name, foreground="#0066cc")
                return

    def _deselect(self):
        self.tree.selection_remove(*self.tree.selection())
        self._clear()
        for frm in self.sub_frms.values(): frm.pack_forget()

    def _delete(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning(T("hint"),T("warn_select_delete")); return
        name=self.tree.item(sel[0])['values'][0]; cat=self._cat_key()
        if not messagebox.askyesno(T("confirm"),T("confirm_delete", name)): return
        del self.dm.materials[cat][name]; self.dm.save_materials(); self._refresh()


# ═══════════════════════════════════════════
#  RecipeTab  配方管理 + 物性錄入
# ═══════════════════════════════════════════
class RecipeTab:
    def __init__(self, nb, dm: DataManager, font_std, font_bold):
        self.dm = dm; self.fs = font_std; self.fb = font_bold
        self.frame = ttk.Frame(nb)
        nb.add(self.frame, text=T("tab_recipe_mgr"))
        self._sel_recipe = None
        self._prop_entries = {}          # {prop_name: ttk.Entry}
        self._prop_frames  = {}          # {category: (frame, toggle_btn, is_visible_var)}
        self._build()

    def _build(self):
        pw = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        pw.pack(fill='both', expand=True, padx=5, pady=5)

        # ── 左側 ──────────────────────────────────────────────────────
        left = ttk.Frame(pw); pw.add(left, weight=1)

        # 配方清單
        rf = ttk.LabelFrame(left, text=T("recipe_list_title"), padding=5); rf.pack(fill='both', expand=True)
        rcols = [("name",T("col_recipe_name"),150),("batch",T("col_batch"),90),("date",T("col_date"),140),("mass",T("col_total_mass"),80)]
        self.recipe_tree = ttk.Treeview(rf, columns=[c[0] for c in rcols], show='headings', height=9)
        for cid,hdr,w in rcols: self.recipe_tree.heading(cid,text=hdr); self.recipe_tree.column(cid,width=w,anchor='center')
        vsb_r = ttk.Scrollbar(rf, orient="vertical", command=self.recipe_tree.yview)
        self.recipe_tree.configure(yscrollcommand=vsb_r.set)
        self.recipe_tree.pack(side='left', fill='both', expand=True); vsb_r.pack(side='right', fill='y')
        self.recipe_tree.bind("<<TreeviewSelect>>", self._on_sel)

        # 配方操作按鈕
        bf = ttk.Frame(left); bf.pack(fill='x', pady=3)
        ttk.Button(bf, text=T("btn_refresh"), command=self.refresh).pack(side='left', fill='x', expand=True, padx=(0,3))
        ttk.Button(bf, text=T("btn_rename"),  command=self._rename).pack(side='left', fill='x', expand=True, padx=3)
        ttk.Button(bf, text=T("btn_delete"),    command=self._delete).pack(side='left', fill='x', expand=True, padx=(3,0))

        # 配方組成預覽
        pf = ttk.LabelFrame(left, text=T("recipe_composition"), padding=5); pf.pack(fill='both', expand=True, pady=5)
        self.detail_txt = tk.Text(pf, wrap='word', state='disabled', font=("Microsoft JhengHei",9), height=14)
        vsb_d = ttk.Scrollbar(pf, orient="vertical", command=self.detail_txt.yview)
        self.detail_txt.configure(yscrollcommand=vsb_d.set)
        self.detail_txt.pack(side='left', fill='both', expand=True); vsb_d.pack(side='right', fill='y')

        # 複製 / 匯出
        ef = ttk.Frame(left); ef.pack(fill='x', pady=3)
        ttk.Button(ef, text=T("btn_copy_vertical"), command=self._copy_row).pack(fill='x')

        # ── 右側：物性編輯器 ───────────────────────────────────────────
        right = ttk.Frame(pw); pw.add(right, weight=2)
        paned_r = ttk.PanedWindow(right, orient=tk.VERTICAL); paned_r.pack(fill='both', expand=True)

        # 物性表單（上半）
        prop_outer = ttk.LabelFrame(right, text=T("prop_input"), padding=5)
        paned_r.add(prop_outer, weight=3)

        sel_row = ttk.Frame(prop_outer); sel_row.pack(fill='x', pady=(0,3))
        self.lbl_sel_recipe = ttk.Label(sel_row, text=T("no_recipe_selected"),
                                         font=("Microsoft JhengHei", 10, "bold"), foreground="#999")
        self.lbl_sel_recipe.pack(side='left', padx=5)
        ttk.Button(sel_row, text=T("btn_deselect"), command=self._deselect_recipe).pack(side='left', padx=8)

        tool_row = ttk.Frame(prop_outer); tool_row.pack(fill='x', pady=(0,5))
        ttk.Button(tool_row, text=T("btn_save_all_props"), command=self._save_props, style="Accent.TButton").pack(side='left')
        ttk.Button(tool_row, text=T("btn_clear_all_props"),    command=self._clear_props).pack(side='left', padx=8)
        ttk.Button(tool_row, text=T("btn_toggle_expand"),      command=self._toggle_all).pack(side='left')
        self._all_expanded = True

        # 可滾動物性表單
        prop_canvas = tk.Canvas(prop_outer, highlightthickness=0)
        vsb_p = ttk.Scrollbar(prop_outer, orient="vertical", command=prop_canvas.yview)
        self.prop_scroll_frame = ttk.Frame(prop_canvas)
        self.prop_scroll_frame.bind("<Configure>",
            lambda e: prop_canvas.configure(scrollregion=prop_canvas.bbox("all")))
        prop_canvas.create_window((0,0), window=self.prop_scroll_frame, anchor="nw")
        prop_canvas.configure(yscrollcommand=vsb_p.set)
        prop_canvas.pack(side="left", fill="both", expand=True); vsb_p.pack(side="right", fill="y")
        # 滑鼠滾輪
        prop_canvas.bind_all("<MouseWheel>", lambda e: prop_canvas.yview_scroll(int(-1*(e.delta/120)),"units"))
        self._prop_canvas = prop_canvas

        self._build_prop_form()

        # 自定義物性管理（下半）
        custom_outer = ttk.LabelFrame(right, text=T("custom_prop_mgr"), padding=5)
        paned_r.add(custom_outer, weight=1)
        self._build_custom_panel(custom_outer)

        self.refresh()

    # ── 物性表單建立 ─────────────────────────────────────────────────
    def _build_prop_form(self):
        for w in self.prop_scroll_frame.winfo_children(): w.destroy()
        self._prop_entries.clear()
        self._prop_frames.clear()
        self._prop_subgroup_frames = {}

        defs = self.dm.get_prop_defs_structured()
        outer_row = 0
        for cat, items in defs.items():
            # ── 分類標題行 ─────────────────────────────────────────
            hdr_f = ttk.Frame(self.prop_scroll_frame)
            hdr_f.grid(row=outer_row, column=0, columnspan=6, sticky='ew', pady=(8,1))
            outer_row += 1
            visible_var = tk.BooleanVar(value=True)
            content_f = ttk.LabelFrame(self.prop_scroll_frame, padding=(5,2))
            content_f.grid(row=outer_row, column=0, columnspan=6, sticky='ew', padx=10)
            outer_row += 1

            btn = ttk.Button(hdr_f, text=f"▼  {T_propcat(cat)}")
            btn.config(command=lambda c=content_f, v=visible_var, b=btn: self._toggle_any(c, v, b))
            btn.pack(side='left')
            self._prop_frames[cat] = (content_f, btn, visible_var)

            # ── 渲染此分類的所有項目（含子群）─────────────────────
            self._render_prop_items(content_f, items)

        self._prop_canvas.configure(scrollregion=self._prop_canvas.bbox("all"))

    def _render_prop_items(self, container, items):
        inner_row = 0
        reg_buf = []

        def flush():
            nonlocal inner_row
            if not reg_buf: return
            for i, (pname, unit, method) in enumerate(reg_buf):
                r = inner_row + i // 2
                c = (i % 2) * 3
                ttk.Label(container, text=T_prop(pname), width=22, anchor='w',
                          font=("Microsoft JhengHei", 9)).grid(
                              row=r, column=c, sticky='w', padx=(5,2), pady=2)
                ent = ttk.Entry(container, width=13)
                ent.grid(row=r, column=c+1, sticky='ew', padx=2, pady=2)
                ToolTip(ent, T("unit_tooltip", unit, T_method(method)))
                ttk.Label(container, text=unit, foreground="#888",
                          font=("Arial", 8)).grid(row=r, column=c+2, sticky='w', padx=(0,10))
                self._prop_entries[pname] = ent
            inner_row += (len(reg_buf) + 1) // 2
            reg_buf.clear()

        for item in items:
            if isinstance(item, tuple) and item[0] == '__group__':
                flush()
                _, grp_name, grp_items = item

                # 子群標題
                grp_hdr = ttk.Frame(container)
                grp_hdr.grid(row=inner_row, column=0, columnspan=6, sticky='ew', pady=(6,0))
                inner_row += 1
                grp_vis = tk.BooleanVar(value=True)
                grp_content = ttk.LabelFrame(container, text="", padding=(4,2))
                grp_content.grid(row=inner_row, column=0, columnspan=6,
                                 sticky='ew', padx=18, pady=(0,4))
                inner_row += 1

                grp_btn = ttk.Button(grp_hdr, text=f"  ▼ 【{T_group(grp_name)}】")
                grp_btn.config(command=lambda c=grp_content, v=grp_vis, b=grp_btn: self._toggle_any(c, v, b))
                grp_btn.pack(side='left', padx=(18,0))
                self._prop_subgroup_frames[grp_name] = (grp_content, grp_btn, grp_vis)

                # 子群項目：2欄並排
                for j, (pname, unit, method) in enumerate(grp_items):
                    gr = j // 2; gc = (j % 2) * 3
                    ttk.Label(grp_content, text=T_prop(pname), width=22, anchor='w',
                              font=("Microsoft JhengHei", 9)).grid(
                                  row=gr, column=gc, sticky='w', padx=(5,2), pady=2)
                    ent = ttk.Entry(grp_content, width=13)
                    ent.grid(row=gr, column=gc+1, sticky='ew', padx=2, pady=2)
                    ToolTip(ent, T("unit_tooltip", unit, T_method(method)))
                    ttk.Label(grp_content, text=unit, foreground="#888",
                              font=("Arial", 8)).grid(row=gr, column=gc+2, sticky='w', padx=(0,10))
                    self._prop_entries[pname] = ent
            else:
                reg_buf.append(item)
        flush()

    def _toggle_any(self, frame, visible_var, btn):
        if visible_var.get():
            frame.grid_remove(); visible_var.set(False)
            btn.config(text=btn.cget('text').replace('▼', '▶'))
        else:
            frame.grid(); visible_var.set(True)
            btn.config(text=btn.cget('text').replace("▶", "▼"))

    def _toggle_all(self):
        self._all_expanded = not self._all_expanded
        # 分類層
        for cat, (cf, btn, v) in self._prop_frames.items():
            if self._all_expanded:
                cf.grid(); v.set(True)
                if btn: btn.config(text=btn.cget('text').replace('▶','▼'))
            else:
                cf.grid_remove(); v.set(False)
                if btn: btn.config(text=btn.cget('text').replace("▼","▶"))
        # 子群層（同步展開/折疊）
        for grp, (cf, btn, v) in self._prop_subgroup_frames.items():
            if self._all_expanded:
                cf.grid(); v.set(True)
                if btn: btn.config(text=btn.cget('text').replace('▶','▼'))
            else:
                cf.grid_remove(); v.set(False)
                if btn: btn.config(text=btn.cget('text').replace("▼","▶"))

    # ── 物性定義管理面板 ──────────────────────────────────────────────
    def _build_custom_panel(self, parent):
        # 說明標籤
        info_f = ttk.Frame(parent); info_f.pack(fill='x', padx=5, pady=(0,3))
        ttk.Label(info_f, text=T("prop_info_hint"),
                  font=("Microsoft JhengHei",9), foreground="#555").pack(side='left')
        ttk.Button(info_f, text=T("btn_restore_builtin"), command=self._restore_builtins).pack(side='right', padx=5)

        # ── 搜尋列 ─────────────────────────────────────────────────
        sf = ttk.Frame(parent); sf.pack(fill='x', padx=5, pady=2)
        ttk.Label(sf, text=T("search")).pack(side='left')
        self.e_search = ttk.Entry(sf, width=20); self.e_search.pack(side='left', padx=5)
        self.e_search.bind('<KeyRelease>', self._filter_prop_defs)
        ttk.Label(sf, text=T("cat_filter")).pack(side='left', padx=(10,2))
        self.cb_filter_cat = ttk.Combobox(sf, state="readonly", width=18)
        self.cb_filter_cat.pack(side='left')
        self.cb_filter_cat.bind("<<ComboboxSelected>>", self._filter_prop_defs)
        ttk.Button(sf, text=T("btn_clear_filter"), command=self._clear_filter).pack(side='left', padx=6)
        self.lbl_count = ttk.Label(sf, text="", foreground="#777", font=("Arial",9))
        self.lbl_count.pack(side='right', padx=5)

        # ── 物性定義總覽表 ─────────────────────────────────────────
        tree_f = ttk.Frame(parent); tree_f.pack(fill='both', expand=True, padx=5)
        cols = [("src",T("col_src"),50),("cat",T("col_cat"),100),("name",T("col_prop_display"),170),("dbkey",T("col_dbkey"),120),("unit",T("lbl_unit").rstrip(":"),65),("method",T("col_method"),220),("_iname","",0),("_icat","",0)]
        self.def_tree = ttk.Treeview(tree_f, columns=[c[0] for c in cols], show='headings', height=9,
                                     selectmode='browse')
        for cid,hdr,w in cols:
            self.def_tree.heading(cid, text=hdr)
            self.def_tree.column(cid, width=w, minwidth=0, stretch=(w>0), anchor='center' if cid in ('src','unit') else 'w')
        # 顏色標識：內建=淺灰，使用者追加=預設
        self.def_tree.tag_configure('builtin', foreground="#888888")
        self.def_tree.tag_configure('user',    foreground="#1a5f9e")
        vsb = ttk.Scrollbar(tree_f, orient="vertical", command=self.def_tree.yview)
        self.def_tree.configure(yscrollcommand=vsb.set)
        self.def_tree.pack(side='left', fill='both', expand=True); vsb.pack(side='right', fill='y')

        # ── 新增 / 刪除列 ─────────────────────────────────────────
        add_f = ttk.LabelFrame(parent, text=T("add_prop_def"), padding=(8,4)); add_f.pack(fill='x', padx=5, pady=(5,0))

        row1 = ttk.Frame(add_f); row1.pack(fill='x', pady=2)
        ttk.Label(row1, text=T("lbl_display_name"), width=10).pack(side='left')
        self.e_pname  = ttk.Entry(row1, width=18); self.e_pname.pack(side='left', padx=(0,6))
        ttk.Label(row1, text=T("lbl_db_key")).pack(side='left')
        self.e_pdbkey = ttk.Entry(row1, width=16); self.e_pdbkey.pack(side='left', padx=(0,6))
        ttk.Label(row1, text=T("lbl_unit")).pack(side='left')
        self.e_punit  = ttk.Entry(row1, width=8); self.e_punit.pack(side='left', padx=(0,6))

        row1b = ttk.Frame(add_f); row1b.pack(fill='x', pady=2)
        ttk.Label(row1b, text=T("lbl_test_method"), width=10).pack(side='left')
        self.e_pmethod = ttk.Entry(row1b, width=40); self.e_pmethod.pack(side='left', fill='x', expand=True)

        row2 = ttk.Frame(add_f); row2.pack(fill='x', pady=2)
        ttk.Label(row2, text=T("lbl_target_cat"), width=10).pack(side='left')
        self.cb_pcat = ttk.Combobox(row2, width=22)
        self.cb_pcat.pack(side='left', padx=(0,8))
        ttk.Label(row2, text=T("cat_input_hint"),
                  foreground="#888", font=("Arial",8)).pack(side='left')

        row3 = ttk.Frame(add_f); row3.pack(fill='x', pady=(3,4))
        ttk.Button(row3, text=T("btn_add_prop"),       command=self._add_prop_def).pack(side='left', padx=(0,8))
        ttk.Button(row3, text=T("btn_del_prop"), command=self._del_prop_def).pack(side='left', padx=(0,8))
        ttk.Button(row3, text=T("btn_copy_prop"),  command=self._copy_def_to_input).pack(side='left', padx=(0,8))
        ttk.Separator(row3, orient='vertical').pack(side='left', fill='y', padx=6)
        ttk.Button(row3, text=T("btn_add_cat"),  command=self._add_cat_dialog).pack(side='left', padx=(0,8))
        ttk.Button(row3, text=T("btn_del_cat"),  command=self._del_cat_dialog).pack(side='left')

        self._refresh_prop_defs()

    def _get_all_cats_for_combo(self):
        """Return translated display names for all categories."""
        return [T_propcat(c) for c in self.dm.get_all_categories()]

    def _refresh_prop_defs(self, search="", cat_filter=""):
        self.def_tree.delete(*self.def_tree.get_children())
        builtin_names = self.dm.get_all_builtin_names()
        defs = self.dm.get_all_prop_defs()
        total = 0
        for cat, items in defs.items():
            if cat_filter and cat != cat_filter: continue
            for name, unit, method in items:
                if search and search.lower() not in T_prop(name).lower() and search.lower() not in T_propcat(cat).lower(): continue
                is_builtin = name in builtin_names
                src  = T("src_builtin") if is_builtin else T("src_user")
                tag  = 'builtin' if is_builtin else 'user'
                dbkey = self.dm.get_prop_csv_key(name)
                dbkey_display = dbkey if dbkey != name else T("eq_display_name")
                self.def_tree.insert("","end", values=(src, T_propcat(cat), T_prop(name), dbkey_display, unit, T_method(method), name, cat), tags=(tag,))
                total += 1
        self.lbl_count.config(text=T("total_items", total))
        cats = [T("all_cats")] + self._get_all_cats_for_combo()
        self.cb_filter_cat['values'] = cats
        self.cb_pcat['values'] = self._get_all_cats_for_combo()

    def _filter_prop_defs(self, _=None):
        search = self.e_search.get().strip()
        cat_f  = self.cb_filter_cat.get()
        if cat_f in ("", T("all_cats")):
            cat_f = ""
        else:
            cat_f = _propcat_reverse(cat_f)
        self._refresh_prop_defs(search, cat_f)

    def _clear_filter(self):
        self.e_search.delete(0,tk.END)
        self.cb_filter_cat.set(T("all_cats"))
        self._refresh_prop_defs()

    def _add_prop_def(self):
        name = self.e_pname.get().strip()
        cat_display = self.cb_pcat.get().strip()
        dbkey = self.e_pdbkey.get().strip()
        if not name: messagebox.showwarning(T("hint"),T("warn_enter_disp_name")); return
        if not cat_display:  messagebox.showwarning(T("hint"),T("warn_enter_cat")); return
        if not dbkey: messagebox.showwarning(T("hint"),T("warn_enter_dbkey")); return
        if not dbkey.replace('_','').replace('-','').isalnum():
            messagebox.showwarning(T("hint"),T("warn_dbkey_format")); return
        cat = _propcat_reverse(cat_display)
        all_defs = self.dm.get_all_prop_defs()
        for items in all_defs.values():
            if any(n == name for n,u,m in items):
                messagebox.showwarning(T("hint"), T("warn_name_exists", name)); return
        existing_keys = [p.get('db_key','') for p in self.dm.custom_props if p.get('db_key')]
        if dbkey in existing_keys:
            messagebox.showwarning(T("hint"), T("warn_dbkey_exists", dbkey)); return
        new_p = {"category": cat, "name": name, "db_key": dbkey,
                 "unit": self.e_punit.get().strip(), "method": self.e_pmethod.get().strip()}
        self.dm.custom_props.append(new_p)
        self.dm.save_custom_props()
        self._refresh_prop_defs(); self._build_prop_form()
        if self._sel_recipe: self._load_prop_values(self._sel_recipe)
        for e in [self.e_pname, self.e_pdbkey, self.e_punit, self.e_pmethod]: e.delete(0,tk.END)
        messagebox.showinfo(T("add_ok"), T("prop_added", name, dbkey, T_propcat(cat)))

    def _del_prop_def(self):
        sel = self.def_tree.selection()
        if not sel: messagebox.showwarning(T("hint"),T("warn_select_item")); return
        vals = self.def_tree.item(sel[0])['values']
        tags = self.def_tree.item(sel[0])['tags']
        display_name = vals[2]; name = str(vals[6])  # _iname: internal zh_TW name
        is_builtin = 'builtin' in tags
        msg = T("confirm_del_builtin", display_name) if is_builtin else T("confirm_del_user", display_name)
        if not messagebox.askyesno(T("confirm_delete_title"), msg): return
        if is_builtin:
            # 以 _deleted 標記記錄至 user_props，讓 get_all_prop_defs 過濾掉
            if not any(p.get('category') == '_deleted' and p.get('name') == name for p in self.dm.custom_props):
                self.dm.custom_props.append({"category": "_deleted", "name": name, "unit": "", "method": ""})
        else:
            self.dm.custom_props = [p for p in self.dm.custom_props if p['name'] != name or p.get('category') == '_deleted']
        self.dm.save_custom_props()
        self._refresh_prop_defs(); self._build_prop_form()
        if self._sel_recipe: self._load_prop_values(self._sel_recipe)
        messagebox.showinfo(T("ok"), T("deleted", display_name))

    def _restore_builtins(self):
        deleted = [p['name'] for p in self.dm.custom_props if p.get('category') == '_deleted']
        if not deleted:
            messagebox.showinfo(T("hint"),T("no_deleted_builtins")); return
        display_list = "\n".join(f"  • {T_prop(n)}" for n in deleted)
        if not messagebox.askyesno(T("confirm_restore"), T("restore_msg", len(deleted))+"\n" + display_list): return
        self.dm.custom_props = [p for p in self.dm.custom_props if p.get('category') != '_deleted']
        self.dm.save_custom_props()
        self._refresh_prop_defs(); self._build_prop_form()
        if self._sel_recipe: self._load_prop_values(self._sel_recipe)
        messagebox.showinfo(T("ok"), T("restored_n", len(deleted)))

    def _copy_def_to_input(self):
        sel = self.def_tree.selection()
        if not sel: return
        vals = self.def_tree.item(sel[0])['values']
        # vals: (src, cat, name, dbkey, unit, method)
        self.e_pname.delete(0,tk.END);   self.e_pname.insert(0,  str(vals[2]))
        self.e_pdbkey.delete(0,tk.END)
        dbk = str(vals[3])
        if dbk != T("eq_display_name"): self.e_pdbkey.insert(0, dbk)
        self.e_punit.delete(0,tk.END);   self.e_punit.insert(0,  str(vals[4]))
        self.e_pmethod.delete(0,tk.END); self.e_pmethod.insert(0, str(vals[5]))
        self.cb_pcat.set(str(vals[1]))

    # ── 自定義分類管理 ──────────────────────────────────────────────
    def _add_cat_dialog(self):
        top = tk.Toplevel(self.frame.winfo_toplevel())
        top.title(T("dlg_add_cat")); top.geometry("460x240"); top.resizable(False, False)
        top.grab_set()

        r = 0
        ttk.Label(top, text=T("lbl_cat_key")).grid(row=r, column=0, padx=10, pady=(12,3), sticky='e')
        e_key = ttk.Entry(top, width=28); e_key.grid(row=r, column=1, padx=10, pady=(12,3), sticky='w')
        r += 1
        ttk.Label(top, text=T("lbl_cat_key_hint"), foreground="#888",
                  font=("Arial",8)).grid(row=r, column=0, columnspan=2, padx=10, sticky='w')
        r += 1

        entries_lang = {}
        lang_labels = {"zh_TW":"lbl_lang_zh_tw","zh_CN":"lbl_lang_zh_cn","en":"lbl_lang_en","ja":"lbl_lang_ja"}
        for lang_code, lbl_key in lang_labels.items():
            lbl_txt = T(lbl_key)
            if lang_code == _CURRENT_LANG: lbl_txt = "★ " + lbl_txt
            ttk.Label(top, text=lbl_txt).grid(row=r, column=0, padx=10, pady=3, sticky='e')
            e = ttk.Entry(top, width=28); e.grid(row=r, column=1, padx=10, pady=3, sticky='w')
            entries_lang[lang_code] = e; r += 1

        def do_add():
            key = e_key.get().strip()
            cur_name = entries_lang[_CURRENT_LANG].get().strip()
            if not key or not cur_name:
                messagebox.showwarning(T("hint"), T("warn_cat_key_empty"), parent=top); return
            all_keys = set(PREDEFINED_PROPS.keys()) | {cc['key'] for cc in _custom_cats}
            if key in all_keys:
                messagebox.showwarning(T("hint"), T("warn_cat_key_exists", key), parent=top); return
            new_cat = {"key": key,
                       "zh_TW": entries_lang["zh_TW"].get().strip() or cur_name,
                       "zh_CN": entries_lang["zh_CN"].get().strip() or cur_name,
                       "en":    entries_lang["en"].get().strip() or cur_name,
                       "ja":    entries_lang["ja"].get().strip() or cur_name}
            _custom_cats.append(new_cat)
            _save_custom_cats()
            top.destroy()
            self._refresh_prop_defs(); self._build_prop_form()
            messagebox.showinfo(T("ok"), T("cat_added", T_propcat(key)))

        ttk.Button(top, text=T("btn_add_cat"), command=do_add).grid(
            row=r, column=0, columnspan=2, pady=10)

    def _del_cat_dialog(self):
        if not _custom_cats:
            messagebox.showinfo(T("hint"), T("no_custom_cat_del")); return
        top = tk.Toplevel(self.frame.winfo_toplevel())
        top.title(T("dlg_del_cat")); top.geometry("380x300"); top.resizable(False, False)
        top.grab_set()

        ttk.Label(top, text=T("dlg_del_cat"), font=("Arial",10,"bold")).pack(pady=(10,5))
        lb = tk.Listbox(top, height=8, font=("Arial",10))
        lb.pack(fill='both', expand=True, padx=15, pady=5)
        for cc in _custom_cats:
            lb.insert(tk.END, f"{cc['key']}  —  {T_propcat(cc['key'])}")

        def do_del():
            sel = lb.curselection()
            if not sel: return
            idx = sel[0]
            cc = _custom_cats[idx]
            key = cc['key']
            disp = T_propcat(key)
            if not messagebox.askyesno(T("confirm_delete_title"),
                                       T("confirm_del_cat", disp), parent=top): return
            # Move any custom props in this category to 7.自定義
            for p in self.dm.custom_props:
                if p.get("category") == key:
                    p["category"] = "7.自定義"
            self.dm.save_custom_props()
            _custom_cats.pop(idx)
            _save_custom_cats()
            top.destroy()
            self._refresh_prop_defs(); self._build_prop_form()
            if self._sel_recipe: self._load_prop_values(self._sel_recipe)
            messagebox.showinfo(T("ok"), T("cat_deleted", disp))

        ttk.Button(top, text=T("btn_del_cat"), command=do_del).pack(pady=10)

    def _refresh_custom(self):
        self._refresh_prop_defs()

    # ── 配方清單 ──────────────────────────────────────────────────────
    def refresh(self):
        self.recipe_tree.delete(*self.recipe_tree.get_children())
        for row in self.dm._read_recipe_rows():
            self.recipe_tree.insert("","end", values=(
                row.get("配方名稱",""), row.get("批次號",""),
                row.get("建立日期",""), row.get("總質量_g","")))

    def _on_sel(self, _=None):
        sel = self.recipe_tree.selection()
        if not sel: return
        self._sel_recipe = self.recipe_tree.item(sel[0])['values'][0]
        self.lbl_sel_recipe.config(text=T("current_recipe", self._sel_recipe), foreground="#0066cc")
        self._show_detail(); self._load_prop_values(self._sel_recipe)

    def _deselect_recipe(self):
        self._sel_recipe = None
        self.recipe_tree.selection_remove(*self.recipe_tree.selection())
        self.lbl_sel_recipe.config(text=T("no_recipe_selected"), foreground="#999")
        self.detail_txt.config(state='normal'); self.detail_txt.delete("1.0",tk.END); self.detail_txt.config(state='disabled')
        self._clear_props()

    def _show_detail(self):
        row = self.dm.get_recipe_row(self._sel_recipe)
        self.detail_txt.config(state='normal'); self.detail_txt.delete("1.0",tk.END)
        if not row: self.detail_txt.config(state='disabled'); return

        self.detail_txt.insert(tk.END, T("detail_recipe_fmt", row.get("配方名稱",""))+"\n")
        batch = row.get('批次號','')
        if batch: self.detail_txt.insert(tk.END, T("detail_batch_fmt", batch)+"\n")
        self.detail_txt.insert(tk.END, T("detail_date_mode", row.get("建立日期",""), row.get("計算模式",""))+"\n")
        self.detail_txt.insert(tk.END, T("detail_total")+T("detail_total_cl", row.get('總質量_g',''), row.get('總氯含量_ppm',''))+"\n\n")

        all_sc = get_all_slot_counts(); all_cn = get_all_cat_cn()
        for cat, cn in all_cn.items():
            cat_disp = get_mat_cat_display(cat)
            n = all_sc.get(cat, 3)
            lines = []
            for i in range(1, n+1):
                nm = row.get(f"{cn}{i}_名稱","")
                if not nm: continue
                mass = row.get(f"{cn}{i}_質量_g",""); pct = row.get(f"{cn}{i}_佔比%","")
                extra = ""
                cmc = _get_custom_mat_cat(cat)
                if cat == "resins" or (cmc and cmc.get('has_eew')): extra = f"  EEW={row.get(f'{cn}{i}_EEW','')}"
                elif cat == "hardeners": extra = T("detail_eq", row.get(f'{cn}{i}_當量',''), row.get(f'{cn}{i}_子類型',''))
                lines.append(f"  {cat_disp}{i}: {nm}  {mass}g ({pct}%){extra}")
            if lines:
                self.detail_txt.insert(tk.END, f"── {cat_disp} ──\n")
                self.detail_txt.insert(tk.END, "\n".join(lines) + "\n")
        self.detail_txt.config(state='disabled')

    def _load_prop_values(self, recipe_name):
        row = self.dm.get_recipe_row(recipe_name)
        if not row: return
        for pname, ent in self._prop_entries.items():
            ent.delete(0, tk.END)
            csv_key = self.dm.get_prop_csv_key(pname)
            val = row.get(csv_key, "") or row.get(pname, "")
            if val: ent.insert(0, str(val))

    def _save_props(self):
        if not self._sel_recipe:
            messagebox.showwarning(T("hint"),T("warn_select_recipe_first")); return
        props = {}
        for pname, ent in self._prop_entries.items():
            v = ent.get().strip()
            if v:
                csv_key = self.dm.get_prop_csv_key(pname)
                props[csv_key] = v
        if not props:
            messagebox.showwarning(T("hint"),T("warn_no_props")); return
        ok = self.dm.update_recipe_props(self._sel_recipe, props)
        if ok:
            messagebox.showinfo(T("props_save_ok"), T("props_saved", len(props)))
        else:
            messagebox.showerror(T("error"),T("props_save_err"))

    def _clear_props(self):
        for ent in self._prop_entries.values(): ent.delete(0,tk.END)

    def _rename(self):
        sel = self.recipe_tree.selection()
        if not sel: messagebox.showwarning(T("hint"),T("warn_select_recipe")); return
        old = self.recipe_tree.item(sel[0])['values'][0]
        new = simpledialog.askstring(T("rename_title"),T("rename_prompt", old), parent=self.frame.winfo_toplevel())
        if not new or new == old: return
        if new in self.dm.get_recipe_names(): messagebox.showwarning(T("hint"),T("name_already_exists", new)); return
        self.dm.rename_recipe(old, new)
        if self._sel_recipe == old: self._sel_recipe = new
        self.refresh(); messagebox.showinfo(T("ok"),T("renamed_ok", new))

    def _delete(self):
        sel = self.recipe_tree.selection()
        if not sel: messagebox.showwarning(T("hint"),T("warn_select_recipe")); return
        name = self.recipe_tree.item(sel[0])['values'][0]
        if not messagebox.askyesno(T("confirm_delete_title2"),T("confirm_del_recipe", name)): return
        self.dm.delete_recipe(name)
        self._deselect_recipe()
        self.refresh()
        messagebox.showinfo(T("ok"),T("deleted_fmt", name))

    def _copy_row(self):
        if not self._sel_recipe:
            messagebox.showwarning(T("hint"),T("warn_select_recipe")); return
        row = self.dm.get_recipe_row(self._sel_recipe)
        if not row: return

        lines = []
        lines.append(T("copy_recipe_hdr_name")+f"\t{row.get('配方名稱','')}")
        lines.append(T("copy_recipe_hdr_batch")+f"\t{row.get('批次號','')}")
        lines.append("")
        lines.append(T("copy_recipe_hdr_mat"))
        all_sc = get_all_slot_counts(); all_cn = get_all_cat_cn()
        for cat, cn in all_cn.items():
            for i in range(1, all_sc.get(cat,3)+1):
                nm = row.get(f"{cn}{i}_名稱","")
                if not nm: continue
                mass = row.get(f"{cn}{i}_質量_g","")
                pct  = row.get(f"{cn}{i}_佔比%","")
                lines.append(f"{nm}\t{mass}\t{pct}")
        lines.append("")

        prop_lines = []
        all_defs = self.dm.get_prop_defs_flat()
        for cat, items in all_defs.items():
            for pname, unit, method in items:
                csv_key = self.dm.get_prop_csv_key(pname)
                val = row.get(csv_key, "") or row.get(pname, "")
                if val:
                    prop_lines.append(f"{T_prop(pname)}\t{val}{unit}")
        if prop_lines:
            lines.append(T("copy_recipe_hdr_prop"))
            lines.extend(prop_lines)

        text = "\n".join(lines) + "\n"
        self.frame.clipboard_clear(); self.frame.clipboard_append(text); self.frame.update()
        messagebox.showinfo(T("copy_ok_title"), T("copy_recipe_ok", self._sel_recipe))


# ═══════════════════════════════════════════
#  EpoxyApp  主協調器
# ═══════════════════════════════════════════
class EpoxyApp:
    def __init__(self, root):
        self.root = root
        root.title(f"{T('app_title')} V4.1.1")
        root.geometry("1400x960")
        root.minsize(1100, 700)

        font_std  = ("Microsoft JhengHei", 10)
        font_bold = ("Microsoft JhengHei", 10, "bold")
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=font_bold)
        try: style.configure("Accent.TButton", font=font_bold, foreground="white", background="#0078d4")
        except: pass

        self.dm = DataManager()

        # 語言選擇列
        lang_f = ttk.Frame(root); lang_f.pack(fill='x', padx=10, pady=(5,0))
        ttk.Label(lang_f, text="Language:", font=("Arial",9)).pack(side='right', padx=(5,2))
        self.lang_cb = ttk.Combobox(lang_f, values=[LANG_DISPLAY[l] for l in SUPPORTED_LANGS],
                                     state="readonly", width=12)
        self.lang_cb.set(LANG_DISPLAY.get(_CURRENT_LANG, "正體中文"))
        self.lang_cb.pack(side='right')
        self.lang_cb.bind("<<ComboboxSelected>>", self._on_lang_change)

        self.nb = ttk.Notebook(root); self.nb.pack(pady=5, expand=True, fill='both')
        self.calc_tab   = CalcTab(self.nb, self.dm, font_std, font_bold)
        self.db_tab     = DatabaseTab(self.nb, self.dm, font_std, font_bold, rebuild_cb=self._rebuild_ui)
        self.recipe_tab = RecipeTab(self.nb, self.dm, font_std, font_bold)

        self.nb.bind("<<NotebookTabChanged>>", self._on_tab)

    def _on_lang_change(self, _=None):
        disp = self.lang_cb.get()
        rev = {v:k for k,v in LANG_DISPLAY.items()}
        lang = rev.get(disp, "zh_TW")
        _save_lang(lang)
        # Reload material column config with new display names
        self.dm.mat_columns = self.dm._load_mat_col_config()
        # Rebuild all tabs with new language
        self._rebuild_ui()

    def _rebuild_ui(self):
        self.root.title(f"{T('app_title')} V4.1.1")
        # Destroy existing tab frames completely
        for child in list(self.nb.winfo_children()):
            child.destroy()
        # Recreate
        font_std  = ("Microsoft JhengHei", 10)
        font_bold = ("Microsoft JhengHei", 10, "bold")
        self.calc_tab   = CalcTab(self.nb, self.dm, font_std, font_bold)
        self.db_tab     = DatabaseTab(self.nb, self.dm, font_std, font_bold, rebuild_cb=self._rebuild_ui)
        self.recipe_tab = RecipeTab(self.nb, self.dm, font_std, font_bold)

    def _on_tab(self, _):
        txt = self.nb.tab(self.nb.select(), "text")
        if txt == T("tab_recipe_mgr"): self.recipe_tab.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    app  = EpoxyApp(root)
    root.mainloop()
