import sys
import csv
import time # TODO: Remove
sys.path.append("../discogs-to-youtube/config")
from config import *
sys.path.append("../discogs-to-youtube/utils")
import discogs_utils
import youtube_utils


def main():
    print("Starting process...")
    test_release_ids = [549650,5311199,5311199,1502385,3099029]
    release_ids = test_release_ids #discogs_utils.get_releases("DJFleaMarket")
    i = 0 # TODO: Remove
    execution_times = [] # TODO: Remove
    with open(VIDEO_IDS_FILEPATH, 'w', newline='') as file:
        writer = csv.writer(file)
        for release_id in release_ids:
            print(f"i = {i}")
            release = discogs_utils.discogs.release(release_id)
            start = time.time() # TODO: Remove

            if discogs_utils.genre_matches(release=release, genre="Electronic"):
                end = time.time() # TODO: Remove
                execution_times.append((end-start) * 1000) # TODO: Remove
                if i % 50 == 0: # TODO: Remove
                    print(f"Avg genre comparison time = [{sum(execution_times) / len(execution_times)}] after {i+1} iterations") # TODO: Remove
                i = i+1
                scarcity_quotient = discogs_utils.get_scarcity_quotient(release)
                video_urls = discogs_utils.get_youtube_urls(release)
                print("Getting video IDs from video URLs")
                ids = set([])
                for url in video_urls:
                    ids.add(youtube_utils.get_id_from_url(url))
                ids = set(filter(lambda x: len(x) > 0, ids))
                for id in ids:
                    writer.writerow([id,scarcity_quotient])
            else:
                end = time.time() # TODO: Remove
                execution_times.append((end-start) * 1000) # TODO: Remove
                if i % 50 == 0: # TODO: Remove
                    print(f"Avg genre comparison time = [{sum(execution_times) / len(execution_times)}] after {i+1} iterations") # TODO: Remove
                i = i+1
            

if __name__ == '__main__':
    main()