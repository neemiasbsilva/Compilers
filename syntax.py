from sly import Parser
from lexer import LexerAnalysis


class ParserAnalysis:
    # Get token list from the lexer (required)
    tokens = LexerAnalysis.tokens

    # Grammar rules and actions
    @_('lista_declaracao')
    def programa(self, p):
        return p.lista_declaracao

    @_('declaracao aux0')
    def lista_declaracao(self, p):
        return p.declaracao, p.aux0

    @_(' ')
    def empty(self, p):
        pass

    @_('declaracao aux0')
    def aux0(self, p):
        return p.lista_declaracao, p.aux0

    @_('empty')
    def aux0(self, p):
        return p.empty

    @_('declaracao_variaveis',
       'declaracao_funcoes')
    def declaracao(self, p):
        return p[0]

    @_('tipo ID ";"')
    def declaracao_variaveis(self, p):
        return p[0], p[1], p[2]

    @_('tipo ID ";" "[" NUMBER "]"')
    def declaracao_variaveis(self, p):
        return p[0], p[1], p[2], p[4], p[5]

    @_('int', 'void')
    def tipo(self, p):
        return p[0]

    @_('tipo ID "(" parametros ")" declaracao_composta')
    def declaracao_funcoes(self, p):
        return p[0], p[1], p[2], p[3], p[4], p[5]

    @_('lista_parametros',
       'void')
    def parametros(self, p):
        return p[0]

    @_('param aux1')
    def lista_parametros(self, p):
        return p[0], p[1]

    @_('param aux1')
    def aux1(self, p):
        return p[0], p[1]

    @_('empty')
    def aux1(self, p):
        return p[0]

    @_('tipo ID')
    def param(self, p):
        return p[0], p[1]

    @_('tipo ID "[" "["')
    def param(self, p):
        return p[0], p[1], p[2]

    @_('"{" declaracoes_locais lista_comando "}"')
    def declaracao_composta(self, p):
        return p[0], p[1], p[2], p[3]

    @_('aux2')
    def declaracoes_locais(self, p):
        return p

    @_('declaracao_variaveis aux2')
    def aux2(self, p):
        return p[0], p[1]

    @_('empty')
    def aux2(self, p):
        return p[0]

    @_('aux3')
    def lista_comandos(self, p):
        return p[0]

    @_('comando aux3')
    def aux3(self, p):
        return p[0], p[1]

    @_('empty')
    def aux3(self, p):
        return p[0]

    @_('declaracao_expressao',
       'declaracao_composta',
       'declaracao_selecao',
       'declaracao_iteracao',
       'declaracao_retorno')
    def comando(self, p):
        return p[0]

    @_('expressao ";"')
    def declaracao_expressao(self, p):
        return p[0], p[1]

    @_('";"')
    def declaracao_expressao(self, p):
        return p[0]

    @_('IF "(" expressao ")" comando')
    def declaracao_selecao(self, p):
        return p[0], p[1], p[2], p[3], p[4]

    @_('IF "(" expressao ")" comando ELSE comando')
    def declaracao_selecao(self, p):
        return p[0], p[1], p[2], p[3], p[4]

    @_('WHILE "(" expressao ")" comando')
    def declaracao_iteracao(self, p):
        return p[0], p[1], p[2], p[3], p[4]

    @_('RETURN ";"')
    def declaracao_retorno(self, p):
        return p[0], p[1]

    @_('RETURN expressao ";"')
    def declaracao_retorno(self, p):
        return p[0], p[1], p[2]

    @_('variavel "=" expressao')
    def expressao(self, p):
        return p[0], '=', p[2]

    @_('expressao_simples')
    def expressao(self, p):
        return p[0]

    @_('ID')
    def variavel(self, p):
        return p[0] @ _('ID')

    @_('ID "[" expressao "]"')
    def variavel(self, p):
        return p[0], p[1], p[2], p[3]

    @_('soma_expressao op_relacional soma_expressao')
    def expressao_simples(self, p):
        return p[0], p[1], p[2]

    @_('soma_expressao')
    def expressao_simples(self, p):
        return p[0]

    @_('LE', 'LT', 'GE', 'GT', 'EQ', 'NE')
    def op_relacional(self, p):
        return p[0]

    @_('termo aux4')
    def soma_expressao(self, p):
        return p[0], p[1]

    @_('soma termo aux4')
    def aux4(self, p):
        return p[0], p[1], p[2]

    @_('empty')
    def aux4(self, p):
        return p[0]

    @_('SUM', 'MINUS')
    def soma(self, p):
        return p[0]

    @_('termo mult fator')
    def termo(self, p):
        return p[0], p[1], p[2]

    @_('fator')
    def termo(self, p):
        return p[0]

    @_('DIVIDE', 'TIMES')
    def mult(self, p):
        return p[0]

    @_('"(" expressao ")"')
    def fator(self, p):
        return p[0], p[1], p[2]

    @_('variavel', 'ativacao', 'NUMBER')
    def fator(self, p):
        return p[0]

    @_('ID "(" argumentos ")"')
    def ativacao(self, p):
        return p[0], p[1], p[2], p[3]

    @_('lista_argumentos', 'empty')
    def argumentos(self, p):
        return p[0]

    @_('expressao aux5')
    def lista_argumentos(self, p):
        return p[0], p[1]

    @_('"," expressao')
    def aux5(self, p):
        return p[0], p[1]

    @_('empty')
    def aux5(self, p):
        return p[0]


def main():
    lexer = LexerAnalysis()
    parser = ParserAnalysis()

    while True:
        try:
            file = open('Inputs/sort.in', 'r')
            data = str()
            for line in file:
                data += str(line)

            result = parser.parse(lexer.tokenize(data))
            print(result)
        except EOFError:
            break


if __name__ == '__main__':
    main()
