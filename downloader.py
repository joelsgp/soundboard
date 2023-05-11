#!/usr/bin/env python

import json
from pathlib import Path

import yt_dlp as yt_ylp
import yt_dlp.utils

from indexer import INDEX_NAME, Index, get_parser


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

    index = read_index(directory)
    video_ids = index.keys()
    if video_ids:
        output = directory.joinpath(DEFAULT_OUTTMPL)
        argv = [
            f"--format={FORMAT}",
            "--extract-audio",
            f"--audio-format={AUDIO_FORMAT}",
            f"--output={output}",
        ]
        argv.extend(f"https://youtube.com/watch?v={k}" for k in index.keys())

        yt_ylp._real_main(argv=argv)


def read_index(directory: Path) -> Index:
    index_path = directory.joinpath(INDEX_NAME)
    with open(index_path, "r") as fp:
        index = json.load(fp)
    return index


def main():
    parser = get_parser()
    args = parser.parse_args()
    for directory in args.directory:
        download_directory(directory)


if __name__ == "__main__":
    main()