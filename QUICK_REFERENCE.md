# 快速上傳參考卡 (Quick Upload Reference)

## 🚀 第一次上傳（新專案）

```bash
# 1. 在本地創建專案目錄
mkdir epoxy-manager
cd epoxy-manager

# 2. 複製檔案到此目錄
# - EpoxyManager.py
# - README.md
# - .gitignore
# - LICENSE

# 3. 初始化 Git
git init
git add .
git commit -m "Initial commit - V4.1.1"

# 4. 在 GitHub 創建新 repository
# https://github.com/new

# 5. 連接並推送
git remote add origin https://github.com/yourusername/epoxy-manager.git
git branch -M main
git push -u origin main

# 6. 創建版本標籤
git tag -a v4.1.1 -m "Release V4.1.1"
git push origin v4.1.1
```

---

## 🔄 更新現有專案

```bash
# 1. 備份數據（重要！）
mkdir backup_$(date +%Y%m%d)
cp *.csv backup_$(date +%Y%m%d)/
cp *.json backup_$(date +%Y%m%d)/

# 2. 進入專案目錄
cd epoxy-manager

# 3. 確認狀態
git status
git branch

# 4. 替換主程式
cp ~/Downloads/EpoxyManager.py .

# 5. 更新 README
cp ~/Downloads/README.md .

# 6. 提交更新
git add EpoxyManager.py README.md
git commit -m "更新至 V4.1.1"

# 7. 創建標籤
git tag -a v4.1.1 -m "Release V4.1.1"

# 8. 推送
git push origin main
git push origin v4.1.1
```

---

## 📝 修改 README 的必要項目

在上傳前，務必修改 README.md 中的以下內容：

```markdown
# 搜尋並替換：
yourusername     → 你的 GitHub 用戶名
您的名字         → 你的真實姓名或暱稱
your.email@example.com → 你的 Email
```

快速替換方法：
```bash
# macOS/Linux
sed -i 's/yourusername/actual-username/g' README.md
sed -i 's/your.email@example.com/actual@email.com/g' README.md

# Windows (使用 Git Bash)
sed -i 's/yourusername/actual-username/g' README.md
sed -i 's/your.email@example.com/actual@email.com/g' README.md
```

---

## 🔧 常用 Git 命令

```bash
# 查看狀態
git status

# 查看變更
git diff

# 添加檔案
git add .                    # 所有檔案
git add EpoxyManager.py      # 特定檔案

# 提交
git commit -m "描述訊息"

# 查看歷史
git log
git log --oneline            # 簡潔模式

# 推送
git push origin main

# 拉取
git pull origin main

# 創建分支
git checkout -b new-branch

# 切換分支
git checkout main

# 查看遠端
git remote -v

# 標籤管理
git tag                      # 列出標籤
git tag -a v1.0 -m "訊息"   # 創建標籤
git push origin v1.0         # 推送標籤
git push --tags              # 推送所有標籤
```

---

## ⚠️ 緊急救援命令

```bash
# 撤銷最後一次 commit（保留變更）
git reset --soft HEAD~1

# 撤銷最後一次 commit（不保留變更）
git reset --hard HEAD~1

# 丟棄本地所有變更
git checkout .

# 清除未追蹤的檔案
git clean -fd

# 回復到特定 commit
git reset --hard <commit-hash>

# 強制推送（謹慎使用！）
git push -f origin main
```

---

## 📋 提交訊息範例

### 功能新增
```
feat: 新增多語言支援功能

- 支援正體中文、簡體中文、英語、日語
- 新增語言切換下拉選單
- 更新所有 UI 文字為可翻譯格式
```

### Bug 修復
```
fix: 修復當量計算精度問題

- 修正浮點數運算誤差
- 調整取整邏輯
- 增加單元測試
```

### 文檔更新
```
docs: 更新 README 和使用說明

- 新增多語言說明章節
- 更新安裝步驟
- 增加常見問題解答
```

### 程式碼重構
```
refactor: 重構數據庫管理模組

- 採用扁平化 CSV 架構
- 優化查詢性能
- 簡化 API 介面
```

---

## 🎯 檢查清單

上傳前檢查：
- [ ] 已備份所有數據檔案
- [ ] README.md 個人資訊已更新
- [ ] .gitignore 設定正確
- [ ] 程式可正常執行
- [ ] commit 訊息清楚明確
- [ ] 敏感資料已排除

上傳後檢查：
- [ ] GitHub 上檔案顯示正確
- [ ] README.md 格式正常
- [ ] 版本標籤已創建
- [ ] Release 已發布（可選）

---

## 💡 最佳實踐

1. **經常提交**：小步快跑，頻繁 commit
2. **清晰訊息**：commit message 要描述性強
3. **定期備份**：數據檔案另外備份
4. **版本標籤**：重要版本打上 tag
5. **文檔更新**：代碼和文檔同步更新
6. **測試後推送**：確保程式可運行再 push

---

## 📞 問題排查

### 無法推送
```bash
# 可能原因：遠端有新內容
git pull origin main --rebase
git push origin main
```

### 合併衝突
```bash
# 查看衝突檔案
git status

# 手動編輯解決衝突後
git add .
git commit -m "解決合併衝突"
```

### 誤刪檔案
```bash
# 恢復已刪除的檔案
git checkout HEAD -- filename.py
```

---

**需要詳細說明？請參閱 GITHUB_UPDATE_GUIDE.md**
