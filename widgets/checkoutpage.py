"""
    结账界面组件
    包括：
        结账卡片
"""
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import HeaderCardWidget

from widgets import orderpage


class CheckoutCard(HeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("checkoutCard")
        self.setMinimumHeight(300)
        self.setContentsMargins(10, 10, 10, 10)
        self.setTitle('结账')

        self.goto_checkout_widget = orderpage.GotoCheckOutWidget()
        self.goto_checkout_widget.setTitle('确认订单')

        self.leftVBox = QVBoxLayout()

        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addLayout(self.leftVBox)

        self.viewLayout.addLayout(self.hBoxLayout)

        self.leftVBox.addWidget(self.goto_checkout_widget)
