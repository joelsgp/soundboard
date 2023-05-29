#!/usr/bin/env python

import shutil
import subprocess
from argparse import ArgumentParser
from pathlib import Path

from common import AUDIO_FORMAT, INDEX_NAME, SoundsIndex


# don't allow video
FORMAT = "bestaudio"
# allow video
# FORMAT = "bestaudio*"

OUTTMPL = f"%(title)s.{AUDIO_FORMAT}"

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
    parser.add_argument(
        "--no-skip-existing", dest="skip_existing", action="store_false"
    )
    parser.add_argument("--yt-dl-executable", type=shutil.which, default=YT_DL_NAME)
    return parser


class Args:
    directory: list[Path]
    recursive: bool
    yt_dl_executable: str
    skip_existing: bool


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


def download_index(
    index: SoundsIndex, executable: str, skip_existing: bool = True, outtmpl: str = OUTTMPL
) -> int:
    directory = index.directory

    video_urls = []
    for video in index.index.values():
        if skip_existing:
            dest_name = outtmpl % video
            dest_path = directory.joinpath(dest_name)
            if dest_path.is_file():
                print(f"Already downloaded: {dest_path}")
                continue

        if video["url"] is not None:
            video_urls.append(video["url"])

    if video_urls:
        outtmpl_directory = directory.joinpath(outtmpl)
        download_urls(video_urls, str(outtmpl_directory), executable)

    return len(video_urls)


def main():
    args = parse_args()

    if args.recursive:
        all_directories = []
        for directory in args.directory:
            glob = directory.rglob(INDEX_NAME)
            inner_directories = (p.parent for p in glob)
            all_directories.extend(inner_directories)
    else:
        all_directories = args.directory

    for directory in all_directories:
        print(f"Entering '{directory}'")
        index = SoundsIndex(directory)
        index.load()
        downloaded = download_index(
            index, args.yt_dl_executable, skip_existing=args.skip_existing
        )
        print(f"'{directory}': {downloaded}")


if __name__ == "__main__":
    main()
