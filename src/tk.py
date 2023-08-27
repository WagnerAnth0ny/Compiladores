
class Token:

    def __init__(self, category, lexeme, row, col):

        self.category = category
        self.lexeme = lexeme
        self.row = row
        self.col = col

    def to_str(self):
        return f"              [{(self.row - 1):04d}, {(self.col):04d}] ({(self.category.value):04d}, {(self.category.name):>20}) {{{self.lexeme}}}"
