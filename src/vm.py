import ops
import native
from lambdaobj import *


# Our stack-based VM! All of its opcodes are defined in `ops.py`
# Other than that it relies on native functions (native.py) for
# all of its internal behavior.

class VM:
    def __init__(self, defs={}):
        self.stack = []
        self.argstarts = []
        # Each (key, value) pair corresponds to
        #   (name, Python equivalent)
        # of a native function.
        self.fns = {
            "+": native.add,
            "-": native.sub,
            "*": native.mul,
            "/": native.div,
            "eq?": native.eqq,
            "atom?": native.atomq,
            "nil?": native.nilq,
            "cons": native.cons,
            "list": native.list,
            "car": native.car,
            "cdr": native.cdr,
        }
        self.defs = defs # definitions added with `define/2` as well as lambda arguments

        self.code = None
        self.pc = 0
        self.optable = ops.OPTABLE
        self.disstate = 0

    def pcval(self, offset=0):
        return self.code[self.pc+offset]

    def size(self):
        return len(self.stack)

    def push(self, val):
        self.stack.append(val)

    def run(self, code):
        self.code = code
        self.pc = 0
        self.stack = []
        length = len(self.code)
        while self.pc < length:
            skip = self.optable[self.pcval()](self) # cool, huh? no internal opcode branching needed!
            self.pc += skip