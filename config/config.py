
import sys
sys.path.append("../config/secrets")
from config_secrets import *

CONFIG_DIR = "../config"
SECRETS_DIR = f"{CONFIG_DIR}/secrets"
GOOGLE_SECRETS_CONFIG_FILEPATH = f"{SECRETS_DIR}/google-secrets.json" # Required
STORED_CREDENTIALS_FILEPATH = f"{SECRETS_DIR}/stored-credentials.json" # Will be created if it does not exist

config = {
    "discogs": {
        # get your Discogs API token from https://www.discogs.com/settings/developers
        "username": discogs_username,
        "token": discogs_token,

        # must be larger than your discogs collection
        "items_per_page": 1000,

        # choose a unique app name for the user agent
        "app_name": "wes-test-app"
    },

    "youtube": {
        # playlist ID can be found in your playlist URL
        "playlist_id": youtube_playlist_id
    }
    
}




    
