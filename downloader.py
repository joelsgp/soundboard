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
    parser.add_argument("--no-recurse", dest="recursive", action="store_false")
    parser.add_argument("--yt-dl-executable", type=shutil.which, default=YT_DL_NAME)
    return parser


class Args:
    directory: list[Path]
    recursive: bool
    yt_dl_executable: str


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

    if args.recursive:
        all_directories = []
        for directory in args.directory:
            glob = directory.rglob("*")
            all_directories.extend(glob)
    else:
        all_directories = args.directory

    for directory in all_directories:
        print(f"Entering '{directory}'")
        index = Index(directory)
        index.load()
        download_index(index, args.yt_dl_executable)


if __name__ == "__main__":
    main()
