from api import SpotifyGET

api = SpotifyGET()

def hyperlink(text, url) -> str:
    return f'\033]8;;{url}\033\\{text}\033]8;;\033\\'

username = api.user_data()
