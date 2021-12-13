from src.scanner.enum_tokens import *


class WordDict:
    def __init__(self):
        self.words = {"OPEN": TokenEnums.RW_OPEN, "CLOSE": TokenEnums.RW_CLOSE, "MAIN": TokenEnums.RW_MAIN,
                      "AND": TokenEnums.OP_AND, "FUNCTION": TokenEnums.RW_FUNCTION, "OR": TokenEnums.OP_OR,
                      "RETURN": TokenEnums.RW_RETURN, "EMPTY": TokenEnums.RW_EMPTY, "IF": TokenEnums.RW_IF,
                      "ELSE": TokenEnums.RW_ELSE, "WHILE": TokenEnums.RW_WHILE, "FOR": TokenEnums.RW_FOR,
                      "FLOAT": TokenEnums.RW_FLOAT, "INT": TokenEnums.RW_INT, "CHAR": TokenEnums.RW_CHAR,
                      "STR": TokenEnums.RW_STR, "BOOL": TokenEnums.RW_BOOL, "SCAN": TokenEnums.RW_SCAN,
                      "PRINT": TokenEnums.RW_PRINT, "PRINTNL": TokenEnums.RW_PRINTNL, "NULL": TokenEnums.RW_NULL,
                      "TRUE": TokenEnums.RW_TRUE, "FALSE": TokenEnums.RW_FALSE}
