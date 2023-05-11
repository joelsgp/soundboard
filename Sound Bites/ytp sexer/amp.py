from pathlib import Path
import ffmpeg

folder = Path()
for file in folder.listdir():
    stream = ffmpeg.input(str(file))
    stream.output(f'amp/{str(file)}')
    stream.run()
