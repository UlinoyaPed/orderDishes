from PyQt5.QtGui import QIcon

from myIcons import MyIcon


class Dish:
    def __init__(self, name, price: float, icon: QIcon, description=''):
        self.name = name
        self.price = price
        self.icon = icon
        self.description = description


burger = Dish('汉堡', 10.99, MyIcon.Burger.icon())
noodles = Dish('面条', 12.99, MyIcon.Noodles.icon())
