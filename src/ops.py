# This is the module where everything regarded how to execute our stack-based code lies.
# We begin with definitions of the integer representations of each primitive VM.
# Those are the ones that interact with it and its stack on a very basic level. These are
# NOT stdlib functions; those are called with OP_CALL and are defined in "vm.py".
#
# Each "op{Name}" function returns a positive integer which is the number the VM PC should
# be increased by, i.e. its operator's positional arity + 1.

OP_ATOM = 0
OP_CALL = 1
OP_DEFINE = 2
OP_FIND = 3
OP_START_ARGS = 4

# Documentation syntax:
#
# <name>/<positional arity> [(<stack-wise arity>)]
# <description>

# OP_ATOM/1
# Pushes an atomic value (first positional argument) onto the stack.
def opAtom(vm):
    vm.stack.append(vm.pcval(1))
    return 2

# OP_CALL/0 (1)
# Calls an internal function based on an atomic symbol identifier.
def opCall(vm):
    vm.fns[vm.stack.pop()](vm)
    return 1

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

OPTABLE = [opAtom, opCall, opDefine, opFind, opStartArgs]