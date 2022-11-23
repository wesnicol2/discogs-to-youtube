import sys
sys.path.append("../discogs-to-youtube/config")
from config import *
sys.path.append("../discogs-to-youtube/utils")
import discogs_utils
import youtube_utils


def main():
    print("Starting process...")
    playlist_id = config['youtube']['playlist_id']
    # release_ids = discogs_utils.get_releases("DJFleaMarket")
    release_ids =list([549650,5311199])
    video_urls = discogs_utils.get_youtube_urls(release_ids) 
    print("Getting video IDs from video URLs")
    ids = [youtube_utils.get_id_from_url(url) for url in video_urls]
    ids = set(filter(lambda x: len(x) > 0, ids))
    for video_id in ids:
        youtube_utils.add_video_to_playlist(video_id, playlist_id)



if __name__ == '__main__':
    main()