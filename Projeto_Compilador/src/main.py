import sys
from anasin import parse_pascal
from translator import EWVMTranslator

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            source = f.read()
            ast = parse_pascal(source)
            
            if ast:
                print("\nÁrvore Sintática Abstrata (AST):")
                print(ast)
                
                translator = EWVMTranslator(ast)
                machine_code = translator.translate()
                print("\nCódigo Gerado:")
                print(machine_code)
            else :
                return 0
    else:
        print("Uso: python main.py <arquivo.pas>")

if __name__ == "__main__":
    main()