import json
from pathlib import Path


# soundux doesn't support ogg or opus >:(
AUDIO_FORMAT = "mp3"
AUDIO_SUFFIX = ".mp3"

INDEX_NAME = "index.json"

Index = dict[str, str]


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
