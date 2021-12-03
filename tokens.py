from enum import Enum


class Token(Enum):
    
    # Identifiers

    ID = 1

    # Operations

    OP_SUM = 2
    OP_SUB = 3
    OP_DIV = 4
    OP_MUL = 5
    OP_GREATER = 6
    OP_LESS = 7
    OP_EQUAL = 8
    OP_EQUALG = 9
    OP_EQUALL = 10
    OP_AND = 11
    OP_OR = 12
    OP_NOT = 13
    OP_NOTUN = 14
    OP_ATR = 15
    OP_MOD = 16

    # Reserved words

    RW_FUNCTION = 17
    RW_RETURN = 18
    RW_WHILE = 19
    RW_FOR = 20
    RW_IF = 21
    RW_ELSE = 22
    RW_FLOAT = 23
    RW_INT = 24
    RW_CHAR = 25
    RW_STR = 26
    RW_BOOL = 28
    RW_TRUE = 29
    RW_FALSE = 30
    RW_NULL = 31
    RW_OPEN = 32
    RW_CLOSE = 33
    RW_SCAN = 34
    RW_PRINT = 35
    RW_PRINTNL = 36
    RW_MAIN = 37
    RW_EMPTY = 38
    BOOL_VALUE = 39
    CTE_INT = 40
    CTE_FLOAT = 41
    CTE_CHAR = 42
    CTE_STR = 43


    # Delimiters

    DEL_OPEN = 44
    DEL_CLOSE = 45
    DEL_OPENP = 46
    DEL_CLOSEP = 47
    DEL_ENDBRA = 48
    DEL_OPENBRA = 49
    DEL_COMMA = 50
    DEL_SEMI = 51

    # Errors

    ER_UNK= 52
    ER_ID = 53
    ER_NUM = 54
    ER_PR = 55
    ER_CHAR = 56

    # Others

    EOF = 57
    COMMENT = 58

