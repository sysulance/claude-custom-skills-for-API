# Claude Code Custom Skills

用於替代 Kimi API 下不可用的 Claude Code 原生斜杠命令。支持自然語言觸發和斜杠命令兩種調用方式。

## 已開發 Skill

| Skill | 斜杠命令 | 自然語言觸發詞 | 功能 |
|-------|---------|--------------|------|
| conversation-resumer | `/history` | 查看歷史對話、恢復對話 | 查看/恢復歷史對話 |
| session-manager | `/session` | 重命名會話、查看會話信息 | 會話管理 |
| todo-manager | `/todo` | 查看待辦、添加任務 | 任務管理 |
| help-system | `/help` | 查看幫助、有哪些技能 | 幫助系統 |
| file-history-browser | `/file` | 查看文件歷史 | 文件操作歷史 |
| cross-project-search | `/search` | 跨項目搜索 | 跨項目搜索內容 |

---

## 🚀 即插即用安裝指南

### 第一步：克隆倉庫

```bash
git clone https://github.com/sysulance/claude-custom-skills-for-API.git
cd claude-custom-skills-for-API
```

### 第二步：一鍵安裝（推薦）

```bash
./install.sh
```

安裝腳本會自動：
- 創建 `~/.claude/skills/` 目錄
- 複製所有 skill 到正確位置
- 備份現有版本（如有）

### 第三步：重啟 Claude Code

**完全退出 Claude Code**，然後重新啟動：

```bash
# 退出當前會話
exit

# 重新啟動
claude
```

### 第四步：驗證安裝

在新對話中輸入：
```
你有什麼可用的 skills？
```

或測試斜杠命令：
```
/history
```

---

## 📁 文件結構

安裝後的目錄結構：

```
~/.claude/
├── skills/                    # 技能目錄（Claude Code 自動掃描）
│   ├── conversation-resumer/
│   │   ├── SKILL.md
│   │   └── scripts/
│   ├── cross-project-search/
│   ├── file-history-browser/
│   ├── help-system/
│   ├── session-manager/
│   └── todo-manager/
├── commands/                  # 斜杠命令定義
│   └── history.md
└── settings.local.json        # 權限配置（自動創建）
```

---

## ⚙️ 手動安裝（如需要）

如果一鍵安裝腳本無法使用，可以手動安裝：

```bash
# 1. 創建 skills 目錄
mkdir -p ~/.claude/skills

# 2. 複製所有 skill
for dir in */; do
    [ -d "$dir" ] || continue
    skill_name=$(basename "$dir")
    # 跳過非 skill 目錄
    [[ "$skill_name" == ".git" ]] && continue
    [[ "$skill_name" == "backups" ]] && continue

    mkdir -p "$HOME/.claude/skills/$skill_name"
    cp -r "$dir"/* "$HOME/.claude/skills/$skill_name/"
    echo "✓ Installed: $skill_name"
done

# 3. 複製斜杠命令
mkdir -p ~/.claude/commands
cp commands/history.md ~/.claude/commands/

echo "✅ 手動安裝完成！"
```

---

## 🔧 權限配置

首次使用 `/history` 等命令時，Claude Code 會詢問權限批准。

### 方法一：對話中批准（推薦）

當提示時選擇：
- **"Always allow"** - 永久允許
- **"Allow once"** - 僅允許一次

### 方法二：預先配置

編輯 `~/.claude/settings.local.json`，添加：

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 ~/.claude/skills/conversation-resumer/scripts/scan_history.py*)",
      "Bash(python3 ~/.claude/skills/session-manager/scripts/session_manager.py*)",
      "Bash(python3 ~/.claude/skills/todo-manager/scripts/todo_manager.py*)",
      "Bash(python3 ~/.claude/skills/help-system/scripts/help_system.py*)",
      "Bash(python3 ~/.claude/skills/file-history-browser/scripts/file_history.py*)",
      "Bash(python3 ~/.claude/skills/cross-project-search/scripts/cross_project_search.py*)"
    ]
  }
}
```

---

## 🌐 跨設備同步

### 推送配置到新設備

```bash
# 1. 在新設備上克隆倉庫
git clone https://github.com/sysulance/claude-custom-skills-for-API.git

# 2. 運行安裝腳本
cd claude-custom-skills-for-API
./install.sh

# 3. 重啟 Claude Code
echo "請完全退出並重新啟動 Claude Code"
```

### 更新現有安裝

```bash
cd ~/.claude/custom-skills  # 或你的克隆路徑
git pull
./install.sh
```

---

## 💡 使用方法

### 斜杠命令

```
/history              # 查看歷史對話
/history --project    # 按項目分組
/history --stats      # 統計信息

/session list         # 列出會話
/session rename XXX   # 重命名會話
/todo                 # 查看待辦
/help                 # 顯示幫助
```

### 自然語言觸發

```
"查看所有歷史對話"    → 觸發 conversation-resumer
"恢復之前的對話"      → 觸發 conversation-resumer
"重命名這個會話"      → 觸發 session-manager
"查看待辦事項"        → 觸發 todo-manager
"有哪些技能"          → 觸發 help-system
```

---

## 🔍 故障排除

### Skill 未被識別

1. **確認安裝位置**
   ```bash
   ls -la ~/.claude/skills/
   ```

2. **確認 SKILL.md 存在**
   ```bash
   ls ~/.claude/skills/*/SKILL.md
   ```

3. **完全重啟 Claude Code**
   - 必須完全退出（不只是 /clear）
   - 然後重新啟動

### 權限錯誤

如果看到 `permission check failed`：
- 在對話中批准執行，選擇 "Always allow"
- 或參考上面的權限配置部分

### 路徑錯誤

確保所有 skill 使用新路徑：
- ✅ 正確：`~/.claude/skills/`
- ❌ 錯誤：`~/.claude/custom-skills/` 或 `~/.claude/plugins/`

---

## 📜 更新日誌

### 2025-03-03 - 重大更新

- ✅ 修復 skill 無法在新對話識別的問題
- ✅ 添加中文自然語言觸發支持
- ✅ 簡化安裝流程，無需 `enabledPlugins` 配置
- ✅ 更新所有路徑至 `~/.claude/skills/`
- ✅ 添加一鍵安裝腳本

---

## 📄 License

MIT

---

## 🙋 問題反饋

如有問題，請在 GitHub Issues 中反饋：
https://github.com/sysulance/claude-custom-skills-for-API/issues
