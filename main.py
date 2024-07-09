from game_engine.feature_module import gemini_api
from t2 import Game

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
