from sly import Lexer


class LexerAnalysis(Lexer):
    # Set of token names. This is always required
    tokens = {NUMBER, ID, WHILE, IF, ELSE, PRINT, RETURN, VOID, INT, PLUS, MINUS, TIMES,
              PLUS, MINUS, TIMES, DIVIDE, ASSIGN, EQ, LT, LE, GT, GE,
              NE}

    literals = {'(', ')', '{', '}', '[', ']', ';',','}


    @_(r'[/][*][^*]*[*]+([^*/][^*]*[*]+)*[/]')
    def ignore_linecomment(self, t):
        self.lineno += t.value.count('\n')

    # String containing ignored characters
    ignore = ' \t'

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
    ID['void'] = VOID
    ID['int'] = INT
    ignore_comment = r'//.*'


    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1


def main():
    # Input correct
    # file = open("Inputs/allofsymbols.in", 'r')
    # file = open("Inputs/sort.in", 'r')
    # file = open("Inputs/mdc.in", 'r')
    file = open("Inputs/listofemails.in", 'r')
    data = str()
    for line in file:
        data += str(line)

    lexer = LexerAnalysis()
    for tok in lexer.tokenize(data):

        if tok.type == 'IF' or tok.type == 'ELSE' or tok.type == 'WHILE':
            print(tok.value)
        elif tok.type == 'PRINT' or tok.type == 'RETURN' or tok.type == 'VOID':
            print(tok.value)
        elif tok.type == 'INT' or tok.type == 'EQ' or tok.type == 'NE':
            print(tok.value)
        elif tok.type == 'LE' or tok.type == 'LT' or tok.type == 'GE':
            print(tok.value)
        elif tok.type == 'GT' or tok.type == 'MINUS' or tok.type == 'PLUS':
            print(tok.value)
        elif tok.type == 'ASSIGN' or tok.type == 'DIVIDE' or tok.type == 'TIMES':
            print(tok.value)
        else:
            print(tok.type)


if __name__ == '__main__':
    main()