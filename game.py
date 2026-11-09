import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QDialog


class HumanStatisticWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('human_statistic.ui', self)


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('game_window.ui', self)
        print('Игра запущена!')

        self.statistic_window = HumanStatisticWindow(self)

        self.btn_human_1.clicked.connect(self.human)
        self.btn_human_2.clicked.connect(self.human)
        self.btn_human_3.clicked.connect(self.human)
        self.btn_human_4.clicked.connect(self.human)

    def human(self):
        title = f'Статистика {self.sender().objectName()[-1]}'
        self.statistic_window.setWindowTitle(title)
        self.statistic_window.show()
        self.statistic_window.raise_()
        self.statistic_window.activateWindow()

    