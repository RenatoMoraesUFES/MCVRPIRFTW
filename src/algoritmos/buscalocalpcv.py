def bl_perm(dic_instancia, solucao_pcv, custo_pcv):
    distancia = dic_instancia["distancia"]
    melhor_solucao = solucao_pcv
    melhor_custo = custo_pcv
    melhoria = True
    while melhoria:
        melhoria = False
        for i in range(1, len(solucao_pcv)-2):
            solucao_atual = solucao_pcv[:]
            aux = solucao_atual[i]
            solucao_atual[i] = solucao_atual[i+1]
            solucao_atual[i+1] = aux
            print(i)
            print("atual: ", solucao_atual)
            print("pcv: ", solucao_pcv)
            novo_custo = (custo_pcv - distancia[solucao_pcv[i-1]][solucao_pcv[i]]
                                    - distancia[solucao_pcv[i+1]][solucao_pcv[i+2]]
                                    + distancia[solucao_atual[i-1]][solucao_atual[i]]
                                    + distancia[solucao_atual[i+1]][solucao_atual[i+2]])
            print('novo custo: ', novo_custo)          
            if novo_custo < melhor_custo:
                melhor_custo = novo_custo
                melhor_solucao = solucao_atual
            solucao_atual = []
        if melhor_custo < custo_pcv:
            solucao_pcv = melhor_solucao
            melhoria = True
