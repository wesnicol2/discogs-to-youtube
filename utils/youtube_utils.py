import re
import requests
import httplib2
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

import sys
sys.path.append("../discogs-to-youtube/config")
from config import *

# Global Youtube API variables
# Required Google authorization 
scopes = [
    "https://www.googleapis.com/auth/youtube.readonly", 
    "https://www.googleapis.com/auth/youtube"
    ]

# Configuration Variables
playlist_id = config['youtube']['playlist_id']

def get_id_from_url(url):
    if "youtube" in url:
        if "attribution" in url:
            try:
                video_id = re.search("%3D(.*)\%26", url).group(1)
            except Exception:
                print(url)
                video_id = ""
        else:
            try:
                video_id = re.search("(\?|\&)(v|ci)=(.*)", url).group(3)
            except Exception:
                print(url)
                video_id = ""
    else:
        try:
            video_id = re.search("\.be\/(.*)", url).group(1)
        except Exception:
                print(url)
                video_id = ""
    return video_id


def add_video_to_playlist(video_id, playlist_id, write=False):
    path = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&access_token={access_token}".format(access_token=access_token)
    payload = { 
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "videoId": video_id,
                    "kind": "youtube#video"
                }
            }
        }

    print(f"Making POST request to add video ID {video_id} to playlist ID: {playlist_id}")
    
    # FOR DEBUGGING
    # print(f"URL: {path}")
    # print(f"data: ")
    # print(json.dumps(payload))

    if write: 
        response = requests.post(
        path,
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'})
        print(f"Response Code: {response.status_code}")
    else:
        print(f"Request not sent - write = [{write}]")


# # # # # # # # Setup # # # # # # # # # # #

# Start the OAuth flow to retrieve credentials
def authorize_credentials(secrets_filepath, scopes):
    print("Authorizing Google Credentials")
    print(f"Secrets filepath: {secrets_filepath}")
    print("Scopes:")
    for scope in scopes:
        print(f"\t{scope}")

    storage = Storage(STORED_CREDENTIALS_FILEPATH)
    # Fetch credentials from storage
    credentials = storage.get()
    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(secrets_filepath, scope=scopes)
        http = httplib2.Http()
        credentials = run_flow(flow, storage, http=http)
    return credentials


credentials = authorize_credentials(secrets_filepath=GOOGLE_SECRETS_CONFIG_FILEPATH, scopes=scopes)
credentials.refresh(httplib2.Http())
access_token = credentials.get_access_token()[0]