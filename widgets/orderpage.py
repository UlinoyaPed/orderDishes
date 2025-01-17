from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout
from qfluentwidgets import ElevatedCardWidget, IconWidget, TitleLabel, themeColor

from dishes import Dish


class DishCard(ElevatedCardWidget):
    def __init__(self, dish: Dish, parent=None):
        super().__init__(parent)
        self.dish = dish
        self.setFixedSize(150, 150)
        self.setContentsMargins(10, 0, 10, 0)

        self.iconWidget = IconWidget(self.dish.icon)
        self.iconWidget.setFixedSize(100, 100)

        self.nameLabel = TitleLabel(self.dish.name)
        self.nameLabel.setTextColor(themeColor())

        self.vBox = QVBoxLayout(self)
        self.vBox.addWidget(self.iconWidget, 0, QtCore.Qt.AlignCenter)
        self.vBox.addWidget(self.nameLabel, 1)

        self.nameLabel.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
