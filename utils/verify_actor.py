def verify_actor(actor, user_actors):
    if actor not in user_actors:
        return False
    else:
        return True