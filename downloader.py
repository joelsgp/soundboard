#!/usr/bin/env python

import shutil
import subprocess
from argparse import ArgumentParser
from pathlib import Path

from common import AUDIO_FORMAT, Index


# don't allow video
FORMAT = "bestaudio"
# allow video
# FORMAT = "bestaudio*"

OUTTMPL = "%(title)s.%(ext)s"

YT_DL_ARGS = (
    "--embed-metadata",
    f"--format={FORMAT}",
    "--extract-audio",
    f"--audio-format={AUDIO_FORMAT}",
)
YT_DL_NAME = "yt-dlp"


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("directory", nargs="+", type=Path)
    return parser


class Args:
    directory: list[Path]


def parse_args() -> Args:
    parser = get_parser()
    args = Args()
    parser.parse_args(namespace=args)
    return args


def download_urls(urls: list[str], outtmpl: str, executable: str):
    args = [executable]
    args.extend(YT_DL_ARGS)
    args.append(f"--output={outtmpl}")
    args.extend(urls)

    subprocess.run(args)


def download_index(index: Index, executable: str, outtmpl: str = OUTTMPL):
    directory = index.directory

    video_ids = []
    for k, v in index.index.items():
        dest_name = outtmpl % {"title": v, "id": k, "ext": AUDIO_FORMAT}
        dest_path = directory.joinpath(dest_name)
        # if False and dest_path.is_file():
        if dest_path.is_file():
            print(f"Already downloaded: {dest_path}")
        else:
            video_ids.append(k)

    if video_ids:
        outtmpl_directory = directory.joinpath(outtmpl)
        download_urls(video_ids, str(outtmpl_directory), executable)


def main():
    args = parse_args()

    executable = shutil.which(YT_DL_NAME)

    for directory in args.directory:
        for inner_directory in directory.rglob("*"):
            print(f"Entering '{inner_directory}'")
            index = Index(inner_directory)
            index.load()
            download_index(index, executable)


if __name__ == "__main__":
    main()
