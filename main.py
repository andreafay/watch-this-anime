from jikanpy import Jikan
from yaspin import yaspin
import inquirer
import random
import time
import sys

jikan = Jikan()
spinner = yaspin(text="✩ Picking the best anime for you ✩")

default_rating = 8.00

def search_anime():
    while True:
        try:
            response = jikan.random(type='anime')
            spinner.start()
            anime_score = response['data']['score']
            if anime_score is not None and anime_score >= default_rating:
                    spinner.stop()
                    time.sleep(0.5)
                    anime_title = response['data']['title']
                    anime_score = response['data']['score']
                    anime_year = response['data']['year']
                    anime_genres = response['data']['genres']
                    genre = [genre['name'] for genre in anime_genres]
                    genres = ", ".join(genre)
                    anime_link = response['data']['url']
                    print("##################################################")
                    print("################### Your anime ###################\n")
                    print(f"# Title: {anime_title}")
                    print(f"# Genres: {genres}")
                    print(f"# Year: {anime_year}")
                    print(f"# Link: {anime_link}")
                    print(f"# Score: {anime_score}")
                    print("\n##################################################")
                    print("##################################################\n")
                    break
            
        except Exception as e:
            pass
            
    what_next = [
    inquirer.List('select',
                message="What now?✩ ",
                choices=['Search again', 'Main menu', 'Exit'],
                ),
            ]
    answer = inquirer.prompt(what_next)
    match answer['select']:
        case 'Search again':
            search_anime()
        case 'Main menu':
            menu()
        case 'Exit':
            sys.exit()


def change_rating():
    global default_rating
    rating = [
    inquirer.List('select',
                message="Default min rating is 8",
                choices=['6', '6.5', '7', '7.5', '8', '8.5', '9'],
                ),
            ]
    answer = inquirer.prompt(rating)
    default_rating = float(answer['select'])
    menu()


def show_settings():
    settings = [
    inquirer.List('select',
                message="Settings",
                choices=['Rating', 'Genres', 'Back'],
                ),
            ]
    answer = inquirer.prompt(settings)
    match answer['select']:
        case 'Rating':
            change_rating()
        case 'Genres':
            menu()
        case 'Back':
            menu()


def menu():
    menu = [
    inquirer.List('select',
                    message="Menu",
                    choices=['Search anime', 'Settings', 'Exit'],
                ),
    ]
    answer = inquirer.prompt(menu)
    match answer['select']:
        case 'Search anime':
            search_anime()
        case 'Settings':
            show_settings()
        case 'Exit':
            sys.exit()


if __name__ == "__main__":
     menu()