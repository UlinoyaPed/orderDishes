"""
    点餐界面组件
    包括：
        菜品卡片
        添加或减少菜品数量的部件
        结账卡片
        结账按钮
"""

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import ElevatedCardWidget, IconWidget, TitleLabel, CardWidget, TransparentToolButton, FluentIcon, \
    SubtitleLabel, PrimaryToolButton, StrongBodyLabel, HeaderCardWidget, ToolButton, FluentWindow

from dishes import Dish

order_dict = {}


class AddOrSubtractWidget(ElevatedCardWidget):
    """
    添加或减少菜品数量的部件
    """

    def __init__(self, dish: Dish, parent=None):
        """
        初始化部件
        :param dish: 菜品
        :param parent: 父部件
        """
        super().__init__(parent)
        self.setFixedSize(150, 50)
        self.setContentsMargins(0, 0, 0, 0)
        self.hBox = QHBoxLayout(self)

        self.dish = dish
        self.num: int = 0

        self.subtract_button = TransparentToolButton(FluentIcon.REMOVE.icon())  # 减少按钮
        self.number_label = SubtitleLabel(str(self.num))  # 数量标签
        self.add_button = PrimaryToolButton(FluentIcon.ADD.icon())  # 添加按钮

        self.hBox.addWidget(self.subtract_button, 0, QtCore.Qt.AlignLeft)
        self.hBox.addWidget(self.number_label, 0, QtCore.Qt.AlignCenter)
        self.hBox.addWidget(self.add_button, 0, QtCore.Qt.AlignRight)

        self.subtract_button.clicked.connect(lambda: self.change_num(-1))  # 减少按钮点击事件
        self.add_button.clicked.connect(lambda: self.change_num(1))  # 添加按钮点击事件

        self.update_checkout_info_func = None

    def change_num(self, change):
        """
        改变数量
        :param change: 改变量 可正可负
        :return:
        """
        self.num += change
        if self.num < 0:
            self.num = 0
        self.number_label.setText(str(self.num))
        order_dict[self.dish] = self.num

        if self.update_checkout_info_func is not None:
            self.update_checkout_info_func()

    def get_num(self) -> int:
        """
        获取数量
        :return: int 菜品的数量
        """
        return self.num

    def set_update_checkout_info(self, func):
        """
        设置更新结账信息的函数
        :param func: 函数
        :return:
        """
        self.update_checkout_info_func = func


class DishCard(CardWidget):
    """
    菜品卡片
    """

    def __init__(self, dish: Dish, parent=None):
        """
        初始化部件
        :param dish: 菜品
        :param parent: 父部件
        """
        super().__init__(parent)
        self.dish = dish
        self.setFixedHeight(200)
        self.setMinimumWidth(300)
        # self.setFixedSize(300, 200)
        self.setContentsMargins(10, 0, 10, 0)

        self.iconWidget = IconWidget(self.dish.icon)  # 图标
        self.iconWidget.setFixedSize(100, 100)

        self.nameLabel = TitleLabel(self.dish.name)  # 名称
        self.nameLabel.setTextColor(QtGui.QColor('#333'))

        self.priceLabel = SubtitleLabel(f'¥{self.dish.price:.2f}/{self.dish.unit}')  # 价格

        self.descriptionLabel = StrongBodyLabel(self.dish.description)  # 描述

        self.add_or_subtract_widget = AddOrSubtractWidget(self.dish)  # 添加或减少部件
        self.update_order_info = None  # 更新订单信息的函数

        self.hBox = QHBoxLayout(self)  # 水平布局
        self.hBox.addWidget(self.iconWidget, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self.rightVBox = QVBoxLayout()
        self.rightVBox.addWidget(self.nameLabel, 1, QtCore.Qt.AlignTop)
        self.rightVBox.addWidget(self.priceLabel, 1, QtCore.Qt.AlignLeft)
        self.rightVBox.addWidget(self.descriptionLabel, 1, QtCore.Qt.AlignLeft)
        self.rightVBox.addWidget(self.add_or_subtract_widget, 2, QtCore.Qt.AlignBottom)

        self.hBox.addLayout(self.rightVBox, 1)

        self.nameLabel.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)

    def set_update_func(self, func):
        """
        设置更新订单信息的函数
        :param func: 函数
        :return:
        """
        self.update_order_info = func
        self.add_or_subtract_widget.set_update_checkout_info(self.update_order_info)


class OrderedDishCard(ElevatedCardWidget):
    """
    已点菜品卡片
    """

    def __init__(self, dish: Dish, num: int, parent=None):
        """
        初始化部件
        :param dish: 菜品
        :param num: 菜品数量
        :param parent: 父部件
        """
        super().__init__(parent)
        self.dish = dish
        self.num = num

        self.setFixedHeight(80)

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
    """
    前往结账的部件
    """

    checkoutRequested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """
        初始化部件
        :param parent: 父部件
        """
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.setMinimumWidth(800)
        self.setTitle('订单信息')

        self.update_button = ToolButton(FluentIcon.ROTATE.icon())
        self.update_button.setFixedSize(50, 50)
        self.update_button.setToolTip('更新订单信息')
        self.update_button.clicked.connect(self.update_order_info)

        self.go_to_checkout_button = PrimaryToolButton(FluentIcon.CHECKBOX.icon())
        self.go_to_checkout_button.setFixedSize(50, 50)
        self.go_to_checkout_button.setToolTip('前往结账')
        self.go_to_checkout_button.clicked.connect(self.go_to_checkout_button_clicked)

        self.hBox = QHBoxLayout()

        self.dish_card_vBox = QVBoxLayout()
        self.button_vBox = QVBoxLayout()

        self.hBox.addLayout(self.dish_card_vBox, 1)
        self.hBox.addLayout(self.button_vBox, 0)

        self.button_vBox.addWidget(self.update_button, 1, QtCore.Qt.AlignBottom)
        self.button_vBox.addWidget(self.go_to_checkout_button, 0, QtCore.Qt.AlignBottom)

        self.viewLayout.addLayout(self.hBox)

    def update_order_info(self):
        """
        更新订单信息
        :return:
        """
        # 清空所有的菜品卡片
        while self.dish_card_vBox.count():
            item = self.dish_card_vBox.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 重新添加所有的菜品卡片
        for dish, num in order_dict.items():
            if num > 0:
                ordered_dish_card = OrderedDishCard(dish, num)
                self.dish_card_vBox.addWidget(ordered_dish_card, 0, QtCore.Qt.AlignTop)

    def go_to_checkout_button_clicked(self):
        """
        前往结账按钮点击事件
        :return:
        """
        self.checkoutRequested.emit()
