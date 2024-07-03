import threading
from ursina import *
import time

app = Ursina()

def input(key):
    if key == 'escape':
        application.quit()

def pause():
    for i in range(5):
        print(i)
        time.sleep(2)
    print('Done')

class Player(Entity):
    
    def __init__(self):
        
        self.work = False
        
        
        super().__init__(
            model='cube',
            color=color.orange,
            scale=(1, 1, 1),
            position=(0, 0.5, 0)
        )

    def update(self):
        speed = 4
        if held_keys['w']:
            self.position += self.forward * speed * time.dt
        if held_keys['s']:
            self.position -= self.forward * speed * time.dt
        if held_keys['a']:
            self.rotation_y -= 100 * time.dt
        if held_keys['d']:
            self.rotation_y += 100 * time.dt
        if held_keys['e'] and self.work == False:
            self.work = True
            threading.Thread(target=pause).start()
            

player = Player()

def update():
    player.update()

app.run()