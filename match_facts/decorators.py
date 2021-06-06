from typing import Callable
import functools
import time
import utils


def timer(func: Callable) -> Callable:
    """Decorator that prints the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_taken_in_secs = round(end - start, 3)
        timetaken_fstring = utils.get_timetaken_fstring(num_seconds=time_taken_in_secs)
        print(f"Executed {func.__name__!r} in: {timetaken_fstring}")
        return result
    return wrapper_timer