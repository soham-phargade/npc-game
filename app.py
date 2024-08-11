from flask import Flask, request, render_template, session
from backend import Game

def flask_input():
    if request.method == 'POST':
        return request.form['input_text']

def flask_output(output):
    global history
    history.append({'input': "", 'output': output})
    

app = Flask(__name__)
app.secret_key = 'secret_key'
history = []
game = Game(3, flask_input, flask_output)
game.round_start()
user_index = game.player_imposter_index


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'round' not in session:
        session['round'] = 1
        game.round_start()

    if 'next_speaker' not in session:
        session['next_speaker'] = game.player_imposter_index

    # If a POST request is received, process the user input
    if request.method == 'POST':
        game.response(session['next_speaker'])

        # Determine the next speaker
        session['next_speaker'] = game.determine_next_speaker()

    #     # Check if the round should continue or move to elimination
    #     if len(history) >= 5:  # 5 responses per round
    #         if game.elimination_voting() == False:
    #             session.pop('round', None)
    #             session.pop('next_speaker', None)
    #             return render_template('index.html', history=history, message="Game Over")
    #         session['round'] += 1
    #         game.round_start()

    # Render the template with the updated history
    return render_template('index.html', 
                           user_index=user_index, 
                           history=history,
                           participants=game.participants.keys())



if __name__ == '__main__':
    app.run(debug=True)
