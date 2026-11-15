import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
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

        self.game_window = None

        self.btn_play.clicked.connect(self.start_game)
        self.btn_settings.clicked.connect(self.settings)
        self.btn_exit.clicked.connect(self.exit)

        self.settings_window = SettingsWindow()

    def start_game(self):
        player_name = self.settings_window.edit_name.text()

        if not player_name:
            QMessageBox.warning(
                self,
                "Имя не введено",
                "Пожалуйста, введите имя персонажа в настройках, "
                "прежде чем начинать игру."
            )
            self.settings()
            self.settings_window.edit_name.setFocus()
            return

        if self.game_window is None:
            self.game_window = GameWindow(self, player_name=player_name)
        self.game_window.player_name = player_name
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