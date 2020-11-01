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
    for i in range(len(prop)-1-nosf):
        volume = 0
        for j in range(len(prop[i])):
            if prop[i][j] == 1:
                volume += volume_caixa[j]
        volumes_totais.append(volume)
    print("Volumes totais por cliente = ", volumes_totais)
    ################################################################

    ################################################################
    #crio uma matriz para salvar as economias feitas ao colocar
    #os arcos i e j na mesma rota
    economia = []
    
    #crio um laço para percorrer todas distancias entre os arcos i e j
    #e descobrir as maiores economias entre os nós
    for i in range(1, len(distancia)-1-nosf):
        for j in range(i, len(distancia)-1-nosf):
            if i != j and distancia[i][j] != 9999:
                saving = (distancia[0][i]
                          +distancia[0][j]
                          -distancia[i][j])
                economia.append((saving,[i,j]))
    economia.sort(reverse=True)
    #for linha in economia:
    #    print(linha)
    #print('\n')

    ################################################################

    rotas = []
    volume = []
    for i in range(1, len(distancia)-1-nosf):
        rotas.append([i])
        volume.append(volumes_totais[i-1])
        
    ################################################################

    def verifica_rota(i, j, rotas):
        r, s = [], []
        for rota in rotas:
            if rota[0] == j:
                r = rota
            elif rota[-1] == i:
                s = rota

            if r and s:
                return True

        return False

    ################################################################
    
    def verifica_capacidade(i, j, volume_maximo, volumes_totais, rotas, volume):
        for rota in rotas:
            if i in rota:
                pos_i = rotas.index(rota)
            if j in rota:
                pos_j= rotas.index(rota)
        if (volume[pos_i] + volume[pos_j]) <= volume_maximo:
            return True
        return False
        
    ################################################################

    def mesclar_rotas(i, j, rotas, volume):
        '''
        r, s = [], []
        for rota in rotas:
            if rota[0] == j:
                r = rota
            elif rota[-1] == i:
                s = rota
        '''

        r, s = [], []
        for rota in rotas:
            if j in rota:
                r = rota
            elif i in rota:
                s = rota
        
        pos_r = rotas.index(r)
        pos_s = rotas.index(s)
        volume_r = volume[pos_r]
        volume_s = volume[pos_s]


        if r[0] == j and s[0] == i:
            rotas.remove(r)
            rotas.remove(s)
            r.reverse()
            rotas.append(r+s)
        elif r[-1] == j and s[-1] == i:
            rotas.remove(r)
            rotas.remove(s)
            s.reverse()
            rotas.append(r+s)
        elif r[0] == j and s[-1] == i:
            rotas.remove(r)
            rotas.remove(s)
            rotas.append(s+r)
        elif r[-1] == j and s[0] == i:
            rotas.remove(r)
            rotas.remove(s)
            rotas.append(r+s)
            

        
        #rotas.remove(r)
        #rotas.remove(s)
        #rotas.append(r+s)
        volume.append(volume_r
                     +volume_s)
        volume.remove(volume_r)
        volume.remove(volume_s)
        
        

    ################################################################
        
    ################################################################

    def paralelo(economia, rotas, volumes_totais, volume_maximo, volume):
    
        for i in range(len(economia)):
            cliente_i = economia[i][1][0]
            cliente_j = economia[i][1][1]
            if verifica_rota(cliente_i, cliente_j, rotas):
                if verifica_capacidade(cliente_i, cliente_j, volume_maximo, volumes_totais, rotas, volume):
                    mesclar_rotas(cliente_i, cliente_j, rotas, volume)

        for rota in rotas:
            if 0 not in rota:
                rota.insert(0, 0)
                rota.append(0)
                
        custo = []
        for rota in rotas:
            custo_corrente = 0
            for i in range(len(rota)-2):
                custo_corrente += distancia[rota[i]][rota[i+1]]
            custo_corrente += distancia[rota[-2]][-1]
            custo.append(custo_corrente)
        soma = 0
        for item in custo:
            soma +=item
        custo.append(soma)

        dic_solucao = {
            'caminho'   : rotas,
            'volume'    : volume,
            'custo'     : custo
            }
    

        return dic_solucao
    
    ################################################################

    ################################################################

    def sequencial(economia, rotas, volumes_totais, volume_maximo, volume):
        
        conseguiu_mesclar_rotas = True
        while conseguiu_mesclar_rotas:
            conseguiu_mesclar_rotas = False
            rota_corrente = []
            #print(len(economia))
            for i in range(len(economia)):
                #print(i)
                cliente_i = economia[i][1][0]
                cliente_j = economia[i][1][1]
                
                if rota_corrente == []:
                    if verifica_rota(cliente_i, cliente_j, rotas):
                        if verifica_capacidade(cliente_i, cliente_j, volume_maximo, volumes_totais, rotas, volume):
                            mesclar_rotas(cliente_i, cliente_j, rotas, volume)
                            rota_corrente = rotas[-1]
                            #print(rota_corrente, rotas)
                            conseguiu_mesclar_rotas = True
                else:
                    if cliente_i in rota_corrente or cliente_j in rota_corrente:
                        if verifica_rota(cliente_i, cliente_j, rotas):
                            if verifica_capacidade(cliente_i, cliente_j, volume_maximo, volumes_totais, rotas, volume):
                                mesclar_rotas(cliente_i, cliente_j, rotas, volume)
                                #print(rota_corrente, rotas)
                                rota_corrente = rotas[-1]
                                conseguiu_mesclar_rotas = True

        for rota in rotas:
            if 0 not in rota:
                rota.insert(0, 0)
                rota.append(0)
                
        custo = []
        for rota in rotas:
            custo_corrente = 0
            for i in range(len(rota)-2):
                custo_corrente += distancia[rota[i]][rota[i+1]]
            custo_corrente += distancia[rota[-2]][-1]
            custo.append(custo_corrente)
        soma = 0
        for item in custo:
            soma +=item
        custo.append(soma)

        dic_solucao = {
            'caminho'   : rotas,
            'volume'    : volume,
            'custo'     : custo
            }


        return dic_solucao

    #################################################################
                                             
    #return paralelo(economia, rotas, volumes_totais, volume_maximo, volume)
    return sequencial(economia, rotas, volumes_totais, volume_maximo, volume)
