# awrwydr
...is a toy McCarthian Lisp-like with a unique backend.

Do
```
python3 path/to/src/awrwydr.py
```
to enter the REPL.

## Explanation
### Function notation
In mathematics and computer science, we've generally accepted the following notation for expressing the value of a function:
```
·(x, y)
```
In this example, `·` represents the function, and `x` and `y` its arguments.

Moreover, if it so happens that the function has specifically two arguments (i.e. it is *binary*), we will often switch up the syntax to have the function (in this case also called an *operator*) stand in the center of the expression, between the arguments:
```
x · y
```
We use this syntax for most basic mathematical binary operations, like addition, subtraction, multiplication and division, and is supported by most (if not all) widely used programming languages today.

However, there's two other notation conventions that abandon this exception: Polish notation and reverse Polish notation (also called prefix notation and postfix/suffix notation respectively). Regardless of arity (number of arguments), the first one always places the function before the arguments...
```
·(x, y)
```
...and the second one the other way around[^1]...
```
(y, x)·
```
These two conventions are characteristic to two families of programming languages: Lisps and Forths. Lisps use parentheses to denote function expressions' beginnings and ends, fundamentally making each function expression a list of tokens, hence the name Lisp: list processor...
```
(+ 2 (* 3 4))
```
...while Forths have no such mechanic, as every token in Forth is executed immediately, without any need for lookahead or context, thanks to an execution-wide stack...
```
4 3 * 2 +
```

### Troi yr awrwydr[^2]
The observant reader might notice that PN and RPN[^3] versions of function expressions seem to always be mirror versions of themselves, with the latter ones being rid of parentheses. This is exactly what Awrwydr's backend is based on!

The REPL reads in a single line of some Lisp-like input. The parser makes its way through it, emitting reversed expressions in the correct order and a small stack-based virtual machine interprets them! This is done in the most simplistic, brain-dead manner possible, though there are some special Lisp constructs that can't simply be translated atom by atom and require some further attention from the parser.

Each source file is documented with care, so you should look into those if you want to learn more about how each component of the interprter works. 

## Using the REPL
If everything goes right, you should be greeted with the message:
```
*~ awrwydr v<version> ~*
Enter an s-expression!
```
At that point you should... simply follow the instruction, really. You can view supported in-built functions in both `Vm.__init__` (src/vm.py) and `Parser.__init__` (src/parser.py). Apart from those, there are a couple of additional language constructs not represented as function calls in the final VM microcode:
- `quote/1`, which takes one s-expression as an argument and simply returns it as data. Identifiers are not resolved and are represented using Python strings,
- `unquote/1`, which takes one s-expression as an argument and weaves its evaluated form into its surrounding quote expression (usable only in `quote/1`),[^3]
- `define/2`, which takes one identifier and one s-expression as arguments and makes it so that past that point, each instance of the identifier is replaced with the evaluated form of the original s-expression.[^4]
- `dis/1`, which takes a single s-expression as an argument and, without evaluating it, outputs its disassembled RPN microcode representation,
- `cond/n`, which takes an arbitrary number `n` of `(COND EXPR)` pairs as arguments, where `COND` is an expression that evaluates to a boolean value and `EXPR` is an expression. The interpreter will evaluate the `EXPR` of the first pair whose `COND` evaluates to true,
- `lambda/2`, which takes one list of identifiers and one s-expression as arguments and creates a lambda abstraction (anonymous function) using the identifiers from the first argument as its parameters and the s-expression as the function body.[^5]

Enter `end`, `(end)` or ctrl-D to exit the REPL gracefully.

All errors are reported within Python's exception system — perhaps when all other important features are implemented I'll look to making a more competent error system.

## Questions
### What's src/prelude.lisp?
It serves both as a test and a way to import some basic functionality that doesn't have to be defined natively. (However at the current moment it is still not available inside of the interpreter; this is being worked on.)
### What does the project name mean? How do you pronounce it?
It's pronounced something close to "hour-wedder" in English and it means "hourglass" in Welsh. I chose it to reflect the manner of PN-to-RPN translation used in this parser (reversal, like the turning of an hourglass).
### Why choose Python as the implementation language?
Python trades performance for ease and speed of development — in the case of a toy interpreter, I value the latter deeply and don't really care about the prior.

[^1]: Obviously that could have also been `(x, y)·` (everything depends on definitions), but I chose the reverse order to illustrate the reversing nature of the interpreter.
[^1]: Welsh for "turning the hourglass \[upside down\]"
[^2]: Short for Polish notation and reverse Polish notation
[^3]: For example, `(quote (1 (unquote (+ 1 1)) 3))` is equivalent to `(quote (1 2 3))`.
[^4]: All this is just the long way to say `define/2` is used to define variables.
[^5]: If you want to create a lambda expression without arguments (something along the lines of a [thunk](https://en.wikipedia.org/wiki/Thunk)), do not include the empty argument list at all, simply write `(lambda EXPR)`.