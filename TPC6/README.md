# Analisador Sintático

## Autor
- **Nome:** José António Costa Soares
- **Número de Aluno:** A103995
- **Foto:**

![José Soares](../images/josesoares.jpg)  

---

## Resumo

Este tpc consiste num analisador léxico em conjunto com um analisador sintático para:
- 5 + 3 * 2
- 2 * 7 - 7 * 3


### Implementação

A implementação baseia-se nos seguintes passos:

- Analisador Léxico

Para recolher os tokens em cada expressão foi utilizado um conjunto de **literais** [+, -, *, /] que representam as operações e também o token **NUM**  que representa os números.

Para construir o analisador utilizei a biblioteca **ply.lex** do python, e tendo feito as expressões regulares para recolher os tokens, tinha pronto o meu analisador léxico para passar os tokens à próxima étapa.

- Analisador Sintático

Desta vez, para a realização deste modulo decidi primeiramente construir a minha gramática de forma a lidar com as restrições provocas pela ordem das operações matemáticas, uma vez que as multiplicações e divisões devem todos preceder as somas ou subtrações. Para isto desenvolbi a seguinte gramática:

```hs
Exp : Term ExpCont

ExpCont: ('+' | '-') Term ExpCont
    | ε

Term : Num TermCont

TermCont: ('*' | '/') Num TermCont
     | ε
```

Esta gramática traduz se num funciomanto recursivo descendente uma vez que as produções de Exp' e Term' usam recursividade à direita, e elimina a Ambiguidade à esquerda, o que facilita a implementação do parser descendente.

O seu funcionamento dá prioridade às operações de mult/div e coloca-as sempre depois das somas e divisões, que por recursão descendente acabam por ser as primeiras a ser realizadas.

Um exemplo poderá ser ```2 + 7 * 2```

```js
          Exp
          /\
         /  \
        /    \
       /      \
    Tern     ExpCont------
    /\        /\       \
   /  \      +  Term   ExpCont
  /    \          /\       \
 Num  TermCont      /  \       ε
 /      \       7   TermCont---
2        ε           /\    \
                    *  2   TermCont
                              \
                               ε

ou de forma simples:

   (+)                         
  /   \
 2     (*)
      /   \
     7     2

```

Durante a construção recursiva, é gerada uma àrvore com a estrutura ```(op, left right)```,  que gera resultados do tipo:

```(+ 2 (* 7 2))```

No final para calcular o valor da expressão, fiz a funcão **evaluate(tree)** que é responsável por fazer de forma recursiva as operações pela ordem definida.


## Resultados 

O analisador léxico foi testado e validou a correta segmentação dos tokens. 

Os arquivos de resultado são:

- [tpc_analex.py](tpc_analex.py) - Código-fonte do analisador léxico.
- [tpc_anasin.py](tpc_anasin.py) - Código-fonte do analisador sintático.
- [input.txt](input.txt) - Arquivo de entrada da expressão.
- [output.txt](output.txt) - Arquivo de saída com os resultados.
