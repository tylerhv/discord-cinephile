from utils.verify_state import verify_state
from utils.verify_player import verify_player
from utils.verify_actor import verify_actor
import discord

async def play_card(message, state, cinephile_players, current_turn, player_index_reference, actor_gif_links):
    if not verify_state(state, "cinephiles"):
        await message.channel.send(f"You cannot use that command right now!")
        return None
    if not verify_player(message.author.name, cinephile_players[current_turn].username):
        await message.channel.send(f"It's not your turn right now!")
        return None 
    actor = " ".join(message.content.split()[1:])
    current_player_index = player_index_reference.index(message.author.name)

    if not verify_actor(actor, cinephile_players[current_player_index].cards):
        await message.channel.send(f"Invalid actor name!")
        return None
    
    gif_link = actor_gif_links.get(actor)
    
    if gif_link == None:
        pass
    else:
        await message.channel.send(file=discord.File(gif_link))

    cinephile_players[current_player_index].cards.remove(actor)
    last_actor_played = actor
    await message.channel.send(f"Current Card: {last_actor_played}")