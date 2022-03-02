from re import T
from lexer import *
from enum_tokens import TokenEnums


class Parser:

    def __init__(self, file):
        self.counter = 0
        self.epsilon = 'ε'
        self.lexer = Lexer(file)
        self.token = None
        self.next_token()
        self.start()

    def next_token(self):
        self.token = self.lexer.next_token()

        if self.verify_category([TokenEnums.ER_UNK,TokenEnums.ER_ID,TokenEnums.ER_NUM,TokenEnums.ER_PR, TokenEnums.ER_CHAR]):
            raise Exception (f"ERRO LÉXICO: {self.token.category} na linha {self.lexer.row - 1} \n {self.lexer.txtline}")

    def verify_category(self, categories):
        return self.token.category in categories

    def print_production(self, left, right):
        print(f"          {left} = {right}")

    def start(self):

        if self.verify_category([TokenEnums.RW_INT, TokenEnums.RW_FLOAT, TokenEnums.RW_BOOL, TokenEnums.RW_CHAR, TokenEnums.RW_STR]):
            self.print_production("S", "DeclaracaoId S")
            self.func_DeclId()
            self.start()

        elif self.verify_category([TokenEnums.RW_FUNCTION]):
            self.print_production("S", "DeclaracaoFunção S")
            self.func_decl()
            self.start()

        else:
            self.print_production("S", self.epsilon)

    def func_DeclId(self):
        if self.verify_category(
                [TokenEnums.RW_INT, TokenEnums.RW_FLOAT, TokenEnums.RW_BOOL, TokenEnums.RW_CHAR, TokenEnums.RW_STR]):
            self.print_production("DeclaraçãoId", "FunctionType Id ';'")
            self.func_type()
            self.func_LId()

            if self.verify_category([TokenEnums.DEL_SEMI]):
                print(self.token.to_str())
                self.next_token()

    def func_type(self):
        if self.verify_category([TokenEnums.RW_INT]):
            self.print_production("Vartype", "Int")
            print(self.token.to_str())
            self.next_token()
        elif self.verify_category([TokenEnums.RW_EMPTY]):
            self.print_production("Vartype", "Empty")
            print(self.token.to_str())
            self.next_token()
        elif self.verify_category([TokenEnums.RW_FLOAT]):
            self.print_production("Vartype", "'Float'")
            print(self.token.to_str())
            self.next_token()
        elif self.verify_category([TokenEnums.RW_BOOL]):
            self.print_production("Vartype", "'Bool'")
            print(self.token.to_str())
            self.next_token()
        elif self.verify_category([TokenEnums.RW_CHAR]):
            self.print_production("Vartype", "'Char'")
            print(self.token.to_str())
            self.next_token()
        elif self.verify_category([TokenEnums.RW_STR]):
            self.print_production("Vartype", "'Str'")
            print(self.token.to_str())
            self.next_token()

    def func_LId(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("LId", "Id Atribuição Id_LL")
            self.func_Id()
            self.atr()
            self.func_id_LL()

    def func_id_LL(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("Id_LL", "',' Id Atribuição Id_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_Id()
            self.atr()
            self.func_id_LL()
        else:
            self.print_production("Id_LL", self.epsilon)

    def atr(self):
        if self.verify_category([TokenEnums.OP_ATR]):
            self.print_production("Atribuição", "'=' CE")
            print(self.token.to_str())
            self.next_token()
            self.func_CE()
        else:
            self.print_production("Atribuição", self.epsilon)

    def func_decl(self):
        if self.verify_category([TokenEnums.RW_FUNCTION]):
            self.print_production("DeclaracaoFunção", "'Function' FunctionType IdOuMain '(' DeclaraçãoConstante ')' Bloco")
            print(self.token.to_str())
            self.next_token()
            self.func_type()
            self.id_main()

            if self.verify_category([TokenEnums.DEL_OPENP]):
                print(self.token.to_str())
                self.next_token()
                self.func_decl_cte()

                if self.verify_category([TokenEnums.DEL_CLOSEP]):
                    print(self.token.to_str())
                    self.next_token()
                    self.block()

    def id_main(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("IdOuMain", "'id'")
            print(self.token.to_str())
            self.next_token()
        elif self.verify_category([TokenEnums.RW_MAIN]):
            self.print_production("IdOuMain", "'Main'")
            print(self.token.to_str())
            self.next_token()

    def func_param(self):
        if self.verify_category(
                [TokenEnums.ID, TokenEnums.DEL_OPENP, TokenEnums.OP_SUB, TokenEnums.RW_BOOL, TokenEnums.CTE_CHAR,
                 TokenEnums.CTE_FLOAT, TokenEnums.CTE_INT, TokenEnums.CTE_STR]):
            self.print_production("ParâmetrosFunção", "CE ParâmetrosFunção_LL")
            print(self.token.to_str())
            self.func_CE()
            self.func_param_LL()

        else:
            self.print_production("ParâmetrosFunção", self.epsilon)

    def func_param_LL(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("ParâmetrosFunção_LL", "',' CE ParâmetrosFunção_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_CE()
            self.func_param_LL()

        else:
            self.print_production("ParâmetrosFunção_LL", self.epsilon)

    def func_decl_cte(self):
        if self.verify_category(
                [TokenEnums.RW_BOOL, TokenEnums.RW_CHAR, TokenEnums.RW_FLOAT, TokenEnums.RW_INT, TokenEnums.RW_STR]):
            self.print_production("DeclaraçãoConstante", "Vartype 'id'  Vector DeclaraçãoConstante_LL")
            self.func_type()
            if self.verify_category([TokenEnums.ID]):
                print(self.token.to_str())
                self.next_token()
                self.vetTipo()
                self.func_decl_cte_LL()
        else:
            self.print_production("DeclaraçãoConstante", self.epsilon)

    def func_decl_cte_LL(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("DeclaraçãoConstante_LL", "',' Tipo 'id'  Vector DeclaraçãoConstante_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_type()

            if self.verify_category([TokenEnums.ID]):
                print(self.token.to_str())
                self.next_token()
                self.vetTipo()
                self.func_decl_cte_LL()

    def vetTipo(self):
        if self.verify_category([TokenEnums.DEL_OPENBRA]):
            self.print_production("VetTipo", "'[' AE ']'")
            print(self.token.to_str())
            self.next_token()
            self.func_AE()

            if self.verify_category([TokenEnums.DEL_ENDBRA]):
                print(self.token.to_str())
                self.next_token()

        else:
            self.print_production("VetTipo", self.epsilon)

    def block(self):
        if self.verify_category([TokenEnums.RW_OPEN]):
            self.counter += 1
            self.print_production("Bloco", "'{' Instrução '}'")
            print(self.token.to_str())
            self.next_token()
            self.instruct()

            if self.verify_category([TokenEnums.RW_CLOSE]):
                print(self.token.to_str())
                self.next_token()
                self.counter -= 1

    def instruct(self):
        if self.verify_category(
                [TokenEnums.RW_BOOL, TokenEnums.RW_CHAR, TokenEnums.RW_FLOAT, TokenEnums.RW_INT, TokenEnums.RW_STR]):
            self.print_production("Instrução", "DeclaraçãoId Instrução")
            self.func_DeclId()
            self.instruct()

        elif self.verify_category(
                [TokenEnums.RW_PRINT, TokenEnums.RW_PRINTNL, TokenEnums.RW_SCAN, TokenEnums.RW_WHILE, TokenEnums.RW_FOR,
                 TokenEnums.RW_IF]):
            print(self.token.lexem)
            self.print_production("Instrução", "Cmd Instrução")
            self.cmd()
            self.instruct()

        elif self.verify_category([TokenEnums.ID]):
            self.print_production("Instrução", "Instrução_LL ';' Instrução")
            self.instruct_LL()

            if self.verify_category([TokenEnums.DEL_SEMI]):
                print(self.token.to_str())
                self.next_token()

            self.instruct()

        elif self.verify_category([TokenEnums.RW_BACK]):
            self.print_production("Instrução", "'Back' Back ';'")
            print(self.token.to_str())
            self.next_token()
            self.back()

            if self.verify_category([TokenEnums.DEL_SEMI]):
                print(self.token.to_str())
                self.next_token()

        else:
            self.print_production("Instrução", self.epsilon)

    def instruct_LL(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("Instrução_LL", "'id' ParamAtr")
            print(self.token.to_str())
            self.next_token()
            self.fParamAtr()

    def fParamAtr(self):
        if self.verify_category([TokenEnums.DEL_OPENP]):
            self.print_production("ParamAtr", "'(' ParâmetrosFunção ')'")
            print(self.token.to_str())
            self.next_token()
            self.func_param()

            if self.verify_category([TokenEnums.DEL_CLOSEP]):
                print(self.token.to_str())
                self.next_token()

        elif self.verify_category([TokenEnums.OP_ATR]):
            self.print_production("ParamAtr", "'=' CE lAtr")
            print(self.token.to_str())
            self.next_token()
            self.func_CE()
            self.lAtr()

        elif self.verify_category([TokenEnums.DEL_OPENBRA]):
            self.print_production("ParamAtr", "'[' AE ']' '=' CE lAtr")
            print(self.token.to_str())
            self.next_token()
            self.func_AE()

            if self.verify_category([TokenEnums.DEL_ENDBRA]):
                print(self.token.to_str())
                self.next_token()

                if self.verify_category([TokenEnums.OP_ATR]):
                    print(self.token.to_str())
                    self.next_token()
                    self.func_CE()
                    self.lAtr()

    def lAtr(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("lAtr", "',' Id '=' CE lAtr")
            print(self.token.to_str())
            self.next_token()
            self.func_Id()

            if self.verify_category([TokenEnums.OP_ATR]):
                print(self.token.to_str())
                self.next_token()
                self.func_CE()
                self.lAtr()
        else:
            self.print_production("lAtr", self.epsilon)


    def func_Id(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("Id", "'id' ArrayOpt")
            print(self.token.to_str())
            self.next_token()
            self.vetTipo()

    def back(self):
        if self.verify_category([TokenEnums.DEL_OPENP, TokenEnums.OP_SUB, TokenEnums.CTE_INT, TokenEnums.RW_BOOL,
                                 TokenEnums.CTE_CHAR, TokenEnums.CTE_FLOAT, TokenEnums.CTE_STR, TokenEnums.ID]):
            self.print_production("Back", "CE")
            self.func_CE()
        else:
            self.print_production("Back", self.epsilon)

    def cmd(self):
        if self.verify_category([TokenEnums.RW_PRINT, TokenEnums.RW_PRINTNL]):
            self.print_production("Cmd", "'Print' '(' 'CTE_STR' PrintParâmetros ')' ';'")
            print(self.token.to_str())
            self.next_token()

            if self.verify_category([TokenEnums.DEL_OPENP]):
                print(self.token.to_str())
                self.next_token()

                if self.verify_category([TokenEnums.CTE_STR, TokenEnums.ID]):
                    print(self.token.to_str())
                    self.next_token()
                    self.func_print_param()

                    if self.verify_category([TokenEnums.DEL_CLOSEP]):
                        print(self.token.to_str())
                        self.next_token()

                        if self.verify_category([TokenEnums.DEL_SEMI]):
                            print(self.token.to_str())
                            self.next_token()

        elif self.verify_category([TokenEnums.RW_SCAN]):
            self.print_production("Cmd", "'Scan' '('  Scan ')' ';'")
            print(self.token.to_str())
            self.next_token()

            if self.verify_category([TokenEnums.DEL_OPENP]):
                print(self.token.to_str())
                self.next_token()
                self.func_scan_param()
                if self.verify_category([TokenEnums.DEL_CLOSEP]):
                    print(self.token.to_str())
                    self.next_token()
                    if self.verify_category([TokenEnums.DEL_SEMI]):
                        print(self.token.to_str())
                        self.next_token()

        elif self.verify_category([TokenEnums.RW_WHILE]):
            self.print_production("Cmd", "'CmdWhile' '(' BE ')' Bloco")
            print(self.token.to_str())
            self.next_token()

            if self.verify_category([TokenEnums.DEL_OPENP]):
                print(self.token.to_str())
                self.next_token()
                self.func_BE()

                if self.verify_category([TokenEnums.DEL_CLOSEP]):
                    print(self.token.to_str())
                    self.next_token()
                    self.block()

        elif self.verify_category([TokenEnums.RW_FOR]):
           # selff.print_production("Cmd", "'CmdFor' other")
            print(self.token.to_str())
            self.next_token()
            self.cmd_for()

        elif self.verify_category([TokenEnums.RW_IF]):
            self.print_production("Cmd", "'CmdIf' '(' BE ')' Bloco CmdIf_LL")
            print(self.token.to_str())
            self.next_token()

            if self.verify_category([TokenEnums.DEL_OPENP]):
                print(self.token.to_str())
                self.next_token()
                self.func_BE()

                if self.verify_category([TokenEnums.DEL_CLOSEP]):
                    print(self.token.to_str())
                    self.next_token()
                    self.block()
                    self.func_if_LL()

    def func_print_param(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("PrintParâmetros", "',' CE PrintParâmetros")
            print(self.token.to_str())
            self.next_token()
            self.func_CE()
            self.func_print_param()

        else:
            self.print_production("PrintParâmetros", self.epsilon)

    def func_scan_param(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("Scan", "'id'  Vector Scan_LL")
            print(self.token.to_str())
            self.next_token()
            self.vetTipo()
            self.func_scan_param_LL()

    def func_scan_param_LL(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("Scan_LL", "',' 'id'  Vector Scan_LL")
            print(self.token.to_str())
            self.next_token()

            if self.verify_category([TokenEnums.ID]):
                print(self.token.to_str())
                self.next_token()
                self.vetTipo()
                self.func_scan_param_LL()

        else:
            self.print_production("Scan_LL", self.epsilon)

    def cmd_for(self):
        if self.verify_category([TokenEnums.DEL_OPENP]):
            self.print_production("For", "'(' 'Int' 'id' '='  AE ',' AE ForStep')' Bloco")
            print(self.token.to_str())
            self.next_token()

            if self.verify_category([TokenEnums.RW_INT]):
                print(self.token.to_str())
                self.next_token()

                if self.verify_category([TokenEnums.ID]):
                    print(self.token.to_str())
                    self.next_token()

                    if self.verify_category([TokenEnums.OP_ATR]):
                        print(self.token.to_str())
                        self.next_token()
                        self.func_AE()

                        if self.verify_category([TokenEnums.DEL_COMMA]):
                            print(self.token.to_str())
                            self.next_token()
                            self.func_AE()
                            self.fstep()

                            if self.verify_category([TokenEnums.DEL_CLOSEP]):
                                print(self.token.to_str())
                                self.next_token()
                                self.block()

    def fstep(self):
        if self.verify_category([TokenEnums.DEL_COMMA]):
            self.print_production("ForStep", "',' AE")
            print(self.token.to_str())
            self.next_token()
            self.func_AE()

        else:
            self.print_production("ForStep", self.epsilon)

    def func_if_LL(self):
        if self.verify_category([TokenEnums.RW_ELSE]):
            self.print_production("CmdIf_LL", "'RW_ELSE' Instrução")
            print(self.token.to_str())
            self.next_token()
            self.block()

        else:
            self.print_production("CmdIf_LL", self.epsilon)

    def func_CE(self):
        self.print_production("CE", "CF CE")
        self.func_BE()
        self.func_CE_LL()

    def func_BE(self):
        self.print_production("BE", "BT BE")
        self.func_BT()
        self.func_BE_LL()

    def func_CE_LL(self):
        if self.verify_category([TokenEnums.OP_CONCAT]):
            self.print_production("CE_LL", "'OP_CONCAT' CF CE_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_BE()
            self.func_CE_LL()
        else:
            self.print_production("CE_LL", self.epsilon)

    def func_BE_LL(self):
        if self.verify_category([TokenEnums.OP_OR]):
            self.print_production("BE_LL", "'OP_OR' BT BE_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_BT()
            self.func_BE_LL()
        else:
            self.print_production("BE_LL", self.epsilon)

    def func_BT(self):
        self.print_production("BT", "BF BT_LL")
        self.func_BF()
        self.func_BT_LL()

    def func_BT_LL(self):
        if self.verify_category([TokenEnums.OP_AND]):
            self.print_production("BT_LL", "'OP_AND' BF BT_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_BF()
            self.func_BT_LL()
        else:
            self.print_production("BT_LL", self.epsilon)

    def func_BF(self):
        if self.verify_category([TokenEnums.OP_NOT]):
            self.print_production("BF", "'OP_NOT' BF")
            print(self.token.to_str())
            self.next_token()
            self.func_BF()

        elif self.verify_category([TokenEnums.DEL_OPENP, TokenEnums.OP_SUB, TokenEnums.CTE_INT, TokenEnums.RW_BOOL,
                                   TokenEnums.CTE_CHAR, TokenEnums.CTE_FLOAT, TokenEnums.CTE_STR, TokenEnums.ID]):
            self.print_production("BF", "AR BF_LL")
            self.func_AR()
            self.func_BF_LL()

    def func_BF_LL(self):
        if self.verify_category([TokenEnums.OP_GREATER]):
            self.print_production("BF_LL", "'OP_GREATER' AR BF_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_AR()
            self.func_BF_LL()

        elif self.verify_category([TokenEnums.OP_LESS]):
            self.print_production("BF_LL", "'OP_LESS' AR BF_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_AR()
            self.func_BF_LL()
        elif self.verify_category([TokenEnums.OP_EQUALG]):
            self.print_production("BF_LL", "'OP_EQUALG' AR BF_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_AR()
            self.func_BF_LL()
        elif self.verify_category([TokenEnums.OP_EQUALL]):
            self.print_production("BF_LL", "'OP_EQUALL' AR BF_LL")
            self.func_AR()
            self.func_BF_LL()
        else:
            self.print_production("BF_LL", self.epsilon)

    def func_AR(self):
        self.print_production("AR", "AT AR_LL")
        self.func_AE()
        self.func_AR_LL()

    def func_AR_LL(self):
        if self.verify_category([TokenEnums.OP_EQUALDIFF]):
            self.print_production("AR_LL", "'OP_EQUALDIFF' AE AR_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_AE()
            self.func_BF_LL()

        elif self.verify_category([TokenEnums.OP_NOT]):
            self.print_production("AR_LL", "'OP_NOT' AE AR_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_AE()
            self.func_AR_LL()

        else:
            self.print_production("AR_LL", self.epsilon)

    def func_AE(self):
        self.print_production("AE", "AT AE_LL")
        self.func_AT()
        self.func_AE_LL()

    def func_AE_LL(self):
        if self.verify_category([TokenEnums.OP_SUM]):
            self.print_production("AE_LL", "'OP_SUM' AT AE")
            print(self.token.to_str())
            self.next_token()
            self.func_AT()
            self.func_AE_LL()

        elif self.verify_category([TokenEnums.OP_SUB]):
            self.print_production("AE_LL", "'OP_SUB' AT AE_LL")
            print(self.token.to_str())
            self.next_token()
            self.func_AT()
            self.func_AE_LL()

        else:
            self.print_production("AE_LL", self.epsilon)

    def func_AT(self):
        self.print_production("AT", "AP AT_LL")
        self.fAP()
        self.func_AT_LL()

    def func_AT_LL(self):
        if self.verify_category([TokenEnums.OP_MUL]):
            self.print_production("AT_LL", "'OP_MUL' AP AT_LL")
            print(self.token.to_str())
            self.next_token()
            self.fAP()
            self.func_AT_LL()

        elif self.verify_category([TokenEnums.OP_DIV]):
            self.print_production("AT_LL", "'OP_DIV' AP AT_LL")
            print(self.token.to_str())
            self.next_token()
            self.fAP()
            self.func_AT_LL()

        else:
            self.print_production("AT_LL", self.epsilon)

    def fAP(self):
        self.print_production("AP", "AF AP_LL")
        self.fAF()
        self.AP_LL()

    def AP_LL(self):

        if self.verify_category([TokenEnums.OP_MOD]):
            self.print_production("AP_LL", "'OP_MOD' AF AP")
            print(self.token.to_str())
            self.next_token()
            self.fAF()
            self.AP_LL()

        else:
            self.print_production("AP_LL", self.epsilon)

    def fAF(self):
        if self.verify_category([TokenEnums.DEL_OPENP]):
            self.print_production("AF", "'(' CE ')'")
            print(self.token.to_str())
            self.next_token()
            self.func_CE()

            if self.verify_category([TokenEnums.DEL_CLOSEP]):
                print(self.token.to_str())
                self.next_token()


        elif self.verify_category([TokenEnums.OP_SUB]):
            self.print_production("AF", "'OP_SUB' AF")
            print(self.token.to_str())
            self.next_token()
            self.fAF()

        elif self.verify_category([TokenEnums.ID]):
            self.call()

        elif self.verify_category([TokenEnums.BOOL_VALUE]):
            self.print_production("AF", "'BOOL_VALUE'")
            print(self.token.to_str())
            self.next_token()

        elif self.verify_category([TokenEnums.CTE_CHAR]):
            self.print_production("AF", "'CTE_CHAR'")
            print(self.token.to_str())
            self.next_token()

        elif self.verify_category([TokenEnums.CTE_FLOAT]):
            self.print_production("AF", "'CTE_FLOAT'")
            print(self.token.to_str())
            self.next_token()

        elif self.verify_category([TokenEnums.CTE_INT]):
            self.print_production("AF", "'CTE_INT'")
            print(self.token.to_str())
            self.next_token()

        elif self.verify_category([TokenEnums.CTE_STR]):
            self.print_production("AF", "'CTE_STR'")
            print(self.token.to_str())
            self.next_token()

    def call(self):
        if self.verify_category([TokenEnums.ID]):
            self.print_production("IdChamadaFunção", "'id' IdChamadaFunção_LL")
            print(self.token.to_str())
            self.next_token()
            self.call_LL()

    def call_LL(self):
        if self.verify_category([TokenEnums.DEL_OPENP]):
            self.print_production("IdChamadaFunção_LL", "'(' ParâmetrosFunção ')'")
            print(self.token.to_str())
            self.next_token()
            self.func_param()

            if self.verify_category([TokenEnums.DEL_CLOSEP]):
                print(self.token.to_str())
                self.next_token()

        elif self.verify_category([TokenEnums.DEL_OPENBRA]):
            self.print_production("IdChamadaFunção_LL", "'[' AE']'")
            print(self.token.to_str())
            self.next_token()
            self.func_AE()

            if self.verify_category([TokenEnums.DEL_ENDBRA]):
                print(self.token.to_str())
                self.next_token()

        else:
            self.print_production("IdChamadaFunção_LL", self.epsilon)
