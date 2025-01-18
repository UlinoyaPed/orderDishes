from enum import Enum

from PyQt5.QtGui import QIcon


class MyIcon(Enum):
    """ Custom icons """

    Beer = "Beer.svg"
    Burger = "Burger.svg"
    Chips = "Chips.svg"
    Donut = "Donut.svg"
    IceCream = "IceCream.svg"
    Martini = "Martini.svg"
    Milk = "Milk.svg"
    Noodles = "Noodles.svg"
    Pizza = "Pizza.svg"

    def icon(self) -> QIcon:
        return QIcon(f'./assets/icons/{self.value}')
