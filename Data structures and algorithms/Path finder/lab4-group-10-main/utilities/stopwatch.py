import time


class Stopwatch:
    """
    A simple class for measuring the time it takes to run some code.
    If you want to do some serious timing you should consider using
    the `timeit` module instead.
    """
    _start: float

    def __init__(self):
        self.reset()

    def reset(self):
        """Resets the elapsed time to 0."""
        self._start = time.perf_counter()

    def elapsed_time(self):
        """Returns the elapsed time in seconds after last reset."""
        now = time.perf_counter()
        return now - self._start

    def finished(self, task: str):
        """Prints a timing report and resets the elapsed time."""
        print(f"{task} took {self.elapsed_time():.2f} seconds.")
        self.reset()

