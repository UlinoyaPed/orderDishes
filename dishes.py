from PyQt5.QtGui import QIcon

from myIcons import MyIcon


class Dish:
    def __init__(self, name, price: float, icon: QIcon, unit='份', description=''):
        self.name = name
        self.price = price
        self.icon = icon
        self.description = description
        self.unit = unit


beer = Dish('啤酒', 5.78, MyIcon.Beer.icon(), '听')
burger = Dish('汉堡', 10.9, MyIcon.Burger.icon())
chips = Dish('薯条', 8.99, MyIcon.Chips.icon())
donut = Dish('甜甜圈', 3.5, MyIcon.Donut.icon())
ice_cream = Dish('冰淇淋', 6.99, MyIcon.IceCream.icon())
martini = Dish('马蒂尼', 4.5, MyIcon.Martini.icon(), '杯')
milk = Dish('牛奶', 3, MyIcon.Milk.icon(), '瓶')
noodles = Dish('面条', 12.66, MyIcon.Noodles.icon())
pizza = Dish('披萨', 15.88, MyIcon.Pizza.icon())

all_dishes = [burger, noodles, donut, ice_cream, chips, pizza, beer, martini, milk]
