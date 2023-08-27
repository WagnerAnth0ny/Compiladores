from tk import *


class Functions:
    def __init__(self, name, rtype, params, declared):
        self.name = name
        self.rtype = rtype
        self.params = params
        self.declared_vars = declared


class SemanticAnalyzer:
    def __init__(self):
        self.declared_functions = {}
        self.declared_variables = {}
        self.found_variables = []
        self.found_vartype = None
        self.found_id = None
        self.found_function = False
        self.last_func_name = ''
        self.param = {}

    def analyze(self, syntax_node, level=0):
        if syntax_node:
            print(syntax_node.node_type)
            if syntax_node.node_type == 'Vartype':
                if syntax_node.children:
                    self.found_vartype = syntax_node.children[0].node_type
                    return
            if syntax_node.node_type == 'IdOuMain':
                if syntax_node.children:
                    for child in syntax_node.children:
                        if child and not isinstance(child.value, str):
                            if (self.analyze_fdeclaration_type(self.found_vartype) and
                                self.analyze_fdeclaration_id(child.value.lexeme)):
                                self.found_function = True
                                self.last_func_name = child.value.lexeme

            if self.found_function and syntax_node.node_type == 'DeclaraçãoConstante':
                if syntax_node.children:
                    ptype = ''
                    pname = ''
                    for child in syntax_node.children:
                        if child:
                            if child.node_type == 'Vartype':
                                ptype = child.children[0].node_type
                            if child.node_type == 'ID':
                                if child.value and not isinstance(child.value, str):
                                    pname = child.value.lexeme
                            self.param[pname] = ptype

            if syntax_node.node_type == 'Instrução':
                returned = None
                if syntax_node.children:
                    for child in syntax_node.children:
                        if child and child.node_type == 'Instrução':
                            if child.children[1].children:
                                if child.children[1].children[0].node_type == 'RW_BACK':
                                    returned = self.get_returned(child.children[1].children)

                                    if returned == 'RW_EMPTY':
                                        print(f'Semantic error: wrong return type {returned}' if returned != self.found_vartype else '')
                                        exit(-1)
                                    elif returned == 'CTE_STR' and self.found_vartype != 'RW_STR':
                                        print(f'Semantic error: wrong return type {returned} expected {self.found_vartype}')
                                        exit(-1)
                                    elif returned == 'CTE_INT' and self.found_vartype != 'RW_INT':
                                        print(
                                            f'Semantic error: wrong return type {returned} expected {self.found_vartype}')
                                        exit(-1)
                                    elif returned == 'CTE_CHAR' and self.found_vartype != 'RW_CHAR':
                                        print(f'Semantic error: wrong return type {returned} expected {self.found_vartype}')
                                        exit(-1)
                                    elif returned == 'CTE_FLOAT' and self.found_vartype != 'RW_FLOAT':
                                        print(f'Semantic error: wrong return type {returned} expected {self.found_vartype}')
                                        exit(-1)
                                    elif returned == 'CTE_BOOL' and self.found_vartype != 'RW_BOOL':
                                        print(f'Semantic error: wrong return type {returned} expected {self.found_vartype}')
                                        exit(-1)

                self.analyze_func(syntax_node, self.last_func_name, returned, self.found_vartype)

            for child in syntax_node.children:
                self.analyze(child, level + 1)

    def analyze_fdeclaration_type(self, func_type):
        if not self.verify_node_type(func_type, ['RW_INT', 'RW_EMPTY', 'RW_FLOAT', 'RW_BOOL', 'RW_STR', 'RW_CHAR']):
            print(f'Semantic error: Invalid type {func_type}.')
            exit(-1)
        return True

    def analyze_fdeclaration_id(self, fun_name):
        if fun_name in list(self.declared_functions.keys()):
            print(f'Semantic error: Function {fun_name} redeclared.')
            exit(-1)
        return True

    def analyze_func(self, syntax_node, func_name, returned, rtype):
        self.declared_variables = {}

        if not syntax_node or not self.found_function:
            return

        return_type = self.found_vartype
        params = self.param

        self.declared_functions[func_name] = Functions(func_name, return_type, params, self.declared_variables)

        if syntax_node.children:
            last_vartype = ''
            for child in syntax_node.children:
                if child.node_type == 'DeclaraçãoId':
                    if child.children:
                        for child2 in child.children:
                            if child2.node_type == 'Vartype':
                                if child2.children[0]:
                                    last_vartype = child2.children[0].node_type
                                    continue
                            if child2.node_type == 'LId':
                                if child2.children[0]:
                                    if child2.children[0].value:
                                        self.declared_variables[child2.children[0].value.lexeme] = last_vartype
                                        self.found_variables.append(child2.children[0].value.lexeme)

        #self.analyze_attribution(syntax_node)

        r = 0
        f = 0

        for v in self.found_variables:
            if v not in list(self.declared_variables.keys()):
                f += 1

            if returned in list(self.declared_variables.keys()):
                r += 1

                isEqual = self.declared_variables[returned] == rtype
                if not isEqual:
                    print(f'Semantic error: expected return {rtype}, got {self.declared_variables[returned]} instead.')
                    exit(-1)

            if self.declared_functions[func_name].params:
                if v not in list(self.declared_functions[func_name].params.keys()):
                    f += 1

                if returned in list(self.declared_functions[func_name].params.keys()):
                    r += 1

                    isEqual = self.declared_functions[func_name].params[returned] == rtype
                    if not isEqual:
                        print(f'Semantic error: expected return {rtype}, got {self.declared_variables[returned]} instead.')
                        exit(-1)

        if r <= 0:
            print(f'Semantic error: identifier {returned} given in return not found.')
            exit(-1)

        if f != 0:
            print(f'Semantic error: variable {v} out of scope or not declared in function.')
            exit(-1)

        self.found_function = False

    def function_exists(self, func_name):
        return func_name in list(self.declared_functions.keys())

    def analyze_return_statement(self, return_type, return_identifier_type):
        return return_type == return_identifier_type

    def verify_node_type(self, node_type, list_type):
        return node_type in list_type

    def get_returned(self, children):
        if children:
            for child in children:
                if isinstance(child.value, str):
                    return 'RW_EMPTY'
                if child.value:
                    if child.value.category.name == 'ID':
                        return child.value.lexeme
                    else:
                        return child.value.category.name


    def verify_declarations(self, children):
        if self.verify_node_type(children.node_type, ['RW_INT', 'RW_EMPTY', 'RW_FLOAT', 'RW_BOOL', 'RW_STR', 'RW_CHAR']):
            if children.children:
                if self.verify_node_type(children.children.node_type, ['ID']):
                    if children.children.children:
                        if self.verify_node_type(children.children.children.node_type, ['Atribuição']):
                            self.verify_attribution(children.children.value.lexeme, children.children.children)
                    if children.children.value.lexem not in list(self.declared_variables.keys()):
                        self.declared_variables[children.children.value.lexeme] = children.node_type
                    else:
                        print(f'Error: variable {children.children.value.lexeme} already declared.')
                        return
                else:
                    print(f'{children.node_type} declarator used but identifier not passed.')
                    return

                for child in children.children:
                    self.verify_declarations(child)

    def analyze_attribution(self, children):
        pass

    def verify_attribution(self, children, child):
        if child.children:
            return self.declared_variables[children] == self.declared_variables[child.children]
