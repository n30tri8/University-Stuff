from lexer import Lexer

if __name__ == '__main__':
    f = open('.\\test_files\\input3.txt', encoding='utf-8')
    data = f.read()
    f.close()
    lexer = Lexer().build()
    lexer.input(data)

    print('lexeme\t|\ttoken\t|\tattribute')
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input

        parsIndex = '-'
        i = -1
        if tok.type == 'ID':
            i = Lexer.sym_table.index(tok.value)
        parsIndex = {'-1': '-'}.get(str(i), str(i))
        print(str(tok.value) + "\t|\t" + tok.type + "\t|\t" + str(parsIndex))
    print('-'*30)
    print('symbol table:')
    print(Lexer.sym_table)
