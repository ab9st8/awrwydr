# awrwydr
Awrwydr is a toy McCarthian Lisp-like with a unique backend.

Do
```
node path/to/src/awrwydr.py
```
to enter the REPL.

## Explanation
### Function notation
In mathematics and computer science, we've generally accepted the following notation for the expression of a function:
```
·(x, y)
```
In this example, `·` is the function, and `x` and `y` are its arguments.

Moreover, if it so happens that the function has specifically two arguments (i.e. it is *binary*), we will often switch up the syntax to have the function (or in this case an *operator*) stand in the center of the expression, between the arguments:
```
x · y
```
This notation is the one we use for most basic mathematical binary operations, like addition, subtraction, multiplication and division.

However, there's two other notation conventions that abandon this exception: Polish notation and reverse Polish notation (also called prefix notation and postfix/suffix notation respectively). Regardless of function arity (number of arguments), the first one always places the function before the arguments...
```
· x y
```
...and the second one the other way around...
```
y x ·
```
These two conventions are characteristic to two families of programming languages: Lisps and Forths. Lisps use parentheses to denote function expressions' beginnings and ends, fundamentally making each function expression a list of tokens, hence the name Lisp <-> list processor...
```
(+ 2 (* 3 4))
```
...while Forths have no such mechanic, as every token in Forth is executed immediately, without any need for lookahead or context, thanks to a program-wide stack...
```
4 3 * 2 +
```

### Troi yr awrwydr[^1]
The observant reader might notice that PN and RPN[^2] versions of function expressions seem to always be mirror versions of themselves, with the latter ones being rid of parentheses. This is exactly Awrwydr's backend is based on!

The interpreter reads in a single line of some Lisp-like input. The parser makes its way through it, emitting reversed expressions in the correct order and a small stack-based virtual machine interprets them! This is done in the most simplistic, brain-dead manner possible, though there are some special Lisp constructs that can't simply be translated atom by atom and require some further care from the parser.

[^1]: Welsh for "turning the hourglass \[upside down\]"
[^2]: short for Polish notation and reverse Polish notation