from game_engine.feature_module import gemini_api
#from t2 import Game
from game_engine.feature_module.gemini_api import gemini

class Game:
    def __init__(self):
        self.convo = []
        self.npcs = 0

    def welcome_message(self):
        print("Welcome to multi AI convo")
        print("How many Robots do you want to talk to?")
    
    def response(self, id, convo_history):
        prompt = f"You are Robot {id}. Based on the provided chat history, respond briefly."
        response = gemini(prompt, convo_history)
        return response

def main():
    game = Game()
    game.welcome_message()
    game.npcs = int(input())
    while True:
        user_message = input("You: ").strip()
        game.convo.append({"role": "user", "parts": [user_message]})
        for id in range(1, game.npcs + 1):
            response = game.response(id, game.convo)
            game.convo.append({"role": f"model", "parts": [f"Robot {id}: {response}"]})
            print(f"Robot {id}: {response}")

if __name__ == "__main__":
    main()
