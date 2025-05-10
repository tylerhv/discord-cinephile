from utils.verify_state import verify_state
from utils.verify_actor import verify_actor
import random

async def shuffle_cards(message, state, cinephile_players, player_index_reference, actors):
    if not verify_state(state, "cinephiles"):
        await message.channel.send(f"You cannot use that command right now!")
        return None

    actor = " ".join(message.content.split()[1:])
    current_player_index = player_index_reference.index(message.author.name)

    if not verify_actor(actor, cinephile_players[current_player_index].cards):
        await message.channel.send(f"Invalid actor name!")
        return None

    card = random.choice(actors)
    cinephile_players[current_player_index].cards.append(card)
    actors.remove(card)
    actors.append(actor)
    cinephile_players[current_player_index].cards.remove(actor)
    await message.author.send(f"You replaceed {actor} for {card}!")    