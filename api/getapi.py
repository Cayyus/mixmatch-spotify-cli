from api.request import SpotifyRequest
from typing import List, Dict

from datetime import datetime

import subprocess


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
        all_albums = []
        next_url = f"{self.API_URL}/me/albums"
        params = {'limit': 50}

        while next_url:
            response = self.get_request(next_url, params=params)
            data = response.json()

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
                    track_duration = track_duration / 60000 # convert to minutes
                    track_data['duration'] = round(track_duration)

                    album_data['tracks'].append(track_data)

                all_albums.append(album_data)

            # Check if there is a next page of albums
            next_url = data.get('next')

        return all_albums
        
    def get_users_playlists(self) -> List[Dict]:
        """
        Get all the playlists saved by the user
        """
        all_playlists = []
        next_url = f"{self.API_URL}/me/playlists"
        params = {'limit': 50}

        while next_url:
            response = self.get_request(next_url, params=params)
            data = response.json()

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

                all_playlists.append(playlist_dict)

            next_url = data.get('next')

            return all_playlists

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
    
    def get_user_top_x(self) -> List:
        """
        Get the user's top tracks and artists
        """
        artists_lst = []
        tracks_lst = []

        artist_params = {
            "limit": 2
        }
        track_params = {
            "limit": 3
        }
        artist_response =  self.get_request(f"{self.API_URL}/me/top/artists", params=artist_params)
        track_response = self.get_request(f"{self.API_URL}/me/top/tracks", params=track_params)

        def parse_response(resp):
           items = resp['items']
           for item in items:
               id = item['id']
               type =  item['type']

               if type == "artist":
                   artists_lst.append(id)
               else:
                   tracks_lst.append(id)
        parse_response(artist_response.json())
        parse_response(track_response.json())

        return artists_lst, tracks_lst
    
    def get_recommendations(self, limit: int = 10) -> List[Dict]:
        """
        Get recommended tracks from Spotify for the user
        """
        tracks_lst = []

        seed_artists, seed_tracks = self.get_user_top_x()
        params = {
            "seed_artists": seed_artists,
            "seed_tracks": seed_tracks,
            "limit": limit
        }

        response = self.get_request(f"{self.API_URL}/recommendations", params=params)
        tracks = response.json()['tracks']

        for track in tracks:
            track_dict = {}

            track_name = track['name']
            track_url = track['external_urls']['spotify']
            track_uri = track['uri']

            album_name = track['album']['name']
            album_url = track['album']['external_urls']['spotify']

            artist_name = track['artists'][0]['name']
            artist_url = track['artists'][0]['external_urls']['spotify']
        
            track_dict['name'], track_dict['url'], track_dict['uri'] = track_name, track_url, track_uri
            track_dict['album_name'], track_dict['album_url'] = album_name, album_url
            track_dict['artist_name'], track_dict['artist_url'] =  artist_name, artist_url
            tracks_lst.append(track_dict)
        
        return tracks_lst

