# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.1.1] - 2025-03-04

### Added
- 整合式扁平配方數據庫架構 (Integrated flat recipe database architecture)
- 完整的多語言系統 (Complete multi-language system)
  - 正體中文 (Traditional Chinese)
  - 简体中文 (Simplified Chinese)
  - English
  - 日本語 (Japanese)
- 增強的物性測試記錄功能 (Enhanced property testing records)
- 自定義欄位管理系統 (Custom field management system)
- 固化劑當量輔助計算器 (Hardener equivalent calculator)
  - 支援胺類、聚酰胺、酸酐、巯基、羥基等類型
  - 自動換算胺值、酸值、羥基值至當量
- 100g 配平功能 (100g balancing feature)
- 質量取整選項 (0.1g / 1g / 10g)
- 配方 Excel 匯出功能 (Recipe Excel export)

### Changed
- 優化了數據庫結構，採用 CSV 扁平化設計 (Optimized database structure with CSV flat design)
- 改進了使用者界面的多語言支援 (Improved multi-language UI support)
- 增強了配方計算精度 (Enhanced formulation calculation precision)
- 重構了數據管理模組 (Refactored data management module)
- 改進了界面佈局和使用者體驗 (Improved UI layout and UX)

### Fixed
- 修復了當量計算的精度問題 (Fixed equivalent calculation precision issues)
- 修復了多語言切換時的界面更新問題 (Fixed UI update issues during language switching)
- 修復了數據保存時的編碼問題 (Fixed encoding issues during data saving)
- 修復了物料選擇下拉選單的重複項目問題 (Fixed duplicate items in material dropdown)

### Security
- 改進了數據檔案的讀寫安全性 (Improved data file I/O security)
- 加強了輸入驗證 (Enhanced input validation)

## [4.0.0] - [Previous Version Date]

### Added
- 基礎配方計算功能 (Basic formulation calculation)
- 物料數據庫管理 (Material database management)
- 配方保存與載入 (Recipe save and load)

### Changed
- 初始版本架構 (Initial version architecture)

## [3.0.0] - [Previous Version Date]

### Added
- 早期功能實現 (Early feature implementation)

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): Backwards-compatible new features
- **PATCH** version (0.0.X): Backwards-compatible bug fixes

## Types of Changes

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

---

## Unreleased

### Planned Features
- [ ] 數據視覺化圖表 (Data visualization charts)
- [ ] 配方比對功能 (Recipe comparison feature)
- [ ] 批量匯入/匯出 (Batch import/export)
- [ ] 配方模板系統 (Recipe template system)
- [ ] 進階搜尋與篩選 (Advanced search and filtering)
- [ ] 使用者權限管理 (User permission management)
- [ ] 雲端同步功能 (Cloud synchronization)
- [ ] 行動應用版本 (Mobile app version)

### Known Issues
- 大量數據時可能出現性能問題 (Performance issues with large datasets)
- 某些特殊字符在 CSV 中可能導致格式問題 (Special characters may cause CSV format issues)

---

## Contributing

如果您想為本專案做出貢獻，請：
1. Fork 本專案
2. 創建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

---

## Support

- 創建 Issue: [GitHub Issues](https://github.com/Dany-Ducky/epoxy-manager/issues)
- Email: danyducky@siacone.art

---

**注意**: 請在每次發布新版本時更新此文件。
