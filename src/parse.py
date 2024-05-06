from cons import *
from ops import *
from lambdaobj import *

# As mentioned in the readme and the name of this project suggests, the process
# of taking some cons- (or Polish notation) code and turning it into RPN-compliant
# code relies heavily on the action of *reversal* of a list structure, since as the
# notation names imply, they are equivalent to each other, but reversed respectively.
#
# The algorithm is simply "reverse everything recursively in a depth-first
# manner", except for a couple of special behaviors like lambda abstractions or variable
# definitions where we need to add a little bit of sparkle to make everything work
# correctly, simply due to the discrepancies of the two syntaxes.
#
# One interesting thing to look at is how PN code (the one we're compiling *from*) has
# variable level of nestation, i.e. everything is represented as a list of lists, while
# on the other hand RPN code (the one we're compiling *to*) has only one level of nestation
# -- each instruction in a list encountered by the stack-based VM can be executed
# instantly.

class Parser:
    def __init__(self):
        # These are all the internal functions (PN) / words (RPN) known to this parser and
        # the stack-based VM. Each
        #     (key, value)
        # pair corresponds to
        #     (name, arity).
        # Arity equal to -1 indicates that the function is vararg (variadic argument) and
        # the parser must mark the start of arguments with the OP_START_ARGS opcode for
        # the VM to know how many values to take into consideration. Another solution to this
        # problem is simply counting how many arguments the function takes and emitting that
        # into the VM microcode, but this is to me seems a bit more intuitive.
        # Yet another solution includes noticing that any sort of vararg function is a fold (the one
        # from functional programming); any kind of arithmetic operation is a fold with itself,
        # `list` is a fold with an expression `lambda a, b: Cons(b, a)`, (as seen in native.py) etc.,
        # so, possibly, the parser alone could interpret these variadic functions as folds and  
        # repeatedly call a binary function on all of its arguments. As an example take
        # ```
        # (+ 1 2 3 4 5)
        # ```
        # That could be interpreted like
        # ```
        # 5 4 + 3 + 2 + 1 +
        # ```
        self.fns = {
            "+": -1,    # adds some numbers
            "-": -1,    # subtracts some numbers
            "*": -1,    # multiplies some numbers
            "/": -1,    # divides some numbers
            "eq?": 2,   # whether two expressions are equal
            "atom?": 1, # whether an expression is an atom
            "nil?": 1,  # whether an expression is nil
            "cons": 2,  # creates a cons pair
            "list": -1, # creates a list from cons pairs
            "car": 1,   # returns the first element of a list expression (PN) / quote (RPN)
            "cdr": 1,   # returns the tail of a list expression (PN) / quote (RPN)
        }

        # when 0, everything is executed as expected.
        # when >0, instead every instruction is disassembled.
        # OP_UPDIS increments this, OP_DOWNDIS decrements — this
        # allows for nested `dis` expressions
        self.disstate = 0
        self.jumppatches = []

    def parse(self, lex):
        res = []

        for expr in lex:
            res += self._parse(expr)
        return res

    def _parse(self, expr):
        if type(expr) is Cons:
            fn = expr.car

            # `(quote EXPR)`
            # Takes an expression [EXPR] as an argument and returns it as data.
            # Identifiers are rendered as Python strings.
            if fn == 'quote':
                if len(expr) != 2:
                    raise Exception("quote/1: invalid number of arguments")
                return self.quote(expr.cdr.car)

            # `(define NAME VALUE)`
            # Takes an identifier [NAME] and an expression [VALUE] as arguments and
            # binds [VALUE] to [NAME], so that every instance of [NAME] past that point
            # is replaced with [VALUE].
            elif fn == 'define':
                if len(expr) != 3:
                    raise Exception("define/2: invalid number of arguments")
                name = expr.cdr.car
                if not type(name) is str:
                    raise Exception("define/2: invalid symbol")
                value = self._parse(expr.cdr.cdr.car)
                return value + [OP_DEFINE, name]

            # `(dis EXPR)`
            # Takes an expression [EXPR] as an argument and, without evaluating it,
            # prints out its disassembled microcode form.
            elif fn == 'dis':
                if len(expr) != 2:
                    raise Exception("dis/1: invalid number of arguments")

                return [OP_UP_DIS] + self._parse(expr.cdr.car) + [OP_DOWN_DIS]

            # `(cond (COND1 EXPR1) (COND2 EXPR2) ...)`
            # Takes a variable number of pairs of expressions as arguments and evaluates them
            # in order. If [COND] evaluates to true, [EXPR] is evaluated and returned.
            # If [COND] evaluates to false, the next pair is evaluated.
            elif fn == 'cond':
                code = []
                for pair in expr.cdr:
                    if not type(pair) is Cons or len(pair) != 2:
                        raise Exception("cond: invalid syntax")
                    cond = pair.car
                    expr = pair.cdr.car
                    
                    # The boolean condition and jump-if-false
                    code += self._parse(cond) + [OP_JIF, 0]
                    jifpatch = len(code) - 1 # save the patch location

                    # The evaluated expression and unconditional jump
                    code += self._parse(expr) + [OP_JUMP, 0]
                    self.jumppatches.append(len(code) - 1) # save the patch location

                    # patch JIF
                    code[jifpatch] = len(code) - jifpatch + 1

                for patch in self.jumppatches:
                    code[patch] = len(code) - patch + 1
                
                self.jumppatches = []
                return code

            # `(lambda (param1 param2 ...) EXPR)`
            # Takes a list of identifiers [param1 param2 ...] and an expression [EXPR]
            # as arguments and returns a lambda object that takes [param1 param2 ...] as
            # arguments and evaluates [EXPR] with them bound.
            elif fn in ['lambda', 'λ']:
                if len(expr) == 3:
                    ids = expr.cdr.car
                    if not type(ids) is Cons:
                        raise Exception("lambda/2: invalid syntax")
                    params = []
                    for param in ids:
                        if not type(param) is str:
                            raise Exception("lambda/2: invalid syntax")
                        params.append(param)
                    
                    expr = self._parse(expr.cdr.cdr.car)
                    return [OP_LAMBDA, params, expr]
                elif len(expr) == 2:
                    expr = self._parse(expr.cdr.car)
                    return [OP_LAMBDA, [], expr]
                else:
                    raise Exception("lambda/1-2: invalid number of arguments")
                
            # An immediate lambda call.
            elif self._parse(fn)[0] == OP_LAMBDA:
                code = []
                if type(expr.cdr) is Cons:
                    for el in reversed(expr.cdr):
                        code += self._parse(el)
                return code + self._parse(fn) + [OP_EVAL]

            # In-built function call.
            elif fn in self.fns.keys():
                code = []
                # if the function is variadic, we need to mark the start of arguments
                if self.fns[fn] == -1:
                    code = [OP_START_ARGS]
                elif len(expr) - 1 != self.fns[fn]: # <list length> - <fn name>
                    raise Exception(f"{fn}/{self.fns[fn]}: invalid number of arguments")

                # This is the highly anticipated "turning of the hourglass"! First we
                # add parsed arguments to our code, and only after that do we add the
                # call opcode with the function name.
                for el in reversed(list(expr.cdr)):
                    arg = self._parse(el)
                    code += arg

                code += [OP_CALL, fn]
                return code

            elif type(fn) is str:
                code = []
                if type(expr.cdr) is Cons:
                    for el in reversed(expr.cdr):
                        code += self._parse(el)
                return code + [OP_FIND, fn, OP_EVAL]

            else:
                raise Exception(f"invalid car: {fn}")

        else:
            # We solemnly pledge to resolve all identifiers and leave them not
            # in literal form! (use `quote` for that)
            if type(expr) is str:
                return [OP_FIND, expr]
            return [OP_ATOM, expr]
    
    def quote(self, expr):
        """Quote an expression into RPN-compliant code."""
        if type(expr) is Cons:
            # `(unquote EXPR)`
            # Usable only in `quote/1`. Weaves the evaluated version of EXPR
            # into its surrounding quote expression.
            if expr.car == 'unquote':
                if len(expr) != 2:
                    raise Exception("unquote/1: invalid number of arguments")
                return self._parse(expr.cdr.car)
            return self.quote(expr.cdr) + self.quote(expr.car) + [OP_CALL, 'cons']
        else:
            return [OP_ATOM, expr]