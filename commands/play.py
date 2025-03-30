from utils.verify_state import verify_state
from utils.verify_player import verify_player
from utils.verify_actor import verify_actor

async def play_card(message, state, cinephile_players, current_turn, player_index_reference):
    state_check = verify_state(state, "cinephiles")
    player_check = verify_player(message.author.name, cinephile_players[current_turn].username)
    if state_check == False:
        await message.channel.send(f"You cannot use that command right now!")
        return None
    if player_check == False:
        await message.channel.send(f"It's not your turn right now!")
        return None 
    actor = " ".join(message.content.split()[1:])
    current_player_index = player_index_reference.index(message.author.name)

    actor_check = verify_actor(actor, cinephile_players[current_player_index].cards)

    if actor_check == False:
        await message.channel.send(f"Invalid actor name!")
        return None

    cinephile_players[current_player_index].cards.remove(actor)
    last_actor_played = actor
    await message.channel.send(f"Current Card: {last_actor_played}")