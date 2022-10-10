# awrwydr
Awrwydr is a toy McCarthian Lisp-like with a unique backend.

Do
```
python path/to/src/awrwydr.py
```
to enter the REPL.

## Explanation
### Function notation
In mathematics and computer science, we've generally accepted the following notation for expressing the value of a function:
```
·(x, y)
```
In this example, `·` represents the function, and `x` and `y` its arguments.

Moreover, if it so happens that the function has specifically two arguments (i.e. it is *binary*), we will often switch up the syntax to have the function (or in this case an *operator*) stand in the center of the expression, between the arguments:
```
x · y
```
This syntax is the one we use for the most basic mathematical binary operations, like addition, subtraction, multiplication and division, and is supported by most (if not all) widely used programming languages today.

However, there's two other notation conventions that abandon this exception: Polish notation and reverse Polish notation (also called prefix notation and postfix/suffix notation respectively). Regardless of arity (number of arguments), the first one always places the function before the arguments...
```
·(x, y)
```
...and the second one the other way around...
```
y x ·
```
These two conventions are characteristic to two families of programming languages: Lisps and Forths. Lisps use parentheses to denote function expressions' beginnings and ends, fundamentally making each function expression a list of tokens, hence the name Lisp: list processor...
```
(+ 2 (* 3 4))
```
...while Forths have no such mechanic, as every token in Forth is executed immediately, without any need for lookahead or context, thanks to an execution-wide stack...
```
4 3 * 2 +
```

### Troi yr awrwydr[^1]
The observant reader might notice that PN and RPN[^2] versions of function expressions seem to always be mirror versions of themselves, with the latter ones being rid of parentheses. This is exactly Awrwydr's backend is based on!

The interpreter reads in a single line of some Lisp-like input. The parser makes its way through it, emitting reversed expressions in the correct order and a small stack-based virtual machine interprets them! This is done in the most simplistic, brain-dead manner possible, though there are some special Lisp constructs that can't simply be translated atom by atom and require some further care from the parser.

Each source file is documented with care, so you should look into those if you want to learn more about how each component of the interprter works. 

## Using the REPL
If everything goes right, you should be greeted with the message:
```
*~ awrwydr v<version> ~*
Enter an s-expression!
```
At that point you should... simply follow the instruction, really. You can view supported in-built functions in both `Vm.__init__` (src/vm.py) and `Parser.__init__` (src/parser.py). Apart from those, there are two additional language constructs, not represented as function calls in the final VM microcode:
- `quote/1`, which takes one s-expression as an argument and simply returns it as data. Identifiers are not resolved and are represented using Python strings,
- `unquote/1`, which takes one s-expression as an argument and weaves it (for evaluation) into its surrounding quote experssion (usable only in `quote/1`),[^3]
- `define/2`, which takes one identifier and one s-expression as arguments and makes it so that past that point, every instance of the identifier will be replaced with the (previously evaluated) s-expression.[^4]
- `dis/1`, which takes a single s-expression as an argument and, without evaluating it, outputs its disassembled RPN microcode representation,
- ~~`lambda/2`, which takes one list of identifiers and one s-expression as arguments and creates a lambda abstraction (anonymous function) using the identifiers from the first argument as its parameters and the s-expression as the function body~~[^5]
- ~~`cond/n`, which takes an arbitrary number `n` of `(X Y)` pairs as arguments, where `X` is an expression that evaluates to a boolean value and `Y` is an s-expression. The interpreter will make its way through the `n` pairs and stop at the first one whose `X` evaluates to `True`, then evaluate `Y`.~~[^5]

Enter `end`, `(end)`, or an empty line to exit the REPL gracefully.

All errors are reported within Python's exception system --- perhaps when all other important features are implemented I'll look to making a more competent error system.

## Questions
### What's src/prelude.lisp?
It serves both as a future[^6] test and a way to import some basic functionality that doesn't have to be defined natively.
### What does the project's name mean? How do you pronounce it?
It's pronounced something close to "hour-wedder" in English and it means "hourglass" in Welsh. I chose it to reflect the manner of PN-to-RPN translation used in this parser (reversal, like the turning of an hourglass).
### Why choose Python as the implementation language?
Python trades performance for ease and speed of development - in the case of a toy interpreter, I value the latter deeply and don't really care about the prior.

[^1]: Welsh for "turning the hourglass \[upside down\]"
[^2]: Short for Polish notation and reverse Polish notation
[^3]: Which means `(quote (1 (unquote (+ 1 1)) 3))` is equivalent to `(quote (1 2 3))`.
[^4]: All this is just the long way to say `define/2` is used to define variables.
[^5]: Not yet implemented!
[^6]: Because not only does the interpreter not know yet how to import files, it doesn't know all the constructs used in the prelude (like `lambda` or `cond`).