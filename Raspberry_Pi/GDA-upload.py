from __future__ import print_function
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from httplib2 import Http
from oauth2client import file, client, tools    
from googleapiclient.http import MediaFileUpload

SCOPES = 'https://www.googleapis.com/auth/drive'
def auth():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service


def upload(filename,filepath,mimetype,drive_service):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                        mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    print (file.get('id'))

upload('Cell-Data.csv','/Users/krishnavenkatramani/Downloads/Cell-Data.csv','text/x-csv',auth())
