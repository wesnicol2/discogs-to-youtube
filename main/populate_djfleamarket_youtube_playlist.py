

import sys
sys.path.append("../config")
from config import *
sys.path.append("../utils")
import discogs_utils
import youtube_utils


def main():
    print("Starting process...")
    playlist_id = config['youtube']['playlist_id']
    releases = discogs_utils.get_releases()
    video_urls = discogs_utils.get_youtube_urls(releases) 
    print("Getting video IDs from video URLs")
    ids = [youtube_utils.get_id_from_url(url) for url in video_urls]
    ids = list(filter(lambda x: len(x) > 0, ids))
    ids = list(unique_everseen(ids))
    for video_id in ids:
        youtube_utils.add_video_to_playlist(video_id, playlist_id)
        

if __name__ == '__main__':
    main()