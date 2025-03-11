# Vending Machine

## Autor
- **Nome:** José António Costa Soares
- **Número de Aluno:** A103995
- **Foto:**

![José Soares](../images/josesoares.jpg)  

---

## Resumo

### Implementação

O projeto inclui um analisador léxico para processar os comandos do usuário e gerir transações de compra. A implementação permite:

- Inserção de moedas válidas
- Consulta do saldo disponível
- Listagem dos produtos disponíveis na máquina
- Seleção e compra de produtos
- Cálculo e devolução do troco

A máquina é configurada a partir de um ficheiro JSON que contém informações sobre os produtos em stock.

A biblioteca ```PLY``` (Python Lex) foi utilizada para construir o analisador léxico. O módulo ```ply.lex``` permitiu definir tokens para diferentes tipos de entrada:

Os comandos (LISTAR, SAIR, MOEDA, SALDO, SELECIONAR) foram reconhecidos com expressões regulares e convertidos para maiúsculas para garantir uniformidade.

Moedas foram identificadas através de tokens ```MONEY_E e MONEY_C```, permitindo validar valores aceitos (1€, 2€, 5c, 10c, 20c, 50c).

Códigos de produto foram identificados pelo formato ```A\d{2}```, para que apenas códigos válidos fossem processados.

Caso um token não fosse reconhecido, a função t_error ignorava o caractere inválido e continuava o processamento, garantindo robustez na interpretação dos comandos do usuário

## Resultados

O analisador léxico foi testado e validou corretamente a segmentação dos tokens. O sistema permite interagir com a máquina de vending de forma eficaz, garantindo que as transações são realizadas corretamente. Os principais arquivos do projeto são:

[tpc.py](tpc.py) -> Código-fonte do programa.

[stock.json](stock.json) -> Arquivo contendo a configuração inicial dos produtos disponíveis na máquina.


