from tabulate import tabulate

from parsers.parse import api, hyperlink
from shared.er import hide_error

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
        print(f'See tracks: python mixmatch.py -fs "{pl["name"]}"')
        print()
