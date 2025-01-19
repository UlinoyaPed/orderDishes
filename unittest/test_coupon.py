import unittest

from coupon import FullPercentReduceCoupon
from dishes import *

order1 = {burger: 3, donut: 2, pizza: 5}
order1_price = burger.price * 3 + donut.price * 2 + pizza.price * 5

order2 = {burger: 1}
order2_price = burger.price * 1


class TestFullPercentReduceCoupon(unittest.TestCase):

    def setUp(self):
        # 创建一个满减折扣券实例
        self.coupon = FullPercentReduceCoupon('满减券', 100, 0.2)

    def test_init(self):
        # 测试初始化时参数的正确性
        self.assertEqual(self.coupon.name, '满减券')
        self.assertEqual(self.coupon.full, 100)
        self.assertEqual(self.coupon.percent, 0.2)

    def test_check_if_can_apply(self):
        # 测试订单总价满足满减条件时的情况

        self.assertTrue(self.coupon.check_if_can_apply(order1))

        # 测试订单总价不满足满减条件时的情况
        self.assertFalse(self.coupon.check_if_can_apply(order2))

    def test_apply(self):
        # 测试订单总价满足满减条件时的折扣计算
        discounted_price = self.coupon.apply(order1)
        self.assertEqual(0.8 * order1_price, discounted_price)

        # 测试订单总价不满足满减条件时的原价返回
        original_price = self.coupon.apply(order2)
        self.assertEqual(order2_price, original_price)


if __name__ == '__main__':
    unittest.main()
