# Somador ON/OFF

## Autor
- **Nome:** José António Costa Soares
- **Número de Aluno:** A103995
- **Foto:**

![José Soares](../images/josesoares.jpg)  


## Resumo
Nesta diretoria encontra-se a resolução do TPC1 proposto na aula teórica realizada no dia 7 de fevereiro.  

O objetivo deste problema era realizar a soma de todas as sequências de dígitos presentes num ficheiro de texto.As restrições estavam focadas na existência de comandos capazes de ligar ou desligar a soma:

- Sempre que fosse encontrado o comando "On", o contador passava a somar os números encontrados.
- Se fosse encontrado o comando "Off", a soma era interrompida.
- O operador "=" servia para exibir o resultado da soma até aquele momento.


### Implementação

A resolução foi realizada em Python, dividindo o problema em três partes principais:

- Tokenização (Lexer)
    - O ficheiro de entrada era processado caractere por caractere.
    - Os números eram reconhecidos e agrupados corretamente, mesmo que contivessem zeros à esquerda.
    - Os comandos "On" e "Off" eram identificados mesmo se estivessem dentro de outras palavras.
    - Caracteres irrelevantes eram ignorados.
  
    Esta função surgiu da tentativa de uma simplificação quanto à recolha/interpretação de dados para um futuro processamento.

    Para isso, utilizei uma classe chamada **Token** para armazenar num para o Tipo ("NUM", "CMD", "EQ") e o Valor depois associado (ex: 123, "On", "Off", "=").

    ```
    class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor 
    ```

    Sendo assim ficheiros de entrada contendo, por exemplo:

    ```
    on1sfa*@daf3=1offosdson 10=
    ```

    Deve resultar numa tokenização em:

    ```
    [Token(CMD, On), Token(NUM, 1), Token(NUM, 3), Token(EQ, =), Token(NUM, 1), Token(CMD, On), Token(NUM, 10), Token(EQ, =)]
    ```



- Interpretação (Somador)

    - O estado do somador era controlado por um booleano (isOn), ativado e desativado conforme os comandos "On" e "Off". Quando ativado, os valores numéricos eram somados.

    - Quando o operador "=" aparecia, o resultado da soma era impresso.

    O que esta função faz é percorrer a lista de tokens e realizar operações conforme o conteúdo atribuido a cada **Token**.

## Lista de Resultados

O programa desenvolvido foi testado com diversos testes e confirmou-se que estes funcionavam corretamente e devolviam os valores esperados.
