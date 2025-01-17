from PyQt5.QtCore import QEasingCurve
from PyQt5.QtWidgets import QSizePolicy
from qfluentwidgets import SimpleCardWidget, FlowLayout, PushButton


class AppInfoCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = FlowLayout(self, needAni=True)
        # 自定义动画参数
        layout.setAnimation(250, QEasingCurve.OutQuad)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.setContentsMargins(30, 30, 30, 30)
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        
