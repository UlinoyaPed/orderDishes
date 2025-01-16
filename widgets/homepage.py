from PyQt5.QtCore import QEasingCurve
from PyQt5.QtWidgets import QPushButton, QSizePolicy
from qfluentwidgets import SimpleCardWidget, FlowLayout


class AppInfoCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = FlowLayout(self, needAni=True)
        # 自定义动画参数
        layout.setAnimation(250, QEasingCurve.OutQuad)

        layout.setContentsMargins(30, 30, 30, 30)
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        layout.addWidget(QPushButton('hello world!'))
        layout.addWidget(QPushButton('hello world!'))
        layout.addWidget(QPushButton('hello world!'))
        layout.addWidget(QPushButton('hello world!'))
        layout.addWidget(QPushButton('hello world!'))
        # self.iconLabel = ImageLabel(parent=self)
        # self.nameLabel = TitleLabel('啊啊啊', parent=self)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
