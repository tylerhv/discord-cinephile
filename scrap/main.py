import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == client.user:
            print("Hello there!")

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

# intents basically says "enable these list of classes"
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
print(client)
client.run(os.getenv("DISCORD_TOKEN"))

