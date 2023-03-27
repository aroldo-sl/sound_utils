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


def retrieve_data_from_yaml(yaml_filePath):
    """
    Retrieves the track titles from a yaml file,
    """
    yaml_filePath = Path(yaml_filePath).expanduser().resolve()
    if not (yaml_filePath.is_file() and yaml_filePath.suffix == ".yaml"):
        raise ValueError("{yaml_filename} is not a yaml file.".format(yaml_filePath = yaml_filePath.name))
    data = None
    with yaml_filePath.open() as yaml_stream:
        data = load(yaml_stream, Loader)
    return data

def select_original_trackPaths(track_dirPath):
    """
    Selects and orders the original track paths.
    """
    track_dirPath=(Path(track_dirPath)).expanduser().resolve()
    if not track_dirPath.is_dir():
        msg = "{d} is not a directory".format(d = track_dirPath)
        raise FileNotFoundError(msg)
    trackPaths = []
    return trackPaths


def test_select_original_trackPaths():
    """
    Tests the FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError) as fnfe:
        tracks = select_original_trackPaths("xy")
    _slog.debug(fnfe.value)
    assert True


def test_retrieve_data_from_yaml(tmp_yaml_filePath = None):
    """
    Uses a test yaml file.
    """
    # setup
    if tmp_yaml_filePath is None:
        tmp_yaml_filePath = Path("HL._yaml/HL0013-john-coltrane.yaml").expanduser().resolve()
    _slog.debug("testing on {yaml_filename}".format(
        yaml_filename = "HL0013-john-coltrane.yaml"))
    if not tmp_yaml_filePath.is_file():
        raise FileNotFoundError(str(tmp_yaml_filePath))
    #
    data = retrieve_data_from_yaml(yaml_filePath = tmp_yaml_filePath)
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

