from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

sky = Sky(texture='night_sky', scale=(10, 10), texture_scale=(10, 10))

floor = Entity(model='plane', position=(0,-5,0), scale=(10, 1, 10), texture='white_cube', collider='box', texture_scale=(10, 10))

player = FirstPersonController(position=(0, 0, 0))

cube = Entity(model='cube', position=(0, -4.5, 0), scale=(1, 1, 1), color=color.red)

timer = Text(text='0', position=(0, 0, 0), color=color.black, scale=10, double_sided=True, parent=cube, billboard=True, origin=(0, 0))

def update():
    timer.text = str(int(timer.text) + 1)

app.run()   