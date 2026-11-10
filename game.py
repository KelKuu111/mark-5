import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QDialog, QMessageBox


class HumanStatisticWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('human_statistic.ui', self)


class TextWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('text_window.ui', self)


class GameWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        uic.loadUi('game_window.ui', self)
        print('Игра запущена!')

        self.main_menu = main_window

        self.statistic_window = HumanStatisticWindow(self)
        self.text_window = TextWindow(self)

        self.btn_human_1.clicked.connect(self.human)
        self.btn_human_2.clicked.connect(self.human)
        self.btn_human_3.clicked.connect(self.human)
        self.btn_human_4.clicked.connect(self.human)

        self.btn_message_1.clicked.connect(self.message)
        self.btn_message_2.clicked.connect(self.message)
        self.btn_message_3.clicked.connect(self.message)
        self.btn_message_4.clicked.connect(self.message)

        self.btn_pause.clicked.connect(self.confirm_exit)

    def confirm_exit(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Выйти в главное меню?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.hide()
            self.close_dialogs()
            self.main_menu.show()

    def close_dialogs(self):
        if self.text_window.isVisible():
            self.text_window.close()
        if self.statistic_window.isVisible():
            self.statistic_window.close()

    def message(self):
        title = f'Сообщение от {self.sender().objectName()[-1]}'
        self.text_window.setWindowTitle(title)
        self.text_window.show()

    def human(self):
        title = f'Статистика {self.sender().objectName()[-1]}'
        self.statistic_window.setWindowTitle(title)
        self.statistic_window.show()
        self.statistic_window.raise_()
        self.statistic_window.activateWindow()

    