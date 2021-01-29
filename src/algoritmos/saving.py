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
    #busco a matriz dos tempos para percorrer os arcos i,j
    tempo = dic_instancia["tempo"]
    jti = dic_instancia["janela_cliente_inicio"]
    jtf = dic_instancia["janela_cliente_fim"]
    ot = dic_instancia["tempo_operacao_caixa"]
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
    #print("Volumes totais por cliente = ", volumes_totais)
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
    #print("Economias")
    #for linha in economia:
    #    print(linha)
    #print('\n')

    ################################################################

    rotas = []
    volume = []
    janela_tempo = []
    for i in range(1, len(distancia)-1-nosf):
        rotas.append([i])
        volume.append(volumes_totais[i-1])
        janela_tempo.append(tempo[0][i])
        
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

    def verifica_tempo(i, j, rotas, tempo, janela_tempo, jti, jtf, ot):
        tempo_gasto_i = 0
        tempo_gasto_j = 0
        for rota in rotas:
            print(rota)
            if i in rota:
                tempo_gasto_i += tempo[0][rota[0]]
                #tempo_gasto_i += tempo[rota[-1]][-1]
                if len(rota) > 1:
                    for cliente in range(len(rota)-1):
                        tempo_gasto_i += tempo[cliente][cliente+1]
            if j in rota:
                #tempo_gasto_j += tempo[0][rota[0]]
                tempo_gasto_j += tempo[rota[-1]][-1]
                if len(rota) > 1:
                    for cliente in range(len(rota)-1):
                        tempo_gasto_j += tempo[cliente][cliente+1]
        if (tempo_gasto_j + tempo_gasto_i) <= jtf[j]:
            return True
        return False

    ################################################################

    def define_dic_trecho(lista_trechos):

        lista_dic_trecho = []
        cont = 0
        
        for rota_corrente in lista_trechos:
            for trecho_corrente in rota_corrente:
                qual_rota = lista_trechos.index(rota_corrente)
                posicao_na_rota = rota_corrente.index(trecho_corrente)
                
                t = trecho_corrente
                
                origem_destino = t

               
                demanda = 0
                for i in range(posicao_na_rota, len(lista_trechos[qual_rota])):
                    if lista_trechos[qual_rota][i][1] != 0:
                        demanda += volumes_totais[lista_trechos[qual_rota][i][1]-1]

                
                if t[1] == 0:
                    custo = distancia[t[0]][-1]
                else:
                    custo = distancia[t[0]][t[1]]


                if t[0] == 0:
                    janela_tempo = (0, tempo[0][t[1]])
                elif t[1] == 0:
                    aux = lista_dic_trecho[cont-1]['janela_tempo'][0][1]
                    janela_tempo = (aux, aux + tempo[t[0]][-1])
                else:
                    aux = lista_dic_trecho[cont-1]['janela_tempo'][0][1]
                    janela_tempo = (aux, aux + tempo[t[0]][t[1]])
                       
                
                dic_trecho = {
                    'rota'              : [qual_rota],
                    'posicao_na_rota'   : [posicao_na_rota],
                    'origem_destino'    : [origem_destino],
                    'demanda'           : [demanda],
                    'custo'             : [custo],
                    'janela_tempo'      : [janela_tempo]
                    }

                lista_dic_trecho.append(dic_trecho)
                cont+=1

                print(dic_trecho)

        return dic_trecho
    
    ################################################################

    def mesclar_rotas(i, j, rotas, volume, janela_tempo):
       
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
        tempo_r = janela_tempo[pos_r]
        tempo_s = janela_tempo[pos_s]        


        rotas.remove(r)
        rotas.remove(s)
        if r[0] == j and s[0] == i:
            r.reverse()
            rotas.append(r+s)
        elif r[-1] == j and s[-1] == i:
            s.reverse()
            rotas.append(r+s)
        elif r[0] == j and s[-1] == i:
            rotas.append(s+r)
        elif r[-1] == j and s[0] == i:
            rotas.append(r+s)

        
        janela_tempo.append(tempo_r
                            +tempo_s)
        janela_tempo.remove(tempo_r)
        janela_tempo.remove(tempo_s)

        
        volume.append(volume_r
                     +volume_s)
        volume.remove(volume_r)
        volume.remove(volume_s)

        

    ################################################################
        
    ################################################################

    def paralelo(economia, rotas, volumes_totais, volume_maximo, volume):
        #print("Inicio JT: ", jti)
        #print("Fim JT: ", jtf)
        #print("Volume máximo: ", volume_maximo)
        for i in range(len(economia)):
            cliente_i = economia[i][1][0]
            cliente_j = economia[i][1][1]
            #print(f"Rotas : {rotas}")
            #print(f"Tempos das rotas: {janela_tempo}")
            #print(f"Demandas das rotas: {volume}\n")
            #print(f"Clientes {cliente_i} e {cliente_j}")
            if verifica_rota(cliente_i, cliente_j, rotas):
                #print("Rota verificada")
                if verifica_capacidade(cliente_i, cliente_j, volume_maximo, volumes_totais, rotas, volume):
                    #print("Capacidade verificada")
                    if verifica_tempo(cliente_i, cliente_j, rotas, tempo, janela_tempo, jti, jtf, ot):
                        #print("Janela de tempo verificada")
                        mesclar_rotas(cliente_i, cliente_j, rotas, volume, janela_tempo)
                        #print("Mesclar rotas\n")
                    #else:
                        #print("Janela de tempo excedida\n")
                #else:
                    #print("Capacidade excedida\n")
            #else:
                #print("Rota não verificada")


        ###INSERE OS ARMAZENS NAS ROTAS (NO INICIO E FIM)###
        for rota in rotas:
            if 0 not in rota:
                rota.insert(0, 0)
                rota.append(0)

        ###TRANSFORMA A ROTA (LISTA) EM UMA LISTA DE TRECHO###
        lista_trechos = []
        for rota in rotas:
            aux = []
            for i in range(len(rota)-1):
                aux.append((rota[i], rota[i+1]))
            lista_trechos.append(aux)
        
        ###CALCULA CUSTO DA ROTA###        
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

        ###PERCORRE LISTA DE TRECHOS E CRIA O DICIONARIO###
        define_dic_trecho(lista_trechos)
        
                                         
        dic_solucao = {
            'caminho'       : rotas,
            'volume'        : volume,
            'custo'         : custo,
            'janela_tempo'  : janela_tempo
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
                            #if verifica_tempo(cliente_i, cliente_j, rotas, tempo, janela_tempo, jti, jtf, ot):
                            mesclar_rotas(cliente_i, cliente_j, rotas, volume, janela_tempo)
                            rota_corrente = rotas[-1]
                            #print(rota_corrente, rotas)
                            conseguiu_mesclar_rotas = True
                else:
                    if cliente_i in rota_corrente or cliente_j in rota_corrente:
                        if verifica_rota(cliente_i, cliente_j, rotas):
                            if verifica_capacidade(cliente_i, cliente_j, volume_maximo, volumes_totais, rotas, volume):
                                #if verifica_tempo(cliente_i, cliente_j, rotas, tempo, janela_tempo, jti, jtf, ot):
                                mesclar_rotas(cliente_i, cliente_j, rotas, volume, janela_tempo)
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
            'caminho'       : rotas,
            'volume'        : volume,
            'custo'         : custo,
            'janela_tempo'  : janela_tempo
            }


        return dic_solucao

    #################################################################
                                             
    return paralelo(economia, rotas, volumes_totais, volume_maximo, volume)
    #return sequencial(economia, rotas, volumes_totais, volume_maximo, volume)
