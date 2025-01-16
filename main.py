import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import MainWindow

if __name__ == '__main__':
    # 高DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 启动
    app = QApplication(sys.argv)
    w = MainWindow.MainWindow()
    w.show()
    app.exec()
