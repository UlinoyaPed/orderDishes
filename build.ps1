# 使用pyinstaller打包Python脚本
pyinstaller -D -w -i .\assets\icons\Burger.png .\main.py

# 复制assets文件夹到打包后的目录
Copy-Item .\assets .\dist\main\assets -recurse

# 重命名dist目录下的main文件夹为新的名称
Rename-Item -Path .\dist\main -NewName "orderDishes"
