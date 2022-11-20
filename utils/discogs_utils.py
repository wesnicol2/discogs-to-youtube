import requests
import time
import discogs_client

import sys
sys.path.append("../config")
from config import *

# Global Discog variables
path = "https://api.discogs.com"
delay_between_requests = 1

# Configuration Variables
username = config['discogs']['username']
token = config['discogs']['token']
items_per_page = config['discogs']['items_per_page']
app_name = config['discogs']['app_name']
playlist_id = config['youtube']['playlist_id']


def get_releases():
    print(dir(discogs.release(20017387)))

def get_user_collection_releases():
    print(f"Getting release IDs for user [{username}] collection")
    headers = {"User-Agent": "{app_name}/1.0".format(app_name=app_name)}
    collection_path = "/users/{username}/collection/folders/0/releases".format(username=username)
    collection_url = "{path}{collection_path}?token={token}&per_page={per_page}".format(
        path=path,
        collection_path=collection_path,
        token=token,
        per_page=items_per_page)
    print(f"Getting releases from collection url: {collection_url}")
    releases = requests.get(collection_url).json()["releases"]
    return releases


def get_youtube_urls(releases):
    release_ids = [release["id"] for release in releases] 
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
        time.sleep(delay_between_requests)

def setup():
    global discogs
    discogs = discogs_client.Client(f"{username}_user_agent/1.0", user_token=token)



setup()