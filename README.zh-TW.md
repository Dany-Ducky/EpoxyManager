# EpoxyManager 環氧樹脂工作站

> 工欲善其事，必先利其器  
> 專為環氧調校，或能延伸至其他熱固性 / 光固化 / PU 等配方系統

**繁體中文** · [English](README.md) · [日本語](README.ja.md)

為**環氧接著劑與密封膠配方設計**打造的桌面工作站，整合機器學習黏度預測、物料資料庫管理、以及完整的四語介面。

---

## ✨ 功能特色

### 🧪 配方設計
- **1K 單組分**配方設計，支援三種配平模式：`target_100g`、`phr_100`、`free`
- **2K 雙組分**配方設計，以當量比驅動 A/B 側計算，支援 EEW / AHEW 當量配平與自訂比例
- 即時成本估算、氯含量追蹤、投料校正
- 一鍵複製到 Excel（垂直/水平排列）

### 📊 機器學習黏度預測
- **五層集成模型**：Gaussian Process Regression + Bayesian Ridge + 自適應 k-NN
- 物理模型備援：Grunberg-Nissan 混合定律、Arrhenius 溫度依賴性、Krieger-Dougherty 填料修正
- 以 Jaccard 相似度加權歷史配方修正
- 累積 ≥2 筆含黏度資料的配方後自動啟用

### 🧮 化學工具箱
- **凝膠時間估算**：Arrhenius 外推 7 種固化劑類型（DICY / 胺類 / 酸酐 / 咪唑 / 巰基 / 潛伏型 / 酚醛）
- **DiBenedetto Tg 預測**：由 Tg₀ / Tg∞ 與固化度推算
- **CTE 預測**：依體積分率以混合律計算
- **UV / 熱雙重固化**設計：光起始劑 + 熱起始劑配比
- **DSC 解析**：Ti / Tp / ΔH / Ea 提取，催化均聚係數
- **熱平衡計算**：絕熱溫升、散熱估算

### 🌏 完整多語言支援
- 即時切換介面語言：**繁體中文 / 简体中文 / English / 日本語**
- 596 個翻譯鍵覆蓋所有 UI 元素、物性名稱、測試方法、提示文字
- 跨語言保持 CSV 欄位相容性

### 🎨 Apple 風格 UI
- 9 種主題色（藍、紫、粉、紅、橙、綠、青、石墨、黑）
- 自訂圓角下拉選單、Tooltip、分段按鈕
- 系統字型自動偵測（SF Pro / Microsoft JhengHei / Hiragino）

### 📦 物料與配方資料庫
- 8 大物性分類，80+ 預建欄位（未固化 / 固化過程 / 機械 / 熱 / 耐化學 / 電 / 可靠性 / 自訂）
- 自訂物料分類（樹脂、固化劑、促進劑、填料、助劑等）支援自訂欄位數與欄位組合
- 固化劑子類型正規化（胺類 / 聚醯胺 / 酸酐 / 巰基 / 咪唑 / DICY / 酚醛 / 潛伏型）
- CSV 儲存，可攜性佳

### 🔬 物性管理
- 配方物性結構化輸入（DSC/DMA/TMA 的 Tg、CTE α1/α2、介電 Dk/Df、導熱率、搭接剪切、回焊耐性、PCT/HAST 可靠性等）
- 黏度-溫度外推、多組分混合黏度

---

## 🚀 快速開始

### 環境需求
- Python **3.10+**
- 已測試於 Windows 10/11、macOS、Linux

### 安裝
```bash
pip install -r requirements.txt
```

### 執行
```bash
python EpoxyManager.py
```

首次執行時，程式會在工作目錄下自動建立空白資料庫與設定檔。

---

## 📂 自動產生的資料檔（已 Gitignore）

程式會在工作目錄下產生下列檔案，內含**您的**資料，預設不會上傳至版本庫：

| 檔案 | 用途 |
|------|------|
| `epoxy_db.csv` | 物料資料庫 |
| `recipe_database.csv` | 配方資料庫（含物性資料）|
| `custom_properties.csv` | 使用者自訂物性欄位 |
| `user_prop_definitions.csv` | 使用者自訂物性分類 |
| `lang_config.json` | 介面語言偏好 |
| `epoxy_prefs.json` | UI 偏好（主題色、資料庫路徑）|
| `custom_categories.json` | 自訂固化劑子類型 |
| `custom_mat_cats.json` | 自訂物料分類 |
| `mat_col_config.json` | 欄位顯示配置 |

---

## 🛠 架構概覽

- **單一檔案 Python 應用**（約 5,670 行）— 無外部設定、無建構步驟
- **UI**：CustomTkinter 搭配自訂 Apple 風格 widget
- **i18n**：596 個翻譯鍵，以 zh_TW 為規範鍵名（CSV 向下相容）
- **資料**：CSV 儲存，內建 schema 自動遷移
- **ML**：scikit-learn GPR + BayesianRidge + k-NN 集成，物理模型備援

---

## 📝 授權

MIT License — 詳見 [LICENSE](LICENSE)

---

## 🙏 致謝

本專案使用 [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)、[scikit-learn](https://scikit-learn.org/)、[NumPy](https://numpy.org/) 建構。

名言出處：
- 孔子《論語·衛靈公》—「工欲善其事，必先利其器」
- 空海（弘法大師）《性霊集》—「良工まずその刀を利くし、能書は必ず好筆を用う」
- 林肯（Abraham Lincoln）—"Give me six hours to chop down a tree and I will spend the first four sharpening the axe."

---

## 🤝 貢獻

歡迎提交 Issue 與 Pull Request。較大幅度的變更請先開 Issue 討論。

若 EpoxyManager 對您的工作有幫助，歡迎給 repo 按個 ⭐。
