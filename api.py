#FILE CONTAINING ALL THE REQUESTS MADE TO THE SPOTIFY API, INCLUDING THE AUTHORIZATION PROCESS


from urllib.parse import urlencode
from dotenv import load_dotenv
from typing import Any, Dict, List
from datetime import datetime

import httpx
import os
import json
import base64
import webbrowser

load_dotenv('creds.env')

timeout = httpx.Timeout(100.0, read=None)


#<------ OAUTH BASE CLASS -------> 

class SpotifyOAuth(object):
    """
    Base class for OAuth2 authentication with the Spotify Web API, used by child classes UserAuthentication and 
    UserAccessToken
    """
    def __init__(self) -> None:
        self.AUTH_URL = "https://accounts.spotify.com"
        self.CLIENT_ID = os.environ.get('CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get("CLIENT_SECRET")



#<------ USER AUTHENTICATION -------> 


class UserAuthentication(SpotifyOAuth):
    """
    Class for sending authentication prompt to user and getting authorization code
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.SCOPES = [
            "user-read-playback-state",
            "user-read-currently-playing",
            "playlist-read-private",
            "playlist-read-collaborative",
            "playlist-modify-private",
            "playlist-modify-public",
            "user-follow-modify",
            "user-follow-read",
            "user-top-read",
            "user-read-recently-played",
            "user-library-modify",
            "user-library-read",
            'user-read-private',
            'user-read-email'
            ]
        
        self.auth_code_params = {
            'client_id': self.CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': 'https://open.spotify.com/',
            'state': 'anythingreally',
            'scope': ' '.join(self.SCOPES),
            'show_dialog': True
        }

    def send_auth_url(self) -> str:
        """
        Create the url, send to the user and return redirect uri
        """
        auth_url = f"{self.AUTH_URL}/authorize?" + urlencode(self.auth_code_params)
        webbrowser.open(auth_url)
        redirect_url = input("Enter the URL in your browser after you were redirected: ")
        if "https://open.spotify.com/" in redirect_url:
            return redirect_url
        else:
            print("Incorrect URL.")
    
    def get_code(self) -> str:
        """
        Extract the authorization code from the redirect uri sent by user
        """
        authorization_code = self.send_auth_url()
        authorization_code = authorization_code.split('code')[1]
        authorization_code = authorization_code.split('=')[1]
        authorization_code = authorization_code.split('&')[0]
        return authorization_code
    
    def __repr__(self) -> str:
        return self.get_code()


#<------ ACCESS TOKEN -------> 


class UserAccessToken(SpotifyOAuth):
    """
    Get the access token to use API endpoints, valid for one-hour
    """
    def __init__(self) -> None:
        super().__init__()
        self.access_token_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.access_token_data = {
            'grant_type': 'authorization_code',
            'code': UserAuthentication(),
            'redirect_uri': 'https://open.spotify.com/',
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET
        }
        self.access_token = ''
        self.refresh_token = ''
        self.check_access_token()
    
    def check_access_token(self) -> Any:
        """
        Check if the access token is already present and if it is valid
        """
        with open('tokens.json', 'r') as file:
            data = json.load(file)
            file.close()
        
        token = data['access_token']
        if token == '':
            self.get_access_token()
        else:
            #Check if the token is valid by sending a simple API request
            auth_headers_valid = {'Authorization': f'Bearer {token}'}
            response = httpx.get("https://api.spotify.com/v1/me", headers=auth_headers_valid)
            if response.status_code == 401:
                self.get_new_access_token()
            else:
                self.access_token = token
            self.access_token = token
            

    def get_access_token(self) -> None:
        """
        Get a one-hour access token to use API endpoints as well as a refresh token
        """
        response = httpx.post(url=f"{self.AUTH_URL}/api/token", headers=self.access_token_headers, data=self.access_token_data, timeout=timeout)
        token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        json_data = {
            'access_token': token,
            'refresh_token': refresh_token
        }
        
        with open('tokens.json', 'w') as file:
            json.dump(json_data, file, indent=2)
            file.close()
        
        self.access_token = token

    def get_new_access_token(self) -> Any:
        """
        Get a new access token when the current one has expired
        """
        with open("tokens.json", 'r') as file:
            data = json.load(file)
            file.close()
        refresh_token = data['refresh_token']

        credentials = f"{self.CLIENT_ID}:{self.CLIENT_SECRET}"
        credentials_base64 = base64.b64encode(credentials.encode()).decode()

        self.access_token_headers['Authorization'] = f"Basic {credentials_base64}"

        refresh_token_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        response = httpx.post(f"{self.AUTH_URL}/api/token", headers=self.access_token_headers, params=refresh_token_data)
        new_access_token = response.json()['access_token']

        json_data = {
            'access_token': new_access_token,
            'refresh_token': refresh_token
        }
        
        with open('tokens.json', 'w') as file:
            json.dump(json_data, file, indent=2)
            file.close()
        
        self.access_token == new_access_token

    
    def __repr__(self) -> str:
        return self.access_token



#<------SPOTIFY API ENDPOINT REQUESTS------>


class SpotifyRequest:
    """Base class for sending requests to the Spotify API, used by child classes SpotifyGET and SpotifyPOST"""

    def __init__(self) -> None:
        self.API_URL = "https://api.spotify.com/v1"
        self.access_token = UserAccessToken()
        self.auth_headers = {'Authorization': f'Bearer {self.access_token}'}
    
    def get_request(self, url:str, params=None) -> httpx.Response:
        """
        Send a GET request to the Spotify Web API
        """
        return httpx.get(url, headers=self.auth_headers, params=params) if params else httpx.get(url, headers=self.auth_headers)


class SpotifyGET(SpotifyRequest):
    """
    Class containing all the GET method endpoint requests for the Spotify Web API
    """

    def __init__(self) -> None:
        super().__init__()
    
    def get_user_albums(self) -> List[Dict]:
        """
        Get the albums saved by the user
        """
        params = {'limit': 50}
        response = self.get_request(f"{self.API_URL}/me/albums", params=params)
        data = response.json()

        album_list = []

        for album_info in data['items']:
            album_data = {}
            
            dt = album_info['added_at']
            dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
            dt = dt.strftime("%Y-%m-%d %I:%M %p")

            album_data['added_at'] = dt
            album_data['album_api_url'] = album_info['album']['external_urls']['spotify']
            album_data['album_name'] = album_info['album']['name']
            album_data['artists'] = [artist['name'] for artist in album_info['album']['artists']]
            album_data['release_date'] = album_info['album']['release_date']
            album_data['total_tracks'] = album_info['album']['total_tracks']

            tracks_data = album_info['album']['tracks']['items']
            album_data['tracks'] = []

            for track in tracks_data:
                track_data = {}
                track_data['track_name'] = track['name']
                track_data['track_href'] = track['external_urls']['spotify']
                track_data['artists'] = [artist['name'] for artist in track['artists']]
                track_duration = track['duration_ms']
                track_duration = track_duration / 60000 #convert to minutes
                track_data['duration'] = round(track_duration)


                album_data['tracks'].append(track_data)

            album_list.append(album_data)

        return album_list
    
    def get_users_playlists(self) -> List[Dict]:
        """
        Get all the playlists saved by the user
        """
        params = {'limit': 50}
        response = self.get_request(f"{self.API_URL}/me/playlists", params=params)
        data = response.json()

        playlists_list = []  # List to store playlists as dictionaries

        for playlist in data['items']:
            playlist_dict = {
                'description': playlist['description'],
                'external_urls': playlist['external_urls']['spotify'],
                'href': playlist['href'],
                'id': playlist['id'],
                'name': playlist['name'],
                'owner': {
                    'display_name': playlist['owner']['display_name'],
                    'external_urls': playlist['owner']['external_urls']['spotify'],
                    'href': playlist['owner']['href'],
                    'id': playlist['owner']['id'],
                },
                'primary_color': playlist['primary_color'],
                'public': playlist['public'],
                'tracks': {
                    'href': playlist['tracks']['href'],
                    'total': playlist['tracks']['total'],
                },
                'type': playlist['type'],
            }

            playlists_list.append(playlist_dict)

        return playlists_list

    def user_data(self) -> str:
        """
        Getting all data related to the user
        """
        try:
            response = self.get_request(f"{self.API_URL}/me")
            name = response.json()['display_name']
            return name
        except KeyError:
            subprocess.run(['python', 'mixmatch.py'])

            
    def get_user_saved_tracks(self) -> List[Dict]:
        """
        Get all the saved tracks by user
        """

        all_items = []

        # Start with the first set of tracks
        next_tracks = f"{self.API_URL}/me/tracks"

        while next_tracks:
            response = self.get_request(next_tracks)
            response_data = response.json()

            # Update the next_tracks variable for the next iteration
            next_tracks = response_data.get('next')

            # Extract the items and append them to the list
            items = response_data.get('items', [])
            all_items.extend(items)

        return {'items': all_items}

    def get_featured_playlists(self) -> List[Dict]:
        """
        Get featured playlists from Spotify
        """
        playlist_lst = []

        params = {
            'limit': 50
        }
        response = self.get_request(f"{self.API_URL}/browse/featured-playlists", params=params)
        data = response.json()

        playlists_data = {}
        playlists_data['featured_name'] = data['message']
        playlists_data['total_playlists'] = data['playlists']['total']
        playlists_data['playlists'] = []

        for playlist in data['playlists']['items']:
            ind_playlist_data = {}
            ind_playlist_data['name'] = playlist['name']
            ind_playlist_data['description'] = playlist['description']
            ind_playlist_data['url'] = playlist['external_urls']['spotify']
            ind_playlist_data['api_url'] = playlist['href']
            ind_playlist_data['tracks'] = playlist['tracks']['total']
            playlists_data['playlists'].append(ind_playlist_data)

        playlist_lst.append(playlists_data)
        return playlist_lst
    
    def get_featured_tracks(self, pl_arg) -> Dict:
        """
        Get the tracks of the featured playlists
        """
        featured_playlists = self.get_featured_playlists()
        for playlist in featured_playlists[0]['playlists']:
            if pl_arg == playlist['name']:
                api_url = playlist['api_url']
                response = self.get_request(api_url)
                return response.json()

    def get_artist(self, q) -> Dict:
        """
        Get information of an artist, gets the artist with the highest follower count
        """
        highest_count = 0
        artis = None

        artist_dict = {}

        q_params = {'q': q, 'type': 'artist', 'limit': 2}
        response = self.get_request(f"{self.API_URL}/search", params=q_params)
        artist = response.json()['artists']
        items = artist['items']
        for item in items:
            follower_count = item['followers']['total']
            if follower_count > highest_count:
                highest_count = follower_count
                artis = item

        name = artis['name']
        url = artis['external_urls']['spotify']
        followers = artis['followers']['total']
        popularity = artis['popularity']
        genres = artis['genres']

        artist_dict['name'] = name
        artist_dict['url'] = url
        artist_dict['followers'] = '{:,}'.format(followers)
        artist_dict['popularity'] = popularity
        artist_dict['genres'] = [genre.capitalize() for genre in genres]

        # Fetch top tracks
        top_tracks_response = self.get_request(f"{self.API_URL}/artists/{artis['id']}/top-tracks")
        tracks = top_tracks_response.json()['tracks']
        artist_tracks = []
        for track in tracks:
            track_dict = {}
            track_dict['name'] = track['name']
            track_dict['url'] = track['external_urls']['spotify']
            track_dict['album_name'] = track['album']['name']
            track_dict['album_link'] = track['album']['external_urls']['spotify']
            track_dict['rel_date'] = track['album']['release_date'].split('-')[0]
            artist_tracks.append(track_dict)

        artist_dict['tracks'] = artist_tracks

        #Fetch related artists
        related_artists_response = self.get_request(f"{self.API_URL}/artists/{artis['id']}/related-artists")
        related_artists = related_artists_response.json()['artists']
        related_artists_ls = []
        for related_artist in related_artists:
            related_artist_dict = {}
            related_artist_dict['name'] = related_artist['name']
            related_artist_dict['url'] = related_artist['external_urls']['spotify']
            related_artists_ls.append(related_artist_dict)
        
        artist_dict['related_artists'] = related_artists_ls

        return artist_dict
