
import sys
sys.path.append("../config/secrets")
from config_secrets import *

config = {
    "discogs": {
        # get your Discogs API token from https://www.discogs.com/settings/developers
        "username": "wesnicol",
        "token": discogs_token
    },

    # must be larger than your discogs collection
    "items_per_page": 1000,
    
    # choose a unique app name for the user agent
    "app_name": "wes-test-app",

    "youtube": {
        # playlist ID can be found in your playlist URL
        "playlist_id": youtube_playlist_id,
        "scopes": [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube"
        ]

    }
    
}



    