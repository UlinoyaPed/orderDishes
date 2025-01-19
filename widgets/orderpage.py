from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import ElevatedCardWidget, IconWidget, TitleLabel, CardWidget, TransparentToolButton, FluentIcon, \
    SubtitleLabel, PrimaryToolButton, StrongBodyLabel, HeaderCardWidget, ToolButton

from dishes import Dish

order_dict = {}


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

        self.update_func = None

    def change_num(self, change):
        self.num += change
        if self.num < 0:
            self.num = 0
        self.number_label.setText(str(self.num))
        order_dict[self.dish] = self.num

        if self.update_func is not None:
            self.update_func()

    def get_num(self):
        return self.num

    def set_update_func(self, func):
        self.update_func = func


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

        self.descriptionLabel = StrongBodyLabel(self.dish.description)

        self.add_or_subtract_widget = AddOrSubtractWidget(self.dish)
        self.update_order_info = None

        self.hBox = QHBoxLayout(self)
        self.hBox.addWidget(self.iconWidget, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self.rightVBox = QVBoxLayout()
        self.rightVBox.addWidget(self.nameLabel, 1, QtCore.Qt.AlignTop)
        self.rightVBox.addWidget(self.priceLabel, 1, QtCore.Qt.AlignLeft)
        self.rightVBox.addWidget(self.descriptionLabel, 1, QtCore.Qt.AlignLeft)
        self.rightVBox.addWidget(self.add_or_subtract_widget, 2, QtCore.Qt.AlignBottom)

        self.hBox.addLayout(self.rightVBox, 1)

        self.nameLabel.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)

    def set_update_func(self, func):
        self.update_order_info = func
        self.add_or_subtract_widget.set_update_func(self.update_order_info)

class OrderedDishCard(ElevatedCardWidget):
    def __init__(self, dish: Dish, num: int, parent=None):
        super().__init__(parent)
        self.dish = dish
        self.num = num

        self.setFixedHeight(100)

        self.iconWidget = IconWidget(self.dish.icon)
        self.iconWidget.setFixedSize(50, 50)

        self.nameLabel = TitleLabel(self.dish.name)
        self.nameLabel.setTextColor(QtGui.QColor('#333'))

        self.priceLabel = SubtitleLabel(f'¥{self.dish.price:.2f}/{self.dish.unit}')

        self.quantityLabel = SubtitleLabel(f'数量: {self.num}')

        self.totalPriceLabel = SubtitleLabel(f'总价: ¥{(self.dish.price * self.num):.2f}')

        self.hBox = QHBoxLayout(self)
        self.hBox.addWidget(self.iconWidget, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.hBox.addWidget(self.nameLabel, 1, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.hBox.addWidget(self.priceLabel, 1, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.hBox.addWidget(self.quantityLabel, 1, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.hBox.addWidget(self.totalPriceLabel, 1, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)


class GotoCheckOutWidget(HeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(300)
        self.setMinimumWidth(800)
        self.setTitle('订单信息')

        self.update_button = ToolButton(FluentIcon.ROTATE.icon())
        self.update_button.setFixedSize(50, 50)
        self.update_button.setToolTip('更新订单信息')
        self.update_button.clicked.connect(self.update_order_info)

        self.go_to_checkout_button = PrimaryToolButton(FluentIcon.CHECKBOX.icon())
        self.go_to_checkout_button.setFixedSize(50, 50)
        self.go_to_checkout_button.setToolTip('前往结账')

        self.hBox = QHBoxLayout()

        self.dish_card_vBox = QVBoxLayout()
        self.button_vBox = QVBoxLayout()

        self.hBox.addLayout(self.dish_card_vBox, 1)
        self.hBox.addLayout(self.button_vBox, 0)

        self.button_vBox.addWidget(self.update_button, 1, QtCore.Qt.AlignBottom)
        self.button_vBox.addWidget(self.go_to_checkout_button, 0, QtCore.Qt.AlignBottom)

        self.viewLayout.addLayout(self.hBox)

    def update_order_info(self):
        while self.dish_card_vBox.count():
            item = self.dish_card_vBox.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for dish, num in order_dict.items():
            if num > 0:
                ordered_dish_card = OrderedDishCard(dish, num)
                self.dish_card_vBox.addWidget(ordered_dish_card)
