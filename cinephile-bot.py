import os
import discord
from discord import User
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

class Player:
    def __init__(self, username):
        self.username = username
        self.cards = []
        self.points = 0

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!join":
        cinephile_players.append(Player(message.author.name))
        player_index_reference.append(message.author.name)
        await message.channel.send(f"{message.author} has joined the game")
        print(cinephile_players)
        
    if message.content.startswith("!play"):
        actor = " ".join(message.content.split()[1:])
        current_player_index = player_index_reference.index(message.author.name)
        cinephile_players[current_player_index].cards.remove(actor)
        last_actor_played = actor
        await message.channel.send(f"Current Card: {last_actor_played}")

    if message.content.startswith("!start"):
        await message.channel.send(f"Distributing cards... \nDo '!cards' to see your cards.")
        cards_to_distribute = 6
        for player in cinephile_players:
            for i in range(cards_to_distribute):
                card = random.choice(actors)
                player.cards.append(card)
                actors.remove(card) 
        global current_turn
        card = random.choice(actors)
        await message.channel.send(f"The Current Card: {card}")
        actors.remove(card)
        await message.channel.send(f"It's {cinephile_players[current_turn].username} turn!")

    if message.content.startswith("!add"):
        points = int(message.content.split()[1:][0]) #retrieve the number that was passed into the command
        current_player_index = player_index_reference.index(message.author.name)
        cinephile_players[current_player_index].points += points
        print(cinephile_players[current_player_index].points)

    if message.content.startswith("!subtract"):
        points = int(message.content.split()[1:][0]) #retrieve the number that was passed into the command
        current_player_index = player_index_reference.index(message.author.name)
        cinephile_players[current_player_index].points +- points
        print(cinephile_players[current_player_index].points)

    if message.content.startswith("!next"):
        current_turn = (current_turn + 1) % len(cinephile_players)
        await message.channel.send(f"It's {cinephile_players[current_turn].username} turn!")

    if message.content.startswith("!end"):
        await message.channel.send(f"Game over!")
        x = ""
        for player in cinephile_players:
            x = f"{x}{player.username}: {player.points}"
        await message.channel.send(x)

    if message.content.startswith("!score"):
        await message.channel.send(f"Current Score:")
        x = ""
        for player in cinephile_players:
            x = f"{x}{player.username}: {player.points}"
        await message.channel.send(x)  

    if message.content.startswith("!cards"):
        current_player_index = player_index_reference.index(message.author.name)
        await message.author.send("Your cards are:\n" + "\n".join(cinephile_players[current_player_index].cards))

    if message.content.startswith("!shuffle"):
        actor = " ".join(message.content.split()[1:])
        current_player_index = player_index_reference.index(message.author.name)
        card = random.choice(actors)
        cinephile_players[current_player_index].cards.append(card)
        actors.remove(card)
        actors.append(actor)
        cinephile_players[current_player_index].cards.remove(actor)
        await message.author.send(f"You replaceed {actor} for {card}!")     
  
    if message.content.startswith("!help"):
        await message.author.send(command_list)




client.run(os.getenv("DISCORD_TOKEN"))
