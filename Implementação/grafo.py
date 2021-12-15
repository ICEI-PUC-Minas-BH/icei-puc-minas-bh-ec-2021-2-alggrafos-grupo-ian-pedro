
import networkx as nx
import matplotlib.pyplot as plt

# Carregando arquivo de texto
def carregar_entrada():
    input = open(r'.\\input.txt', 'r')
    friend_list = []
    emails = []
    new_line = input.readline()
    num_group = int(new_line,10)
    for i in range(num_group):
        group_member_string = input.readline()
        group_member_list = group_member_string[0:-1].split(' ')
        friend_list.append(group_member_list[0:-1])

    while True:
        line = input.readline()
        if(line == '0\n'):
            break
        line = line.replace('\n','')
        email = line.split(' ')
        emails.append(email)

    group_member_list_name = []

    for i in range(num_group):
        group_member_list_name.append(input.readline().replace('\n',''))    
    input.close()
    return (num_group,friend_list,group_member_list_name,emails)


# Função para gerar arestas
def gerar_arestas(iterable):
    arestas = []
    for i, edges in enumerate(iterable):
        for edge in edges:
            arestas.append((i+1,int(edge)))
    return arestas


# Função para gerar uma matriz de incidencia
def gerar_matriz_incidencia(arestas,vertices_num):
    matriz_incidencia = []
    #iniciar uma matriz com todos os valores igual a 0
    for i in range(vertices_num):
        matriz_incidencia.append([])
        for j in range(vertices_num):
            matriz_incidencia[i].append(0)

    for a,b in arestas:
        matriz_incidencia[a-1][b-1] = 1
    
    return matriz_incidencia

# Função para retornar o grau de um vertice
def grau_do_vertice(vertice,matriz_incidencia):
    count = 0
    for aresta in matriz_incidencia[vertice-1]:
        if aresta == 1:
            count += 1
    return count

# função para definir as caracteriscas com base nos envios
def gerar_caracteristica(envios,email):
    caracteristicas = ''
    if  (envios < int(email[1])):
        caracteristicas += email[3] + ' '
    elif int(email[1]) <= envios and envios < int(email[2]):
        caracteristicas += email[4] + ' '
    else:
        caracteristicas += email[5] + ' '

    return caracteristicas

# Procedimento para gerar arquivo de saida
def gerar_saida(num_group,friend_list,group_member_list_name,emails):
    output_list = []
    arestas = gerar_arestas(friend_list)
    matriz_incidencia = gerar_matriz_incidencia(arestas,num_group)
    caracteristicas = {name: '' for name in group_member_list_name}

    for email in emails:
        result_dfs = dfs(int(email[0]))
        for i in range(num_group):

            if str(i + 1) in result_dfs:
                envios = grau_do_vertice(i+1,matriz_incidencia)
            else:
                envios = 0

            caracteristicas[group_member_list_name[i]] += gerar_caracteristica(envios,email)

    for name in group_member_list_name:
        output_list.append(name +': '+ caracteristicas[name]+'\n')
        
    output = open(r'.\\output.txt', 'w')    
    output.writelines(output_list)
    output.close()
    pass

# Função de busca em profundidade
def dfs(start_node):
    visited = {node+1: False for node in range(num_group)}
    stack = [start_node]
    result = []
    while stack:
        curr_node = stack.pop()
        if not visited[curr_node]:
            result.append(str(curr_node))
            visited[curr_node] = True
        for node in G.neighbors(curr_node):
            if not visited[node]:
                stack.append(node)
    return result


# Carregando dados de entrada
num_group,friend_list,group_member_list_name,emails = carregar_entrada()

# Definindo as arestas do grafo
arestas = gerar_arestas(friend_list)

# Instanciando o grafo direcionado
G = nx.DiGraph()

# Populando grafo NetworkX
for edge in arestas:
    G.add_edge(edge[0],edge[1])  


# Print matriz de incidencia
matriz_incidencia = gerar_matriz_incidencia(arestas,num_group)

print("Matriz de Incidencia\n")
for i in matriz_incidencia:
    print(i)


# Gerando visualização do grafo
labels = {}
for i,label in enumerate(group_member_list_name):
    labels[i+1] = label + ' | ' + str(i+1)

# Gerando o arquivo de saida
gerar_saida(num_group,friend_list,group_member_list_name,emails)

# Exibindo grafo inicial
plt.figure('Grafo inicial')
nx.draw_networkx(G,labels=labels, with_labels = True,node_size = 2500)

# Exibindo grafos resultantes
for i,email in enumerate(emails):
    plt.figure('Grafo resultante email ' + str(i+1) )
    color_map = []
    vertice_inicial = int(email[0])
    dfs_r = dfs(vertice_inicial)
    print("\nAlcance email " + str(i+1))
    print('->'.join(dfs_r))
    for node in G:
        if node == vertice_inicial:
            color_map.append('red')
        elif str(node) not in dfs_r:
            color_map.append('cyan')
        else: 
            color_map.append('green')
    nx.draw_networkx(G,labels=labels,node_color=color_map, with_labels = True,node_size = 2500)

plt.show()

