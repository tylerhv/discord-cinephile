import os
import discord
from discord import User
from classes.Player import Player
from commands.join import join_game
from commands.play import play_card
from commands.start import start_game
from commands.scores import add_score, subtract_score, display_score
from commands.next import next_turn
from commands.end import end_game
from commands.cards import cards
from commands.shuffle import shuffle_cards

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

refresh_actors = actors
index = [i for i in range(len(actors))]

state = "main_menu"

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
        state, cinephile_players, player_index_reference, last_actor_played, current_turn, actors = await end_game(message, state, cinephile_players, player_index_reference, last_actor_played, current_turn, actors, refresh_actors)
        return
    
    if message.content.startswith("!score"):
        await display_score(message, state, cinephile_players)
        return

    if message.content.startswith("!cards"):
        await cards(message, state, cinephile_players, player_index_reference)
        return

    if message.content.startswith("!shuffle"):
        await shuffle_cards(message, state, cinephile_players, player_index_reference, actors)
        return
  
    if message.content.startswith("!help"):
        await message.author.send(command_list)

client.run(os.getenv("DISCORD_TOKEN"))
