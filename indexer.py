#!/usr/bin/env python

from argparse import ArgumentParser
from pathlib import Path

from common import Index


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


def main():
    # todo cli option to enable or disable preserving
    # todo cli option for recursing
    args = parse_args()

    for directory in args.directory:
        for inner_directory in directory.rglob("*"):
            print(f"Entering '{inner_directory}'")
            index = Index(inner_directory)
            index.load()
            processed, indexed = index.index_directory()
            index.save()
            print(f"'{inner_directory}': {indexed}/{processed}")


if __name__ == "__main__":
    main()
