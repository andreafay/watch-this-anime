from jikanpy import Jikan
from yaspin import yaspin
import inquirer
import keyboard
import time
import sys

jikan = Jikan()
spinner = yaspin(text="✩ Picking the best anime for you ✩")

default_rating = 8.00
default_genres = []
to_watch = []
watched = []

def search_anime():
    global default_genres
    global to_watch
    global watched

    while True:
        try:
            response = jikan.random(type='anime')
            spinner.start()
            anime_score = response['data']['score']
            anime_genres = response['data']['genres']
            anime_title = response['data']['title']
            genres_list = [genre['name'] for genre in anime_genres]
            if (not watched or anime_title not in watched) and (anime_score is not None and anime_score >= default_rating):
                    if (not default_genres or (default_genres and check_genre_presence(default_genres, genres_list))):
                        spinner.stop()
                        time.sleep(0.5)
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
                choices=['Search again', 'Mark as to watch', 'Mark as watched', 'Main menu', 'Exit'],
                ),
            ]
    answer = inquirer.prompt(what_next)
    match answer['select']:
        case 'Search again':
            search_anime()
        case 'Mark as to watch':
            mark_as_to_watch(anime_title)
            show_menu()
        case 'Mark as watched':
            mark_as_watched(anime_title)
            show_menu()
        case 'Main menu':
            show_menu()
        case 'Exit':
            sys.exit()


def mark_as_to_watch(title):
    with open("to_watch.txt", "a") as file:
        file.write(title + "\n")


def get_to_watch_list(onStart):
    to_watch_list = []
    try:
        with open("to_watch.txt", "r") as file:
            for line in file:
                to_watch_list.append(line.strip())
        return to_watch_list
    except FileNotFoundError:
        if onStart:
            pass
        print("The to watch list is empty :)")


def show_to_watch_list():
    global to_watch
    to_watch = get_to_watch_list(False)
    file = 'to_watch.txt'
    if to_watch:
        print("############ My To Watch Titles ############")
        for title in to_watch:
            print(f"✿ {title}")
        print("\nPress [W] to mark as a watched a title from the list")
        print("Press [R] to remove a title from the list")
        print("Press [M] to go back to the menu\n")
        while True:
            key = keyboard.read_key()
            match key:
                case 'w':
                    print("w")
                case 'r':
                    titles = [
                    inquirer.Checkbox('select',
                    message="What titles you want to remove?",
                    choices=to_watch,
                    ),
                    ]
                    answer = inquirer.prompt(titles)
                    result = [title for title in to_watch if title not in (answer['select'])]
                    remove_titles(result, file)
                    time.sleep(0.5)
                    show_menu()
                case 'm':
                    show_menu()
                case _: 
                    continue
    else:
        print("The to watch list is empty :)\n")
        time.sleep(0.5)
        show_menu()
                


def mark_as_watched(title):
    with open("watched.txt", "a") as file:
        file.write(title + "\n")


def get_watched_list(onStart):
    watched_list = []
    try:
        with open("watched.txt", "r") as file:
            for line in file:
                watched_list.append(line.strip())
        return watched_list
    except FileNotFoundError:
        if onStart:
            pass
        print("The watched list is empty :)")
        return watched


def show_watched_list():
    global watched
    watched = get_watched_list(False)
    file = 'watched.txt'
    if watched:
        print("############ My Watched Titles ############")
        for title in watched:
            print(f"✿ {title}")
        print("\nPress [R] to remove a title from the list")
        print("Press [M] to go back to the menu\n")
        while True:
            key = keyboard.read_key()
            match key:
                case 'r':
                    titles = [
                    inquirer.Checkbox('select',
                    message="What titles you want to remove?",
                    choices=watched,
                    ),
                    ]
                    answer = inquirer.prompt(titles)
                    result = [title for title in watched if title not in (answer['select'])]
                    remove_titles(result, file)
                    time.sleep(0.5)
                    show_menu()
                case 'm':
                    show_menu()
                case _: 
                    continue
    else:
        print("The watched list is empty :)\n")
        time.sleep(0.5)
        show_menu()


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


def remove_titles(titles, file):
    with open(file, 'w') as f:
        for title in titles:
            f.write(title + '\n')


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
    global to_watch
    global watched
    to_watch = get_to_watch_list(True)
    watched = get_watched_list(True)
    menu = [
    inquirer.List('select',
                    message="Menu",
                    choices=['Search anime', 'My To Watch list', 'My Watched list', 'Settings', 'Exit'],
                ),
    ]
    answer = inquirer.prompt(menu)
    match answer['select']:
        case 'Search anime':
            search_anime()
        case 'My To Watch list':
            show_to_watch_list()
            print('\n')
        case 'My Watched list':
            show_watched_list()
            print('\n')
        case 'Settings':
            show_settings_menu()
        case 'Exit':
            sys.exit()


if __name__ == "__main__":
     show_menu()