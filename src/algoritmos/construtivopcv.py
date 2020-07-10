def pcv(dic_instancia):
    #complexidade de tempo: O(n²)
    """ Esta funcao ira resolver o problema do caixeiro
    viajante tendo como entrada as matrizes de distancia
    do problema MCVRPIRFTW interpretando as distancias do
    arco ij como o custo da viagem.
    """

    N = len(dic_instancia["distancia"]) #numero de nós no grafo
    visitados = [True] + (N-1)*[False] #vetor de visitados, False se ainda não foi visitado
    rota, custo = [0], 0.0
    N -= 2 # desconto o armazem central e o central virtual
    i = 0 #armazem central inicial

    while N > 0:
        min_j = 9999 #menor distância até agora
        j = 0 #nó mais próximo
        for k in range(0, len(dic_instancia["distancia"])-1): # pego o nó mais próximo que ainda não foi visitado
            if dic_instancia["distancia"][i][k] < min_j and not visitados[k]:
                j, min_j = k, dic_instancia["distancia"][i][k]
        custo += min_j 
        rota += [j]
        visitados[j] = True
        N -= 1
        i = j
        
    rota += [0]
    custo += dic_instancia["distancia"][i][-1] #armazem central virtual, fim da rota
    return rota, custo
    