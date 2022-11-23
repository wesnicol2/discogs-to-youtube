import sys
sys.path.append("../discogs-to-youtube/config/secrets")
from config_secrets import *

CONFIG_DIR = "../discogs-to-youtube/config"
SECRETS_DIR = f"{CONFIG_DIR}/secrets"
GOOGLE_SECRETS_CONFIG_FILEPATH = f"{SECRETS_DIR}/google-secrets.json" # Required
STORED_CREDENTIALS_FILEPATH = f"{SECRETS_DIR}/google-stored-credentials.json" # Will be created if it does not exist

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


        # must be larger than your discogs collection
        "items_per_page": 1000,

        # choose a unique app name for the user agent
        "app_name": "wes_test_app"
        "user_agent" "test_app_discogs_api_example/2.0"
    },

    "youtube": {
        # playlist ID can be found in your playlist URL
        "playlist_id": youtube_playlist_id
    }
    
}

# Assign values dependent on other config values below here
config['discogs']['user_agent'] = f"{config['discogs']['app_name']}_discogs_api_example/2.0"



