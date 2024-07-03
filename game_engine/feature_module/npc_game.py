import random
from feature_module.gemini_api import gemini

class NPCGame:
    def __init__(self):
        self.npcs = {}  # Dictionary to store NPC interactions
        self.available_npcs = 5  # Assume we have 5 NPCs for simplicity

    def get_random_npc(self):
        npc_id = random.randint(1, self.available_npcs)
        if npc_id not in self.npcs:
            self.npcs[npc_id] = []
        return npc_id

    def interact_with_npc(self, npc_id, message):
        if npc_id in self.npcs:
            self.npcs[npc_id].append(message)
            
            return gemini(message)
        else:
            print(f"NPC {npc_id} not found. Please try again.")

    def get_npc_conversation(self, npc_id):
        if npc_id in self.npcs:
            return self.npcs[npc_id]
        else:
            return []

    def get_available_npcs(self):
        return self.npcs.keys()

    def display_welcome_message(self):
        print("Welcome to NPC game!")
        print("Choose from the following NPCs or say 'random':")

    def display_npc_conversation(self, npc_id):
        conversations = self.get_npc_conversation(npc_id)
        if conversations:
            print(f"Previous conversation(s) with NPC {npc_id}: {', '.join(conversations)}")
        else:
            print(f"No previous conversations with NPC {npc_id}.")
