from argparse import ArgumentParser, Namespace
from parse_dict import print_albums, username
import os

parser = ArgumentParser()
parser.add_argument('-al', '--albums', nargs='?', const='', help='Print out your saved albums or a specific album if a name is provided')

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
