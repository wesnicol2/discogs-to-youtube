import requests
import time
import discogs_client

import sys
sys.path.append("../discogs-to-youtube/config")
from config import *

# Global Discog variables
base_path = "https://api.discogs.com"
delay_between_requests = 1
max_per_page = config['discogs']['max_results_per_page']


def get_scarcity_quotient(release):
    want_count = release.community.want
    have_count = release.community.have
    scarcity = want_count - have_count
    scarcity_quotient = scarcity / (want_count + have_count)
    return scarcity_quotient 

def get_releases(seller_username):
    path = f"{base_path}/users/{seller_username}/inventory?per_page={max_per_page}"
    print(f"Making GET request for inventory of discogs user {seller_username}")
    print(f"URL: {path}")

    release_ids = set()
    while True:
        response = requests.get(path)
        if response.status_code != 200:
            print(f"Response['reason']: [{response.reason}]")
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
    

def get_youtube_urls(release, max_videos=1):
    video_urls = set([])
    release_videos = release.videos
    # release_urls = [video["uri"] for video in release_videos]
    # video_urls += release_urls

    video_urls = set([release_video.data["uri"] for release_video in release_videos[:max_videos]])
    return video_urls


def genre_matches(release, genre):
    print(f"Checking {release.title} genre") # TODO: Remove
    if genre.strip() in release.genres:
        print("MATCH!!")
        return True
    else:
        return False

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
