from datetime import datetime, UTC

def time_now() -> str:
    """Return ISO 8601 formatted UTC Time

    Returns
    -------
    str
        Time of execution as string
    """
    time = datetime.now(UTC).replace(microsecond=0).isoformat()
    return str(time)

