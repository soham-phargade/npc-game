from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# city_texture = load_texture('assets/obj/citybits_texture.png')

app = Ursina()

EditorCamera()
sky = Sky()

# player = FirstPersonController()

# wall = Entity(model='assets/stone_wall.fbx', texture='assets/stone_wall',scale=0.01, collider='mesh',position=(0, 0.5, 0), double_sided=True)
city = Entity(model='assets/obj/box_B', texture = 'assets/obj/citybits_texture.png')

app.run()