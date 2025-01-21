# git shell

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 统计所有文件的行数
git ls-files "*.py" | xargs wc -l | sort -n

# 等待
read -p "Press any key to continue..."
