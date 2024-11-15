
# YouTube Playlist Downloader

A tool to download YouTube playlists as MP3 files. This is useful if you have a playlist of music that you want to download and listen to offline.

## Installation and Usage

## Install Playwright
```bash
pip install playwright
```

# Install Google Chrome
# Make sure you have Google Chrome installed as this tool relies on it for web automation.

# Start Google Chrome with remote debugging:
# On Linux:
```bash
google-chrome --remote-debugging-port=8080
```
# On Windows:
```bash
chrome.exe --remote-debugging-port=8080
```
# Use the script to download a YouTube playlist:
# Example usage:
usage: Youtube Playlist Downloader [-h] [-u URL] [-r]

Downloading YouTube playlist

options:
  -h, --help         Show this help message and exit
  -u URL, --url URL  The URL link of the YouTube playlist
  -r, --restore      Restore the previous session
