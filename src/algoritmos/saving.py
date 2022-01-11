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
    matriz_tempo = dic_instancia["tempo"]
    jti = dic_instancia["janela_cliente_inicio"]
    jtf = dic_instancia["janela_cliente_fim"]
    ot = dic_instancia["tempo_operacao_caixa"]
    #busco também os volumes de cada caixa dos clientes
    volume_caixa = dic_instancia["volume_caixa"]
    #busco volume máximo dos compartimentos das bicicletas
    volume_maximo = 50
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
        janela_tempo.append((jti[i], jtf[i]))
    #print("rotas ", rotas, "\nvolume ", volume, "\njanela_tempo" , janela_tempo)
        
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

    def verifica_tempo(i, j, rotas, matriz_tempo, janela_tempo, jti, jtf, ot):
        tempo_gasto_i = 0
        tempo_gasto_j = 0
        for rota in rotas:
            #print(rota)
            if i in rota:
                tempo_gasto_i += matriz_tempo[0][rota[0]]
                #tempo_gasto_i += matriz_tempo[rota[-1]][-1]
                if len(rota) > 1:
                    for cliente in range(len(rota)-1):
                        tempo_gasto_i += matriz_tempo[cliente][cliente+1]
            if j in rota:
                #tempo_gasto_j += matriz_tempo[0][rota[0]]
                tempo_gasto_j += matriz_tempo[rota[-1]][-1]
                if len(rota) > 1:
                    for cliente in range(len(rota)-1):
                        tempo_gasto_j += matriz_tempo[cliente][cliente+1]
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
                    janela_tempo = (0, matriz_tempo[0][t[1]])
                elif t[1] == 0:
                    aux = lista_dic_trecho[cont-1]['janela_tempo'][0][1]
                    janela_tempo = (aux, aux + matriz_tempo[t[0]][-1])
                else:
                    aux = lista_dic_trecho[cont-1]['janela_tempo'][0][1]
                    janela_tempo = (aux, aux + matriz_tempo[t[0]][t[1]])
                       
                
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

                #print(dic_trecho)

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
                    #if verifica_tempo(cliente_i, cliente_j, rotas, tempo, janela_tempo, jti, jtf, ot):
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
        custo_logistico = 200*len(rotas)
        custo_km = 0.4*soma

        
        volume_corrente = []
        for item in volume:
            volume_corrente.append([item])
        #print("R: ", R)
        for rota in rotas:
            for cliente in rota[1:-1]:
                volume_corrente[rotas.index(rota)].append(volume_corrente[rotas.index(rota)][len(volume_corrente[rotas.index(rota)])-1]
                                                -volumes_totais[cliente-1])

        volume_todas_rotas = []
        for rota in rotas:
            volume_da_rota = 0
            for cliente in rota[1:-1]:
                volume_da_rota += volumes_totais[cliente-1]
            volume_todas_rotas.append(volume_da_rota)

        utilizacao = []
        for i in range(len(volume_todas_rotas)):
            utilizacao.append((volume_todas_rotas[i]/volume_maximo)*100)
        util_media = 0
        for x in utilizacao:
            util_media += x
        util_media = util_media/len(utilizacao)
        

        ###PERCORRE LISTA DE TRECHOS E CRIA O DICIONARIO###
                                                 
        dic_solucao = {
            'Instancia'             : dic_instancia["nome_instancia"],
            'Caminho'               : rotas,
            'Volume'                : volume,
            'Volume Corrente'       : volume_corrente,
            'Volume Maximo'         : volume_maximo,
            'Distancia Percorrida'  : custo,
            'Custo Logistico'       : custo_logistico,
            'Custo KM'              : custo_km,
            'Quantidade de Veiculos': len(rotas),
            'Utilizacao Media'      : util_media
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
                            #if verifica_tempo(cliente_i, cliente_j, rotas, matriz_tempo, janela_tempo, jti, jtf, ot):
                            mesclar_rotas(cliente_i, cliente_j, rotas, volume, janela_tempo)
                            rota_corrente = rotas[-1]
                            #print(rota_corrente, rotas)
                            conseguiu_mesclar_rotas = True
                else:
                    if cliente_i in rota_corrente or cliente_j in rota_corrente:
                        if verifica_rota(cliente_i, cliente_j, rotas):
                            if verifica_capacidade(cliente_i, cliente_j, volume_maximo, volumes_totais, rotas, volume):
                                #if verifica_tempo(cliente_i, cliente_j, rotas, matriz_tempo, janela_tempo, jti, jtf, ot):
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

    def calcula_custo_inserir(u, arco, rota_corrente):
        #Parametro a1 dá prioridade para os custos de distancia
        a1 = 0.5
        #Parametro a2 dá prioridade para os custos de tempo
        a2 = 0.5
        #print("u: ", u, "\narco: ", arco, "\nrota corrente: ", rota_corrente)

        
        c11 = (distancia[arco[0]][u]    
               + distancia[u][arco[1]]
               - distancia[arco[0]][arco[1]])
        
        #tempo de inicio do servico em j+1 do arco (j,j+1), ou seja, em arco[1]
        if arco[1] == 0:
            posicao_j = len(rota_corrente)-1
        else:
            posicao_j = rota_corrente.index(arco[1])
        bj = 0
        for i in range(posicao_j):
            if rota_corrente[i] == 0:                
                if rota_corrente[i+1] == 0:
                    bj += matriz_tempo[rota_corrente[i]][-1]
                else:
                    bj += matriz_tempo[rota_corrente[i]][rota_corrente[i+1]]
            else:
                if rota_corrente[i+1] == 0:
                    bj += matriz_tempo[rota_corrente[i]][-1] + ot
                else:
                    bj += matriz_tempo[rota_corrente[i]][rota_corrente[i+1]] + ot
            if bj < jti[rota_corrente[i+1]]:
                bj = jti[rota_corrente[i+1]]
        
        # tempo de inicio do servico em j+1 com a inserção de u
        posicao_inserir = rota_corrente.index(arco[0])
        rota_corrente.insert(posicao_inserir + 1, u)
        if arco[1] == 0:
            posicao_j = len(rota_corrente)-1
        else:
            posicao_j = rota_corrente.index(arco[1])
        bju = 0
        for i in range(posicao_j):
            if rota_corrente[i] == 0:                
                if rota_corrente[i+1] == 0:
                    bju += matriz_tempo[rota_corrente[i]][-1]
                else:
                    bju += matriz_tempo[rota_corrente[i]][rota_corrente[i+1]]
            else:
                if rota_corrente[i+1] == 0:
                    bju += matriz_tempo[rota_corrente[i]][-1] + ot
                else:
                    bju += matriz_tempo[rota_corrente[i]][rota_corrente[i+1]] + ot
            if bju < jti[rota_corrente[i+1]]:
                bju = jti[rota_corrente[i+1]]
        rota_corrente.remove(u)        

        c12 = bju - bj

        c1 = a1*c11 + a2*c12

        c2 = distancia[0][u] - c1

        return c2

    def inserir_u_em_rota(u, arco, rota_corrente):
        #print("u: ", u, "\narco: ", arco, "\nrota corrente: ", rota_corrente)
        posicao_j = rota_corrente.index(arco[0])
        #print("posicao j: ", posicao_j)
        rota_corrente.insert(posicao_j + 1, u)
        #print(rota_corrente)
        pass

    def testa_viabilidade(u, arco, rota_corrente, volume, volume_maximo, jti, jtf, matriz_tempo):
        #print("\nTestando viabilidade...\n")
        #print("Entradas: ", "\nu: ", u, "\narco: ", arco, "\nrota corrente: ", rota_corrente)
        #print("volume: ", volume, "\nvolume_max: ", volume_maximo)
        #print("(jti, jtf): ", (jti, jtf), "\nmatriz tempo: ", matriz_tempo)

        ###### TESTE DE CAPACIDADE ######
        demanda = 0
        # FOR percorre a rota_corrente excluindo o armazem no inicio e no fim
        for cliente in rota_corrente[1:-1]:
            demanda += volume[cliente-1]
        demanda += volume[u-1]
        #print("Nova demanda com a inserção: ", demanda)
        #print("Volume máximo: ", volume_maximo)
        #print("Demanda: ", demanda)
        if demanda > volume_maximo:
            #print("Limite de demanda ultrapassado.")
            return False

        ###### TESTE DE TEMPO ######
        posicao_j = rota_corrente.index(arco[0])
        rota_corrente.insert(posicao_j + 1, u)
        #print("Rota corrente com insercao u no arco: ", rota_corrente)
        bju = 0
        for i in range(len(rota_corrente)-1):
            if rota_corrente[i] == 0:                
                if rota_corrente[i+1] == 0:
                    bju += matriz_tempo[rota_corrente[i]][-1]
                else:
                    bju += matriz_tempo[rota_corrente[i]][rota_corrente[i+1]]
            else:
                if rota_corrente[i+1] == 0:
                    bju += matriz_tempo[rota_corrente[i]][-1] + ot
                else:
                    bju += matriz_tempo[rota_corrente[i]][rota_corrente[i+1]] + ot
            if bju < jti[rota_corrente[i+1]]:
                bju = jti[rota_corrente[i+1]]
            #print("cliente: ", rota_corrente[i+1])
            #print("bju: ", bju)
            #print(f"jt[cliente]: ({jti[rota_corrente[i+1]]},{jtf[rota_corrente[i+1]]})")
            if bju > jtf[rota_corrente[i+1]]:
                #print("Limite de Janela de Tempo ultrapassado.")
                rota_corrente.remove(u)
                return False

        rota_corrente.remove(u)

        #print("Inserção Viável.")
        return True
    
    #################################################################

    def PFIH(rotas, volumes_totais, volume_maximo, volume, janela_tempo):
        """ Funcao PFIH de Solomon que resolve o VRP com restricao
            de janela de tempo. Essa funcao substitui o Savings.
            Ainda está em fase de construção.
        """
        #print(f"\nInicio da instancia {dic_instancia['nome_instancia']}\n")
        R = []
        #NR = rotas
        while rotas != []:
            #print("\n------Marcação de novo laço------\n")
            CI = []
            #print("NR: ", rotas)
            for i in rotas:
                if i not in R:
                    custo_inicializacao = -(distancia[0][i[0]])
                    CI.append((custo_inicializacao, i[0]))
            CI.sort()
            rota_corrente = [0, CI[0][1], 0]
            rotas.remove([CI[0][1]])
            #print("CI: ", CI, "\nRota Corrente :", rota_corrente)
            
            insercao_viavel = True
            while insercao_viavel:
                insercao_viavel = False
                H = []
                for i in rotas:
                    for j in range(len(rota_corrente)-1):
                        custo_inserir = calcula_custo_inserir(i[0], (rota_corrente[j], rota_corrente[j+1]), rota_corrente)
                        H.append([custo_inserir, i, (rota_corrente[j], rota_corrente[j+1])])
                H.sort(reverse=True)
                #print("H( ck, vi, (j,j+1) ): ", H)

                for h in H:
                    if testa_viabilidade(h[1][0], h[2], rota_corrente, volume, volume_maximo, jti, jtf, matriz_tempo):
                        # h[1] = elemento i - h[2] = arco (j,j+1)
                        inserir_u_em_rota(h[1][0], h[2], rota_corrente)
                        rotas.remove(h[1])
                        insercao_viavel = True
                        break
                #print("\nNR: ", rotas, "\nRota Corrente :", rota_corrente)
            R.append(rota_corrente)

        ###CALCULA CUSTO DA ROTA###
        #print("volumes_totais: ", volumes_totais)
        #print("volume: ", volume)
        custo = []
        for rota in R:
            custo_corrente = 0
            for i in range(len(rota)-2):
                custo_corrente += distancia[rota[i]][rota[i+1]]
            custo_corrente += distancia[rota[-2]][-1]
            custo.append(custo_corrente)

        # custo fixo da bicleta convencional
        # mais o custo por kilometro vezes a soma
        soma = 0
        for item in custo:
            soma +=item
        custo_logistico = 200*len(R)
        custo_km = 0.4*soma

        ###CALCULA VOLUME EM CADA ROTA###
        volume_todas_rotas = []
        for rota in R:
            volume_da_rota = 0
            for cliente in rota[1:-1]:
                volume_da_rota += volume[cliente-1]
            volume_todas_rotas.append(volume_da_rota)

        ###VOLUME ATUAL EM CADA INSTANTE NA ROTA###
        volume_corrente = []
        for item in volume_todas_rotas:
            volume_corrente.append([item])
        #print("R: ", R)
        for rota in R:
            for cliente in rota[1:-1]:
                volume_corrente[R.index(rota)].append(volume_corrente[R.index(rota)][len(volume_corrente[R.index(rota)])-1]
                                                -volume[cliente-1])
        #print("volume: ", volume)
        #print("volume_corrente: ", volume_corrente)

        utilizacao = []
        for i in range(len(volume_todas_rotas)):
            utilizacao.append((volume_todas_rotas[i]/volume_maximo)*100)
        util_media = 0
        for x in utilizacao:
            util_media += x
        util_media = util_media/len(utilizacao)
        
        
        ###DIC SOLUCAO###
        dic_solucao = {
            'Instancia'             : dic_instancia["nome_instancia"],
            'Caminho'               : R,
            'Volume'                : volume_todas_rotas,
            'Volume Corrente'       : volume_corrente,
            'Volume Maximo'         : volume_maximo,
            'Distancia Percorrida'  : custo,
            'Custo Logistico'       : custo_logistico,
            'Custo KM'              : custo_km,
            'Quantidade de Veiculos': len(R),
            'Utilizacao Media'      : util_media
            }

        return dic_solucao
    
    #################################################################
                                             
    #return paralelo(economia, rotas, volumes_totais, volume_maximo, volume)
    #return sequencial(economia, rotas, volumes_totais, volume_maximo, volume)
    return PFIH(rotas, volumes_totais, volume_maximo, volume, janela_tempo)
