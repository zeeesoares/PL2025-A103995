# Obras e Compositores

## Autor
- **Nome:** José António Costa Soares
- **Número de Aluno:** A103995
- **Foto:**

![José Soares](../images/josesoares.jpg)  

---

## Resumo

Nesta diretoria encontra-se a resolução do TPC2 proposto na aula teórica realizada no dia 14 de fevereiro de 2025.

Neste TPC, o objetivo foi processar um arquivo de texto com informações sobre obras musicais, sem usar o módulo CSV do Python, para realizar as seguintes operações:

1. Criar uma lista ordenada alfabeticamente com os compositores musicais.
2. Distribuir as obras por período, contando quantas obras existem em cada período.
3. Criar um dicionário onde cada período tem uma lista alfabética dos títulos das obras catalogadas nesse período.

A implementação foi feita em Python, e os dados foram lidos e processados utilizando expressões regulares e manipulação de texto, sem recorrer ao módulo CSV.


Neste programa, o objetivo é processar um arquivo de entrada contendo informações sobre obras musicais e gerar diversos relatórios. As obras são descritas por campos como nome, descrição, ano de criação, período, compositor, duração e ID. O programa foi desenvolvido em Python, dividindo-se em duas grandes etapas: o processamento do arquivo e a realização das consultas.

## Etapas de Implementação

### 1. Processamento do Arquivo (Parser)

O objetivo era ler o conteúdo do arquivo `obras.csv`, processar as informações e criar objetos representando as obras musicais. O arquivo possui os seguintes campos separados por ponto e vírgula (`;`):

- Nome da obra
- Descrição
- Ano de criação
- Período
- Compositor
- Duração
- ID

#### Tokenização e Expressão Regular

Foi utilizada uma **expressão regular** para fazer o parsing do conteúdo do arquivo. A função `parse_obra` recebe as linhas do arquivo e aplica a expressão regular para encontrar as correspondências. 

A expressão regular usada foi:

```python
pattern = r'([^;]+);(?:()|([^"\n;][^\n;]*)|(?:"((?:[^"]|"")*)"));(\d+);([^;]+);([^;]+);(\d{2}:\d{2}:\d{2});([^;]\d+)'
```

O padrão precisa capturar várias partes da linha:

- ```([^;]+)``` - Captura o nome da obra, que é o primeiro campo até o ponto e vírgula.
- ```(?:()|([^"\n;][^\n;]*)|(?:"((?:[^"]|"")*)"))``` - Captura a descrição, que pode ser entre aspas ou sem aspas.
- ```(\d+)``` - Captura o ano de criação, que é um número.
- ```([^;]+)``` - Captura o período, até o próximo ponto e vírgula.
- ```([^;]+)``` - Captura o compositor, que pode ser "Sobrenome, Nome" ou "Nome Sobrenome".
- ```(\d{2}:\d{2}:\d{2})``` - Captura a duração, que está no formato hh:mm:ss.
- ```([^;]\d+)``` - Captura o ID da obra.

Depois da tokenização, seguiu-se com a normalização dos campos, uma vez que era necessário retirar caracteres vazios ```\s+```.


#### Geração da Estrutura

Depois de ter conseguido separar cada campo, o próximo passo foi guardar cada objeto (Obra) num dicionário para futuro tratamento de dados a envolver as 3 *queries* pedidas.

Para isso utilizei uma classe ```Obra``` constituida por:
```
class Obra:
    def __init__(self, nome, descricao, ano_criacao, periodo, compositor, duracao, _id):
        self.nome = nome
        self.descricao = descricao
        self.ano_criacao = ano_criacao
        self.periodo = periodo
        self.compositor = compositor
        self.duracao = duracao
        self._id = _id
```


#### Resolução das Quesões

- **1. Criar uma lista ordenada alfabeticamente com os compositores musicais.**  
Através do dicionário ```obras```, foi criada uma lista em que à medida que eram percorridas as obras, era adicionada a essa mesma lista o autor de cada obra.

- **2. Distribuir as obras por período, contando quantas obras existem em cada período.**  
Através do dicionário ```obras```, foi criado outro dicionário que permitiu associar cada periodo com as suas obras. Desta forma, e através do tamanho da lista consegui recolher a informação de quantas obras estavam inseridas em cada período.

- **3. Criar um dicionário onde cada período tem uma lista alfabética dos títulos das obras catalogadas nesse período.**
Aproveitando o dicionário gerado na alínea anterior, apenas foi necesssário ordenar a lista respetiva a cada periodo com os títulos das obras.


## Lista de Resultados

O programa desenvolvido foi testado com diversos testes e confirmou-se que estes funcionavam corretamente e devolviam os valores esperados.

Cada questão do enunciado pode ser verificada em:

- [nomesCompositores.txt](nomesCompositores.txt) - 1. Criar uma lista ordenada alfabeticamente com os compositores musicais
- [obrasPorPeriodoNumero.txt](obrasPorPeriodoNumero.txt) - 2. Distribuir as obras por período, contando quantas obras existem em cada período
- [obrasPorPeriodoNome.txt](obrasPorPeriodoName.txt) - 3. Criar um dicionário onde cada período tem uma lista alfabética dos títulos das obras catalogadas nesse período