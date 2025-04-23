import os
import argparse
from datetime import datetime
from googleapiclient.discovery import build
from pytube import YouTube
import yt_dlp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found. Please set it in the .env file.")

OUTPUT_DIR = "downloaded_audios"


def get_youtube_service():
    return build("youtube", "v3", developerKey=API_KEY)


def get_channel_id_by_handle(handle):
    youtube = get_youtube_service()
    handle = handle.lstrip("@")
    request = youtube.channels().list(part="id,snippet", forHandle=handle)
    response = request.execute()
    if response.get("items"):
        return response["items"][0]["id"]
    raise ValueError(f"Channel with handle @{handle} not found.")


def get_videos_from_channel(channel_id, start_date, end_date):
    youtube = get_youtube_service()
    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            publishedAfter=f"{start_date}T00:00:00Z",
            publishedBefore=f"{end_date}T23:59:59Z",
            maxResults=50,
            pageToken=next_page_token,
            type="video",
        )
        response = request.execute()
        videos += [
            {"video_id": item["id"]["videoId"], "title": item["snippet"]["title"]}
            for item in response.get("items", [])
        ]
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos


def download_audio(video_id, output_dir):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"🎵 Downloading audio: {url}")
            ydl.download([url])
    except Exception as e:
        print(f"❌ Failed to download {url}. Error: {e}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download YouTube audio clips by date."
    )
    parser.add_argument(
        "--handle", required=False, help="YouTube channel handle (e.g., @ZILISULTRA)"
    )
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)", required=False)
    parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD), defaults to today",
        default=datetime.today().strftime("%Y-%m-%d"),
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.start_date:
        args.start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        if not args.start_date:
            print("Start date is required. Exiting.")
            return
    if not args.handle:
        args.handle = "@ZILISULTRA"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    channel_id = get_channel_id_by_handle(args.handle)
    videos = get_videos_from_channel(channel_id, args.start_date, args.end_date)

    print(
        f"📺 Found {len(videos)} videos between {args.start_date} and {args.end_date}"
    )

    for video in videos:
        download_audio(video["video_id"], OUTPUT_DIR)


if __name__ == "__main__":
    main()
