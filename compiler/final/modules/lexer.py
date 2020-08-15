import ply.lex as lex


class Lexer:
    # reserved = {
    #     'Program': 'PROGRAM_KW',
    #     'Int': 'INT_KW',
    #     'Real': 'REAL_KW',
    #     'Bool': 'BOOL_KW',
    #     'Procedure': 'PROCEDURE_KW',
    #     'Function': 'FUNCTION_KW',
    #     'Begin': 'BEGIN_KW',
    #     'End': 'END_KW',
    #     'If': 'IF_KW',
    #     'Then': 'THEN_KW',
    #     'Else': 'ELSE_KW',
    #     'While': 'WHILE_KW',
    #     'Do': 'DO_KW',
    #     'For': 'FOR_KW',
    #     'To': 'TO_KW',
    #     'Downto': 'DOWNTO_KW',
    #     'Case': 'CASE_KW',
    #     'Return': 'RETURN_KW',
    #     'And Then': 'AND_THEN_KW',
    #     'Or Else': 'OR_ELSE_KW',
    #     'True': 'TRUE_KW',
    #     'False': 'FALSE_KW'
    # }

    literals = [
        '+',
        '-',
        '*',
        '/',
        ',',
        ':',
        ';',
        '(',
        ')'
    ]
    tokens = [
        'ID',
        'NUMBER_INT',
        'NUMBER_REAL',
        'ASSIGNMENT',
        'GT',
        'GE',
        'NE',
        'EQ',
        'LT',
        'LE',
        # 'COMMENT',
        'PROGRAM_KW',
        'INT_KW',
        'REAL_KW',
        'BOOL_KW',
        'PROCEDURE_KW',
        'FUNCTION_KW',
        'BEGIN_KW',
        'END_KW',
        'IF_KW',
        'THEN_KW',
        'ELSE_KW',
        'WHILE_KW',
        'DO_KW',
        'FOR_KW',
        'TO_KW',
        'DOWNTO_KW',
        'CASE_KW',
        'RETURN_KW',
        'AND_THEN_KW',
        'OR_ELSE_KW',
        'TRUE_KW',
        'FALSE_KW'
    ]

    t_PROGRAM_KW = r'Program'
    t_INT_KW = r'Int'
    t_REAL_KW = r'Real'
    t_BOOL_KW = r'Bool'
    t_PROCEDURE_KW = r'Procedure'
    t_FUNCTION_KW = r'Function'
    t_BEGIN_KW = r'Begin'
    t_END_KW = r'End'
    t_IF_KW = r'If'
    t_THEN_KW = r'Then'
    t_ELSE_KW = r'Else'
    t_WHILE_KW = r'While'
    t_DO_KW = r'Do'
    t_FOR_KW = r'For'
    t_TO_KW = r'To'
    t_DOWNTO_KW = r'Downto'
    t_CASE_KW = r'Case'
    t_RETURN_KW = r'Return'
    t_AND_THEN_KW = r'And[ ]Then'
    t_OR_ELSE_KW = r'Or[ ]Else'
    t_TRUE_KW = r'True'
    t_FALSE_KW = r'False'

    t_ASSIGNMENT = r':='

    t_GT = r'\.GT\.'
    t_GE = r'\.GE\.'
    t_NE = r'\.NE\.'
    t_EQ = r'\.EQ\.'
    t_LT = r'\.LT\.'
    t_LE = r'\.LE\.'

    # t_ignore_COMMENT = r'\#.*'
    t_ignore = ' \t'

    def t_NUMBER_REAL(self, t):
        r'\#[\+-]?[0-9]+\.[0-9]+'
        t.value = t.value[1:len(t.value)]
        while t.value[0] == '0' and t.value[1] != '.':
            t.value = t.value[1:len(t.value)]
        while t.value[len(t.value) - 1] == '0' and t.value[len(t.value) - 2] != '.':
            t.value = t.value[0:len(t.value) - 1]
        try:
            t.value = float(t.value)
        except ValueError:
            print('cant convert to float: ' + str(t.value))
        return t

    def t_NUMBER_INT(self, t):
        r'\#[\+-]?[0-9]+'
        t.value = t.value[1:len(t.value)]
        while t.value[0] == '0' and len(t.value) != 1:
            t.value = t.value[1:len(t.value)]
        try:
            t.value = int(t.value)
        except ValueError:
            print('cant convert to int: ' + str(t.value))
        return t

    def t_ID(self, t):
        r'[a-zA-Z][0-9][a-zA-Z_0-9]*'
        # TODO: future
        # if t.type == 'ID':
        #     if t.value not in self.sTable:
        #         self.sTable.append(t.value)
        return t

    def t_newline(self, t):
        r'\r?\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % (t.value[0]))
        t.lexer.skip(1)

    def build(self, **kwargs):
        '''
        build the lexer
        '''
        self.lexer = lex.lex(module=self, **kwargs)

        return self.lexer