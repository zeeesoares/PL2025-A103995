import re

class Obra:
    def __init__(self, nome, descricao, ano_criacao, periodo, compositor, duracao, _id):
        self.nome = nome
        self.descricao = descricao
        self.ano_criacao = ano_criacao
        self.periodo = periodo
        self.compositor = compositor
        self.duracao = duracao
        self._id = _id
    
    def __repr__(self):
        return (f"Obra(nome={self.nome}, descricao={self.descricao}, ano_criacao={self.ano_criacao}, "
                f"periodo={self.periodo}, compositor={self.compositor}, duracao={self.duracao}, _id={self._id})")


def normalize_field(field):
    return re.sub(r'\s+', ' ', field.strip())

def normalize_compositor(compositor):
    match = re.match(r'([^,]+), ([^,]+)', compositor)
    if match:
        return f"{match.group(2)} {match.group(1)}"
    else:
        return compositor  

def parse_obra(lines):
    pattern = r'([^;]+);(?:()|([^"\n;][^\n;]*)|(?:"((?:[^"]|"")*)"));(\d+);([^;]+);([^;]+);(\d{2}:\d{2}:\d{2});([^;]\d+)'
    
    matches = re.findall(pattern, lines)
    
    obras = {} 

    for match in matches:
        nome = normalize_field(match[0])
        descricao = normalize_field(match[3].strip('"')) 
        ano_criacao = normalize_field(match[4])
        periodo = normalize_field(match[5])
        compositor = normalize_compositor(normalize_field(match[6]))
        duracao = normalize_field(match[7])
        _id = normalize_field(match[8])

        obra = Obra(nome, descricao, ano_criacao, periodo, compositor, duracao, _id)
        obras[_id] = obra
    
    return obras

def getCompositores(obras):
    compositores = set()
    for obra in obras.values():
        compositores.add(obra.compositor)
    return compositores

def obrasPorPeriodo(obras):
    periodos = {}
    for obra in obras.values():
        periodo = obra.periodo
        if periodo in periodos:
            periodos[periodo].append(obra.nome)
        else:
            periodos[periodo] = [obra.nome]

    for periodo in periodos:
        periodos[periodo] = sorted(periodos[periodo])
    return periodos
 

def Query1(result_file):
    with open(result_file, 'w') as f:
        f.write("Compositores: [\n")
        for comp in sorted(getCompositores(obras)):
            f.write(f"   {comp},\n")
        f.write("]\n")

def Query2(result_file):
    with open(result_file, 'w') as f:
        for periodo, listaObras in obrasPorPeriodo(obras).items():
            f.write(f"Obras do período {periodo}: {len(listaObras)}\n")

def Query3(result_file):
    with open(result_file, 'w') as f:
        for periodo, listaObras in obrasPorPeriodo(obras).items():
            f.write(f"Obras do período {periodo}:\n")
            for obra in listaObras:
                f.write(f"    {obra}\n")
            f.write("\n")

if __name__ == "__main__":
    ficheiro = 'obras.csv'
    obras = {}

    with open(ficheiro, 'r') as f:
        lines = f.read()
        obras = parse_obra(lines)
    Query1("nomesCompositores.txt")
    Query2("obrasPorPeriodoNumero.txt")
    Query3("obrasPorPeriodoName.txt")