import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

import mainWindow

if __name__ == '__main__':
    # 高DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 启动
    translator = FluentTranslator()
    app = QApplication(sys.argv)
    app.installTranslator(translator)
    w = mainWindow.MainWindow()
    w.show()
    app.exec()
