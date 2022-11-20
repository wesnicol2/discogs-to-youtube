import requests
import json
import re
from more_itertools import unique_everseen
import time
from oauth2client import client, GOOGLE_TOKEN_URI, GOOGLE_REVOKE_URI
import httplib2

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

import sys
sys.path.append("../config")
from config import *

CONFIG_DIR = "../config"
SECRETS_DIR = f"{CONFIG_DIR}/secrets"

GOOGLE_SECRETS_CONFIG_FILEPATH = f"{SECRETS_DIR}/google-secrets.json"
STORED_CREDENTIALS_FILEPATH = f"{SECRETS_DIR}/stored-credentials.json"

def main():
    # INPUTS

    # get your Discogs API token from https://www.discogs.com/settings/developers
    username = config['discogs']['username']
    token = config['discogs']['token']

    # must be larger than your discogs collection
    items_per_page = config['items_per_page']

    # choose a unique app name for the user agent
    app_name = config['app_name']

    # playlist ID can be found in your playlist URL
    playlist_id = config['youtube']['playlist_id']

    # Required Google authorization 
    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube"]

    print("Starting process")

    path = "https://api.discogs.com"
    headers = {"User-Agent": "{app_name}/1.0".format(app_name=app_name)}
    sleep = 2
    collection_path = "/users/{username}/collection/folders/0/releases".format(username=username)


    collection_url = "{path}{collection_path}?token={token}&per_page={per_page}".format(
        path=path,
        collection_path=collection_path,
        token=token,
        per_page=items_per_page)

    print(f"Getting releases from collection url: {collection_url}")

    releases = requests.get(collection_url).json()["releases"]

    with open("full_collection.json", "w") as fp:
        json.dump(releases, fp)

    print("Getting release IDs for collection")
    release_ids = [release["id"] for release in releases]


    full_collection_details = []
    video_urls = []

    for release_id in release_ids:
        print("Getting videos for {id}".format(id=release_id))
        release_url = "{path}/releases/{id}?token={token}".format(
            path=path,
            id=release_id,
            token=token)
        try:
            release_json = requests.get(release_url).json()
            release_videos = release_json["videos"]
            release_urls = [video["uri"] for video in release_videos]
            release_urls = [release_urls[0]]
            video_urls += release_urls
        except KeyError:
            None
        time.sleep(sleep)

    # serialise full collection info
    print("Serializing full collection info")
    with open("full_collection_details.json", "w") as fp:
        json.dump(full_collection_details, fp)


    def get_id(url):
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


    print("Getting video IDs from video URLs")
    ids = [get_id(url) for url in video_urls]
    ids = list(filter(lambda x: len(x) > 0, ids))
    ids = list(unique_everseen(ids))

    
    credentials = authorize_credentials(secrets_filepath=GOOGLE_SECRETS_CONFIG_FILEPATH, scopes=scopes)

    print("Refreshing Google credentials")
    credentials.refresh(httplib2.Http())
    access_token = credentials.get_access_token()[0]

    path = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&access_token={access_token}".format(access_token=access_token)

    for video_id in ids:
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
        request = requests.post(
            path,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'})

####################################### -- FUNCTIONS -- #####################################################

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



if __name__ == '__main__':
    main()