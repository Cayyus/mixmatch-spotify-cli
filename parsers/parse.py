from api.getapi import SpotifyGET
from api.postapi import SpotifyPOST

api = SpotifyGET()
papi = SpotifyPOST()

def hyperlink(text, url) -> str:
    return f'\033]8;;{url}\033\\{text}\033]8;;\033\\'

username = api.user_data()
