from utils.verify_state import verify_state

async def cards(message, state, cinephile_players, player_index_reference):
    if not verify_state(state, "cinephiles"):
        await message.channel.send(f"You cannot use that command right now!")
        return
    current_player_index = player_index_reference.index(message.author.name)
    await message.author.send("Your cards are:\n" + "\n".join(cinephile_players[current_player_index].cards))