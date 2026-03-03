import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv, os, datetime, json

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
_BUILTIN_MAT_COLS = [
    {"db_key":"Name",       "display":"名稱",   "unit":"",          "data_key":"_name",     "visible":True, "builtin":True, "locked":True},
    {"db_key":"Type",       "display":"類型",   "unit":"",          "data_key":"type",      "visible":True, "builtin":True},
    {"db_key":"Appearance", "display":"外觀特性","unit":"",          "data_key":"appearance","visible":True, "builtin":True},
    {"db_key":"Viscosity_cP25","display":"粘度","unit":"cP(25℃)",   "data_key":"viscosity", "visible":True, "builtin":True},
    {"db_key":"Dk",         "display":"介電常數","unit":"",          "data_key":"dk",        "visible":True, "builtin":True},
    {"db_key":"Surface_Energy","display":"表面能","unit":"mN/m(25℃)","data_key":"surface_energy","visible":True,"builtin":True},
    {"db_key":"Molecular_Structure","display":"分子結構","unit":"",  "data_key":"structure", "visible":True, "builtin":True},
    {"db_key":"EEW_AHEW",  "display":"EEW/當量","unit":"",          "data_key":"_eq",       "visible":True, "builtin":True, "special":True},
    {"db_key":"Cl_ppm",    "display":"氯",      "unit":"ppm",       "data_key":"cl",        "visible":True, "builtin":True},
    {"db_key":"Source",     "display":"來源",    "unit":"",          "data_key":"source",    "visible":False,"builtin":True},
    {"db_key":"Description","display":"備註",    "unit":"",          "data_key":"desc",      "visible":False,"builtin":True},
]

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
    for cat, n in SLOT_COUNTS.items():
        cn = CAT_CN[cat]
        for i in range(1, n + 1):
            for field in SLOT_FIELDS[cat]:
                cols.append(f"{cn}{i}_{field}")
    return cols

FIXED_COLUMNS = _build_fixed_columns()


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
        cols = [dict(c) for c in _BUILTIN_MAT_COLS]
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
        data = {k: {} for k in SLOT_COUNTS}
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
        except Exception as e: messagebox.showerror("錯誤", f"物料庫儲存失敗: {e}")
        except Exception as e: messagebox.showerror("錯誤", f"物料庫儲存失敗: {e}")

    def get_active_eq(self, info):
        st = info.get('h_subtype','')
        return info.get({'聚酰胺':'polyamide_eq','酸酐':'anhydride_eq',
                         '巯基':'mercapto_eq','羥基':'hydroxyl_eq'}.get(st,'ahew'), 1) or 1

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
                if k not in FIXED_COLUMNS and k not in seen_extra:
                    seen_extra.append(k)
        all_cols = FIXED_COLUMNS + seen_extra
        try:
            with open(RECIPE_DB_FILE, 'w', encoding='utf-8-sig', newline='') as f:
                w = csv.DictWriter(f, fieldnames=all_cols, extrasaction='ignore')
                w.writeheader()
                for row in rows:
                    w.writerow({c: row.get(c, '') for c in all_cols})
        except Exception as e: messagebox.showerror("錯誤", f"配方庫寫入失敗: {e}")

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
            return [h for h in headers if h not in FIXED_COLUMNS]
        except: return []

    def build_recipe_row(self, recipe_name, batch_no, calc_mode, materials_list, total_mass, total_cl):
        row = {c: "" for c in FIXED_COLUMNS}
        row["配方名稱"]   = recipe_name
        row["批次號"]     = batch_no
        row["建立日期"]   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row["計算模式"]   = calc_mode
        row["總質量_g"]   = f"{total_mass:.4f}"
        row["總氯含量_ppm"] = f"{total_cl:.2f}"

        counters = {c: 0 for c in SLOT_COUNTS}
        for m in materials_list:
            cat = m.get("orig_cat")
            if cat not in counters: continue
            counters[cat] += 1
            idx = counters[cat]
            if idx > SLOT_COUNTS[cat]: continue
            cn   = CAT_CN[cat]
            name = m["name"]
            info = self.materials[cat].get(name, {})
            mass = m.get("rounded_mass", 0)
            pct  = m.get("pct", 0)

            row[f"{cn}{idx}_名稱"]   = name
            row[f"{cn}{idx}_質量_g"] = str(mass)
            row[f"{cn}{idx}_佔比%"]  = f"{pct:.4f}"
            row[f"{cn}{idx}_氯_ppm"] = str(info.get("cl", ""))

            if cat == "resins":
                row[f"{cn}{idx}_EEW"]    = str(info.get("eew",""))
                row[f"{cn}{idx}_類型"]   = info.get("type","")
                row[f"{cn}{idx}_分子結構"] = info.get("structure","")

            elif cat == "hardeners":
                row[f"{cn}{idx}_當量"]   = str(self.get_active_eq(info))
                row[f"{cn}{idx}_子類型"] = info.get("h_subtype","")
                row[f"{cn}{idx}_校正%"]  = str(m.get("corr_pct",""))
                row[f"{cn}{idx}_分子結構"] = info.get("structure","")

            else:  # additives / fillers / catalysts
                row[f"{cn}{idx}_類型"]   = info.get("type","")

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
        except Exception as e: messagebox.showerror("錯誤", f"使用者物性定義儲存失敗: {e}")

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
        for p in self.custom_props:
            c = p.get("category") or "7.自定義"
            if c not in cats and c != '_deleted': cats.append(c)
        return cats


