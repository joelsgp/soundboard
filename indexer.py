#!/usr/bin/env python

import json
import re
from argparse import ArgumentParser
from pathlib import Path


INDEX_NAME = 'index.json'
RE_YT_ID = re.compile(r'^(.*)-([a-zA-Z0-9]{11}).*$')

Index = dict[str, str]


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('directory', type=Path)
    return parser


def index_file(index: Index, filepath: Path):
    m = RE_YT_ID.fullmatch(filepath.name)
    if m is not None:
        video_title = m.group(1)
        video_id = m.group(2)
        index[video_id] = video_title


def index_directory(directory: Path):
    print(directory)

    index = {}
    for p in directory.iterdir():
        if p.is_dir():
            index_directory(p)
        elif p.is_file():
            index_file(index, p)

    print(len(index))

    write_index(index, directory)


def write_index(index: Index, directory: Path):
    index_path = directory.parent.joinpath(INDEX_NAME)
    with open(index_path, 'x') as fp:
        json.dump(index, fp)


def main():
    parser = get_parser()
    args = parser.parse_args()
    index_directory(args.directory)


if __name__ == '__main__':
    main()
