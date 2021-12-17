from lexer import *
import sys

string = ""

tk = Lexer(sys.argv[1])

while not tk.is_EOF():
    currTk = tk.next_token()

    print(currTk.to_str())
