from ply import yacc
from .lexer import Lexer
from common.entity import Entity
from common.symtable import SymbolTable
from .to_c import ToC


class QuadRuple:
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg_one = arg1
        self.arg_two = arg2
        self.result = result

    def __str__(self):
        t = (self.op, self.arg_one, self.arg_two, self.result)
        return str(t)


class Yacc:
    tokens = Lexer.tokens

    precedence = (
        ('left', 'OR_ELSE_KW'),
        ('left', 'AND_THEN_KW'),
        ('left', 'EQ', 'NE'),
        ('left', 'LT', 'GT', 'LE', 'GE'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        # ('nonassoc', 'ELSE_KW'),
        ('nonassoc', 'IFTHEN'),
        ('nonassoc', 'IFELSE'),
        ('nonassoc', 'normal_assign'),
        ('nonassoc', 'for_assign')
    )

    def __init__(self):
        self.quadruples = []
        self.symtables = []
        # self.offsets = []

    def p_program_1(self, p):
        """program : programInitiator PROGRAM_KW ID ';' declist block ';'
        """
        print('Rule 1.1: program → Program IDtoken ; declist block;')
        to_c = ToC(self.quadruples, self.symtables[0])
        c_file = open("output/main.c", "w+")
        c_file.write(to_c.to_c())
        c_file.close()

        q_file = open("output/quads.txt", "w+")
        for q in self.quadruples:
            q_file.write(str(q) + '\n')
        q_file.close()

    def p_program_2(self, p):
        """program : programInitiator PROGRAM_KW ID ';' block ';'"""

        print('Rule 1: program → Program IDtoken ; block;')
        to_c = ToC(self.quadruples, self.symtables[0])
        c_file = open("output/main.c", "w+")
        c_file.write(to_c.to_c())
        c_file.close()

        q_file = open("output/quads.txt", "w+")
        for q in self.quadruples:
            q_file.write(str(q) + '\n')
        q_file.close()

    def p_program_initiator(self, p):
        """programInitiator : empty"""
        SymbolTable.scope_seq = 0
        self.symtables.append(SymbolTable(None, 'scope', 'root'))

        print("Rule *: programInitiator -> empty")

    def p_declist_1(self, p):
        """declist : dec

        """
        print('Rule 2.1: declist → dec')

    def p_declist_2(self, p):
        """declist : declist dec
        """
        print('Rule 2.2: declist → declist dec')

    def p_dec_1(self, p):
        """dec : vardec
        """
        print('Rule 3.1: dec → vardec')

    def p_dec_2(self, p):
        """dec : procdec
        """
        print('Rule 3.2: dec → procdec')

    def p_dec_3(self, p):
        """dec : funcdec
        """
        print('Rule 3.3: dec → funcdec')

    def p_type_1(self, p):
        """type : INT_KW
        """
        print('Rule 4.1: type → Int')
        p[0] = 'Int'

    def p_type_2(self, p):
        """type : REAL_KW
        """
        print('Rule 4.2: type → Real')
        p[0] = 'Real'

    def p_type_3(self, p):
        """type : BOOL_KW
        """
        print('Rule 4.3: type → Bool')
        p[0] = 'Bool'

    def p_iddec_1(self, p):
        """iddec : ID
        """
        p[0] = (p[1], None)
        print('Rule 5.1: iddec → IDtoken')

    def p_iddec_2(self, p):
        """iddec : ID ASSIGNMENT exp
        """
        if p[3].type == 'bool':
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[3].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[3].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[0] = (p[1], t)
        else:
            p[0] = (p[1], p[3].place)
        print('Rule 5.2: iddec → IDtoken ∶= exp')

    def p_idlist_1(self, p):
        """idlist : iddec
        """
        p[0] = [p[1]]
        print('Rule 6.1: idlist → iddec ')

    def p_idlist_2(self, p):
        """idlist : idlist ',' iddec
        """
        p[0] = [*p[1], p[3]]
        print('Rule 6: idlist → idlist , iddec')

    def p_vardec(self, p):
        """vardec : type idlist ';'"""
        for (name, value) in p[2]:

            self.symtables[-1].insert_variable(name, p[1])
            if value is not None:
                name = self.symtables[-1].get_symbol_name(name)
                value = self.symtables[-1].get_symbol_name(value)
            self.quadruples.append(QuadRuple(op='=', arg1=value, arg2='', result=name))
        print('vardec → type idlist ;')

    def p_procdec_1(self, p):
        """procdec : PROCEDURE_KW ID '(' paramdecs_final ')' block ';'"""
        print('Rule 7.1: procdec → Procedure IDtoken ( paramdecs ) block ;')

    def p_procdec_2(self, p):
        """procdec : PROCEDURE_KW ID '(' paramdecs_final ')' declist block ';'"""
        print('Rule 7.2: procdec → Procedure IDtoken ( paramdecs ) declist block ;')

    def p_funcdec_1(self, p):
        """funcdec : funInitiator scopeInitiator block ';'"""
        s = self.symtables[-1]

        if s.header['return_type'] != 'void':
            y = Entity()
            y.place = '0'
            y.type = s.header['return_type']
            self.p_stmt_8(['', 'return', y])
        else:
            self.p_stmt_8(['', 'return'])

        self.symtables.pop()
        self.symtables[-1].insert_procedure(s)
        Entity.backpatch(p[1].next_list, len(self.quadruples))
        print('Rule 8.1: funcdec → Function IDtoken ( paramdecs ) ∶ type block ;')

    def p_funcdec_2(self, p):
        """funcdec : funInitiator scopeInitiator declist block ';'"""
        s = self.symtables[-1]

        if s.header['return_type'] != 'void':
            y = Entity()
            y.place = '0'
            y.type = s.header['return_type']
            self.p_stmt_8(['', 'return', y])
        else:
            self.p_stmt_8(['', 'return'])

        self.symtables.pop()
        self.symtables[-1].insert_procedure(s)
        Entity.backpatch(p[1].next_list, len(self.quadruples))
        print('Rule 8.2: funcdec → Function IDtoken ( paramdecs ) ∶ type declist block ;')

    def p_funInitiator(self, p):
        """
        funInitiator : FUNCTION_KW ID '(' quadder nexter paramdecs_final ')' ':' type
        """
        s = SymbolTable(self.symtables[-1], 'function', p[2])
        s.header['return_type'] = p[9]
        s.header['start'] = p[4].quad + 1
        #
        p[0] = Entity()
        p[0].next_list = p[5].next_list
        s.header['params'] = p[6]
        self.symtables.append(s)

    def p_paramdecs_final(self, p):
        """
        paramdecs_final : paramdecs
        """
        p[0] = p[1]
        index = 0
        for (name, type) in p[0]:
            index += 1
            self.quadruples.append(
                QuadRuple(op='seek',
                          arg1=index,
                          arg2=type,
                          result=self.symtables[-1].get_symbol_name(name)))

    def p_paramdecs_1(self, p):
        """paramdecs : paramdec
        """
        p[0] = p[1]
        print('Rule 9.1: paramdecs → paramdec')

    def p_paramdecs_2(self, p):
        """paramdecs : paramdecs ';' paramdec
        """
        p[0] = p[1] + p[3]
        print('Rule 9.2: paramdecs → paramdecs ; paramdec')

    def p_paramdec(self, p):
        """paramdec : type paramlist"""
        p[0] = []
        for name in p[2]:
            type = p[1]
            if '*' in name:
                name = name[:-1]
                type = type + '*'
            p[0].append((name, type))
            self.symtables[-1].insert_variable(name, type)
        print('Rule 10: paramdec → type paramlist')

    def p_paramlist_1(self, p):
        """paramlist : ID
        """
        p[0] = [p[1]]
        print('Rule 11.1: paramlist → IDtoken')

    def p_paramlist_2(self, p):
        """paramlist : paramlist ',' ID
        """
        p[0] = [*p[1], p[3]]
        print('Rule 11.2: paramlist → paramlist , IDtoken')

    def p_block_1(self, p):
        """block : BEGIN_KW scopeInitiator stmtlist END_KW
        """
        p[0] = Entity()
        # p[0].next_list = p[3].next_list
        s = self.symtables.pop()

        self.symtables[-1].insert_scope(s)
        print('Rule 12.1: block → Begin stmtlist End')

    def p_scope_initiator(self, p):
        """scopeInitiator : empty
        """
        self.symtables.append(SymbolTable(self.symtables[-1], 'scope'))
        print("Rule *: scopeInitiator -> empty")

    def p_block_2(self, p):
        """block : stmt
        """
        p[0] = p[1]
        print('Rule 12.2: block → stmt')

    def p_stmtlist_1(self, p):
        """stmtlist : stmt
        """
        p[0] = p[1]
        print('Rule 13.1: stmtlist → stmt')

    def p_stmtlist_2(self, p):
        """stmtlist : stmtlist ';' stmt
        """
        p[0] = Entity()
        if p[3] is not None:
            p[0].next_list = p[1].next_list + p[3].next_list

        print('Rule 13.2: stmtlist → stmtlist ; stmt')

    def p_lvalue(self, p):
        """lvalue : ID"""
        p[0] = Entity()
        p[0].place = p[1]
        p[0].type = self.symtables[-1].get_symbol_type(p[1])
        print('Rule 14: lvalue → IDtoken')

    def p_assign_stmt(self, p):
        """assignment_stmt : lvalue ASSIGNMENT exp
        """
        p[0] = Entity()
        p[0].type = p[1].type
        p[0].place = p[1].place

        if p[3].type == 'bool':
            Entity.backpatch(p[3].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='',
                                             result=self.symtables[-1].get_symbol_name(p[1].place)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[3].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='',
                                             result=self.symtables[-1].get_symbol_name(p[1].place)))
        else:
            self.quadruples.append(QuadRuple(op='=', arg1=self.symtables[-1].get_symbol_name(p[3].place),
                                             arg2='',
                                             result=self.symtables[-1].get_symbol_name(p[1].place)))
        print('Rule : assignment_stmt → lvalue ≔ exp')

    def p_assignment_stmt_1(self, p):
        """
        stmt : assignment_stmt %prec normal_assign
        """
        p[0] = p[1]
        print('Rule 15.1: stmt → lvalue ≔ exp')

    def p_selection_stmt_2(self, p):
        """
        stmt : selectionIfInitiator quadder block nexter quadder
        """
        p[0] = Entity()
        if p[3] is not None:
            p[0].next_list = p[3].next_list
        Entity.backpatch(p[1].true_list, p[2].quad)
        Entity.backpatch(p[1].false_list, p[5].quad)
        Entity.backpatch(p[4].next_list, p[5].quad)

        print("Rule 15.2: stmt ->",
              "IF_KW exp block")

    def p_selection_stmt_3(self, p):
        """stmt : selectionIfInitiator quadder block nexter ELSE_KW quadder block quadder %prec IFELSE
        """
        p[0] = Entity()
        p[0].next_list = p[3].next_list + p[7].next_list
        Entity.backpatch(p[1].true_list, p[2].quad)
        Entity.backpatch(p[1].false_list, p[6].quad)
        Entity.backpatch(p[4].next_list, p[8].quad)
        print("Rule 15.3: stmt ->",
              "IF_KW exp block ELSE_KW block")

    def p_selection_if_initiator(self, p):
        """ selectionIfInitiator : IF_KW exp THEN_KW %prec IFTHEN
        """
        p[0] = Entity()
        p[0].type = 'bool'
        if p[2].type == 'bool':
            p[0].true_list = p[2].true_list
            p[0].false_list = p[2].false_list
        else:
            self.quadruples.append(
                QuadRuple(op='if', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='', result=''))
            qt = QuadRuple(op='goto', arg1='-', arg2='', result='')
            self.quadruples.append(qt)
            p[0].true_list = [qt]
            qf = QuadRuple(op='goto', arg1='-', arg2='', result='')
            p[0].false_list = [qf]

            self.quadruples.append(qf)

    def p_iteration_stmt_4(self, p):
        """ stmt : iterationInitiator quadder block nexter
        """
        if p[3] is not None:
            Entity.backpatch(p[3].next_list, len(self.quadruples))
        Entity.backpatch(p[4].next_list, p[1].quad)
        Entity.backpatch(p[1].true_list, p[2].quad)
        Entity.backpatch(p[1].false_list, len(self.quadruples))
        print("Rule 15.4: stmt ->",
              "WHILE_KW exp DO_KW block")

    def p_iteration_initiator(self, p):
        """iterationInitiator : WHILE_KW quadder exp DO_KW
        """
        p[0] = Entity()
        p[0].type = 'bool'
        p[0].quad = p[2].quad
        if p[3].type == 'bool':
            p[0].true_list = p[3].true_list
            p[0].false_list = p[3].false_list
        else:
            self.quadruples.append(
                QuadRuple(op='if', arg1=self.symtables[-1].get_symbol_name(p[3].place), arg2='', result=''))
            qt = QuadRuple(op='goto', arg1='-', arg2='', result='')
            self.quadruples.append(qt)
            p[0].true_list = [qt]
            qf = QuadRuple(op='goto', arg1='-', arg2='', result='')
            p[0].false_list = [qf]
            self.quadruples.append(qf)

    def p_stmt_5(self, p):
        """
        stmt : for_init_up quadder block nexter
        """
        Entity.backpatch(p[4].next_list, p[1].quad)
        Entity.backpatch(p[1].false_list, p[2].quad)
        self.quadruples.insert(-1, QuadRuple(op='+', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='1',
                               result=self.symtables[-1].get_symbol_name(p[1].place)))
        Entity.backpatch(p[1].true_list, len(self.quadruples))
        if p[3] is not None:
            Entity.backpatch(p[3].next_list, len(self.quadruples))
        # TODO handle scoping in for variables
        print('Rule 15.5: stmt → For lvalue ∶= exp To exp Do block')

    def p_for_init_up(self, p):
        """
        for_init_up : forInitiator TO_KW quadder exp DO_KW
        """
        p[0] = Entity()
        p[0].place = p[1].place
        p[0].type = 'bool'
        p[0].quad = p[3].quad
        p[2] = ">"
        # TODO what if init var or exp be boolean? handle like exp > exp rule
        self.quadruples.append(QuadRuple(op='if', result='',
                                         arg1='%s %s %s' % (self.symtables[-1].get_symbol_name(p[1].place),
                                                            self.symtables[-1].get_symbol_name(p[2]),
                                                            self.symtables[-1].get_symbol_name(p[4].place)),
                                         arg2=''))
        qt = QuadRuple(op='goto', result='', arg1='-', arg2='')
        qf = QuadRuple(op='goto', result='', arg1='-', arg2='')
        p[0].true_list.append(qt)
        p[0].false_list.append(qf)
        self.quadruples.append(qt)
        self.quadruples.append(qf)

    def p_stmt_6(self, p):
        """
        stmt : for_init_down quadder block nexter
        """
        Entity.backpatch(p[4].next_list, p[1].quad)
        Entity.backpatch(p[1].false_list, p[2].quad)
        if self.symtables[-1].get_symbol_name(p[1].place) is not None:
            self.quadruples.insert(-1, QuadRuple(op='-', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='1',
                               result=self.symtables[-1].get_symbol_name(p[1].place)))
        else:
            self.quadruples.insert(-1, QuadRuple(op='-', arg1='n2', arg2='1',
                                                 result='n2'))
        Entity.backpatch(p[1].true_list, len(self.quadruples))
        if p[3] is not None:
            Entity.backpatch(p[3].next_list, len(self.quadruples))
        print('Rule 15.6: stmt → For lvalue ∶= exp Downto exp Do block')

    def p_for_init_down(self, p):
        """
        for_init_down : forInitiator DOWNTO_KW quadder exp DO_KW
        """
        p[0] = Entity()
        p[0].type = 'bool'
        p[0].quad = p[3].quad
        p[2] = "<"
        # TODO what if init var or exp be boolean? handle like exp > exp rule
        self.quadruples.append(QuadRuple(op='if', result='',
                                         arg1='%s %s %s' % (self.symtables[-1].get_symbol_name(p[1].place),
                                                            self.symtables[-1].get_symbol_name(p[2]),
                                                            self.symtables[-1].get_symbol_name(p[4].place)),
                                         arg2=''))
        qt = QuadRuple(op='goto', result='', arg1='-', arg2='')
        qf = QuadRuple(op='goto', result='', arg1='-', arg2='')
        p[0].true_list.append(qt)
        p[0].false_list.append(qf)
        self.quadruples.append(qt)
        self.quadruples.append(qf)

    def p_for_initiator(self, p):
        """
        forInitiator : FOR_KW assignment_stmt %prec for_assign
        """
        p[0] = p[2]

    def p_stmt_7(self, p):
        """stmt : CASE_KW exp nexter caseelement END_KW quadder
        """
        Entity.backpatch(p[3].next_list, p[6].quad)
        case_next = []
        for i in range(len(p[4].case_dict)):
            key = p[4].case_dict[i][0]
            case_entry = p[4].case_dict[i][1]
            q1 = QuadRuple(op='if', arg1=str(self.symtables[-1].get_symbol_name(p[2].place)) + ' == ' + str(self.symtables[
                -1].get_symbol_name(key)), arg2='', result='')
            q2 = QuadRuple(op='goto', arg1=str(case_entry[0]), arg2='', result='')
            self.quadruples.append(q1)
            self.quadruples.append(q2)
            case_next.append(case_entry[1])


        # just for compatiblity
        Entity.backpatch(case_next, len(self.quadruples))

        if len(p[4].next_list) != 0:
            Entity.backpatch(p[4].next_list, len(self.quadruples))

        print('Rule 15.7: stmt → Case exp caseelement End')

    def p_caseelement_1(self, p):
        """caseelement : NUMBER_INT ':' quadder block ';' nexter
        """
        p[0] = Entity()

        p[0].next_list = p[6].next_list

        # just for compatiblity
        q1 = QuadRuple(op='goto', arg1='-', arg2='', result='')
        self.quadruples.append(q1)
        p[0].case_dict.append([str(p[1]), [str(p[3].quad), q1]])
        print('Rule 16.1: caseelement → INTtoken ∶ block ;')

    def p_caseelement_2(self, p):
        """caseelement : caseelement NUMBER_INT ':' quadder block ';' nexter
        """
        p[0] = Entity()

        p[0].next_list = p[7].next_list + p[1].next_list

        # just for compatiblity
        q1 = QuadRuple(op='goto', arg1='-', arg2='', result='')
        # self.quadruples.append(q1)

        p[0].case_dict += (p[1].case_dict)

        p[0].case_dict.append([str(p[2]), [str(p[4].quad), q1]])
        print('Rule 16.2: caseelement → caseelement INTtoken ∶ block ;')

    def p_stmt_8(self, p):
        """stmt : RETURN_KW exp
        """
        p[0] = Entity()
        # Our function symbol table
        s = self.symtables[-1].get_parent_function()

        # Create return statement if in main
        if s.name == '#aa11':
            self.quadruples.append(QuadRuple(op='return', result='', arg1='', arg2=''))
            return

        # Restore previous location
        t1 = self.symtables[-1].new_temp('jmp_buf')
        self.quadruples.append(
            QuadRuple(op='pop', result='%s' % self.symtables[-1].get_symbol_name(t1), arg1='jmp_buf', arg2=''))

        if p[2].type == 'bool':
            t2 = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[2].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t2)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[2].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t2)))
            self.quadruples.append(
                QuadRuple(op='push', result='', arg1=self.symtables[-1].get_symbol_name(t2), arg2='int'))
        else:
            t2 = self.symtables[-1].new_temp(p[2].type)
            self.quadruples.append(QuadRuple(op='=', result=self.symtables[-1].get_symbol_name(t2),
                                             arg1=self.symtables[-1].get_symbol_name(p[2].place), arg2=p[2].type))
            self.quadruples.append(
                QuadRuple(op='push', result='', arg1=self.symtables[-1].get_symbol_name(t2), arg2=p[2].type))

        # Goto to previous location
        self.quadruples.append(
            QuadRuple(op='longjmp', arg1=self.symtables[-1].get_symbol_name(t1), arg2='1820', result=''))
        print('Rule 15.8: stmt → Return exp')

    def p_stmt_9(self, p):
        """stmt : exp
        """
        p[0] = p[1]
        print('Rule 15.9: stmt →  exp')

    def p_and_initiator(self, p):  # TODO wrong result
        """andInitiator : exp AND_THEN_KW
        """
        p[0] = Entity()
        p[0].type = 'bool'
        if p[1].type == 'bool':
            p[0].true_list = p[1].true_list
            p[0].false_list = p[1].false_list
        else:
            self.quadruples.append(
                QuadRuple(op='if', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='', result=''))
            qt = QuadRuple(op='goto', arg1='-', arg2='', result='')
            self.quadruples.append(qt)
            p[0].true_list = [qt]
            qf = QuadRuple(op='goto', arg1='-', arg2='', result='')
            p[0].false_list = [qf]
            self.quadruples.append(qf)

    def p_exp_1(self, p):
        """exp : andInitiator quadder exp
        """
        p[0] = Entity()
        p[0].type = 'bool'
        Entity.backpatch(p[1].true_list, p[2].quad)
        if p[3].type == 'bool':
            p[0].false_list = p[1].false_list + p[3].false_list
            p[0].true_list = p[3].true_list
        else:
            self.quadruples.append(
                QuadRuple(op='if', arg1=self.symtables[-1].get_symbol_name(p[3].place), arg2='', result=''))
            qt = QuadRuple(op='goto', arg1='-', arg2='', result='')
            self.quadruples.append(qt)
            qf = QuadRuple(op='goto', arg1='-', arg2='', result='')
            p[0].false_list = p[1].false_list + [qf]
            p[0].true_list = [qt]

            self.quadruples.append(qf)

        print('Rule 16.1: exp → exp And Then exp ')

    def p_or_initiator(self, p):  # TODO wrong result
        """orInitiator : exp OR_ELSE_KW
        """
        p[0] = Entity()
        p[0].type = 'bool'
        if p[1].type == 'bool':
            p[0].true_list = p[1].true_list
            p[0].false_list = p[1].false_list
        else:
            self.quadruples.append(
                QuadRuple(op='if', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='', result=''))
            qt = QuadRuple(op='goto', arg1='-', arg2='', result='')
            self.quadruples.append(qt)
            p[0].true_list = [qt]
            qf = QuadRuple(op='goto', arg1='-', arg2='', result='')
            p[0].false_list = [qf]
            self.quadruples.append(qf)

    def p_exp_2(self, p):
        """exp : orInitiator quadder exp
        """
        p[0] = Entity()
        p[0].type = 'bool'
        Entity.backpatch(p[1].false_list, p[2].quad)
        if p[3].type == 'bool':
            p[0].true_list = p[1].true_list + p[3].true_list
            p[0].false_list = p[3].false_list
        else:
            self.quadruples.append(
                QuadRuple(op='if', arg1=self.symtables[-1].get_symbol_name(p[3].place), arg2='', result=''))
            qt = QuadRuple(op='goto', arg1='-', arg2='', result='')
            self.quadruples.append(qt)
            p[0].true_list = p[1].true_list + [qt]
            qf = QuadRuple(op='goto', arg1='-', arg2='', result='')
            p[0].false_list = [qf]
            self.quadruples.append(qf)

        print('Rule 16.2: exp → exp Or Else exp ')

    def p_exp_3(self, p):
        """exp : exp '+' quadder exp
        """
        p[0] = Entity()
        if p[1].type == 'bool':
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[4].type)
                p[0].type = p[4].type
                q1 = QuadRuple(op='+', arg1='1', arg2=self.symtables[-1].get_symbol_name(p[4].place),
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=self.symtables[-1].get_symbol_name(p[4].place), arg2='',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q1)
                Entity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                Entity.backpatch(p[1].false_list, len(self.quadruples) - 1)
            else:
                p[0].place = self.symtables[-1].new_temp('int')
                p[0].type = 'int'
                q1 = QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(p[0].place))
                q4 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q5 = QuadRuple(op='+', arg1=self.symtables[-1].get_symbol_name(p[0].place), arg2='1',
                               result=self.symtables[-1].get_symbol_name(p[0].place))

                self.quadruples.append(q1)
                Entity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                Entity.backpatch(p[1].false_list, len(self.quadruples) - 1)
                self.quadruples.append(q4)
                self.quadruples.append(q5)
                Entity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                Entity.backpatch(p[4].false_list, len(self.quadruples))
        else:
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q = QuadRuple(op='+', arg1=self.symtables[-1].get_symbol_name(p[1].place),
                              arg2=self.symtables[-1].get_symbol_name(p[4].place),
                              result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q)
            else:
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q1 = QuadRuple(op='+', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='1',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q1)
                Entity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)

                Entity.backpatch(p[4].false_list, len(self.quadruples) - 1)

        print('Rule 16.3: exp → exp + exp ')

    def p_exp_4(self, p):
        """exp : exp '-' quadder exp
        """
        p[0] = Entity()
        if p[1].type == 'bool':
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[4].type)
                p[0].type = p[4].type
                q1 = QuadRuple(op='-', arg1='1', arg2=self.symtables[-1].get_symbol_name(p[4].place),
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=self.symtables[-1].get_symbol_name(p[4].place), arg2='',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q1)
                Entity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                Entity.backpatch(p[1].false_list, len(self.quadruples) - 1)
            else:
                p[0].place = self.symtables[-1].new_temp('int')
                p[0].type = 'int'
                q1 = QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(p[0].place))
                q4 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q5 = QuadRuple(op='-', arg1=self.symtables[-1].get_symbol_name(p[0].place), arg2='1',
                               result=self.symtables[-1].get_symbol_name(p[0].place))

                self.quadruples.append(q1)
                Entity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                Entity.backpatch(p[1].false_list, len(self.quadruples) - 1)
                self.quadruples.append(q4)
                self.quadruples.append(q5)
                Entity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                Entity.backpatch(p[4].false_list, len(self.quadruples))
        else:
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q = QuadRuple(op='-', arg1=self.symtables[-1].get_symbol_name(p[1].place),
                              arg2=self.symtables[-1].get_symbol_name(p[4].place),
                              result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q)
            else:
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q1 = QuadRuple(op='-', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='1',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q1)
                Entity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                Entity.backpatch(p[4].false_list, len(self.quadruples) - 1)

        print('Rule 16.4: exp →  exp - exp ')

    def p_exp_5(self, p):
        """exp : exp '*' quadder exp
        """
        p[0] = Entity()
        if p[1].type == 'bool':
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[4].type)
                p[0].type = p[4].type
                q1 = QuadRuple(op='*', arg1='1', arg2=self.symtables[-1].get_symbol_name(p[4].place),
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=self.symtables[-1].get_symbol_name(p[4].place), arg2='',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q1)
                Entity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                Entity.backpatch(p[1].false_list, len(self.quadruples) - 1)
            else:
                p[0].place = self.symtables[-1].new_temp('int')
                p[0].type = 'int'
                q1 = QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(p[0].place))
                q4 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q5 = QuadRuple(op='*', arg1=self.symtables[-1].get_symbol_name(p[0].place), arg2='1',
                               result=self.symtables[-1].get_symbol_name(p[0].place))

                self.quadruples.append(q1)
                Entity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                Entity.backpatch(p[1].false_list, len(self.quadruples) - 1)
                self.quadruples.append(q4)
                self.quadruples.append(q5)
                Entity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                Entity.backpatch(p[4].false_list, len(self.quadruples))
        else:
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q = QuadRuple(op='*', arg1=self.symtables[-1].get_symbol_name(p[1].place),
                              arg2=self.symtables[-1].get_symbol_name(p[4].place),
                              result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q)
            else:
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q1 = QuadRuple(op='*', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='1',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q1)
                Entity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)

                Entity.backpatch(p[4].false_list, len(self.quadruples) - 1)

        print('Rule 16.5: exp → exp ∗ exp ')

    def p_exp_6(self, p):
        """exp : exp '/' quadder exp
        """
        p[0] = Entity()
        if p[1].type == 'bool':
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[4].type)
                p[0].type = p[4].type
                q1 = QuadRuple(op='/', arg1='1', arg2=self.symtables[-1].get_symbol_name(p[4].place),
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=self.symtables[-1].get_symbol_name(p[4].place), arg2='',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q1)
                Entity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                Entity.backpatch(p[1].false_list, len(self.quadruples) - 1)
            else:
                p[0].place = self.symtables[-1].new_temp('int')
                p[0].type = 'int'
                q1 = QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q3 = QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(p[0].place))
                q4 = QuadRuple(op='goto', arg1=p[3].quad, arg2='', result='')
                q5 = QuadRuple(op='/', arg1=self.symtables[-1].get_symbol_name(p[0].place), arg2='1',
                               result=self.symtables[-1].get_symbol_name(p[0].place))

                self.quadruples.append(q1)
                Entity.backpatch(p[1].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)
                Entity.backpatch(p[1].false_list, len(self.quadruples) - 1)
                self.quadruples.append(q4)
                self.quadruples.append(q5)
                Entity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                Entity.backpatch(p[4].false_list, len(self.quadruples))
        else:
            if p[4].type != 'bool':
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q = QuadRuple(op='/', arg1=self.symtables[-1].get_symbol_name(p[1].place),
                              arg2=self.symtables[-1].get_symbol_name(p[4].place),
                              result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q)
            else:
                p[0].place = self.symtables[-1].new_temp(p[1].type)
                p[0].type = p[1].type
                q1 = QuadRuple(op='/', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='1',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                q2 = QuadRuple(op='goto', arg1=len(self.quadruples) + 3, arg2='', result='')
                q3 = QuadRuple(op='=', arg1=self.symtables[-1].get_symbol_name(p[1].place), arg2='',
                               result=self.symtables[-1].get_symbol_name(p[0].place))
                self.quadruples.append(q1)
                Entity.backpatch(p[4].true_list, len(self.quadruples) - 1)
                self.quadruples.append(q2)
                self.quadruples.append(q3)

                Entity.backpatch(p[4].false_list, len(self.quadruples) - 1)

        print('Rule 16.6: exp → exp / exp ')

    def p_exp_7(self, p):
        """exp : '(' exp ')'
        """
        p[0] = p[2]
        print('Rule 16.7: exp → ( exp ) ')

    def p_exp_9(self, p):
        """exp : NUMBER_INT
        """
        p[0] = Entity()
        p[0].place = p[1]
        p[0].type = 'Int'
        print('Rule 16.9: exp → INTtoken ')

    def p_exp_10(self, p):
        """exp : NUMBER_REAL
        """
        p[0] = Entity()
        p[0].place = p[1]
        p[0].type = 'Real'
        print('Rule 16.10: exp → REALtoken ')

    def p_exp_11(self, p):
        """exp : TRUE_KW
        """
        p[0] = Entity()
        p[0].type = 'bool'
        q = QuadRuple(result='', op='goto', arg1='-', arg2='')
        p[0].true_list.append(q)

        self.quadruples.append(q)
        print('Rule 16.11: exp → True ')

    def p_exp_12(self, p):
        """exp : FALSE_KW
        """
        p[0] = Entity()
        p[0].type = 'bool'
        q = QuadRuple(result='', op='goto', arg1='-', arg2='')
        p[0].false_list.append(q)
        self.quadruples.append(q)
        print('Rule 16.12: exp → False ')

    def p_exp_13(self, p):
        """exp : lvalue
        """
        p[0] = p[1]  # TODO: check it?
        print('Rule 16.13: exp → lvalue ')

    def p_exp_14(self, p):
        """exp : ID '(' explist ')'
        """
        # Called function is ours or defines in root
        s = self.symtables[-1].get_parent_function()
        if s.name != p[1]:
            s = self.symtables[0].symbols[p[1]]

        # Provides place if function return something
        if s.header['return_type'] != 'void':
            p[0] = Entity()
            p[0].type = s.header['return_type']
            p[0].place = self.symtables[-1].new_temp(p[0].type)

        # Push the current state
        self.quadruples.append(
            QuadRuple(op='store_env', arg1=self.symtables[-1].get_parent_function(), arg2='', result=''))

        # Push the arguments
        for (name, type) in reversed(p[3]):
            t = self.symtables[-1].new_temp(type)
            self.quadruples.append(QuadRuple(op='=', arg1=self.symtables[-1].get_symbol_name(name), arg2='',
                                             result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(
                QuadRuple(op='push', arg1=self.symtables[-1].get_symbol_name(t), arg2=type, result=''))

        # Setjmp and check it's return value
        t1 = self.symtables[-1].new_temp('int')
        t2 = self.symtables[-1].new_temp('jmp_buf')
        self.quadruples.append(QuadRuple(op='setjmp', arg1=self.symtables[-1].get_symbol_name(t2), arg2='',
                                         result=self.symtables[-1].get_symbol_name(t1)))
        self.quadruples.append(
            QuadRuple(op='if', arg1='%s != 1820' % self.symtables[-1].get_symbol_name(t1), arg2='', result=''))
        self.quadruples.append(
            QuadRuple(op='push', arg1='%s' % self.symtables[-1].get_symbol_name(t2), arg2='jmp_buf', result=''))
        self.quadruples.append(
            QuadRuple(op='if', arg1='%s != 1820' % self.symtables[-1].get_symbol_name(t1), arg2='', result=''))
        self.quadruples.append(QuadRuple(op='goto', arg1=s.header['start'], arg2='', result=''))
        # Pop the function return value
        if s.header['return_type'] != 'void':
            self.quadruples.append(
                QuadRuple(op='pop', arg1=p[0].type, arg2='', result=self.symtables[-1].get_symbol_name(p[0].place)))

        # Pop the arguments
        for _ in p[3]:
            self.quadruples.append(QuadRuple(op='pop', arg1='', arg2='', result=''))

        # Pop the current state
        if s.header['return_type'] != 'void':
            self.quadruples.append(QuadRuple(op='restore_env', arg1=self.symtables[-1].get_parent_function(),
                                             arg2=self.symtables[-1].get_symbol_name(p[0].place), result=''))
        else:
            self.quadruples.append(
                QuadRuple(op='restore_env', arg1=self.symtables[-1].get_parent_function(), arg2='', result=''))

        print('Rule 16.14: IDtoken ( explist ) ')

    def p_exp_15(self, p):
        """exp : exp GT quadder exp
        """
        p[2] = ">"
        p[0] = Entity()
        p[0].type = 'bool'
        if p[1].type == 'bool':
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[1].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[1].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[1].place = t
        if p[4].type == 'bool':
            self.quadruples.append(QuadRuple(op='goto', arg1=p[3].quad, arg2='', result=''))
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[4].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[4].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[4].place = t

        self.quadruples.append(QuadRuple(op='if', result='',
                                         arg1='%s %s %s' % (self.symtables[-1].get_symbol_name(p[1].place),
                                                            self.symtables[-1].get_symbol_name(p[2]),
                                                            self.symtables[-1].get_symbol_name(p[4].place)),
                                         arg2=''))
        qt = QuadRuple(op='goto', result='', arg1='-', arg2='')
        qf = QuadRuple(op='goto', result='', arg1='-', arg2='')
        p[0].true_list.append(qt)
        p[0].false_list.append(qf)
        self.quadruples.append(qt)
        self.quadruples.append(qf)
        print('Rule 16.15: exp →  exp -> GT')

    def p_exp_16(self, p):
        """exp : exp GE quadder exp
        """
        p[2] = ">="
        p[0] = Entity()
        p[0].type = 'bool'
        if p[1].type == 'bool':
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[1].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[1].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[1].place = t
        if p[4].type == 'bool':
            self.quadruples.append(QuadRuple(op='goto', arg1=p[3].quad, arg2='', result=''))
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[4].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[4].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[4].place = t

        self.quadruples.append(QuadRuple(op='if', result='',
                                         arg1='%s %s %s' % (self.symtables[-1].get_symbol_name(p[1].place),
                                                            self.symtables[-1].get_symbol_name(p[2]),
                                                            self.symtables[-1].get_symbol_name(p[4].place)),
                                         arg2=''))
        qt = QuadRuple(op='goto', result='', arg1='-', arg2='')
        qf = QuadRuple(op='goto', result='', arg1='-', arg2='')
        p[0].true_list.append(qt)
        p[0].false_list.append(qf)
        self.quadruples.append(qt)
        self.quadruples.append(qf)
        print('Rule 16.16: exp → exp -> GE')

    def p_exp_17(self, p):
        """exp : exp NE quadder exp
        """
        p[2] = "!="
        p[0] = Entity()
        p[0].type = 'bool'
        if p[1].type == 'bool':
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[1].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[1].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[1].place = t
        if p[4].type == 'bool':
            self.quadruples.append(QuadRuple(op='goto', arg1=p[3].quad, arg2='', result=''))
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[4].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[4].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[4].place = t

        self.quadruples.append(QuadRuple(op='if', result='',
                                         arg1='%s %s %s' % (self.symtables[-1].get_symbol_name(p[1].place),
                                                            self.symtables[-1].get_symbol_name(p[2]),
                                                            self.symtables[-1].get_symbol_name(p[4].place)),
                                         arg2=''))
        qt = QuadRuple(op='goto', result='', arg1='-', arg2='')
        qf = QuadRuple(op='goto', result='', arg1='-', arg2='')
        p[0].true_list.append(qt)
        p[0].false_list.append(qf)
        self.quadruples.append(qt)
        self.quadruples.append(qf)
        print('Rule 16.17: exp → exp -> NE')

    def p_exp_18(self, p):
        """exp : exp EQ quadder exp
        """
        p[2] = "=="
        p[0] = Entity()
        p[0].type = 'bool'
        if p[1].type == 'bool':
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[1].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[1].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[1].place = t
        if p[4].type == 'bool':
            self.quadruples.append(QuadRuple(op='goto', arg1=p[3].quad, arg2='', result=''))
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[4].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[4].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[4].place = t

        self.quadruples.append(QuadRuple(op='if', result='',
                                         arg1='%s %s %s' % (self.symtables[-1].get_symbol_name(p[1].place),
                                                            self.symtables[-1].get_symbol_name(p[2]),
                                                            self.symtables[-1].get_symbol_name(p[4].place)),
                                         arg2=''))
        qt = QuadRuple(op='goto', result='', arg1='-', arg2='')
        qf = QuadRuple(op='goto', result='', arg1='-', arg2='')
        p[0].true_list.append(qt)
        p[0].false_list.append(qf)
        self.quadruples.append(qt)
        self.quadruples.append(qf)
        print('Rule 16.18: exp → exp -> EQ')

    def p_exp_19(self, p):
        """exp : exp LT quadder exp
        """
        p[2] = "<"
        p[0] = Entity()
        p[0].type = 'bool'
        if p[1].type == 'bool':
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[1].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[1].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[1].place = t
        if p[4].type == 'bool':
            self.quadruples.append(QuadRuple(op='goto', arg1=p[3].quad, arg2='', result=''))
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[4].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[4].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[4].place = t

        self.quadruples.append(QuadRuple(op='if', result='',
                                         arg1='%s %s %s' % (self.symtables[-1].get_symbol_name(p[1].place),
                                                            self.symtables[-1].get_symbol_name(p[2]),
                                                            self.symtables[-1].get_symbol_name(p[4].place)),
                                         arg2=''))
        qt = QuadRuple(op='goto', result='', arg1='-', arg2='')
        qf = QuadRuple(op='goto', result='', arg1='-', arg2='')
        p[0].true_list.append(qt)
        p[0].false_list.append(qf)
        self.quadruples.append(qt)
        self.quadruples.append(qf)
        print('Rule 16.19: exp → exp -> LT')

    def p_exp_20(self, p):
        """exp : exp LE quadder exp
        """
        p[2] = "<="
        p[0] = Entity()
        p[0].type = 'bool'
        if p[1].type == 'bool':
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[1].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[1].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[1].place = t
        if p[4].type == 'bool':
            self.quadruples.append(QuadRuple(op='goto', arg1=p[3].quad, arg2='', result=''))
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[4].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[4].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[4].place = t

        self.quadruples.append(QuadRuple(op='if', result='',
                                         arg1='%s %s %s' % (self.symtables[-1].get_symbol_name(p[1].place),
                                                            self.symtables[-1].get_symbol_name(p[2]),
                                                            self.symtables[-1].get_symbol_name(p[4].place)),
                                         arg2=''))
        qt = QuadRuple(op='goto', result='', arg1='-', arg2='')
        qf = QuadRuple(op='goto', result='', arg1='-', arg2='')
        p[0].true_list.append(qt)
        p[0].false_list.append(qf)
        self.quadruples.append(qt)
        self.quadruples.append(qf)

        print('Rule 16.20: exp → exp -> LE')

    def p_explist_1(self, p):
        """explist : exp
        """
        if p[1].type == 'bool':
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[1].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[1].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            p[0] = [(t, 'int')]
        else:
            p[0] = [(p[1].place, p[1].type)]
        print('Rule 17.1: explist → exp')

    def p_explist_2(self, p):
        """explist : explist ',' exp
        """
        if p[3].type == 'bool':
            t = self.symtables[-1].new_temp('int')
            Entity.backpatch(p[3].true_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='1', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            self.quadruples.append(QuadRuple(op='goto', arg1=len(self.quadruples) + 2, arg2='', result=''))
            Entity.backpatch(p[3].false_list, len(self.quadruples))
            self.quadruples.append(QuadRuple(op='=', arg1='0', arg2='', result=self.symtables[-1].get_symbol_name(t)))
            if p[0] is not None:
                p[0] = p[1].append((t, 'int'))
            else:
                p[0] = [(t, 'int')]
        else:
            if p[0] is not None:
                p[0] = p[1].append((p[3].place, p[3].type))
            else:
                p[0] = [(p[3].place, p[3].type)]
        print('Rule 17.2: explist → explist , exp')

    def p_quadder(self, p):
        """quadder : empty
        """
        p[0] = Entity()
        p[0].quad = len(self.quadruples)

        print("Rule Quadder: quadder -> quadder -> empty")

    def p_nexter(self, p):
        """nexter : empty
        """
        p[0] = Entity()
        q = QuadRuple(op='goto', arg1='-', arg2='', result='')
        p[0].next_list.append(q)
        self.quadruples.append(q)

    def p_empty(self, p):
        """empty :
        """
        pass

    def p_error(self, p):
        print("unknown text at %r" % (p.value,))

    def build(self, **kwargs):
        """
        build the parser
        """
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
