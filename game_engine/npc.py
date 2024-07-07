from ursina import *
import threading
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QDesktopWidget

if __name__ == '__main__':
    from feature_module.npc_game import NPCGame
    from player import Player
    
else:
    from .feature_module.npc_game import NPCGame

class NPC(Entity):
    def __init__(self, player, npc_map, position=(0, 0, 0), name="untitled", **kwargs):
        super().__init__(position=position, **kwargs)
        self.player = player
        self.name = name
        self.npc_map = npc_map
        self.gravity = 0.1
        self.is_talking = False
        self.speech = Text('', origin=(0, 17, 0), color=color.black)
        self.dialogue_box = None
        self.npc_map.add_npc(self.name)
        self.velocity = Vec3(0, 0, 0)  # Initialize velocity

    def update(self):
        # Applies gravity while ignoring other NPCs
        other_npcs = [npc for npc in scene.entities if isinstance(npc, NPC) and npc is not self]
        ground_check = raycast(self.position + Vec3(0, 1, 0), Vec3(0, -1, 0), distance=2, ignore=[self] + other_npcs)
        if ground_check.hit:
            self.y = ground_check.world_point.y + self.scale_y / 2
        else:
            self.y -= self.gravity

        # Collision avoidance with predictive movement and damping
        avoidance_force = Vec3(0, 0, 0)
        for npc in other_npcs:
            future_position = npc.position + npc.velocity * 0.1  # Predict future position
            distance_to_npc = distance_xz(self.position, future_position)
            if distance_to_npc < 2:  # Adjust the avoidance radius as needed
                repulsion = (self.position - future_position).normalized() / (distance_to_npc**2)
                avoidance_force += repulsion

        # Smooth the avoidance force
        avoidance_force = avoidance_force * 0.5

        # Change direction of NPC towards player
        direction = Vec3(self.player.x - self.x, 0, self.player.z - self.z).normalized()
        self.rotation_y = math.degrees(math.atan2(direction.x, direction.z))

        # Combine movement direction with avoidance force
        movement = direction * 0.1 + avoidance_force

        # Update velocity with damping
        damping_factor = 0.9  # Adjust damping factor as needed
        self.velocity = (self.velocity + movement).normalized() * 0.1
        self.velocity *= damping_factor

        # Move NPC towards player while avoiding other NPCs
        if distance_xz(self.position, self.player.position) > 5:
            self.position += self.velocity
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

    app = Ursina()
    player = Player(position=(10, 25, 10))
    npc_map = NPCGame()
    npc1 = NPC(player, npc_map, model = 'cube', position=(-5, 1, 0), collider='box', name='NPC1')    
    npc2 = NPC(player, npc_map, model = 'cube', position=(5, 1, 0), collider='box', name='NPC2')    
    
    
    # box = Entity(model='cube', scale=(1, 1, 1), position=(0, 1, 0), collider='box')
    # text = Text(text='hi', parent=box, position=(0,1.5,0), origin=(0, 0), background=True, color=color.black, scale=10)
    
    Sky()
    
    ground = Entity(model='plane', scale=(100, -1, 100), texture='grass', collider='box')

    # Adding slopes
    slope1 = Entity(model='plane', scale=(10, 1, 10), rotation=(45, 0, 0), 
                    position=(10, 0, 0), texture='grass', double_sided=True, collider='box')

    def input(key):
        if key == 'escape':
            application.quit()
    
    app.run()