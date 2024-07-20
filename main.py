from game_engine.feature_module import gemini_api
from game_engine.feature_module.gemini_api import gemini
import random

class Participant:
    def __init__(self, id, priority_score=0):
        self.id = id
        #TODO self.name = name
        self.priority_score = priority_score
        self.votes = 0

    def __str__(self):
        return f"Robot {self.id}"

    def __repr__(self):
        return f"Robot {self.id}"

class Game:
    def __init__(self, npc_count):
        self.convo_history = []
        self.participants = {}
        self.npcs = npc_count
        self.player_imposter_index = random.randint(1, self.npcs)
        self.round = 0

    def initialize_participants(self):
        # MARK: WORKING
        print("Creating a game...")
        for id in range(1, self.npcs + 1):
            self.participants[id] = (Participant(id, 0))

    def round_start(self):
        # MARK: WORKING
        self.round += 1
        print(f"This is round {self.round} \nThere are {self.npcs} robots remaining")
    
    def elimination_voting(self):
        # MARK: HAS LOGIC ISSUES
        # Reset votes
        for participant in self.participants.values():
            participant.votes = 0
        
        print(f"Alright, that's the end of round {self.round}. Please vote who you think is the imposter")

        # Collect votes
        for participant_id in self.participants:
            if participant_id != self.player_imposter_index:
                # Prompt generation and voting logic
                # TODO: wtf is bellow, make a method to get vote as participant id and encapsulate the error check within it
                vote = random.randint(1, self.npcs)
                print(f"Robot {participant_id}: {vote}")
            else:
                # TODO: error check for user input
                vote = int(input(f"Robot {self.player_imposter_index} (You): ").strip())
            
            self.participants[participant_id].votes += 1
        
        # Determine and eliminate the participant with the most votes
        eliminated_id = max(self.participants, key=lambda x: self.participants[x].votes)
        del self.participants[eliminated_id]
        self.npcs -= 1
        print(f"Robot {eliminated_id} has been eliminated")
        print("Remaining Participants:", self.participants)
    
    def response(self, id, convo_history):
        # MARK: Maybe check id in the print statements
        if id != self.player_imposter_index:
            # TODO: prompt engineering for line bellow
            prompt = f"You are Robot {id}. Based on the provided chat history, respond briefly. Avoid including the speaker's name in the response"
            response = gemini(prompt, convo_history)
            self.convo_history.append({"role": "model", "parts": [f"Robot {id}: {response}"]})
            print(f"Robot {id}: {response}")
        else:
            user_message = input(f"Robot {self.player_imposter_index} (You): ").strip()
            self.convo_history.append({"role": "model", "parts": [f"Robot {id}: {user_message}"]})
        return
    
    def determine_next_speaker(self):
        next_speaker = random.choice(list(self.participants.keys()))
        return next_speaker

def main():
    
    print("Guess the imposter \nAIs vs one Human edition")
    
    while True:
        try:
            npc_count = int(input("How many participants would you like (at least 3)? "))
            if npc_count >= 3:
                game = Game(npc_count)
                print(f"You are Robot {game.player_imposter_index}, an imposter!")
                game.initialize_participants()
                break
            else:
                print("Please enter a number greater than or equal to 3.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    next_speaker = game.player_imposter_index #intialize the user as first speaker

    while True:
        game.round_start()
        for _ in range(5):
            game.response(next_speaker, game.convo_history)
            next_speaker = game.determine_next_speaker()
        game.elimination_voting()
        next_speaker = game.determine_next_speaker()
        
if __name__ == "__main__":
    main()