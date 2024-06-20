from feature_module.npc_game import NPCGame

def main():
    game = NPCGame()
    game.display_welcome_message()

    while True:
        available_npcs = game.get_available_npcs()
        print("Available NPCs: ", ' '.join(map(str, available_npcs)))
        user_input = input().strip()

        if user_input.lower() == 'random':
            npc_id = game.get_random_npc()
            print(f"You are talking to NPC {npc_id}:")
        else:
            try:
                npc_id = int(user_input)
                if npc_id not in available_npcs:
                    print(f"NPC {npc_id} not available. Please choose again.")
                    continue
            except ValueError:
                print("Invalid input. Please type 'random' or an NPC number.")
                continue

        while True:
            user_message = input("You: ").strip()
            if user_message.lower() == "quit":
                break
            #print("{npc_id}: ", game.interact_with_npc(npc_id, user_message))
            print(game.interact_with_npc(npc_id, user_message))
        game.display_npc_conversation(npc_id)

        print("Choose from the following NPCs or say 'random':")

if __name__ == "__main__":
    main()