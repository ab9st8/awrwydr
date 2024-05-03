import cons

class Lexer:
    def __init__(self):
        self.code = None
        self.cursor = 0

    def lex(self, code):
        self.__init__() # just for good measure
        self.code = code
        
        res = [] # a Python list of Awrwydr `Cons`es and raw lexemes

        while not self.isAtEnd():
            expr = self.expr(self.advance())
            if expr is not None:
                res.append(expr)
        print(res)
        return res

    def expr(self, lexeme):
        # for when we call recursively, obviously this won't fire from the `Lexer.lex` loop
        # if self.isAtEnd(): raise Exception("unexpected end of input")

        # lexeme = self.advance()

        if lexeme == '%':
            while not self.isAtEnd() and self.curr() != '\n':
                self.cursor += 1 # stupid but alr
            return None

        # FWIW at lex-time we don't actually check if these s-expressions make any sense.
        # they can be gibberish but as long as they're not ill-formed they're making it through
        elif lexeme == '(':
            sexpr = cons.Cons(None, None)
            while True:
                lexeme = self.advance()
                if lexeme == ')': break
                sexpr.append(self.expr(lexeme))

                # this is cleaner than putting it in the loop condition (i think)
                if self.isAtEnd(): raise Exception("unterminated s-expression")

            return sexpr

        elif lexeme == ')':
            raise Exception("unexpected closing paren `)`")

        else:
            return lexeme

    def curr(self):
        """Returns the character currently being inspected."""
        return self.code[self.cursor]

    def isAtEnd(self):
        """Returns true if there are no more characters to be read from the input."""
        return self.cursor >= len(self.code)

    def advance(self):
        """Returns the next discernible token in the source code. Assumes cursor is not at end! Do not call when unsure"""

        # skip any kind of whitespace, we don't really care as long as it's
        # all differentiable from each other.
        # there might also be a trailing newline from a comment
        while self.cursor < len(self.code) and self.curr().isspace(): self.cursor += 1

        # skip comments, starting at '%' and ending at nearest newline
        if self.curr() == '%':
            # print("HANDLING A COMMENT")
            return '%' # we only begin ignoring comments inside `Lexer.expr()`

        # '('
        if self.curr() == '(':
            self.cursor += 1
            return '('

        # ')'
        elif self.curr() == ')':
            self.cursor += 1
            return ')'

        # a number literal
        elif self.curr().isdigit():
            lexeme = ""

            # TODO: decimal-point support
            while not self.isAtEnd() and self.curr().isdigit():
                lexeme += self.curr()
                self.cursor += 1
            return int(lexeme)

        # a symbol atom
        elif self.curr().isalpha() or self.curr() in ['+', '-', '*', '/']:
            lexeme = ""
            while not self.isAtEnd() and (self.curr().isalpha() or self.curr() in ['+', '-', '*', '/', '?']):
                lexeme += self.curr()
                self.cursor += 1
            if lexeme == "true": return True
            elif lexeme == "false": return False
            elif lexeme == "nil": return None
            # print(f"returning lexeme {lexeme}")
            return lexeme

        # nothing matched so we should probably report an error
        else:
            raise Exception(f"`{self.curr()}`: unknown lexeme")