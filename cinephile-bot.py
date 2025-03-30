import os
import discord
from discord import User
from classes.Player import Player
from utils.verify_state import verify_state
from utils.verify_player import verify_player
from utils.verify_actor import verify_actor
from utils.verify_unique_player import verify_unique_player
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
    if message.author == client.user:
        return

    if message.content == "!join":
        check = verify_state(state, "main_menu")
        unique_player_check = verify_unique_player(message.author.name, player_index_reference)
        if check == False:
            await message.channel.send(f"You cannot use that command right now!")
            return None
        if unique_player_check == False:
            await message.channel.send(f"You are already in the game!")
            return None

        cinephile_players.append(Player(message.author.name))
        player_index_reference.append(message.author.name)
        await message.channel.send(f"{message.author} has joined the game")
        print(cinephile_players)
        
    if message.content.startswith("!play"):
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

    if message.content.startswith("!start"):
        check = verify_state(state, "main_menu")
        if check == False:
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

    if message.content.startswith("!add"):
        check = verify_state(state, "cinephiles")
        if check == False:
            await message.channel.send(f"You cannot use that command right now!")
            return None
        points = int(message.content.split()[1:][0]) #retrieve the number that was passed into the command
        current_player_index = player_index_reference.index(message.author.name)
        cinephile_players[current_player_index].points += points
        await message.channel.send(f"{message.author.name} has {cinephile_players[current_player_index].points} points!")

    if message.content.startswith("!subtract"):
        check = verify_state(state, "cinephiles")
        if check == False:
            await message.channel.send(f"You cannot use that command right now!")
            return None
        points = int(message.content.split()[1:][0]) #retrieve the number that was passed into the command
        current_player_index = player_index_reference.index(message.author.name)
        cinephile_players[current_player_index].points -= points
        await message.channel.send(f"{message.author.name} has {cinephile_players[current_player_index].points} points!")

    if message.content.startswith("!next"):
        check = verify_state(state, "cinephiles")
        player_check = verify_player(message.author.name, cinephile_players[current_turn].username)
        if check == False:
            await message.channel.send(f"You cannot use that command right now!")
            return None
        if player_check == False:
            await message.channel.send(f"It's not your turn right now!")
            return None 
        current_turn = (current_turn + 1) % len(cinephile_players)
        await message.channel.send(f"It's {cinephile_players[current_turn].username} turn!")

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
        check = verify_state(state, "cinephiles")
        if check == False:
            await message.channel.send(f"You cannot use that command right now!")
            return None
        await message.channel.send(f"Current Score:")
        x = ""
        for player in cinephile_players:
            x = f"{x}{player.username}: {player.points}\n"
        await message.channel.send(x)  

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
