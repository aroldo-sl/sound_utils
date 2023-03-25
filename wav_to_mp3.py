#!/usr/bin/env python3
# @file: wav_to_mp3.py
# @date: Mon Jun 21 20:18:06 2021
# @description: 
"""
Module docstring.
"""
import logging
__level__ = logging.INFO
import os, sys
from pathlib import Path
from pydub import AudioSegment 
wav = AudioSegment.from_wav


def _make_slog():
    strfmt = """%(levelname)s:%(name)s:%(module)s.%(funcName)s:%(lineno)s
%(message)s"""
    import random, string
    logfmt = logging.Formatter(strfmt)
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setLevel(__level__)
    handler.setFormatter(logfmt)
    fmt_string = "".join(random.sample(string.ascii_letters, 4))
    slog = logging.getLogger(__name__ + "-" + fmt_string)
    slog.addHandler(handler)
    slog.setLevel(__level__)
    return slog
_slog = _make_slog()

def make_songfile_pair(input_songfile):
    """
    Converting pair from wav to mp3
    """
    input_songfile = Path(input_songfile)
    input_songfile = input_songfile.resolve()
    input_parent   = input_songfile.parent
    output_parent  = input_parent.with_suffix(".mp3")
    output_parent.mkdir(exist_ok = True)
    # _slog.info("output folder: {folder}".format(folder=output_parent))
    output_songfile_name  = input_songfile.with_suffix(".mp3").name
    output_songfile       = output_parent.joinpath(output_songfile_name)
    return str(input_songfile), str(output_songfile)

def make_songfile_pairs(input_folder):
    """
    Selects the input songfiles and returns a list of converting
    pairs. (input_songfile, ouput_songfile)
    """
    input_folder = Path(input_folder)
    input_folder = input_folder.resolve()
    songfile_pairs = []
    entries =  input_folder.glob("*.wav")
    for entry in entries:
        number = int(entry.name[:2])
        if number % 2 == 0:
            pair = make_songfile_pair(entry)
            songfile_pairs.append(pair)
    return songfile_pairs

def convert_folder(input_folder):
    """
    Makes the conversion from songfiles in input_folder.
    The selection of songfiles to be converted is coded
    in make_songfile_pairs.
    """
    songfile_pairs = make_songfile_pairs(input_folder = input_folder)
    for input_songfile,  output_songfile in songfile_pairs:
        wav_song = wav(input_songfile)
        wav_song.export(output_songfile, format = "mp3", bitrate="192k")
        print(input_songfile, "\n->", output_songfile)
    return None







def _script():
    """
    Runs if this module is called as a
    Python script.
    """
    _slog.info("Running {script}".format(script=sys.argv[0]))

if __name__ == "__main__":
   _script()

