"""
    主窗口
    包含主界面和设置界面
    主界面包含主页、点餐、结算三个界面
    设置界面包含主题切换、关于等选项
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from qfluentwidgets import FluentIcon, NavigationItemPosition, MSFluentWindow, ScrollArea, OptionsSettingCard, \
    FlowLayout

import dishes
from config import MyConfig
from myIcons import MyIcon
from widgets import homepage, orderpage, checkoutpage


class BaseInterface(ScrollArea):
    """
    基础界面
    包含一个垂直布局
    用于添加各种组件
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("base")
        self.view = QWidget()

        self.layout = QVBoxLayout(self.view)
        self.layout.setContentsMargins(5, 5, 5, 10)

        self.add_items()

        self.setWidgetResizable(True)
        self.enableTransparentBackground()
        self.setWidget(self.view)

    def add_items(self):
        pass


class HomeInterface(BaseInterface):
    """
    主页界面
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("home")

    def add_items(self):
        self.appCard = homepage.AppInfoCard()
        self.layout.addWidget(self.appCard, 0, Qt.AlignTop)


class OrderInterface(BaseInterface):
    """
    点餐界面
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("order")

    def add_items(self):
        self.flowLayout = FlowLayout()

        self.layout.addLayout(self.flowLayout, 0)

        self.goto_checkout_widget = orderpage.GotoCheckOutWidget()

        for dish in dishes.all_dishes:
            dCard = orderpage.DishCard(dish)
            dCard.set_update_func(self.goto_checkout_widget.update_order_info)
            self.flowLayout.addWidget(dCard)

        self.layout.addWidget(self.goto_checkout_widget, 0, Qt.AlignTop)


class CheckoutInterface(BaseInterface):
    """
    结算界面
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("checkout")

    def add_items(self):
        self.checkout_card = checkoutpage.CheckoutCard()
        self.layout.addWidget(self.checkout_card, 0, Qt.AlignTop)


class SettingsInterface(BaseInterface):
    """
    设置界面
    """

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
        self.layout.addWidget(self.switch_dark_mode_card, 0, Qt.AlignTop)


class MainWindow(MSFluentWindow):
    """
    主窗口
    """

    def __init__(self):
        super().__init__()

        # 界面初始化
        self.setWindowTitle("点餐系统")
        self.setMinimumSize(800, 600)
        self.resize(1100, 800)
        desktop = QApplication.desktop().availableGeometry()  # 获取屏幕大小
        w, h = desktop.width(), desktop.height()  # 获取屏幕宽和高
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)  # 移动窗口居中
        self.setWindowIcon(MyIcon.Burger.icon())  # 设置图标

        # 添加界面
        self.homeInterface = HomeInterface()  # 主页界面
        self.orderInterface = OrderInterface()  # 点餐界面
        self.checkoutInterface = CheckoutInterface()  # 结账界面
        self.settingsInterface = SettingsInterface()  # 设置界面

        self.homeInterface.appCard.startRequested.connect(
            lambda: self.switchTo(self.orderInterface))  # 设置主页界面的切换到点餐界面
        self.orderInterface.goto_checkout_widget.checkoutRequested.connect(
            lambda: self.switchTo(self.checkoutInterface))  # 设置点餐界面的切换到结账界面

        self.addSubInterface(self.homeInterface, FluentIcon.HOME, "主页",
                             position=NavigationItemPosition.TOP)  # TOP是指在导航栏的最上方
        self.addSubInterface(self.orderInterface, FluentIcon.ADD, "点餐",
                             position=NavigationItemPosition.SCROLL)  # SCROLL是指在导航栏的中间
        self.addSubInterface(self.checkoutInterface, FluentIcon.ACCEPT, "结账",
                             position=NavigationItemPosition.SCROLL)
        self.addSubInterface(self.settingsInterface, FluentIcon.SETTING, "设置",
                             position=NavigationItemPosition.BOTTOM)  # BOTTOM是指在导航栏的最下方
