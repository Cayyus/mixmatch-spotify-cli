from parsers.parse import api, papi, hyperlink
from shared.er import hide_error

def parse_recommendations(limit: int = 10):
    try: 
        recommended_tracks = api.get_recommendations(limit)
    except Exception as e:
        hide_error(str(e))

    print("Spotify's recommended tracks:")
    for recommended_track in recommended_tracks:
        msg = f"{hyperlink(recommended_track['name'], recommended_track['url'])} ({hyperlink(recommended_track['album_name'], recommended_track['album_url'])}) by {hyperlink(recommended_track['artist_name'], recommended_track['artist_url'])}"
        print(msg)

    add_playlist = str(input("Do you want to create a new playlist or add these tracks to a existing playlist? (c/e) "))

    if add_playlist not in ['c', 'e']:
        print("Invalid response.") 
        return
    
    uris = []
    for recommended_track in recommended_tracks:
        uris.append(recommended_track['uri'])

    if add_playlist == 'c':
        playlist_id = papi.create_playlist(name='Recommended Songs (by Mixmatch)')
        adding = papi.add_to_playlist(playlist_id, uris)

        if adding != 201:
            print("An error occured. Try again")
        else:
            print(f"All tracks added successfully! Check it out {hyperlink('here', f'https://open.spotify.com/playlist/{playlist_id}')}.")
    else:
        while True:
            playlist_to_add = str(input("Type the name of the playlist you want to add to: "))
            
            if playlist_to_add.lower() == "0":
                return

            search_results = api.search_user_playlists(playlist_to_add)

            if search_results:
                for number, playlist in search_results.items():
                    print(f"{number}: {hyperlink(playlist['name'], playlist['url'])}")
                
                try:
                    choice = int(input("Enter the serial number of the playlist you want to select: "))
                    selected_playlist = search_results.get(choice)
                    if selected_playlist:
                        adding = papi.add_to_playlist(selected_playlist['id'], uris=uris)

                        if adding != 201:
                            print("An error occurred. Try again.")
                        else:
                            playlist_url = f"https://open.spotify.com/playlist/{selected_playlist['id']}"
                            print(f"All tracks added successfully! Check it out {hyperlink('here', playlist_url)}.")
                        return
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print(f"No playlist found with the name '{playlist_to_add}'. Please try again.")

