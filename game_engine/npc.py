from ursina import *
import threading
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QDesktopWidget
from feature_module.gemini_api import gemini


class NPC(Entity):
    def __init__(self, player, position=(0, 0, 0), name="untitled", **kwargs):
        super().__init__(position=position, **kwargs)
        self.player = player
        self.name = name
        self.gravity = 0.1
        self.is_talking = False
        self.speech = Text('', origin=(0,17,0), color = color.black)
        
        self.dialogue_box = None

    def update(self):
        # Applies gravity to NPC
        ground_check = raycast(self.position + Vec3(0, 1, 0), Vec3(0, -1, 0), distance=2, ignore=[self])
        if ground_check.hit:
            self.y = ground_check.world_point.y + self.scale_y / 2
        else:
            self.y -= self.gravity
        
        if self.y < -10:
            self.y = 10

        # Change direction of NPC towards player
        direction = Vec3(self.player.x - self.x, 0, self.player.z - self.z).normalized()
        self.rotation_y = math.degrees(math.atan2(direction.x, direction.z))

        # Move NPC towards player
        if distance_xz(self.position, self.player.position) > 5:
            self.position += direction * 0.1
            self.speech.text = ''
            self.is_talking = False

        # Check for interaction
        if distance_xz(self.position, self.player.position) <= 2:
            if held_keys['e'] and not self.is_talking:
                self.speech.text = f'my name is {self.name}'
                self.is_talking = True
                
            if held_keys['left mouse'] and not self.is_talking:
                self.is_talking = True
                threading.Thread(target=self.get_response).start()
                
    def get_user_input(self):
        app = QApplication([])
        text_edit = QTextEdit()
        submit_button = QPushButton("Submit")
        cancel_button = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.addWidget(text_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        dialog = QDialog()
        dialog.setWindowTitle("Input Dialog")
        dialog.setGeometry(QDesktopWidget().availableGeometry().center().x() - 200,
                           QDesktopWidget().availableGeometry().center().y() - 150, 400, 300)
        dialog.setLayout(layout)

        def submit():
            dialog.user_input = text_edit.toPlainText()
            dialog.accept()

        submit_button.clicked.connect(submit)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            return dialog.user_input
        return None
    
    def get_response(self):
        response = self.get_user_input()
        if response:
            gemini_response = gemini(response)
            print(gemini_response)
            self.speech.text = gemini_response
            self.is_talking = True


if __name__ == '__main__':
    from player import Player
    app = Ursina()
    player = Player(position=(25, 100, 10))
    npc1 = NPC(player, model = 'cube', position=(0, 1, 0), collider='box', name='NPC1')    
    
    # box = Entity(model='cube', scale=(1, 1, 1), position=(0, 1, 0), collider='box')
    # text = Text(text='hi', parent=box, position=(0,1.5,0), origin=(0, 0), background=True, color=color.black, scale=10)

    Sky()
    
    ground = Entity(model='plane', scale=(100, -1, 100), texture='grass', collider='box')

    # Adding slopes
    slope1 = Entity(model='plane', scale=(10, 1, 10), rotation=(45, 0, 0), position=(10, 0, 0), texture='grass', collider='box')
    slope2 = Entity(model='plane', scale=(10, 1, 10), rotation=(0, 0, 45), position=(20, 0, 20), texture='grass', collider='box')

    def input(key):
        if key == 'escape':
            application.quit()
            
    def update():
        player.update()
            
    app.run()