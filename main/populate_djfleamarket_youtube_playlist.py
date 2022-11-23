import sys
sys.path.append("../discogs-to-youtube/config")
from config import *
sys.path.append("../discogs-to-youtube/utils")
import discogs_utils
import youtube_utils


def main():
    test_release_ids = [549650,5311199]
    print("Starting process...")
    playlist_id = config['youtube']['playlist_id']
    release_ids = discogs_utils.get_releases("DJFleaMarket")
    releases = [discogs_utils.discogs.release(release_id) for release_id in release_ids ] # get releases
    releases = discogs_utils.filter_releases(releases=releases, genre="Electronic")
    video_urls = [discogs_utils.get_youtube_urls(release) for release in releases]
    print("Getting video IDs from video URLs")
    ids = [youtube_utils.get_id_from_url(url) for url in video_urls]
    ids = set(filter(lambda x: len(x) > 0, ids))
    for video_id in ids:
        youtube_utils.add_video_to_playlist(video_id, playlist_id)



if __name__ == '__main__':
    main()