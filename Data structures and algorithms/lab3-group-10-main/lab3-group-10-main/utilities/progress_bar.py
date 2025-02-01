from sys import stderr
from time import time
from typing import TypeVar
from collections.abc import Iterator, Iterable
from types import TracebackType


T = TypeVar("T")

class ProgressBar(Iterable[T]):
    """
    A simple progress bar, inspired by the `tqdm` module.
    For "real" programs, consider installing `tqdm` instead,
    it has many more features (such as nested progress bars).
    """
    # Class-variable to turn on/off all progress bars.
    visible: bool = True

    # Instance variables.
    iterator: Iterator[T]
    description: str
    start_time: float
    total: int
    n: int
    interval: int
    unit: int
    unit_suffix: str
    bar_width: int
    descr_width: int

    def __init__(
        self, iterable: Iterable[T] = (), description: str = "Logging",
        total: int = 0, unit: int = 0,
        bar_width: int = 40, descr_width: int = 25,
    ):
        self.start_time = time()
        self.iterator = iter(iterable)
        self.description = description
        self.total = total
        if not self.total:
            self.total = len(iterable)  # type: ignore
        self.n = 0
        self.interval = max(1, min(self.total//200, 100))
        if unit == 0:
            unit = 1 if self.total < 20_000 else 1_000 if self.total < 20_000_000 else 1_000_000
        self.unit = unit
        if unit == 1:
            self.unit_suffix = " "
        elif unit == 1_000:
            self.unit_suffix = "k"
        elif unit == 1_000_000:
            self.unit_suffix = "M"
        else:
            raise ValueError("Can only handle unit == 1 or 1000 or 1_000_000")
        self.bar_width = bar_width
        self.descr_width = descr_width
        self._print_infoline()

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        try:
            el = next(self.iterator)
        except StopIteration:
            self._print_infoline()
            self._close_infoline()
            raise
        self.n += 1
        if self.n % self.interval == 0:
            self._print_infoline()
        return el

    def __enter__(self) -> 'ProgressBar[T]':
        return self

    def __exit__(self, exc_type: BaseException, exc_val: BaseException, exc_tb: TracebackType):
        self._print_infoline()
        self._close_infoline()
        pass

    def set_value(self, n: int):
        """Sets a new value for the counter. It has to be larger than the old value."""
        if n > self.n:
            self.n = n
            if n % self.interval == 0:
                self._print_infoline()

    def update(self, add: int):
        """Increases the counter by a give number."""
        self.n += add
        if self.n % self.interval == 0:
            self._print_infoline()

    def _print_infoline(self):
        if ProgressBar.visible:
            percent = 0.0
            if self.total > 0:
                percent = self.n / self.total
            hashes = round(percent * self.bar_width)
            pbar = "[" + "=" * hashes + "." * (self.bar_width - hashes) + "]"
            elapsed = time() - self.start_time
            print(
                f"{self.description:{self.descr_width}s} {percent:4.0%} {pbar} "
                f"{self.n/self.unit:6.0f}{self.unit_suffix} "
                f"of {self.total/self.unit:.0f}{self.unit_suffix}  | {elapsed:6.1f} s",
                file=stderr, end="\r", flush=True
            )

    def _close_infoline(self):
        if ProgressBar.visible:
            print(file=stderr)

