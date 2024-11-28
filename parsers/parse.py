from api.getapi import SpotifyGET
from api.postapi import SpotifyPOST
from api.putapi import SpotifyPUT

api = SpotifyGET()
papi = SpotifyPOST()
puapi = SpotifyPUT()

def hyperlink(text, url) -> str:
    return f'\033]8;;{url}\033\\{text}\033]8;;\033\\'

username = api.user_data()
