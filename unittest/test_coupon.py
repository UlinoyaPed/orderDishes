import unittest

from coupon import FullPercentReduceCoupon
from dishes import *

test_dish = Dish('测试菜品', 10, QIcon())


def create_order(dish, num):
    order = {dish: num}
    return order



class TestFullPercentReduceCoupon(unittest.TestCase):

    def setUp(self):
        # 创建一个满减折扣券实例
        self.coupon = FullPercentReduceCoupon('满减券，最多减20', 100, 0.2, 20)

    def test_check_if_can_apply(self):
        # 测试订单总价满足满减条件时的情况

        self.assertTrue(self.coupon.check_if_can_apply(create_order(test_dish, 100)))

        # 测试订单总价不满足满减条件时的情况
        self.assertFalse(self.coupon.check_if_can_apply(create_order(test_dish, 5)))

    def test_apply(self):
        # 测试订单总价满足满减条件时的折扣计算
        discounted_price = self.coupon.apply(create_order(test_dish, 100))
        self.assertEqual(100 * 10 - 20, discounted_price)

        # 测试订单总价不满足满减条件时的原价返回
        original_price = self.coupon.apply(create_order(test_dish, 5))
        self.assertEqual(5 * 10, original_price)

        # 测试未达到最大优惠金额
        discounted_price = self.coupon.apply(create_order(test_dish, 10))
        self.assertEqual(10 * 10 * 0.8, discounted_price)


if __name__ == '__main__':
    unittest.main()
