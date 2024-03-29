from datetime import datetime

from hiro.slot import build_schedule


C0 = "0 * * * *"
C1 = "1 * * * *"
C2 = "2 * * * *"
C3 = "3 * * * *"
START = datetime(1985, 6, 9, 17, 30)
END = datetime(1986, 1, 11, 16, 0)


def test_be_empty_on_no_crontabs():
    assert not list(build_schedule(START, END))


def test_dates_generated():
    assert isinstance(next(build_schedule(START, END, C1)), datetime)


def test_dates_within_range():
    for d in build_schedule(START, END, C1):
        assert END >= d >= START


def test_last_date():
    for d in build_schedule(START, END, C0):
        if d == END:
            return
    assert False


def test_dates_from_all_crontabs():
    assert set(d.minute for d in build_schedule(START, END, C1, C2, C3)) == {1, 2, 3}


def test_not_contain_duplicate_dates():
    assert len(list(build_schedule(START, END, C1))) == len(list(build_schedule(START, END, C1, C1)))
