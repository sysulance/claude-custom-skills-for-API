#!/bin/bash
# Claude Code Custom Skills 安装脚本（已修复版）

set -e

echo "🚀 安装 Claude Code Custom Skills..."
echo ""

# 正确的安装目录
SKILLS_DIR="$HOME/.claude/skills"

# 创建目录
mkdir -p "$SKILLS_DIR"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📦 安装技能到: $SKILLS_DIR"
echo ""

# 安装每个 Skill
for skill in conversation-resumer session-manager todo-manager help-system file-history-browser cross-project-search; do
    if [ -d "$SCRIPT_DIR/$skill" ]; then
        skill_path="$SKILLS_DIR/$skill"

        # 如果已存在，先备份
        if [ -d "$skill_path" ]; then
            backup_path="${skill_path}.backup.$(date +%Y%m%d_%H%M%S)"
            echo "  📁 备份现有版本到: $backup_path"
            mv "$skill_path" "$backup_path"
        fi

        # 复制新版本
        echo "  📦 安装 $skill..."
        cp -r "$SCRIPT_DIR/$skill" "$SKILLS_DIR/"

        # 验证 SKILL.md 存在
        if [ -f "$skill_path/SKILL.md" ]; then
            echo "  ✅ $skill 安装完成"
        else
            echo "  ⚠️  $skill 缺少 SKILL.md，可能无法正常工作"
        fi
    else
        echo "  ⚠️  $skill 未找到，跳过"
    fi
done

echo ""
echo "✅ 安装完成！"
echo ""
echo "📋 下一步："
echo "  1. 重新启动 Claude Code 或新开一个对话"
echo "  2. 输入: 你有什么可用的 skills？"
echo "  3. 验证技能是否被正确加载"
echo ""
echo "📋 可选：添加别名到 shell 配置"
echo "  echo 'source ~/.claude/custom-skills/.bash_aliases' >> ~/.zshrc"
echo "  source ~/.zshrc"
echo ""
echo "📁 技能安装位置:"
echo "  $SKILLS_DIR/"
echo ""
