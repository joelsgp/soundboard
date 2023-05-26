#!/usr/bin/env python

import shutil
import subprocess
from argparse import ArgumentParser
from pathlib import Path

from common import AUDIO_FORMAT, read_index


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


def download_urls(urls: list[str], outtmpl: str, executable: str):
    args = [executable]
    args.extend(YT_DL_ARGS)
    args.append(f"--output={outtmpl}")
    args.extend(urls)

    subprocess.run(args)


def download_directory(directory: Path, executable: str, recurse: bool = True):
    for p in directory.iterdir():
        if recurse and p.is_dir():
            download_directory(p, executable)

    outtmpl = OUTTMPL

    index = read_index(directory)
    video_ids = []
    for k, v in index.items():
        dest_name = outtmpl % {"title": v, "id": k, "ext": AUDIO_FORMAT}
        dest_path = directory.joinpath(dest_name)
        # if False and dest_path.is_file():
        if dest_path.is_file():
            print(f"Already downloaded: {dest_path}")
        else:
            video_ids.append(k)

    if video_ids:
        outmpl_directory = directory.joinpath(outtmpl)
        download_urls(video_ids, str(outmpl_directory), executable)


def main():
    parser = get_parser()
    args = parser.parse_args()

    executable = shutil.which(YT_DL_NAME)

    for directory in args.directory:
        download_directory(directory, executable)


if __name__ == "__main__":
    main()
