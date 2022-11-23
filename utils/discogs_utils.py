import requests
import time
import discogs_client
import json

import sys
sys.path.append("../discogs-to-youtube/config")
from config import *

# Global Discog variables
base_path = "https://api.discogs.com"
delay_between_requests = 1
max_per_page = 100 # Discogs API only allows 100 results per page


# Configuration Variables
username = config['discogs']['username']
token = config['discogs']['token']
items_per_page = config['discogs']['items_per_page']
app_name = config['discogs']['app_name']
playlist_id = config['youtube']['playlist_id']

# Common objects
session = requests.Session()


def get_releases(seller_username):
    path = f"{base_path}/users/{seller_username}/inventory?per_page={max_per_page}"
    print(f"Making GET request for inventory of discogs user {seller_username}")
    print(f"URL: {path}")

    release_ids = set()
    while True:
        response = requests.get(path)
        if response.status_code != 200:
            break
        time.sleep(delay_between_requests) # Discogs only allows 60 requests per minute

        response = response.json()
        listings = response['listings']
        for listing in listings:
            # Could filters be added here in the future?
            release = listing['release']
            release_ids.add(release['id'])
            print(f"Retrieved title: [{release['title']}]")

        path = response['pagination']['urls']['next']

    return release_ids
    

def get_user_collection_releases():
    print(f"Getting release IDs for user [{username}] collection")
    headers = {"User-Agent": config['discogs']['user_agent']}
    collection_path = "/users/{username}/collection/folders/0/releases".format(username=username)
    collection_url = "{base_path}{collection_path}?token={token}&per_page={per_page}".format(
        base_path=base_path,
        collection_path=collection_path,
        token=token,
        per_page=items_per_page)
    print(f"Getting releases from collection url: {collection_url}")
    releases = requests.get(collection_url).json()["releases"]
    return releases


def get_youtube_urls(release, max_videos=1):
    video_urls = set([])
    release_videos = release.videos
    # release_urls = [video["uri"] for video in release_videos]
    # video_urls += release_urls

    video_urls = set([release_video.data["uri"] for release_video in release_videos[:max_videos]])
    return video_urls


def filter_releases(releases, genre):
    filtered_releases = set([])
    for release in releases:
        if genre in release.genres:
            print(f"[{release.title}] matches given genre [{genre}]")
            filtered_releases.add(release)    
    return filtered_releases# [release for release in releases if genre in release.genres]



def authenticate():
    # A user-agent is required with Discogs API requests. Be sure to make your
    # user-agent unique, or you may get a bad response.

    # instantiate our discogs_client object.
    global discogs
    discogs = discogs_client.Client(
        user_agent=config['discogs']['user_agent'],
        consumer_key=config['discogs']['consumer_key'],
        consumer_secret=config['discogs']['consumer_secret'],
        token=config['discogs']['oauth_token'],
        secret=config['discogs']['oauth_token_secret']
    )

    # fetch the identity object for the current logged in user.
    user = discogs.identity()

    print("Discogs authentication compmlete.")
    print(' == User ==')
    print(f'    * username           = {user.username}')
    print(f'    * name               = {user.name}')
    

    


def setup():
    authenticate()


setup()
