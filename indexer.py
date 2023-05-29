#!/usr/bin/env python

from argparse import ArgumentParser
from pathlib import Path

from common import SoundsIndex


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("directory", nargs="+", type=Path)
    parser.add_argument("--no-recurse", dest="recursive", action="store_false")
    parser.add_argument("--no-preserve", dest="preserve", action="store_false")
    return parser


class Args:
    directory: list[Path]
    recursive: bool
    preserve: bool


def parse_args() -> Args:
    parser = get_parser()
    args = Args()
    parser.parse_args(namespace=args)
    return args


def expand_directories(directories: list[Path]):
    all_directories = []
    for directory in directories:
        glob = directory.rglob("*")
        inner_directories = (p for p in glob if p.is_dir())
        all_directories.extend(inner_directories)

    directories.extend(all_directories)


def main():
    args = parse_args()

    directories = args.directory
    if args.recursive:
        expand_directories(directories)

    for directory in directories:
        print(f"Entering '{directory}'")
        index = SoundsIndex(directory)
        if args.preserve:
            index.load()
        indexed = index.index_directory()
        index.save()
        print(f"'{directory}': {indexed}")


if __name__ == "__main__":
    main()