# ═══════════════════════════════════════════
#  CalcTab  配方設計與計算
# ═══════════════════════════════════════════
class CalcTab:
    MODE_MAP = {
        "stoich (按當量配比)":          "stoich",
        "weight (按樹脂總量百分比)":    "weight",
        "target_100 (目標總重 100g)":   "target_100",
    }

    def __init__(self, nb, dm: DataManager, font_std, font_bold):
        self.dm = dm; self.fs = font_std; self.fb = font_bold
        self.frame = ttk.Frame(nb)
        nb.add(self.frame, text="🗡 配方設計與計算")
        self.calc_rows = {c: [] for c in SLOT_COUNTS}
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
        rf = ttk.LabelFrame(self.sf, text="1. 樹脂", padding=5); rf.pack(fill='x', pady=5, padx=5)
        self.resin_box = ttk.Frame(rf); self.resin_box.pack(fill='both', expand=True)
        ttk.Button(rf, text="+ 添加樹脂", command=lambda: self.add_row('resins', self.resin_box)).pack(anchor='w')

        # 固化劑
        hf = ttk.LabelFrame(self.sf, text="2. 固化劑", padding=5); hf.pack(fill='x', pady=5, padx=5)
        mf = ttk.Frame(hf); mf.pack(fill='x', pady=2)
        ttk.Label(mf, text="計算模式:").pack(side='left')
        self.calc_mode = tk.StringVar(value="stoich (按當量配比)")
        mcb = ttk.Combobox(mf, textvariable=self.calc_mode, state="readonly", width=28,
                           values=list(self.MODE_MAP.keys()))
        mcb.bind("<<ComboboxSelected>>", self._update_ui); mcb.pack(side='left', padx=5)
        self.h_header = ttk.Frame(hf); self.h_header.pack(fill='x')
        self.hardener_box = ttk.Frame(hf); self.hardener_box.pack(fill='both', expand=True)
        ttk.Button(hf, text="+ 添加固化劑", command=lambda: self.add_row('hardeners', self.hardener_box)).pack(anchor='w')

        # 助劑/填料/催化劑
        for cat, title in [('additives','3. 助劑'),('fillers','4. 填料'),('catalysts','5. 催化劑')]:
            f = ttk.LabelFrame(self.sf, text=title, padding=5); f.pack(fill='x', pady=5, padx=5)
            box = ttk.Frame(f); box.pack(fill='both', expand=True)
            setattr(self, f"{cat}_box", box)
            ttk.Button(f, text=f"+ 添加{title[3:]}", command=lambda c=cat, b=box: self.add_row(c, b)).pack(anchor='w')

        # 右側結果
        ra = ttk.Frame(pw, padding=10); pw.add(ra, weight=2)
        cf = ttk.LabelFrame(ra, text="計算設定", padding=5); cf.pack(fill='x', pady=5)

        row1 = ttk.Frame(cf); row1.pack(fill='x', pady=2)
        ttk.Label(row1, text="質量取整:").pack(side='left', padx=5)
        self.round_opt = tk.StringVar(value="2位小數")
        ttk.Combobox(row1, textvariable=self.round_opt,
                     values=["不取整","整數","1位小數","2位小數"], width=10, state="readonly").pack(side='left')

        self.t100_frame = ttk.LabelFrame(cf, text="100g 配平選項", padding=5)
        self.inc_add = tk.BooleanVar(value=True); self.inc_fil = tk.BooleanVar(value=True); self.inc_cat = tk.BooleanVar(value=True)
        for var, lbl in [(self.inc_add,"助劑"),(self.inc_fil,"填料"),(self.inc_cat,"催化劑")]:
            ttk.Checkbutton(self.t100_frame, text=f"{lbl}參與100g配平", variable=var).pack(anchor='w')

        ttk.Button(cf, text="▶ 開始計算並生成報表", command=self.calculate).pack(fill='x', pady=5)

        tf = ttk.Frame(ra); tf.pack(fill='both', expand=True)
        cols = [("name","物料名稱",200),("mass","質量 (g)",100),("percent","佔比 (%)",100),("cl","氯 (ppm)",110)]
        self.tree = ttk.Treeview(tf, columns=[c[0] for c in cols], show='headings', height=20)
        for cid, hdr, w in cols: self.tree.heading(cid, text=hdr); self.tree.column(cid, width=w, anchor='center')
        vsbt = ttk.Scrollbar(tf, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsbt.set)
        self.tree.pack(side='left', fill='both', expand=True); vsbt.pack(side='right', fill='y')
        self.tree.tag_configure('total', font=self.fb, background="#e1f5fe")
        self.tree.bind("<ButtonPress-1>",   self._ds); self.tree.bind("<B1-Motion>", self._dm)
        self.tree.bind("<ButtonRelease-1>", self._dr)

        bf = ttk.Frame(ra); bf.pack(fill='x', pady=10)
        ttk.Button(bf, text="📋 複製到 Excel",  command=self._copy).pack(side='left', fill='x', expand=True, padx=(0,5))
        ttk.Button(bf, text="💾 儲存配方至數據庫", command=self._save).pack(side='left', fill='x', expand=True, padx=(5,0))

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
        mode = self.MODE_MAP.get(self.calc_mode.get(), "stoich")
        self._sync_resin_modes()
        self._sync_hardener_header()
        if mode == "target_100": self.t100_frame.pack(fill='x', pady=5)
        else: self.t100_frame.pack_forget()

    def _sync_resin_modes(self, _=None):
        mode = self.MODE_MAP.get(self.calc_mode.get(), "stoich")
        allow = (mode == "target_100")
        avail = ["固定質量"] + (["比例(待算)"] if allow else [])
        for rd in self.calc_rows['resins']:
            if rd.get('cb_mode'):
                rd['cb_mode']['values'] = avail
                if not allow and rd['mode_var'].get() == "比例(待算)":
                    rd['mode_var'].set("固定質量")
                    if rd.get('lbl_unit'): rd['lbl_unit'].config(text="g")

    def _sync_hardener_header(self):
        n = len(self.calc_rows['hardeners'])
        for w in self.h_header.winfo_children(): w.destroy()
        ttk.Label(self.h_header, text="名稱/類型", width=25).pack(side='left')
        if n > 1: ttk.Label(self.h_header, text="當量比例/佔比", width=12).pack(side='left', padx=5)
        ttk.Label(self.h_header, text="校正(C)%", width=10).pack(side='left', padx=5)
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
        ToolTip(btn_clear, "清空並重選物料")
        rd = {"frame": row, "cb": cb}

        if cat == 'resins':
            mv = tk.StringVar(value="固定質量")
            cbm = ttk.Combobox(row, textvariable=mv, width=8, state="readonly"); cbm.pack(side='left', padx=5)
            ent = ttk.Entry(row, width=8); ent.pack(side='left', padx=5)
            lbl = ttk.Label(row, text="g", font=("Arial",8)); lbl.pack(side='left')
            cbm.bind("<<ComboboxSelected>>", lambda e: lbl.config(text="g" if mv.get()=="固定質量" else "R-parts"))
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
            self.dm.materials[cat].get(cb.get().split("  [")[0], {}).get('desc','').strip() or "無備註")))
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
            mode = self.MODE_MAP.get(self.calc_mode.get(), "stoich")
            mats = []; fixed_r_mass = 0.0; fixed_r_eq = 0.0
            ratio_r = []; total_r_parts = 0.0
            inc = {'additives': self.inc_add.get(), 'fillers': self.inc_fil.get(), 'catalysts': self.inc_cat.get()}

            for rd in self.calc_rows['resins']:
                nm = rd['cb'].get().split("  [")[0]; vs = rd['entry'].get()
                if not nm or not vs: continue
                v = float(vs); info = self.dm.materials['resins'].get(nm,{})
                eew = info.get('eew',0)
                if rd['mode_var'].get() == "固定質量":
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
                    if inc[cat] and mode == "target_100": others += mass
                    info = self.dm.materials[cat].get(nm,{})
                    mats.append({"orig_cat":cat,"name":nm,"mass":mass,"cl_ppm":info.get('cl',0),"type":cat.capitalize()})

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
                        if m['type'] in ['Additives','Fillers','Catalysts'] and inc.get(m['orig_cat'],False): m['mass'] *= sc
                        elif m['type'] in ['Resin(Fixed)','Hardener']: m['mass'] *= sc
            else:
                if mode != "target_100": raise ValueError("非 '目標100g' 模式不允許使用樹脂比例(待算)")
                A = total_r_parts; B = C = 0.0
                veq = sum(r['parts']/r['eew'] for r in ratio_r if r['eew']>0)
                for h in h_cfgs:
                    if total_hr > 0:
                        sh = h['input_val']/total_hr
                        B += veq*sh*h['eq']*h['corr']; C += fixed_r_eq*sh*h['eq']*h['corr']
                cf = fixed_r_mass + others + C; vc = A + B
                if vc == 0: raise ValueError("無法計算：變動部分係數為0")
                u = (100.0-cf)/vc
                if u < 0: raise ValueError("無法配平至100g：固定質量已超過目標")
                tfe = fixed_r_eq + u*veq
                for r in ratio_r: mats.append({"orig_cat":"resins","name":r['name'],"mass":u*r['parts'],"cl_ppm":r['cl_ppm'],"type":"Resin(Calc)"})
                for h in h_cfgs:
                    hm = (tfe*(h['input_val']/total_hr)*h['eq']*h['corr']) if total_hr>0 else 0
                    mats.append({"orig_cat":"hardeners","name":h['name'],"mass":hm,"cl_ppm":h['cl_ppm'],
                                 "type":"Hardener","corr_pct":h['corr_pct']})

            sp = {'Additives':1,'Resin(Fixed)':2,'Resin(Ratio)':2,'Resin(Calc)':2,'Hardener':3,'Fillers':4,'Catalysts':5}
            mats.sort(key=lambda m: sp.get(m['type'],99))

            opt = self.round_opt.get()
            pl = {"整數":0,"1位小數":1,"2位小數":2}.get(opt, None)
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
            self.tree.insert("","end", values=("總計",fmt.format(rt),"100.00",f"{fcl:.0f}"), tags=('total',))

            # 快取供儲存使用
            self._last_mats = mats; self._last_total = rt; self._last_cl = fcl
            self._last_mode = self.MODE_MAP.get(self.calc_mode.get(),"stoich")
        except ValueError as ve: messagebox.showerror("輸入錯誤", str(ve))
        except Exception as e: messagebox.showerror("計算錯誤", str(e))

    # ── 匯出 / 儲存 ──────────────────────────────────────────────────
    def _copy(self):
        try:
            text = "物料名稱\t質量 (g)\t佔比 (%)\t氯含量 (ppm)\n"
            for item in self.tree.get_children():
                vals = self.tree.item(item,"values")
                if vals[0] == "---": continue
                text += "\t".join(map(str,vals)) + "\n"
            self.frame.clipboard_clear(); self.frame.clipboard_append(text); self.frame.update()
            messagebox.showinfo("複製成功","表格已複製，可在 Excel 中 Ctrl+V 貼上。")
        except Exception as e: messagebox.showerror("錯誤",f"複製失敗: {e}")

    def _save(self):
        if not hasattr(self,'_last_mats') or not self._last_mats:
            messagebox.showwarning("提示","請先執行計算"); return
        top = tk.Toplevel(self.frame.winfo_toplevel())
        top.title("儲存配方"); top.geometry("360x160"); top.resizable(False, False)
        top.grab_set()
        ttk.Label(top, text="配方名稱：").grid(row=0, column=0, padx=10, pady=(15,5), sticky='e')
        e_name = ttk.Entry(top, width=28); e_name.grid(row=0, column=1, padx=10, pady=(15,5))
        ttk.Label(top, text="批次號：").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        e_batch = ttk.Entry(top, width=28); e_batch.grid(row=1, column=1, padx=10, pady=5)
        def do_save():
            name = e_name.get().strip()
            if not name:
                messagebox.showwarning("提示","請輸入配方名稱", parent=top); return
            batch = e_batch.get().strip()
            row = self.dm.build_recipe_row(name, batch, self._last_mode, self._last_mats,
                                           self._last_total, self._last_cl)
            self.dm.save_new_recipe(row)
            top.destroy()
            messagebox.showinfo("成功", f"配方 '{name}' 已儲存至 {RECIPE_DB_FILE}")
        ttk.Button(top, text="💾 確認儲存", command=do_save).grid(row=2, column=0, columnspan=2, pady=15)


