# This class describes a lambda object; i.e. an expression
# with parameters (`params`).
class Lambda:
    def __init__(self, params, code):
        self.params = params # a list of strings (names of parameters)
        self.code = code     # executable VM microcode