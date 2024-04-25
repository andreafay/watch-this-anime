from jikanpy import Jikan
from yaspin import yaspin
import inquirer
import random
import time
import sys

jikan = Jikan()
spinner = yaspin(text="✩ Picking the best anime for you ✩")

default_rating = 8.00
default_genres = []

def search_anime():
    global default_genres

    while True:
        try:
            response = jikan.random(type='anime')
            spinner.start()
            anime_score = response['data']['score']
            anime_genres = response['data']['genres']
            genres_list = [genre['name'] for genre in anime_genres]
            if anime_score is not None and anime_score >= default_rating:
                    if (not default_genres or (default_genres and check_genre_presence(default_genres, genres_list))):
                        spinner.stop()
                        time.sleep(0.5)
                        anime_title = response['data']['title']
                        anime_score = response['data']['score']
                        anime_year = response['data']['year']
                        genres = ", ".join(genres_list)
                        anime_link = response['data']['url']
                        print("##################################################")
                        print("################### Your anime ###################\n")
                        print(f"# Title: {anime_title}")
                        print(f"# Genres: {genres}")
                        print(f"# Year: {anime_year}")
                        print(f"# Score: {anime_score}")
                        print(f"# Link: {anime_link}")
                        print("\n##################################################")
                        print("##################################################\n")
                        break
            
        except Exception as e:
            pass
            
    what_next = [
    inquirer.List('select',
                message="What now?✩ ",
                choices=['Search again', 'Mark as watched', 'Main menu', 'Exit'],
                ),
            ]
    answer = inquirer.prompt(what_next)
    match answer['select']:
        case 'Search again':
            search_anime()
        case 'Mark as watched':
            mark_as_watched()
        case 'Main menu':
            show_menu()
        case 'Exit':
            sys.exit()


def mark_as_watched():
    print('Watched!')


def check_genre_presence(genres_to_check, available_genres):
    return any(genre in available_genres for genre in genres_to_check)


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
    show_settings_menu()


def set_genres():
    global default_genres
    genres = [
    inquirer.Checkbox('select',
                message="Pick the genres you would like",
                choices=['Action', 'Adventure', 'Avant Garde', 'Award Winning', 'Boys Love', 'Comedy', 'Drama',
                         'Fantasy', 'Girls Love', 'Gourmet', 'Horror', 'Mistery', 'Romance', 'Sci-Fi'
                         'Slice of Life', 'Sports', 'Supernatural', 'Suspense'],
                default=default_genres,
                ),
            ]
    answer = inquirer.prompt(genres)
    default_genres = (answer['select'])
    show_settings_menu()

def show_settings_menu():
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
            set_genres()
        case 'Back':
            show_menu()


def show_menu():
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
            show_settings_menu()
        case 'Exit':
            sys.exit()


if __name__ == "__main__":
     show_menu()