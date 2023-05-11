import os
from pathlib import Path


def convert(folder: Path):
    for content in folder.iterdir():
        if content.is_dir():
            convert(content)

        elif content.is_file() and content.suffix == ".wav":
            file_converted = content.with_suffix(".mp3")

            command = f'ffmpeg -y -i "{content}" "{file_converted}"'
            print(command)
            os.system(command)

            content.unlink()


if __name__ == "__main__":
    convert(Path())
