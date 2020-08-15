from modules.lexer import Lexer
from modules.parser import Yacc

if __name__ == '__main__':
    f = open('./Testcases/boolean.txt', encoding='utf-8')
    data = f.read()
    f.close()

    y = Yacc()
    lexer = Lexer()
    y.build().parse(data, lexer.build(), False)

# lexer = Lexer().build()
    # lexer.input(data)
    #
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break  # No more input
    #     parsIndex = '-'
    #     i = -1
    #     # if tok.type == 'ID':
    #     #     i = Lexer.sTable.index(tok.value)
    #     # parsIndex = {'-1': '-'}.get(str(i), str(i))
    #     print(tok)
