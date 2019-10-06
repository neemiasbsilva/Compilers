from sly import Parser
from lexer import LexerAnalysis
from anytree import Node, RenderTree
import re
import json

class Expr:
    pass


class Program(Expr):
    def __init__(self, program):
        self.program = program

# class ListDeclaration(Expr):
#     def __init__(self, decl_left, decl_right):
#         self.decl_left = decl_left
#         self.decl_right = decl_right
#
# class Declaration(Expr):
#     def __init__(self, decl_variable):
#         self.decl_varible = decl_variable
#     def __init__(self, decl_function):
#         self.decl_function = fu

class ParserAnalysis(Parser):
    # Get token list from the lexer (required)
    tokens = LexerAnalysis.tokens

    # Grammar rules and actions
    @_('lista_declaracao')
    def programa(self, p):
        return Program(p.lista_declaracao)

    @_(' ')
    def empty(self, p):
        pass

    @_('declaracao aux0')
    def lista_declaracao(self, p):
        return "Lista_Declaracao:: ", p.declaracao, p.aux0
    @_('declaracao aux0')
    def aux0(self, p):
        return "Lista_Declaracao:: ", p.lista_declaracao, p.aux0
    @_('empty')
    def aux0(self, p):
        pass

    @_('declaracao_variaveis',
       'declaracao_funcoes')
    def declaracao(self, p):
        return "Declaracao:: ", p[0]

    @_('tipo ID ";" "[" NUMBER "]" ";"')
    def declaracao_variaveis(self, p):
        return "Declaracao_variaveis:: ", p[0], p[1], p[2], p[3], p[4], \
               p[5], p[6]
    @_('tipo ID "[" NUMBER "]" ";"')
    def declaracao_variaveis(self, p):
        return "Declaracao_variaveis:: ", p[0], p[1], p[2], p[3], p[4], p[5]
    @_('tipo ID ";"')
    def declaracao_variaveis(self, p):
        return "Declaracao_variaveis:: ", p[0], p[1], p[2]


    @_('INT', 'VOID')
    def tipo(self, p):
        return "Tipo:: ", p[0]

    @_('tipo ID "(" parametros ")" declaracao_composta')
    def declaracao_funcoes(self, p):
        return "Declaracao_funcoes:: ", p[0], p[1], p[2], p[3], p[4], p[5]

    @_('lista_parametros',
       'VOID')
    def parametros(self, p):
        return "Parametros:: ", p[0]
    @_('param aux1')
    def lista_parametros(self, p):
        return "Lista_parametros:: ", p[0], p[1]
    @_('"," param aux1')
    def aux1(self, p):
        return p[0], p[1]
    @_('empty')
    def aux1(self, p):
        pass

    @_('tipo ID "[" "]"')
    def param(self, p):
        return "Param:: ", p[0], p[1], p[2]
    @_('tipo ID')
    def param(self, p):
        return "Param:: ", p[0], p[1]

    @_('"{" declaracoes_locais lista_comandos "}"')
    def declaracao_composta(self, p):
        return ("Declaracao_composta:: ", p[0], p[1], p[2], p[3])

    @_('aux2')
    def declaracoes_locais(self, p):
        return "Declaracao_local:: ", p[0]

    @_('declaracao_variaveis aux2')
    def aux2(self, p):
        return p[0], p[1]
    @_('empty')
    def aux2(self, p):
        pass

    @_('aux3')
    def lista_comandos(self, p):
        return "Lista_comandos:: ", p[0]
    @_('comando aux3')
    def aux3(self, p):
        return p[0], p[1]

    @_('empty')
    def aux3(self, p):
        pass

    @_('declaracao_expressao',
       'declaracao_composta',
       'declaracao_selecao',
       'declaracao_iteracao',
       'declaracao_retorno')
    def comando(self, p):
        return "Comando:: ", p[0]

    @_('expressao ";"')
    def declaracao_expressao(self, p):
        return "Declaracao_expressao:: ", p[0], p[1]
    @_('";"')
    def declaracao_expressao(self, p):
        return "Declaracao_expressao:: ", p[0]

    @_('IF "(" expressao ")" comando')
    def declaracao_selecao(self, p):
        return "Declaracao_selecao:: ", p[0], p[1], p[2], p[3], p[4]

    @_('IF "(" expressao ")" comando ELSE comando')
    def declaracao_selecao(self, p):
        return "Declaracao_selecao:: ", p[0], p[1], p[2], p[3], p[4]

    @_('WHILE "(" expressao ")" comando')
    def declaracao_iteracao(self, p):
        return "Declaracao_iteracao:: ", p[0], p[1], p[2], p[3], p[4]

    @_('RETURN ";"')
    def declaracao_retorno(self, p):
        return "Declaracao_retorno:: ", p[0], p[1]

    @_('RETURN expressao ";"')
    def declaracao_retorno(self, p):
        return "Declaracao_retorno:: ", p[0], p[1], p[2]

    @_('variavel ASSIGN expressao')
    def expressao(self, p):
        return "Expressao:: ", p[0], p[1], p[2]

    @_('expressao_simples')
    def expressao(self, p):
        return "Expressao:: ", p[0]

    @_('ID "[" expressao "]"')
    def variavel(self, p):
        return "Variavel:: ", p[0], p[1], p[2], p[3]
    @_('ID')
    def variavel(self, p):
        return "Variavel:: ", p[0]

    @_('soma_expressao op_relacional soma_expressao')
    def expressao_simples(self, p):
        return "Expressao_simples:: ", p[0], p[1], p[2]

    @_('soma_expressao')
    def expressao_simples(self, p):
        return "Expressao_simples:: ", p[0]

    @_('LE', 'LT', 'GE', 'GT', 'EQ', 'NE')
    def op_relacional(self, p):
        return "Op_relacional:: ", p[0]

    @_('termo aux4')
    def soma_expressao(self, p):
        return "Soma_expressao:: ", p[0], p[1]
    @_('soma termo aux4')
    def aux4(self, p):
        return p[0], p[1], p[2]
    @_('empty')
    def aux4(self, p):
        pass

    @_('PLUS', 'MINUS')
    def soma(self, p):
        return "Soma:: ",p[0]

    @_('termo mult fator')
    def termo(self, p):
        return "Termo:: ", p[0], p[1], p[2]

    @_('fator')
    def termo(self, p):
        return "Termo:: ", p[0]

    @_('DIVIDE', 'TIMES')
    def mult(self, p):
        return "Mult:: ", p[0]

    @_('"(" expressao ")"')
    def fator(self, p):
        return "Fator:: ", p[0], p[1], p[2]

    @_('variavel', 'ativacao', 'NUMBER')
    def fator(self, p):
        return "Fator:: ", p[0]

    @_('ID "(" argumentos ")"')
    def ativacao(self, p):
        return "Ativacao:: ", p[0], p[1], p[2], p[3]

    @_('lista_argumentos', 'empty')
    def argumentos(self, p):
        return "Argumentos:: ", p[0]

    @_('expressao aux5')
    def lista_argumentos(self, p):
        return "Lista_argumentos:: ", p.expressao, p.aux5
    @_('"," expressao aux5')
    def aux5(self, p):
        return p[0], p[1]
    @_('empty')
    def aux5(self, p):
        pass



def main():
    lexer = LexerAnalysis()
    parser = ParserAnalysis()
    file = open('Inputs/sort.in', 'r')
    while True:
        try:
            data = str()
            for line in file:
                data += str(line)

        except EOFError:
            break
        if data:
            result = parser.parse(lexer.tokenize(data))
            json_str = json.dumps(result.program, sort_keys=True, indent=2)
            print('Programa:: {}'.format(json_str))
            with open()
            break


if __name__ == '__main__':
    main()
