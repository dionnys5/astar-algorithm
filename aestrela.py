import csv

file_routes = 'rotas-paris.csv' # Arquivo com rotas
class Node:
    # Classe que define um nó da árvore de busca, já permite guardar os valores
    def __init__(self,estacao):
        self.estacao = estacao
        self.parent = None
        self.children = []
        self.H = 0
        self.G = 0
        self.F = 0

    def __str__(self):
        return self.estacao + '\n'

def visit_node(estacao, goal, file_routes):
    # Função que visita o nó, define os valores e encontra o nome dos filhos (sem calcular valores pra eles)
    current = Node(estacao)
    with open(file_routes, 'r') as routes:
        data = csv.DictReader(routes, delimiter=';')
        for d in data:
            if (d['estacao1'] == current.estacao or d['estacao2'] == current.estacao) and d['real'] != '-':
                if d['estacao1'] == estacao:
                    current.children.append(d['estacao2'])
                else:
                    current.children.append(d['estacao1'])
            if current.estacao == goal:
                current.H = 0
            else:
                if (d['estacao1'] == current.estacao and d['estacao2'] == goal)\
                        or (d['estacao2'] == current.estacao and d['estacao1'] == goal):
                    current.H = float(d['direto'])
    return current


def calcula_custo(parent, child, file_routes):
    # Função que calcula o custo real do nó atual até o nó pai
    with open(file_routes, 'r') as routes:
        g = 0
        data = csv.DictReader(routes, delimiter=';')
        for d in data:
            if (d['estacao1'] == parent.estacao and d['estacao2'] == child.estacao) or\
                    (d['estacao1'] == child.estacao and d['estacao2'] == parent.estacao):
                return float(d['real'])
        return g


def get_min(fronteira):
    # Função pra percorrer e encontrar o melhor caminho com base na fronteira atual
    menor = None
    for i in fronteira:
        if menor is None:
            menor = i
        else:
            if menor.F > i.F:
                menor = i
    return menor

def aStar(start, goal, file_routes):
    #Inicia a fronteira e as estações visitadas
    fronteira = set()
    visitados = set()
    # Visita o nó inicial (define a estrutura)
    current = visit_node(start, goal, file_routes)
    if current.estacao == goal:
        # Verifica se foi digitado a estação inicial = a estação destino
        return {'caminho': ['Já está no seu destino'], 'custo_final': current.F}
    current.F = current.H + current.G
    #Adiciona o nó pai (inicial) na fronteira
    fronteira.add(current)
    # Continua a busca enquanto a fronteira não estiver vazia (ou se encontrar o melhor caminho)
    while fronteira:
        fronteira_atual = []
        for i in fronteira:
            fronteira_atual.append({'estação': i.estacao, 'valor função F': i.F})
        print(f"Fronteira ao visita o nó {current}: {fronteira_atual}")
        # Pega da fronteira o menor valor da função F (G + H)
        current = get_min(fronteira)
        #Se encontrar o que está procurar, retorna o caminho
        if current.estacao == goal:
            fronteira_atual = []
            for i in fronteira:
                fronteira_atual.append({'estação': i.estacao, 'valor função F': i.F})
            print(f"Fronteira ao visita o nó {current}: {fronteira_atual}")
            custo_final = current.F
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return {'caminho': path[::-1], 'custo_final': custo_final}
        #Remove remove da fronteira antes de visitar
        fronteira.remove(current)
        #Adiciona aos visitados
        visitados.add(current.estacao)
        #Visita os filhos children e adiciona eles na fronteira
        for node in current.children:
            child = visit_node(node, goal, file_routes)
            #Se já foi visitado, não precisa visitar novamente
            if child.estacao in visitados:
                continue
            #Calcula a função G (distância até o nó inicial)
            child.G = current.G + calcula_custo(current, child, file_routes)
            #Define o nó pai
            child.parent = current
            child.F = child.G + child.H
            if child.H < current.H:
                #Adiciona na fronteira só os filhos que estão indo pra mais perto do nó destino
                fronteira.add(child)
    #Gera uma exceção se não tiver caminho
    raise ValueError('No Path Found')

result = aStar('5', '10', file_routes)
print('RESULTADO: ')
for i in result['caminho']:
    print(i)
print("Custo final: {:.2f} horas".format(float(result['custo_final'])/30)) # Cálcula o custo de tempo, que é a distância dividido por 30 (velocidade em km/h)
