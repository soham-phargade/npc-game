from flask import Flask, request, render_template
from backend import Game

def flask_input():
    while True:
        if request.method == 'POST':
            return request.form['input_text']

def flask_output(output):
    global history
    history.append({'input': "", 'output': output})
    

app = Flask(__name__)
history = []
game = Game(3, flask_input, flask_output)
game.round_start()
user_index = game.player_imposter_index


@app.route('/', methods=['GET', 'POST'])
async def index():
    next_speaker = game.player_imposter_index
    game.response(next_speaker, game.convo_history)
    next_speaker = game.determine_next_speaker()
    game.response(next_speaker, game.convo_history)
    
    if request.method == 'POST':
        user_input = flask_input()
        if user_input:
            history.append({'input': user_input, 'output': user_input})

    return render_template('index.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
