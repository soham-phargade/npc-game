from game_engine.feature_module import gemini_api
from game_engine.feature_module.gemini_api import gemini
import random

class Participant:
    def __init__(self, id, priority_score=0):
        self.id = id
        self.priority_score = priority_score

    def __str__(self):
        return f"Robot {self.id}"

    def __repr__(self):
        return f"Robot {self.id}"
  
class Game:
    def __init__(self):
        self.convo_history = []
        self.participants = []
        self.votes = []
        self.npcs = 0
        self.round = 0

    def welcome_message(self):
        print("Guess the imposter \n AIs vs one Human edition")
        while True:
            try:
                self.npcs = int(input("How many participants would you like (at least 3)? "))
                if self.npcs >= 3:
                    self.player_imposter_index = random.randint(1, self.npcs)
                    print(f"You are Robot {self.player_imposter_index}, an imposter!")
                    self.initialize_participants()
                    break
                else:
                    print("Please enter a number greater than or equal to 3.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def initialize_participants(self):
        print("Creating a game...")
        for id in range(1, self.npcs + 1):
            self.participants.append(Participant(id, 0))
        votes = [0]*(self.npcs+1)

    def round_start(self):
        self.round+=1
        print(f"This is round {self.round} \nThere are {self.npcs} robots remaining")
    
    def elimination_voting(self):
    # Reset votes
        self.votes[:] = [0] * (self.npcs + 1)  # Ensure votes list matches the number of participants
        print(f"Alright, that's the end of round {self.round}. Please vote who you think is the imposter")

    # Collect votes
        for participant in self.participants:
            if participant.id != self.player_imposter_index:
            # Prompt generation and voting logic
            # prompt = f"You are Robot {participant['id']}. Based on the provided chat history, respond only with the integer index of robot who you think is the imposter."
            # vote = gemini(prompt, self.convo_history)
                vote = random.randint(1, self.npcs)
                print(f"Robot {participant.id}: {vote}")
            else:
                vote = int(input(f"Robot {self.player_imposter_index} (You): ").strip())

        # Ensure the vote is within valid range
            if 0 < vote <= self.npcs:
                self.votes[vote] += 1

    # Determine and eliminate the participant with the most votes
        if any(self.votes):
            eliminated_id = self.votes.index(max(self.votes))
            self.participants = [p for p in self.participants if p.id != eliminated_id]
            self.npcs -= 1
            print(f"Robot {eliminated_id} has been eliminated")
        else:
            print("No valid votes received. No one is eliminated this round.")

        print("Remaining Participants:", self.participants)
    
    def response(self, id, convo_history):
        if id != self.player_imposter_index:
            prompt = f"You are Robot {id}. Based on the provided chat history, respond briefly. Avoid including the speaker's name in the response"
            response = gemini(prompt, convo_history)
            self.convo_history.append({"role": "model", "parts": [f"Robot {id}: {response}"]})
            print(f"Robot {id}: {response}")
        else:
            user_message = input(f"Robot {self.player_imposter_index} (You): ").strip()
            #self.convo_history.append({"role": "user", "parts": [user_message]})
            self.convo_history.append({"role": "model", "parts": [f"Robot {id}: {user_message}"]})
        return
    
    def determine_next_speaker(self):
        next_speaker = random.randint(1,self.npcs)
        return next_speaker
        #Placeholder

def main():
    game = Game()
    game.welcome_message()

    next_speaker = game.player_imposter_index #intialize the user as first speaker

    while True:
        game.round_start()
        for i in range(5):
            game.response(next_speaker, game.convo_history)
            next_speaker = game.determine_next_speaker()
        game.elimination_voting()
        
if __name__ == "__main__":
    main()