from flask import Flask, request, render_template
from backend import Game

def flask_input():
    if request.method == 'POST':
        return request.form['input_text']

def flask_output(output):
    global history
    history.append({'input': "", 'output': output})
    

app = Flask(__name__)
history = []
game = Game(7, flask_input, flask_output)
#game.round_start()
game.elimination_voting()
user_index = game.player_imposter_index
number_of_players = len(game.participants.keys())


@app.route('/', methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':
        user_input = flask_input()
        if user_input:
            history.append({'input': user_input, 'output': user_input})

    return render_template('index.html', 
                           user_index=user_index, 
                           history=history,
                           number_of_players=number_of_players,
                           participants=game.participants.keys())

if __name__ == '__main__':
    app.run(debug=True)
