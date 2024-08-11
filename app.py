from flask import Flask, request, render_template
from backend import Game

def flask_input():
    if request.method == 'POST':
        return request.form['input_text']

def flask_output(output):
    global history
    history.append({'input': "", 'output': output})
    

app = Flask(__name__)
players_remaining = "5"
history = []
game = Game(3, flask_input, flask_output)
game.round_start()
user_index = game.player_imposter_index


@app.route('/', methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':
        user_input = flask_input()
        if user_input:
            history.append({'input': user_input, 'output': user_input})

    return render_template('index.html', 
                           user_index=user_index, 
                           players_remaining=players_remaining, 
                           history=history,
                           participants=game.participants.keys())

if __name__ == '__main__':
    app.run(debug=True)
