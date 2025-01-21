pyinstaller -D -w -i .\assets\icons\Burger.png .\main.py

Copy-Item .\assets .\dist\main\assets -recurse
