from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import ElevatedCardWidget, IconWidget, TitleLabel, CardWidget, TransparentToolButton, FluentIcon, \
    SubtitleLabel, PrimaryToolButton

from dishes import Dish

order_dict = {}


# class OrderInfo:
#     dish: Dish
#     num: int = 0
#
#     def __init__(self, dish: Dish, num: int):
#         self.dish = dish
#         self.num = num


class AddOrSubtractWidget(ElevatedCardWidget):
    def __init__(self, dish, parent=None):
        super().__init__(parent)
        self.setFixedSize(150, 50)
        self.setContentsMargins(0, 0, 0, 0)
        self.hBox = QHBoxLayout(self)

        self.dish = dish
        self.num: int = 0

        self.subtract_button = TransparentToolButton(FluentIcon.REMOVE.icon())
        self.number_label = SubtitleLabel(str(self.num))
        self.add_button = PrimaryToolButton(FluentIcon.ADD.icon())

        self.hBox.addWidget(self.subtract_button, 0, QtCore.Qt.AlignLeft)
        self.hBox.addWidget(self.number_label, 0, QtCore.Qt.AlignCenter)
        self.hBox.addWidget(self.add_button, 0, QtCore.Qt.AlignRight)

        self.subtract_button.clicked.connect(lambda: self.change_num(-1))
        self.add_button.clicked.connect(lambda: self.change_num(1))

    def change_num(self, change):
        self.num += change
        if self.num < 0:
            self.num = 0
        self.number_label.setText(str(self.num))
        order_dict[self.dish] = self.num

    def get_num(self):
        return self.num


class DishCard(CardWidget):
    def __init__(self, dish: Dish, parent=None):
        super().__init__(parent)
        self.dish = dish
        self.setFixedSize(300, 200)
        self.setContentsMargins(10, 0, 10, 0)

        self.iconWidget = IconWidget(self.dish.icon)
        self.iconWidget.setFixedSize(100, 100)

        self.nameLabel = TitleLabel(self.dish.name)
        self.nameLabel.setTextColor(QtGui.QColor('#333'))

        self.priceLabel = SubtitleLabel(f'¥{self.dish.price:.2f}/{self.dish.unit}')

        self.add_or_subtract_widget = AddOrSubtractWidget(self.dish)

        self.hBox = QHBoxLayout(self)
        self.hBox.addWidget(self.iconWidget, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self.rightVBox = QVBoxLayout()
        self.rightVBox.addWidget(self.nameLabel, 1, QtCore.Qt.AlignTop)
        self.rightVBox.addWidget(self.priceLabel, 1, QtCore.Qt.AlignLeft)
        self.rightVBox.addWidget(self.add_or_subtract_widget, 2, QtCore.Qt.AlignBottom)

        self.hBox.addLayout(self.rightVBox, 1)

        self.nameLabel.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)


class CheckOutWidget(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(300)
