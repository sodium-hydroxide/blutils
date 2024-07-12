"""Source code for Utilities"""

from datetime import datetime, UTC
import re
import numpy as np
import numpy.typing as npt


def time_now() -> str:
    """Return ISO 8601 formatted UTC Time

    Returns
    -------
    str
        Time of execution as string
    """
    time = datetime.now(UTC).replace(microsecond=0).isoformat()
    return str(time)


def clean_split(x:str) -> list[str]:
    """Split strings at a space without keeping empty characters"""
    return [
        char for char in x.split(" ")
        if char != ""
    ]


def re_identify_line(
        x:list[str],
        pattern:str
    )-> npt.NDArray[np.int64]:
    """Idendify lines containing features

    Parameters
    ----------
    x : list[str]
        Homogenous list of strings
    pattern : str
        Pattern to search for

    Returns
    -------
    np.ndarray[typing.Any, np.int64]
        Array containing the indices of the file containing the feature
    """
    present_in_line = [bool(re.search(pattern, i)) for i in x]
    line_numbers = np.array(
        [i for i,t in enumerate(present_in_line) if t],
        dtype=np.int64
    )

    return line_numbers
