from api import SpotifyGET
from tabulate import tabulate
from parsers.parser import hyperlink

api = SpotifyGET()

saved_playlists = api.get_users_playlists()
featured_playlists = api.get_featured_playlists()


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
    for playlist in featured_playlists[0]['playlists']:
        print(f"Name: {hyperlink(playlist['name'], playlist['url'])}")
        print(f"Description: {playlist['description']}")
        print(f"Tracks: {playlist['tracks']}")
        print(f'See tracks: python mixmatch.py --fs "{playlist["name"]}"')
        print()
