import enum_tokens

class WordDict:
    def __init__(self):
        self.words = {}

        enum_token = enum_tokens.Token()

        self.words["OPEN"] = enum_token.RW_OPEN
        self.words["CLOSE"] = enum_token.RW_CLOSE
        self.words["MAIN"] = enum_token.RW_MAIN
        self.words["AND"] = enum_token.OP_AND
        self.words["FUNCTION"] = enum_token.RW_FUNCTION
        self.words["OR"] = enum_token.OP_OR
        self.words["RETURN"] = enum_token.RW_RETURN
        self.words["EMPTY"] = enum_token.RW_EMPTY
        self.words["IF"] = enum_token.RW_IF
        self.words["ELSE"] = enum_token.RW_ELSE
        self.words["WHILE"] = enum_token.RW_WHILE
        self.words["FOR"] = enum_token.RW_FOR
        self.words["FLOAT"] = enum_token.RW_FLOAT
        self.words["INT"] = enum_token.RW_INT
        self.words["CHAR"] = enum_token.RW_CHAR
        self.words["STR"] = enum_token.RW_STR
        self.words["BOOL"] = enum_token.RW_BOOL
        self.words["SCAN"] = enum_token.RW_SCAN
        self.words["PRINT"] = enum_token.RW_PRINT
        self.words["PRINTNL"] = enum_token.RW_PRINTNL
        self.words["NULL"] = enum_token.RW_NULL
        self.words["TRUE"] = enum_token.RW_TRUE
        self.words["FALSE"] = enum_token.RW_FALSE


