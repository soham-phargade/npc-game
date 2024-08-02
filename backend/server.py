from flask import Flask, request, jsonify
from flask_cors import CORS
from main import Game

app = Flask(__name__)
CORS(app)

game = None

@app.route('/start_game', methods=['POST'])
def start_game():
    global game
    data = request.json
    npc_count = data.get('npc_count', 3)
    game = Game(npc_count)
    game.initialize_participants()
    return jsonify({
        'message': 'Guess the imposter \nAIs vs one Human edition',
        'player_imposter_index': game.player_imposter_index
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    global game
    data = request.json
    player_id = data.get('id')
    message = data.get('message')
    print(f"Received message: {message} from player {player_id}")  # Debug log
    game.response(player_id, game.convo_history)
    response = game.convo_history[-1]['parts'][0]
    print(f"Sending response: {response}")  # Debug log
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
