class ASTNode:
    def __init__(self, type, children=None, value=None, extra=None, lineno=None):
        self.type = type
        self.children = children if children else []
        self.extra = extra or {}
        self.value = value
        self.lineno = lineno

    def __repr__(self, level=0):
        indent = "  " * level
        rep = f"{indent}{self.type}"
        if self.value is not None:
            rep += f" [{self.value}]"
        if self.lineno is not None:
            rep += f" (linha {self.lineno})"
        rep += "\n"
        
        for child in self.children:
            if isinstance(child, ASTNode):
                rep += child.__repr__(level + 1)
            else:
                rep += f"{'  ' * (level + 1)}{child}\n"
        return rep

    def accept(self, visitor):

        # Procura o método de visita correspondente ao tipo do nó

        method_name = f'visit_{self.type.lower()}'
        visitor_method = getattr(visitor, method_name, None)
        
        if visitor_method is not None:
            return visitor_method(self)
        
        # Se não houver um método específico, visita os filhos
        
        for child in self.children:
            if isinstance(child, ASTNode):
                child.accept(visitor)