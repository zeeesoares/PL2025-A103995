from ast_tree import ASTNode

class EWVMTranslator:
    def __init__(self, ast: ASTNode):
        self.ast = ast
        self.output = []
        self.label_counter = 0
        self.scope_stack = [{}]  # Pilha de escopos de variáveis: cada escopo é um dicionário
        self.functions = {}  # {name: (type, offset)}
        self.var_offset = 0
        self.isFunction = False
        self.current_scope = None
        self.function_output = []
        self.function_var_offset = 0


    def declare_variable(self, name, var_type, offset, array_size=None):
        current_scope = self.scope_stack[-1]
        if array_size is not None:
            current_scope[name] = (var_type, offset, array_size)
        else:
            current_scope[name] = (var_type, offset)

    def lookup_variable(self, name):
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        raise ValueError(f"Variável '{name}' não declarada")


    def translate(self) -> str:
        """Método principal que inicia a tradução"""
        self.ast.accept(self)
        return "\n".join(self.output + self.function_output)

    def visit_program(self, node: ASTNode):
        for child in node.children:
            child.accept(self)

    def visit_block(self, node: ASTNode):
        for child in node.children:
            if child.type in ["Declarations"]:
                child.accept(self)

        for child in node.children:
            if child.type == "Functions":
                child.accept(self)

        for child in node.children:
            if child.type == "Compound":
                child.accept(self)
    

    def visit_declarations(self, node: ASTNode):
        for decl in node.children:
            decl.accept(self)

    def visit_declist(self, node: ASTNode):
        for decl in node.children:
            decl.accept(self)

    def visit_declaration(self, node: ASTNode):
        var_type = node.children[1].value
        for id_node in node.children[0].children:
            var_name = id_node.value
            if var_type == "array":
                array_size = int(node.children[1].extra["upper_bound"]) - int(node.children[1].extra["lower_bound"]) + 1
                self.output.append(f"PUSHI {array_size}")
                self.output.append("ALLOCN")
                self.declare_variable(var_name, var_type, self.var_offset, array_size)
                self.var_offset += 1  
                if (self.isFunction):
                    self.function_var_offset += 1

            else:
                self.declare_variable(var_name, var_type, self.var_offset)
                self.output.append("PUSHI 0")
                self.var_offset += 1
                if (self.isFunction):
                    self.function_var_offset += 1

    def visit_functions(self, node: ASTNode):
        for func in node.children:
            func.accept(self)

    def visit_function(self, node: ASTNode):
        self.isFunction = True
        old_output = self.output
        self.output = []

        self.scope_stack.append({})  
        
        func_name = node.value
        self.functions[func_name] = (node.value, func_name)
        self.declare_variable(func_name, node.value, self.var_offset)
        self.var_offset += 1

        self.output.append("")
        self.output.append(f"{func_name}:")
        for child in node.children:
            child.accept(self)
        
        self.output.append(f"POP {self.function_var_offset}")
        self.function_var_offset = 0
        self.output.append("RETURN")

        self.scope_stack.pop()  

        self.function_output.extend(self.output)
        self.output = old_output
        self.isFunction = False

    def visit_parameters(self, node: ASTNode):
        for param in node.children:
            param.accept(self)

    def visit_parameter(self, node: ASTNode):
        id_list = node.children[0]  
        var_type = node.children[1].value  

        for id_node in id_list.children:
            var_name = id_node.value

            param_offset = -len(self.scope_stack[-1]) 

            self.declare_variable(var_name, var_type, self.var_offset)
            self.var_offset += 1
            self.function_var_offset += 1

            self.output.append("PUSHFP")
            self.output.append(f"LOAD {param_offset}")



    def visit_compound(self, node: ASTNode):
        if (not self.isFunction):
            self.output.append("START")
        for child in node.children:
            child.accept(self)

        if (not self.isFunction):
            self.output.append("STOP")

    def visit_compoundblock(self, node: ASTNode):
        for child in node.children:
            child.accept(self)

    def visit_statement_list(self, node: ASTNode):
        for stmt in node.children:
            stmt.accept(self)
    
    def visit_assign(self, node: ASTNode):
        var_node = node.children[0]
        expr = node.children[1]

        if var_node.type == "ArrayAcess":
            array_name = var_node.value
            index_node = var_node.children[0]

            expr.accept(self)

            index_node.accept(self)

            base_offset = self.lookup_variable(array_name)[1]
            self.output.append(f"PUSHG {base_offset}")
            self.output.append("LOADN")

            self.output.append("STOREN")

        else:
            expr.accept(self)
            var_name = var_node.value
            self.output.append(f"STOREG {self.lookup_variable(var_name)[1]}")

    def visit_variable(self, node: ASTNode):
        var_name = node.value
        
        if var_name in self.scope_stack[-1]:
            var_info = self.lookup_variable(var_name)
            if isinstance(var_info, tuple):
                self.output.append(f"PUSHG {var_info[1]}")
            else:
                raise ValueError(f"Acesso incorreto à variável ou array '{var_name}'")
        else:
            raise ValueError(f"Variável '{var_name}' não declarada")
        
    def visit_arrayacess(self, node: ASTNode):
        array_name = node.value
        index_node = node.children[0]
        
        if array_name in self.scope_stack[-1]:
            var_info = self.lookup_variable(array_name)
            
            if var_info[0] not in ["array", "string"]:
                raise ValueError(f"'{array_name}' não é um array ou string.")
            
            base_address_offset = var_info[1]  

            self.output.append(f"PUSHG {base_address_offset}") 
            index_node.accept(self) 
            self.output.append("PUSHI 1")  
            self.output.append("SUB")
            if var_info[0] == "string":
                self.output.append("CHARAT")  
            else:
                self.output.append("LOADN")  
        else:
            raise ValueError(f"Array ou string '{array_name}' não declarado.")

                
    def visit_write(self, node: ASTNode):
        for child in node.children:
            if child.type == "Variable":
                var_name = child.value
                if var_name in self.scope_stack[-1]:
                    var_type = self.lookup_variable(var_name)[0]
                    if var_type == "integer":
                        self.output.append(f"PUSHG {self.lookup_variable(var_name)[1]}\nWRITEI")
                    elif var_type == "real":
                        self.output.append(f"PUSHG {self.lookup_variable(var_name)[1]}\nWRITEF")
                    elif var_type == "string":
                        self.output.append(f"PUSHG {self.lookup_variable(var_name)[1]}\nWRITES")
                    elif var_type == "boolean":
                        self.output.append(f"PUSHG {self.lookup_variable(var_name)[1]}\nWRITEI")
                    else:
                        raise ValueError(f"Tipo de variável desconhecido: {var_type}")
                else:
                    raise ValueError(f"Variável '{var_name}' não declarada")
            elif child.type == "Literal":
                self.visit_literal(child)
                val = child.value
                if isinstance(val, int):
                    self.output.append("WRITEI")
                elif isinstance(val, float):
                    self.output.append("WRITEF")
                elif isinstance(val, str):
                    self.output.append("WRITES")
                elif val.lower() in ["true", "false"]:
                    self.output.append("WRITEI")
                else:
                    raise ValueError(f"Tipo de literal desconhecido: {val}")
            else:
                raise ValueError(f"Tipo de nó inesperado em write: {child.type}")


    def visit_read(self, node: ASTNode):
        for var in node.children:
            var_name = var.value
            
            if var_name in self.scope_stack[-1]:
                var_type = self.lookup_variable(var_name)[0]
                if var_type == "integer":
                    self.output.append(f"READ\nATOI\nSTOREG {self.lookup_variable(var_name)[1]}")
                elif var_type == "real":
                    self.output.append(f"READ\nATOF\nSTOREG {self.lookup_variable(var_name)[1]}")
                elif var_type == "string":
                    self.output.append(f"READ\nSTOREG {self.lookup_variable(var_name)[1]}")
                elif var_type == "array":
                    index_node = var.children[0]
                    base_offset = self.lookup_variable(var.value)[1]
                    self.output.append(f"PUSHG {base_offset}")
                    index_node.accept(self)  
                    self.output.append("PUSHI 1")
                    self.output.append("SUB")
                    self.output.append("READ")
                    self.output.append("ATOI")
                    self.output.append("STOREN")


                else:
                    raise ValueError(f"Tipo de variável desconhecido: {var_type}")
            
    def visit_ifelse(self, node: ASTNode):
        label_else = f"ELSE{self.label_counter}"
        label_end = f"ENDIF{self.label_counter}"
        self.label_counter += 1

        condition = node.children[0]
        then_branch = node.children[1]
        else_branch = node.children[2] if len(node.children) > 2 else None

        condition.accept(self)
        self.output.append(f"JZ {label_else}")
        
        then_branch.accept(self)
        self.output.append(f"JUMP {label_end}")

        self.output.append(f"{label_else}:")
        if else_branch:
            else_branch.accept(self)

        self.output.append(f"{label_end}:")

    
    def visit_while(self, node: ASTNode):
        label_start = f"WHILE{self.label_counter}"
        label_end = f"ENDWHILE{self.label_counter}"
        self.label_counter += 1
        self.output.append(f"{label_start}:")
        condition = node.children[0]
        body = node.children[1]
        condition.accept(self)
        self.output.append(f"JZ {label_end}")
        body.accept(self)
        self.output.append(f"JUMP {label_start}")
        self.output.append(f"{label_end}:")
        pass


    def visit_for(self, node: ASTNode):
        label_start = f"FOR{self.label_counter}"
        label_end = f"ENDFOR{self.label_counter}"
        self.label_counter += 1

        assign_node = node.children[0]  
        end_expr = node.children[1]
        body = node.children[2]
        direction = node.value 

        var_node = assign_node.children[0]
        start_expr = assign_node.children[1]

        var_name = var_node.value
        
        offset = self.lookup_variable(var_name)[1]

        start_expr.accept(self)
        self.output.append(f"STOREG {offset}")

        self.output.append(f"{label_start}:")

        self.output.append(f"PUSHG {offset}")  
        end_expr.accept(self)                  

        if direction == "TO":
            self.output.append("INFEQ")          
        else:
            self.output.append("SUPEQ")          

        self.output.append(f"JZ {label_end}")

        body.accept(self)

        self.output.append(f"PUSHG {offset}")
        self.output.append("PUSHI 1")
        if direction == "TO":
            self.output.append("ADD")
        else:
            self.output.append("SUB")
        self.output.append(f"STOREG {offset}")

        self.output.append(f"JUMP {label_start}")
        self.output.append(f"{label_end}:")

    def visit_repeat(self, node: ASTNode):
        label_start = f"REPEAT{self.label_counter}"
        label_end = f"ENDREPEAT{self.label_counter}"
        self.label_counter += 1

        self.output.append(f"{label_start}:")
        body = node.children[0]
        condition = node.children[1]

        body.accept(self)

        condition.accept(self)
        self.output.append(f"JZ {label_end}")
        self.output.append(f"JUMP {label_start}")
        self.output.append(f"{label_end}:")

    def visit_call(self, node: ASTNode):
        if node.value == "length":
            array_name = node.children[0].value
            if array_name in self.scope_stack[-1]:
                var_info = self.lookup_variable(array_name)
                
                if var_info[0] == "string":
                    self.output.append(f"PUSHG {var_info[1]}")  
                    self.output.append("STRLEN")  
                elif var_info[0] == "array":
                    self.output.append(f"PUSHG {var_info[1]}") 
                    self.output.append("PUSHI 0") 
                    self.output.append("LOADN") 
                else:
                    raise ValueError(f"Tipo de variável não reconhecido para 'length': {var_info[0]}")
            else:
                raise ValueError(f"Variável '{array_name}' não declarada.")
        else:
            func_name = node.value
            if func_name in self.functions:
                for arg in node.children:
                    arg.accept(self)  # Avalia e empilha os argumentos
                self.output.append(f"PUSHA {func_name}")
                self.output.append("CALL")
            else:
                raise ValueError(f"Função '{func_name}' não declarada.")

    def visit_not(self, node: ASTNode):
        node.children[0].accept(self)
        self.output.append("NOT")

    def visit_logicalop(self, node: ASTNode):
        left = node.children[0]
        right = node.children[1]
        op = node.value

        left.accept(self)
        right.accept(self)

        if op == "and":
            self.output.append("AND")
        elif op == "or":
            self.output.append("OR")
        else:
            raise ValueError(f"Operador lógico desconhecido: {op}")

    def visit_relop(self, node: ASTNode):
        left = node.children[0]
        right = node.children[1]
        op = node.value 

        left.accept(self)
        right.accept(self)

        if op == ">":
            self.output.append("SUP")
        elif op == "<":
            self.output.append("INF")
        elif op == "=":
            self.output.append("EQUAL")
        elif op == "<=":
            self.output.append("INFEQ")
        elif op == ">=":
            self.output.append("SUPEQ")
        elif op == "<>":
            self.output.append("NOTEQ")
        else:
            raise ValueError(f"Operador relacional desconhecido: {op}")


    def visit_addop(self, node: ASTNode):
        left = node.children[0]
        right = node.children[1]
        
        left.accept(self)
        right.accept(self)
        
        op = node.value
        if op == "+":
            self.output.append("ADD")
        elif op == "-":
            self.output.append("SUB")
        else:
            raise ValueError(f"Operador de adição/subtração desconhecido: {op}")


    def visit_mulop(self, node: ASTNode):
        left = node.children[0]
        right = node.children[1]
        
        left.accept(self)
        right.accept(self)
        
        op = node.value
        if op == "*":
            self.output.append("MUL")
        elif op == "/":
            self.output.append("DIV")
        elif op == "div":
            self.output.append("DIV")
        elif op == "mod":
            self.output.append("MOD")
        else:
            raise ValueError(f"Operador de multiplicação/divisão desconhecido: {op}")

    def visit_unary(self, node: ASTNode):
        pass

    def visit_literal(self, node: ASTNode):
        if node.value in ["true", "false"]:
            if node.value == "false":
                self.output.append("PUSHI 0")
            else:   
                self.output.append("PUSHI 1")
        elif isinstance(node.value, int):
            self.output.append(f"PUSHI {node.value}")
        elif isinstance(node.value, float):
            self.output.append(f"PUSHF {node.value}")
        elif isinstance(node.value, str):
            if len(node.value) == 3:
                self.output.append(f"PUSHI {ord(node.value[1])}")
            else :
                self.output.append(f'PUSHS "{node.value}"')
        else:
            raise ValueError(f"Tipo de literal desconhecido: {node.value}")
        

if __name__ == "__main__":
    from anasin import parse_pascal
    from sys import argv
    if len(argv) > 1:
        with open(argv[1], "r") as f:
            ast = parse_pascal(f.read())
            if ast:
                translator = EWVMTranslator(ast)
                generated_code = translator.translate()
                print(generated_code)
    else:
        print("Nenhum arquivo fornecido. Usando o arquivo de teste padrão.")
