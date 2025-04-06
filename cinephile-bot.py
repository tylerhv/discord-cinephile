import os
import discord
from discord import User
from classes.Player import Player
from utils.verify_state import verify_state
from utils.verify_player import verify_player
from utils.verify_actor import verify_actor
from commands.join import join_game
from commands.play import play_card
from commands.start import start_game
from commands.scores import add_score, subtract_score, display_score
from commands.next import next_turn
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
actor_path = "reference/actors.txt"
help_path = "reference/help.txt"
cinephile_players = []
player_index_reference = []
last_actor_played = ""
current_turn = 0
with open(help_path, "r") as f:
    command_list = f.read()

with open(actor_path, "r") as actors_file:
    actors = actors_file.read().split("\n")

index = [i for i in range(len(actors))]

state = "main_menu"
print(type(actors))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global state
    global current_turn
    global cinephile_players
    global player_index_reference
    global last_actor_played
    global actors

    if message.author == client.user:
        return

    if message.content == "!join":
        await join_game(message, state, cinephile_players, player_index_reference)
        return
        
    if message.content.startswith("!play"):
        await play_card(message, state, cinephile_players, current_turn, player_index_reference)
        return

    if message.content.startswith("!start"):
        state = await start_game(message, state, cinephile_players, actors, current_turn)
        return

    if message.content.startswith("!add"):
        await add_score(message, state, player_index_reference, cinephile_players)
        return

    if message.content.startswith("!subtract"):
        await subtract_score(message, state, player_index_reference, cinephile_players)
        return

    if message.content.startswith("!next"):
        current_turn = await next_turn(message, state, current_turn, cinephile_players)
        return

    if message.content.startswith("!end"):
        check = verify_state(state, "cinephiles")
        if check == False:
            await message.channel.send(f"You cannot use that command right now!")
            return None
        await message.channel.send(f"Game over!")
        x = ""
        state = "main_menu"
        for player in cinephile_players:
            x = f"{x}{player.username}: {player.points}\n"
        cinephile_players = []
        player_index_reference = []
        last_actor_played = ""
        current_turn = 0
        await message.channel.send(x)

    if message.content.startswith("!score"):
        await display_score(message, state, cinephile_players)
        return

    if message.content.startswith("!cards"):
        check = verify_state(state, "cinephiles")
        if check == False:
            await message.channel.send(f"You cannot use that command right now!")
            return None
        current_player_index = player_index_reference.index(message.author.name)
        await message.author.send("Your cards are:\n" + "\n".join(cinephile_players[current_player_index].cards))

    if message.content.startswith("!shuffle"):
        check = verify_state(state, "cinephiles")

        if check == False:
            await message.channel.send(f"You cannot use that command right now!")
            return None
        
        actor = " ".join(message.content.split()[1:])
        current_player_index = player_index_reference.index(message.author.name)
        actor_check = verify_actor(actor, cinephile_players[current_player_index].cards)

        if actor_check == False:
            await message.channel.send(f"Invalid actor name!")
            return None

        card = random.choice(actors)
        cinephile_players[current_player_index].cards.append(card)
        actors.remove(card)
        actors.append(actor)
        cinephile_players[current_player_index].cards.remove(actor)
        await message.author.send(f"You replaceed {actor} for {card}!")     
  
    if message.content.startswith("!help"):
        await message.author.send(command_list)

client.run(os.getenv("DISCORD_TOKEN"))
