import sys
sys.path.append("../discogs-to-youtube/config")
from config import *
sys.path.append("../discogs-to-youtube/utils")
import discogs_utils
import youtube_utils


def main():
    test_release_ids = [549650,5311199,5311199,1502385,3099029]
    print("Starting process...")
    playlist_id = config['youtube']['playlist_id']
    release_ids = discogs_utils.get_releases("DJFleaMarket")
    releases = [discogs_utils.discogs.release(release_id) for release_id in release_ids ] # get releases
    releases = discogs_utils.filter_releases(releases=releases, genre="Electronic")
    releases = sorted(releases, key=discogs_utils.get_scarcity_quotient, reverse=True)

    video_urls = [discogs_utils.get_youtube_urls(release) for release in releases]
    print("Getting video IDs from video URLs")
    ids = set([])
    for urls in video_urls:
        ids.update(set([youtube_utils.get_id_from_url(url) for url in urls]))

    ids = set(filter(lambda x: len(x) > 0, ids))
    max_google_calls = 200
    google_calls = 0
    for video_id in ids:
        if google_calls < max_google_calls:
            google_calls += 1
            youtube_utils.add_video_to_playlist(video_id, playlist_id, write=True)
        else:
            print(f"Max calls to google exceeded. Skipping POST request for video ID [{video_id}]")



if __name__ == '__main__':
    main()