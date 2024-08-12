from backend import gemini
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import random

console = Console()

class Participant:
    def __init__(self, id, priority_score=0):
        self.id = id
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
        console.print("[bold green]Creating a game...[/bold green]")
        for id in range(1, self.npcs + 1):
            self.participants[id] = Participant(id, 0)

    def round_start(self):
        self.round += 1
        message = f"Game Host: This is round {self.round} \nThere are {self.npcs} robots remaining"
        self.convo_history.append({"role": "model", "parts": [message]})
        console.print(Panel(message, title="Round Start", expand=False))

    def elimination_voting(self):
        for participant in self.participants.values():
            participant.votes = 0

        message = f"Game Host: Alright, that's the end of round {self.round}. Please vote who you think is the imposter."
        self.convo_history.append({"role": "model", "parts": [message]})
        console.print(Panel(message, title="Voting Time", expand=False))

        for participant_id in self.participants:
            if participant_id != self.player_imposter_index:
                prompt = f"You are Robot {participant_id}. Based on the provided chat history, respond only with the integer id number of the human imposter. Avoid including the speaker's name in the response."
                vote = int(gemini(prompt, self.convo_history).strip())
                self.convo_history.append({"role": "model", "parts": [f"Robot {participant_id}: {vote}"]})
                console.print(f"[bold cyan]Robot {participant_id}: {vote}[/bold cyan]")
            else:
                vote = int(console.input(f"[bold yellow]Robot {self.player_imposter_index} (You): [/bold yellow]").strip())
                self.convo_history.append({"role": "model", "parts": [f"Robot {self.player_imposter_index}: {vote}"]})

            self.participants[vote].votes += 1
        
        eliminated_id = max(self.participants, key=lambda x: self.participants[x].votes)

        if eliminated_id == self.player_imposter_index:
            message = f"Game Host: Robot {eliminated_id} has been eliminated. The human imposter has been caught!"
            console.print(Panel(message, title="Game Over", style="bold red", expand=False))
            return False
        else:
            del self.participants[eliminated_id]
            self.npcs -= 1

        if len(self.participants.keys()) <= 2:
            message = f"Game Host: Robot {eliminated_id} has been eliminated. The human imposter has won!"
            console.print(Panel(message, title="Game Over", style="bold green", expand=False))
            return False

        message2 = f"Game Host: Robot {eliminated_id} has been eliminated."
        message3 = f"Game Host: Remaining Participants - {len(self.participants)}"
        self.convo_history.append({"role": "model", "parts": [message2]})
        console.print(Panel(message2, title="Elimination Result", expand=False))
        self.convo_history.append({"role": "model", "parts": [message3]})
        console.print(Panel(message3, title="Remaining Participants", expand=False))
    
    def response(self, id, convo_history):
        if id != self.player_imposter_index:
            prompt = f"You are Robot {id}. Based on the provided chat history, respond briefly. Avoid including the speaker's name in the response."
            response = gemini(prompt, convo_history).strip()
            self.convo_history.append({"role": "model", "parts": [f"Robot {id}: {response}"]})
            console.print(f"[bold cyan]Robot {id}: {response}[/bold cyan]")
        else:
            user_message = console.input(f"[bold yellow]Robot {self.player_imposter_index} (You): [/bold yellow]").strip()
            self.convo_history.append({"role": "model", "parts": [f"Robot {id}: {user_message}"]})

    def determine_next_speaker(self):
        return random.choice(list(self.participants.keys()))

def main():
    intro_message = "Guess the imposter \nAIs vs one Human edition"
    intro_message2 = "The AI vs. human imposter game involves players trying to identify which participant, among AI-controlled Robots, is actually a human imposter by analyzing conversation and behavior clues."
    console.print(Panel(intro_message, title="Welcome to TEMP", style="bold magenta", expand=False))
    console.print(Panel(intro_message2, expand=False))
    
    while True:
        try:
            npc_count = int(console.input("[bold blue]How many participants would you like (at least 3)? [/bold blue]").strip())
            if npc_count >= 3:
                game = Game(npc_count)
                console.print(f"[bold yellow]You are Robot {game.player_imposter_index}, an imposter![/bold yellow]")
                game.initialize_participants()
                break
            else:
                console.print("[bold red]Please enter a number greater than or equal to 3.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a valid integer.[/bold red]")

    game.convo_history.append({"role": "model", "parts": [f"Game Host: {intro_message}"]})
    game.convo_history.append({"role": "model", "parts": [f"Game Host: {intro_message2}"]})

    next_speaker = game.player_imposter_index  # Initialize the user as first speaker

    while True:
        game.round_start()
        for _ in range(5):
            game.response(next_speaker, game.convo_history)
            next_speaker = game.determine_next_speaker()
        if not game.elimination_voting():
            break
        next_speaker = game.determine_next_speaker()

if __name__ == "__main__":
    main()
