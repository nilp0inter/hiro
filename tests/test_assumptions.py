from datetime import datetime

from croniter import croniter
from cytoolz.itertoolz import merge_sorted, take


def test_merge_sorted_works_with_croniter():
    base = datetime(1985, 6, 9, 17, 30)
    foo = croniter("0 7 */7 * *", base, ret_type=datetime)
    bar = croniter("0 5 */5 * *", base, ret_type=datetime)

    merged = merge_sorted(foo, bar)

    a, b, c, d, e = take(5, merged)

    assert a == datetime(1985, 6, 11, 5, 0, 0)
    assert b == datetime(1985, 6, 15, 7, 0, 0)
    assert c == datetime(1985, 6, 16, 5, 0, 0)
    assert d == datetime(1985, 6, 21, 5, 0, 0)
    assert e == datetime(1985, 6, 22, 7, 0, 0)
