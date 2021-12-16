from lexer import *

tk = Lexer("/home/hellena/Downloads/GitHub/Compiladores/src/code_examples/shellsort.lp")
string = ""

while not tk.is_EOF():
    currTk = tk.next_token()

    print(f"[{currTk.category.name}, {currTk.lexem}]")

