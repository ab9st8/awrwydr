from ops import *
import native

# Our stack-based VM! It operates on only five opcodes, all defined
# in ops.py. Other than that it relies on native functions (native.py)
# for all of its internal behavior.

class VM:
    def __init__(self):
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
            "log": native.log,
            "eq?": native.eqq,
            "atom?": native.atomq,
            "nil?": native.nilq,
            "cons": native.cons,
            "list": native.list,
            "car": native.car,
            "cdr": native.cdr,
        }
        self.defs = {} # definitions added by the user

        self.code = None
        self.pc = 0

    def pcval(self, offset=0):
        return self.code[self.pc+offset]

    def size(self):
        return len(self.stack)

    def run(self, code):
        self.code = code
        self.pc = 0
        self.stack = []
        length = len(self.code)
        while self.pc != length:
            skip = OPTABLE[self.pcval()](self) # cool, huh? no internal opcode branching needed!
            self.pc += skip

        if self.size() > 0:
            print(f":: {self.stack.pop()}\n")