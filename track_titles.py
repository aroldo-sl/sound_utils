#!/usr/bin/env python3
# @file: track_titles.py
# @date: 2023-03-25T22:17:02
# @author: Aroldo Souza-Leite
# @description: 
"""
Retriev the track titles from .yaml files and
rename the track files correspondingly.
"""
import logging
__level__ = logging.DEBUG
import os, shutil, sys, logging, re
from pathlib import Path
from string import Template
from pprint import pprint, pformat
import pytest
from yaml import load, Loader, dump, Dumper
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

#### test data ###
_test_dirPath = Path("tests").expanduser().resolve()
_test_data_dirPath = _test_dirPath/"data"
_test_data_raw_dirPath = _test_data_dirPath/"raw"
_test_data_processing_dirPath = _test_data_dirPath/"processing"
_track_raw_dirPath = _test_data_raw_dirPath/"HL/HL0049-miles-davies-standards"
_track_processing_dirPath = _test_data_processing_dirPath/"HL/HL0049-miles-davies-standards"
_track_dirPath = _track_processing_dirPath
_yaml_filePath = _test_data_processing_dirPath/"HL._yaml/HL0049-miles-davies-standards.yaml"

_setup_info = \
f"""
test_dirPath\n-> {_test_dirPath}
test_data_dirPath\n-> {_test_data_dirPath}
test_data_raw_dirPath\n-> {_test_data_raw_dirPath}
test_data_processing_dirPath\n-> {_test_data_processing_dirPath}
track_raw_dirPath\n-> {_track_raw_dirPath}
track_processing_dirPath\n-> {_track_processing_dirPath}
track_dirPath\n-> {_track_dirPath}
yaml_filePath\n-> {_yaml_filePath}
"""

def _build_data():
    """
    Setting up the test environment.
    """
    _slog.debug("building test data:\n" + _setup_info)
    shutil.copytree(src = _test_data_raw_dirPath,
                    dst = _test_data_processing_dirPath,
                    dirs_exist_ok = True)
    _slog.debug("test data ready.")
_build_data()



## to unhide a code block got to the block top and press "<f5> h"

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

@pytest.mark.xfail(reason = "The track name has the wrong format.")
def test_TrackName_BadString():
    name = "trash.rubbish"
    try:
        name_obj = TrackName(name)
    except TrackName.BadString as exc:
        pytest.fail(str(exc), pytrace = False)


def retrieve_data_from_yaml(yaml_filePath):
    """
    Retrieves the track titles from a yaml file,
    """
    yaml_filePath = Path(yaml_filePath).expanduser().resolve()
    if not (yaml_filePath.is_file() and yaml_filePath.suffix == ".yaml"):
        raise ValueError("{yaml_filename} is not a yaml file.".format(yaml_filename = yaml_filePath.name))
    data = None
    with yaml_filePath.open() as yaml_stream:
        data = load(yaml_stream, Loader)
    return data

def test_retrieve_data_from_yaml(yaml_filePath = _yaml_filePath):
    """
    Uses a test yaml file.
    """
    yaml_filePath = Path(yaml_filePath).expanduser().resolve()
    if not yaml_filePath.is_file():
        raise ValueError(str(yaml_filePath))
    #
    data = retrieve_data_from_yaml(yaml_filePath = yaml_filePath)
    assert type(data) is dict
    assert data["folder"] == yaml_filePath.with_suffix("").name


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


def make_renaming_pairs(yaml_filePath, track_dirPath, suffix = ".wav"):
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
    yaml_data = retrieve_data_from_yaml(yaml_filePath = yaml_filePath)
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

def test_make_renaming_pairs(yaml_filePath = _yaml_filePath,
                             track_dirPath = _track_dirPath,
                             suffix = ".wav"):
    """
    uses test_select_original_trckPaths.
    """
    renaming_pairs = make_renaming_pairs(yaml_filePath = yaml_filePath,
                                                track_dirPath = track_dirPath,
                                                suffix = suffix)
    _slog.debug("\n" + pformat(renaming_pairs))
    assert True

def rename_tracks(yaml_filePath, track_dirPath, suffix = "-wav"):
    """
    Uses make_renaming_pairs.
    """
    renaming_pairs = make_renaming_pairs(yaml_filePath = yaml_filePath,
                                         track_dirPath = track_dirPath,
                                         suffix = suffix)
    renaming_filePath_pairs = [(track_dirPath/old_name, track_dirPath/new_name)\
                                for (old_name, new_name) in renaming_pairs]
    for filePath, target_filePath in renaming_filePath_pairs:
        filePath.rename(target_filePath)
    return renaming_filePath_pairs

def test_rename_tracks(yaml_filePath = _yaml_filePath,
                         track_dirPath = _track_dirPath,
                         suffix = ".wav"):
    """
    Tests renaming_tracks.
    """
    renaming_filePath_pairs = rename_tracks(yaml_filePath = yaml_filePath,
                                            track_dirPath = track_dirPath,
                                            suffix = suffix)
    _slog.debug(pformat(renaming_filePath_pairs))
    assert True


