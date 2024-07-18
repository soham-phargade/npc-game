from game_engine.feature_module import gemini_api
from game_engine.feature_module.gemini_api import gemini
  
class Game:
    def __init__(self):
        self.convo_history = []
        self.npcs = 0
        self.participants = [{"id": 0, "priority_score": 1, "last_spoken": 0}] #id 0 is user

    def welcome_message(self):
        print("Welcome to multi AI convo")
        print("How many Robots do you want to talk to?")
    
    def response(self, id, convo_history):
        if id != 0:
            prompt = f"You are Robot {id}. Based on the provided chat history, respond briefly."
            response = gemini(prompt, convo_history)
            self.convo_history.append({"role": f"model", "parts": [f"Robot {id}: {response}"]})
            print(f"Robot {id}: {response}")
        else:
            user_message = input("You: ").strip()
            self.convo_history.append({"role": "user", "parts": [user_message]})
        return
    
    def initialize_participants(self):
        for id in range(1, self.npcs + 1):
            self.participants.append({"id": id, "priority_score": 0, "last_spoken": 0})
        
    def calculate_priority_score(self, participant, convo_history):
        import random
        relevance_score = random.random()  # Placeholder 
        return relevance_score
    
    def determine_next_speaker(self):
        import random
        next_speaker = random.randint(0,self.npcs)
        return next_speaker
        #Placeholder
        '''
        max_score = -1
        next_speaker_index = -1
        
        for i, participant in enumerate(self.participants):
            participant["priority_score"] = self.calculate_priority_score(participant, self.convo_history)
            if participant["priority_score"] > max_score:
                max_score = participant["priority_score"]
                next_speaker_index = i

        self.participants[next_speaker_index]["last_spoken"] = len(self.convo_history)
        return self.participants[next_speaker_index]
        '''

def main():
    game = Game()
    game.welcome_message()
    game.npcs = int(input())
    game.initialize_participants()

    next_speaker = 0

    while True:
        game.response(next_speaker, game.convo_history)
        next_speaker = game.determine_next_speaker()
        
if __name__ == "__main__":
    main()