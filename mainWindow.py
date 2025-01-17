from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from qfluentwidgets import FluentIcon, NavigationItemPosition, MSFluentWindow, ScrollArea, OptionsSettingCard, qconfig

import dishes
from config import MyConfig
from myIcons import MyIcon
from widgets import homepage, orderpage


class BaseInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("base")
        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setContentsMargins(5, 5, 5, 10)

        self.add_items()

        self.setWidgetResizable(True)
        self.enableTransparentBackground()
        self.setWidget(self.view)

    def add_items(self):
        pass


class HomeInterface(BaseInterface):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("home")

    def add_items(self):
        self.appCard = homepage.AppInfoCard()
        self.vBoxLayout.addWidget(self.appCard, 0, Qt.AlignTop)


class OrderInterface(BaseInterface):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("order")

    def add_items(self):
        self.dCard = orderpage.DishCard(dishes.burger)
        self.vBoxLayout.addWidget(self.dCard, 0, Qt.AlignTop)


class SettingsInterface(BaseInterface):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("settings")

    def add_items(self):
        self.switch_dark_mode_card = OptionsSettingCard(
            MyConfig.themeMode,
            FluentIcon.BRUSH,
            "应用主题",
            "调整你的应用外观",
            texts=["浅色", "深色", "跟随系统设置"],
        )
        self.vBoxLayout.addWidget(self.switch_dark_mode_card, 0, Qt.AlignTop)



class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()

        # 界面初始化
        self.setWindowTitle("点餐系统")
        self.setMinimumSize(800, 600)
        self.resize(1200, 800)
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.setWindowIcon(MyIcon.Burger.icon())  # 设置图标

        # 添加界面
        self.homeInterface = HomeInterface()
        self.orderInterface = OrderInterface()
        self.settingsInterface = SettingsInterface()

        self.homeInterface.appCard.set_switch_to_order(self, self.orderInterface)

        self.addSubInterface(self.homeInterface, FluentIcon.HOME, "主页",
                             position=NavigationItemPosition.TOP)  # TOP是指在导航栏的最上方
        self.addSubInterface(self.orderInterface, FluentIcon.ADD, "点餐",
                             position=NavigationItemPosition.SCROLL)
        self.addSubInterface(self.settingsInterface, FluentIcon.SETTING, "设置",
                             position=NavigationItemPosition.BOTTOM)  # BOTTOM是指在导航栏的最下方
