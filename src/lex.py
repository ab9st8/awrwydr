import cons

class Lexer:
    def __init__(self):
        self.code = None
        self.cursor = 0

    def lex(self, code):
        self.__init__() # just for good measure
        self.code = code
        result = self.expr()
        if self.cursor != len(code):
            raise Exception("trailing expressions past a single s-expression")
        return result

    def expr(self):
        lexeme = self.advance()
        if lexeme == '(':
            result = cons.Cons(self.expr(), None)
            while self.curr() != ')':
                result.append(self.expr())
                if self.isAtEnd(): raise Exception("unterminated s-expression")
            self.cursor += 1
            return result

        elif lexeme == ')':
            raise Exception("unexpected closing paren `)`")

        else:
            return lexeme # return lexeme parsed into atomic Python literal

    def curr(self):
        """Returns the character currently being inspected."""
        return self.code[self.cursor]

    def isAtEnd(self):
        return self.cursor >= len(self.code)

    def advance(self):
        """Returns the next discernable token in the source code."""

        # skip any kind of whitespace, we don't really care as long as it's
        # all differentiable from each other
        while self.cursor < len(self.code) and self.curr().isspace(): self.cursor += 1

        # '('
        if self.curr() == '(':
            self.cursor += 1
            return '('

        # ')'
        elif self.curr() == ')':
            self.cursor += 1
            return ')'

        # a number atom
        elif self.curr().isdigit():
            result = ""
            while self.cursor < len(self.code) and self.curr().isdigit():
                result += self.curr()
                self.cursor += 1
            return int(result)

        # a symbol atom
        elif self.curr().isalpha() or self.curr() in ['+', '-', '*', '/']:
            result = ""
            while self.cursor < len(self.code) and self.curr().isalpha() or self.curr() in ['+', '-', '*', '/', '?']:
                result += self.curr()
                self.cursor += 1
            return result

