
###############################################################################

def ConstrutivoMenorDistancia(dic_instancia,configuracoes):
    """ Funcao que calcula uma solução viável para o problema do caixeiro viajante considerando
    como entrada a mareix de distancias do dicionario da instancia passado como parâmentro
    """
    #print(dic_instancia, end='\n\n\n')
    
    C = dic_instancia["distancia"]
    print("C = ", C)
    N = list(range(0,len(C)-1))
    print("N = ",N,"\n")
    H = [0]
    print("H = ",H)
    L = 0
    print("L = ", L)
    N.remove(0)
    print("N = ",N)
    i = 0
    print("i =", i, "\n")
    
    while(N != []):
        distancias_correntes = C[i]
        print("DC = ",distancias_correntes)
        dist_min = min(distancias_correntes)
        min_pos = distancias_correntes.index(dist_min) # pega a posição do valor da distancia minima
        while(min_pos in H):
            distancias_correntes[min_pos] = distancias_correntes[min_pos] + 9999
            print("DC = ",distancias_correntes)
            dist_min = min(distancias_correntes)
            min_pos = distancias_correntes.index(dist_min) # pega a posição do valor da distancia minima					
        print("dist_min =", dist_min)
        print("min_pos =", min_pos)
        #### próximas duas linhas só existem para poder pegar a cidade com maior indice em caso de empate
        #### e assim reproduzir fielmente o exemplo dos slides
        ultima_ocorrencia = [j for j,val in enumerate(distancias_correntes) if val==dist_min]
        print("ultima_ocorrencia =", ultima_ocorrencia)
        ####
        min_pos = ultima_ocorrencia[len(ultima_ocorrencia)-1]
        H.append(min_pos)
        L = L + dist_min
        N.remove(min_pos)
        i = min_pos
        print("H = ",H)
        print("L = ", L)
        print("N = ",N)
        print("i =", i, "\n")
    distancias_correntes = C[i]
    print("DC = ",distancias_correntes)
    L = L + distancias_correntes[0]  #### fixamos a origem como a cidade 0, voltar para a origem
    print("H = ",H)
    print("L = ", L)
    
       
    
    return dic_instancia
    #
#fim ConstrutivoMenorDistancia(dic_instancia,configuracoes)
##############################################################################
