import random

if __name__ == "__main__":
    from gemini_api import gemini
else:
    from .gemini_api import gemini
    
    
class NPCGame:
    def __init__(self):
        self.npcs = {}
        self.available_npcs = 0
        
    def add_npc(self, npc_id):
        
            """
            Adds a new NPC to the game.

            Parameters:
            npc_id (int): The ID of the NPC to be added.

            Returns:
            None
            """
            
            if npc_id not in self.npcs:
                self.npcs[npc_id] = []
                self.available_npcs += 1
            else:
                print(f"NPC {npc_id} already exists. Please try again.")

    def get_random_npc(self):
            
            """
            Returns a random NPC ID from the available NPCs.

            Returns:
                int: A random NPC ID.
            """
            
            npc_id = random.randint(1, self.available_npcs)
            npc_id = self.npcs.keys()[npc_id]
            
            return npc_id

    def interact_with_npc(self, npc_id, message):
        
            """
            Interacts with an NPC by sending a message and receiving a response.

            Args:
                npc_id (int): The ID of the NPC to interact with.
                message (str): The message to send to the NPC.

            Returns:
                str: The response message from the NPC.
            """
            
            if npc_id in self.npcs:
                self.npcs[npc_id].append({"role":"user","parts":[message]})
                gemini_message = gemini(message, self.npcs[npc_id]) # this needs to be edited
                self.npcs[npc_id].append({"role":"model","parts":[gemini_message]})
                return gemini_message
            else:
                print(f"NPC {npc_id} not found. Please try again.")

    def get_npc_conversation(self, npc_id):
            
            """
            Retrieve the conversation of an NPC based on its ID.

            Parameters:
            npc_id (int): The ID of the NPC.

            Returns:
            list: The conversation of the NPC as a list of strings.

            """
            
            if npc_id in self.npcs:
                return self.npcs[npc_id]
            else:
                return []

    def get_available_npcs(self):
            
            """
            Returns a list of available NPCs in the game.

            Returns:
                list: A list of available NPCs.
            """
            
            return self.npcs.keys()

    def display_welcome_message(self):
            
            """
            Displays a welcome message for the NPC game.
            """

            print("Welcome to NPC game!")
            print("Choose from the following NPCs or say 'random':")

    def display_npc_conversation(self, npc_id):
            
            """
            Display the previous conversation(s) with the specified NPC.

            Args:
                npc_id (int): The ID of the NPC.

            Returns:
                None
            """

            conversations = self.get_npc_conversation(npc_id)
            if conversations:
                print(f"Previous conversation(s) with NPC {npc_id}: {conversations}")
            else:
                print(f"No previous conversations with NPC {npc_id}.")
