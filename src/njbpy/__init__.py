"""Minor Utilities Used by Noah Blair

Functions
---------

time_now : () -> str
    Return ISO 8601 formatted UTC Time

clean_split : (str) -> list[str]
    Split strings at a space without keeping empty characters

re_identify_line : (list[str], str) -> NDArray[int64]
    Idendify lines containing features

"""

from ._njbpy import (
    time_now,
    clean_split,
    re_identify_line
)


__all__ = [
    "time_now",
    "clean_split",
    "re_identify_line"
]
