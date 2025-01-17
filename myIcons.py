from enum import Enum

from PyQt5.QtGui import QIcon


class MyIcon(Enum):
    """ Custom icons """

    Noodles = "Noodles.svg"
    Burger = "Burger.svg"

    def icon(self) -> QIcon:
        return QIcon(f'./assets/icons/{self.value}')
