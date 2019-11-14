from pip._internal import operations
from sly import Parser
from lexer import LexerAnalysis
from anytree import Node, RenderTree
from anytree.importer import JsonImporter
import sys

import json

hash_table = [None] * 10000

def hashing_func(key):
    return key % len(hash_table)

def insert(hash_table, key, value):
    hash_key = hashing_func(key)
    hash_table[hash_key].append(value)
class ParserAnalysis(Parser):
    # Parser Debugin
    # debugfile = 'parser.out'
    i = 0
    # Get token list from the lexer (required)
    tokens = LexerAnalysis.tokens

    operations = {
        '+': lambda x, y: x + y,
        '−': lambda x, y: x - y,
        '∗': lambda x, y: x * y,
        '/': lambda x, y: x / y,
    }
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
    )
    # Grammar rules and actions
    @_('lista_declaracao')
    def programa(self, p):
        return {'Programa': p.lista_declaracao}

    @_(' ')
    def empty(self, p):
        pass

    @_('lista_declaracao declaracao')
    def lista_declaracao(self, p):
        return {"ListaDeclaracao": (p[0], p[1])}
    @_('declaracao')
    def lista_declaracao(self, p):
        return {"ListaDeclaracao": p[0]}

    @_('declaracao_variaveis',
       'declaracao_funcoes')
    def declaracao(self, p):
        self.i += 1
        return {'Declaracao': p[0]}

    @_('tipo ID "[" NUMBER "]" ";"')
    def declaracao_variaveis(self, p):
        return {"Declaracao_Variaveis": ( p[0], p[1], p[2], p[3], p[4], p[5])}
    # @_('tipo ID "[" NUMBER "]" error')
    # def declaracao_variaveis(self, p):
    #     print("Syntax error at line {}.".format(getattr(p, 'lineno', 0)))

    @_('tipo ID ";"')
    def declaracao_variaveis(self, p):
        return 'Declaracao_Variaveis: ', p[0], p[1], p[2]
    @_('tipo ID error')
    def declaracao_variaveis(self, p):
        print("error: {}".format(p[2]))

    @_('INT', 'VOID')
    def tipo(self, p):
        return 'Tipo: ', p[0]

    @_('tipo ID "(" parametros ")" declaracao_composta')
    def declaracao_funcoes(self, p):
        return 'Declaracao_Funcoes: ', p[0], p[1], p[2], p[3], p[4], p[5]

    @_('lista_parametros',
       'VOID')
    def parametros(self, p):
        return 'Parmetros: ', p[0]
    @_('lista_parametros "," param')
    def lista_parametros(self, p):
        return 'Lista_Parametros: ', p[0], p[1], p[2]
    @_('param')
    def lista_parametros(self, p):
        return p[0]


    @_('tipo ID "[" "]"')
    def param(self, p):
        return 'Param: ', p[0], p[1], p[2]
    @_('tipo ID')
    def param(self, p):
        return 'Param: ', p[0], p[1]

    @_('"{" declaracoes_locais lista_comandos "}"')
    def declaracao_composta(self, p):
        return 'Declaracao_Composta: ', p[0], p[1], p[2], p[3]

    @_('declaracoes_locais declaracao_variaveis')
    def declaracoes_locais(self, p):
        return 'Declaracao_Locais: ', p[0]
    @_('empty')
    def declaracoes_locais(self, p):
        pass

    @_('lista_comandos comando')
    def lista_comandos(self, p):
        return 'Lista_Comandos: ', p[0], p[1]
    @_('empty')
    def lista_comandos(self, p):
        pass

    @_('declaracao_expressao',
       'declaracao_composta',
       'declaracao_selecao',
       'declaracao_iteracao',
       'declaracao_retorno')
    def comando(self, p):
        return 'Comando: ',p[0]
    @_('expressao ";"')
    def declaracao_expressao(self, p):
        return 'Declaracao_Expressao: ', p[0], p[1]
    @_('";"')
    def declaracao_expressao(self, p):
        return 'Declaracao_Expressao: ', p[0]


    @_('IF "(" expressao ")" comando ELSE comando')
    def declaracao_selecao(self, p):
        return 'Declaracao_Selecao: ', p[0], p[1], p[2], p[3], p[4]
    @_('IF "(" expressao ")" comando')
    def declaracao_selecao(self, p):
        return 'Declaracao_Selecao: ', p[0], p[1], p[2], p[3], p[4]


    @_('WHILE "(" expressao ")" comando')
    def declaracao_iteracao(self, p):
        return 'Declaracao_Iteracao: ', p[0], p[1], p[2], p[3], p[4]


    @_('RETURN expressao ";"')
    def declaracao_retorno(self, p):
        return 'Declaracao_Retorno: ', p[0], p[1], p[2]
    @_('RETURN ";"')
    def declaracao_retorno(self, p):
        return 'Declaracao_Retorno: ', p[0], p[1]


    @_('variavel ASSIGN expressao')
    def expressao(self, p):
        return 'Expressao: ', p[0], p[1], p[2]
    @_('expressao_simples')
    def expressao(self, p):
        return 'Expressao: ', p[0]

    @_('ID "[" expressao "]"')
    def variavel(self, p):
        return 'Variavel: ', p[0], p[1], p[2], p[3]
    @_('ID')
    def variavel(self, p):
        return 'Variavel: ', p[0]

    @_('soma_expressao op_relacional soma_expressao')
    def expressao_simples(self, p):
        return 'Expressao_Simples: ', p[0], p[1], p[2]
    # @_('soma_expressao error soma_expressao')
    # def expressao_simples(self, p):
    #     print("error: {}".format(p[1]))
    @_('soma_expressao')
    def expressao_simples(self, p):
        return 'Expr_Simples: ', p[0]

    @_('LE', 'LT', 'GE', 'GT', 'EQ', 'NE')
    def op_relacional(self, p):
        return 'Op_Relacional: ', p[0]

    @_('soma_expressao soma termo')
    def soma_expressao(self, p):
        # sum = int()
        # if p[1] == "+" and p[1]:
        #     sum = int(p[0]) + int(p[2])
        # else:
        #     sum = int(p[0]) - int(p[2])
        return 'Soma_Expressao: ', p[0], p[1], p[2]
    @_('termo')
    def soma_expressao(self, p):
        return p[0]

    @_('PLUS', 'MINUS')
    def soma(self, p):
        return p[0]

    @_("termo mult fator")
    def termo(self, p):
        return 'Termo: ', p[0], p[1], p[2]
    @_('fator')
    def termo(self, p):
        return p[0]

    @_('DIVIDE', 'TIMES')
    def mult(self, p):
        return 'Mult: ', p[0]

    @_('"(" expressao ")"')
    def fator(self, p):
        return p[0], p[1], p[2]

    @_('variavel', 'ativacao', 'NUMBER')
    def fator(self, p):
        return p[0]

    @_('ID "(" argumentos ")"')
    def ativacao(self, p):
        return 'Ativacao: ', p[0], p[1], p[2], p[3]

    @_('lista_argumentos', 'empty')
    def argumentos(self, p):
        return 'Argumentos: ', p[0]

    @_('lista_argumentos "," expressao')
    def lista_argumentos(self, p):
        return 'Lista_Argumentos: ', p.lista_argumentos, p[1], p[2]
    @_('expressao')
    def lista_argumentos(self, p):
        return p[0]

def main():
    lexer = LexerAnalysis()
    parser = ParserAnalysis()
    file = open('Inputs/' + sys.argv[1] + '.in', 'r')
    while True:
        try:
            data = str()
            for line in file:
                data += str(line)

        except EOFError:
            break
        if data:
            result = parser.parse(lexer.tokenize(data))
            if parser.i == 0:
                print("Semantic Error; The program have one or more list declaration!!!")
                exit()
            print(parser.i)
            print(result['Programa'])
            json_str = json.dumps(result, sort_keys=True, indent=2)
            # f = open('Outputs/'+ sys.argv[1] +'.out', 'w')
            # f.write(str(json_str))
            # f.close()
            # print(json_str)
            break


if __name__ == '__main__':
    main()
