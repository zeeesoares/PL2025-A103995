class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo  # "NUM", "CMD", "EQ"
        self.valor = valor  # O valor do token (ex: 123, "On", "Off", "=")

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"

def lexer(ficheiro):
    tokens = []    
    with open(ficheiro, 'r', encoding='utf-8') as f:
        conteudo = f.read()  
        i = 0
        n = len(conteudo)

        while i < n:
            char = conteudo[i]

            if char.isdigit():
                num = ""
                while i < n and conteudo[i].isdigit():
                    num += conteudo[i]
                    i += 1
                tokens.append(Token("NUM", int(num)))
                continue  

            elif char.isalpha():
                palavra = ""
                while i < n and conteudo[i].isalpha():  
                    palavra += conteudo[i]
                    i += 1
                palavra = palavra.lower()
                
                if "on" in palavra:
                    tokens.append(Token("CMD", "On"))
                elif "off" in palavra:
                    tokens.append(Token("CMD", "Off"))
                continue 

            elif char == "=":
                tokens.append(Token("EQ", "="))
            
            i += 1 

    return tokens


def interpreter(tokens):
    isOn = True
    count = 0
    for token in tokens:
        if token.tipo == "CMD":
            if token.valor == "On":
                isOn = True
            elif token.valor == "Off":
                isOn = False
        elif token.tipo == "EQ":
            print(count)
        elif token.tipo == "NUM":
            if isOn:
                count += token.valor

    return count

tokens = lexer("dataset.txt")  
print(tokens)  
value = interpreter(tokens)
print(f"Resultado Final: {value}")