import json
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QDialog, QMessageBox


with open('replicas.json', 'r', encoding='utf-8') as f:
    REPLICAS = json.load(f)


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

        self.stage = 1
        
        self.main_menu = main_window

        self.statistic_window = HumanStatisticWindow(self)
        self.text_window = TextWindow(self)

        self.btn_human_1.clicked.connect(self.human)
        self.btn_human_2.clicked.connect(self.human)
        self.btn_human_3.clicked.connect(self.human)
        self.btn_human_4.clicked.connect(self.human)

        self.btn_text_1.clicked.connect(self.message)
        self.btn_text_2.clicked.connect(self.message)
        self.btn_text_3.clicked.connect(self.message)
        self.btn_text_4.clicked.connect(self.message)

        self.btn_text_1.setVisible(True)
        self.btn_text_2.setVisible(False)
        self.btn_text_3.setVisible(True)
        self.btn_text_4.setVisible(False)

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
        btn = self.sender()
        char_id = btn.objectName()[-1]

        stage_data = REPLICAS.get(str(self.stage), {})
        data = stage_data.get(char_id)
        if data is None:
            return

        self.text_window.setWindowTitle(f'Новое сообщение!')
        self.text_window.msg_from.setText(f'Сообщение от {char_id}')
        self.text_window.msg.setText(data["text"])
        self.text_window.show()
        btn.hide()

        self.update_stage()

    def human(self):
        title = f'Статистика {self.sender().objectName()[-1]}'
        self.statistic_window.setWindowTitle(title)
        self.statistic_window.show()
        self.statistic_window.raise_()
        self.statistic_window.activateWindow()

    def update_stage(self):
        any_visible = any(
            getattr(self, f'btn_text_{i}').isVisible() for i in range(1, 5)
        )
        if not any_visible:
            self.stage += 1
            self.show_buttons_for_stage()

    def show_buttons_for_stage(self):
        stage_data = REPLICAS.get(str(self.stage), {})
        for i in range(1, 5):
            btn = getattr(self, f"btn_text_{i}")
            btn.setVisible(str(i) in stage_data)