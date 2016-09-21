import os
import subprocess
import sys

from datetime import datetime


def run(filename):
    """
    Platform independent "open" to show URLs on browsers or open the file
    on the right program.
    """
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def pretty_date(seconds):
    """
    Get a datetime object or a int() Epoch timestamp and return a pretty
    string like 'an hour ago', 'Yesterday', '3 months ago', 'just now', etc.
    """

    days = int(seconds / 60.0 / 60.0 / 24.0)
    ago = "ago" if seconds < 0 else ""
    seconds = abs(seconds)
    today = [
        (10, "just now"),
        (60, "%s seconds %s" % (seconds, ago)),
        (120, "one minute %s" % ago),
        (3600, "%s minutes %s" % (seconds / 60, ago)),
        (7200, "an hour %s" % ago),
        (86400, "%s hours %s" % (seconds / 3600, ago)),
    ]
    units = [
        (2, "Yesterday"),
        (7, "%s days %s" % (days, ago)),
        (31, "%s weeks %s" % (days / 7, ago)),
        (365, "%s months %s" % (days / 30, ago)),
        (sys.maxint, "%s years %s" % (days / 365, ago)),
    ]

    unit = days if days > 0 else seconds
    units = units if days > 0 else today
    for value, pretty in units:
        if unit < value:
            return pretty.strip()
