#!/usr/bin/env python

import json
import subprocess
from argparse import ArgumentParser
from pathlib import Path

from common import AUDIO_SUFFIX, Index, write_index


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("directory", nargs="+", type=Path)
    return parser


def get_purl(filepath: Path) -> str:
    args = [
        "ffprobe",
        "-loglevel", "error",
        "-print_format", "json",
        "-show_entries", "format_tags=purl",
        str(filepath),
    ]
    stdout = subprocess.check_output(args, text=True)
    obj = json.loads(stdout)
    purl = obj["format"]["tags"]["purl"]
    return purl


def index_file(index: Index, filepath: Path):
    video_title = filepath.stem
    try:
        video_id = get_purl(filepath)
    except KeyError:
        return
    index[video_id] = video_title


def index_directory(directory: Path, recurse: bool = True):
    print(f"Entering '{directory}'")
    # todo cli option to disable this
    # try:
    #     index = read_index(directory)
    # except FileNotFoundError:
    #     index = {}
    index = {}

    files_indexed = 0
    for p in directory.iterdir():
        if p.name.startswith("."):
            # ignore hidden entries
            pass
        elif recurse and p.is_dir():
            index_directory(p)
        elif p.is_file() and p.suffix == AUDIO_SUFFIX:
            # todo multithreading
            index_file(index, p)
            files_indexed += 1

    print(f"'{directory}': {len(index)}/{files_indexed}")

    write_index(index, directory)


# todo make into an index Class


def main():
    parser = get_parser()
    args = parser.parse_args()
    for directory in args.directory:
        index_directory(directory)


if __name__ == "__main__":
    main()
