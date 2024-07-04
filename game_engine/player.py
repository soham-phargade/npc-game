from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Player(FirstPersonController):
    def __init__(self, position=(0, 0, 0), **kwargs):
        super().__init__(**kwargs)
        self.spawn = position
        self.position = self.spawn  # Set position after initialization

    def update(self):
        super().update()  # Call the parent class update method

        self.camera_pivot.y = 2 - held_keys['left control']

        if self.y < -10:
            self.position = self.spawn
        
        if held_keys['left control']:
            self.speed = 1
        else:
            self.speed = 5

if __name__ == '__main__':
    app = Ursina()
    
    player = Player(position=(0, 5, 0))  # Set the initial position here

    Sky()
    ground = Entity(model='plane', scale=(100, 0, 100), texture='grass', collider='box')

    def input(key):
        if key == 'escape':
            application.quit()
        
    app.run()
