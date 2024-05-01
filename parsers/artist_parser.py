from parsers.parse import api, hyperlink
from shared.er import hide_error

def parse_artist(q):
    try:
        artist = api.get_artist(q)
    except Exception as e:
        hide_error(str(e))
    
    tracs = {}
    ras = {}

    name, url, popularity, followers = artist['name'], artist['url'], artist['popularity'], artist['followers']
    genres = ', '.join(artist['genres'])
    tracks = artist['tracks']
    related_artists = artist['related_artists']

    for track in tracks:
        t_name = track['name']
        t_url = track['url']
        t_album = track['album_name']
        t_albumurl = track['album_link']
        t_albumreldate = track['rel_date']

        tracs[t_name] = {
            'url': t_url,
            'album': t_album,
            'albumurl': t_albumurl,
            'albumreldate': t_albumreldate
        }
    
    for related_artist in related_artists:
        ra_name = related_artist['name']
        ra_url = related_artist['url']

        ras[ra_name] = {'url': ra_url}
    

    string = f"""
Artist Name: {hyperlink(name, url)}
Followers: {followers}
Popularity: {popularity}
Genres: {genres}

Artist's top tracks:
"""
    print(string)
    for track_name, track_info in tracs.items():
        print(f"{hyperlink(track_name, track_info['url'])}, {hyperlink(track_info['album'], track_info['albumurl'])} ({track_info['albumreldate']})")
    print('\n')
    
    print("Related Artists:")
    for ra, ra_info in ras.items():
        print(f"{hyperlink(ra, ra_info['url'])}", end=', ')
