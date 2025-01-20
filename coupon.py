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
        self.requirement = '无'
        self._total_price: float = 0

    def apply(self, order: dict) -> float:
        """
        应用优惠券
        :param order: 订单 格式为 {菜品: 数量}
        :return: float 优惠后的总价
        """
        raise NotImplementedError

    def check_if_can_apply(self, order: dict) -> bool:
        """
        检查是否可以应用优惠券
        :param order: 订单
        :return: bool 是否可以应用
        """
        raise NotImplementedError

    def calculate_total_price(self, order: dict) -> float:
        """
        计算总价
        :param order: 订单
        :return: float 总价
        """
        self._total_price = 0
        for dish, num in order.items():
            if not isinstance(dish, Dish):  # 防止出现非菜品的情况
                continue
            if num > 0:
                self._total_price += dish.price * num
        return self._total_price


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
        self.requirement = f'消费达到{self.full:.2f}元'

    def check_if_can_apply(self, order):
        self.calculate_total_price(order)
        if self._total_price >= self.full:
            return True
        return False

    def apply(self, order):
        if self.check_if_can_apply(order):
            return self._total_price - self.reduce
        else:
            return self._total_price


class PercentReduceCoupon(CouponBase):
    """
    无条件折扣券
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

    def check_if_can_apply(self, order):
        self.calculate_total_price(order)
        return True

    def apply(self, order):
        if self.check_if_can_apply(order):
            return self._total_price * (1 - self.percent)
        else:
            return self._total_price


class FullPercentReduceCoupon(PercentReduceCoupon):
    """
    满减折扣券 满多少才打折扣
    """

    def __init__(self, name, full: float, percent: float):
        """
        初始化满减折扣券
        注意填的是折扣比例，比如打八折填0.2
        :param name: 名称
        :param full: 满多少元
        :param percent: 折扣比例 0-1
        """
        super().__init__(name, percent)
        if full < 0:
            raise ValueError('full must be greater than 0')
        self.full = full
        self.requirement = f'消费达到{self.full:.2f}元'

    def check_if_can_apply(self, order):
        self.calculate_total_price(order)
        if self._total_price >= self.full:
            return True
        return False

    def apply(self, order):
        if self.check_if_can_apply(order):
            return self._total_price * (1 - self.percent)
        else:
            return self._total_price


class VoucherCoupon(CouponBase):
    """
    无条件代金券
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

    def check_if_can_apply(self, order):
        self.calculate_total_price(order)
        return True

    def apply(self, order):
        if self.check_if_can_apply(order):
            need_to_pay = self._total_price - self.voucher
            if need_to_pay < 0:
                return 0
            else:
                return need_to_pay
        else:
            return self._total_price


all_coupons = [FullReduceCoupon('满200减50券', 200, 50),
               PercentReduceCoupon('9折券', 0.1),
               VoucherCoupon('10元代金券', 10),
               FullPercentReduceCoupon('满100打8折券', 100, 0.2)]
