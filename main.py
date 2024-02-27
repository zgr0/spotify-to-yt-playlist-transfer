from spotify import *
from youtube import *

spotify_client_id=""
spotify_client_secret=""
youtube = build('youtube', 'v3', credentials=authenticate())
spotify_playlist_id=input("spotify playlist id:")
access_token,expiration_time=get_access_token(spotify_client_id,spotify_client_secret)
access_token, expiration_time = get_or_refresh_token(spotify_client_id,spotify_client_secret, access_token, expiration_time)
    # Replace with your desired playlist title, description, and song names
playlist_title,playlist_description = get_playlist_name_and_description(spotify_playlist_id,access_token)
    
song_names = get_playlist_tracks(spotify_playlist_id,access_token)
create_playlist_from_songs(youtube, playlist_title, playlist_description, song_names)
