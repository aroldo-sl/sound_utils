#!/usr/bin/env python3
# @file: wav_cd_utils.py
# @date: 2023-03-12T12:45:24
# @author: Aroldo Souza-Leite
# @description: 
"""
Some utilities for processing files copied from
wav cds.
"""
import os, sys, logging
__level__ = logging.DEBUG
from pathlib import Path
from pydub import AudioSegment
wav = AudioSegment.from_wav


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


track_pattern = \
    """
    (?P<track>Track\s)
    (?P<number>\d{1,2})
    (?P<suffix>\..+)$
     """

# def new_track_name(track_name):
#     """
#     From Track 1.wav to 01.wav.
#     From Track 12.wav to 12.wav.
#     """
#     track_number_plus_ext = track_name.split(" ")[1]
#     new_name = "{:0>6}".format(track_number_plus_ext)
#     return new_name

def test_new_track_name():
    """
    Testet es auf Track 1.wav
    """
    old_name = "Track 1.wav"
    new_name = new_track_name(old_name)
    assert new_name == "01.wav"

def test_2_new_track_name():
    """
    Testet es on Track 12.wav
    """
    old_name = "Track 12.wav"
    new_name = new_track_name(old_name)
    assert new_name == "12.wav"


def filePath_wav_to_mp3(filePath_wav):
    """
    Makes the corresponding  mp3 filenamepath.
    """
    ## In case filePath_wav is a file name:
    filePath_wav = Path(filePath_wav).resolve()
    filename_wav = filePath_wav.name
    filePath_mp3 = filePath_wav.with_suffix(".mp3")
    filename_mp3 = filePath_mp3.name
    return filePath_mp3

def test_filePath_wav_to_mp3():
    """
    From something.wav to something.mp3
    """
    filename_wav = "something.wav"

    filePath_mp3 = filePath_wav_to_mp3(filename_wav)
    filename_mp3 = filePath_mp3.name
    assert filename_mp3 == "something.mp3"

def select_filePaths_wav(dirPath, select_even_prefixes = True):
    """
    Selects the wav files to be converted.
    """
    if select_even_prefixes:
        r = 0
    else:
        r = 1
    filePaths_wav = [filePath for filePath in dirPath.glob("*.wav") \
                     if int(filePath.name[:2]) % 2 == r]
    return filePaths_wav


def make_converting_pairs(dirPath, select_even_prefixes = True):
    """
    The converting pairs from wav to mp3 in dirPath.
    """
    filePaths_wav = select_filePaths_wav(dirPath = dirPath)
    filePaths_mp3 = [filePath_wav_to_mp3(filePath_wav) for filePath_wav in filePaths_wav]
    converting_pairs = zip(filePaths_wav, filePaths_mp3)
    return converting_pairs

def convert_wav_to_mp3(filePath_wav, filePath_mp3):
    """
    Converts a wav sound file to an mp3 sound file.
    """
    filePath_wav = Path(filePath_wav).resolve()
    filename_wav = str(filePath_wav)
    _slog.debug(f"converting {filename_wav}")
    assert filePath_wav.is_file(), f"{filename_wav} is not a file."
    filename_mp3 = str(filePath_mp3)
    wav_song = wav(filename_wav)
    wav_song.export(filename_mp3, format = "mp3", bitrate="192k")


def convert_all_wav_to_mp3(dirPath_wav, select_even_prefixes = True):
    """
    Converts all selected wav files to mp3.
    """
    converting_pairs = make_converting_pairs(
        dirPath_wav,
        select_even_prefixes = select_even_prefixes)
    for filePath_wav, filePath_mp3 in converting_pairs:
        convert_wav_to_mp3(filePath_wav, filePath_mp3)


def make_dirPath__mp3(dirPath):
    """
    Makes a parallel folder to dirPath.
    """
    dirPath = Path(dirPath).resolve()
    foldername = str(dirPath)
    assert dirPath.is_dir(), f"{foldername} is not a folder"
    dirPath__mp3 = dirPath.with_suffix("._mp3")
    foldername__mp3 = str(dirPath__mp3)
    assert (not dirPath__mp3.is_file()), f"{foldername__mp3} is a file"
    dirPath__mp3.mkdir(exist_ok = True)
    _slog.info(f"the mp3 files will go to \n{foldername__mp3}")
    return dirPath__mp3

def move_mp3_to_dirPath__mp3(dirPath):
    """
    Moves mp3 files to a parallel folder.
    The parallel folder has ._mp3 as a suffix.
    """
    dirPath = Path(dirPath).resolve()
    foldername = str(dirPath)
    assert dirPath.is_dir(), f"{foldername} is not a folder"
    dirPath__mp3 = make_dirPath__mp3(dirPath)
    all_mp3 = dirPath.glob("*.mp3")
    for filePath_mp3 in all_mp3:
        new_filePath_mp3 = dirPath__mp3/(filePath_mp3.name)
        filePath_mp3.rename(new_filePath_mp3)
        _slog.debug("moved " + str(filePath_mp3) +  " to \n" + str(new_filePath_mp3))



def _script():
    """
    Runs if this module is called as a
    Python script.
    """
    _slog.debug(sys.argv[0])

if __name__ == "__main__":
   _script()




