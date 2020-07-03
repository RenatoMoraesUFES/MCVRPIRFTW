import os
import networkx as nx
import matplotlib.pyplot as plt

###############################################################################

def escrita(texto, dic_instancia):
    """ Funcao de escrita dos dados obtidos na funcao leitura
        Abre um arquivo de saida e percorre todo o arquivo texto
        Escreve uma copia identica ao arquivo original
    """
	
    entrada    = dic_instancia["nome_instancia"]          #             # nome do arquivo .dat da instancia			
    #nos        = dic_instancia["clientes"]                # quantidade de clientes (int) 
    #nosf       = dic_instancia["facilidades"]             # quantidade facilidades (int)
    #m          = dic_instancia["num_veiculo_frota"]       # numero de veiculos da frota(int) 
    #ncp        = dic_instancia["num_max_compartimentos"]  # número máximo de compartimentos(int) 
    #M          = dic_instancia["M_grande"]                # parâmetro auxiliar  um número "muito grande" (int)
    #distancia  = dic_instancia["distancia"]               # distancia em km (ou custo) do arco i j  onde i e j podem ser clientes e/ou facilidades. (float)
    #t          = dic_instancia["tempo"]                   # matriz tempo em horas de i para j  onde i e j podem ser clientes e/ou facilidades (lista de lista float - matriz)
    #wti        = dic_instancia["janela_cliente_inicio"]   # inicio da janela de tempo cliente (lista int)
    #wtf        = dic_instancia["janela_cliente_fim"]      # fim da janela de tempo cliente (lista int)    
    #ot         = dic_instancia["tempo_operacao_caixa"]    # tempo médio de operação de uma caixa (h) (0.02h = 1.2min) (float)
    #N          = dic_instancia["num_caixas"]              # Numero de caixas (int)
    #prop       = dic_instancia["caixas_do_cliente"]       # Qual caixa pertence a qual cliente (lista de lista boolean - matriz) "Boolean type can only be one of True or False"
    #vlb        = dic_instancia["volume_caixa"]            # volumes das caixas (lista float)        
    #vlc        = dic_instancia["num_caixa_maior_cliente"] # soma dos numeros de caixa do maior cliente (lista de lista float - matriz)
    #ck         = dic_instancia["custo_fixo_bike"]         # custo fixo das bicicletas (lista int)
    #cd         = dic_instancia["custo_km_rodado"]         # custo por km rodado (lista float)				
				
				
			
    if not os.path.exists('OUTPUT'):    #se o caminho não existe
        os.makedirs('OUTPUT')           #crio um diretorio
    os.chdir('OUTPUT')      #entro para escrita do arquivo de saida
    saida = entrada + '.out' # define nome do arquivo de saida
    fout = open(saida, 'w')
    #percorrer todo o texto inutil
    for linha in texto: # linha eh uma string       
        fout.write(linha)
    fout.close()
    os.chdir('..')
    #print("\n\nFIM - verificar arquivo de saida.\n")
#fim escrita
###############################################################################

    
###############################################################################

def grafo_distancia(dic_instancia):
    """ Funcao para criar um arquivo de saida '.dot'
        Gera um grafo para a lista de listas (matriz) 'distancia' pelo graphviz
    """

    ### OPCAO 1 COM NETWORKX EM PROCESSO ###
    '''grafo_dist = nx.Graph()
    
    for i in range(len(dic_instancia['distancia'])-2):
        for j in range(len(dic_instancia['distancia'][i])-1):
            if i != j and dic_instancia['distancia'][i][j] != 9999:
                if dic_instancia['distancia'][i][j] < 2:
                    grafo_dist.add_edge(i,j, value=dic_instancia['distancia'][i][j])

    pos = nx.shell_layout(grafo_dist)
    nx.draw(grafo_dist, pos, with_labels=1)
    nx.draw_networkx_edge_labels(grafo_dist, pos)
    #plt.text(0,1,str(grafo_dist.size(weight='value')), fontdict=None)
    plt.show()'''

    ### OPCAO 2 COM GRAPHVIZ EM PROCESSO (MAIS AVANCADO) ###
    caminho = 'OUTPUT'
    name = dic_instancia["nome_instancia"]
    distancia = dic_instancia["distancia"]
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    file = caminho + '/' + name + '_DIST.dot'
    #abro um arquivo '.dot' para linguagem graphviz
    arq = open(file, 'w')
    #primeira linha como padrao da linguagem
    arq.write('strict graph {\n')
    #arq.write('0 [pos="0,0!"];\n')  ### fixar armazem central no centro
    for i in range(len(distancia)-1):
        ### 'if' para fixar posicao dos nós; preciso trabalhar na posicao
        #if i != 0 and i != len(distancia)-1:
            #arq.write(str(i) + f' [pos="{i},{i}!"];\n')
        for j in range(len(distancia[i])-1):
            #ignoro as distancias entre si mesmos e as 'infinitas' ditas '9999'
            if not i == j and distancia[i][j] != 9999:
                #aresta como vertice os indices da matriz distancia
                arq.write(str(i)
                            + '--'
                            + str(j)
                            + ' [label =  "'
                            + "%.3f" %distancia[i][j]
                            + 'km"];\n')
    arq.write('}')
    arq.close()
    #print("\nVerificar arquivo '.dot' de saída.\n")
    os.chdir('OUTPUT')
    os.system('dot ' + name + '_DIST.dot -Tpng -o' + name + '_DIST.png')
    #os.system('dot -Kfdp -n -Tpng -o '
     #         + name + '_DIST.png '
      #        + name + '_DIST.dot')
    os.chdir('..')
    #print("\nVerificar arquivo '.png' de saída.\n")

    # codigo acima equivale a execucao no terminal:
    # -> dot nomedoarquivo.dot -Tpng -o nomedografo.png
