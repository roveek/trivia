from random import random
from time import perf_counter, sleep


class Timer:

    def __init__(self, precision: int = 4):
        self._start = None
        self._stop = None
        self.precision = int(precision)
        self.start()

    def start(self) -> 'Timer':
        self._start = perf_counter()
        return self

    def stop(self) -> 'Timer':
        self._stop = self.elapsed()
        return self

    def elapsed(self) -> float:
        if self._stop is not None:
            return self._stop
        return perf_counter() - self._start

    def __str__(self):
        message = f'{{time:.{self.precision}f}}'
        return message.format(time=self.elapsed())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        if exc_val:
            return False
        return self


if __name__ == '__main__':
    # t = Timer(precision=1)
    with Timer(precision=9) as t:
        sleep(random())
        print(f'{t}')
    print(f'{t}')
    sleep(1)
    print(f'{t}')
