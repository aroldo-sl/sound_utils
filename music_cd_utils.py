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


def new_track_name(track_name):
    """
    From Track 1.wav to 01.wav.
    From Track 12.wav to 12.wav.
    """
    track_number_plus_ext = track_name.split(" ")[1]
    new_name = "{:0>6}".format(track_number_plus_ext)
    return new_name

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


def wav_to_mp3(wav_filename):
    """
    Converts wav to mp3.
    """
    ## Erstellt den Namen der mp3-Ausgangsdatei.
    wav_filepath = Path(wav_filename).resolve()
    mp3_filepath = wav_filepath.with_suffix(".mp3")
    print("{wav_filename} --> {mp3_filename}".format(
        wav_filename = wav_filepath.name,
        mp3_filename = mp3_filepath.name))
    
    


def _script():
    """
    Runs if this module is called as a
    Python script.
    """
    _slog.debug(sys.argv[0])

if __name__ == "__main__":
   _script()




