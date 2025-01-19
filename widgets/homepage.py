"""
    主页组件
    包括：
        应用信息卡片
"""

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import SimpleCardWidget, IconWidget, TitleLabel, PrimaryPushButton, FluentIcon, HyperlinkLabel, \
    StrongBodyLabel, FluentWindow

from myIcons import MyIcon


class AppInfoCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(200)

        self.icon = IconWidget(MyIcon.Burger.icon())
        self.icon.setFixedSize(100, 100)

        self.title = TitleLabel("点餐系统")
        self.link = HyperlinkLabel(QUrl("https://ulinoyaped.eu.org"), "访问网站")
        self.startButton = PrimaryPushButton(FluentIcon.ADD_TO, "开始")
        self.description = StrongBodyLabel("一个基于Qt的点餐系统")

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.hBoxLayout.setSpacing(20)

        self.hBoxLayout.addWidget(self.icon, 0, QtCore.Qt.AlignLeft)

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

        self.titleHbox = QHBoxLayout()
        self.titleHbox.setContentsMargins(0, 0, 0, 0)

        self.titleHbox.addWidget(self.title, 2, QtCore.Qt.AlignTop)
        self.titleHbox.addWidget(self.startButton, 1, QtCore.Qt.AlignTop)

        self.vBoxLayout.addLayout(self.titleHbox, 1)
        self.vBoxLayout.addWidget(self.link, 0, QtCore.Qt.AlignTop)
        self.vBoxLayout.addWidget(self.description, 3, QtCore.Qt.AlignVCenter)

        self.hBoxLayout.addLayout(self.vBoxLayout, 1)

        self.order_interface = None
        self.window = None
        self.startButton.clicked.connect(self.start_button_clicked)

    def set_switch_to_order(self, window: FluentWindow, switch_to):
        self.order_interface = switch_to
        self.window = window

    def start_button_clicked(self):
        if self.order_interface is not None and self.window is not None:
            self.window.switchTo(self.order_interface)
