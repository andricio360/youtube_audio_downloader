# 🎵 YouTube Audio Downloader by Date

This Python script allows you to **download audio files from videos** posted on a specific **YouTube channel** within a **custom date range**. It uses the **YouTube Data API v3** and `yt-dlp` to extract audio in MP3 format.

## 🚀 Features

- Download audio from all videos posted by a channel in a date range.
- Specify the start and end dates via command-line arguments.
- Automatically defaults the end date to today if not provided.
- Interactive prompt for start date if missing.
- Outputs MP3 audio files with original video titles.

---

## 🧰 Requirements

- Python 3.7+
- A Google Developer API Key with access to the **YouTube Data API v3**
- `ffmpeg` installed and available in your system's path

### 🔧 Install dependencies

```bash
pip install -r requirements.txt
```

### 📦 Required Libraries
requirements.txt should contain:
```plaintext
google-api-python-client
pytube
yt-dlp
python-dotenv
```

## 📁 Setup

1.	Create a .env file in the root directory and add your API key:
    API_KEY=your_youtube_api_key_here

2.	Ensure ffmpeg is installed (used by yt-dlp for audio conversion):

### macOS (Homebrew)
    brew install ffmpeg

### Ubuntu
sudo apt install ffmpeg

## ▶️ Usage

CLI Example
```bash
python main.py --handle @ZILISULTRA --start-date 2025-04-04
```

### Command Line Arguments
- `--handle`: The YouTube channel handle (e.g., @ZILISULTRA). (Not Required)
- `--start-date`: The start date in YYYY-MM-DD format (e.g., 2025-04-04). (Required)
- `--end-date`: The end date in YYYY-MM-DD format (default is today). (Optional, defaults to today)

## 📦 Output

Downloaded audio files will be saved as .mp3 in the downloaded_audios/ folder with the video titles as filenames.