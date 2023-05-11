#!/usr/bin/env python

import json
from pathlib import Path

import yt_dlp as yt_ylp
import yt_dlp.utils

from indexer import INDEX_NAME, Index, get_parser


DEFAULT_OUTTMPL = yt_dlp.utils.DEFAULT_OUTTMPL


def download_directory(directory: Path, recurse: bool = True):
    for p in directory.iterdir():
        if recurse and p.is_dir():
            download_directory(p)

    output = directory.joinpath(DEFAULT_OUTTMPL)
    argv = [
        "--format='bestaudio*'",
        "--extract-audio",
        "--audio-format='opus'",
        f"--output='{output}'",
    ]

    index = read_index(directory)
    argv.extend(f"https://youtube.com/watch?v={k}" for k in index.keys())

    yt_ylp.main(argv=argv)


def read_index(directory: Path) -> Index:
    index_path = directory.joinpath(INDEX_NAME)
    with open(index_path, "r") as fp:
        index = json.load(fp)
    return index


def main():
    parser = get_parser()
    args = parser.parse_args()
    download_directory(args.directory)


if __name__ == "__main__":
    main()
