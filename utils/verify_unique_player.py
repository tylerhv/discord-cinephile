def verify_unique_player(player, player_list):
    print(player)
    print(player_list)
    if player in player_list:
        return False
    else:
        return True