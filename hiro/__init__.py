from datetime import datetime

from croniter import croniter
from cytoolz.itertoolz import merge_sorted


def build_schedule(start, end, *crontabs):
    for d in merge_sorted(*(croniter(c, start, ret_type=datetime) for c in crontabs)):
        if d > end:
            return
        yield d
