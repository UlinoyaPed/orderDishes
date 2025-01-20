"""
    结账界面组件
    包括：
        优惠券卡片
        结账卡片
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import HeaderCardWidget, ElevatedCardWidget, IconWidget, InfoBarIcon, SubtitleLabel

import coupon
from myIcons import MyIcon
from widgets import orderpage


class CouponCardWidget(ElevatedCardWidget):
    """
    每个优惠券卡片
    """
    clickedRequested = QtCore.pyqtSignal()

    def __init__(self, coupon_item: coupon.CouponBase, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)

        self.coupon_item = coupon_item
        self.okIcon = InfoBarIcon.SUCCESS.icon()
        self.noIcon = InfoBarIcon.ERROR.icon()

        self.hBox = QHBoxLayout(self)

        self.status = False
        self.status_icon = IconWidget(self.noIcon)
        self.status_icon.setFixedSize(25, 25)
        self.coupon_icon = IconWidget(MyIcon.Coupon.icon())
        self.coupon_icon.setFixedSize(40, 40)
        self.coupon_name_label = SubtitleLabel(self.coupon_item.name)

        self.hBox.addWidget(self.coupon_icon, 0, QtCore.Qt.AlignLeft)
        self.hBox.addWidget(self.coupon_name_label, 1, QtCore.Qt.AlignLeft)
        self.hBox.addWidget(self.status_icon, 0, QtCore.Qt.AlignRight)

    def switch_status_icon(self, which_icon=None):
        """
        切换图标
        :param which_icon: True为正确图标 False为错误图标
        :return:
        """
        if which_icon is None:
            self.status = not self.status
        else:
            self.status = which_icon

        if self.status is True:
            self.status_icon.setIcon(self.okIcon)
        if self.status is False:
            self.status_icon.setIcon(self.noIcon)

    def mousePressEvent(self, e):
        """
        鼠标点击事件
        :param e:
        :return:
        """
        self.clickedRequested.emit()


class CheckoutCouponCard(HeaderCardWidget):
    """
    结账页面优惠券
    """
    updateRequested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("优惠券")
        self.setMinimumHeight(300)
        self.vBox = QVBoxLayout(self)

        self.coupon_card_list = []
        for c in coupon.all_coupons:
            coupon_card = CouponCardWidget(c)
            coupon_card.clickedRequested.connect(self.handle_coupon_clicked)
            self.coupon_card_list.append(coupon_card)
            self.vBox.addWidget(coupon_card, 1, QtCore.Qt.AlignTop)

        self.viewLayout.addLayout(self.vBox)

    def get_active_coupon(self):
        """
        获取当前激活的优惠券
        :return: 当前激活的优惠券
        """
        for c in self.coupon_card_list:
            if c.status:
                return c.coupon_item

    def handle_coupon_clicked(self):
        """
        处理优惠券点击事件
        :return:
        """
        for c in self.coupon_card_list:
            if c is not self.sender():
                c.switch_status_icon(False)
            else:
                c.switch_status_icon()
        self.updateRequested.emit()  # 发出信号


class PaymentCard(HeaderCardWidget):
    """
    支付卡片
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.setTitle("支付")

        self._total_price: float = 0
        self._reduction: float = 0
        self._required_pay: float = 0
        self.total_price_label = SubtitleLabel()
        self.reduction_label = SubtitleLabel()
        self.required_pay_label = SubtitleLabel()
        self.set_text_content()

        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.total_price_label, 0, QtCore.Qt.AlignTop)
        self.vBox.addWidget(self.reduction_label, 0, QtCore.Qt.AlignTop)
        self.vBox.addWidget(self.required_pay_label, 0, QtCore.Qt.AlignTop)
        self.viewLayout.addLayout(self.vBox)

    def set_text_content(self, total_price: float = 0, reduction: float = 0, required_pay: float = 0):
        self._total_price = total_price
        self._reduction = reduction
        self._required_pay = required_pay
        self.total_price_label.setText(f"总价: ¥{self._total_price:.2f}")
        self.reduction_label.setText(f"优惠: ¥{self._reduction:.2f}")
        self.required_pay_label.setText(f"应付: ¥{self._required_pay:.2f}")


class CheckoutCard(HeaderCardWidget):
    """
    结账卡片
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("checkoutCard")
        # self.setMinimumHeight(300)
        self.setContentsMargins(10, 10, 10, 10)
        self.setTitle('结账')

        self.mainVBox = QVBoxLayout()

        self.confirm_checkout_widget = orderpage.OrderInformationWidget()
        self.confirm_checkout_widget.setTitle('确认订单')
        self.checkout_coupon_card = CheckoutCouponCard()

        self.payment_card = PaymentCard()

        self.hBoxLayout = QHBoxLayout()
        self.leftVBox = QVBoxLayout()
        self.rightVBox = QVBoxLayout()
        self.hBoxLayout.addLayout(self.leftVBox, 3)
        self.hBoxLayout.addLayout(self.rightVBox, 2)

        self.mainVBox.addLayout(self.hBoxLayout, 1)
        self.viewLayout.addLayout(self.mainVBox)

        self.leftVBox.addWidget(self.confirm_checkout_widget, 1, QtCore.Qt.AlignTop)
        self.rightVBox.addWidget(self.checkout_coupon_card)

        self.rightVBox.addWidget(self.payment_card, 0)

        self.checkout_coupon_card.updateRequested.connect(self.update_content)

    def update_content(self):
        order_dict = orderpage.get_order_dict()
        active_coupon = self.checkout_coupon_card.get_active_coupon()
        if active_coupon is not None:
            total_price = active_coupon.calculate_total_price(order_dict)
            required_pay = active_coupon.apply(order_dict)
            reduction = total_price - required_pay
            self.payment_card.set_text_content(total_price, reduction, required_pay)
        else:
            total_price = sum([d.price * order_dict[d] for d in order_dict])
            self.payment_card.set_text_content(total_price, 0, total_price)
