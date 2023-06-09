import hashlib
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


Video = TypedDict(
    "Video",
    {
        "title": str,
        "duration": float,
        "md5sum": str,
        "fingerprint": Optional[str],
        "url": Optional[str],
    },
)


def ffprobe(file_path: Path) -> tuple[float, Optional[str]]:
    args = [
        "ffprobe",
        "-loglevel",
        "error",
        "-print_format",
        "json",
        "-show_entries",
        "format=duration:format_tags=purl",
        "-f",
        AUDIO_FORMAT,
        str(file_path),
    ]
    stdout = subprocess.check_output(args, text=True)
    obj = json.loads(stdout)
    duration = float(obj["format"]["duration"])
    try:
        purl = obj["format"]["tags"]["purl"]
    except KeyError:
        purl = None
    return duration, purl


def fpcalc(file_path: Path) -> str:
    args = ["fpcalc", "-plain", "-format", AUDIO_FORMAT, str(file_path)]
    fingerprint = subprocess.check_output(args, text=True, stderr=subprocess.PIPE)
    fingerprint = fingerprint.removesuffix("\n")
    return fingerprint


class SoundsIndex:
    def __init__(self, directory: Path, file_path: Path = None):
        self.directory = directory
        if file_path is None:
            file_path = self.directory.joinpath(INDEX_NAME)
        self.file_path = file_path

        self.index: dict[str, Video] = {}

    def load(self):
        with open(self.file_path, "r", encoding="utf-8") as fp:
            videos = json.load(fp)
        for v in videos:
            self.index[v["title"]] = v

    def save(self):
        videos = list(self.index.values())
        with open(self.file_path, "w", encoding="utf-8") as fp:
            json.dump(videos, fp, ensure_ascii=False, indent=4, sort_keys=True)
            fp.write("\n")

    def index_file(self, file_path: Path):
        try:
            duration, url = ffprobe(file_path)
        except subprocess.CalledProcessError:
            print(f"Not a valid '{AUDIO_FORMAT}' file: {file_path}", file=sys.stderr)
            return

        try:
            fingerprint = fpcalc(file_path)
        except subprocess.CalledProcessError:
            fingerprint = None

        with open(file_path, "rb") as f:
            # noinspection PyTypeChecker
            md5sum = hashlib.file_digest(f, hashlib.md5).hexdigest()

        title = file_path.stem
        video = Video(
            title=title,
            duration=duration,
            md5sum=md5sum,
            fingerprint=fingerprint,
            url=url,
        )
        self.index[title] = video

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
