# Conversor de MarkDown para HTML

## Autor
- **Nome:** José António Costa Soares
- **Número de Aluno:** A103995
- **Foto:**

![José Soares](../images/josesoares.jpg)  

---

## Resumo

O problema abordado neste projeto foi a conversão de texto em formato Markdown para HTML, permite a formatação de títulos, listas, negrito, itálico, imagens e links. O objetivo foi criar um conversor simples que pudesse interpretar um arquivo Markdown e transformá-lo em uma página HTML **estruturada**.

### Implementação

A implementação foi feita em Python utilizando expressões regulares para identificar e substituir elementos do Markdown pelos seus equivalentes mas em HTML. O processo seguiu os seguintes passos:

- Tokenização: O texto Markdown é separado em linhas para facilitar a análise. Esse processo é necessário porque o Markdown possui características distintas, como a interpretação de quebras de linha, listas que podem ser representadas por números ou traços e títulos identificados por "#".
- Análise Sintática: Cada linha é analisada para determinar o tipo. Além disso, independentemente da categoria da linha, são sempre verificadas e convertidas as marcações de negrito, itálico, imagens e links.
- Conversão Semântica: Após a identificação dos elementos, cada estrutura Markdown é convertida para sua equivalente em HTML:
    - Títulos: Convertidos em tags ```<h1>``` a ```<h6>```.
    - Listas Ordenadas: Convertidas para ```<ol>``` com itens ```<li>```.
    - Texto: Convertidos para parágrafos ```<p>``` .

- Escrita em Arquivo: O HTML gerado é guardado no arquivo de saída.

---

## Resultados

O programa desenvolvido foi testado com diversos testes e confirmou-se que estes funcionavam corretamente e devolviam os valores esperados.

Os arquivos gerados durante o processamento são:
- [tpc.py](tpc.py) - Código-fonte do conversor.
- [in.md](in.md) - Arquivo de entrada contendo o texto em Markdown.
- [result.html](result.html) - Arquivo de saída com o HTML convertido.