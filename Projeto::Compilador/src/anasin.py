import sys
import ply.yacc as yacc
from analex import tokens, lexer
from ast_tree import ASTNode
from semantics import SemanticAnalyzer
from difflib import get_close_matches

class Parser:
    tokens = tokens  
    
    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()
        self.reset()
        self.parser = yacc.yacc(module=self)
        
    def reset(self):
        self.variables = {}
        self.errors = []
        self.used_vars = set()
        self.declared_vars = set()
        self.functions = {'length', 'write', 'writeln', 'read', 'readln'}
        self.current_function = None

    def parse(self, source_code):
        self.reset()
        ast = self.parser.parse(source_code, lexer=lexer)
        
        if self.errors:
            print(f"\nEncontrados {len(self.errors)} erros sintáticos:")
            for error in self.errors:
                print(f"- {error}")
            raise Exception("Erros sintáticos encontrados.")
        

        
        semantic_errors = self.semantic_analyzer.analyze(ast, self)
        
        if semantic_errors:
            print(f"\nEncontrados {len(semantic_errors)} erros semânticos:")
            for error in semantic_errors:
                print(f"- {error}")
            raise Exception("Erros semânticos encontrados.")
        
        return ast

    def p_program(self, p):
        """program : PROGRAM ID SEMI block DOT"""
        p[0] = ASTNode("Program", children=[p[4]], value=p[2])

    def p_block(self, p):
        """
        block : declaration_section func_section declaration_section compound_section
            | declaration_section compound_section
        """
        if len(p) == 5:
            p[0] = ASTNode("Block", children = [p[1],p[2],p[3],p[4]])
        else:
            p[0] = ASTNode("Block", children= [p[1],p[2]])

    def p_declaration_section(self, p):
        """
        declaration_section :
                            | VAR declaration_list
        """
        if len(p) == 1:
            p[0] = ASTNode("Declarations", children = [])
        else:
            p[0] = ASTNode("Declarations", children= [p[2]])

    def p_declaration_list(self, p):
        """
        declaration_list : declaration
                        | declaration_list declaration
        """
        if len(p) == 2:
            p[0] = ASTNode("DeclList", children=[p[1]])
        else:
            p[0] = ASTNode("DeclList", children=p[1].children + [p[2]])

    def p_declaration(self, p):
        """declaration : id_list COLON type SEMI"""
        p[0] = ASTNode("Declaration", children = [p[1], p[3]])

        var_type = p[3].value
        if var_type == "array":
            array_base_type = p[3].children[-1].value
            var_type = {'base_type': array_base_type}
        for id_node in p[1].children:
            self.variables[id_node.value] = var_type

    def p_id_list(self, p):
        """
        id_list : ID
                | id_list COMMA ID
        """
        if len(p) == 2:
            p[0] = ASTNode("IdList", children=[ASTNode("Id", value=p[1])])
            self.declared_vars.add(p[1])
        else:
            p[0] = ASTNode("IdList", children=p[1].children + [ASTNode("Id", value= p[3])])
            self.declared_vars.add(p[3])

    def p_type(self, p):
        """
        type : INTEGER
            | BOOLEAN
            | STRING
            | REAL
            | ARRAY LBRACK NUMBER DOTDOT NUMBER RBRACK OF type
        """
        if len(p) == 2:
            p[0] = ASTNode("Type", value = p[1].lower())
        else:
            p[0] = ASTNode(
                "Type", 
                value="array",
                children=[p[8]],  
                extra={
                    "lower_bound": p[3],
                    "upper_bound": p[5]
                }
            )


    def p_func_section(self, p):
        """
        func_section :
                    | func_section func_declaration
        """
        if len(p) == 1:
            p[0] = ASTNode("Functions", children=[])
        else:
            p[0] = ASTNode("Functions", children= p[1].children + [p[2]])

    def p_func_declaration(self, p):
        """
        func_declaration : FUNCTION ID LPAREN parameters RPAREN COLON type SEMI block SEMI
                        | PROCEDURE ID LPAREN parameters RPAREN SEMI block SEMI
        """
        if len(p) == 11:
            self.current_function = p[2]
            p[0] = ASTNode("Function", value = p[2], children= [p[4],p[7],p[9]])
            self.functions.add(p[2])
        
    def p_parameters(self, p):
        """
        parameters :
                | parameter_list
        """
        p[0] = ASTNode("Parameters", children=[] if len(p) == 1 else p[1].children)

    def p_parameter_list(self, p):
        """
        parameter_list : parameter
                    | parameter_list SEMI parameter
        """
        if len(p) == 2:
            p[0] = ASTNode("ParamList", children=[p[1]])
        else:
            p[0] = ASTNode("ParamList", children=p[1].children + [p[3]])

    def p_parameter(self, p):
        """parameter : id_list COLON type"""
        p[0] = ASTNode("Parameter", children=[p[1], p[3]])
        for id_node in p[1].children:
            self.variables[id_node.value] = p[3].value

    def p_compound_section(self, p):
        """compound_section : BEGIN statement_list END"""
        if p[1].upper() != "BEGIN":
            error_msg = (
                f"Erro de sintaxe na linha {p.lineno(1)}: Esperado 'BEGIN', mas encontrado '{p[1]}'."
            )
            self.errors.append(error_msg)

        if p[3].upper() != "END":
            error_msg = (
            f"Erro de sintaxe na linha {p.lineno(3)}: Esperado 'END', mas encontrado '{p[3]}'."
            )
            self.errors.append(error_msg)

        p[0] = ASTNode("Compound", children=[p[2]])

    def p_statement_list(self, p):
        """
        statement_list : statement
                    | statement_list SEMI statement
        """
        if len(p) == 2:
            p[0] = ASTNode("StatementList", children=[p[1]] if p[1] else [])
        else:
            p[0] = ASTNode("StatementList", children=p[1].children + ([p[3]] if p[3] else []))

    def p_statement(self, p):
        """
        statement : assign_statement
                | if_statement
                | while_statement
                | for_statement
                | repeat_statement
                | compound_section_block
                | function_call
                | write_statement
                | read_statement
                |
        """
        if len(p) == 1:
            p[0] = None
        else:
            p[0] = p[1]

    def p_compound_section_block(self, p):
        """compound_section_block : BEGIN statement_list END"""
        if p[1].upper() != "BEGIN":
            error_msg = (
                f"Erro de sintaxe na linha {p.lineno(1)}: Esperado 'BEGIN', mas encontrado '{p[1]}'."
            )
            self.errors.append(error_msg)

        if p[3].upper() != "END":
            error_msg = (
            f"Erro de sintaxe na linha {p.lineno(3)}: Esperado 'END', mas encontrado '{p[3]}'."
            )
            self.errors.append(error_msg)

        p[0] = ASTNode("CompoundBlock", children=[p[2]])

    def p_assign_statement(self, p):
        """assign_statement : variable ASSIGN expression
        """
        p[0] = ASTNode("Assign", children=[p[1],p[3]])

    def p_variable(self, p):
        """
        variable : ID
                | ID LBRACK expression RBRACK
        """
        if len(p) == 2:
            if self.current_function == p[1]:
                p[0] = ASTNode("Function_name", value= p[1])
            else: 
                p[0] = ASTNode("Variable",value= p[1])
                if p[1] not in self.used_vars:
                    self.used_vars.add(p[1])
        else:
            p[0] = ASTNode("ArrayAcess", children =[p[3]], value=p[1])
            if p[1] not in self.used_vars:
                self.used_vars.add(p[1])

    def p_if_statement(self, p):
        """
        if_statement : IF expression THEN statement
                    | IF expression THEN statement ELSE statement
        """
        if len(p) == 5:
            p[0] = ASTNode("IfElse", children=[p[2], p[4]])
        else:
            p[0] = ASTNode("IfElse", children=[p[2], p[4], p[6]])

    def p_while_statement(self, p):
        """while_statement : WHILE expression DO statement"""
        p[0] = ASTNode("While", children=[p[2], p[4]])

    def p_for_statement(self, p):
        """
        for_statement : FOR variable ASSIGN expression TO expression DO statement
                    | FOR variable ASSIGN expression DOWNTO expression DO statement
        """
        direction = "TO" if p[5].upper() == "TO" else "DOWNTO"
        p[0] = ASTNode("For", value=direction, children=[
            ASTNode("Assign", children=[p[2],p[4]]), p[6], p[8]
        ])

    def p_repeat_statement(self, p):
        """repeat_statement : REPEAT statement_list UNTIL expression"""
        p[0] = ASTNode("RepeatUntil", children=p[2] + [p[4]])

    def p_function_call(self, p):
        """function_call : ID LPAREN argument_list RPAREN"""
        p[0] = ASTNode("Call", value=p[1], children=p[3])

    def p_argument_list(self, p):
        """
        argument_list :
                    | expression
                    | argument_list COMMA expression
        """
        if len(p) == 1:
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_write_statement(self, p):
        """write_statement : write_func LPAREN output_list RPAREN"""
        p[0] = ASTNode("Write", value=p[1], children=p[3])

    def p_write_func(self, p):
        """
        write_func : WRITE
                | WRITELN
        """
        p[0] = p[1]

    def p_read_statement(self, p):
        """read_statement : read_func LPAREN variable_list RPAREN"""
        p[0] = ASTNode("Read",value = p[1], children = p[3])

    def p_read_func(self, p):
        """
        read_func : READ
                | READLN
        """
        p[0] = p[1]

    def p_output_list(self, p):
        """
        output_list : expression
                    | output_list COMMA expression
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_variable_list(self, p):
        """
        variable_list : variable
                    | variable_list COMMA variable
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expression(self, p):
        """expression : logical_expression"""
        p[0] = p[1]

    def p_logical_expression(self, p):
        """
        logical_expression : relational_expression
                        | logical_expression AND relational_expression
                        | logical_expression OR relational_expression
                        |  NOT relational_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        elif p[1] == "not":
            p[0] = ASTNode("Not", children=[p[2]])
        else:
            p[0] = ASTNode("LogicalOp", value=p[2], children=[p[1], p[3]])

    def p_relational_expression(self, p):
        """
        relational_expression : addition_expression
                            | addition_expression relop addition_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ASTNode("RelOp", value=p[2], children=[p[1], p[3]])

    def p_relop(self, p):
        """
        relop : EQ
            | NE
            | LT
            | LE
            | GT
            | GE
        """
        p[0] = p[1]

    def p_addition_expression(self, p):
        """
        addition_expression : mult_expression
                        | addition_expression addop mult_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ASTNode("AddOp", value=p[2], children=[p[1], p[3]])

    def p_addop(self, p):
        """
        addop : PLUS
            | MINUS
        """
        p[0] = p[1]

    def p_mult_expression(self, p):
        """
        mult_expression : unary_expression
                        | mult_expression mulop unary_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ASTNode("MulOp", value=p[2], children=[p[1], p[3]])

    def p_mulop(self, p):
        """
        mulop : TIMES
            | DIVIDE
            | DIV
            | MOD
        """
        p[0] = p[1]

    def p_unary_expression(self, p):
        """
        unary_expression : primary_expression
                        | sign unary_expression
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ASTNode("Unary",value = p[1],children=[p[2]])

    def p_sign(self, p):
        """
        sign : PLUS
            | MINUS
        """
        p[0] = p[1]

    def p_primary_expression(self, p):
        """
        primary_expression : variable
                        | NUMBER
                        | STRING_LITERAL
                        | TRUE
                        | FALSE
                        | LPAREN expression RPAREN
                        | function_call
                        | CHAR_LITERAL
        """
        if len(p) == 2:
            if isinstance(p[1],ASTNode):
                p[0] = p[1]
            else:
                p[0] = ASTNode("Literal",value=p[1])
        else:
            p[0] = p[2]

    def p_error(self, p):
        valid_tokens = [
            'PROGRAM', 'VAR', 'BEGIN', 'END', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO',
            'FOR', 'TO', 'DOWNTO', 'REPEAT', 'UNTIL', 'FUNCTION', 'PROCEDURE',
            'READ', 'READLN', 'WRITE', 'WRITELN', 'ARRAY', 'OF', 'INTEGER', 'BOOLEAN',
            'STRING', 'REAL', 'TRUE', 'FALSE', 'NOT', 'AND', 'OR', 'DIV', 'MOD',
            'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
            'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK', 'SEMI', 'COLON', 'COMMA', 'ASSIGN',
            'DOT', 'DOTDOT', 'ID', 'NUMBER', 'STRING_LITERAL', 'CHAR_LITERAL'
        ]

        if p:
            if p.type not in valid_tokens:  
                msg = f"Erro de sintaxe na linha {p.lineno}: token inesperado '{p.value}'."
                suggestions = get_close_matches(p.value, valid_tokens, n=3, cutoff=0.7)
                
                if suggestions:
                    msg += " Talvez você quis dizer: " + ', '.join([f"'{sug}'" for sug in suggestions])
                else:
                    msg += " Verifique a sintaxe."

                if msg not in self.errors:
                    self.errors.append(msg)

            elif p.type in {'ID', 'VAR', 'BEGIN', 'IF', 'WHILE', 'FOR', 'FUNCTION', 'PROCEDURE'}:
                msg = f"Erro de sintaxe na linha {p.lineno}: Esperado ';' antes '{p.value}'."
                msg += " Certifique-se de que todas as instruções ou declarações sejam terminadas com ';'."

                if msg not in self.errors:
                    self.errors.append(msg)

        else:
            if not self.errors:
                self.errors.append("Erro de sintaxe: final inesperado do arquivo. Verificar se há algum bloco fechado incorretamente.")

parser = Parser()

def parse_pascal(source_code):
    return parser.parse(source_code)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            source = f.read()
            ast = parse_pascal(source)
            if ast:
                print("Análise sintática concluída com sucesso!")
                print(ast)



    

