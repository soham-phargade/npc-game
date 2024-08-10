from flask import Flask, request, render_template
from backend import Game

def flask_input():
    if request.method == 'POST':
        return request.form['input_text']
    return None

def flask_output(output):
    global history
    history.append({'input': "", 'output': output})

app = Flask(__name__)
history = []
game = Game(3, flask_output)
flask_output(game.round_start())
user_index = game.player_imposter_index

def start_elimination(user_vote):
    # Pass the user_vote directly to the game's elimination_voting method
    result = game.elimination_voting(user_vote)
    print(result)
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = flask_input()
        if user_input:
            output = start_elimination(int(user_input))
            history.append({'input': user_input, 'output': output})

    return render_template('index.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)
