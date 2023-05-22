#!/usr/bin/env python

import json
import subprocess
from argparse import ArgumentParser
from pathlib import Path


INDEX_NAME = "index.json"

Index = dict[str, str]


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
    video_title = filepath.name
    try:
        video_id = get_purl(filepath)
    except (KeyError, subprocess.CalledProcessError):
        return
    index[video_id] = video_title


def index_directory(directory: Path, recurse: bool = True):
    print(f"Entering '{directory}'")
    try:
        index = read_index(directory)
    except FileNotFoundError:
        index = {}

    files_indexed = 0
    for p in directory.iterdir():
        if p.name.startswith("."):
            # ignore hidden entries
            pass
        elif recurse and p.is_dir():
            index_directory(p)
        elif p.is_file():
            index_file(index, p)
            files_indexed += 1

    print(f"'{directory}': {len(index)}/{files_indexed}")

    write_index(index, directory)


# todo make into an index Class
def read_index(directory: Path) -> Index:
    index_path = directory.joinpath(INDEX_NAME)
    with open(index_path, "r", encoding="utf-8") as fp:
        index = json.load(fp)
    return index


def write_index(index: Index, directory: Path):
    index_path = directory.joinpath(INDEX_NAME)
    with open(index_path, "w", encoding="utf-8") as fp:
        json.dump(index, fp, ensure_ascii=False, indent=4, sort_keys=True)
        fp.write("\n")


def main():
    parser = get_parser()
    args = parser.parse_args()
    for directory in args.directory:
        index_directory(directory)


if __name__ == "__main__":
    main()
