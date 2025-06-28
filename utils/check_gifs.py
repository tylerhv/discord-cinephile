# run this code to see which gifs are present and which are missing
import os

def check_gifs_appear(actors):
    for actor in actors:
        if not os.path.isfile(f"reference/gifs/{actor.lower()}.gif"):
            print(f"{actor.upper()} NOT FOUND!")

if __name__ == "__main__":
    with open("reference/actors.txt", "r") as actors_file:
        actors = actors_file.read().split("\n")
    check_gifs_appear(actors)
