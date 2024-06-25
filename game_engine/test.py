from ursina import *

class DynamicWrapInput(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.input_text = ''
        self.max_chars_per_line = 20  # Maximum characters per line
        self.scale_factor = 0.5  # Scale factor for text size
        self.text_entity = Text(parent=self, text='', origin=(-.5, .5), scale=(self.scale_factor, self.scale_factor))
        self.update_text()

    def on_key_press(self, key):
        if key == '\x08':  # Handle backspace
            self.input_text = self.input_text[:-1]
        elif key.isprintable():
            self.input_text += key
        self.update_text()

    def update_text(self):
        # Split text into lines based on maximum characters per line
        lines = [self.input_text[i:i+self.max_chars_per_line] for i in range(0, len(self.input_text), self.max_chars_per_line)]
        # Join lines with '\n' to simulate text wrapping
        wrapped_text = '\n'.join(lines)
        self.text_entity.text = wrapped_text
        # Calculate number of lines
        num_lines = len(lines)
        # Adjust scale_y to fit number of lines
        self.text_entity.scale_y = num_lines * self.scale_factor

app = Ursina()

dynamic_input = DynamicWrapInput(scale=(0.5, 0.5), position=(0, 0), parent=scene)

def update():
    pass

def input(key):
    if key == 'escape':
        application.quit()

app.run()
