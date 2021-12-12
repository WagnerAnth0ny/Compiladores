import traceback
import sys
from token import *

class Lexer():

    def __init__(self,file):
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
        return  string.isspace()

    def is_EOF(self):
        return self.pos == len(self.content)

    #TODO: Esse monstro
    def  next_token(self):
        self.state = 0

    def next_char(self):

        return self.content[self.pos + 1]

    def back(self):
        self.pos -=1

    def new_line(self):

        tmp = " "

        try:
            tmp = self.reader.readline()

        except IOError as e:
            traceback.print_exc()

        if tmp != None:
            line = tmp
            
            print(f"{self.row} {self.content}")

            line += " "
            self.row += 1
            pos = 0
            col = 0

            return True

        return False