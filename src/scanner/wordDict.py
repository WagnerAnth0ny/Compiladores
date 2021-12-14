from enum_tokens import *


class WordDict:
    words = {"Open": TokenEnums.RW_OPEN, "Close": TokenEnums.RW_CLOSE, "Main": TokenEnums.RW_MAIN,
                      "AND": TokenEnums.OP_AND, "Function": TokenEnums.RW_FUNCTION, "OR": TokenEnums.OP_OR,
                      "RETURN": TokenEnums.RW_RETURN, "EMPTY": TokenEnums.RW_EMPTY, "IF": TokenEnums.RW_IF,
                      "ELSE": TokenEnums.RW_ELSE, "WHILE": TokenEnums.RW_WHILE, "FOR": TokenEnums.RW_FOR,
                      "FLOAT": TokenEnums.RW_FLOAT, "Int": TokenEnums.RW_INT, "CHAR": TokenEnums.RW_CHAR,
                      "STR": TokenEnums.RW_STR, "BOOL": TokenEnums.RW_BOOL, "SCAN": TokenEnums.RW_SCAN,
                      "Print": TokenEnums.RW_PRINT, "PRINTNL": TokenEnums.RW_PRINTNL, "NULL": TokenEnums.RW_NULL,
                      "TRUE": TokenEnums.RW_TRUE, "FALSE": TokenEnums.RW_FALSE}
