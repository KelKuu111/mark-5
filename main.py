import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QGraphicsOpacityEffect
from game import GameWindow


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.btn_settings_exit.clicked.connect(self.hide)


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_menu.ui', self)

        self.btn_play.clicked.connect(self.start_game)
        self.btn_settings.clicked.connect(self.settings)
        self.btn_exit.clicked.connect(self.exit)

        self.settings_window = SettingsWindow()

    def start_game(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.hide()

    def settings(self):
        print('Вход в настройки')
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def exit(self):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec())