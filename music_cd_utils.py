#!/usr/bin/env python3
# @file: wav_cd_utils.py
# @date: 2023-03-12T12:45:24
# @author: Aroldo Souza-Leite
# @description: 
"""
Some utilities for processing files copied from
wav cds.
"""
import pytest
import os, sys, logging
__level__ = logging.DEBUG
from pathlib import Path
import re
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

## to unhide a code block go to the top of the block and press "<f5> h"


class TrackName:
    """
    The track filename should have the form
    Track 1.wav or Track 11.wav.
    """
    ## A compiled regular expression for
    ## describing the track file name.
    regexp = re.compile(
        r"""
        (?P<track>Track\s)  # the trackname begins with 'Track'
        (?P<number>\d{1,2}) # then comes one or two digits
        (?P<suffix>\..+)$   # at the end comes the suffix ('.wav')
        """,
        re.VERBOSE)

    class BadString(ValueError):
        """
        Wrong input for the TrackFilename class.
        """

    def __init__(self, name):
        """
        Expects a standard track file name.
        Raises TrackName.Error if the track
        name doesn't match TrackName.regexp.
        """
        self.match_obj = TrackName.regexp.match(name)
        if self.match_obj is None:
            raise TrackName.BadString(name)
        self.name = name
        self.normalized_name  = None

    def normalize(self):
        """
        Normalizes the track filename using
        filename_re
        """
        self.normalized_name = "normalized " + self.name

def test_TrackName_1():
    """
    tests the TrackName class.
    """
    name = "Track 1.wav"
    name_obj = TrackName(name)
    assert name_obj.name == "Track 1.wav"

def test_TrackName_BadString():
    name = "trash.rubbish"
    try:
        name_obj = TrackName(name)
    except TrackName.BadString as exc:
        pytest.fail(str(exc), pytrace = False)


def filePath_wav_to_mp3(filePath_wav):
    """
    Makes the corresponding  mp3 filePath.
    """
    ## In case filePath_wav is not a Path object:
    filePath_wav = Path(filePath_wav).expanduser().resolve()
    filePath_mp3 = filePath_wav.with_suffix(".mp3")
    _slog.debug("resulting file name:{filename}".format(filename = filePath_mp3.name))
    return filePath_mp3

def test_filePath_wav_to_mp3():
    """
    From something.wav to something.mp3
    """
    filename_wav = "something.wav"
    filePath_mp3 = filePath_wav_to_mp3(filename_wav)
    filename_mp3 = filePath_mp3.name
    assert filename_mp3 == "something.mp3"

def select_filePaths_wav(dirPath_wav, glob_expression = "*_.wav"):
    """
    Selects the wav files to be converted.
    """
    # in case dirPath is not a Path object:
    dirPath_wav = Path(dirPath_wav).expanduser().resolve()
    #
    selected_filePaths_wav = dirPath_wav.glob(glob_expression)
    selected_filePaths_wav = list(selected_filePaths_wav)
    return selected_filePaths_wav


def make_converting_pairs(dirPath_wav, glob_expression = "*_.wav"):
    """
    Make a list of the convertion pairs from wav to mp3 in dirPath_wav.
    """
    selected_filePaths_wav = select_filePaths_wav(dirPath_wav = dirPath_wav,
                                                  glob_expression = glob_expression)
    filePaths_mp3 = [filePath_wav_to_mp3(filePath_wav) for filePath_wav in selected_filePaths_wav]
    converting_pairs = zip(selected_filePaths_wav, filePaths_mp3)
    converting_pairs = list(converting_pairs)
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

def make_dirPath_mp3(dirPath_wav):
    """
    Makes a parallel folder to dirPath with the wav files.
    """
    dirPath_wav = Path(dirPath_wav).expanduser().resolve()
    assert dirPath_wav.is_dir(), \
        "{foldername} is not a folder".format(foldername = dirPath_wav.name)
    dirPath_mp3 = dirPath_wav.with_suffix("._mp3")
    assert (not dirPath_mp3.is_file())
     
    dirPath_mp3.mkdir(exist_ok = True)
    return dirPath_mp3

def test_make_dirPath_mp3():
    """
    Tests make_dirPath_mp3.
    """
    dirPath_mp3 = make_dirPath_mp3("rubbish")
    assert dirPath_mp3.is_dir()


# def move_mp3_to_dirPath_mp3(dirPath_wav, glob_expression = "*.mp3"):
#     """
#     Moves mp3 files from dirPath_wav to a parallel folder
#     dirPath_mp3
#     The parallel folder has ._mp3 as a suffix (note the underscore!)
#     """
#     for source_filePath in dirPath_wav.glob(glob_expression)
#     _slog.debug("moved " + str(filePath_mp3) +  " to \n" + str(new_filePath_mp3))
#     return filePaths_mp3


# def test_move_mp3_to_dirPath_mp3():
#     """
#     Tests move_mp3_to_dirPath_mp3.
#     """
#     dirPath_wav = Path("rubbish").expanduser().resolve()
#     moved_filePaths_mp3 = move_mp3_to_dirPath_mp3(dirPath_wav = dirPath_wav)
#     assert not list(dirPath_wav.glob("*.mp3"))
#     assert set(filePaths_mp3) <= set(list(dirPath_wav.with_suffix("._mp3").) == 

    assert list

def _script():
    """
    Runs if this module is called as a
    Python script.
    """
    _slog.debug(f"testing {__file__}")
    if __level__ >= logging.DEBUG:
        pytest.main(["-v", __file__])


if __name__ == "__main__":
   _script()




