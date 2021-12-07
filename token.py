

class Token():
    def __init__(self, category, lexema, line, column):
        self.category = category
        self.lexema = lexema
        self.line = line
        self.column = column
