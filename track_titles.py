#!/usr/bin/env python3
# @file: track_titles.py
# @date: 2023-03-25T22:17:02
# @author: Aroldo Souza-Leite
# @description: 
"""
Retriev the track titles from .yaml files and
rename the track files correspondingly.
"""
import os, sys, logging
from pathlib import Path
import pytest
from pprint import pprint, pformat
from yaml import load, Loader, dump, Dumper
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

def retrieve_data_from_yaml(yamlPath):
    """
    Retrieves the track titles from a yaml file,
    """
    yamlPath = Path(yamlPath).expanduser().resolve()
    if not (yamlPath.is_file() and yamlPath.suffix == ".yaml"):
        raise ValueError("{yaml_filename} is not a yaml file.".format(yamlPath = yamlPath.name))
    data = None
    with yamlPath.open() as yaml_stream:
        data = load(yaml_stream, Loader)
    return data

def select_original_trackPaths(trackDirPath, suffix = ".wav"):
    """
    Selects and orders the original track paths.
    """
    trackDirPath=(Path(trackDirPath)).expanduser().resolve()
    if not trackDirPath.is_dir():
        msg = "{d} is not a directory".format(d = trackDirPath)
        raise FileNotFoundError(msg)
    trackPaths = []
    trackPaths = list(trackDirPath.glob("*{suffix}".format(suffix = suffix)))
    trackPaths.sort()
    return trackPaths


def test_select_original_trackPaths():
    """
    Tests select_original_trackPaths on a concrete directory.
    """
    trackDirPath = Path("octo-Musiksammlung/HL/HL0012-essential-jazz-classics")
    trackPaths = select_original_trackPaths(trackDirPath)
    assert type(trackPaths) is list
    return trackPaths
    
def make_renaming_pairs(yamlPath, trackDirPath, suffix = ".wav"):
    """
    Makes the renaming pairs.
    """
    trackPaths = select_original_trackPaths(trackDirPath = trackDirPath,
                                            suffix = suffix)
def test_make_renaming_pairs():
    """
    uses test_select_original_trckPaths.
    """
    test_select_original_trackPaths()


def test_select_original_trackPaths_error():
    """
    Tests the FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError) as fnfe:
        tracks = select_original_trackPaths("xy")
    _slog.debug(fnfe.value)
    assert True


def test_retrieve_data_from_yaml(tmp_yamlPath = None):
    """
    Uses a test yaml file.
    """
    # setup
    if tmp_yamlPath is None:
        tmp_yamlPath = Path("HL._yaml/HL0013-john-coltrane.yaml").expanduser().resolve()
    _slog.debug("testing on {yaml_filename}".format(
        yaml_filename = "HL0013-john-coltrane.yaml"))
    if not tmp_yamlPath.is_file():
        raise FileNotFoundError(str(tmp_yamlPath))
    #
    data = retrieve_data_from_yaml(yamlPath = tmp_yamlPath)
    assert type(data) is dict
    assert data["folder"] == "HL0013-john-coltrane"

# # @pytest.mark.xfail(reason = "this test must fail")
# def test_x():
#     raise Exception("failing on purpuse")  

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

