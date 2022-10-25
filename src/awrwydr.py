from ensurepip import version
from sys import stderr

from lex import Lexer
from parse import Parser
from vm import VM


VERSION = "0.1.0"

message = f"""*~ awrwydr v{VERSION} ~*
Enter an s-expression!"""

print(message)

lexer = Lexer()
parser = Parser()
vm = VM()

while True:
    code = input(">> ")
    if code in ["", "end", "(end)"] or code.isspace():
        print("Diolch, hwyl!")
        break
    
    vm.run(parser.parse(lexer.lex(code)))
    if vm.size() > 0:
        print(f":: {vm.stack.pop()}\n")