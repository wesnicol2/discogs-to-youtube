import sys
import csv
sys.path.append("../discogs-to-youtube/config")
from config import *
sys.path.append("../discogs-to-youtube/utils")
import discogs_utils
import youtube_utils


def main():
    test_release_ids = [549650,5311199,5311199,1502385,3099029]
    print("Starting process...")
    release_ids = test_release_ids#discogs_utils.get_releases("DJFleaMarket")
    with open(VIDEO_IDS_FILEPATH, 'w') as file:
        writer = csv.writer(file)
        file_header = ["video_id", "scarcity_quotient"]
        writer.writerow(file_header)
        for release_id in release_ids:
            release = discogs_utils.discogs.release(release_id)
            if discogs_utils.genre_matches(release=release, genre="Electronic"):
                scarcity_quotient = discogs_utils.get_scarcity_quotient(release)
                video_urls = discogs_utils.get_youtube_urls(release)
                print("Getting video IDs from video URLs")
                ids = set([])
                for url in video_urls:
                    ids.add(youtube_utils.get_id_from_url(url))
                ids = set(filter(lambda x: len(x) > 0, ids))
                for id in ids:
                    writer.writerow([id,scarcity_quotient])
            

if __name__ == '__main__':
    main()