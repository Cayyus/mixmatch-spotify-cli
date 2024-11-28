from tabulate import tabulate

from parsers.parse import api, papi, puapi, hyperlink
from paginators.playlist_paginator import PlaylistTable
from utils.er import hide_error

import curses

import os
from dotenv import load_dotenv

load_dotenv("creds.env")


try:
    saved_playlists = api.get_users_playlists()
    featured_playlists = api.get_featured_playlists()
except Exception as e:
    hide_error(str(e))

def parse_print_playlists() -> None: 
   headers = ['Name', 'Owner']
   table = []
   for playlist in saved_playlists:
       url = playlist['external_urls']
       name = playlist['name']
       owner = playlist['owner']
       owner_name = owner['display_name']
       owner_link = owner['external_urls']
       hyper_u = hyperlink(owner_name, owner_link)
       hyper_pl = hyperlink(name, url)
       table.append([hyper_pl, hyper_u])
   print(tabulate(table, headers=headers, tablefmt='grid'))


def parse_featured():
    for pl in featured_playlists[0]['playlists']:
        print(f"Name: {hyperlink(pl['name'], pl['url'])}")
        print(f"Description: {pl['description']}")
        print(f"Tracks: {pl['tracks']}")
        print(f'See tracks: {os.environ.get("COMMAND_PREFIX")} -fs "{pl["name"]}"')
        print()

def parse_search_user(playlist_name):
    try:
        search_results = api.search_user_playlists(playlist_name)
    except Exception as e:
        hide_error(str(e))
        return

    if search_results:
        print("Matching Playlists:")
        for number, playlist in search_results.items():
            print(f"{number}: {playlist['name']} (URL: {playlist['url']})")

        while True:
            choice = input("Enter the number of the playlist you want to select (or type 'exit' to quit): ").strip()

            if choice.lower() == 'exit':
                print("Exiting the selection.")
                return

            if not choice.isdigit() or int(choice) not in search_results:
                print("Invalid choice. Please try again.")
                continue
            else:
                break  # Breaks the infinite loop when choice is valid

        selected_playlist = search_results[int(choice)]
        playlist_content = api.get_playlist_details(selected_playlist['id'])
        os.system("cls")
        print(f"""{hyperlink(playlist_content['name'], playlist_content['url'])}
Owner: {hyperlink(playlist_content['owner_name'], playlist_content['owner_url'])}
Tracks: {playlist_content['tracks']}
Followers: {playlist_content['followers']}
""")

        while True:
            print("Type 0 to exit")
            print("Type 1 to view playlist tracks")
            print("Type 2 to add track/tracks to this playlist")
            print("Type 3 to remove track/tracks from this playlist")
            print("Type 4 to change playlist details\n")

            type_choice = input("Choose an action: ").strip()

            if type_choice not in ['0', '1', '2', '3', '4']:
                print("Invalid choice. Please try again.")
                continue

            type_choice = int(type_choice)  

            if type_choice == 0:
                print("Exiting.")
                return
            elif type_choice == 1:
                all_tracks = []

                playlists = api.get_playlist_content(selected_playlist['id'])
                playlists_items = playlists['items']

                for item in playlists_items:
                    name, url = item['track']['name'], item['track']['external_urls']['spotify']
                    artists = ', '.join([artist['name'] for artist in item['track']['artists']])
                    duration_min = item['track']['duration_ms'] // 60000
                    all_tracks.append([name, url, artists, duration_min])

                def tracktable_main(stdscr):
                    table = PlaylistTable(stdscr, all_tracks)     
                    table.run()
                curses.wrapper(tracktable_main)
                return
            
            elif type_choice == 2:
                tracks_to_add = str(input("Enter track URL to add to playlist or multiple tracks by separating with comma: ")).split(',')
                track_uris = list(set([f"spotify:track:{track.split('/track/')[1].split('?')[0]}" for track in tracks_to_add if 'https://open.spotify.com/track' in track]))

                adding = papi.add_to_playlist(selected_playlist['id'], uris=track_uris)
                if adding != 201:
                    print("Something went wrong. Try again.")
                    print(f"Error code: {adding}")
                    return
                else:
                    print("Successfully saved tracks to playlist!")
                    return
                
            elif type_choice == 3:
                print("Logic for remove tracks here")
            
            elif type_choice == 4:
                name = str(input("Enter new name (press enter to skip): "))
                desc =  str(input("Enter new description (press enter to skip): "))
                public =  str(input("Enter new playlist status (public or private): "))
                
                public_bool = None  # Default to None if input is invalid
                if public == "public":
                    public_bool = True
                elif public == "private":
                    public_bool = False
                # Call change_playlist_details with only the provided values
                changed = puapi.change_playlist_details(
                    id=selected_playlist['id'],
                    name=name if name else None,
                    desc=desc if desc else None,
                    public=public_bool if public_bool is not None else None
                )
                
                if changed == 200:
                    print("Successfully changed playlist details!")
                    return
                else:
                    print("An error occured. Try again.")
                    return
    else:
        print(f"No playlists found with the name '{playlist_name}'. Please try again.")
