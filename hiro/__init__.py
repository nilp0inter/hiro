from datetime import datetime
from itertools import cycle
from random import randint
import argparse
import sys

from croniter import croniter
from cytoolz.itertoolz import merge_sorted, unique, drop


def build_schedule(start, end, *crontabs):
    for d in unique(merge_sorted(*(croniter(c, start, ret_type=datetime) for c in crontabs))):
        if d > end:
            return
        yield d


def valid_crontab(expr):
    if not croniter.is_valid(expr):
        raise ValueError("Invalid expression {expr!r}")
    return expr


def build_parser(default_before):
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--schedule", type=valid_crontab, action="append", required=True, help="schedule in crontab format")
    parser.add_argument("-A", "--after", type=datetime.fromisoformat, action="append", required=True, help="minimum date, can be provided several times, the greater will be selected")
    parser.add_argument("-B", "--before", type=datetime.fromisoformat, default=[default_before], action="append", required=False, help="maximum date, can be provided several times, the lesser will be selected")
    parser.add_argument("-r", "--random-seconds", action="store_true", help="randomize seconds")
    parser.add_argument("-R", "--skip-random", default=None, type=int, help="skip random event with a max")
    return parser


def main():
    now = datetime.now(tz=datetime.now().astimezone().tzinfo)

    parser = build_parser(now)

    args = parser.parse_args()
    after = max(args.after)
    before = min(args.before)

    it = build_schedule(after, before, *args.schedule)

    if args.skip_random is not None:
        it = drop(randint(0, args.skip_random), cycle(it))

    for d in it:
        d = d.replace(second=randint(0, 59)) if args.random_seconds else d
        print(d)
        sys.exit(0)
    sys.exit(1)
