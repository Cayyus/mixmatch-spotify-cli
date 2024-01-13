from argparse import ArgumentParser, Namespace
from parsing import print_albums, username, parse_print_playlists
from track_paginator import st_wrap
import os

parser = ArgumentParser()
parser.add_argument('-al', '--albums', nargs='?', const='', help='Print out your saved albums or a specific album if a name is provided')
parser.add_argument('-pl', '--playlists', help='Print out your saved playlists', action='store_true')
parser.add_argument('-st', '--liked_songs', help="See all your liked songs", action='store_true')

args: Namespace = parser.parse_args()

os.system('cls')
print(f"Hello {username}")
print("Type python mixmatch.py -h to see all commands.")

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
