import os
import pathlib

def upload(videoname):
    root = pathlib.Path(__file__).parent.resolve()
    filename = 'upload.wav'
    command2wav = f"""ffmpeg -i {videoname} -ac 1 -ar 16000 {filename}"""
    print(filename)
    os.remove(filename)
    os.system(command2wav)
    return filename
