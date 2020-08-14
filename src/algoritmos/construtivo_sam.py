def construtivo(dic_instancia, solucao_bl2, custo_bl2):
    """ Esta função lê o dicionário da instância de entrada e
        retorna a solução final do problema MCVRPIRFTW que
        pretende encontrar uma rota com o menor custo possível
        em que uma bicicleta com multiplos compartimentos,
        convencional ou elétrica, saia do armazém central,
        vá até os clientes e reabasteça em armazéns intermediários
        respeitando uma janela de tempo.
    """

    #busco a matriz distancia no dicionario de entrada para facilitar o nome da variável
    distancia = dic_instancia["distancia"]
    #busco a matriz que tem qual caixa pertence a qual cliente
    #faco uma copia para fazer alteracoes futuras
    copia_prop= []
    for linha in range(len(dic_instancia["caixas_do_cliente"])):
        copia_linha = []
        for item in dic_instancia["caixas_do_cliente"][linha]:
            copia_linha.append(item)
        copia_prop.append(copia_linha)
    #busco também os volumes de cada caixa dos clientes
    volume_caixa = dic_instancia["volume_caixa"]
    #busco volume máximo dos compartimentos das bicicletas
    volume_maximo = 20
    #busco o numero de facilidades na instancia
    nosf = dic_instancia["facilidades"]

    volume = 0
    novo_custo = custo_bl2
    for cliente in range(1, len(solucao_bl2)):
        for caixa in range(len(copia_prop[solucao_bl2[cliente]])):
            if copia_prop[solucao_bl2[cliente]][caixa] == 1:
                volume += volume_caixa[caixa]
            if volume >= volume_maximo:
                solucao_bl2.insert(cliente+1, len(distancia)-3)
                volume = 0
                novo_custo = (novo_custo
                              -distancia[cliente][cliente+1]
                              +distancia[cliente][-2]
                              +distancia[cliente+1][-2])
    print(solucao_bl2)
    print(novo_custo)
                              
    """
    #crio uma matriz para salvar as economias feitas ao colocar
    #os arcos i e j na mesma rota
    economia = []
    
    #crio um laço para percorrer todas distancias entre os arcos i e j
    #e descobrir as maiores economias entre os nós
    for i in range(1, len(distancia)-1-nosf):
        economias_i = []
        for j in range(i, len(distancia)-1-nosf):
            if i != j and distancia[i][j] != 9999:
                saving = (distancia[0][i]
                          +distancia[0][j]
                          -distancia[i][j])
                economias_i.append(saving)
        economia.append(economias_i)

    #busco a maior economia entre os nós i e j da matriz economia
    rota = []
    for linha in economia:
        maior_economia = 0
        for item in linha:
            if item > maior_economia:
                maior_economia = item
                i = economia.index(linha) + 1
                j = linha.index(item) + i + 1

    #a partir da matriz das economias crio rotas dois a dois com as
    #maiores economias de cada linha
        volume = 0
        nova_rota = [0]
        for x in range(len(copia_prop[i-1])):
            if copia_prop[i-1][x] == 1:
                if volume + volume_caixa[x] < volume_maximo:
                    volume += volume_caixa[x]
                    copia_prop[i-1][x] = 0
        if volume < volume_maximo:
            nova_rota.append(i)
            for y in range(len(copia_prop[j-1])):
                if copia_prop[j-1][y] == 1:
                    if volume + volume_caixa[y] < volume_maximo:
                        volume += volume_caixa[y]
                        copia_prop[j-1][y] = 0
            if volume < volume_maximo:
                nova_rota.append(j)
            elif volume == volume_maximo:
                nova_rota.append(j)
                nova_rota.append(0)
                if nova_rota not in rota:
                    rota.append(nova_rota)
                continue
            elif volume >= volume_maximo:
                nova_rota.append(0)
                if nova_rota not in rota:
                    rota.append(nova_rota)
                continue
            nova_rota.append(0)
            if nova_rota not in rota:
                rota.append(nova_rota)
        elif volume == volume_maximo:
            nova_rota.append(i)
            nova_rota.append(0)
            if nova_rota not in rota:
                rota.append(nova_rota)
            continue
        elif volume >= volume_maximo:
            nova_rota.append(0)
            if nova_rota not in rota:
                rota.append(nova_rota)
            continue
    print(rota)
    
    #procuro juntar todas as rotas respeitando o volume máximo
    join = rota[0][:-1]
    for i in range (len(rota)):
        for j in range(i, len(rota)):
            if join[i+2] == rota[j][1]:
                if rota[j][1] not in join:
                    join.append(rota[j][1])
                if rota[j][2] not in join:
                    join.append(rota[j][2])
            elif join[i+2] == rota[j][2]:
                if rota[j][2] not in join:
                    join.append(rota[j][2])
                if rota[j][1] not in join:
                    join.append(rota[j][1])
    join.append(0)  
    print(join)

    
    print(dic_instancia["nome_instancia"])
    for linha in economia:
        for item in linha:
            print(" %.2f " %item, end='')
        print("\n")
        """
    
            
            
