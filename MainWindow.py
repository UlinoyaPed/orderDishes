from qfluentwidgets import FluentIcon, NavigationItemPosition, MSFluentWindow, ScrollArea

from widgets import homepage


class Home(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("home")

        self.appCard = homepage.AppInfoCard(self)
        self.setWidget(self.appCard)


class OrderFrame(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("order")


class Settings(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("settings")


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()

        # 界面初始化
        self.setWindowTitle("点餐系统")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(FluentIcon.APPLICATION.icon())  # 设置图标

        # 添加界面
        self.homeInterface = Home()
        self.orderInterface = OrderFrame()
        self.settingsInterface = Settings()

        self.addSubInterface(self.homeInterface, FluentIcon.HOME, "主页",
                             position=NavigationItemPosition.TOP)  # TOP是指在导航栏的最上方
        self.addSubInterface(self.orderInterface, FluentIcon.ADD, "点餐",
                             position=NavigationItemPosition.SCROLL)
        self.addSubInterface(self.settingsInterface, FluentIcon.SETTING, "设置",
                             position=NavigationItemPosition.BOTTOM)  # BOTTOM是指在导航栏的最下方
