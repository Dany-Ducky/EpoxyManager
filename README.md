# 環氧樹脂工作站 (Epoxy Manager) V3.4.0

![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/License-MIT-green.svg)


## 🌟 核心功能

* **多組分整合計算**：支持同時處理多種樹脂 (Resins)、固化劑 (Hardeners)、助劑 (Additives)、填料 (Fillers) 與催化劑 (Catalysts) 的比例分配。
* **精確化學計算**：
    * 自動計算配方總重與質量百分比 (wt%)。
    * 即時運算 **EEW (環氧當量)** 與 **活潑氫當量** 平衡。
    * 追蹤總氯含量 (Total Chlorine ppm) 以符合低鹵素要求。
* **扁平化數據庫管理**：內建材料數據庫 (CSV 架構)，方便快速調用常用原料，無需重複輸入規格。
* **配方紀錄系統**：支援保存歷史配方、查看修改紀錄，並可重新載入計算。
* **數據導出優化**：提供「一鍵複製到 Excel」功能，自動優化垂直/水平表格格式，方便實驗紀錄。

## 🛠️ 技術需求

本程式使用 Python 內建庫開發，無需安裝額外的重量級框架：

## 環境要求
- 操作系統：Windows 10/11, macOS, 或 Linux
- 語言環境：**Python 3.8 或以上版本**
- 依賴庫：無（僅使用標準庫）

## 📂 檔案結構

為了確保程式正常運行，請保持以下檔案架構（程式運行後會自動生成缺失的資料庫文件）：

```text
.
├── EpoxyManager3.4.0.py    # 主程式檔案
├── epoxy_db.csv            # 原料數據庫
├── recipe_database.csv     # 配方歷史紀錄
├── custom_properties.csv   # 自定義屬性配置
└── mat_col_config.json     # 欄位顯示設定
