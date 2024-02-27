import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

api_key = "AIzaSyA5E_UfscEUJAcyYn5AUcLMsQpyTC-jbeU"
credentials = ""

def authenticate():
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json',
                scopes=['https://www.googleapis.com/auth/youtube.force-ssl']
            )

            flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
            credentials = flow.credentials
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)

    return credentials

def create_playlist(youtube, title, description):
    request = youtube.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': title,
                'description': description
            },
            'status': {
                'privacyStatus': 'public'  # You can change the privacy status if needed
            }
        }
    )
    response = request.execute()
    return response['id']

def search_video(youtube, query):
    request = youtube.search().list(
        part='id',
        q=query,
        type='video',
        maxResults=1
    )
    response = request.execute()
    if 'items' in response and response['items']:
        return response['items'][0]['id']['videoId']
    else:
        return None

def add_video_to_playlist(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part='snippet',
        body={
            'snippet': {
                'playlistId': playlist_id,
                'position': 0,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
    )
    request.execute()

def create_playlist_from_songs(youtube, playlist_title, playlist_description, song_names):
    # Create a new playlist
    playlist_id = create_playlist(youtube, playlist_title, playlist_description)

    # Add videos to the playlist
    for song_name in song_names:
        video_id = search_video(youtube, song_name)
        if video_id:
            add_video_to_playlist(youtube, playlist_id, video_id)
        else:
            print(f"Video for '{song_name}' not found.")

    print(f"Playlist '{playlist_title}' created successfully with {len(song_names)} songs.")

def main():
    youtube = build('youtube', 'v3', credentials=authenticate())

    # Replace with your desired playlist title, description, and song names
    playlist_title = "My Playlist"
    playlist_description = "A playlist created using the YouTube API"
    song_names = ["Kızılötesi", "Onun Arabası Var", "Gangnam Style"]

    create_playlist_from_songs(youtube, playlist_title, playlist_description, song_names)

if __name__ == '__main__':
    main()
