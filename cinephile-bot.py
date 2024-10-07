import os
import discord
from discord import User
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

actor_path = "reference/actors.txt"
cinephile_players = []
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
        await message.channel.send(f"{message.author} has joined the game")
        print(cinephile_players)
        
    if message.content.startswith("!Play"):
        last_actor_played = " ".join(message.content.split()[1:])
        print(last_actor_played)

    if message.content.startswith("!Start"):
        await message.channel.send(f"Distributing cards...")
        cards_to_distribute = 6
        for player in cinephile_players:
            for i in range(cards_to_distribute):
                card = random.choice(actors)
                player.cards.append(card)
                actors.remove(card)
                  


client.run(os.getenv("DISCORD_TOKEN"))
