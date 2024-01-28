from parser import *
import sys
from semantic import *

try:
    sint = Parser(sys.argv[1])

    tree_root = sint.start()
    tree_root.print_tree()

    semantic = SemanticAnalyzer()
    semantic.analyze(tree_root)

    if sint.token.category != TokenEnums.EOF:
        raise Exception(f"ERRO SINTÁTICO na linha {sint.lexer.row - 1}: {sint.lexer.txtline}")

    print('Arquivo compilado com sucesso!')

except Exception as e:
    raise


