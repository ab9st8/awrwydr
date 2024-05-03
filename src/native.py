from functools import reduce
from copy import copy

from cons import Cons

# If a function is variadic, like `add`, it means it has to be some sort of
# reducing action, i.e. a function that is defined for some specified number
# of arguments (in the case of basic arithmetic operators, 2), but can be
# recursively applied to a list of arguments of arbitrary length equal to or greater
# than the mentioned default.
# The reduction is done simply with Python's `reduce`. Only in-built functions are
# variadic, because the original McCarthian Lisp did not feature any mechanisms for
# defining variadic functions.

def add(vm):
    size = vm.argstarts.pop()
    args = []
    while len(vm.stack) != size:
        el = vm.stack.pop()
        if not type(el) is int:
            raise Exception("`+/n`: invalid argument type")
        args.append(el)

    vm.push(reduce(lambda a, b: a+b, args))

def sub(vm):
    size = vm.argstarts.pop()
    args = []
    while len(vm.stack) != size:
        el = vm.stack.pop()
        if not type(el) is int:
            raise Exception("`-/n`: invalid argument type")
        args.append(el)

    vm.push(reduce(lambda a, b: a-b, args))

def mul(vm):
    size = vm.argstarts.pop()
    args = []
    while len(vm.stack) != size:
        el = vm.stack.pop()
        if not type(el) is int:
            raise Exception("`*/n`: invalid argument type")
        args.append(el)

    vm.push(reduce(lambda a, b: a*b, args))

def div(vm):
    size = vm.argstarts.pop()
    args = []
    while len(vm.stack) != size:
        el = vm.stack.pop()
        if not type(el) is int:
            raise Exception("`//n`: invalid argument type")
        args.append(el)

    vm.push(reduce(lambda a, b: a/b, args))

def list(vm):
    size = vm.argstarts.pop()
    args = []
    while len(vm.stack) != size:
        el = vm.stack.pop()
        args.append(el)

    args.reverse() # :/
    vm.push(reduce(lambda a, b: Cons(b, a), args, None))

def eqq(vm):
    def eq(a, b):
        if type(a) is Cons and type(b) is Cons:
            return eq(a.car, b.car) and eq(a.cdr, b.cdr)
        return a == b

    a = vm.stack.pop()
    b = vm.stack.pop()
    
    vm.push(eq(a, b))

def atomq(vm):
    el = vm.stack.pop()
    vm.push(type(el) is int or type(el) is str)

def nilq(vm):
    el = vm.stack.pop()
    vm.push(el is None)

def cons(vm):
    a = vm.stack.pop()
    b = vm.stack.pop()
    vm.push(Cons(a, b))

def car(vm):
    el = vm.stack.pop()
    if not type(el) is Cons:
        raise Exception("Invalid type for internal function `car`")
    vm.push(el.car)

def cdr(vm):
    el = vm.stack.pop()
    if not type(el) is Cons:
        raise Exception("Invalid type for internal function `cdr`")
    vm.push(el.cdr)
