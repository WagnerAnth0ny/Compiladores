from lexer import *
from enum_tokens import TokenEnums
from syntax_tree import *


class Parser:

    def __init__(self, file):
        self.counter = 0
        self.epsilon = 'ε'
        self.lexer = Lexer(file)
        self.token = None
        self.next_token()
        self.current_scope = None

    def next_token(self):
        self.token = self.lexer.next_token()

        if self.verify_category([TokenEnums.ER_UNK,TokenEnums.ER_ID,TokenEnums.ER_NUM,TokenEnums.ER_PR, TokenEnums.ER_CHAR]):
            raise Exception (f"ERRO LÉXICO: {self.token.category} na linha {self.lexer.row - 1} \n {self.lexer.txtline}")

    def verify_category(self, categories):
        return self.token.category in categories

    def print_production(self, left, right):
        # print(f"          {left} = {right}")
        pass

    def start(self):
        if self.verify_category([TokenEnums.RW_INT, TokenEnums.RW_FLOAT, TokenEnums.RW_BOOL, TokenEnums.RW_CHAR, TokenEnums.RW_STR]):
            self.print_production("S", "DeclaracaoId S")

            syntax_node = SyntaxNode('DeclaracaoId', value=self.token)
            syntax_node.add_children(self.func_DeclId())
            syntax_node.add_children(self.start())

            return syntax_node

        elif self.verify_category([TokenEnums.RW_FUNCTION]):
            self.print_production("S", "DeclaracaoFunção S")

            syntax_node = SyntaxNode('DeclaracaoFunção')
            syntax_node.add_children(self.func_decl())
            syntax_node.add_children(self.start())

            return syntax_node

        else:
            self.print_production("S", self.epsilon)

            return SyntaxNode('S', self.epsilon)

    def func_DeclId(self):
        if self.verify_category(
                [TokenEnums.RW_INT, TokenEnums.RW_FLOAT, TokenEnums.RW_BOOL, TokenEnums.RW_CHAR, TokenEnums.RW_STR]):
            self.print_production("DeclaraçãoId", "FunctionType Id ';'")

            syntax_node = SyntaxNode('DeclaraçãoId', value=self.token)
            syntax_node.add_children(self.func_type())
            syntax_node.add_children(self.func_LId())

            if self.verify_category([TokenEnums.DEL_SEMI]):
                print(self.token.to_str())

                semicolon_node = SyntaxNode('DEL_SEMI', value=self.token)
                syntax_node.add_children(semicolon_node)
                self.next_token()
            else:
                print(f'Syntax error: ";" expected, line: {self.lexer.row}')
                exit(-1)

            return syntax_node

    def func_type(self):
        if self.verify_category([TokenEnums.RW_INT]):
            self.print_production("Vartype", "Int")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Vartype')
            int_node = SyntaxNode('RW_INT', value=self.token)
            syntax_node.add_children(int_node)

            self.next_token()

            return syntax_node

        elif self.verify_category([TokenEnums.RW_EMPTY]):
            self.print_production("Vartype", "Empty")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Vartype')
            empty_node = SyntaxNode('RW_EMPTY', value=self.token)
            syntax_node.add_children(empty_node)

            self.next_token()

            return syntax_node

        elif self.verify_category([TokenEnums.RW_FLOAT]):
            self.print_production("Vartype", "'Float'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Vartype')
            float_node = SyntaxNode('RW_FLOAT', value=self.token)
            syntax_node.add_children(float_node)

            self.next_token()

            return syntax_node

        elif self.verify_category([TokenEnums.RW_BOOL]):
            self.print_production("Vartype", "'Bool'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Vartype')
            bool_node = SyntaxNode('RW_BOOL', value=self.token)
            syntax_node.add_children(bool_node)

            self.next_token()

            return syntax_node

        elif self.verify_category([TokenEnums.RW_CHAR]):
            self.print_production("Vartype", "'Char'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Vartype')
            char_node = SyntaxNode('RW_CHAR', value=self.token)
            syntax_node.add_children(char_node)

            self.next_token()

            return syntax_node

        elif self.verify_category([TokenEnums.RW_STR]):
            self.print_production("Vartype", "'Str'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Vartype')
            string_node = SyntaxNode('RW_STR', value=self.token)
            syntax_node.add_children(string_node)

            self.next_token()

            return syntax_node
        else:
            print(f'Syntax error: type not defined. Line:{self.lexer.row}')
            exit(-1)

    def func_LId(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("LId", "Id Atribuição Id_LL")

            syntax_node = SyntaxNode('LId')

            syntax_node.add_children(self.func_Id())
            syntax_node.add_children(self.atr())
            syntax_node.add_children(self.func_id_LL())

            return syntax_node
        else:
            print(f'Syntax error: identifier expected, line: {self.lexer.row}')
            exit(-1)

    def func_id_LL(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("Id_LL", "',' Id Atribuição Id_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Id_LL')
            comma_node = SyntaxNode('DEL_COMMA', value=self.token)
            syntax_node.add_children(comma_node)

            self.next_token()

            syntax_node.add_children(self.func_Id())
            syntax_node.add_children(self.atr())
            syntax_node.add_children(self.func_id_LL())

            return syntax_node
        else:
            self.print_production("Id_LL", self.epsilon)


    def atr(self):
        if self.verify_category([TokenEnums.OP_ATR]):
            self.print_production("Atribuição", "'=' CE")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Atribuição')
            equal_node = SyntaxNode('OP_ATR', value=self.token)
            syntax_node.add_children(equal_node)

            self.next_token()

            syntax_node.add_children(self.func_CE())

            return syntax_node
        else:
            self.print_production("Atribuição", self.epsilon)

    def func_decl(self):
        if self.verify_category([TokenEnums.RW_FUNCTION]):
            self.print_production("DeclaracaoFunção", "'Function' FunctionType IdOuMain '(' DeclaraçãoConstante ')' Bloco")
            print(self.token.to_str())

            syntax_node = SyntaxNode('DeclaracaoFunção')
            function_node = SyntaxNode('RW_FUNCTION', value=self.token)
            syntax_node.add_children(function_node)

            self.next_token()

            syntax_node.add_children(self.func_type())
            syntax_node.add_children(self.id_main())

            if self.verify_category([TokenEnums.DEL_OPENP]):
                print(self.token.to_str())

                open_node = SyntaxNode('DEL_OPENP', value=self.token)
                syntax_node.add_children(open_node)

                self.next_token()
                syntax_node.add_children(self.func_decl_cte())

                if self.verify_category([TokenEnums.DEL_CLOSEP]):
                    print(self.token.to_str())

                    close_node = SyntaxNode('DEL_CLOSEP', value=self.token)
                    syntax_node.add_children(close_node)

                    self.next_token()
                    syntax_node.add_children(self.block())

                else:
                    print(f'Syntax error: expected ")", line: {self.lexer.row}')
                    exit(-1)

            else:
                print(f'Syntax error: expected "(", line: {self.lexer.row}')
                exit(-1)

            return syntax_node
        else:
            print(f'Syntax error: reserved word "Function" expected, line: {self.lexer.row}')
            exit(-1)

    def id_main(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("IdOuMain", "'id'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('IdOuMain')
            id_node = SyntaxNode('ID', value=self.token)
            id_node.set_scope(self.token.lexeme)
            syntax_node.add_children(id_node)

            self.next_token()

            return syntax_node

        elif self.verify_category([TokenEnums.RW_MAIN]):
            self.print_production("IdOuMain", "'Main'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('IdOuMain')
            main_node = SyntaxNode('RW_MAIN', value=self.token)
            main_node.set_scope(self.token.lexeme)
            syntax_node.add_children(main_node)

            self.next_token()

            return syntax_node
        else:
            print(f'Syntax error: Expected "Main" or identifier, line: {self.lexer.row}')
            exit(-1)

    def func_param(self):
        if self.verify_category(
                [TokenEnums.ID, TokenEnums.DEL_OPENP, TokenEnums.OP_SUB, TokenEnums.RW_BOOL, TokenEnums.CTE_CHAR,
                 TokenEnums.CTE_FLOAT, TokenEnums.CTE_INT, TokenEnums.CTE_STR]):
            self.print_production("ParâmetrosFunção", "CE ParâmetrosFunção_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('ParâmetrosFunção')

            syntax_node.add_children(self.func_CE())
            syntax_node.add_children(self.func_param_LL())

            return syntax_node
        else:
            self.print_production("ParâmetrosFunção", self.epsilon)

    def func_param_LL(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("ParâmetrosFunção_LL", "',' CE ParâmetrosFunção_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('ParâmetrosFunção_LL')

            comma_node = SyntaxNode('DEL_COMMA', value=self.token)
            syntax_node.add_children(comma_node)

            self.next_token()

            syntax_node.add_children(self.func_CE())
            syntax_node.add_children(self.func_param_LL())

            return syntax_node
        else:
            self.print_production("ParâmetrosFunção_LL", self.epsilon)

    def func_decl_cte(self):
        if self.verify_category(
                [TokenEnums.RW_BOOL, TokenEnums.RW_CHAR, TokenEnums.RW_FLOAT, TokenEnums.RW_INT, TokenEnums.RW_STR]):
            self.print_production("DeclaraçãoConstante", "Vartype 'id'  Vector DeclaraçãoConstante_LL")

            syntax_node = SyntaxNode('DeclaraçãoConstante')
            syntax_node.add_children(self.func_type())

            if self.verify_category([TokenEnums.ID]):
                print(self.token.to_str())

                id_node = SyntaxNode('ID', value=self.token)
                syntax_node.add_children(id_node)

                self.next_token()

                syntax_node.add_children(self.vetTipo())
                syntax_node.add_children(self.func_decl_cte_LL())

            else:
                print(f'Syntax error: identifier expected, line: {self.lexer.row}')
                exit(-1)

            return syntax_node
        else:
            self.print_production("DeclaraçãoConstante", self.epsilon)

    def func_decl_cte_LL(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("DeclaraçãoConstante_LL", "',' Tipo 'id'  Vector DeclaraçãoConstante_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('DeclaraçãoConstante_LL')

            comma_node = SyntaxNode('DEL_COMMA', value=self.token)
            syntax_node.add_children(comma_node)

            self.next_token()

            syntax_node.add_children(self.func_type())

            if self.verify_category([TokenEnums.ID]):
                print(self.token.to_str())
                id_node = SyntaxNode('ID', value=self.token)
                syntax_node.add_children(id_node)

                self.next_token()

                syntax_node.add_children(self.vetTipo())
                syntax_node.add_children(self.func_decl_cte_LL())

            else:
                print(f'Syntax error: expected identifier, line {self.lexer.row}')
                exit(-1)

            return syntax_node

    def vetTipo(self):
        if self.verify_category([TokenEnums.DEL_OPENBRA]):
            self.print_production("VetTipo", "'[' AE ']'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('VetTipo')

            open_bracket_node = SyntaxNode('DEL_OPENBRA', value=self.token)
            syntax_node.add_children(open_bracket_node)

            self.next_token()

            syntax_node.add_children(self.func_AE())

            if self.verify_category([TokenEnums.DEL_ENDBRA]):
                print(self.token.to_str())

                close_bracket_node = SyntaxNode('DEL_ENDBRA', value=self.token)
                syntax_node.add_children(close_bracket_node)

                self.next_token()

            else:
                print(f'Syntax error: expected "]", line: {self.lexer.row}')
                exit(-1)

            return syntax_node

        else:
            self.print_production("VetTipo", self.epsilon)

    def block(self):
        if self.verify_category([TokenEnums.RW_OPEN]):
            self.counter += 1
            self.print_production("Bloco", "'{' Instrução '}'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Bloco')

            open_block_node = SyntaxNode('RW_OPEN', value=self.token)
            syntax_node.add_children(open_block_node)

            self.next_token()

            syntax_node.add_children(self.instruct())

            if self.verify_category([TokenEnums.RW_CLOSE]):
                print(self.token.to_str())

                close_block_node = SyntaxNode('RW_CLOSE', value=self.token)
                syntax_node.add_children(close_block_node)

                self.next_token()
                self.counter -= 1
            else:
                print(f'Syntax error: expected "Close", line: {self.lexer.row}')
                exit(-1)

            return syntax_node
        else:
            print(f'Syntax error: expected "Open", line: {self.lexer.row}')
            exit(-1)

    def instruct(self):
        if self.verify_category(
                [TokenEnums.RW_BOOL, TokenEnums.RW_CHAR, TokenEnums.RW_FLOAT, TokenEnums.RW_INT, TokenEnums.RW_STR]):
            self.print_production("Instrução", "DeclaraçãoId Instrução")

            syntax_node = SyntaxNode('Instrução')

            syntax_node.add_children(self.func_DeclId())

            syntax_node.add_children(self.instruct())

            return syntax_node

        elif self.verify_category(
                [TokenEnums.RW_PRINT, TokenEnums.RW_PRINTNL, TokenEnums.RW_SCAN, TokenEnums.RW_WHILE, TokenEnums.RW_FOR,
                 TokenEnums.RW_IF]):
            print(self.token.lexeme)
            self.print_production("Instrução", "Cmd Instrução")

            syntax_node = SyntaxNode('Instrução')

            syntax_node.add_children(self.cmd())

            syntax_node.add_children(self.instruct())

            return syntax_node

        elif self.verify_category([TokenEnums.ID]):
            self.print_production("Instrução", "Instrução_LL ';' Instrução")

            syntax_node = SyntaxNode('Instrução')
            id_node = SyntaxNode('ID', self.token)
            syntax_node.add_children(id_node)

            syntax_node.add_children(self.instruct_LL())

            if self.verify_category([TokenEnums.DEL_SEMI]):
                print(self.token.to_str())

                semicolon_node = SyntaxNode('DEL_SEMI', value=self.token)
                syntax_node.add_children(semicolon_node)

                self.next_token()

            else:
                print(f'Syntax error: expected ";", line: {self.lexer.row}')
                exit(-1)

            syntax_node.add_children(self.instruct())

            return syntax_node

        elif self.verify_category([TokenEnums.RW_BACK]):
            self.print_production("Instrução", "'Back' Back ';'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Instrução')

            self.next_token()
            syntax_node.add_children(self.back())

            if self.verify_category([TokenEnums.DEL_SEMI]):
                print(self.token.to_str())

                semicolon_node = SyntaxNode('DEL_SEMI', value=self.token)
                syntax_node.add_children(semicolon_node)

                self.next_token()
            else:
                print(f'Syntax error: expected ";", line: {self.lexer.row}')
                exit(-1)

            return syntax_node

        else:
            self.print_production("Instrução", self.epsilon)

    def instruct_LL(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("Instrução_LL", "'id' ParamAtr")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Instrução_LL')

            self.next_token()

            syntax_node.add_children(self.fParamAtr())

            return syntax_node
        else:
            print(f'Syntax error: expected identifier, line: {self.lexer.row}')
            exit(-1)

    def fParamAtr(self):
        if self.verify_category([TokenEnums.DEL_OPENP]):
            self.print_production("ParamAtr", "'(' ParâmetrosFunção ')'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('ParamAtr')
            open_node = SyntaxNode('DEL_OPENP', value=self.token)
            syntax_node.add_children(open_node)

            self.next_token()

            syntax_node.add_children(self.func_param())

            if self.verify_category([TokenEnums.DEL_CLOSEP]):
                print(self.token.to_str())

                close_node = SyntaxNode('DEL_CLOSEP', value=self.token)
                syntax_node.add_children(close_node)

                self.next_token()
            else:
                print(f'Syntax error: expected ")", line: {self.lexer.row}')
                exit(-1)

            return syntax_node

        elif self.verify_category([TokenEnums.OP_ATR]):
            self.print_production("ParamAtr", "'=' CE lAtr")
            print(self.token.to_str())

            syntax_node = SyntaxNode('ParamAtr')
            atr_node = SyntaxNode('OP_ATR', value=self.token)
            syntax_node.add_children(atr_node)

            self.next_token()

            syntax_node.add_children(self.func_CE())
            syntax_node.add_children(self.lAtr())

            return syntax_node

        elif self.verify_category([TokenEnums.DEL_OPENBRA]):
            self.print_production("ParamAtr", "'[' AE ']' '=' CE lAtr")
            print(self.token.to_str())

            syntax_node = SyntaxNode('ParamAtr')
            open_bracket_node = SyntaxNode('DEL_OPENBRA', value=self.token)
            syntax_node.add_children(open_bracket_node)

            self.next_token()

            syntax_node.add_children(self.func_AE())

            if self.verify_category([TokenEnums.DEL_ENDBRA]):
                print(self.token.to_str())

                close_block_node = SyntaxNode('DEL_ENDBRA', value=self.token)
                syntax_node.add_children(close_block_node)

                self.next_token()

                if self.verify_category([TokenEnums.OP_ATR]):
                    print(self.token.to_str())
                    self.next_token()

                    atr_node = SyntaxNode('OP_ATR', value=self.token)
                    syntax_node.add_children(atr_node)

                    syntax_node.add_children(self.func_CE())
                    syntax_node.add_children(self.lAtr())
                else:
                    print(f'Syntax error: expected "=", line: {self.lexer.row}')
                    exit(-1)
            else:
                print(f'Syntax error: expected "]", line: {self.lexer.row}')
                exit(-1)

            return syntax_node

    def lAtr(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("lAtr", "',' Id '=' CE lAtr")
            print(self.token.to_str())

            syntax_node = SyntaxNode('lAtr')
            comma_node = SyntaxNode('DEL_COMMA', value=self.token)
            syntax_node.add_children(comma_node)

            self.next_token()

            syntax_node.add_children(self.func_Id())

            if self.verify_category([TokenEnums.OP_ATR]):
                print(self.token.to_str())
                self.next_token()

                atr_node = SyntaxNode('OP_ATR', value=self.token)
                syntax_node.add_children(atr_node)

                syntax_node.add_children(self.func_CE())
                syntax_node.add_children(self.lAtr())
            else:
                print(f'Syntax error: expected "=", line: {self.lexer.row}')
                exit(-1)

            return syntax_node
        else:
            self.print_production("lAtr", self.epsilon)

    def func_Id(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("Id", "'id' ArrayOpt")
            print(self.token.to_str())

            syntax_node = SyntaxNode('ID', value=self.token)

            self.next_token()

            syntax_node.add_children(self.vetTipo())

            return syntax_node
        else:
            print(f'Syntax error: expected identifier, line: {self.lexer.row}')
            exit(-1)

    def back(self):
        if self.verify_category([TokenEnums.DEL_OPENP, TokenEnums.OP_SUB, TokenEnums.CTE_INT, TokenEnums.RW_BOOL,
                                 TokenEnums.CTE_CHAR, TokenEnums.CTE_FLOAT, TokenEnums.CTE_STR, TokenEnums.ID]):
            self.print_production("Back", "CE")

            syntax_node = SyntaxNode('RW_BACK', value=self.token)

            syntax_node.add_children(self.func_CE())

            return syntax_node
        else:
            self.print_production("Back", self.epsilon)

            return SyntaxNode('RW_BACK', self.epsilon)

    def cmd(self):
        if self.verify_category([TokenEnums.RW_PRINT, TokenEnums.RW_PRINTNL]):
            self.print_production("Cmd", "'Print' '(' 'CTE_STR' PrintParâmetros ')' ';'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Cmd')
            print_node = SyntaxNode('RW_PRINT', value=self.token)
            syntax_node.add_children(print_node)

            self.next_token()

            if self.verify_category([TokenEnums.DEL_OPENP]):
                print(self.token.to_str())

                open_block_node = SyntaxNode('DEL_OPENP', value=self.token)
                syntax_node.add_children(open_block_node)

                self.next_token()

                if self.verify_category([TokenEnums.CTE_STR, TokenEnums.ID]):
                    print(self.token.to_str())

                    cte_str_node = SyntaxNode('CTE_STR', value=self.token)
                    syntax_node.add_children(cte_str_node)

                    self.next_token()

                    syntax_node.add_children(self.func_print_param())

                    if self.verify_category([TokenEnums.DEL_CLOSEP]):
                        print(self.token.to_str())

                        close_block_node = SyntaxNode('DEL_CLOSEP', value=self.token)
                        syntax_node.add_children(close_block_node)

                        self.next_token()

                        if self.verify_category([TokenEnums.DEL_SEMI]):
                            print(self.token.to_str())

                            semicolon_node = SyntaxNode('DEL_SEMI', value=self.token)
                            syntax_node.add_children(semicolon_node)

                            self.next_token()
                        else:
                            print(f'Syntax error: expected ";", line: {self.lexer.row}')
                            exit(-1)
                    else:
                        print(f'Syntax error: expected ")", line: {self.lexer.row}')
                        exit(-1)
                else:
                    print(f'Syntax error: expected "STR" or identifier, line: {self.lexer.row}')
                    exit(-1)
            else:
                print(f'Syntax error: expected "(", line: {self.lexer.row}')
                exit(-1)

            return syntax_node

        elif self.verify_category([TokenEnums.RW_SCAN]):
            self.print_production("Cmd", "'Scan' '('  Scan ')' ';'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Cmd')
            scan_node = SyntaxNode('RW_SCAN', value=self.token)
            syntax_node.add_children(scan_node)

            self.next_token()

            if self.verify_category([TokenEnums.DEL_OPENP]):
                print(self.token.to_str())

                open_block_node = SyntaxNode('DEL_OPENP', value=self.token)
                syntax_node.add_children(open_block_node)

                self.next_token()

                syntax_node.add_children(self.func_scan_param())
                if self.verify_category([TokenEnums.DEL_CLOSEP]):
                    print(self.token.to_str())

                    close_block_node = SyntaxNode('DEL_CLOSEP', value=self.token)
                    syntax_node.add_children(close_block_node)

                    self.next_token()
                    if self.verify_category([TokenEnums.DEL_SEMI]):
                        print(self.token.to_str())

                        semicolon_node = SyntaxNode('DEL_SEMI', value=self.token)
                        syntax_node.add_children(semicolon_node)

                        self.next_token()
                    else:
                        print(f'Syntax error: expected ";", line: {self.lexer.row}')
                        exit(-1)
                else:
                    print(f'Syntax error: expected ")", line: {self.lexer.row}')
                    exit(-1)
            else:
                print(f'Syntax error: expected "(", line: {self.lexer.row}')
                exit(-1)

        elif self.verify_category([TokenEnums.RW_WHILE]):
            self.print_production("Cmd", "'CmdWhile' '(' BE ')' Bloco")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Cmd')
            while_node = SyntaxNode('RW_WHILE', value=self.token)
            syntax_node.add_children(while_node)

            self.next_token()

            if self.verify_category([TokenEnums.DEL_OPENP]):
                print(self.token.to_str())

                open_block_node = SyntaxNode('DEL_OPENP', value=self.token)
                syntax_node.add_children(open_block_node)

                self.next_token()

                syntax_node.add_children(self.func_BE())

                if self.verify_category([TokenEnums.DEL_CLOSEP]):
                    print(self.token.to_str())

                    close_block_node = SyntaxNode('DEL_CLOSEP', value=self.token)
                    syntax_node.add_children(close_block_node)

                    self.next_token()

                    syntax_node.add_children(self.block())
                else:
                    print(f'Syntax error: expected ")", line: {self.lexer.row}')
                    exit(-1)
            else:
                print(f'Syntax error: expected "(", line: {self.lexer.row}')
                exit(-1)

            return syntax_node

        elif self.verify_category([TokenEnums.RW_FOR]):
            self.print_production("Cmd", "'CmdFor' other")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Cmd')
            for_node = SyntaxNode('RW_FOR', value=self.token)
            syntax_node.add_children(for_node)

            self.next_token()

            syntax_node.add_children(self.cmd_for())

            return syntax_node

        elif self.verify_category([TokenEnums.RW_IF]):
            self.print_production("Cmd", "'CmdIf' '(' BE ')' Bloco CmdIf_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Cmd')
            cmd_if_block = SyntaxNode('RW_IF', value=self.token)
            syntax_node.add_children(cmd_if_block)

            self.next_token()

            if self.verify_category([TokenEnums.DEL_OPENP]):
                print(self.token.to_str())

                open_block_node = SyntaxNode('DEL_OPENP', value=self.token)
                syntax_node.add_children(open_block_node)

                self.next_token()

                syntax_node.add_children(self.func_BE())

                if self.verify_category([TokenEnums.DEL_CLOSEP]):
                    print(self.token.to_str())

                    close_block_node = SyntaxNode('DEL_CLOSEP', value=self.token)
                    syntax_node.add_children(close_block_node)

                    self.next_token()

                    syntax_node.add_children(self.block())
                    syntax_node.add_children(self.func_if_LL())
                else:
                    print(f'Syntax error: expected ")", line: {self.lexer.row}')
                    exit(-1)
            else:
                print(f'Syntax error: expected "(", line: {self.lexer.row}')
                exit(-1)

            return syntax_node

    def func_print_param(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("PrintParâmetros", "',' CE PrintParâmetros")
            print(self.token.to_str())

            syntax_node = SyntaxNode('PrintParâmetros')
            comma_node = SyntaxNode('DEL_COMMA', value=self.token)
            syntax_node.add_children(comma_node)

            self.next_token()

            syntax_node.add_children(self.func_CE())
            syntax_node.add_children(self.func_print_param())

            return syntax_node

        else:
            self.print_production("PrintParâmetros", self.epsilon)


    def func_scan_param(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("Scan", "'id'  Vector Scan_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Scan')
            id_node = SyntaxNode('ID', value=self.token)
            syntax_node.add_children(id_node)

            self.next_token()

            syntax_node.add_children(self.vetTipo())
            syntax_node.add_children(self.func_scan_param_LL())

            return syntax_node
        else:
            print(f'Syntax error: expected identifier, line: {self.lexer.row}')
            exit(-1)

    def func_scan_param_LL(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("Scan_LL", "',' 'id'  Vector Scan_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('Scan_LL')
            comma_node = SyntaxNode('DEL_COMMA', value=self.token)
            syntax_node.add_children(comma_node)

            self.next_token()

            if self.verify_category([TokenEnums.ID]):
                print(self.token.to_str())

                id_node = SyntaxNode('ID', value=self.token)
                syntax_node.add_children(id_node)

                self.next_token()

                syntax_node.add_children(self.vetTipo())
                syntax_node.add_children(self.func_scan_param_LL())
            else:
                print(f'Syntax error: expected identifier, line: {self.lexer.row}')
                exit(-1)

            return syntax_node

        else:
            self.print_production("Scan_LL", self.epsilon)

    def cmd_for(self):
        if self.verify_category([TokenEnums.DEL_OPENP]):
            self.print_production("For", "'(' 'Int' 'id' '='  AE ',' AE ForStep')' Bloco")
            print(self.token.to_str())

            syntax_node = SyntaxNode('For')
            open_block_node = SyntaxNode('DEL_OPENP', value=self.token)
            syntax_node.add_children(open_block_node)

            self.next_token()

            if self.verify_category([TokenEnums.RW_INT]):
                print(self.token.to_str())

                int_node = SyntaxNode('RW_INT', value=self.token)
                syntax_node.add_children(int_node)

                self.next_token()

                if self.verify_category([TokenEnums.ID]):
                    print(self.token.to_str())

                    id_node = SyntaxNode('ID', value=self.token)
                    syntax_node.add_children(id_node)

                    self.next_token()

                    if self.verify_category([TokenEnums.OP_ATR]):
                        print(self.token.to_str())

                        atr_node = SyntaxNode('OP_ATR', value=self.token)
                        syntax_node.add_children(atr_node)

                        self.next_token()

                        syntax_node.add_children(self.func_AE())

                        if self.verify_category([TokenEnums.DEL_COMMA]):
                            print(self.token.to_str())

                            comma_node = SyntaxNode('DEL_COMMA', value=self.token)
                            syntax_node.add_children(comma_node)

                            self.next_token()

                            syntax_node.add_children(self.func_AE())
                            syntax_node.add_children(self.fstep())

                            if self.verify_category([TokenEnums.DEL_CLOSEP]):
                                print(self.token.to_str())

                                close_block_node = SyntaxNode('DEL_CLOSEP', value=self.token)
                                syntax_node.add_children(close_block_node)

                                self.next_token()

                                syntax_node.add_children(self.block())
                            else:
                                print(f'Syntax error: expected ")", line: {self.lexer.row}')
                                exit(-1)
                    else:
                        print(f'Syntax error: expected "=", line: {self.lexer.row}')
                        exit(-1)
                else:
                    print(f'Syntax error: expected identifier, line: {self.lexer.row}')
                    exit(-1)
            else:
                print(f'Syntax error: expected Int, line: {self.lexer.row}')
                exit(-1)

            return syntax_node
        else:
            print(f'Syntax error: expected "(", line: {self.lexer.row}')
            exit(-1)

    def fstep(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("ForStep", "',' AE")
            print(self.token.to_str())

            syntax_node = SyntaxNode('ForStep')
            comma_node = SyntaxNode('DEL_COMMA', value=self.token)
            syntax_node.add_children(comma_node)

            self.next_token()

            syntax_node.add_children(self.func_AE())

            return syntax_node

        else:
            self.print_production("ForStep", self.epsilon)

    def func_if_LL(self):
        if self.verify_category([TokenEnums.RW_ELSE]):
            self.print_production("CmdIf_LL", "'RW_ELSE' Instrução")
            print(self.token.to_str())

            syntax_node = SyntaxNode('CmdIf_LL')
            else_block = SyntaxNode('RW_ELSE', value=self.token)
            syntax_node.add_children(else_block)

            self.next_token()

            syntax_node.add_children(self.block())

            return syntax_node

        else:
            self.print_production("CmdIf_LL", self.epsilon)
            return SyntaxNode('CmdIf_LL', self.epsilon)

    def func_CE(self):
        self.print_production("CE", "CF CE")

        syntax_node = SyntaxNode('CE')
        cf_node = SyntaxNode('CF', value=self.token)
        syntax_node.add_children(cf_node)

        syntax_node.add_children(self.func_BE())
        syntax_node.add_children(self.func_CE_LL())

        return syntax_node

    def func_BE(self):
        self.print_production("BE", "BT BE")

        syntax_node = SyntaxNode('BE')
        be_node = SyntaxNode('BT', value=self.token)
        syntax_node.add_children(be_node)

        syntax_node.add_children(self.func_BT())
        syntax_node.add_children(self.func_BE_LL())

        return syntax_node

    def func_CE_LL(self):
        if self.verify_category([TokenEnums.OP_CONCAT]):
            self.print_production("CE_LL", "'OP_CONCAT' CF CE_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('CE_LL')
            op_concat_node = SyntaxNode('OP_CONCAT', value=self.token)
            syntax_node.add_children(op_concat_node)

            self.next_token()

            syntax_node.add_children(self.func_BE())
            syntax_node.add_children(self.func_CE_LL())

            return syntax_node

        else:
            self.print_production("CE_LL", self.epsilon)

    def func_BE_LL(self):
        if self.verify_category([TokenEnums.OP_OR]):
            self.print_production("BE_LL", "'OP_OR' BT BE_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('BE_LL')
            op_or = SyntaxNode('OP_OR', value=self.token)
            syntax_node.add_children(op_or)

            self.next_token()

            syntax_node.add_children(self.func_BT())
            syntax_node.add_children(self.func_BE_LL())

            return syntax_node

        else:
            self.print_production("BE_LL", self.epsilon)

    def func_BT(self):
        self.print_production("BT", "BF BT_LL")

        syntax_node = SyntaxNode('BT')
        bf_node = SyntaxNode('BF', value=self.token)
        syntax_node.add_children(bf_node)

        syntax_node.add_children(self.func_BF())
        syntax_node.add_children(self.func_BT_LL())

    def func_BT_LL(self):
        if self.verify_category([TokenEnums.OP_AND]):
            self.print_production("BT_LL", "'OP_AND' BF BT_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('BT_LL')
            op_and_node = SyntaxNode('OP_AND', value=self.token)
            syntax_node.add_children(op_and_node)

            self.next_token()

            syntax_node.add_children(self.func_BF())
            syntax_node.add_children(self.func_BT_LL())

            return syntax_node
        else:
            self.print_production("BT_LL", self.epsilon)

    def func_BF(self):
        if self.verify_category([TokenEnums.OP_NOT]):
            self.print_production("BF", "'OP_NOT' BF")
            print(self.token.to_str())

            syntax_node = SyntaxNode('BF')
            op_not_node = SyntaxNode('OP_NOT', value=self.token)
            syntax_node.add_children(op_not_node)

            self.next_token()

            syntax_node.add_children(self.func_BF())

            return syntax_node

        elif self.verify_category([TokenEnums.DEL_OPENP, TokenEnums.OP_SUB, TokenEnums.CTE_INT, TokenEnums.RW_BOOL,
                                   TokenEnums.CTE_CHAR, TokenEnums.CTE_FLOAT, TokenEnums.CTE_STR, TokenEnums.ID]):
            self.print_production("BF", "AR BF_LL")

            syntax_node = SyntaxNode('BF')
            ar_node = SyntaxNode('AR', value=self.token)
            syntax_node.add_children(ar_node)

            syntax_node.add_children(self.func_AR())
            syntax_node.add_children(self.func_BF_LL())

            return syntax_node

    def func_BF_LL(self):
        if self.verify_category([TokenEnums.OP_GREATER]):
            self.print_production("BF_LL", "'OP_GREATER' AR BF_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('BF_LL')
            op_greater_node = SyntaxNode('OP_GREATER', value=self.token)
            syntax_node.add_children(op_greater_node)

            self.next_token()

            syntax_node.add_children(self.func_AR())
            syntax_node.add_children(self.func_BF_LL())

            return syntax_node

        elif self.verify_category([TokenEnums.OP_LESS]):
            self.print_production("BF_LL", "'OP_LESS' AR BF_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('BF_LL')
            op_less_node = SyntaxNode('OP_LESS', value=self.token)
            syntax_node.add_children(op_less_node)

            self.next_token()

            syntax_node.add_children(self.func_AR())
            syntax_node.add_children(self.func_BF_LL())

            return syntax_node

        elif self.verify_category([TokenEnums.OP_EQUALG]):
            self.print_production("BF_LL", "'OP_EQUALG' AR BF_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('BF_LL')
            op_equal_node = SyntaxNode('OP_EQUALG', value=self.token)
            syntax_node.add_children(op_equal_node)

            self.next_token()

            syntax_node.add_children(self.func_AR())
            syntax_node.add_children(self.func_BF_LL())

            return syntax_node

        elif self.verify_category([TokenEnums.OP_EQUALL]):
            self.print_production("BF_LL", "'OP_EQUALL' AR BF_LL")

            syntax_node = SyntaxNode('BF_LL')
            op_equal_node = SyntaxNode('OP_EQUALL', value=self.token)
            syntax_node.add_children(op_equal_node)

            syntax_node.add_children(self.func_AR())
            syntax_node.add_children(self.func_BF_LL())

            return syntax_node
        else:
            self.print_production("BF_LL", self.epsilon)

    def func_AR(self):
        self.print_production("AR", "AT AR_LL")

        syntax_node = SyntaxNode('AR')
        at_node = SyntaxNode('AT', value=self.token)
        syntax_node.add_children(at_node)

        syntax_node.add_children(self.func_AE())
        syntax_node.add_children(self.func_AR_LL())

        return syntax_node

    def func_AR_LL(self):
        if self.verify_category([TokenEnums.OP_EQUALDIFF]):
            self.print_production("AR_LL", "'OP_EQUALDIFF' AE AR_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AR_LL')
            op_equal_diff_node = SyntaxNode('OP_EQUAL_DIFF', value=self.token)
            syntax_node.add_children(op_equal_diff_node)

            self.next_token()

            syntax_node.add_children(self.func_AE())
            syntax_node.add_children(self.func_BF_LL())

            return syntax_node

        elif self.verify_category([TokenEnums.OP_NOT]):
            self.print_production("AR_LL", "'OP_NOT' AE AR_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AR_LL')
            op_not_node = SyntaxNode('OP_NOT', value=self.token)
            syntax_node.add_children(op_not_node)

            self.next_token()

            syntax_node.add_children(self.func_AE())
            syntax_node.add_children(self.func_AR_LL())

            return syntax_node

        else:
            self.print_production("AR_LL", self.epsilon)

    def func_AE(self):
        self.print_production("AE", "AT AE_LL")

        syntax_node = SyntaxNode('AE')
        at_node = SyntaxNode('AT', value=self.token)
        syntax_node.add_children(at_node)

        syntax_node.add_children(self.func_AT())
        syntax_node.add_children(self.func_AE_LL())

        return syntax_node

    def func_AE_LL(self):
        if self.verify_category([TokenEnums.OP_SUM]):
            self.print_production("AE_LL", "'OP_SUM' AT AE")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AE_LL')
            op_sum_node = SyntaxNode('OP_SUM', value=self.token)
            syntax_node.add_children(op_sum_node)

            self.next_token()

            syntax_node.add_children(self.func_AT())
            syntax_node.add_children(self.func_AE_LL())

            return syntax_node

        elif self.verify_category([TokenEnums.OP_SUB]):
            self.print_production("AE_LL", "'OP_SUB' AT AE_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AE_LL')
            op_sub_node = SyntaxNode('OP_SUB', value=self.token)
            syntax_node.add_children(op_sub_node)

            self.next_token()

            syntax_node.add_children(self.func_AT())
            syntax_node.add_children(self.func_AE_LL())

            return syntax_node

        else:
            self.print_production("AE_LL", self.epsilon)

    def func_AT(self):
        self.print_production("AT", "AP AT_LL")

        syntax_node = SyntaxNode('AT')
        ap_node = SyntaxNode('AP', value=self.token)
        syntax_node.add_children(ap_node)

        syntax_node.add_children(self.fAP())
        syntax_node.add_children(self.func_AT_LL())

        return syntax_node

    def func_AT_LL(self):
        if self.verify_category([TokenEnums.OP_MUL]):
            self.print_production("AT_LL", "'OP_MUL' AP AT_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AT_LL')
            op_mul = SyntaxNode('OP_MUL', value=self.token)
            syntax_node.add_children(op_mul)

            self.next_token()

            syntax_node.add_children(self.fAP())
            syntax_node.add_children(self.func_AT_LL())

            return syntax_node

        elif self.verify_category([TokenEnums.OP_DIV]):
            self.print_production("AT_LL", "'OP_DIV' AP AT_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AT_LL')
            op_div_node = SyntaxNode('OP_DIV', value=self.token)
            syntax_node.add_children(op_div_node)

            self.next_token()

            syntax_node.add_children(self.fAP())
            syntax_node.add_children(self.func_AT_LL())

            return syntax_node

        else:
            self.print_production("AT_LL", self.epsilon)

    def fAP(self):
        self.print_production("AP", "AF AP_LL")

        syntax_node = SyntaxNode('AP')
        af_node = SyntaxNode('AF', value=self.token)
        syntax_node.add_children(af_node)

        syntax_node.add_children(self.fAF())
        syntax_node.add_children(self.AP_LL())

        return syntax_node

    def AP_LL(self):
        if self.verify_category([TokenEnums.OP_MOD]):
            self.print_production("AP_LL", "'OP_MOD' AF AP")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AP_LL')
            op_mod = SyntaxNode('OP_MOD', value=self.token)
            syntax_node.add_children(op_mod)

            self.next_token()

            syntax_node.add_children(self.fAF())
            syntax_node.add_children(self.AP_LL())

            return syntax_node

        else:
            self.print_production("AP_LL", self.epsilon)

    def fAF(self):
        if self.verify_category([TokenEnums.DEL_OPENP]):
            self.print_production("AF", "'(' CE ')'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AF')
            open_block_node = SyntaxNode('DEL_OPENP', value=self.token)
            syntax_node.add_children(open_block_node)

            self.next_token()

            syntax_node.add_children(self.func_CE())

            if self.verify_category([TokenEnums.DEL_CLOSEP]):
                print(self.token.to_str())

                close_block_node = SyntaxNode('DEL_CLOSEP', value=self.token)
                syntax_node.add_children(close_block_node)

                self.next_token()

            else:
                print(f'Syntax error: expected ")", line: {self.lexer.row}')
                exit(-1)

            return syntax_node

        elif self.verify_category([TokenEnums.OP_SUB]):
            self.print_production("AF", "'OP_SUB' AF")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AF')
            op_sub_node = SyntaxNode('OP_SUB', value=self.token)
            syntax_node.add_children(op_sub_node)

            self.next_token()
            syntax_node.add_children(self.fAF())

            return syntax_node

        elif self.verify_category([TokenEnums.ID]):
            syntax_node = SyntaxNode('id', value=self.token)

            syntax_node.add_children(self.call())

            return syntax_node

        elif self.verify_category([TokenEnums.BOOL_VALUE]):
            self.print_production("AF", "'BOOL_VALUE'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AF')
            bool_value_node = SyntaxNode('BOOL_VALUE', value=self.token)
            syntax_node.add_children(bool_value_node)

            self.next_token()

            return syntax_node

        elif self.verify_category([TokenEnums.CTE_CHAR]):
            self.print_production("AF", "'CTE_CHAR'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AF')
            cte_char_node = SyntaxNode('CTE_CHAR', value=self.token)
            syntax_node.add_children(cte_char_node)

            self.next_token()

            return syntax_node

        elif self.verify_category([TokenEnums.CTE_FLOAT]):
            self.print_production("AF", "'CTE_FLOAT'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AF')
            cte_float_node = SyntaxNode('CTE_FLOAT', value=self.token)
            syntax_node.add_children(cte_float_node)

            self.next_token()

            return syntax_node

        elif self.verify_category([TokenEnums.CTE_INT]):
            self.print_production("AF", "'CTE_INT'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AF')
            cte_int_node = SyntaxNode('CTE_INT', value=self.token)
            syntax_node.add_children(cte_int_node)

            self.next_token()

            return syntax_node

        elif self.verify_category([TokenEnums.CTE_STR]):
            self.print_production("AF", "'CTE_STR'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('AF')
            cte_str = SyntaxNode('CTE_STR', value=self.token)
            syntax_node.add_children(cte_str)

            self.next_token()

            return syntax_node

    def call(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("IdChamadaFunção", "'id' IdChamadaFunção_LL")
            print(self.token.to_str())

            syntax_node = SyntaxNode('IdChamadaFunção')
            id_node = SyntaxNode('ID', value=self.token)
            syntax_node.add_children(id_node)

            self.next_token()

            syntax_node.add_children(self.call_LL())

            return syntax_node
        else:
            print(f'Syntax error: expected identifier, line: {self.lexer.row}')
            exit(-1)

    def call_LL(self):
        if self.verify_category([TokenEnums.DEL_OPENP]):
            self.print_production("IdChamadaFunção_LL", "'(' ParâmetrosFunção ')'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('IdChamadaFunção_LL')
            open_block_node = SyntaxNode('DEL_OPENP', value=self.token)
            syntax_node.add_children(open_block_node)

            self.next_token()

            syntax_node.add_children(self.func_param())

            if self.verify_category([TokenEnums.DEL_CLOSEP]):
                print(self.token.to_str())

                close_block_node = SyntaxNode('DEL_CLOSEP', value=self.token)
                syntax_node.add_children(close_block_node)

                self.next_token()
            else:
                print(f'Syntax error: expected ")", line: {self.lexer.row}')
                exit(-1)

            return syntax_node

        elif self.verify_category([TokenEnums.DEL_OPENBRA]):
            self.print_production("IdChamadaFunção_LL", "'[' AE']'")
            print(self.token.to_str())

            syntax_node = SyntaxNode('IdChamadaFunção_LL')
            open_bracket_node = SyntaxNode('DEL_OPENBRA', value=self.token)
            syntax_node.add_children(open_bracket_node)

            self.next_token()

            syntax_node.add_children(self.func_AE())

            if self.verify_category([TokenEnums.DEL_ENDBRA]):
                print(self.token.to_str())

                close_bracket_node = SyntaxNode('DEL_ENDBRA', value=self.token)
                syntax_node.add_children(close_bracket_node)

                self.next_token()
            else:
                print(f'Syntax error: expected "]", line: {self.lexer.row}')
                exit(-1)

            return syntax_node

        else:
            self.print_production("IdChamadaFunção_LL", self.epsilon)
