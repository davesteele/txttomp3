import pytest
from time import sleep
from collections import namedtuple
from timeit import default_timer as timer

from txttomp3.txttomp3 import rate_limit


@pytest.mark.parametrize("mintime,maxtime,sleeptime,args", [
        (0, 1, 0, [0]),
        (4, 6, 0, [5]),
        (4, 6, 0, [5, 2]),
        (4, 6, 0, [2, 5]),
        (4, 6, 5, [0]),
        (4, 6, 5, [5]),
        (4, 6, 3, [5]),
        (4, 6, 5, [3]),
    ]
)
def test_rate_limit(mintime, maxtime, sleeptime, args):
    start = timer()

    with rate_limit(*[x/1000.0 for x in args]):
        sleep(sleeptime/1000.0)

    duration = (timer() - start) * 1000

    assert(duration > mintime)
    assert(duration < maxtime)
