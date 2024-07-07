from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# EditorCamera()
sky = Sky()

player = FirstPersonController()

floor = Entity(model='plane', scale=(100, 0, 100), texture='grass', collider='box')
maze = Entity(model='cottage', texture="brick", scale=1,position=(0,0.1,0), double_sided=True)

app.run()