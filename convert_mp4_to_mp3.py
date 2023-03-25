#!/usr/bin/env python3
# @file: convert_mp4_to_mp3.py
# @date: 2023-03-25T20:56:17
# @author: Aroldo Souza-Leite
# @description: 
"""
Converts mp4 video files to mp3 audio files.
"""
import os, sys, logging
from pathlib import Path
from moviepy.video.io.VideoFileClip import VideoFileClip
__level__ = logging.DEBUG



######################### <_get_slog>   #########
def _get_slog ( level = __level__):
    "Wrapper for the get_slog function"

    import  random, string

    class SLogFormatter(logging.Formatter):
        "A log formatter for SLogHandler"
        fmt = "%(levelname)s:%(name)s:%(module)s.%(funcName)s:%(lineno)s\n%(message)s"
        def __init__(self, fmt = None):
            if fmt is None:
                fmt = SLogFormatter.fmt
            super().__init__(fmt = fmt)

    class SLogHandler(logging.StreamHandler):
        "Simple logging handler."
        def __init__(self, stream = sys.stderr, level = __level__):
            super().__init__(stream = stream)
            self.setLevel(level)
            self.setFormatter(SLogFormatter())

    def get_slog(handler = None, level = __level__):
        "Make a simple logger"
        if handler is None:
            handler = SLogHandler()
        handler.setLevel(level)
        random_string = "".join(random.sample(string.ascii_letters, 4))
        log_name  = __name__ + "-" + random_string
        slog = logging.getLogger(log_name)
        slog.addHandler(handler)
        slog.setLevel(level)
        return slog
    return get_slog(level = level)
######################### </_get_slog>  #########

_slog = _get_slog(level = __level__)

## to unhide a code block got to the block top and press "<f5> h"


def convert(mp4_filePath, output_dirPath = None):
    """
    Converts mp4 to mp3.
    Default output_dirPath is Path.cwd.
    """
    mp4_filePath = Path(mp4_filePath).expanduser().resolve()
    if not mp4_filePath.is_file():
        raise ValueError(str(mp4_filePath) + " is not a file.")
    if output_dirPath is None:
        output_dirPath = Path.cwd()
    output_dirPath.mkdir(exist_ok = True)
    mp3_filePath = mp4_filePath.with_suffix(".mp3")
    mp3_filePath = output_dirPath/(mp3_filePath.name)
    with VideoFileClip(str(mp4_filePath)) as mp4_video:
                       mp3_audio_clip = mp4_video.audio
                       mp3_audio_clip.write_audiofile(str(mp3_filePath))
    msg = "{input_file}\n->{output_file}".format(
        input_file = mp4_filePath,
        output_file = mp3_filePath)
    print(msg)
    


def _script():
    """
    Runs if this module is called as a
    Python script.
    """
    _slog.debug("running {this_script}".format(this_script = __file__))
    # mp4_filePath = sys.argv[1]
    # convert(mp4_filePath)


if __name__ == "__main__":
   _script()


# yasnippet: 

