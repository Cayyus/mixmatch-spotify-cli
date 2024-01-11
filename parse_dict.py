from api import SpotifyGET
from tabulate import tabulate
from typing import Any

api = SpotifyGET(params={'limit': 50})

def hyperlink(text, url) -> str:
    return f'\033]8;;{url}\033\\{text}\033]8;;\033\\'

username = api.user_data()
albums = api.get_user_albums()
playlists = api.get_users_playlists()

def parse_print_playlists() -> None:
   headers = ['Name', 'Owner']
   table = []
   for playlist in playlists:
       url = playlist['external_urls']
       name = playlist['name']
       owner = playlist['owner']
       owner_name = owner['display_name']
       owner_link = owner['external_urls']
       hyper_u = hyperlink(owner_name, owner_link)
       hyper_pl = hyperlink(name, url)
       table.append([hyper_pl, hyper_u])
   print(tabulate(table, headers=headers, tablefmt='grid'))

def parse_album(album, specific_album=None) -> Any:
   if specific_album and album['album_name'] != specific_album:
       return None
   album_name = album['album_name']
   total_tracks = album['total_tracks']
   artist = album['artists'][0] 
   tracks = [(track['track_name'], track['artists'], track['duration'], track['track_href']) for track in album['tracks']]
   return (album_name, artist, total_tracks, tracks)


def print_albums(specific_album=None) -> None:
  if specific_album is None:
      parsed_albums = [album for album in [parse_album(album) for album in albums] if album is not None]
      for album_tuple in parsed_albums:
        album_name, artist, tt_tracks, tracks = album_tuple
        print(f"{album_name} by {artist}")
        print(f"{tt_tracks} tracks")
        print(f'See Tracks: python mixmatch.py --al "{album_name}"')
        print()
  elif specific_album is not None:
      parsed_albums = [album for album in [parse_album(album, specific_album) for album in albums] if album is not None]
      if parsed_albums:
        album_name, artist, tt_tracks, tracks = parsed_albums[0]
        print(f"{album_name} by {artist}")
        print(f"{tt_tracks} tracks")

        headers = ["Track", "Artists", "Duration"]
        track_data = [(hyperlink(track[0], track[3]), ', '.join(track[1]), f"{track[2]} minutes") for track in tracks]

        print(tabulate(track_data, headers=headers, tablefmt="grid"))
        print()
