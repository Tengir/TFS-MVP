def custom_enumerate(iterable, start=0):
    for i, elem in enumerate(iterable[start:]):
        yield i, elem
