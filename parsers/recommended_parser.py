from parsers.parse import api, papi, hyperlink
from shared.er import hide_error

def parse_recommendations():
    try: 
        recommended_tracks = api.get_recommendations()
    except Exception as e:
        hide_error(str(e))

    print("Spotify's recommended tracks:")
    for recommended_track in recommended_tracks:
        msg = f"{hyperlink(recommended_track['name'], recommended_track['url'])} ({hyperlink(recommended_track['album_name'], recommended_track['album_url'])}) by {hyperlink(recommended_track['artist_name'], recommended_track['artist_url'])}"
        print(msg)

    add_playlist = str(input("Do you want to add these tracks to a new playlist? (y/n) "))

    if add_playlist not in ['y', 'n']:
        print("Invalid response.") 
        return

    if add_playlist == 'y':
        uris = []
        for recommended_track in recommended_tracks:
            uris.append(recommended_track['uri'])
        
        playlist_id = papi.create_playlist(name='Recommended Songs (by Mixmatch)')
        adding = papi.add_to_playlist(playlist_id, uris)

        if adding != 201:
            print("An error occured. Try again")
        else:
            print(f"All tracks added successfully! Check it out {hyperlink('here', f'https://open.spotify.com/playlist/{playlist_id}')}.")
    else:
        return
