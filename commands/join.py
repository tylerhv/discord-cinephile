# commands/join.py

from classes.Player import Player
from utils.verify_state import verify_state
from utils.verify_unique_player import verify_unique_player

async def join_game(message, state, cinephile_players, player_index_reference):
    # Check if the game is in the 'main_menu' state
    if not verify_state(state, "main_menu"):
        await message.channel.send(f"You cannot use that command right now!")
        return None

    # Check if the player is unique (not already in the game)
    if not verify_unique_player(message.author.name, player_index_reference):
        await message.channel.send(f"You are already in the game!")
        return None

    # Add the player to the game
    cinephile_players.append(Player(message.author.name))
    player_index_reference.append(message.author.name)
    await message.channel.send(f"{message.author} has joined the game")