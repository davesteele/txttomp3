import pytest
from time import sleep
from collections import namedtuple
from timeit import default_timer as timer
from txttomp3.txttomp3 import rate_limit


@pytest.mark.parametrize("mintime,maxtime,sleeptime,args", [
        (0, 0.001, 0, [0]),
        (.004, .006, 0, [.005]),
        (.004, .006, 0, [.005, .002]),
        (.004, .006, 0, [.002, .005]),
        (.004, 0.006, .005, [0]),
        (.004, 0.006, .005, [.005]),
        (.004, 0.006, .003, [.005]),
    ]
)
def test_rate_limit(mintime, maxtime, sleeptime, args):
    start = timer()

    with rate_limit(*args):
        sleep(sleeptime)

    end = timer()
    duration = end - start

    assert(duration > mintime)
    assert(duration < maxtime)


