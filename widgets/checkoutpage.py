"""
    结账界面组件
    包括：
        优惠券卡片
        结账卡片
"""
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import HeaderCardWidget, ElevatedCardWidget, IconWidget, InfoBarIcon, SubtitleLabel

import coupon
from myIcons import MyIcon
from widgets import orderpage


class CouponCardWidget(ElevatedCardWidget):
    """
    优惠券卡片
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
            which_icon = self.status

        if which_icon:
            self.status_icon.setIcon(self.okIcon)
        else:
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

    def handle_coupon_clicked(self):
        """
        处理优惠券点击事件
        :return:
        """
        for c in self.coupon_card_list:
            if c is not self.sender():
                c.switch_status_icon(False)
            else:
                c.switch_status_icon(True)


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
        self.total_price_label = SubtitleLabel(f"总价: ¥{self._total_price:.2f}")
        self.reduction_label = SubtitleLabel(f"优惠: ¥{self._reduction:.2f}")
        self.required_pay_label = SubtitleLabel(f"应付: ¥{self._required_pay:.2f}")

        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.total_price_label, 0, QtCore.Qt.AlignTop)
        self.vBox.addWidget(self.reduction_label, 0, QtCore.Qt.AlignTop)
        self.vBox.addWidget(self.required_pay_label, 0, QtCore.Qt.AlignTop)
        self.viewLayout.addLayout(self.vBox)

class CheckoutCard(HeaderCardWidget):
    """
    结账卡片
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("checkoutCard")
        self.setMinimumHeight(300)
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
