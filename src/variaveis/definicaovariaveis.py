import os

######## Armazenar a instancia como um dicionario ##########
dic_instancia = {
    'nome_instancia'          : {}, #             # nome do arquivo .dat da instancia 
    'clientes'                : {}, # 'nos'       # quantidade de clientes (int) 
    'facilidades'             : {}, # 'nosf'      # quantidade facilidades (int)
    'num_veiculo_frota'       : {}, # 'm'         # numero de veiculos da frota(int) 
    'num_max_compartimentos'  : {}, # 'ncp'       # número máximo de compartimentos(int) 
    'M_grande'                : {}, # 'M'         # parâmetro auxiliar, um número "muito grande" (int)
    'distancia'               : {}, # 'distancia' # distancia em km (ou custo) do arco i,j, onde i e j podem ser clientes e/ou facilidades. (float)
    'tempo'                   : {}, # 't'         # matriz tempo em horas de i para j, onde i e j podem ser clientes e/ou facilidades (lista de lista float - matriz)
    'janela_cliente_inicio'   : {}, # 'wti'       # inicio da janela de tempo cliente (lista int)
    'janela_cliente_fim'      : {}, # 'wtf'       # fim da janela de tempo cliente (lista int)    
    'tempo_operacao_caixa'    : {}, # 'ot'        # tempo médio de operação de uma caixa (h) (0.02h = 1.2min) (float)
    'num_caixas'              : {}, # 'N'         # Numero de caixas (int)
    'caixas_do_cliente'       : {}, # 'prop'      # Qual caixa pertence a qual cliente (lista de lista boolean - matriz) "Boolean type can only be one of True or False"
    'volume_caixa'            : {}, # 'vlb'       # volumes das caixas (lista float)        
    'num_caixa_maior_cliente' : {}, # 'vlc'       # soma dos numeros de caixa do maior cliente (lista de lista float - matriz)
    'custo_fixo_bike'         : {}, # 'ck'        # custo fixo das bicicletas (lista int)
    'custo_km_rodado'         : {}, # 'cd'        # custo por km rodado (lista float)
}

######## Armazenar a entrada como um dicionario (alternativo) ##########
#dic_entrada = {
#    'nos'       : {}, # quantidade de clientes (int) 
#    'nosf'      : {}, # quantidade facilidades (int)
#    'm'         : {}, # numero de veiculos da frota(int) 
#    'ncp'       : {}, # número máximo de compartimentos (int) 
#    'M'         : {}, # parâmetro auxiliar, um número "muito grande" (int)
#    'distancia' : {}, # distancia em km (ou custo) do arco i,j, onde i e j podem ser clientes e/ou facilidades. (float)
#    't'         : {}, # matriz tempo em horas de i para j, onde i e j podem ser clientes e/ou facilidades (lista de lista float - matriz)
#    'wti'       : {}, # inicio da janela de tempo cliente (lista int)
#    'wtf'       : {}, # fim da janela de tempo cliente (lista int)    
#    'ot'        : {}, # tempo médio de operação de uma caixa (h) (0.02h = 1.2min) (float)
#    'N'         : {}, # Numero de caixas (int)
#    'prop'      : {}, # Qual caixa pertence a qual cliente (lista de lista boolean - matriz) "Boolean type can only be one of True or False"
#    'vlb'       : {}, # volumes das caixas (lista float)        
#    'vlc'       : {}, # soma dos numeros de caixa do maior cliente (lista de lista float - matriz)
#    'ck'        : {}, # custo fixo das bicicletas (lista int)
#    'cd'        : {}, # custo por km rodado (lista float)
#}




###############################################################################

def imprime_distancia(ll):
    """ Esta funcao imprime a matriz distancia
        Ela le a lista elemento por elemento
        E imprime num modelo de visualizacao facil
    """

    print('|{:^100}|'.format('destino'))
    print("origem |", end='')
    for i in range(len(ll)-1):
        print("%4.d" %i, end='  |  ')
    print('\n')
    for i in range(len(ll)):
        if not ll[i] == []:
            print("%5.d" %i, end='  |  ')
            for j in ll[i]:
                if type(j) == int:
                    print(j, end='  |  ')
                else:
                    print("%5.3f" %j, end=' |  ')
            print("\n")
###############################################################################

###############################################################################

def imprime_janelas_tempo(wti, wtf):
    """ Esta funcao imprime as janelas de tempos dos clientes
        A funcao le as duas listas contendo o inicio e o fim
        da janela de tempo de cada cliente
        e imprime num modelo de visualizacao facil
    """

    for i in range(len(wti)):
        print("Cliente ", i, "= [", wti[i], "->", wtf[i], "]\n")
       
###############################################################################

###############################################################################

def imprime_prop(prop):
    """ Funcao para imprimir qual caixa percente a qual cliente
        Cada linha representa um cliente
        A funcao identifica se a caixa (j) pertence ao cliente (i)
        Verificando se eh 1 (True) ou (0) False
        E imprime num modelo de visualizacao facil
    """

    for i in range(len(prop)):
        caixas = []
        for j in range(len(prop[i])):
            if prop[i][j] == 1:
                caixas.append(j)
        if caixas != []:
            print("Cliente ", i, " = ", caixas)
        
###############################################################################

###############################################################################

def imprime_qual_bicicleta(prop, vlb, distancia):
    """ Funcao em teste para calcular o custo usando uma bic
        convenc ou eletr para percorrer a distancia 0,i+1
        se a caixa j pertencer ao cliente i.
    """

    for i in range (len(prop)):
        for j in range (len(prop[i])):
            distancia_a_ser_percorrida = prop[i][j]*distancia[0][i+1]
            volume = vlb[j]
            if distancia_a_ser_percorrida != 0:
                if volume <= 5:
                    custo = 200 + 0.4*distancia_a_ser_percorrida
                    print(f"A.C -> {i+1} Bic Conv custa R${custo}.")
                    print(f" Caixa {j} volume {volume}")
                else:
                    custo = 500 + distancia_a_ser_percorrida
                    print(f"A.C. -> {i+1} Bic Eletr custa R${custo}.")
                    print(f" Levando caixa {j} com volume {volume}")
                    
###############################################################################


