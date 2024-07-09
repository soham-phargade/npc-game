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
