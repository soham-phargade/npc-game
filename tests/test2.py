from ursina import *

app = Ursina()

# Basic setup
window.title = 'Reverse Turing Test Game Demo'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Player setup
player = Entity(model='cube', color=color.orange, scale_y=2)

# NPC setup
npc = Entity(model='cube', color=color.azure, scale_y=2, position=(2, 0, 0))

# Dialogue Text
dialogue_text = Text(text='', position=(-0.85, 0.4), origin=(0, 0), scale=2, color=color.white)

# Trust Meter
trust_meter = Entity(model='cube', color=color.red, position=(-0.7, 0.3), scale=(0.1, 0.02, 1))
trust_level = 50

app.run()
