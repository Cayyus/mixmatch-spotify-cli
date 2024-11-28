from api.request import SpotifyRequest


class SpotifyPUT(SpotifyRequest):
    def __init__(self) -> None:
        super().__init__()

    def change_playlist_details(self, id: str, name: str = None, desc: str = None, public: bool = False):
        data = {}
    
        if name:
            data['name'] = name
        if desc:
            data['description'] = desc
        if public is not None:  
            data['public'] = public
        
        response = self.put_request(f"{self.API_URL}/playlists/{id}", data=data)
        return response.status_code
