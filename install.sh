#!/bin/bash
# Claude Code Custom Skills 安装脚本

set -e

echo "🚀 安装 Claude Code Custom Skills..."

SKILLS_DIR="$HOME/.claude/custom-skills"
PLUGINS_DIR="$HOME/.claude/plugins"

# 创建目录
mkdir -p "$SKILLS_DIR"
mkdir -p "$PLUGINS_DIR"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 安装每个 Skill
for skill in conversation-resumer session-manager todo-manager help-system; do
    echo "📦 安装 $skill..."
    
    # 复制源码
    if [ -d "$SCRIPT_DIR/$skill" ]; then
        cp -r "$SCRIPT_DIR/$skill" "$SKILLS_DIR/"
        
        # 打包 .skill 文件
        cd "$SKILLS_DIR/$skill"
        zip -r "$PLUGINS_DIR/$skill.skill" . -x "*.pyc" -x "__pycache__/*" > /dev/null 2>&1
        
        echo "  ✅ $skill 安装完成"
    else
        echo "  ⚠️  $skill 未找到，跳过"
    fi
done

# 复制别名文件
cp "$SCRIPT_DIR/.bash_aliases" "$SKILLS_DIR/"

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  1. 添加别名到 shell 配置:"
echo "     echo 'source ~/.claude/custom-skills/.bash_aliases' >> ~/.bashrc"
echo ""
echo "  2. 重新加载配置:"
echo "     source ~/.bashrc"
echo ""
echo "  3. 测试命令:"
echo "     resumer      # 查看历史对话"
echo "     session list # 列出会话"
echo "     todo         # 查看待办"
echo "     help-cc      # 显示帮助"
echo ""
