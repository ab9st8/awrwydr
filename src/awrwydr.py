# from sys import stderr

from os.path import dirname, join
from colorama import Fore, Style
import argparse

from lex import Lexer
from parse import Parser
from vm import VM


VERSION = "0.1.1"

MESSAGE        = Style.BRIGHT + f"""*~ awrwydr v{VERSION} ~*\nEnter an s-expression!""" + Style.RESET_ALL
PRELUDE_PATH   = join(dirname(__file__), "prelude.lisp")
ERROR_PROMPT   = Fore.RED + ":: " + Fore.RESET
SUCCESS_PROMPT = Fore.BLUE + ":: " + Fore.RESET

argparser = argparse.ArgumentParser(prog="awrwydr", description="an hourglass Lisp")
argparser.add_argument("-v", "--verbose", action="store_true")
args = argparser.parse_args()

print(MESSAGE)

# Awrwydr internals
lexer  = Lexer()
parser = Parser()
vm     = VM()

# loading the prelude
try:
    with open(PRELUDE_PATH, "r") as f:
        vm.run(parser.parse(lexer.lex(f.read())))
    print(SUCCESS_PROMPT + Style.DIM + "<`prelude.lisp` loaded!>" + Style.RESET_ALL)
except Exception as e:
    msg = Style.DIM + "<run with `-v` or `--verbose` to see exception>" + Style.RESET_ALL
    if args.verbose:
        msg = Style.DIM + f"<exception: {e.args[0]}>" + Style.RESET_ALL
    print(ERROR_PROMPT + Style.DIM + "<`prelude.lisp` faulty or not found>" + Style.RESET_ALL)
    print(ERROR_PROMPT + msg)

print(vm.defs)

# REPL loop
while True:
    try:
        code = input(Style.DIM + ">> " + Style.RESET_ALL) # prompt
    except EOFError:
        code = "end" # lol
        print("\n")
    finally:
        if code in ["end", "(end)"] or code.isspace():
            print(Style.BRIGHT + "Diolch, hwyl!" + Style.RESET_ALL)
            break

    try:
        vm.run(parser.parse(lexer.lex(code)))
    except Exception as e:
        print(ERROR_PROMPT + f"<exception: {e.args[0]}>")
    
    if vm.size() > 0:
        print(SUCCESS_PROMPT + str(vm.stack.pop()))