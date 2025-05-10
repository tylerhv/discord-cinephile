from utils.verify_state import verify_state
from utils.verify_player import verify_player

async def next_turn(message, state, current_turn, cinephile_players):

    if not verify_state(state, "cinephiles"):
        await message.channel.send(f"You cannot use that command right now!")
        return current_turn
    if not verify_player(message.author.name, cinephile_players[current_turn].username):
        await message.channel.send(f"It's not your turn right now!")
        return current_turn
    
    current_turn = (current_turn + 1) % len(cinephile_players)
    await message.channel.send(f"It's {cinephile_players[current_turn].username} turn!")

    return current_turn
