# 環氧樹脂工作站 (Epoxy Resin Workstation)

[![Version](https://img.shields.io/badge/version-4.1.1-blue.svg)](https://github.com/Dany-Ducky/EpoxyManager)
[![Python](https://img.shields.io/badge/python-3.6+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

一套專業的環氧樹脂配方設計與管理系統，提供多語言介面和完整的材料數據庫。

A professional epoxy resin formulation design and management system with multi-language interface and comprehensive material database.

[中文](#中文說明) | [English](#english-description)

---

## 中文說明

### ✨ 主要功能

#### 🗡 配方設計與計算
- **智能配方計算**：支援固定質量和固定比例兩種計算模式
- **多元材料系統**：樹脂、固化劑、助劑、填料、催化劑全覆蓋
- **當量平衡分析**：自動計算環氧當量(EEW)和硬化劑當量(AHEW)比例
- **氯含量追蹤**：精確計算總氯含量(ppm)
- **100g配平功能**：可選擇性地將配方標準化至100g總量
- **一鍵報表生成**：計算結果可直接複製到Excel
- **配方保存**：將設計完成的配方儲存至數據庫

#### 🕷 物料數據庫管理
- **完整參數記錄**：
  - 基礎屬性：類別、名稱、類型、外觀
  - 物理性質：黏度、介電常數、表面能
  - 化學特性：分子結構、氯含量
  - 當量資訊：EEW/AHEW直接輸入或輔助計算
- **固化劑當量計算器**：
  - 支援胺類、聚酰胺、酸酐、巰基、羥基等類型
  - 自動換算胺值、酸值、羥基值至當量
- **自定義欄位系統**：可新增、刪除、顯示/隱藏欄位
- **資料操作**：新增、編輯、刪除、另存為新物料

#### 📋 配方管理與物性
- **配方庫管理**：查看、編輯、重命名、刪除已儲存的配方
- **物性測試記錄**：
  - 流動性測試：Viscosity、Gelation Time
  - 熱性能：Tg、TMA、TGA
  - 機械性能：Tensile、Flex、Shear
  - 熱機械：CTE、Storage Modulus
  - 電性能：Dk、Df
  - 其他：Moisture Absorption、Copper Peel Strength等
- **數據匯出**：配方和物性數據可複製到Excel進行進一步分析

#### 🌍 多語言支援
- 正體中文 (Traditional Chinese)
- 简体中文 (Simplified Chinese)
- English
- 日本語 (Japanese)

### 📋 系統需求

- **Python**: 3.6 或更高版本
- **作業系統**: Windows / macOS / Linux
- **必要套件**: tkinter (通常隨Python內建)

### 🚀 安裝與使用

#### 方法一：直接執行
```bash
# 1. 下載專案
git clone https://github.com/Dany-Ducky/EpoxyManager.git
cd EpoxyManager

# 2. 執行程式
python EpoxyManager.py
```

#### 方法二：建立虛擬環境（推薦）
```bash
# 1. 建立虛擬環境
python -m venv venv

# 2. 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 執行程式
python EpoxyManager.py
```

### 📁 資料檔案

程式執行時會自動創建以下檔案：
- `material_database.csv` - 物料數據庫（樹脂、固化劑、助劑、填料、催化劑）
- `recipe_database.csv` - 配方數據庫
- `lang_config.json` - 語言設定檔
- `mat_col_config.json` - 物料欄位設定檔
- `prop_definitions.json` - 物性定義檔

> ⚠️ **重要**：請務必備份這些檔案，它們包含您的所有數據！

### 🎯 使用流程

1. **設定語言**：在右上角選擇您偏好的語言
2. **建立材料庫**：
   - 切換到「物料數據庫管理」頁籤
   - 新增您的樹脂、固化劑等材料資訊
   - 使用固化劑計算器輔助計算當量
3. **設計配方**：
   - 切換到「配方設計與計算」頁籤
   - 從下拉選單選擇材料並設定質量或比例
   - 調整計算模式（固定質量/固定比例）
   - 點擊「開始計算」生成完整報表
4. **保存配方**：
   - 輸入配方名稱和批次號
   - 儲存至配方數據庫
5. **記錄物性**：
   - 切換到「配方管理與物性」頁籤
   - 選擇配方並輸入測試結果
   - 追蹤配方的實際性能表現

### 🔧 進階功能

#### 質量取整選項
- **0.1g**：適用於小批量實驗（精度要求高）
- **1g**：適用於中型批量
- **10g**：適用於大批量生產

#### 100g配平系統
可設定特定材料是否參與100g標準化計算，靈活控制配方總量。

#### 自定義欄位
在物料數據庫中，您可以新增特定行業或實驗室需要的自定義參數欄位。

### 📊 數據格式

所有數據以CSV格式儲存，方便與Excel、數據分析工具整合：
- 採用UTF-8編碼
- 欄位名稱中英文對照
- 支援匯出到Excel進行進一步分析

### 🤝 貢獻指南

歡迎提交Issue和Pull Request！

1. Fork 此專案
2. 創建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟Pull Request

### 📝 版本歷史

#### V4.1.1 (Current)
- 整合式扁平配方數據庫架構
- 完整的多語言系統（中文、英語、日語）
- 增強的物性測試記錄功能
- 自定義欄位管理系統

#### 舊版本
請參閱 [CHANGELOG.md](CHANGELOG.md) 查看完整版本歷史

### 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件

### 👥 作者

- Dany-Ducky - [GitHub](https://github.com/Dany-Ducky)

### 🙏 致謝

感謝所有貢獻者和使用者的支持！

---

## English Description

### ✨ Key Features

#### 🗡 Formulation Design & Calculation
- **Smart Formula Calculator**: Supports both fixed mass and fixed ratio modes
- **Multi-Material System**: Comprehensive coverage of resins, hardeners, additives, fillers, and catalysts
- **Equivalent Balance Analysis**: Auto-calculate EEW (Epoxy Equivalent Weight) and AHEW ratios
- **Chlorine Content Tracking**: Precise calculation of total chlorine content (ppm)
- **100g Balancing**: Optional normalization to 100g total mass
- **One-Click Reports**: Results directly copyable to Excel
- **Recipe Storage**: Save designed formulas to database

#### 🕷 Material Database Management
- **Complete Parameter Recording**:
  - Basic properties: Category, name, type, appearance
  - Physical properties: Viscosity, dielectric constant, surface energy
  - Chemical characteristics: Molecular structure, chlorine content
  - Equivalent info: Direct EEW/AHEW input or assisted calculation
- **Hardener Equivalent Calculator**:
  - Supports amine, polyamide, anhydride, mercaptan, hydroxyl types
  - Auto-convert amine value, acid value, hydroxyl value to equivalent
- **Custom Field System**: Add, delete, show/hide fields
- **Data Operations**: Add, edit, delete, save as new material

#### 📋 Recipe Management & Properties
- **Recipe Library**: View, edit, rename, delete saved recipes
- **Property Testing Records**:
  - Flow properties: Viscosity, Gelation Time
  - Thermal: Tg, TMA, TGA
  - Mechanical: Tensile, Flex, Shear
  - Thermo-mechanical: CTE, Storage Modulus
  - Electrical: Dk, Df
  - Others: Moisture Absorption, Copper Peel Strength, etc.
- **Data Export**: Copy recipes and properties to Excel for analysis

#### 🌍 Multi-Language Support
- Traditional Chinese (正體中文)
- Simplified Chinese (简体中文)
- English
- Japanese (日本語)

### 📋 Requirements

- **Python**: 3.6 or higher
- **OS**: Windows / macOS / Linux
- **Dependencies**: tkinter (usually included with Python)

### 🚀 Installation & Usage

#### Method 1: Direct Execution
```bash
# 1. Clone the repository
git clone https://github.com/Dany-Ducky/epoxy-manager.git
cd epoxy-manager

# 2. Run the program
python EpoxyManager.py
```

#### Method 2: Virtual Environment (Recommended)
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Run the program
python EpoxyManager.py
```

### 📁 Data Files

The program automatically creates these files:
- `material_database.csv` - Material database (resins, hardeners, additives, fillers, catalysts)
- `recipe_database.csv` - Recipe database
- `lang_config.json` - Language configuration
- `mat_col_config.json` - Material column settings
- `prop_definitions.json` - Property definitions

> ⚠️ **Important**: Always backup these files - they contain all your data!

### 🎯 Workflow

1. **Set Language**: Choose your preferred language in the top-right corner
2. **Build Material Database**:
   - Switch to "Material Database Management" tab
   - Add your resins, hardeners, and other materials
   - Use hardener calculator to assist with equivalent calculations
3. **Design Formula**:
   - Switch to "Formulation Design & Calculation" tab
   - Select materials from dropdown and set mass or ratio
   - Adjust calculation mode (fixed mass/fixed ratio)
   - Click "Calculate" to generate complete report
4. **Save Recipe**:
   - Enter recipe name and batch number
   - Save to recipe database
5. **Record Properties**:
   - Switch to "Recipe & Properties" tab
   - Select recipe and input test results
   - Track actual performance of formulations

### 🔧 Advanced Features

#### Mass Rounding Options
- **0.1g**: For small-scale experiments (high precision)
- **1g**: For medium batches
- **10g**: For large-scale production

#### 100g Balancing System
Configure which materials participate in 100g normalization for flexible total mass control.

#### Custom Fields
Add industry-specific or lab-specific parameter fields in the material database.

### 📊 Data Format

All data stored in CSV format for easy integration with Excel and analysis tools:
- UTF-8 encoding
- Bilingual field names (Chinese/English)
- Export support to Excel for further analysis

### 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📝 Version History

#### V4.1.1 (Current)
- Integrated flat recipe database architecture
- Complete multi-language system (Chinese, English, Japanese)
- Enhanced property testing recording
- Custom field management system

#### Previous Versions
See [CHANGELOG.md](CHANGELOG.md) for full version history

### 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details

### 👥 Author

- Dany-Ducky - [GitHub](https://github.com/Dany-Ducky)

### 🙏 Acknowledgments

Thanks to all contributors and users for their support!

---

## 📸 Screenshots

### Main Interface
![Main Interface](screenshots/main.png)

### Formula Calculation
![Formula Calculation](screenshots/calculation.png)

### Material Database
![Material Database](screenshots/database.png)

### Recipe Management
![Recipe Management](screenshots/recipes.png)

---

## 💡 Tips

- **Backup Regularly**: Export your CSV files to prevent data loss
- **Version Control**: Use git to track changes in your material database
- **Collaboration**: Share material_database.csv with team members
- **Documentation**: Add detailed notes in the material database for future reference

---

## 🐛 Known Issues

Please check the [Issues](https://github.com/Dany-Ducky/EpoxyManager/issues) page for current bugs and feature requests.

## 📞 Support

- Create an issue: [GitHub Issues](https://github.com/Dany-Ducky/EpoxyManager/issues)

---

**⭐ If you find this project useful, please give it a star!**
