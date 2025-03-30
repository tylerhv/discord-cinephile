from utils.verify_state import verify_state
import random

async def start_game(message, state, cinephile_players, actors, current_turn):
    if not verify_state(state, "main_menu"):
        await message.channel.send(f"You cannot use that command right now!")
        return None
    await message.channel.send(f"Distributing cards... \nDo '!cards' to see your cards.")
    state = "cinephiles"
    cards_to_distribute = 6
    for player in cinephile_players:
        for i in range(cards_to_distribute):
            card = random.choice(actors)
            player.cards.append(card)
            actors.remove(card)
    card = random.choice(actors)
    await message.channel.send(f"The Current Card: {card}")
    actors.remove(card)
    await message.channel.send(f"It's {cinephile_players[current_turn].username} turn!")
    
    return state