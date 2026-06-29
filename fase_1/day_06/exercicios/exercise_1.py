# Exercise 1.
# Write a context manager class Timer that measures how long the with
# block took. On __enter__ it records the start time; on __exit__ it
# prints the elapsed seconds. Use time.perf_counter(). It does not need
# to suppress exceptions. Then explain, in your own words, what as binds
# to if you write with Timer() as t: — and what you'd have to do to make t useful.

import time

class Timer:
    def __enter__(self):
        self.start_time = time.perf_counter_ns()
        self.end_time = 0.0
        self.elapsed = None
        return self

    def __exit__(self, exc_type, exc, tb):
        self.end_time = time.perf_counter_ns()
        self.elapsed = (self.end_time - self.start_time)/1_000_000
        return False


with Timer() as timer:
    time.sleep(0.5)

print("Elapsed time (outside): ", timer.elapsed)

