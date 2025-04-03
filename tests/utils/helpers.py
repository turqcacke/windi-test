from contextlib import contextmanager


@contextmanager
def dummy_contextmanager(*args, **kwargs):
    yield
