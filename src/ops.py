# This is the module where everything regarding how to execute our stack-based code lies.
# We begin with definitions of the integer representations of each primitive VM opcode;
# the ones that interact with it and its stack on a very basic level. These are NOT built-in
# functions; those are called with OP_CALL and are defined in "native.py".
#
# Each "op{Name}" function returns a positive integer which is the number the VM PC should
# be increased by, i.e. its operator's positional arity + 1.

OP_ATOM = 0
OP_CALL = 1
OP_DEFINE = 2
OP_FIND = 3
OP_START_ARGS = 4
OP_UP_DIS = 5
OP_DOWN_DIS = 6
OP_JUMP = 7
OP_JIF = 8

# Documentation syntax:
#
# <name>/<positional arity> [(<stack-wise arity>)]
# <description>

# OP_ATOM/1
# Pushes an atomic value (first positional argument) onto the stack.
def opAtom(vm):
    vm.stack.append(vm.pcval(1))
    return 2

# OP_CALL/1
# Calls an internal function based on an atomic symbol identifier (first positional argument).
def opCall(vm):
    vm.fns[vm.pcval(1)](vm)
    return 2

# OP_DEFINE/1 (1)
# Binds a value (stack top) to a symbol (first positional argument).
def opDefine(vm):
    vm.defs[vm.pcval(1)] = vm.stack.pop()
    return 2

# OP_FIND/1
# Finds a symbol (first positional argument) in the symbol table and pushes it onto the stack.
def opFind(vm):
    name = vm.pcval(1)
    if not name in vm.defs:
        raise Exception(f"symbol \"{name}\" not defined")
    vm.stack.append(vm.defs[name])
    return 2

# OP_START_ARGS/0
# Creates a new marker for vararg function calls.
def opStartArgs(vm):
    vm.argstarts.append(len(vm.stack))
    return 1

# OP_UP_DIS/0
# Makes the VM start disassembling if starting from 0.
def opUpDis(vm):
    vm.disstate += 1
    vm.optable = DISOPTABLE
    return 1

# OP_JUMP/1
# Advances the PC by the value of the first positional argument.
def opJump(vm):
    return vm.pcval(1)

# OP_JIF/1 (1)
# Jumps to the first positional argument if the top of the stack is false.
def opJif(vm):
    if not vm.stack.pop():
        return vm.pcval(1)
    return 2


# These are the disassembly versions of each of the VM's opcodes. They will be executed
# instead of their default counterparts above when up into disassembly mode with `OP_UP_DIS`.

def disAtom(vm):
    print(f"{vm.pc:03} -- OP_ATOM   {str(vm.pcval(1))}")
    return 2

def disCall(vm):
    print(f"{vm.pc:03} -- OP_CALL   {vm.pcval(1)}")
    return 2

def disDefine(vm):
    print(f"{vm.pc:03} -- OP_DEFINE {vm.pcval(1)}")
    return 2

def disFind(vm):
    print(f"{vm.pc:03} -- OP_FIND   {vm.pcval(1)} ")
    return 2

def disStartArgs(vm):
    print(f"{vm.pc:03} -- OP_START_ARGS")
    return 1

def disUpDis(vm):
    vm.disstate += 1
    print(f"{vm.pc:03} -- OP_UP_DIS")
    return 1

def disJump(vm):
    print(f"{vm.pc:03} -- OP_JUMP   {vm.pcval(1)}")
    return 2


def disJif(vm):
    print(f"{vm.pc:03} -- OP_JIF    {vm.pcval(1)}")
    return 2

# OP_DOWN_DIS/0
# Makes the VM end disassembling if vm.disstate reaches 0. This is the only opcode that does not have
# two optable-dependent variants -- there is no logical way in which we could encounter
# an `OP_DOWN_DIS` outside of disassembly mode.
def disDownDis(vm):
    vm.disstate -= 1
    if vm.disstate == 0:
        vm.optable = OPTABLE
    else:
        print(f"{vm.pc:03} -- OP_DOWN_DIS")
    return 1

OPTABLE = [opAtom, opCall, opDefine, opFind, opStartArgs, opUpDis, disDownDis, opJump, opJif]
DISOPTABLE = [disAtom, disCall, disDefine, disFind, disStartArgs, disUpDis, disDownDis, disJump, disJif]