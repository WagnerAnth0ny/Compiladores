from parser import *
import sys

try:
    sint = Parser(sys.argv[1])

    if sint.token.category != TokenEnums.EOF:
        raise Exception(f"ERRO SINTÁTICO na linha {sint.lexer.row - 1}: {sint.lexer.txtline}")


except Exception as e:
    raise


