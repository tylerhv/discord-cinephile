import os
import discord
from discord import User
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

actor_path = "reference/actors.txt"
cinephile_players = []
player_index_reference = []
last_actor_played = ""

with open(actor_path, "r") as actors_file:
    actors = actors_file.read().split("\n")

index = [i for i in range(len(actors))]


class Player:
    def __init__(self, username):
        self.username = username
        self.cards = []

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!Join":
        cinephile_players.append(Player(message.author.name))
        player_index_reference.append(message.author.name)
        await message.channel.send(f"{message.author} has joined the game")
        print(cinephile_players)
        
    if message.content.startswith("!Play"):
        actor = " ".join(message.content.split()[1:])
        current_player_index = player_index_reference.index(message.author.name)
        cinephile_players[current_player_index].cards.remove(actor)
        last_actor_played = actor
        print(cinephile_players[current_player_index].cards)

    if message.content.startswith("!Start"):
        await message.channel.send(f"Distributing cards...")
        cards_to_distribute = 6
        for player in cinephile_players:
            for i in range(cards_to_distribute):
                card = random.choice(actors)
                player.cards.append(card)
                actors.remove(card)
        print(cinephile_players[0].cards)
                  


client.run(os.getenv("DISCORD_TOKEN"))
