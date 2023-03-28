#!/usr/bin/env python3
# @file: track_titles.py
# @date: 2023-03-25T22:17:02
# @author: Aroldo Souza-Leite
# @description: 
"""
Retriev the track titles from .yaml files and
rename the track files correspondingly.
"""
import os, sys, logging, re
from string import Template
from pathlib import Path
import pytest
from pprint import pprint, pformat
from yaml import load, Loader, dump, Dumper
__level__ = logging.DEBUG
_track_dirPath = "tests/HL/HL0049-miles-davies-standards"
_yamlPath = "tests/HL._yaml/HL0049-miles-davies-standards.yaml"

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

def retrieve_data_from_yaml(yamlPath):
    """
    Retrieves the track titles from a yaml file,
    """
    yamlPath = Path(yamlPath).expanduser().resolve()
    if not (yamlPath.is_file() and yamlPath.suffix == ".yaml"):
        raise ValueError("{yaml_filename} is not a yaml file.".format(yaml_filename = yamlPath.name))
    data = None
    with yamlPath.open() as yaml_stream:
        data = load(yaml_stream, Loader)
    return data

def test_retrieve_data_from_yaml(yamlPath = _yamlPath):
    """
    Uses a test yaml file.
    """
    yamlPath = Path(yamlPath).expanduser().resolve()
    if not yamlPath.is_file():
        raise FileNotFoundError(str(yamlPath))
    #
    data = retrieve_data_from_yaml(yamlPath = yamlPath)
    assert type(data) is dict
    assert data["folder"] == yamlPath.with_suffix("").name


def select_original_trackPaths(track_dirPath, suffix = ".wav"):
    """
    Selects and orders the original track paths.
    """
    track_dirPath=(Path(track_dirPath)).expanduser().resolve()
    if not track_dirPath.is_dir():
        msg = "{d} is not a directory".format(d = track_dirPath)
        raise FileNotFoundError(msg)
    trackPaths = []
    trackPaths = list(track_dirPath.glob("*{suffix}".format(suffix = suffix)))
    trackPaths.sort()
    return trackPaths

def test_select_original_trackPaths_error():
    """
    Tests the FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError) as fnfe:
        tracks = select_original_trackPaths("xy")
    assert True

def test_select_original_trackPaths():
    """
    Tests select_original_trackPaths on a concrete directory.
    returns track_dirPath, suffix, trackPaths
    """
    track_dirPath = Path(_track_dirPath)
    suffix = ".wav"
    trackPaths = select_original_trackPaths(track_dirPath = track_dirPath, suffix = suffix)
    assert type(trackPaths) is list
    return track_dirPath, suffix, trackPaths


def make_renaming_pairs(yamlPath, track_dirPath, suffix = ".wav"):
    """
    Makes the renaming pairs.
    """
    track_name_re_template  =  Template(
                                  r"""
                                  (?P<prefix>\A\d{2})         # a number formatted to two digits
                                  (?P<hyphen>-)               # the hyphen after the track number
                                  (?P<title>.*?)              # the song title if present
                                  (?P<underscore>_*?)         # maybe an underscore
                                  (?P<suffix>\${suffix}$$)    # the suffix (file name extension)
                                  """)
    track_name_re = track_name_re_template.substitute(suffix = suffix)
    track_name_re = re.compile(track_name_re, re.X)
    trackPaths = select_original_trackPaths(track_dirPath = track_dirPath,
                                            suffix = suffix)
    track_filenames = [trackPath.name for trackPath in trackPaths]
    track_filename_matches = [track_name_re.match(track_filename) for track_filename in track_filenames]
    track_filename_dict = {track_filename_match.group("prefix"):
                              {"prefix":track_filename_match.group("prefix"),
                               "hyphen":track_filename_match.group("hyphen"),
                               "title" :track_filename_match.group("title"),
                               "underscore":track_filename_match.group("underscore"),
                               "suffix": track_filename_match.group("suffix")} 
                             for  track_filename_match in track_filename_matches}
    yaml_data = retrieve_data_from_yaml(yamlPath = yamlPath)
    yaml_tracks_dict = yaml_data["tracks"]
    yaml_tracks_dict = {"{:>02}".format(key):value for key,value in yaml_tracks_dict.items()}
    yaml_tracks_dict = {key:value["ascii"] for key, value in yaml_tracks_dict.items()}
    renaming_pairs = [] 
    for key, value in yaml_tracks_dict.items():
         if key in track_filename_dict:
              old_name_dict = track_filename_dict[key]
              (prefix, hyphen, title, underscore, suffix) = tuple(old_name_dict.values())
              old_name = prefix + hyphen + title + underscore + suffix
              new_name = prefix + hyphen + value + underscore + suffix
              renaming_pairs.append((old_name, new_name))
    return renaming_pairs

   
def test_make_renaming_pairs(yamlPath = _yamlPath,
                             track_dirPath = _track_dirPath,
                             suffix = ".wav"):
    """
    uses test_select_original_trckPaths.
    """
    renaming_pairs = make_renaming_pairs(yamlPath = yamlPath,
                                                track_dirPath = track_dirPath,
                                                suffix = suffix)
    _slog.debug("\n" + pformat(renaming_pairs))
    assert True


def make_parallel_mp3_folder(track_dirPath):
    """
    Creates a parallel forder for mp3 sound files.
    returns track_dirPath_mp3.
    """
    track_dirPath = Path(track_dirPath).expanduser().resolve()
    if not track_dirPath.is_dir():
        raise FileNotFoundError("{track_dirPath} is not a folder.".format(
            track_dirPath = str(track_dirPath)))
    track_dirPath_mp3 = track_dirPath.with_suffix("._mp3")
    if track_dirPath_mp3.is_file():
        raise ValueError("There is already a file {track_dirPath_mp3}".format(
            track_dirPath_mp3 = str(track_dirPath_mp3)))
    track_dirPath_mp3.mkdir(exist_ok = True)
    _slog.info("mp3 files go to {track_dirPath_mp3}".format(
        track_dirPath_mp3 = str(track_dirPath_mp3)))
    return track_dirPath_mp3


def test_make_parallel_mp3_folder(track_dirPath = _track_dirPath):
    """
    Tests make_parallel_mp3_folder.
    """
    track_dirPath_mp3 = make_parallel_mp3_folder(track_dirPath = track_dirPath)
    assert track_dirPath_mp3.is_dir()
    return track_dirPath_mp3

@pytest.mark.xfail(raises = FileNotFoundError)
def test_make_parallel_mp3_folder_2l(track_dirPath = "xyz"):
    """
    xyz does not exist
    """
    # this should raise FileNotFoundError:
    make_parallel_mp3_folder(track_dirPath = track_dirPath)
    assert True

def test_make_parallel_mp3_folder_3(test_dirPath = "tests"):
    """
    The parallel folders exists as a file.
    """
    test_dirPath = Path(test_dirPath).expanduser().resolve()
    tmp_track_dirPath = test_dirPath/"tmp_track_dirPath"
    tmp_track_dirPath.mkdir(exist_ok = True, parents = True)
    _slog.info("{tmp_track_dirPath}=".format(tmp_track_dirPath = tmp_track_dirPath))
    assert True
    


    def setup():
        tmp_track_dirPath= Path("tests/tmp_dirPath")


    
def _script():
    """
    Runs if this module is called as a
    Python script.
    """
    _slog.info("Running " + __file__)
    pytest.main(["-v", __file__])

if __name__ == "__main__":
   _script()


# yasnippet: 

