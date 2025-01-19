"""
    结账界面组件
    包括：
        结账卡片
"""

from qfluentwidgets import SimpleCardWidget, TitleLabel, PrimaryPushButton

from widgets import orderpage


class CheckoutCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("checkoutCard")
        self.setFixedSize(250, 300)
        self.setContentsMargins(10, 10, 10, 10)
        self.total_price: float = 0

        self.titleLabel = TitleLabel("Total Price", parent=self)

        self.checkoutButton = PrimaryPushButton("Checkout", parent=self)
        self.checkoutButton.move(50, 50)
        self.checkoutButton.clicked.connect(self.checkout)

    def checkout(self):
        self.total_price = 0
        for dish in orderpage.order_dict:
            num = orderpage.order_dict.get(dish, 0)
            if num > 0:
                self.total_price += dish.price * num

        self.titleLabel.setText(f'¥{self.total_price:.2f}')
