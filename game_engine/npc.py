from ursina import *
from player import Player

class NPC(Entity):
    def __init__(self, position=(0, 0, 0), **kwargs):
        super().__init__(**kwargs)

    def update(self):
        pass
    


if __name__ == '__main__':
    app = Ursina()
    player = Player()
    npc1 = NPC(model='cube', position=(0, 10, 0), Collider='box')

    Sky()
    
    ground = Entity(model='plane', scale=(100, 0, 100), texture='grass', collider='box')

    
    def input(key):
        if key == 'escape':
            application.quit()
            
    def update():
        
        if distance_xz(player.position, npc1.position) > 5:
            npc1.look_at(player)
            npc1.position += (player.position - npc1.position).normalized() * 0.1
        
        
    app.run()
