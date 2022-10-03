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
    res = lexer.lex(code)
    if type(res) is str and res.startswith("\\"):
        stderr.write(res + "\n")
        break
    res = parser.parse(res)
    vm.run(res)