# ═══════════════════════════════════════════
#  DatabaseTab  物料數據庫管理
# ═══════════════════════════════════════════
class DatabaseTab:
    H_SUBTYPES = ["胺類","聚酰胺","酸酐","巯基","羥基"]

    def __init__(self, nb, dm: DataManager, font_std, font_bold):
        self.dm = dm; self.fs = font_std; self.fb = font_bold
        self.frame = ttk.Frame(nb)
        nb.add(self.frame, text="🕷 物料數據庫管理")
        self._edit_name = None
        self._build()

    def _build(self):
        f = ttk.Frame(self.frame, padding=10); f.pack(fill='both', expand=True)
        left = ttk.LabelFrame(f, text="數據編輯", padding=10); left.pack(side='left', fill='y', padx=5)

        sel_f = ttk.Frame(left); sel_f.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0,5))
        self.lbl_sel_mat = ttk.Label(sel_f, text="（未選中數據）",
                                      font=("Microsoft JhengHei", 9, "bold"), foreground="#999")
        self.lbl_sel_mat.pack(side='left')
        ttk.Button(sel_f, text="✖ 取消選中", command=self._deselect).pack(side='right')

        ttk.Label(left, text="類別:").grid(row=1, column=0, sticky='w')
        self.db_cat = tk.StringVar(value="樹脂")
        cb = ttk.Combobox(left, textvariable=self.db_cat, values=list(CAT_CN.values()), state="readonly", width=18)
        cb.grid(row=1, column=1, sticky='ew', pady=2); cb.bind("<<ComboboxSelected>>", self._refresh)

        # 固定編輯欄位
        for r, lbl, attr in [(2,"名稱:","e_name"),(3,"類型:","e_type"),
                              (4,"外觀特性:","e_appear"),(5,"粘度 cP(25℃):","e_visc"),
                              (6,"介電常數:","e_dk"),(7,"表面能 mN/m(25℃):","e_se"),
                              (8,"分子結構:","e_struct"),
                              (9,"來源:","e_src"),(10,"氯(ppm):","e_cl")]:
            ttk.Label(left, text=lbl).grid(row=r, column=0, sticky='w')
            e = ttk.Entry(left); e.grid(row=r, column=1, sticky='ew', pady=2); setattr(self, attr, e)

        self.row_val = ttk.Frame(left); self.row_val.grid(row=11, column=0, columnspan=2, pady=5, sticky='ew')
        self.lbl_eq = ttk.Label(self.row_val, text="EEW:", width=12); self.lbl_eq.pack(side='left')
        self.e_eq = ttk.Entry(self.row_val, font=self.fb); self.e_eq.pack(side='left', fill='x', expand=True)

        self.frm_h = ttk.LabelFrame(left, text="⚙️ 固化劑當量輔助計算", padding=5)
        ttk.Label(self.frm_h, text="子類型:").pack(anchor='w')
        self.cb_hst = ttk.Combobox(self.frm_h, values=self.H_SUBTYPES, state="readonly")
        self.cb_hst.pack(fill='x', pady=2); self.cb_hst.bind("<<ComboboxSelected>>", self._on_hst)
        self.sub_frms = {}; self._build_hst_frames()

        # 自定義欄位區域
        self._custom_row_start = 15
        self.frm_custom = ttk.LabelFrame(left, text="📝 自定義欄位", padding=5)
        self.frm_custom.grid(row=self._custom_row_start, column=0, columnspan=2, sticky='ew', pady=5)
        self._custom_entries = {}
        self._build_custom_entries()

        ttk.Label(left, text="備註:").grid(row=16, column=0, sticky='w', pady=(10,0))
        self.e_info = tk.Text(left, height=4, width=30); self.e_info.grid(row=17, column=0, columnspan=2, sticky='ew')

        btn_row = ttk.Frame(left); btn_row.grid(row=18, column=0, columnspan=2, pady=8, sticky='ew')
        ttk.Button(btn_row, text="💾 儲存",       command=self._save).pack(side='left', fill='x', expand=True, padx=(0,3))
        ttk.Button(btn_row, text="📄 另存為新物料", command=self._save_as_new).pack(side='left', fill='x', expand=True, padx=3)
        ttk.Button(btn_row, text="🗑 刪除選中",   command=self._delete).pack(side='left', fill='x', expand=True, padx=(3,0))

        # 右側列表
        right = ttk.Frame(f); right.pack(side='right', fill='both', expand=True)
        # 欄位管理按鈕列
        col_mgr_f = ttk.Frame(right); col_mgr_f.pack(fill='x', pady=(0,3))
        ttk.Button(col_mgr_f, text="⚙ 欄位管理", command=self._open_col_manager).pack(side='left', padx=5)
        ttk.Label(col_mgr_f, text="(新增/刪除/顯示隱藏欄位)", foreground="#777",
                  font=("Arial",8)).pack(side='left')
        # 樹形列表
        self._tree_frame = ttk.Frame(right)
        self._tree_frame.pack(fill='both', expand=True)
        self._build_tree()
        self._refresh()

    def _build_hst_frames(self):
        # 胺類
        f = ttk.Frame(self.frm_h)
        ttk.Label(f,text="胺值:").grid(row=0,column=0,sticky='w')
        self.e_amine_av = ttk.Entry(f,width=10); self.e_amine_av.grid(row=0,column=1)
        ttk.Button(f,text="計算(56100/胺值)",command=lambda:self._cs(self.e_amine_av,56100)).grid(row=1,column=0,columnspan=2,sticky='ew')
        self.sub_frms["胺類"] = f
        # 聚酰胺
        f = ttk.Frame(self.frm_h)
        ttk.Label(f,text="胺值:").grid(row=0,column=0,sticky='w'); self.e_poly_av=ttk.Entry(f,width=10); self.e_poly_av.grid(row=0,column=1)
        ttk.Label(f,text="係數f:").grid(row=1,column=0,sticky='w'); self.e_poly_f=ttk.Entry(f,width=10); self.e_poly_f.grid(row=1,column=1)
        ttk.Button(f,text="計算(56100/胺值×f)",command=self._calc_poly).grid(row=2,column=0,columnspan=2,sticky='ew')
        ttk.Separator(f,orient='horizontal').grid(row=3,column=0,columnspan=2,sticky='ew',pady=4)
        ttk.Label(f,text="分子量:").grid(row=4,column=0,sticky='w'); self.e_poly_mw=ttk.Entry(f,width=10); self.e_poly_mw.grid(row=4,column=1)
        ttk.Label(f,text="活性氫數:").grid(row=5,column=0,sticky='w'); self.e_poly_hn=ttk.Entry(f,width=10); self.e_poly_hn.grid(row=5,column=1)
        ttk.Button(f,text="計算(MW/活性氫數)",command=lambda:self._cd(self.e_poly_mw,self.e_poly_hn)).grid(row=6,column=0,columnspan=2,sticky='ew')
        self.sub_frms["聚酰胺"] = f
        # 酸酐
        f = ttk.Frame(self.frm_h)
        ttk.Label(f,text="酸值:").grid(row=0,column=0,sticky='w'); self.e_anh_ac=ttk.Entry(f,width=10); self.e_anh_ac.grid(row=0,column=1)
        ttk.Button(f,text="計算(56100/酸值)",command=lambda:self._cs(self.e_anh_ac,56100)).grid(row=1,column=0,columnspan=2,sticky='ew')
        ttk.Separator(f,orient='horizontal').grid(row=2,column=0,columnspan=2,sticky='ew',pady=4)
        ttk.Label(f,text="分子量:").grid(row=3,column=0,sticky='w'); self.e_anh_mw=ttk.Entry(f,width=10); self.e_anh_mw.grid(row=3,column=1)
        ttk.Label(f,text="酸酐基數:").grid(row=4,column=0,sticky='w'); self.e_anh_gp=ttk.Entry(f,width=10); self.e_anh_gp.grid(row=4,column=1)
        ttk.Button(f,text="計算(MW/酸酐基數)",command=lambda:self._cd(self.e_anh_mw,self.e_anh_gp)).grid(row=5,column=0,columnspan=2,sticky='ew')
        self.sub_frms["酸酐"] = f
        # 巯基
        f = ttk.Frame(self.frm_h)
        ttk.Label(f,text="分子量:").grid(row=0,column=0,sticky='w'); self.e_mer_mw=ttk.Entry(f,width=10); self.e_mer_mw.grid(row=0,column=1)
        ttk.Label(f,text="巯基數:").grid(row=1,column=0,sticky='w'); self.e_mer_gp=ttk.Entry(f,width=10); self.e_mer_gp.grid(row=1,column=1)
        ttk.Button(f,text="計算(MW/巯基數)",command=lambda:self._cd(self.e_mer_mw,self.e_mer_gp)).grid(row=2,column=0,columnspan=2,sticky='ew')
        self.sub_frms["巯基"] = f
        # 羥基
        f = ttk.Frame(self.frm_h)
        ttk.Label(f,text="羥值:").grid(row=0,column=0,sticky='w'); self.e_hyd_oh=ttk.Entry(f,width=10); self.e_hyd_oh.grid(row=0,column=1)
        ttk.Button(f,text="計算(56100/羥值)",command=lambda:self._cs(self.e_hyd_oh,56100)).grid(row=1,column=0,columnspan=2,sticky='ew')
        self.sub_frms["羥基"] = f

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
        st = self.cb_hst.get()
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
            ttk.Label(self.frm_custom, text="（無自定義欄位，可在「欄位管理」中新增）",
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
        dlg.title("欄位管理"); dlg.geometry("520x480"); dlg.resizable(True, True)
        dlg.transient(self.frame.winfo_toplevel()); dlg.grab_set()

        ttk.Label(dlg, text="勾選要在列表中顯示的欄位：", font=("Microsoft JhengHei",10,"bold")).pack(anchor='w', padx=10, pady=(10,5))

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
            tag = "內建" if col.get('builtin') else "自定義"
            txt = f"{display}   [DB: {col['db_key']}]   ({tag})"
            chk = ttk.Checkbutton(inner, text=txt, variable=var)
            if locked: chk.config(state='disabled')
            chk.grid(row=i, column=0, sticky='w', pady=1)
            chk_vars[col['db_key']] = var

        # 新增自定義欄位區
        add_f = ttk.LabelFrame(dlg, text="➕ 新增自定義欄位", padding=8)
        add_f.pack(fill='x', padx=10, pady=5)
        r1 = ttk.Frame(add_f); r1.pack(fill='x', pady=2)
        ttk.Label(r1, text="顯示名稱*:").pack(side='left')
        e_disp = ttk.Entry(r1, width=14); e_disp.pack(side='left', padx=(2,8))
        ttk.Label(r1, text="DB Key(英文)*:").pack(side='left')
        e_key = ttk.Entry(r1, width=14); e_key.pack(side='left', padx=(2,8))
        ttk.Label(r1, text="單位:").pack(side='left')
        e_unit = ttk.Entry(r1, width=10); e_unit.pack(side='left', padx=2)

        def do_add():
            dk = e_key.get().strip(); dd = e_disp.get().strip(); du = e_unit.get().strip()
            if not dk or not dd:
                messagebox.showwarning("提示","請填寫顯示名稱和DB Key", parent=dlg); return
            if not dk.isidentifier():
                messagebox.showwarning("提示","DB Key 只能包含英文字母、數字和底線，且不能以數字開頭", parent=dlg); return
            if not self.dm.add_mat_column(dk, dd, du):
                messagebox.showwarning("提示",f"DB Key「{dk}」已存在", parent=dlg); return
            var = tk.BooleanVar(value=True); chk_vars[dk] = var
            idx = len(self.dm.mat_columns) - 1
            txt = f"{dd}   [DB: {dk}]   (自定義)"
            if du: txt = f"{dd} ({du})   [DB: {dk}]   (自定義)"
            ttk.Checkbutton(inner, text=txt, variable=var).grid(row=idx, column=0, sticky='w', pady=1)
            for ew in [e_disp, e_key, e_unit]: ew.delete(0, tk.END)
            messagebox.showinfo("OK", f"已新增欄位「{dd}」", parent=dlg)

        def do_del():
            custom = self.dm.get_custom_mat_cols()
            if not custom:
                messagebox.showinfo("提示","目前無自定義欄位可刪除", parent=dlg); return
            names = [f"{c['display']} [{c['db_key']}]" for c in custom]
            del_dlg = tk.Toplevel(dlg); del_dlg.title("刪除自定義欄位"); del_dlg.geometry("300x200")
            del_dlg.transient(dlg); del_dlg.grab_set()
            lb = tk.Listbox(del_dlg, selectmode='browse')
            for n in names: lb.insert(tk.END, n)
            lb.pack(fill='both', expand=True, padx=10, pady=5)
            def confirm_del():
                sel = lb.curselection()
                if not sel: return
                col = custom[sel[0]]
                if messagebox.askyesno("確認", f"確定刪除欄位「{col['display']}」？", parent=del_dlg):
                    self.dm.remove_mat_column(col['db_key'])
                    del_dlg.destroy()
                    dlg.destroy()
                    self._open_col_manager()
            ttk.Button(del_dlg, text="🗑 刪除選中", command=confirm_del).pack(pady=5)

        r2 = ttk.Frame(add_f); r2.pack(fill='x', pady=2)
        ttk.Button(r2, text="✅ 新增欄位", command=do_add).pack(side='left', padx=(0,8))
        ttk.Button(r2, text="🗑 刪除自定義欄位", command=do_del).pack(side='left')

        def on_close():
            for col in self.dm.mat_columns:
                if col['db_key'] in chk_vars:
                    col['visible'] = chk_vars[col['db_key']].get()
            self.dm._save_mat_col_config()
            self._build_tree()
            self._build_custom_entries()
            self._refresh()
            dlg.destroy()

        ttk.Button(dlg, text="確定", command=on_close).pack(pady=8)
        dlg.protocol("WM_DELETE_WINDOW", on_close)

    def _cat_key(self): return {v:k for k,v in CAT_CN.items()}.get(self.db_cat.get(),"resins")

    def _clear(self):
        for attr in ['e_name','e_type','e_appear','e_visc','e_dk','e_se','e_struct','e_src','e_cl','e_eq',
                     'e_amine_av','e_poly_av','e_poly_mw','e_poly_hn',
                     'e_anh_ac','e_anh_mw','e_anh_gp','e_mer_mw','e_mer_gp','e_hyd_oh']:
            getattr(self,attr).delete(0,tk.END)
        if hasattr(self,'e_poly_f'): self.e_poly_f.delete(0,tk.END); self.e_poly_f.insert(0,"1.0")
        self.e_info.delete("1.0",tk.END); self.cb_hst.set(''); self._edit_name = None
        self.lbl_sel_mat.config(text="（未選中數據）", foreground="#999")
        for ent in self._custom_entries.values(): ent.delete(0,tk.END)

    def _refresh(self, _=None):
        self.tree.delete(*self.tree.get_children()); self._clear()
        cat = self._cat_key(); data = self.dm.materials.get(cat,{})
        if cat == "resins": self.row_val.grid(); self.lbl_eq.config(text="EEW直接輸入:"); self.frm_h.grid_remove()
        elif cat == "hardeners": self.row_val.grid(); self.lbl_eq.config(text="當量直接輸入:"); self.frm_h.grid(row=12,column=0,columnspan=2,pady=5,sticky='ew')
        else: self.row_val.grid_remove(); self.frm_h.grid_remove()
        vis_cols = self.dm.get_visible_mat_cols()
        for name, info in sorted(data.items()):
            vals = []
            for c in vis_cols:
                dk = c.get('data_key','')
                if dk == '_name': vals.append(name)
                elif dk == '_eq':
                    eq = f"{info.get('eew',0):.2f}" if cat=="resins" else (f"{self.dm.get_active_eq(info):.2f}" if cat=="hardeners" else "—")
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
        self.lbl_sel_mat.config(text=f"▶ 編輯中：{name}", foreground="#0066cc")
        self.e_name.insert(0,name); self.e_type.insert(0,info.get('type',''))
        self.e_appear.insert(0,info.get('appearance','')); self.e_visc.insert(0,info.get('viscosity',''))
        self.e_dk.insert(0,info.get('dk','')); self.e_se.insert(0,info.get('surface_energy',''))
        self.e_struct.insert(0,info.get('structure','')); self.e_src.insert(0,info.get('source',''))
        self.e_cl.insert(0,str(info.get('cl',0))); self.e_info.insert("1.0",info.get('desc',''))
        for dk, ent in self._custom_entries.items():
            ent.insert(0, str(info.get(dk, '')))
        if cat=="resins": self.e_eq.insert(0,str(info.get('eew',0)))
        elif cat=="hardeners":
            st=info.get('h_subtype',''); self.cb_hst.set(st); self._on_hst()
            self.e_eq.insert(0,f"{self.dm.get_active_eq(info):.2f}")
            if st=="胺類": self.e_amine_av.insert(0,str(info.get('amine_value','')))
            elif st=="聚酰胺":
                self.e_poly_av.insert(0,str(info.get('amine_value','')))
                self.e_poly_f.delete(0,tk.END); self.e_poly_f.insert(0,str(info.get('f_factor',1.0)))
                self.e_poly_mw.insert(0,str(info.get('mw',''))); self.e_poly_hn.insert(0,str(info.get('func_group_num','')))
            elif st=="酸酐":
                self.e_anh_ac.insert(0,str(info.get('acid_value',''))); self.e_anh_mw.insert(0,str(info.get('mw',''))); self.e_anh_gp.insert(0,str(info.get('func_group_num','')))
            elif st=="巯基": self.e_mer_mw.insert(0,str(info.get('mw',''))); self.e_mer_gp.insert(0,str(info.get('func_group_num','')))
            elif st=="羥基": self.e_hyd_oh.insert(0,str(info.get('hydroxyl_value','')))

    def _save(self):
        cat=self._cat_key(); name=self.e_name.get().strip()
        if not name: messagebox.showwarning("提示","請輸入物料名稱"); return
        if self._edit_name and self._edit_name!=name: del self.dm.materials[cat][self._edit_name]
        nd = self._collect_form_data(cat)
        if nd is None: return
        self.dm.materials[cat][name]=nd; self.dm.save_materials(); self._refresh()
        self._on_sel_by_name(name)
        messagebox.showinfo("OK","已成功儲存至物料庫")

    def _save_as_new(self):
        cat=self._cat_key(); name=self.e_name.get().strip()
        if not name: messagebox.showwarning("提示","請輸入物料名稱"); return
        if name in self.dm.materials.get(cat,{}):
            if not messagebox.askyesno("名稱已存在",
                f"物料「{name}」已存在於 {self.db_cat.get()} 類別中。\n\n"
                "確定要覆蓋嗎？如不要覆蓋，請先修改名稱欄。"):
                return
        nd = self._collect_form_data(cat)
        if nd is None: return
        self.dm.materials[cat][name]=nd; self.dm.save_materials(); self._refresh()
        self._on_sel_by_name(name)
        messagebox.showinfo("OK",f"已另存「{name}」至物料庫")

    def _collect_form_data(self, cat):
        try:
            eq_val = float(self.e_eq.get() or 0)
        except ValueError:
            messagebox.showwarning("提示","EEW/當量值格式錯誤"); return None
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
        if cat=="resins": nd["eew"]=eq_val
        elif cat=="hardeners":
            st=self.cb_hst.get(); nd["h_subtype"]=st
            nd["ahew"]=eq_val
            if st=="胺類": nd["amine_value"]=float(self.e_amine_av.get() or 0)
            elif st=="聚酰胺": nd["polyamide_eq"]=eq_val; nd["amine_value"]=float(self.e_poly_av.get() or 0); nd["f_factor"]=float(self.e_poly_f.get() or 1.0); nd["mw"]=float(self.e_poly_mw.get() or 0); nd["func_group_num"]=float(self.e_poly_hn.get() or 0)
            elif st=="酸酐": nd["anhydride_eq"]=eq_val; nd["acid_value"]=float(self.e_anh_ac.get() or 0); nd["mw"]=float(self.e_anh_mw.get() or 0); nd["func_group_num"]=float(self.e_anh_gp.get() or 0)
            elif st=="巯基": nd["mercapto_eq"]=eq_val; nd["mw"]=float(self.e_mer_mw.get() or 0); nd["func_group_num"]=float(self.e_mer_gp.get() or 0)
            elif st=="羥基": nd["hydroxyl_eq"]=eq_val; nd["hydroxyl_value"]=float(self.e_hyd_oh.get() or 0)
        return nd

    def _on_sel_by_name(self, name):
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == name:
                self.tree.selection_set(item)
                self.tree.see(item)
                self._edit_name = name
                self.lbl_sel_mat.config(text=f"▶ 編輯中：{name}", foreground="#0066cc")
                return

    def _deselect(self):
        self.tree.selection_remove(*self.tree.selection())
        self._clear()
        for frm in self.sub_frms.values(): frm.pack_forget()

    def _delete(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("提示","請選擇要刪除的物料"); return
        name=self.tree.item(sel[0])['values'][0]; cat=self._cat_key()
        if not messagebox.askyesno("確認",f"確定刪除「{name}」？"): return
        del self.dm.materials[cat][name]; self.dm.save_materials(); self._refresh()


# ═══════════════════════════════════════════
#  RecipeTab  配方管理 + 物性錄入
# ═══════════════════════════════════════════
class RecipeTab:
    def __init__(self, nb, dm: DataManager, font_std, font_bold):
        self.dm = dm; self.fs = font_std; self.fb = font_bold
        self.frame = ttk.Frame(nb)
        nb.add(self.frame, text="📂 配方管理")
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
        rf = ttk.LabelFrame(left, text="📋 配方清單", padding=5); rf.pack(fill='both', expand=True)
        rcols = [("name","配方名稱",150),("batch","批次號",90),("date","建立日期",140),("mass","總質量_g",80)]
        self.recipe_tree = ttk.Treeview(rf, columns=[c[0] for c in rcols], show='headings', height=9)
        for cid,hdr,w in rcols: self.recipe_tree.heading(cid,text=hdr); self.recipe_tree.column(cid,width=w,anchor='center')
        vsb_r = ttk.Scrollbar(rf, orient="vertical", command=self.recipe_tree.yview)
        self.recipe_tree.configure(yscrollcommand=vsb_r.set)
        self.recipe_tree.pack(side='left', fill='both', expand=True); vsb_r.pack(side='right', fill='y')
        self.recipe_tree.bind("<<TreeviewSelect>>", self._on_sel)

        # 配方操作按鈕
        bf = ttk.Frame(left); bf.pack(fill='x', pady=3)
        ttk.Button(bf, text="🔄 刷新",    command=self.refresh).pack(side='left', fill='x', expand=True, padx=(0,3))
        ttk.Button(bf, text="✏️ 重命名",  command=self._rename).pack(side='left', fill='x', expand=True, padx=3)
        ttk.Button(bf, text="🗑 刪除",    command=self._delete).pack(side='left', fill='x', expand=True, padx=(3,0))

        # 配方組成預覽
        pf = ttk.LabelFrame(left, text="📄 配方組成", padding=5); pf.pack(fill='both', expand=True, pady=5)
        self.detail_txt = tk.Text(pf, wrap='word', state='disabled', font=("Microsoft JhengHei",9), height=14)
        vsb_d = ttk.Scrollbar(pf, orient="vertical", command=self.detail_txt.yview)
        self.detail_txt.configure(yscrollcommand=vsb_d.set)
        self.detail_txt.pack(side='left', fill='both', expand=True); vsb_d.pack(side='right', fill='y')

        # 複製 / 匯出
        ef = ttk.Frame(left); ef.pack(fill='x', pady=3)
        ttk.Button(ef, text="📋 複製整行數據到Excel", command=self._copy_row).pack(fill='x')

        # ── 右側：物性編輯器 ───────────────────────────────────────────
        right = ttk.Frame(pw); pw.add(right, weight=2)
        paned_r = ttk.PanedWindow(right, orient=tk.VERTICAL); paned_r.pack(fill='both', expand=True)

        # 物性表單（上半）
        prop_outer = ttk.LabelFrame(right, text="🔬 物性數據錄入", padding=5)
        paned_r.add(prop_outer, weight=3)

        sel_row = ttk.Frame(prop_outer); sel_row.pack(fill='x', pady=(0,3))
        self.lbl_sel_recipe = ttk.Label(sel_row, text="（尚未選中配方）",
                                         font=("Microsoft JhengHei", 10, "bold"), foreground="#999")
        self.lbl_sel_recipe.pack(side='left', padx=5)
        ttk.Button(sel_row, text="✖ 取消選中", command=self._deselect_recipe).pack(side='left', padx=8)

        tool_row = ttk.Frame(prop_outer); tool_row.pack(fill='x', pady=(0,5))
        ttk.Button(tool_row, text="💾 儲存所有已填物性數據", command=self._save_props, style="Accent.TButton").pack(side='left')
        ttk.Button(tool_row, text="🗑 清空所有物性欄位",    command=self._clear_props).pack(side='left', padx=8)
        ttk.Button(tool_row, text="▲▼ 全部展開/折疊",      command=self._toggle_all).pack(side='left')
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
        custom_outer = ttk.LabelFrame(right, text="🔧 自定義物性欄位", padding=5)
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

            btn = ttk.Button(hdr_f, text=f"▼  {cat}")
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
                ttk.Label(container, text=pname, width=22, anchor='w',
                          font=("Microsoft JhengHei", 9)).grid(
                              row=r, column=c, sticky='w', padx=(5,2), pady=2)
                ent = ttk.Entry(container, width=13)
                ent.grid(row=r, column=c+1, sticky='ew', padx=2, pady=2)
                ToolTip(ent, f"單位: {unit}\n方法: {method}")
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

                grp_btn = ttk.Button(grp_hdr, text=f"  ▼ 【{grp_name}】")
                grp_btn.config(command=lambda c=grp_content, v=grp_vis, b=grp_btn: self._toggle_any(c, v, b))
                grp_btn.pack(side='left', padx=(18,0))
                self._prop_subgroup_frames[grp_name] = (grp_content, grp_btn, grp_vis)

                # 子群項目：2欄並排
                for j, (pname, unit, method) in enumerate(grp_items):
                    gr = j // 2; gc = (j % 2) * 3
                    ttk.Label(grp_content, text=pname, width=22, anchor='w',
                              font=("Microsoft JhengHei", 9)).grid(
                                  row=gr, column=gc, sticky='w', padx=(5,2), pady=2)
                    ent = ttk.Entry(grp_content, width=13)
                    ent.grid(row=gr, column=gc+1, sticky='ew', padx=2, pady=2)
                    ToolTip(ent, f"單位: {unit}\n方法: {method}")
                    ttk.Label(grp_content, text=unit, foreground="#888",
                              font=("Arial", 8)).grid(row=gr, column=gc+2, sticky='w', padx=(0,10))
                    self._prop_entries[pname] = ent
            else:
                reg_buf.append(item)
        flush()

    def _toggle_any(self, frame, visible_var, btn):
        if visible_var.get():
            frame.grid_remove(); visible_var.set(False)
            btn.config(text=btn.cget('text').replace("▼", "▶"))
        else:
            frame.grid(); visible_var.set(True)
            btn.config(text=btn.cget('text').replace("▶", "▼"))

    def _toggle_all(self):
        self._all_expanded = not self._all_expanded
        # 分類層
        for cat, (cf, btn, v) in self._prop_frames.items():
            if self._all_expanded:
                cf.grid(); v.set(True)
                if btn: btn.config(text=btn.cget('text').replace("▶","▼"))
            else:
                cf.grid_remove(); v.set(False)
                if btn: btn.config(text=btn.cget('text').replace("▼","▶"))
        # 子群層（同步展開/折疊）
        for grp, (cf, btn, v) in self._prop_subgroup_frames.items():
            if self._all_expanded:
                cf.grid(); v.set(True)
                if btn: btn.config(text=btn.cget('text').replace("▶","▼"))
            else:
                cf.grid_remove(); v.set(False)
                if btn: btn.config(text=btn.cget('text').replace("▼","▶"))

    # ── 物性定義管理面板 ──────────────────────────────────────────────
    def _build_custom_panel(self, parent):
        # 說明標籤
        info_f = ttk.Frame(parent); info_f.pack(fill='x', padx=5, pady=(0,3))
        ttk.Label(info_f, text="💡 所有項目均可刪除。內建項目（灰色）刪除後可點「恢復內建預設」還原。",
                  font=("Microsoft JhengHei",9), foreground="#555").pack(side='left')
        ttk.Button(info_f, text="🔄 恢復內建預設", command=self._restore_builtins).pack(side='right', padx=5)

        # ── 搜尋列 ─────────────────────────────────────────────────
        sf = ttk.Frame(parent); sf.pack(fill='x', padx=5, pady=2)
        ttk.Label(sf, text="🔍 搜尋:").pack(side='left')
        self.e_search = ttk.Entry(sf, width=20); self.e_search.pack(side='left', padx=5)
        self.e_search.bind('<KeyRelease>', self._filter_prop_defs)
        ttk.Label(sf, text="分類過濾:").pack(side='left', padx=(10,2))
        self.cb_filter_cat = ttk.Combobox(sf, state="readonly", width=18)
        self.cb_filter_cat.pack(side='left')
        self.cb_filter_cat.bind("<<ComboboxSelected>>", self._filter_prop_defs)
        ttk.Button(sf, text="清除過濾", command=self._clear_filter).pack(side='left', padx=6)
        self.lbl_count = ttk.Label(sf, text="", foreground="#777", font=("Arial",9))
        self.lbl_count.pack(side='right', padx=5)

        # ── 物性定義總覽表 ─────────────────────────────────────────
        tree_f = ttk.Frame(parent); tree_f.pack(fill='both', expand=True, padx=5)
        cols = [("src","來源",50),("cat","分類",100),("name","顯示名稱",170),("dbkey","DB Key",120),("unit","單位",65),("method","測試方法",220)]
        self.def_tree = ttk.Treeview(tree_f, columns=[c[0] for c in cols], show='headings', height=9,
                                     selectmode='browse')
        for cid,hdr,w in cols:
            self.def_tree.heading(cid, text=hdr)
            self.def_tree.column(cid, width=w, anchor='center' if cid in ('src','unit') else 'w')
        # 顏色標識：內建=淺灰，使用者追加=預設
        self.def_tree.tag_configure('builtin', foreground="#888888")
        self.def_tree.tag_configure('user',    foreground="#1a5f9e")
        vsb = ttk.Scrollbar(tree_f, orient="vertical", command=self.def_tree.yview)
        self.def_tree.configure(yscrollcommand=vsb.set)
        self.def_tree.pack(side='left', fill='both', expand=True); vsb.pack(side='right', fill='y')

        # ── 新增 / 刪除列 ─────────────────────────────────────────
        add_f = ttk.LabelFrame(parent, text="➕ 新增物性定義", padding=(8,4)); add_f.pack(fill='x', padx=5, pady=(5,0))

        row1 = ttk.Frame(add_f); row1.pack(fill='x', pady=2)
        ttk.Label(row1, text="顯示名稱*:", width=10).pack(side='left')
        self.e_pname  = ttk.Entry(row1, width=18); self.e_pname.pack(side='left', padx=(0,6))
        ttk.Label(row1, text="DB Key(英文)*:").pack(side='left')
        self.e_pdbkey = ttk.Entry(row1, width=16); self.e_pdbkey.pack(side='left', padx=(0,6))
        ttk.Label(row1, text="單位:").pack(side='left')
        self.e_punit  = ttk.Entry(row1, width=8); self.e_punit.pack(side='left', padx=(0,6))

        row1b = ttk.Frame(add_f); row1b.pack(fill='x', pady=2)
        ttk.Label(row1b, text="測試方法:", width=10).pack(side='left')
        self.e_pmethod = ttk.Entry(row1b, width=40); self.e_pmethod.pack(side='left', fill='x', expand=True)

        row2 = ttk.Frame(add_f); row2.pack(fill='x', pady=2)
        ttk.Label(row2, text="目標分類*:", width=10).pack(side='left')
        self.cb_pcat = ttk.Combobox(row2, width=22)
        self.cb_pcat.pack(side='left', padx=(0,8))
        ttk.Label(row2, text="（可選已有分類，或直接輸入新分類名）",
                  foreground="#888", font=("Arial",8)).pack(side='left')

        row3 = ttk.Frame(add_f); row3.pack(fill='x', pady=(3,4))
        ttk.Button(row3, text="✅ 新增",       command=self._add_prop_def).pack(side='left', padx=(0,8))
        ttk.Button(row3, text="🗑 刪除選中使用者項目", command=self._del_prop_def).pack(side='left', padx=(0,8))
        ttk.Button(row3, text="📋 複製選中項目到新增欄",  command=self._copy_def_to_input).pack(side='left')

        self._refresh_prop_defs()

    def _get_all_cats_for_combo(self):
        return self.dm.get_all_categories()

    def _refresh_prop_defs(self, search="", cat_filter=""):
        self.def_tree.delete(*self.def_tree.get_children())
        builtin_names = self.dm.get_all_builtin_names()
        defs = self.dm.get_all_prop_defs()
        total = 0
        for cat, items in defs.items():
            if cat_filter and cat != cat_filter: continue
            for name, unit, method in items:
                if search and search.lower() not in name.lower() and search.lower() not in cat.lower(): continue
                is_builtin = name in builtin_names
                src  = "📌內建" if is_builtin else "✏️用戶"
                tag  = 'builtin' if is_builtin else 'user'
                dbkey = self.dm.get_prop_csv_key(name)
                dbkey_display = dbkey if dbkey != name else "(=顯示名稱)"
                self.def_tree.insert("","end", values=(src, cat, name, dbkey_display, unit, method), tags=(tag,))
                total += 1
        self.lbl_count.config(text=f"共 {total} 項")
        cats = ["（全部）"] + self._get_all_cats_for_combo()
        self.cb_filter_cat['values'] = cats
        self.cb_pcat['values'] = self._get_all_cats_for_combo()

    def _filter_prop_defs(self, _=None):
        search = self.e_search.get().strip()
        cat_f  = self.cb_filter_cat.get()
        cat_f  = "" if cat_f in ("","（全部）") else cat_f
        self._refresh_prop_defs(search, cat_f)

    def _clear_filter(self):
        self.e_search.delete(0,tk.END)
        self.cb_filter_cat.set("（全部）")
        self._refresh_prop_defs()

    def _add_prop_def(self):
        name = self.e_pname.get().strip()
        cat  = self.cb_pcat.get().strip()
        dbkey = self.e_pdbkey.get().strip()
        if not name: messagebox.showwarning("提示","請輸入顯示名稱"); return
        if not cat:  messagebox.showwarning("提示","請選擇或輸入目標分類"); return
        if not dbkey: messagebox.showwarning("提示","請輸入DB Key（英文鍵名，用於數據庫存儲）"); return
        if not dbkey.replace('_','').replace('-','').isalnum():
            messagebox.showwarning("提示","DB Key 只能包含英文字母、數字、底線和連字號"); return
        all_defs = self.dm.get_all_prop_defs()
        for items in all_defs.values():
            if any(n == name for n,u,m in items):
                messagebox.showwarning("提示", f"顯示名稱「{name}」已存在，請使用不同名稱"); return
        existing_keys = [p.get('db_key','') for p in self.dm.custom_props if p.get('db_key')]
        if dbkey in existing_keys:
            messagebox.showwarning("提示", f"DB Key「{dbkey}」已存在，請使用不同鍵名"); return
        new_p = {"category": cat, "name": name, "db_key": dbkey,
                 "unit": self.e_punit.get().strip(), "method": self.e_pmethod.get().strip()}
        self.dm.custom_props.append(new_p)
        self.dm.save_custom_props()
        self._refresh_prop_defs(); self._build_prop_form()
        if self._sel_recipe: self._load_prop_values(self._sel_recipe)
        for e in [self.e_pname, self.e_pdbkey, self.e_punit, self.e_pmethod]: e.delete(0,tk.END)
        messagebox.showinfo("新增成功", f"已將「{name}」(DB: {dbkey}) 新增至「{cat}」，物性表單已更新")

    def _del_prop_def(self):
        sel = self.def_tree.selection()
        if not sel: messagebox.showwarning("提示","請先選擇要刪除的項目"); return
        vals = self.def_tree.item(sel[0])['values']
        src  = vals[0]; name = vals[2]; cat = vals[1]
        is_builtin = "內建" in str(src)
        msg = f"確定刪除內建屬性「{name}」？\n可點「恢復內建預設」還原。" if is_builtin else f"確定刪除使用者屬性「{name}」？\n（已填入此屬性的配方數據不受影響）"
        if not messagebox.askyesno("確認刪除", msg): return
        if is_builtin:
            # 以 _deleted 標記記錄至 user_props，讓 get_all_prop_defs 過濾掉
            if not any(p.get('category') == '_deleted' and p.get('name') == name for p in self.dm.custom_props):
                self.dm.custom_props.append({"category": "_deleted", "name": name, "unit": "", "method": ""})
        else:
            self.dm.custom_props = [p for p in self.dm.custom_props if p['name'] != name or p.get('category') == '_deleted']
        self.dm.save_custom_props()
        self._refresh_prop_defs(); self._build_prop_form()
        if self._sel_recipe: self._load_prop_values(self._sel_recipe)
        messagebox.showinfo("OK", f"已刪除「{name}」")

    def _restore_builtins(self):
        deleted = [p['name'] for p in self.dm.custom_props if p.get('category') == '_deleted']
        if not deleted:
            messagebox.showinfo("提示","目前沒有被刪除的內建項目"); return
        if not messagebox.askyesno("確認恢復", f"將恢復以下 {len(deleted)} 個內建項目：\n" + "\n".join(f"  • {n}" for n in deleted)): return
        self.dm.custom_props = [p for p in self.dm.custom_props if p.get('category') != '_deleted']
        self.dm.save_custom_props()
        self._refresh_prop_defs(); self._build_prop_form()
        if self._sel_recipe: self._load_prop_values(self._sel_recipe)
        messagebox.showinfo("OK", f"已恢復 {len(deleted)} 個內建項目")

    def _copy_def_to_input(self):
        sel = self.def_tree.selection()
        if not sel: return
        vals = self.def_tree.item(sel[0])['values']
        # vals: (src, cat, name, dbkey, unit, method)
        self.e_pname.delete(0,tk.END);   self.e_pname.insert(0,  str(vals[2]))
        self.e_pdbkey.delete(0,tk.END)
        dbk = str(vals[3])
        if dbk != "(=顯示名稱)": self.e_pdbkey.insert(0, dbk)
        self.e_punit.delete(0,tk.END);   self.e_punit.insert(0,  str(vals[4]))
        self.e_pmethod.delete(0,tk.END); self.e_pmethod.insert(0, str(vals[5]))
        self.cb_pcat.set(str(vals[1]))

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
        self.lbl_sel_recipe.config(text=f"▶ 當前選中：{self._sel_recipe}", foreground="#0066cc")
        self._show_detail(); self._load_prop_values(self._sel_recipe)

    def _deselect_recipe(self):
        self._sel_recipe = None
        self.recipe_tree.selection_remove(*self.recipe_tree.selection())
        self.lbl_sel_recipe.config(text="（尚未選中配方）", foreground="#999")
        self.detail_txt.config(state='normal'); self.detail_txt.delete("1.0",tk.END); self.detail_txt.config(state='disabled')
        self._clear_props()

    def _show_detail(self):
        row = self.dm.get_recipe_row(self._sel_recipe)
        self.detail_txt.config(state='normal'); self.detail_txt.delete("1.0",tk.END)
        if not row: self.detail_txt.config(state='disabled'); return

        self.detail_txt.insert(tk.END, f"配方：{row.get('配方名稱','')}\n")
        batch = row.get('批次號','')
        if batch: self.detail_txt.insert(tk.END, f"批次號：{batch}\n")
        self.detail_txt.insert(tk.END, f"日期：{row.get('建立日期','')}   模式：{row.get('計算模式','')}\n")
        self.detail_txt.insert(tk.END, f"總質量：{row.get('總質量_g','')} g    氯：{row.get('總氯含量_ppm','')} ppm\n\n")

        for cat, cn in CAT_CN.items():
            n = SLOT_COUNTS[cat]
            lines = []
            for i in range(1, n+1):
                nm = row.get(f"{cn}{i}_名稱","")
                if not nm: continue
                mass = row.get(f"{cn}{i}_質量_g",""); pct = row.get(f"{cn}{i}_佔比%","")
                extra = ""
                if cat == "resins": extra = f"  EEW={row.get(f'{cn}{i}_EEW','')}"
                elif cat == "hardeners": extra = f"  當量={row.get(f'{cn}{i}_當量','')}  {row.get(f'{cn}{i}_子類型','')}"
                lines.append(f"  {cn}{i}: {nm}  {mass}g ({pct}%){extra}")
            if lines:
                self.detail_txt.insert(tk.END, f"── {cn} ──\n")
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
            messagebox.showwarning("提示","請先選擇一個配方"); return
        props = {}
        for pname, ent in self._prop_entries.items():
            v = ent.get().strip()
            if v:
                csv_key = self.dm.get_prop_csv_key(pname)
                props[csv_key] = v
        if not props:
            messagebox.showwarning("提示","尚未填寫任何物性數值"); return
        ok = self.dm.update_recipe_props(self._sel_recipe, props)
        if ok:
            messagebox.showinfo("成功", f"已儲存 {len(props)} 項物性數據至配方行\n({RECIPE_DB_FILE})")
        else:
            messagebox.showerror("錯誤","找不到對應配方行，請確認配方已存在於數據庫")

    def _clear_props(self):
        for ent in self._prop_entries.values(): ent.delete(0,tk.END)

    def _rename(self):
        sel = self.recipe_tree.selection()
        if not sel: messagebox.showwarning("提示","請先選擇配方"); return
        old = self.recipe_tree.item(sel[0])['values'][0]
        new = simpledialog.askstring("重命名",f"將「{old}」重命名為：", parent=self.frame.winfo_toplevel())
        if not new or new == old: return
        if new in self.dm.get_recipe_names(): messagebox.showwarning("提示",f"名稱「{new}」已存在"); return
        self.dm.rename_recipe(old, new)
        if self._sel_recipe == old: self._sel_recipe = new
        self.refresh(); messagebox.showinfo("OK",f"已重命名為「{new}」")

    def _delete(self):
        sel = self.recipe_tree.selection()
        if not sel: messagebox.showwarning("提示","請先選擇配方"); return
        name = self.recipe_tree.item(sel[0])['values'][0]
        if not messagebox.askyesno("確認刪除",f"確定刪除配方「{name}」？\n（包含所有已錄入的物性數據）"): return
        self.dm.delete_recipe(name)
        self._deselect_recipe()
        self.refresh()
        messagebox.showinfo("OK",f"已刪除「{name}」")

    def _copy_row(self):
        if not self._sel_recipe:
            messagebox.showwarning("提示","請先選擇配方"); return
        row = self.dm.get_recipe_row(self._sel_recipe)
        if not row: return

        lines = []
        lines.append(f"配方名稱\t{row.get('配方名稱','')}")
        lines.append(f"批次號\t{row.get('批次號','')}")
        lines.append("")
        lines.append("物料名稱\t質量(g)\t佔比(%)")
        for cat, cn in CAT_CN.items():
            for i in range(1, SLOT_COUNTS[cat]+1):
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
                    prop_lines.append(f"{pname}\t{val}{unit}")
        if prop_lines:
            lines.append("物性項目\t數值")
            lines.extend(prop_lines)

        text = "\n".join(lines) + "\n"
        self.frame.clipboard_clear(); self.frame.clipboard_append(text); self.frame.update()
        messagebox.showinfo("複製成功",
            f"已複製「{self._sel_recipe}」配方數據（垂直表格格式）\n可在 Excel 中 Ctrl+V 貼上。")


# ═══════════════════════════════════════════
#  EpoxyApp  主協調器
# ═══════════════════════════════════════════
class EpoxyApp:
    def __init__(self, root):
        self.root = root
        root.title("環氧樹脂工作站 V3.4.0")
        root.geometry("1400x960")
        root.minsize(1100, 700)

        font_std  = ("Microsoft JhengHei", 10)
        font_bold = ("Microsoft JhengHei", 10, "bold")
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=font_bold)
        try: style.configure("Accent.TButton", font=font_bold, foreground="white", background="#0078d4")
        except: pass

        self.dm = DataManager()

        self.nb = ttk.Notebook(root); self.nb.pack(pady=5, expand=True, fill='both')
        self.calc_tab   = CalcTab(self.nb, self.dm, font_std, font_bold)
        self.db_tab     = DatabaseTab(self.nb, self.dm, font_std, font_bold)
        self.recipe_tab = RecipeTab(self.nb, self.dm, font_std, font_bold)

        self.nb.bind("<<NotebookTabChanged>>", self._on_tab)

    def _on_tab(self, _):
        txt = self.nb.tab(self.nb.select(), "text")
        if "配方管理" in txt: self.recipe_tab.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    app  = EpoxyApp(root)

    root.mainloop()

