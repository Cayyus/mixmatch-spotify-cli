from urllib.parse import urlencode
from dotenv import load_dotenv
from typing import Any

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
        self.timeout = httpx.Timeout(360.0, read=None)

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
        
        token = data.get('access_token', '')
        if token == '':
            self.get_access_token()
        else:
            #Check if the token is valid by sending a simple API request
            auth_headers_valid = {'Authorization': f'Bearer {token}'}
            response = httpx.get("https://api.spotify.com/v1/me", headers=auth_headers_valid, timeout=self.timeout)
            if response.status_code == 401:
                self.get_new_access_token()
            else:
                self.access_token = token
            self.access_token = token
            

    def get_access_token(self) -> None:
        """
        Get a one-hour access token to use API endpoints as well as a refresh token
        """
        response = httpx.post(url=f"{self.AUTH_URL}/api/token", headers=self.access_token_headers, data=self.access_token_data, timeout=self.timeout)
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

        response = httpx.post(f"{self.AUTH_URL}/api/token", headers=self.access_token_headers, params=refresh_token_data, timeout=self.timeout)
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
