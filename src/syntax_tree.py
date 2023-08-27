class SyntaxNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.scope = None
        self.nparams = None
        self.children = []

    def add_children(self, child_node):
        self.children.append(child_node)

    def set_scope(self, scope):
        self.scope = scope

    def set_nparams(self, nparams):
        self.nparams = nparams

    def print_tree(self, level=0, parent=None):
        indent = "  " * level

        print(f'Level: {level}, Parent: {parent}' + indent + self.node_type)

        if self.value and not isinstance(self.value, str) and parent:
            print(f'Level: {level}, Parent: {parent}' + indent + self.node_type + ' ' + self.value.lexeme)
        else:
            print(f'Level: {level}, Parent: {parent}' + indent + self.node_type)

        for child in self.children:
            if child:
                child.print_tree(level + 1, self.node_type)
