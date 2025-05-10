from utils.verify_state import verify_state
       
async def add_score(message, state, player_index_reference, cinephile_players):
    if not verify_state(state, "cinephiles"):
        await message.channel.send(f"You cannot use that command right now!")
        return None
    points = int(message.content.split()[1:][0]) #retrieve the number that was passed into the command
    current_player_index = player_index_reference.index(message.author.name)
    cinephile_players[current_player_index].points += points
    await message.channel.send(f"{message.author.name} has {cinephile_players[current_player_index].points} points!")

async def subtract_score(message, state, player_index_reference, cinephile_players):
    if not verify_state(state, "cinephiles"):
        await message.channel.send(f"You cannot use that command right now!")
        return None
    points = int(message.content.split()[1:][0]) #retrieve the number that was passed into the command
    current_player_index = player_index_reference.index(message.author.name)
    cinephile_players[current_player_index].points -= points
    await message.channel.send(f"{message.author.name} has {cinephile_players[current_player_index].points} points!")

async def display_score(message, state, cinephile_players):
    if not verify_state(state, "cinephiles"):
        await message.channel.send(f"You cannot use that command right now!")
        return None
    await message.channel.send(f"Current Score:")
    x = ""
    for player in cinephile_players:
        x = f"{x}{player.username}: {player.points}\n"
    await message.channel.send(x)  