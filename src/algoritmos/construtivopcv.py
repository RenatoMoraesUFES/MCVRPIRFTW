def pcv(dic_instancia):
    """ Esta funcao ira resolver o problema do caixeiro
        viajante tendo como entrada as matrizes de distancia
        do problema MCVRPIRFTW interpretando as distancias do
        arco ij como o custo da viagem.
    """

    copia_dist= []
    for linha in range(len(dic_instancia["distancia"])):
        copia_linha = []
        for item in dic_instancia["distancia"][linha]:
            copia_linha.append(item)
        copia_dist.append(copia_linha) #faco uma copia da matriz distancia para fazer alteracoes futuras
    
    H = [0]  #H recebe os indices dos nós já na solução (inicia em 0, que é o armz central)
    L = 0    #L recebe o custo total da viagem até o momento
    #N recebe os nós que ainda não estão na solucao, lenght de distancia tem o -1 para ignorar o armazem virtual
    N = list(range(1, len(copia_dist)-1)) #o zero já inicia fora pois já é parte da solucao em H
    i = 0  #indice do nó corrente
    
    while N != []:
        #obter o menor valor dos arcos que saem de i para j
        valor_j = min(copia_dist[i][:-1]) #removi o ultimo elemento que se refere ao armazem central virtual
        j = copia_dist[i][:-1].index(valor_j) #acho o indice de j
        for k in range(0, len(copia_dist)-1): #faco os nos ja visitados nao aparecerem nos minimos novamente
            copia_dist[k][j] = 9999
        H.append(j)
        if valor_j != 9999:
            L += valor_j
        if j in N:
            N.remove(j)
        i = j
    if H[len(H)-1] != 0:
        H.append(0)
    L += copia_dist[i][len(copia_dist)-1]
    
    return H, L
