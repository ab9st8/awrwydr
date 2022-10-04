class Cons:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        return f"({' '.join([str(el) for el in self])})"
    
    # With this we can iterate over a cons like a list.
    def __iter__(self):
        yield self.car
        if type(self.cdr) is Cons:
            yield from self.cdr
        elif self.cdr is not None:
            yield self.cdr

    def __reversed__(self):
        return reversed(list(self.__iter__()))

    # Append a value to the end of the linked list.
    def append(self, value):
        if self.cdr is Cons:
            self.cdr.append(value)
        else:
            self.cdr = Cons(value, None) # basically we ignore the last cdr of an ill-formed list

    # Recursive in true functional fashion!
    def length(self):
        if self.cdr is None:
            return 1
        else:
            return 1 + self.cdr.length()
    
