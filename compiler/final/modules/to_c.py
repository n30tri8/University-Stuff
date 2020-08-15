from common.symtable import SymbolTable


class ToC:
    def __init__(self, quadruples, symtable):
        self.quadruples = quadruples
        self.symtable = symtable
        self.env = {}

    def store_env(self, symbol_table):
        # Push the environment from the symbol table
        self.env[symbol_table.name] = []
        code = "/* Store the environment of %s */\n" % symbol_table.name
        q = []
        q.append(symbol_table)
        while bool(q):
            t = q.pop()
            for symbol in t.symbols:
                if isinstance(t.symbols[symbol], str):
                    qn = t.get_symbol_name(symbol)
                    code += '\tstack_push(main_stack, &%s, sizeof(%s));\n' % (qn, t.symbols[symbol])
                    self.env[symbol_table.name].append((qn, t.symbols[symbol]))
                elif isinstance(t.symbols[symbol], SymbolTable):
                    s = t.symbols[symbol]
                    if s.type == 'scope':
                        q.append(s)
        return code

    def restore_env(self, symbol_table, return_storage):
        # Pop the environment from the symbol table
        code = "/* Restore the environment of %s */\n" % symbol_table.name
        for (name, type) in reversed(self.env[symbol_table.name]):
            if name == return_storage:
                code += '\tstack_pop(main_stack, NULL, 0);\n'
            else:
                code += '\tstack_pop(main_stack, &%s, sizeof(%s));\n' % (name, type)
        del self.env[symbol_table.name]
        return code

    def to_c(self):
        c_code = ""

        # Objects array for allocating and deallocating
        objects = []

        # Includes :)
        c_code += "#include <stdio.h>\n"
        c_code += "#include <stdlib.h>\n"
        c_code += "#include <setjmp.h>\n"
        c_code += '\n'
        c_code += '#include "stack.h"\n'
        c_code += '\n'

        # Variable declaration based on BFS
        q = []
        q.append(self.symtable)
        while bool(q):
            t = q.pop()
            for symbol in t.symbols:
                if isinstance(t.symbols[symbol], str):
                    qn = t.get_symbol_name(symbol)
                    if t.symbols[symbol] in ['Int', 'Real']:
                        pn = 'double'
                    elif t.symbols[symbol] in ['Bool']:
                        pn = 'boolean'
                    else:
                        print(t.symbols[symbol])
                    c_code += '%s %s;\n' % (pn, qn)
                elif isinstance(t.symbols[symbol], SymbolTable):
                    s = t.symbols[symbol]
                    q.append(s)
        c_code += '\n'

        # Main !
        c_code += "int main(){\n"

        # Stack initiation
        c_code += "\tstruct stack *main_stack;\n"
        c_code += "\n"
        c_code += "\tmain_stack = stack_create();\n"

        # QuadRuples to code
        noq = len(self.quadruples)
        for i, entry in enumerate(self.quadruples):

            op = entry.op
            arg1 = entry.arg_one
            arg2 = entry.arg_two
            result = entry.result

            line = ''
            if op == 'if':
                line += "if (" + str(arg1) + ")"
            elif op == 'goto':
                line += "goto " + self.make_label(arg1) + ";"
            elif op == '+':
                line += str(result) + " = " + str(arg1) + " + " + str(arg2) + ";"
            elif op == '-':
                line += str(result) + " = " + str(arg1) + " - " + str(arg2) + ";"
            elif op == '*':
                line += str(result) + " = " + str(arg1) + " * " + str(arg2) + ";"
            elif op == '/':
                line += str(result) + " = " + str(arg1) + " / " + str(arg2) + ";"
            elif op == '%':
                line += str(result) + " = " + str(arg1) + " % " + str(arg2) + ";"
            elif op == "=":
                if arg1 is None:
                    arg1 = 0
                line += str(result) + " = " + str(arg1) + ";"
            elif op == "rand":
                line += str(result) + " = rand();"
            elif op == "push":
                line += "stack_push(main_stack, &%s, sizeof(%s));" % (arg1, arg2)
            elif op == "pop":
                if result != '':
                    line += "stack_pop(main_stack, &%s, sizeof(%s));" % (result, arg1)
                else:
                    line += "stack_pop(main_stack, NULL, 0);"
            elif op == "seek":
                line += "stack_seek(main_stack, %d, &%s, sizeof(%s));" % (arg1, result, arg2)
            elif op == "return":
                line += "return 0;"
            elif op == "setjmp":
                line += "%s = setjmp(%s);" % (result, arg1)
            elif op == "longjmp":
                line += "longjmp(%s, %s);" % (arg1, arg2)
            elif op == "store_env":
                line += self.store_env(arg1)
            elif op == "restore_env":
                line += self.restore_env(arg1, arg2)
            c_code += "\t%s: %s\n" % (self.make_label(i), line)
        c_code += "\t%s:;\n" % (self.make_label(noq))
        c_code += "}"
        print("TAC generated")
        return c_code

    def make_label(self, index):
        return "L" + str(index)