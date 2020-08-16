def construtivo(dic_instancia):
    """ Esta função lê o dicionário da instância de entrada e
        retorna a solução final do problema MCVRPIRFTW que
        pretende encontrar uma rota com o menor custo possível
        em que uma bicicleta com multiplos compartimentos,
        convencional ou elétrica, saia do armazém central,
        vá até os clientes e reabasteça em armazéns intermediários
        respeitando uma janela de tempo.
    """
    ################################################################
    #busco a matriz distancia no dicionario de entrada para facilitar o nome da variável
    distancia = dic_instancia["distancia"]
    #busco a matriz que tem qual caixa pertence a qual cliente
    prop = dic_instancia["caixas_do_cliente"]
    #busco também os volumes de cada caixa dos clientes
    volume_caixa = dic_instancia["volume_caixa"]
    #busco volume máximo dos compartimentos das bicicletas
    volume_maximo = 100
    #busco o numero de facilidades na instancia
    nosf = dic_instancia["facilidades"]
    ################################################################

    ################################################################
    #Loop para percorrer qual caixa pertence a qual cliente
    #E sua respectiva soma de volumes de caixas
    #Para atender a restrição de que cada cliente é visitado
    #uma unica vez por um unico veiculo
    volumes_totais = []
    for i in range(len(prop)):
        volume = 0
        for j in range(len(prop[i])):
            if prop[i][j] == 1:
                volume += volume_caixa[j]
        volumes_totais.append(volume)
    #print(volumes_totais)
    ################################################################

    ################################################################
    #crio uma matriz para salvar as economias feitas ao colocar
    #os arcos i e j na mesma rota
    economia = []
    dic_economia = {}
    
    #crio um laço para percorrer todas distancias entre os arcos i e j
    #e descobrir as maiores economias entre os nós
    for i in range(1, len(distancia)-1-nosf):
        for j in range(i, len(distancia)-1-nosf):
            if i != j and distancia[i][j] != 9999:
                saving = (distancia[0][i]
                          +distancia[0][j]
                          -distancia[i][j])
                economia.append(saving)
                dic_economia[str(saving)] = str(i) + str(j)
    economia.sort(reverse=True)

    print(dic_instancia["nome_instancia"])
    #print(dic_economia)
    #print(economia)
    #print(dic_economia[str(economia[0])])
    ################################################################

    ################################################################
    #uno as rotas de maior economia
    rota = []
    custo = 0
    volume_atual = 0
    cliente_i = int(dic_economia[str(economia[0])][0])  
    cliente_j = int(dic_economia[str(economia[0])][1])
    for i in range(1, len(economia)):
        if volume_atual + volumes_totais[cliente_i-1] <= volume_maximo:
            volume_atual += volumes_totais[cliente_i-1]
            if not cliente_i in rota:
                rota.append(cliente_i)
        if volume_atual + volumes_totais[cliente_j-1] <= volume_maximo:
            if not cliente_j in rota:
                volume_atual += volumes_totais[cliente_j-1]
                rota.append(cliente_j)
        cliente_i = int(dic_economia[str(economia[i])][0])
        cliente_j = int(dic_economia[str(economia[i])][1])
        if cliente_i in rota:
            if volume_atual + volumes_totais[cliente_j-1] <= volume_maximo:
                if not cliente_j in rota:
                    volume_atual += volumes_totais[cliente_j-1]
                    rota.append(cliente_j)
        if cliente_j in rota:
            if volume_atual + volumes_totais[cliente_i-1] <= volume_maximo:
                if not cliente_i in rota:
                    volume_atual += volumes_totais[cliente_i-1]
                    rota.append(cliente_i)
    
    
    rota.insert(0, 0)
    rota.append(0)
    print(rota)

    for i in range(len(rota)-2):
        custo += distancia[rota[i]][rota[i+1]]
    custo += distancia[rota[-2]][-1]
    print(custo)



    
