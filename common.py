import json
import subprocess
import sys

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, TypedDict


# Soundux doesn't support ogg or opus >:(
AUDIO_FORMAT = "mp3"
AUDIO_SUFFIX = ".mp3"
INDEX_NAME = "index.json"


Video = TypedDict("Video", {"title": str, "duration": float, "fingerprint": str, "url": Optional[str]})


def get_purl_ffprobe(file_path: Path) -> str:
    args = [
        "ffprobe",
        "-loglevel",
        "error",
        "-print_format",
        "json",
        "-show_entries",
        "format_tags=purl",
        "-f",
        AUDIO_FORMAT,
        str(file_path),
    ]
    stdout = subprocess.check_output(args, text=True)
    obj = json.loads(stdout)
    purl = obj["format"]["tags"]["purl"]
    return purl


def fpcalc(file_path: Path) -> tuple[float, str]:
    args = [
        "fpcalc",
        "-json",
        str(file_path)
    ]
    stdout = subprocess.check_output(args, text=True)
    obj = json.loads(stdout)
    duration = obj["duration"]
    fingerprint = obj["fingerprint"]
    return duration, fingerprint


class Index:
    def __init__(self, directory: Path, file_path: Path = None):
        self.directory = directory
        if file_path is None:
            file_path = self.directory.joinpath(INDEX_NAME)
        self.file_path = file_path

        self.index: list[Video] = []

    def load(self):
        with open(self.file_path, "r", encoding="utf-8") as fp:
            self.index = json.load(fp)

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as fp:
            json.dump(self.index, fp, ensure_ascii=False, indent=4, sort_keys=True)
            fp.write("\n")

    def index_file(self, file_path: Path):
        try:
            url = get_purl_ffprobe(file_path)
        except subprocess.CalledProcessError:
            print(f"Not a valid '{AUDIO_FORMAT}' file: {file_path}", file=sys.stderr)
            return
        except KeyError:
            # audio is valid but doesn't have url metadata
            url = None

        duration, fingerprint = fpcalc(file_path)
        video = Video(title=file_path.stem, duration=duration, fingerprint=fingerprint, url=url)
        self.index.append(video)

    def index_directory(self, ignore_hidden: bool = True) -> int:

        if ignore_hidden:
            glob = f"[!.]*{AUDIO_SUFFIX}"
        else:
            glob = f"*{AUDIO_SUFFIX}"

        valid_paths = [path for path in self.directory.glob(glob) if path.is_file()]

        files_added = 0
        with ThreadPoolExecutor() as executor:
            for _ in executor.map(self.index_file, valid_paths):
                files_added += 1

        return files_added
