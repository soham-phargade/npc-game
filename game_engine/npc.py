from ursina import *
import threading
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QDesktopWidget
from feature_module.gemini_api import gemini
from feature_module.npc_game import NPCGame


class NPC(Entity):
    def __init__(self, player, npc_map, position=(0, 0, 0), name="untitled", **kwargs):
        super().__init__(position=position, **kwargs)
        self.player = player
        self.name = name
        self.npc_map = npc_map
        self.gravity = 0.1
        self.is_talking = False
        self.speech = Text('', origin=(0,17,0), color = color.black)
        self.dialogue_box = None
        self.npc_map.add_npc(self.name)

    def update(self):
        # Applies gravity to NPC
        ground_check = raycast(self.position + Vec3(0, 1, 0), Vec3(0, -1, 0), distance=2, ignore=[self])
        if ground_check.hit:
            self.y = ground_check.world_point.y + self.scale_y / 2
        else:
            self.y -= self.gravity

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
        # Check if QApplication instance exists
        app = QApplication.instance()
        app_created = False
        if app is None:
            app = QApplication([])
            app_created = True

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

        user_input = None
        if dialog.exec_() == QDialog.Accepted:
            user_input = dialog.user_input

        if app_created:
            app.quit()

        return user_input
    
    def get_response(self):
        # take input from box and generate gemini response
        response = self.get_user_input()
        
        print(self.npc_map.npcs)
        
        if response:
            gemini_response = self.npc_map.interact_with_npc(self.name, response)
            print(gemini_response)
            self.speech.text = gemini_response
            self.is_talking = True


if __name__ == '__main__':
    from player import Player
    app = Ursina()
    
    npc_map = NPCGame()
    
    player = Player(position=(25, 50, 25))
        
    npc1 = NPC(player, npc_map, model = 'cube', position=(-10, 1, -10), collider='box', name='NPC1')
    # npc2 = NPC(player, npc_map, model = 'cube', position=(10, 1, 10), collider='box', name='NPC2')   

    print(npc_map.get_available_npcs())
    
    # box = Entity(model='cube', scale=(1, 1, 1), position=(0, 1, 0), collider='box')
    # text = Text(text='hi', parent=box, position=(0,1.5,0), origin=(0, 0), background=True, color=color.black, scale=10)

    Sky()
    
    ground = Entity(model='plane', scale=(100, -10, 100), texture='grass', collider='box')

    # Adding slopes
    slope1 = Entity(model='plane', scale=(10, 1, 10), rotation=(45, 0, 0), position=(10, 0, 0), texture='grass', collider='box')
    slope2 = Entity(model='plane', scale=(10, 1, 10), rotation=(0, 0, 45), position=(20, 0, 20), texture='grass', collider='box')

    def input(key):
        if key == 'escape':
            application.quit()
            
    def update():
        player.update()
            
    app.run()