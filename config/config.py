import sys
sys.path.append("../discogs-to-youtube/config/secrets")
from config_secrets import *

BASE_DIR = "../discogs-to-youtube"
CONFIG_DIR = f"{BASE_DIR}/config"
SECRETS_DIR = f"{CONFIG_DIR}/secrets"
GOOGLE_SECRETS_CONFIG_FILEPATH = f"{SECRETS_DIR}/google-secrets.json" # Required
STORED_CREDENTIALS_FILEPATH = f"{SECRETS_DIR}/google-stored-credentials.json" # Will be created if it does not exist
RESOURCES_DIR = f"{BASE_DIR}/resources"
VIDEO_IDS_FILEPATH = f"{RESOURCES_DIR}/video_ids.csv"

config = {
    "discogs": {
        # get your Discogs API token from https://www.discogs.com/settings/developers
        "username": discogs_username,
        "token": discogs_token,

        # Your consumer key and consumer secret generated and provided by Discogs.
        # See http://www.discogs.com/settings/developers . These credentials
        # are assigned by application and remain static for the lifetime of your discogs
        # application. the consumer details below were generated for the
        # 'discogs-oauth-example' application.
        "consumer_key": discogs_consumer_key,
        "consumer_secret": discogs_consumer_secret,

        # With an active auth token, we're able to reuse the client object and request
        # additional discogs authenticated endpoints, such as database search.
        "oauth_token": discogs_oauth_token,
        "oauth_token_secret": discogs_oauth_token_secret,

        # choose a unique app name for the user agent
        "app_name": "wes_test_app",
        "user_agent": "test_app_discogs_api_example/2.0",

        # Discogs API only allows 100 results per page
        "max_results_per_page": 100
    },

    "youtube": {
        # playlist ID can be found in your playlist URL
        "playlist_id": youtube_playlist_id,

        # Max daily API calls (Quota) is 200 per day at the time of writing this
        "max_daily_api_calls": 200
    }
    
}

# Assign values dependent on other config values below here
config['discogs']['user_agent'] = f"{config['discogs']['app_name']}_discogs_api_example/2.0"



