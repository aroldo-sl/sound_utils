#!/usr/bin/env python3
# @file: convert_all_wav_to_mp3.py
# @date: 2023-04-13T13:43:02
# @author: Aroldo Souza-Leite
# @description: 
"""
inline documentation of this module (99:.\*.py)
"""
import os, sys, logging
__level__ = logging.INFO
from sound_utils import convert_all_wav_to_mp3


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



def _script():
    """
    Runs if this module is called as a
    Python script.
    """
    source_dirPath = sys.argv[0]
    suffix = ".wav"
    _slog.info(f"converting {suffix} files from {source_dirPath}")


if __name__ == "__main__":
   _script()


# yasnippet: 

