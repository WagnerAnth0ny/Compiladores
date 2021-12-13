import traceback
import sys
from token import *
from enum_tokens import *


class Lexer():

    def __init__(self, file):
        try:

            self.pos = 0
            self.row = 1
            self.col = 1
            self.reader = open(file, 'rb')
            self.new_line()

            self.content = " "
            self.state = None

        except IOError as e:
            traceback.print_exc()

    @staticmethod
    def is_digit(string):
        return string.isdigit()

    @staticmethod
    def is_operator(string):

        return string in ['>', '<', '=', '!']

    @staticmethod
    def is_lower(string):
        return string.islower()

    @staticmethod
    def is_upper(string):
        return string.isupper()

    @staticmethod
    def is_blank(string):
        return string.isspace()

    @staticmethod
    def is_letter(string):
        return string.isalpha()

    @staticmethod
    def is_alphanum(string):
        return string.isalpha() or string.isdigit()

    def is_EOF(self):
        return self.pos == len(self.content)

    def next_token(self):
        self.state = 0
        lexem = ""

        while True:
            if self.is_EOF:
                if self.new_line():
                    data = self.content.split('')
                else:
                    return Token(TokenEnums.EOF, "EOF", self.row, self.col)

            currChar = self.next_char()

        if self.state == 0:

            if self.is_blank(currChar):
                lexem += currChar
                self.state = 0

            elif self.is_lower(currChar):
                lexem += currChar
                self.state = 1

            elif self.is_digit(currChar):
                lexem += currChar
                self.state = 3

            elif self.is_operator(currChar):
                lexem += currChar
                self.state = 7

            elif currChar == '\'':
                lexem += currChar
                self.state = 8

            elif self.is_upper(currChar):
                lexem += currChar
                self.state = 11

            elif currChar == '#':
                lexem += currChar
                self.state = 13

            elif currChar == '+':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.OP_SUM, lexem, self.row, self.col)

            elif currChar == '-':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.OP_SUB, lexem, self.row, self.col)

            elif currChar == '*':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.OP_MUL, lexem, self.row, self.col)

            elif currChar == '/':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.OP_DIV, lexem, self.row, self.col)

            elif currChar == '%':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.OP_MOD, lexem, self.row, self.col)

            elif currChar == '(':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.DEL_OPENP, lexem, self.row, self.col)

            elif currChar == ')':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.DEL_CLOSEP, lexem, self.row, self.col)

            elif currChar == '[':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.DEL_OPENBRA, lexem, self.row, self.col)

            elif currChar == ']':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.DEL_ENDBRA, lexem, self.row, self.col)

            elif currChar == ';':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.DEL_SEMI, lexem, self.row, self.col)

            elif currChar == ',':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.DEL_COMMA, lexem, self.row, self.col)

            elif currChar == '~':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.OP_NOTUN, lexem, self.row, self.col)

            elif currChar == '&':
                lexem += currChar
                self.col += 1
                return Token(TokenEnums.OP_CONCAT, lexem, self.row, self.col)

            else:
                Token(TokenEnums.ER_UNK, lexem, self.row, self.col)

        elif self.state == 1:
            if self.is_operator(currChar) or self.is_blank(currChar) or not self.is_alphanum(currChar):
                self.back()
                self.state = 2

            elif self.is_digit(currChar) or self.is_lower(currChar) or self.is_upper(currChar):
                lexem += currChar;

            else:
                self.col += 1
                Token(TokenEnums.ER_ID, lexem, self.row, self.col)

        elif self.state == 2:
            self.back()
            self.col += 1
            return Token(TokenEnums.ID, lexem, self.row, self.col)

        elif self.state == 3:
            if currChar == '.':
                lexem += currChar
                self.state = 4
                self.col = +1
            elif not self.is_alphanum(currChar):
                self.back()
                self.state = 5
            elif self.is_digit(currChar):
                lexem += currChar
            else:
                self.col += 1
                Token(TokenEnums.ER_NUM, lexem, self.row, self.col)

        elif self.state == 4:
            if self.is_digit(currChar):
                lexem += currChar

            elif self.is_operator(currChar) or self.is_blank(currChar) or not self.is_alphanum(currChar):
                self.back()
                self.state = 6

            else:
                self.col += 1
                Token(TokenEnums.ER_NUM, lexem, self.row, self.col)

        elif self.state == 5:
            self.back()
            self.col += 1
            return Token(TokenEnums.CTE_INT, lexem, self.row, self.col)

        elif self.state == 6:
            self.back()
            self.col += 1
            return Token(TokenEnums.CTE_FLOAT, lexem, self.row, self.col)

        elif self.state == 7:
            self.back()
            self.back()
            currChar = self.next_char()

            if currChar == '>':
                currChar = self.next_char()
                self.col += 1

                if currChar == '=':
                    lexem += currChar
                    return Token(TokenEnums.OP_EQUALG, lexem, self.row, self.col)
                else:
                    self.back()
                    return Token(TokenEnums.OP_GREATER, lexem, self.row, self.col)


            elif currChar == '<':
                currChar = self.next_char()
                self.col += 1

                if currChar == '=':
                    lexem += currChar
                    return Token(TokenEnums.OP_EQUALL, lexem, self.row, self.col)
                else:
                    self.back()
                    return Token(TokenEnums.OP_LESS, lexem, self.row, self.col)

            elif currChar == '!' or currChar == '=':
                currChar = self.next_char()
                self.col += 1

                if currChar == '=':
                    lexem += currChar
                    return Token(TokenEnums.OP_EQUALDIFF, lexem, self.row, self.col)
                else:
                    self.back()
                    return Token(TokenEnums.OP_NOT, lexem, self.row, self.col)

            else:
                Token(TokenEnums.ER_UNK, lexem, self.row, self.col)

        elif self.state == 8:
            if chr(32) <= currChar <= chr(126):
                lexem += currChar
                currChar = self.next_char()

                if currChar == '\'':
                    lexem += currChar
                    self.state = 9

                else:
                    self.back()
                    self.state = 10

            else:
                self.col += 1
                Token(TokenEnums.ER_CHAR, lexem, self.row, self.col)

        elif self.state == 9:
            self.back()
            self.col += 1
            return Token(TokenEnums.CTE_CHAR, lexem, self.row, self.col)

        # TODO
        elif self.state == 10:
            if currChar >= chr(32) and currChar <= chr(126):
                lexem += currChar

                if currChar == '\'':
                    self.col += 1
                    return Token(TokenEnums.CTE_STR, lexem, self.row, self.col)

            else:
                self.col += 1
                Token(TokenEnums.ER_CHAR, lexem, self.row, self.col)


        elif self.state == 11:
            if not (self.is_lower(currChar)) or self.is_blank(currChar):
                self.back()
                self.state = 12

            elif self.is_lower(currChar):
                lexem += currChar

        elif self.state == 12:
            self.back()
            self.col += 1
            # TODO
            # if hash

            # else:
            # return Token(TokenEnums.ER_PR, lexem, self.row,self.col)

        elif self.state == 13:
            if self.is_blank():
                self.state = 0

    def next_char(self):

        return self.content[self.pos + 1]

    def back(self):
        self.pos -= 1

    def new_line(self):

        tmp = " "

        try:
            tmp = self.reader.readline()

        except IOError as e:
            traceback.print_exc()

        if tmp is not None:
            line = tmp

            print(f"{self.row} {self.content}")

            line += " "
            self.row += 1
            pos = 0
            col = 0

            return True

        return False
