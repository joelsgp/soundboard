import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


# Soundux doesn't support ogg or opus >:(
AUDIO_FORMAT = "mp3"
AUDIO_SUFFIX = ".mp3"

INDEX_NAME = "index.json"


VideoUrl = str
VideoTitle = str
IndexDict = dict[VideoUrl, VideoTitle]


def get_purl_ffprobe(file_path: Path) -> str:
    args = [
        "ffprobe",
        "-loglevel", "error",
        "-print_format", "json",
        "-show_entries", "format_tags=purl",
        str(file_path),
    ]
    stdout = subprocess.check_output(args, text=True)
    obj = json.loads(stdout)
    purl = obj["format"]["tags"]["purl"]
    return purl


class Index:
    def __init__(self, directory: Path, file_path: Path = None):
        self.directory = directory
        if file_path is None:
            file_path = self.directory.joinpath(INDEX_NAME)
        self.file_path = file_path

        self.index: IndexDict = {}

    def load(self):
        with open(self.file_path, "r", encoding="utf-8") as fp:
            self.index = json.load(fp)

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as fp:
            json.dump(self.index, fp, ensure_ascii=False, indent=4, sort_keys=True)
            fp.write("\n")

    def index_file(self, file_path: Path):
        try:
            video_url = get_purl_ffprobe(file_path)
        except KeyError:
            return
        video_title = file_path.stem
        self.index[video_url] = video_title

    def index_directory(self, ignore_hidden: bool = True) -> tuple[int, int]:
        files_processed = 0

        valid_paths = []
        for path in self.directory.iterdir():
            files_processed += 1
            if ignore_hidden and path.name.startswith("."):
                pass
            elif path.is_file() and path.suffix == AUDIO_SUFFIX:
                valid_paths.append(path)

        files_added = 0
        with ThreadPoolExecutor() as executor:
            for _ in executor.map(self.index_file, valid_paths):
                files_added += 1

        return files_processed, files_added
