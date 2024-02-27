#you need to use this for the first authentication from google api
def authenticate(api_key=None):
    if api_key:
        return googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, ['https://www.googleapis.com/auth/youtube.force-ssl']
        )
        credentials = flow.run_console()
        return googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)
authenticate()