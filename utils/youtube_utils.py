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
max_daily_api_calls = config['youtube']['max_daily_api_calls']


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

    if not video_id in get_video_ids_in_playlist(playlist_id):
        if write and add_video_to_playlist.number_of_calls < max_daily_api_calls:
            add_video_to_playlist.number_of_calls += 1 # Keep track of number of calls to google
            response = requests.post( # Quota cost = 50? Think about replacing number_of_calls with quota system
            path,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'})
            print(f"Response Code: {response.status_code}")
        else:
            print(f"Request not sent")
            print(f"Write = [{write}]")
            print(f"Calls made to Youtube API = [{add_video_to_playlist.number_of_calls}] / [{max_daily_api_calls}]")
    else:
        print("Request not sent")
        print(f"Video ID [{video_id}] already exists in playlist [{playlist_id}].")
        


def get_video_ids_in_playlist(playlist_id):
    print(f"Getting videos ids in playlist: [{playlist_id}]")
    path = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&part=snippet&access_token={access_token}"
    response = requests.get(path) # Quota cost = 1? Think about replacing number_of_calls with quota system
    # TODO: Update to allow for pagination
    video_ids = []
    while True:
        status_code = response.status_code
        print(f"Response code: [{status_code}]")
        response = response.json()
        try:
            if status_code == 200: # TODO: Extract request handling into a separate file
                video_ids.extend([video['snippet']['resourceId']['videoId'] for video in response['items']])
                next_page_token = response['nextPageToken']
                response = requests.get(f"{path}&pageToken={next_page_token}")
            elif status_code == 400:
                break
                # TODO: Implement handling for 400 response code
            elif status_code == 401:
                break
                # TODO: Implement handling for 400 response code
            elif status_code == 403:
                if "exceded" in response['error']['message']:
                    print("Youtube API quota has been exceded.")    
                break
            elif status_code == 404:
                print(f"Playlist ID [{playlist_id}] was not found. (Also, double check that that truly was the cause of the 404. There's a small possiblity it could have been caused by a pagination request")
                break
        except KeyError:
            break # KeyError will occur when there is no next page token, indicating the end of pagiation
             
    return video_ids

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
add_video_to_playlist.number_of_calls = 0  # Start API request counter at 0 