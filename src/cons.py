class Cons:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        result = '('
        obj = self
        while True:
            result += str(obj.car)
            if obj.cdr is None:
                break
            result += ' '
            if type(obj.cdr) is not Cons:
                result += f". {obj.cdr}"
                break
            obj = obj.cdr
        
        result += ')'
        return result
    
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
        if self.car is None and value is not None:
            self.car = value
        elif type(self.cdr) is not Cons:
            # basically we ignore the last cdr of an ill-formed list,
            # we're only using this function on lex-time (well-formed) lists anyway
            self.cdr = Cons(value, None)
        else:
            self.cdr.append(value)

    def __len__(self):
        return len(list(self.__iter__()))
    
