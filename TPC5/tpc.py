import json
import datetime
import re
import ply.lex as lex

tokens = [
    'COMMAND',
    'MONEY_E',
    'MONEY_C',
    'PRODUCT_CODE'
]

t_COMMAND = r'(?i)LISTAR|SAIR|MOEDA|SALDO|SELECIONAR'

t_PRODUCT_CODE = r'A\d{2}'

valid_coins = {1, 2, 5, 10, 20, 50} 

def t_MONEY_E(t):
    r'(\d)+e'
    value = int(t.value[:-1])
    if value in valid_coins:
        t.value = value
    else:
        t.value = None  
    return t

def t_MONEY_C(t):
    r'(\d)+c'
    value = int(t.value[:-1])
    if value in valid_coins:
        t.value = value
    else:
        t.value = None  
    return t

t_ignore = ' \t,'

def t_error(t):
    t.lexer.skip(1)

def create_lexer(input_data):
    lexer_instance = lex.lex()
    lexer_instance.input(input_data)
    return lexer_instance

def get_tokens(input_data):
    lexer_instance = create_lexer(input_data)
    tokens_list = []
    while True:
        tok = lexer_instance.token()
        if not tok:
            break
        if tok.value is not None:  
            if tok.type == 'COMMAND': 
                tok.value = tok.value.upper()
            tokens_list.append(tok)
    return tokens_list

def logger(line):
    print(f'maq: {line}')

def open_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_stock(stock, cod, nome, quant, preco):
    stock['stock'].append({
        'cod': cod,
        'nome': nome,
        'quant': quant,
        'preco': preco
    })

def buy_product(stock, cod, saldo):
    for product in stock['stock']:
        if product['cod'] == cod:
            if product['quant'] > 0 and product['preco'] <= saldo:
                product['quant'] -= 1
                saldo = round(saldo - product['preco'], 2)
                logger(f'Saldo atual: {saldo}€ ')
                return product, saldo
            else:
                return None
    return None

def list_stock(stock):
    result = "\n"
    result += "  code  |    name     |  quantity   |  price  \n"
    result += "--------------------------------------------------\n"
    for product in stock['stock']:
        result += f"  {product['cod']:<5} | {product['nome']:<11} | {product['quant']:<11} | {product['preco']:<8} \n"
    return result

def give_change(amount):
    coins = [200, 100, 50, 20, 10, 5, 2, 1] 
    change = {}
    for coin in coins:
        coin_count = amount // coin
        if coin_count > 0:
            change[coin] = coin_count
            amount -= coin_count * coin
    return change

def config_vend(filename):
    config = open_json(filename)
    saldo = 0.0
    current_date = datetime.datetime.now().date()
    logger(f'{current_date}, Stock carregado, Estado atualizado.')
    logger('Bom dia. Estou disponível para atender o seu pedido.')
    
    while True:
        input_user = input('>> ')

        tokens = get_tokens(input_user)
        
        if len(tokens) == 0:
            logger(f'Erro no comando!')
            continue

        if tokens[0].type == 'COMMAND':
            if tokens[0].value == 'SAIR':
                logger('Obrigado. Volte sempre.')
                change = give_change(int(saldo * 100))
                if change == {}:
                    logger('Não há troco a devolver.')
                    break
                change_msg = "Troco: "
                for coin, count in change.items():
                    if coin >= 100:
                        coin_value = f'{coin // 100}€'
                    else:
                        coin_value = f'{coin}c'
                    change_msg += f"{count}x{coin_value} "
                logger(change_msg.strip())
                save_json(filename, config)
                break
            elif tokens[0].value == 'LISTAR':
                logger(list_stock(config))
            elif tokens[0].value == 'MOEDA':
                if len(tokens) == 1:
                    logger(f'Comando inválido!')
                for token in tokens[1:]:
                    if token.type == 'MONEY_E' or token.type == 'MONEY_C':
                        if token.value is not None: 
                            saldo += token.value / 100 if token.type == 'MONEY_C' else token.value
                            logger(f'Saldo disponível: {saldo}€')
                        else:
                            logger("Moeda inválida. Tente novamente.")
            elif tokens[0].value == 'SALDO':
                logger(f'Saldo atual: {saldo}€ ')
            elif tokens[0].value == 'SELECIONAR':
                if len(tokens) != 2:
                    logger('Comando inválido.')
                    continue
                product, saldo = buy_product(config, tokens[1].value, saldo)
                if product:
                    logger(f'Produto {product["nome"]} comprado com sucesso.')

            else:
                logger('Comando inválido.')
        else:
            logger(f'Erro no comando!')

if __name__ == '__main__':
    config_vend('stock.json')
