
class Token():

    def __init__(self, category, lexem, row, col):

        self.category = category
        self.lexem = lexem
        self.row = row
        self.col = col

    def to_str(self):
        return f"              [{(self.row - 1):04d}, {(self.col):04d}] ({(self.category.value):04d}, {(self.category.name):>20}) {{{self.lexem}}}"
	