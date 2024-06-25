from ursina import *
from player import Player

class NPC(Entity):
    def __init__(self, player, position=(0, 0, 0), name="untitled", **kwargs):
        super().__init__(position=position, **kwargs)
        self.player = player
        self.name = name
        self.gravity = 0.1
        
        self.dialogue_box = None
        self.is_talking = False

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

        # Check for interaction
        if distance_xz(self.position, self.player.position) <= 2:  # Interaction distance
            if held_keys['e'] and not self.is_talking:
                self.start_conversation()

    def start_conversation(self):
        self.is_talking = True
        self.dialogue_box = Text(text="Type something and press Enter:", position=(-0.5, -0.3), origin=(0,0), background=True, scale=1.5)
        self.text_input = InputField(scale=(1, 0.1), character_limit=250, text='', active=True)
        self.text_input.active = True


if __name__ == '__main__':
    app = Ursina()
    player = Player()
    npc1 = NPC(player, model='cube', position=(0, 10, 0), collider='box', name='NPC1')

    Sky()
    
    ground = Entity(model='plane', scale=(100, 0, 100), texture='grass', collider='box')

    # Adding slopes
    slope1 = Entity(model='plane', scale=(10, 1, 10), rotation=(45, 0, 0), position=(10, 0, 0), texture='grass', collider='box')
    slope2 = Entity(model='plane', scale=(10, 1, 10), rotation=(0, 0, 45), position=(20, 0, 20), texture='grass', collider='box')

    def input(key):
        if key == 'escape':
            application.quit()
            
    app.run()
