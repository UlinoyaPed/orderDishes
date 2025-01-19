from dishes import Dish


class CouponBase:
    """
    优惠券基类
    """
    def __init__(self, name):
        """
        初始化优惠券
        :param name: 名称
        """
        self.name = name
        self.total_price: float = 0

    def apply(self, order: dict) -> float:
        """
        应用优惠券
        :param order: 订单 格式为 {菜品: 数量}
        :return: float 优惠后的总价
        """
        raise NotImplementedError

    def calculate_total_price(self, order: dict):
        self.total_price = 0
        for dish, num in order.items():
            if not isinstance(dish, Dish):  # 防止出现非菜品的情况
                continue
            if num > 0:
                self.total_price += dish.price * num


class FullReduceCoupon(CouponBase):
    """
    满减券
    """

    def __init__(self, name, full: float, reduce: float):
        super().__init__(name)
        if full < 0:
            raise ValueError('full must be greater than 0')
        if reduce < 0:
            raise ValueError('reduce must be greater than 0')
        if full < reduce:
            raise ValueError('full must be greater than reduce')
        self.full = full
        self.reduce = reduce

    def apply(self, order):
        self.calculate_total_price(order)
        total = self.total_price
        if total >= self.full:
            return total - self.reduce
        return total


class PercentReduceCoupon(CouponBase):
    """
    折扣券
    """

    def __init__(self, name, percent: float):
        """
        初始化折扣券
        注意填的是折扣比例，比如打八折填0.2
        :param name: 名称
        :param percent: 折扣比例 0-1
        """
        super().__init__(name)
        if percent > 1:
            raise ValueError('percent must be less than 1')
        elif percent < 0:
            raise ValueError('percent must be greater than 0')
        self.percent = percent

    def apply(self, order):
        self.calculate_total_price(order)
        total = self.total_price
        return total * (1 - self.percent)


class VoucherCoupon(CouponBase):
    """
    代金券
    """

    def __init__(self, name, voucher: float):
        """
        初始化代金券
        :param name: 名称
        :param voucher: 代金券金额
        """
        super().__init__(name)
        if voucher < 0:
            raise ValueError('voucher must be greater than 0')
        self.voucher = voucher

    def apply(self, order):
        self.calculate_total_price(order)
        total = self.total_price
        total -= self.voucher
        if total < 0:
            return 0
        return total
