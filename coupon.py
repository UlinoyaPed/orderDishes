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

        self.has_max_reduce: bool = False  # 是否有最大优惠金额
        self.max_reduce: float = 0  # 最大优惠金额

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

    def __init__(self, name, off_percent: float, max_reduce: float = 0):
        """
        初始化折扣券
        注意填的是折扣比例，比如打八折填0.2
        :param name: 名称
        :param off_percent: 折扣比例 0-1
        """
        super().__init__(name)
        if off_percent > 1:
            raise ValueError('percent must be less than 1')
        elif off_percent < 0:
            raise ValueError('percent must be greater than 0')
        self.percent = off_percent

        # 最大优惠金额
        if max_reduce == 0:
            self.has_max_reduce = False
        elif max_reduce < 0:
            raise ValueError('max_reduce must be greater than 0')
        else:
            self.has_max_reduce = True
        self.max_reduce = max_reduce

    def check_if_can_apply(self, order):
        self.calculate_total_price(order)
        return True

    def apply(self, order):
        if self.check_if_can_apply(order):
            if self.has_max_reduce:  # 如果有最大优惠金额
                if self._total_price * self.percent > self.max_reduce:
                    return self._total_price - self.max_reduce  # 超过最大优惠金额
                else:
                    return self._total_price * (1 - self.percent)
            else:  # 没有最大优惠金额
                return self._total_price * (1 - self.percent)
        else:
            return self._total_price


class FullPercentReduceCoupon(PercentReduceCoupon):
    """
    满减折扣券 满多少才打折扣
    """

    def __init__(self, name, full: float, off_percent: float, max_reduce: float = 0):
        """
        初始化满减折扣券
        注意填的是折扣比例，比如打八折填0.2
        :param name: 名称
        :param full: 满多少元
        :param off_percent: 折扣比例 0-1
        """
        super().__init__(name, off_percent, max_reduce)
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
            if self.has_max_reduce:  # 如果有最大优惠金额
                if self._total_price * self.percent > self.max_reduce:
                    return self._total_price - self.max_reduce  # 超过最大优惠金额
                else:
                    return self._total_price * (1 - self.percent)
            else:
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


all_coupons = [
    VoucherCoupon('10元代金券', 10),
    FullReduceCoupon('满200减50券', 200, 50),
    PercentReduceCoupon('9折券', 0.1),
    PercentReduceCoupon('6折券，最多减20', 0.4, 20),
    FullPercentReduceCoupon('满100打8折券，最多减30', 100, 0.2, 30),
]
