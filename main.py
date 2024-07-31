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
        message = (f"Game Host: This is round {self.round} \nThere are {self.npcs} robots remaining")
        self.convo_history.append({"role": "model", "parts": [f"{message}"]})
        print(message)

    def elimination_voting(self):
        # Reset votes
        for participant in self.participants.values():
            participant.votes = 0

        message = f"Game Host: Alright, that's the end of round {self.round}. Please vote who you think is the imposter"
        self.convo_history.append({"role": "model", "parts": [f"{message}"]})
        print(message)

        # Collect votes
        for participant_id in self.participants:
            if participant_id != self.player_imposter_index:
                # Prompt generation and voting logic
                # TODO: wtf is bellow, make a method to get vote as participant id and encapsulate the error check within it
                prompt = f"You are Robot {participant_id}. Based on the provided chat history, respond only with the integer id number of the human imposter. Avoid including the speaker's name in the response"
                vote = int(gemini(prompt, self.convo_history).strip()) 
                self.convo_history.append({"role": "model", "parts": [f"Robot {participant_id}: {vote}"]})
                print(f"Robot {participant_id}: {vote}")
            else:
                # TODO: error check for user input
                vote = int(input(f"Robot {self.player_imposter_index} (You): ").strip())
                self.convo_history.append({"role": "model", "parts": [f"Robot {self.player_imposter_index}: {vote}"]})
            
            self.participants[vote].votes += 1
        
        # Determine and eliminate the participant with the most votes
        eliminated_id = max(self.participants, key=lambda x: self.participants[x].votes)
        
        if eliminated_id == self.player_imposter_index:
            message = f"Game Host: Robot {eliminated_id} has been eliminated. The human imposter has been caught!"
            print(message)
            return False
        else:
            del self.participants[eliminated_id]
            self.npcs -= 1
      
        if len(self.participants.keys()) <= 2:
            message = f"Game Host: Robot {eliminated_id} has been eliminated. The human imposter has won"
            print(message)
            return False
        
        message2 = f"Game Host: Robot {eliminated_id} has been eliminated"
        self.convo_history.append({"role": "model", "parts": [f"{message2}"]})
        print(message2)
        message3 = f"Game Host: Remaining Participants - {self.participants}"
        self.convo_history.append({"role": "model", "parts": [f"{message3}"]})
        print(message3)
    
    def response(self, id, convo_history):
        # MARK: Maybe check id in the print statements
        if id != self.player_imposter_index:
            # TODO: prompt engineering for line bellow
            prompt = f"You are Robot {id}. Based on the provided chat history, respond briefly. Avoid including the speaker's name in the response"
            response = gemini(prompt, convo_history).strip()
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
    
    message = "Guess the imposter \nAIs vs one Human edition"
    message2 = "The AI vs. human imposter game involves players trying to identify which participant, among AI-controlled Robots, is actually a human imposter by analyzing conversation and behavior clues."
    print(message)
    print(message2)
    
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

    game.convo_history.append({"role": "model", "parts": [f"Game Host: {message}"]})
    game.convo_history.append({"role": "model", "parts": [f"Game Host: {message2}"]})


    next_speaker = game.player_imposter_index #intialize the user as first speaker
    #next_speaker = game.determine_next_speaker()

    while True:
        game.round_start()
        for _ in range(5):
            game.response(next_speaker, game.convo_history)
            next_speaker = game.determine_next_speaker()
        if game.elimination_voting() == False:
            break
        next_speaker = game.determine_next_speaker()
        
if __name__ == "__main__":
    main()