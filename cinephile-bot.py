import os
import discord
from discord import User

actor_path = "reference/actors.txt"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

cinephile_players = []

with open(actor_path, "r") as actors_file:
    actors = actors_file.read()

print(actors.split("\n"))
    

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

    if message.content == "!Play":
        cinephile_players.append(Player(message.author.name))
        await message.channel.send(f"{message.author} has joined the game")
        print(cinephile_players)

client.run(os.getenv("DISCORD_TOKEN"))
