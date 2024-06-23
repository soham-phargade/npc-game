from ursina import *

app = Ursina()

EditorCamera()
sky = Sky()

maze = Entity(model='made', texture='brick')

app.run()