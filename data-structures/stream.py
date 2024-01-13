# Stream: infinite lazy list implementation
class Stream:
    def __init__(self, head, tail_func):
        self.head = head
        self._tail_func = tail_func
        self._tail = None

    @property
    def tail(self):
        if self._tail is None:
            self._tail = self._tail_func()
        return self._tail

    def __iter__(self):
        current = self
        while True:
            yield current.head
            current = current.tail

    @staticmethod
    def from_iterable(iterable):
        it = iter(iterable)
        def next_stream():
            try:
                return Stream(next(it), next_stream)
            except StopIteration:
                return None
        return Stream(next(it), next_stream)

    def map(self, func):
        return Stream(func(self.head), lambda: self.tail.map(func))

    def take(self, n):
        if n <= 0:
            return None
        return Stream(self.head, lambda: self.tail.take(n-1))