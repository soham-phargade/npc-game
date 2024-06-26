from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# EditorCamera()
sky = Sky()

player = FirstPersonController()

floor = Entity(model='plane', scale=(100, 0, 100), texture='grass', collider='box')
maze = Entity(model='made',scale=10,texture='brick',position=(0,0.1,0), collider='mesh')

app.run()