import sys
import csv
sys.path.append("../discogs-to-youtube/config")
from config import *
sys.path.append("../discogs-to-youtube/utils")
import youtube_utils

max_google_calls = config['youtube']['max_daily_api_calls']
playlist_id = config['youtube']['playlist_id']


def main():
    data = {}
    with open(VIDEO_IDS_FILEPATH, 'r') as file:
        data = dict((rows[0],rows[1]) for rows in csv.reader(file))

    # Assume the CSV file contains 2 rows
    # 1) Video ID
    # 2) Weight (sorting order, largest to smallest)
    sorted_data = (sorted(data.items(), reverse=True, key=lambda kv:
                 (kv[1], kv[0]))) 
    
    for id in sorted_data : youtube_utils.add_video_to_playlist(id[0].strip(), playlist_id, write=False) 


if __name__ == '__main__':
    main()