from flask import Flask, request, render_template
from backend import Game

app = Flask(__name__)

history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    #if request.method == 'GET':
        #game = Game(4)
        #return Game.round_start()
    if request.method == 'POST':
        user_input = request.form['input_text']
        output = your_python_function(user_input)
        history.append({'input': user_input, 'output': output})
    return render_template('index.html', history=history)

def your_python_function(input_text):
    # Your existing logic here
    return "Processed: " + input_text

def game_loop():
    game = Game(3)
    
    
    return game.round_start()

if __name__ == '__main__':
    app.run(debug=True)