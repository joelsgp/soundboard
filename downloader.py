#!/usr/bin/env python

from pathlib import Path

import yt_dlp as yt_ylp
import yt_dlp.utils

import indexer


# don't allow video
FORMAT = "bestaudio"
# allow video
# FORMAT = "bestaudio*"
# soundux doesn't support ogg or opus >:(
AUDIO_FORMAT = "mp3"
DEFAULT_OUTTMPL = yt_dlp.utils.DEFAULT_OUTTMPL["default"]


def download_directory(directory: Path, recurse: bool = True):
    for p in directory.iterdir():
        if recurse and p.is_dir():
            download_directory(p)

    outtmpl = directory.joinpath(DEFAULT_OUTTMPL)

    index = indexer.read_index(directory)
    video_ids = []
    for k, v in index.items():
        # todo change
        dest_path = directory.joinpath(
            DEFAULT_OUTTMPL % {"title": v, "id": k, "ext": AUDIO_FORMAT}
        )
        # if False and dest_path.is_file():
        if dest_path.is_file():
            print(f"Already downloaded: {dest_path}")
        else:
            video_ids.append(k)

    if video_ids:
        argv = [
            "--embed-metadata",
            f"--format={FORMAT}",
            "--extract-audio",
            f"--audio-format={AUDIO_FORMAT}",
            f"--output={outtmpl}",
        ]
        # argv.extend(f"https://youtube.com/watch?v={vid}" for vid in video_ids)
        argv.extend(video_ids)
        print(argv)

        # todo switch to subprocess
        yt_ylp._real_main(argv=argv)


def main():
    parser = indexer.get_parser()
    args = parser.parse_args()
    for directory in args.directory:
        download_directory(directory)


if __name__ == "__main__":
    main()