def make_parallel_mp3_folder(source_dirPath):
    """
    Creates a parallel forder for mp3 sound files.
    returns target_dirPath_mp3.
    """
    source_dirPath = Path(source_dirPath).expanduser().resolve()
    if not source_dirPath.is_dir():
        raise FileNotFoundError("{source_dirPath} is not a folder.".format(
            source_dirPath = str(source_dirPath)))
    target_dirPath_mp3 = source_dirPath.with_suffix("._mp3")
    target_dirpath_mp3 = str(target_dirPath_mp3)
    if target_dirPath_mp3.is_file():
        raise FileExistsError("There is already a file {target_dirpath_mp3}".format(
            target_dirpath_mp3 = target_dirpath_mp3))
    target_dirPath_mp3.mkdir(exist_ok = True)
    _slog.info("mp3 files go to {target_dirpath_mp3}".format(
        target_dirpath_mp3 = target_dirpath_mp3))
    return target_dirPath_mp3

def test_make_parallel_mp3_folder(source_dirPath = _track_dirPath):
    """
    Tests make_parallel_mp3_folder.
    """
    target_dirPath_mp3 = make_parallel_mp3_folder(source_dirPath = source_dirPath)
    assert target_dirPath_mp3.is_dir()
    # tear down
    shutil.rmtree(target_dirPath_mp3)
    return target_dirPath_mp3

@pytest.mark.xfail(raises = FileNotFoundError, reason = "a FileNotFoundError war raised")
def test_make_parallel_mp3_folder_2l(source_dirPath = "xyz"):
    """
    xyz does not exist
    """
    # this should raise FileNotFoundError:
    make_parallel_mp3_folder(source_dirPath = source_dirPath)
    assert True

# @pytest.mark.xfail(raises = FileExistsError)
def test_make_parallel_mp3_folder_3(test_dirPath = "tests"):
    """
    The parallel folders exists as a file.
    """
    test_dirPath = Path(test_dirPath).expanduser().resolve()
    tmp_track_dirPath = test_dirPath/"tmp_track_dirPath"
    tmp_track_dirPath.mkdir(exist_ok = True, parents = True)
    wrong_filePath = tmp_track_dirPath.with_suffix("._mp3")
    wrong_filePath.touch(exist_ok = True)
    msg_fmt = \
"""
temporary track folder:{tmp_track_dirPath}
wrong parallel mp3 file:{wrong_filePath}                
"""
    msg = msg_fmt.format(
        tmp_track_dirPath = tmp_track_dirPath,
        wrong_filePath = wrong_filePath)
    _slog.info(msg)
    try:
        track_dirPath_mp3 = make_parallel_mp3_folder(source_dirPath = tmp_track_dirPath)
    except FileExistsError as err:
        msg = "\n" + "FileExisError:" + str(err)
        _slog.debug(msg)
        pytest.xfail(msg)
    assert True

def convert_wav_to_mp3(source_filePath, target_filePath_mp3):
    """
    Converts a wav sound file to an mp3 sound file.
    """
    source_filePath = Path(source_filePath).expanduser().resolve()
    source_filepath = str(source_filePath)
    _slog.debug("converting {source_filepath}".format(source_filepath = source_filepath))
    assert source_filePath.is_file(), "{source_filepath} is not a file.".format(source_filepath = source_filepath)
    target_filepath_mp3 = str(target_filePath_mp3)
    wav_song = wav(source_filepath)
    wav_song.export(target_filepath_mp3, format = "mp3", bitrate="192k")
    return source_filePath, target_filePath_mp3

def test_convert_wav_to_mp3():
    source_dirPath = _track_dirPath
    source_filePaths = list(_track_dirPath.glob("*.wav"))
    source_filePaths.sort()
    source_filePath = source_filePaths[0]
    target_filePath_mp3 = source_filePath.with_suffix(".mp3")
    convert_wav_to_mp3(source_filePath = source_filePath,
                       target_filePath_mp3 = target_filePath_mp3)
    source_filepath = str(source_filePath)
    target_filepath_mp3 = str(target_filePath_mp3)
    _slog.debug("\nconverting {source_filepath} \n-> {target_filepath_mp3}\n".format(
        source_filepath = source_filepath,
        target_filepath_mp3 = target_filepath_mp3))

    assert target_filePath_mp3.is_file(), \
        "failed to create {target_filepath_mp3}".format(
            target_filepath_mp3 = target_filepath_mp3)
    # tear down
    target_filePath_mp3.unlink()

def make_conversion_filePath_pairs(source_dirPath, suffix = ".wav"):
    """
    File pairs for the conversion of wav sound files to mp3 sound files
    targeted to  a parallel folder.
    """
    source_dirPath = Path(source_dirPath).expanduser().resolve()
    source_dirpath = str(source_dirPath)
    assert source_dirPath.is_dir(), "{source_dirpath} is not a directory".format(source_dirpath = source_dirpath)
    target_dirPath_mp3 = make_parallel_mp3_folder(source_dirPath = source_dirPath)
    source_filePaths = list(source_dirPath.glob("*" + suffix))
    def make_target_filePath(source_filePath):
        target_filename = source_filePath.with_suffix(".mp3").name
        assert type(target_filename) is str
        target_filePath = target_dirPath_mp3/target_filename
    conversion_filePath_pairs = [(source_filePath, make_target_filePath(source_filePath)) \
                                 for source_filePath in source_filePaths]
    return conversion_filePath_pairs

def test_make_conversion_filePath_pairs(source_dirPath = _track_dirPath, suffix = ".wav"):
    """
    Tests make_convertion_filePath_pairs.
    """
    ĉonversion_filePath_pairs = make_conversion_filePath_pairs (source_dirPath = source_dirPath)
    assert True

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

