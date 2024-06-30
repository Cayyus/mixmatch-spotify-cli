from argparse import ArgumentParser, Namespace
import os

from parsers.parse import username
from parsers.album_parsers import print_albums
from parsers.playlist_parsers import parse_featured, parse_print_playlists
from parsers.artist_parser import parse_artist
from parsers.recommended_parser import parse_recommendations

from paginators.track_paginator import st_wrap
from paginators.featured_tracktable import fs_wrap

from dotenv import load_dotenv

load_dotenv('creds.env')

parser = ArgumentParser()
parser.add_argument('-al', '--albums', nargs='?', const='', 
                    help='Print out your saved albums or a specific album if a name is provided')
parser.add_argument('-pl', '--playlists', help='Print out your saved playlists', action='store_true')
parser.add_argument('-st', '--liked_songs', help="See all your liked songs", action='store_true')
parser.add_argument('-fs', '--featured_playlists', help='Discover playlists featured by Spotify', 
                    nargs="?", const='')
parser.add_argument('-art', '--artist', help='Get information on a artist', nargs='?', const='')
parser.add_argument("-frt", "--find_rectracks", help="Find recommended tracks from Spotify", action="store_true")

args: Namespace = parser.parse_args()

os.system('cls')
if username is not None:
  print(f"Hello there, {username}.")
else:
  print("Hello there!")
print(f"Type {os.environ.get('COMMAND_PREFIX')} -h to see all commands.")

if args.albums is not None:
  os.system('cls') 
  if args.albums != '':  # album name is provided
    print_albums(args.albums)
  else:
    print_albums()

if args.playlists:
  os.system('cls')
  parse_print_playlists()

if args.liked_songs:
  os.system('cls')
  st_wrap()

if args.featured_playlists is not None:
  os.system('cls')
  if args.featured_playlists != '':
      fs_wrap(args.featured_playlists)
  else:
      parse_featured()

if args.artist is not None:
  os.system('cls')
  if args.artist != '':
    parse_artist(args.artist)
  else:
    print('Please type a artist name using mixmatch.py --art "artist name"')

if args.find_rectracks:
  os.system("cls")
  parse_recommendations()
