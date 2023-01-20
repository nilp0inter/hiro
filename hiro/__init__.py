from datetime import datetime

from croniter import croniter
from cytoolz.itertoolz import merge_sorted, unique


def build_schedule(start, end, *crontabs):
    for d in unique(merge_sorted(*(croniter(c, start, ret_type=datetime) for c in crontabs))):
        if d > end:
            return
        yield d


def main():
    print("Hi!")
