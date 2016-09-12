def some(cls):
    class Some:
        def __eq__(self, other):
            return type(other) == cls

    return Some()
