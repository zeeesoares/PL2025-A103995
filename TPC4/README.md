# Analisador Léxico

## Autor
- **Nome:** José António Costa Soares
- **Número de Aluno:** A103995
- **Foto:**

![José Soares](../images/josesoares.jpg)  

---

## Resumo

Este tpc consiste num analisador léxico para consultas, foi implementado em Python através da bibliotaca PLY. O objetivo é identificar e classificar corretamente os tokens presentes numa consulta, tais como palavras-chave (SELECT, WHERE, LIMIT), variáveis, literais, predicados e outros símbolos.

### Implementação

A implementação baseia-se nos seguintes passos:

- Palavras-chave (Keywords)
    - SELECT, WHERE, LIMIT

    - Devem ser reconhecidos como tokens específicos, geralmente sem distinção entre maiúsculas e minúsculas.

- Símbolos e Pontuação

  - { (abre chave) → LBRACE

  - } (fecha chave) → RBRACE
  - . (ponto final para tripla) → DOT

- Variáveis

   - ?nome, ?desc, ?s, ?w

- Predicados e Tipos RDF

    - a → PREDICATE (atalho para rdf:type)
  
    - dbo:MusicalArtist, dbo:artist, foaf:name, dbo:abstract


- Literais (Strings e Números)

  - "Chuck Berry"@en

  - 1000 (limite) Número inteiro → NUM

- Comentários

  - \# DBPedia: obras de Chuck Berry - Linha que começa com # → COMMENT

## Resultados 
Entrada:
```
\# DBPedia: obras de Chuck Berry
SELECT ?nome ?desc WHERE {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
```


Tokens gerados:

```
LexToken(COMMENT,'# DBPedia: obras de Chuck Berry',1,0)
LexToken(SELECT,'SELECT',3,33)
LexToken(VAR,'?nome',3,40)
LexToken(VAR,'?desc',3,46)
LexToken(LITERAL,'WHERE ',3,52)
LexToken(LBRACE,'{',3,58)
LexToken(VAR,'?s',4,64)
LexToken(PREDICATE,'a',4,67)
LexToken(PREDICATE,'dbo:MusicalArtist',4,69)
LexToken(DOT,'.',4,86)
LexToken(VAR,'?s',5,92)
LexToken(PREDICATE,'foaf:name',5,95)
LexToken(LITERAL,'"Chuck Berry"@en ',5,105)
LexToken(DOT,'.',5,122)
LexToken(VAR,'?w',6,128)
LexToken(PREDICATE,'dbo:artist',6,131)
LexToken(VAR,'?s',6,142)
LexToken(DOT,'.',6,144)
LexToken(VAR,'?w',7,150)
LexToken(PREDICATE,'foaf:name',7,153)
LexToken(VAR,'?nome',7,163)
LexToken(DOT,'.',7,168)
LexToken(VAR,'?w',8,174)
LexToken(PREDICATE,'dbo:abstract',8,177)
LexToken(VAR,'?desc',8,190)
LexToken(RBRACE,'}',9,196)
LexToken(LITERAL,'LIMIT 1000',9,198)
```

O analisador léxico foi testado e validou a correta segmentação dos tokens. 

Os arquivos de resultado são:

- [tpc.py](tpc.py) - Código-fonte do conversor.
- [input.txt](input.txt) - Arquivo de entrada contendo a consulta.
- [output.txt](output.txt) - Arquivo de saída com os tokens.


