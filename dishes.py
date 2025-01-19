"""
    所有菜品
"""

from PyQt5.QtGui import QIcon

from myIcons import MyIcon


class Dish:
    def __init__(self, name, price: float, icon: QIcon, unit='份', description=''):
        self.name = name
        self.price = price
        self.icon = icon
        self.description = description
        self.unit = unit


beer = Dish('啤酒', 5.78, MyIcon.Beer.icon(), '听', '精酿小麦果汁\n不保证不挨处分')
burger = Dish('汉堡', 20, MyIcon.Burger.icon(), description='经典汉堡')
chips = Dish('薯条', 9.5, MyIcon.Chips.icon())
donut = Dish('甜甜圈', 3.5, MyIcon.Donut.icon(), '个')
ice_cream = Dish('冰淇淋', 13.5, MyIcon.IceCream.icon())
martini = Dish('马蒂尼', 4.5, MyIcon.Martini.icon(), '杯', '其实我也不知道这是什么\n网上找的图标文件名叫Martini')
milk = Dish('牛奶', 3, MyIcon.Milk.icon(), '瓶', '(防御 +2)')
noodles = Dish('面条', 12.66, MyIcon.Noodles.icon(), '碗')
pizza = Dish('披萨', 15.88, MyIcon.Pizza.icon())

all_dishes = [burger, noodles, pizza, chips, donut, ice_cream, beer, martini, milk]
