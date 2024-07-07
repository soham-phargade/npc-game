from ursina import *
from game_engine.npc import NPC
from game_engine.player import Player
from game_engine.feature_module.npc_game import NPCGame

if __name__ == '__main__':
    app = Ursina()
    player = Player(position=(10, 50, 10))
    npc_map = NPCGame()
    npc1 = NPC(player, npc_map, model = 'cube', position=(0, 1, 0), collider='box', name='NPC1')    
    
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
