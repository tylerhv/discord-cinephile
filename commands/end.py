from utils.verify_state import verify_state

async def end_game(message, state, cinephile_players, player_index_reference, last_actor_played, current_turn, actors, refresh_actors):
    if not verify_state(state, "cinephiles"):
        await message.channel.send(f"You cannot use that command right now!")
        return state, cinephile_players, player_index_reference, last_actor_played, current_turn, actors
    await message.channel.send(f"Game over!")
    x = ""
    state = "main_menu"
    for player in cinephile_players:
        x = f"{x}{player.username}: {player.points}\n"
    cinephile_players = []
    player_index_reference = []
    last_actor_played = ""
    current_turn = 0
    actors = refresh_actors
    await message.channel.send(x)
    return state, cinephile_players, player_index_reference, last_actor_played, current_turn, actors