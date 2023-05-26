#!/usr/bin/env python

from argparse import ArgumentParser
from pathlib import Path

from common import Index


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


def main():
    args = parse_args()

    if args.recursive:
        all_directories = []
        for directory in args.directory:
            glob = directory.rglob("*")
            inner_directories = (p for p in glob if p.is_dir())
            all_directories.extend(inner_directories)
    else:
        all_directories = args.directory

    for directory in all_directories:
        print(f"Entering '{directory}'")
        index = Index(directory)
        if args.preserve:
            index.load()
        processed, indexed = index.index_directory()
        index.save()
        print(f"'{directory}': {indexed}/{processed}")


if __name__ == "__main__":
    main()
