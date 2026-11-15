import json
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QDialog, QMessageBox


player_name = ''

with open('replicas.json', 'r', encoding='utf-8') as f:
    REPLICAS = json.load(f)

with open('characters.json', 'r', encoding='utf-8') as f:
    CHARACTERS = json.load(f)

with open('health.json', 'r', encoding='utf-8') as f:
    HEALTH_STAGES = json.load(f)

with open('tasks.json', 'r', encoding='utf-8') as f:
    TASKS = json.load(f)


class HumanStatisticWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('human_statistic.ui', self)


class TextWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('text_window.ui', self)


class InfoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('info_window.ui', self)


class GameWindow(QWidget):
    def __init__(self, main_window=None, player_name=""):
        super().__init__()
        uic.loadUi('game_window.ui', self)
        print('Игра запущена!')

        self.player_name = player_name
        self.stage = "1"
        ###########################################
        self.current_stage.setText(self.stage)
        ###########################################
        
        self.main_menu = main_window

        self.statistic_window = HumanStatisticWindow(self)
        self.text_window = TextWindow(self)
        self.info_window = InfoWindow(self)

        self.btn_human_1.clicked.connect(self.human)
        self.btn_human_2.clicked.connect(self.human)
        self.btn_human_3.clicked.connect(self.human)
        self.btn_human_4.clicked.connect(self.human)

        self.btn_text_1.clicked.connect(self.message)
        self.btn_text_2.clicked.connect(self.message)
        self.btn_text_3.clicked.connect(self.message)
        self.btn_text_4.clicked.connect(self.message)

        self.btn_pause.clicked.connect(self.confirm_exit)
        self.btn_info.clicked.connect(self.information)

        self.text_window.btn_ans_1.clicked.connect(self.on_choice)
        self.text_window.btn_ans_2.clicked.connect(self.on_choice)
        self.text_window.btn_ans_1.setVisible(False)
        self.text_window.btn_ans_2.setVisible(False)

        self.about_text = self.statistic_window.about.text()
        self.health_text = self.statistic_window.health.text()
        self.info_text = self.info_window.info_text.text()

        self.health = {}
        self.apply_health_stages()

        self.update_tasks()

        self.information()

    def confirm_exit(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Выйти в главное меню?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.main_menu.show()
            self.hide()
            self.close_dialogs()

    def close_dialogs(self):
        if self.text_window.isVisible():
            self.text_window.close()
        if self.statistic_window.isVisible():
            self.statistic_window.close()

    def message(self):
        btn = self.sender()
        char_id = btn.objectName()[-1]

        stage_data = REPLICAS.get(self.stage, {})
        data = stage_data.get(char_id)
        if data is None:
            return

        self.text_window.btn_ans_1.setVisible(False)
        self.text_window.btn_ans_2.setVisible(False)

        self.text_window.setWindowTitle(f'Новое сообщение!')
        self.text_window.msg_from.setText(f'От: {CHARACTERS[char_id]["name"]}')
        self.text_window.msg.setText(data["text"])
        self.text_window.show()

        if data.get("choices") is not None:
            self.text_window.btn_ans_1.setText(data["choices"][0]["text"])
            self.text_window.btn_ans_2.setText(data["choices"][1]["text"])
            self.text_window.btn_ans_1.setVisible(True)
            self.text_window.btn_ans_2.setVisible(True)
            self.current_msg_btn = [btn, data]
        else:
            btn.hide()
            self.update_stage()

    def update_stage(self, next_stage=None):
        any_visible = any(
            getattr(self, f'btn_text_{i}').isVisible() for i in range(1, 5)
        )
        if next_stage:
            self.stage = next_stage
            self.show_buttons_for_stage()
            self.apply_health_stages()
            self.update_tasks()

            ###########################################
            self.current_stage.setText(self.stage)
            ###########################################
            
            return
        if not any_visible:
            self.stage = str(int(self.stage) + 1)
            self.show_buttons_for_stage()
            self.apply_health_stages()
            self.update_tasks()

        ###########################################
        self.current_stage.setText(self.stage)
        ###########################################

    def on_choice(self):
        self.text_window.btn_ans_1.setVisible(False)
        self.text_window.btn_ans_2.setVisible(False)

        btn_idx = int(self.sender().objectName()[-1]) - 1
        self.current_msg_btn[0].hide()
        next_stage = self.current_msg_btn[1]["choices"][btn_idx].get("next")
        self.text_window.close()
        self.update_stage(next_stage)

    def show_buttons_for_stage(self):
        stage_data = REPLICAS.get(self.stage, {})
        for i in range(1, 5):
            btn = getattr(self, f"btn_text_{i}")
            btn.setVisible(str(i) in stage_data)

    def information(self):
        self.info_window.setWindowTitle('Основная информация')

        change = self.info_text
        change = change.replace('{name}', self.player_name)
        self.info_window.info_text.setText(change)

        self.info_window.show()
        self.info_window.raise_()
        self.info_window.activateWindow()

    def human(self):
        title = f'Статистика'
        self.statistic_window.setWindowTitle(title)
        self.statistic_window.show()
        self.statistic_window.raise_()
        self.statistic_window.activateWindow()

        char_id = self.sender().objectName()[-1]

        # Основная Информация
        character = CHARACTERS[char_id]

        name = character["name"]
        age = character["age"]
        gender = character["gender"]
        bonus = character["bonus"]

        self.statistic_window.from_who.setText(name)

        changes = self.about_text
        changes = changes.replace('{age}', age)
        changes = changes.replace('{gender}', gender)
        changes = changes.replace('{bonus}', bonus)
        self.statistic_window.about.setText(changes)

        # Здоровье
        health = self.health.get(char_id, {})

        pulse = health.get("pulse", "-")
        pressure = health.get("pressure", "-")
        state = health.get("state", "-")

        changes = self.health_text
        changes = changes.replace('{pulse}', pulse)
        changes = changes.replace('{pressure}', pressure)
        changes = changes.replace('{state}', state)
        self.statistic_window.health.setText(changes)

    def apply_health_stages(self):
        change = HEALTH_STAGES.get(self.stage, {})
        for idx, changes in change.items():
            if idx not in self.health:
                self.health[idx] = {}
            self.health[idx].update(changes)

    def update_tasks(self):
        task = TASKS.get(self.stage, {})
        self.current_tasks_label.setText('\n'.join(task.get("tasks", "-")))