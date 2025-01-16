from PyQt5.QtWidgets import QFrame, QHBoxLayout
from qfluentwidgets import FluentWindow, FluentIcon, NavigationItemPosition


class Home(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("home")
        self.setLayout(QHBoxLayout())


class OrderFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("order")
        self.setLayout(QHBoxLayout())


class Settings(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("settings")
        self.setLayout(QHBoxLayout())


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        # 界面初始化
        self.setWindowTitle("点餐系统")
        self.setMinimumSize(800, 600)

        # 添加界面
        self.homeInterface = Home()
        self.settingsInterface = Settings()

        self.addSubInterface(self.homeInterface, FluentIcon.HOME, "主页",
                             position=NavigationItemPosition.TOP)  # TOP是指在导航栏的最上方
        self.addSubInterface(self.settingsInterface, FluentIcon.SETTING, "设置",
                             position=NavigationItemPosition.BOTTOM)  # BOTTOM是指在导航栏的最下方
