from sly import Lexer


class LexerAnalysis(Lexer):
    # Set of token names. This is always required
    tokens = {NUMBER, ID, WHILE, IF, ELSE, PRINT, RETURN, PLUS, MINUS, TIMES,
              PLUS, MINUS, TIMES, DIVIDE, ASSIGN, EQ, LT, LE, GT, GE,
              NE}

    literals = {'(', ')', '{', '}', ';'}

    # String containing ignored characters
    ignore = '\t'

    # Regular expression rules for tokens
    PLUS = r'\+'
    MINUS = r'\-'
    TIMES = r'\*'
    DIVIDE = r'/'
    EQ = r'=='
    ASSIGN = r'='
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Identifiers and Keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['print'] = PRINT
    ID['return'] = RETURN

    ignore_comment = r'[/][*][^*]*[*]+([^*/][^*]*[*]+)*[/]'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r'% (self.lineno, t.value[0]))

def main():
    data = open("")

if __name__ == '__main__':
    main()