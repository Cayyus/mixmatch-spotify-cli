from api.request import SpotifyRequest


class SpotifyPOST(SpotifyRequest):
    """
    Class for sending POST requests to the Spotify Web API
    """
    def __init__(self) -> None:
        super().__init__()
    
    def create_playlist(self, name: str, desc: str = None, public: bool = False) -> str:
        """
        Create a playlist in Spotify
        """
        data = {
            'name': name,
            'description': desc,
        }
        if public:
            data['public'] = "true"
        else:
            data['public'] = 'false'


        user_id = self.get_request(f"{self.API_URL}/me").json()['id']

        cr_playlist = self.post_request(f"{self.API_URL}/users/{user_id}/playlists", data=data)
        
        if cr_playlist.status_code == 201:
            return cr_playlist.json()['id']
        else:
            return cr_playlist.status_code
    
    def add_to_playlist(self, playlist_id: str, uris: list):
        """
        Add items to a playlist
        """
        data = {
            'uris': uris
        }

        add_resp = self.post_request(f"{self.API_URL}/playlists/{playlist_id}/tracks", data=data)

        return add_resp.status_code