###############################################################################

###############################################################################

def grafo_caixas_do_cliente(dic_instancia):
    """ Funcao para criar um arquivo de saida '.dot'
        Gera um grafo para a lista de listas (matriz) 'prop'
        O grafo mostra quais caixas (j) pertencem a quais clientes (i) em 'prop'
    """

    ### OPCAO 1 COM NETWORKX ###
    '''grafo_caixas = nx.Graph()
    for i in range(len(dic_instancia['caixas_do_cliente'])-1):
        cliente = f"Cliente{i}"
        for j in range(len(dic_instancia['caixas_do_cliente'][i])):
            caixa = f"Caixa{j}"
            if dic_instancia['caixas_do_cliente'][i][j] == 1:
                grafo_caixas.add_edge(cliente, caixa, value=100)
    pos = nx.planar_layout(grafo_caixas)
    nx.draw(grafo_caixas, pos, with_labels=1)
    plt.text(0,1,str(grafo_caixas.size(weight='value')), fontdict=None)
    plt.show()'''

    ### OPCAO 2 COM GRAPHVIZ ###
    caminho = 'OUTPUT'
    name = dic_instancia["nome_instancia"]
    prop = dic_instancia["caixas_do_cliente"]
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    file = caminho + '/' + name + '_caixas_do_cliente.dot'

    arq = open(file, 'w')
    arq.write('strict graph {\n')
    arq.write('rankdir = LR;\n')
    for i in range(len(prop)-1):
        cliente = str(i) + ' [label = "Cliente ' + str(i) + '"];\n'
        arq.write(cliente)
        for j in range(len(prop[i])):
            if prop[i][j] == 1:
                caixa = str(str(i)
                            + str(j)
                            + ' [label = "Caixa '
                            + str(j)
                            + '", shape=box];\n')
                arq.write(caixa)
                arq.write(str(i) + '--' + str(i) + str(j) + ' ;\n')
    arq.write('}')
    arq.close()
    #print("\nVerificar '.dot' arquivo de saída.\n")
    
    os.chdir('OUTPUT')
    os.system('dot ' + name + '_caixas_do_cliente.dot -Tpng -o' + name + '_caixas_do_cliente.png')
    os.chdir('..')
    #print("\nVerificar arquivo '.png' de saída.\n")

###############################################################################

###############################################################################

def grafo_solucao_pcv(dic_instancia, solucao_pcv):
    """ Esta funcao cria um grafo com os arcos da matriz distancia
        com enfase na viagem mais curta (solucao do problema do caixeiro
        viajante) que pode ser feita.
    """
    
    caminho = 'OUTPUT'
    name = dic_instancia["nome_instancia"]
    distancia = dic_instancia["distancia"]
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    file = caminho + '/' + name + '_solucao_pcv.dot'
    #abro um arquivo '.dot' para linguagem graphviz
    arq = open(file, 'w')
    #primeira linha como padrao da linguagem
    arq.write('strict graph {\n')


    for i in range(len(distancia)-1):
        for j in range(i, len(distancia[i])-1):
            #ignoro as distancias entre si mesmos e as 'infinitas' ditas '9999'
            if i != j:
                if i == 0 and j == solucao_pcv[len(solucao_pcv)-2]:
                    arq.write(str(i)
                              +'--'
                              + str(j)
                              + ' [label =  "'
                              + "%.3f" %distancia[0][solucao_pcv[len(solucao_pcv)-2]]
                              + 'km"];\n')
                elif j == solucao_pcv[solucao_pcv.index(i)+1]:
                    arq.write(str(i)
                              + '--'
                              + str(j)
                              + ' [label =  "'
                              + "%.3f" %distancia[i][j]
                              + 'km"];\n')
                elif j == solucao_pcv[solucao_pcv.index(i)-1]:
                    arq.write(str(i)
                              + '--'
                              + str(j)
                              + ' [label = "'
                              + "%.3f" %distancia[i][j]
                              + 'km"];\n')
                else:
                    #aresta como vertice os indices da matriz distancia
                    arq.write(str(i) + '--' + str(j) + ' [color=grey];\n')
            
    arq.write('}')
    arq.close()
    #print("\nVerificar arquivo '.dot' de saída.\n")
    
    os.chdir('OUTPUT')
    os.system('dot ' + name + '_solucao_pcv.dot -Tpng -o' + name + '_solucao_pcv.png')
    #os.system('dot -Kfdp -n -Tpng -o '
     #         + name + '_solucao_pcv.png '
      #        + name + '_solucao_pcv.dot')
    os.chdir('..')
    #print("\nVerificar arquivo '.png' de saída.\n")

    # codigo acima equivale a execucao no terminal:
    # -> dot nomedoarquivo.dot -Tpng -o nomedografo.png
