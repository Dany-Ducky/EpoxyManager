# GitHub 更新上傳指南 (GitHub Update Guide)

本指南專為已有舊版本儲存庫的使用者，說明如何更新到 V4.1.1 版本。

This guide is for users who already have an old version in their repository, explaining how to update to V4.1.1.

---

## 📋 目錄 (Table of Contents)

- [方法一：直接覆蓋更新（推薦）](#方法一直接覆蓋更新推薦)
- [方法二：建立新分支更新](#方法二建立新分支更新)
- [方法三：完全重新開始](#方法三完全重新開始)
- [更新後的檢查事項](#更新後的檢查事項)
- [常見問題](#常見問題)

---

## 方法一：直接覆蓋更新（推薦）

### 適用情況
- 你的舊版本沒有其他使用者正在使用
- 你想要保留 commit 歷史
- 你已經備份了重要的數據檔案

### 步驟

#### 1. 備份現有數據 ⚠️
```bash
# 進入專案目錄
cd EpoxyManager

# 備份數據檔案（非常重要！）
mkdir backup_$(date +%Y%m%d)
cp material_database.csv backup_$(date +%Y%m%d)/
cp recipe_database.csv backup_$(date +%Y%m%d)/
cp lang_config.json backup_$(date +%Y%m%d)/ 2>/dev/null
cp mat_col_config.json backup_$(date +%Y%m%d)/ 2>/dev/null
cp prop_definitions.json backup_$(date +%Y%m%d)/ 2>/dev/null
```

#### 2. 確認當前狀態
```bash
# 檢查當前分支
git branch

# 檢查是否有未提交的變更
git status

# 如果有未提交的變更，先提交或暫存
git add .
git commit -m "保存舊版本最後狀態"
```

#### 3. 更新主程式檔案
```bash
# 備份舊版本程式（可選）
cp EpoxyManager.py EpoxyManager_old.py

# 將新版本的 EpoxyManager.py 複製到專案目錄
# （將下載的新檔案複製過來）
```

#### 4. 更新 README
```bash
# 將新的 README.md 複製到專案目錄
# 記得修改 README 中的以下內容：
# - GitHub 用戶名 (Dany-Ducky)
# - 作者資訊
# - Email 聯絡方式
```

#### 5. 創建或更新其他文件
```bash
# 創建 .gitignore（如果還沒有）
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Backup files
backup_*/
*_old.py

# OS
.DS_Store
Thumbs.db

# Optional: 如果不想上傳數據檔案到 GitHub
# material_database.csv
# recipe_database.csv
# lang_config.json
# mat_col_config.json
# prop_definitions.json
EOF
```

```bash
# 創建 LICENSE（MIT License 範例）
cat > LICENSE << EOF
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

```bash
# 創建 CHANGELOG.md
cat > CHANGELOG.md << EOF
# Changelog

## [4.1.1] - 2025-03-04

### Added
- 整合式扁平配方數據庫架構
- 完整的多語言系統（正體中文、簡體中文、英語、日語）
- 增強的物性測試記錄功能
- 自定義欄位管理系統
- 固化劑當量輔助計算器
- 100g 配平功能

### Changed
- 優化了數據庫結構，採用 CSV 扁平化設計
- 改進了使用者界面的多語言支援
- 增強了配方計算精度

### Fixed
- 修復了當量計算的精度問題
- 修復了多語言切換時的界面更新問題

## [Previous Versions]
- 請參閱 git commit 歷史

---

格式基於 [Keep a Changelog](https://keepachangelog.com/)
EOF
```

#### 6. 提交更新
```bash
# 查看變更
git status

# 添加所有更新的檔案
git add EpoxyManager.py README.md .gitignore LICENSE CHANGELOG.md

# 提交更新
git commit -m "更新至 V4.1.1 版本

- 整合式扁平配方數據庫架構
- 完整多語言系統
- 增強物性測試功能
- 新增自定義欄位管理"
```

#### 7. 創建版本標籤
```bash
# 創建標籤
git tag -a v4.1.1 -m "Release V4.1.1 - 環氧樹脂工作站"

# 查看標籤
git tag
```

#### 8. 推送到 GitHub
```bash
# 推送主分支
git push origin main  # 或 git push origin master（根據你的主分支名稱）

# 推送標籤
git push origin v4.1.1

# 或推送所有標籤
git push --tags
```

---

## 方法二：建立新分支更新

### 適用情況
- 你想保留舊版本供參考
- 其他使用者可能還在使用舊版本
- 你想先測試新版本再合併

### 步驟

#### 1. 創建新分支
```bash
# 確保在主分支
git checkout main  # 或 master

# 創建並切換到新分支
git checkout -b version-4.1.1
```

#### 2. 更新檔案
```bash
# 將新版本的檔案複製到專案目錄
# EpoxyManager.py
# README.md
# 其他文件...

# 添加並提交
git add .
git commit -m "更新至 V4.1.1"
```

#### 3. 推送新分支
```bash
git push origin version-4.1.1
```

#### 4. 在 GitHub 上創建 Pull Request
1. 前往你的 GitHub repository
2. 點擊 "Pull requests" 頁籤
3. 點擊 "New pull request"
4. 選擇 base: main, compare: version-4.1.1
5. 填寫 PR 描述並創建
6. 審查後合併到主分支

#### 5. 合併後清理
```bash
# 切回主分支
git checkout main
git pull origin main

# 刪除本地分支（可選）
git branch -d version-4.1.1
```

---

## 方法三：完全重新開始

### 適用情況
- 舊版本有太多問題
- 你想要乾淨的 git 歷史
- 舊版本已經不需要了

### 步驟

#### 1. 備份數據
```bash
# 備份整個舊專案
cp -r EpoxyManager EpoxyManager-backup
```

#### 2. 刪除舊 repository（謹慎！）
```bash
# 在 GitHub 網站上：
# 1. 進入 repository Settings
# 2. 滾動到最底部
# 3. 點擊 "Delete this repository"
# 4. 確認刪除
```

#### 3. 創建新 repository
```bash
# 創建新目錄
mkdir EpoxyManager
cd EpoxyManager

# 初始化 git
git init

# 複製新版本檔案
# EpoxyManager.py
# README.md
# .gitignore
# LICENSE
# CHANGELOG.md

# 添加檔案
git add .
git commit -m "Initial commit - V4.1.1"

# 在 GitHub 創建新 repository 後
git remote add origin https://github.com/Dany-Ducky/EpoxyManager.git
git branch -M main
git push -u origin main
```

---

## 更新後的檢查事項

### ✅ 必須檢查

- [ ] 程式能正常執行
- [ ] 數據檔案已備份並保留
- [ ] README.md 中的個人資訊已更新
- [ ] .gitignore 設定正確
- [ ] LICENSE 檔案存在
- [ ] 版本標籤已創建

### ✅ 建議檢查

- [ ] 創建 screenshots 資料夾並添加截圖
- [ ] 更新 CHANGELOG.md 包含更詳細的變更記錄
- [ ] 添加 requirements.txt（如果有額外依賴）
- [ ] 創建 CONTRIBUTING.md（如果開放貢獻）
- [ ] 設定 GitHub Actions（如果需要 CI/CD）

---

## 在 GitHub 上創建 Release

更新完成後，在 GitHub 上創建正式 Release：

### 步驟

1. **前往 Releases 頁面**
   - 在 repository 主頁點擊右側的 "Releases"
   - 點擊 "Create a new release"

2. **選擇標籤**
   - 選擇剛才創建的 `v4.1.1` 標籤
   - 或者創建新標籤

3. **填寫 Release 資訊**
   ```
   標題: V4.1.1 - 環氧樹脂工作站
   
   描述:
   ## 🎉 新功能
   - 整合式扁平配方數據庫架構
   - 完整的多語言系統（正體中文、簡體中文、英語、日語）
   - 增強的物性測試記錄功能
   - 自定義欄位管理系統
   
   ## 🔧 改進
   - 優化數據庫結構
   - 改進使用者界面
   - 增強計算精度
   
   ## 📥 安裝方式
   下載 EpoxyManager.py 並執行：
   ```bash
   python EpoxyManager.py
   ```
   
   ## 📖 完整文檔
   請參閱 README.md
   ```

4. **上傳檔案**（可選）
   - 可以上傳打包好的 .zip 檔案
   - 或者讓 GitHub 自動生成 source code 壓縮檔

5. **發布**
   - 點擊 "Publish release"

---

## 常見問題

### Q1: 更新後舊的數據檔案會丟失嗎？
**A**: 不會。只要你按照步驟備份了數據檔案，它們會被保留。新版本程式會自動讀取現有的數據檔案。

### Q2: 需要刪除舊的 Python 檔案嗎？
**A**: 建議保留備份（EpoxyManager_old.py），但在 git 中只保留新版本。可以在 .gitignore 中添加 `*_old.py`。

### Q3: 如何保留舊版本供參考？
**A**: 使用 git tag 或分支保留舊版本：
```bash
# 在更新前為舊版本創建標籤
git tag -a v3.0.0 -m "舊版本"
git push origin v3.0.0
```

### Q4: 是否應該將數據檔案上傳到 GitHub？
**A**: 
- **優點**：方便備份和分享
- **缺點**：可能包含敏感資料
- **建議**：
  - 如果是個人專案或範例數據：可以上傳
  - 如果包含商業數據：加入 .gitignore 不上傳
  - 使用 .gitignore.example 提供範例

### Q5: 更新失敗怎麼辦？
**A**: 
```bash
# 回復到更新前的狀態
git reset --hard HEAD~1

# 或回復到特定 commit
git reset --hard <commit-hash>

# 強制推送（謹慎使用！）
git push -f origin main
```

### Q6: 如何讓多人協作時平滑更新？
**A**: 
1. 使用方法二（建立新分支）
2. 在 README 中添加遷移指南
3. 保留舊版本分支一段時間
4. 通知所有協作者更新時間

---

## 📞 獲取幫助

如果在更新過程中遇到問題：

1. **檢查 GitHub Issues**: [查看已知問題](https://github.com/Dany-Ducky/epoxy-manager/issues)
2. **創建新 Issue**: 描述你的問題和錯誤訊息
3. **Email**: danyducky@siacone.art

---

## 📚 相關資源

- [Git 官方文檔](https://git-scm.com/doc)
- [GitHub 官方文檔](https://docs.github.com/)
- [語義化版本控制](https://semver.org/lang/zh-TW/)
- [如何寫好 Commit Message](https://chris.beams.io/posts/git-commit/)

---

**更新愉快！如有問題歡迎提出 Issue。**
