from ast_tree import ASTNode


class SemanticAnalyzer:
    def __init__(self):
        self.errors = []
        self.symbol_table = {}
        self.current_scope = None
        self.used_vars = set()
        self.declared_vars = set()

    def analyze(self, ast, parser):
        self.errors = []
        self.symbol_table = parser.variables.copy()
        self.used_vars = parser.used_vars
        self.declared_vars = parser.declared_vars
        self.functions = parser.functions
        
        if ast is not None:
            self._check_semantics(ast)

        
        unused_vars = self.declared_vars - self.used_vars
        for var in unused_vars:
            self.errors.append(f"Aviso: Variável '{var}' declarada mas não utilizada")
           
        undeclared_vars = self.used_vars - self.declared_vars
        for var in undeclared_vars:
            if (var not in self.symbol_table and var not in self.functions):
                self.errors.append(f"Erro: Variável '{var}' utilizada mas não declarada")
            
        return self.errors

    def _check_semantics(self, ast_node):
        if ast_node is None:
            return None

        if ast_node.type == "Assign":
            var = ast_node.children[0]
            expr = ast_node.children[1]

            var_type = self.symbol_table.get(var.value)
            expr_type = self._check_semantics(expr)

            if var_type and expr_type and var_type != expr_type:
                self.errors.append(f"Erro semântico: tentativa de atribuir {expr_type} a variável '{var.value}' do tipo {var_type}")

            return var_type

        elif ast_node.type == "Variable":
            var_type = self.symbol_table.get(ast_node.value)
            return var_type

        elif ast_node.type == "Literal":
            val = ast_node.value
            if isinstance(val, int):
                return "integer"
            elif isinstance(val, float):
                return "real"
            elif val in ["true", "false"]:
                return "boolean"
            elif isinstance(val, str):
                return "string"

        elif ast_node.type in ["AddOp", "MulOp"]:
            left_type = self._check_semantics(ast_node.children[0])
            right_type = self._check_semantics(ast_node.children[1])

            if left_type != right_type:
                self.errors.append(f"Aviso : operação '{ast_node.value}' entre tipos incompatíveis: {left_type} e {right_type}")
                return None
            else:
                return left_type

        elif ast_node.type == "RelOp":
            left_type = self._check_semantics(ast_node.children[0])
            right_type = self._check_semantics(ast_node.children[1])

            if left_type != right_type:
                self.errors.append(f"Aviso : comparação entre tipos diferentes: {left_type} e {right_type}")

            return "boolean"

        elif ast_node.type in ["LogicalOp", "Not"]:
            for child in ast_node.children:
                child_type = self._check_semantics(child)
                if child_type != "boolean":
                    self.errors.append(f"Erro semântico: operação lógica esperava BOOLEAN mas recebeu {child_type}")
            return "boolean"

        elif ast_node.type == "Call":
            if ast_node.value not in self.symbol_table and ast_node.value not in self.functions:
                self.errors.append(f"Erro semântico: Função/procedure '{ast_node.value}' não declarada")
            return "integer"

        elif ast_node.type in ["Write", "Read"]:
            for child in ast_node.children:
                if child.type == "Variable" or child.type == "Call":
                    self._check_semantics(child)
                elif child.type == "Literal" and isinstance(child.value, str):
                    continue  
            return None

        elif ast_node.type == "ArrayAcess":
            array_var = ast_node.value
            index_expr = ast_node.children[0]

            var_info = self.symbol_table.get(array_var)

            if var_info is None:
                self.errors.append(f"Erro semântico: variável '{array_var}' não declarada")
                return None

            if isinstance(var_info, dict) and 'base_type' in var_info:
                base_type = var_info['base_type']
            elif var_info == "string":
                base_type = var_info
            else:
                self.errors.append(f"Erro semântico: tentativa de acesso à variável '{array_var}', não é array nem string")
                return None

            index_type = self._check_semantics(index_expr)
            if index_type != "integer":
                self.errors.append(f"Erro semântico: índice do array '{array_var}' deveria ser INTEGER mas foi {index_type}")

            return base_type

        else:
            for child in ast_node.children:
                if isinstance(child, ASTNode):
                    self._check_semantics(child)

        return None