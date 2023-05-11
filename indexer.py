#!/usr/bin/env python

import json
import re
from argparse import ArgumentParser
from pathlib import Path


INDEX_NAME = "index.json"
RE_YT_ID = re.compile(r"^(.*) \[([\w\-]{11})\]\..+$")

Index = dict[str, str]


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("directory", nargs="+", type=Path)
    return parser


def index_file(index: Index, filepath: Path):
    m = RE_YT_ID.fullmatch(filepath.name)
    if m is not None:
        video_title = m.group(1)
        video_id = m.group(2)
        index[video_id] = video_title


def index_directory(directory: Path, recurse: bool = True):
    print(f"Entering '{directory}'")

    try:
        index = read_index(directory)
    except FileNotFoundError:
        index = {}
    files_indexed = 0
    for p in directory.iterdir():
        if recurse and p.is_dir():
            index_directory(p)
        elif p.is_file():
            index_file(index, p)
            files_indexed += 1

    print(f"'{directory}': {len(index)}/{files_indexed}")

    write_index(index, directory)


def read_index(directory: Path) -> Index:
    index_path = directory.joinpath(INDEX_NAME)
    with open(index_path, "r") as fp:
        index = json.load(fp)
    return index


def write_index(index: Index, directory: Path):
    index_path = directory.joinpath(INDEX_NAME)
    with open(index_path, "w") as fp:
        json.dump(index, fp, indent=4, sort_keys=True)
        fp.write("\n")


def main():
    parser = get_parser()
    args = parser.parse_args()
    for directory in args.directory:
        index_directory(directory)


if __name__ == "__main__":
    main()
