import httpx

from api.oauth import UserAccessToken

class SpotifyRequest:
    """Base class for sending requests to the Spotify API, used by child classes SpotifyGET and SpotifyPOST"""

    def __init__(self) -> None:
        self.API_URL = "https://api.spotify.com/v1"
        self.access_token = UserAccessToken()
        self.auth_headers = {'Authorization': f'Bearer {self.access_token}'}
        self.timeout = httpx.Timeout(360.0, read=None)
    
    def get_request(self, url:str, params=None) -> httpx.Response:
        """
        Send a GET request to the Spotify Web API
        """
        return httpx.get(url, headers=self.auth_headers, params=params, timeout=self.timeout) if params else httpx.get(url, headers=self.auth_headers, timeout=self.timeout)

    def post_request(self, url:str, data) -> httpx.Response:
        return httpx.post(url, headers=self.auth_headers, json=data, timeout=self.timeout)
