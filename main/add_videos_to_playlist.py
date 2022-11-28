import sys
sys.path.append("../discogs-to-youtube/config")
from config import *
sys.path.append("../discogs-to-youtube/utils")
import youtube_utils


def main():
    playlist_id = config['youtube']['playlist_id']
    with open(VIDEO_IDS_FILEPATH, 'r') as file:
        for id in file: 
            max_google_calls = 200
            google_calls = 0
            if google_calls < max_google_calls:
                google_calls += 1
                youtube_utils.add_video_to_playlist(id.strip(), playlist_id, write=False)
            else:
                print(f"Max calls to google exceeded. Skipping POST request for video ID [{id}]")


if __name__ == '__main__':
    main()