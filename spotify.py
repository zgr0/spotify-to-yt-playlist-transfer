import requests
import json
from base64 import b64encode
from datetime import datetime, timedelta

def get_access_token(client_id, client_secret):
    token_url = "https://accounts.spotify.com/api/token"
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = b64encode(credentials.encode()).decode('utf-8')

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
    }
    data = {
        "grant_type": "client_credentials",
    }

    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get('access_token')
        expires_in = token_info.get('expires_in', 3600)
        expiration_time = datetime.now() + timedelta(seconds=expires_in)
        return access_token, expiration_time
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None, None

def get_or_refresh_token(client_id, client_secret, current_token, expiration_time):
    if expiration_time and expiration_time < datetime.now():
        print("Refreshing token...")
        return get_access_token(client_id, client_secret)
    else:
        return current_token, expiration_time

# Replace with your own client ID and client secret
client_id = ""
client_secret = ""

# Initialize variables to store access token and expiration time
access_token, expiration_time = get_access_token(client_id, client_secret)

def get_playlist_tracks(playlist_id, access_token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    playlist_data = response.json()

    # Extracting track names
    track_names = [track['track']['name'] for track in playlist_data['tracks']['items']]
    
    return track_names
def get_playlist_name_and_description(playlist_id,access_token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response=requests.get(url,headers=headers)
    playlist_data=response.json()
    playlist_name=playlist_data['name']
    playlist_description=playlist_data['description']
    return playlist_name,playlist_description
spotify_playlist_id=""
playlist_name,playlist_description=get_playlist_name_and_description(spotify_playlist_id,access_token)
print(playlist_name)
