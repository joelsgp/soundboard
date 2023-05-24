#!/bin/bash
set -eux
yt-dlp --embed-metadata --format='bestaudio' --extract-audio --audio-format='mp3' --output='%(title)s.%(ext)s' "$@"
