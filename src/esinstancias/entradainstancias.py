import os

###############################################################################

def carrega_instancia(entrada):
    """ Funcao de leitura de arquivo '.dat' para o problema MCVRPIRFTW
        Cria variaveis para cada tipo de dado
        Le o arquivo e preenche as estruturas
        Armazena elas para uso posterior
        Retorna variaveis preenchidas em um dicionario
    """

    #VARIAVEIS LOCAIS A FUNCAO carrega_instancia()
    #variaveis simples (inteiros ou floats)
    nos, nosf, m, ncp, M, ot, N = 0, 0, 0, 0, 0, 0, 0
    distancia = []  #matriz distancia de i ate j
    t = []          #matriz tempo de i ate j
    prop = []       #matriz caixa j pertence ao cliente i (1 sim 0 nao)
    vlc = []        #lista de listas int ou float
    wti = []        #lista simples inicio janela de tempo
    wtf = []        #lista simples fim janela de tempo
    vlb = []        #lista simples com volumes das caixas (float)
    ck = []         #lista custo fixo das bicicletas
    cd = []         #lista custo por km rodado
    if not os.path.exists('INPUT'):
        print("Diretório de entrada não encontrado.")
        print("carrega instancia.")
        exit()
    os.chdir('INPUT')  #entro no diretorio para leitura do arquivo de input
    try:
        fhand = open(entrada, encoding = "ISO-8859-1")
    except:
        print(f"Arquivo {entrada} nao encontrado!")
        os.chdir('..')
        return -1
    linha = fhand.readline()
    #inicio leitura
    while linha:
        valor = linha.split()  #transformo linha em lista de strings
        if valor:              #se nao for vazio
            #Se encontro 'nos' na primeira string da lista
            if (valor[0] == 'nos'):
                #print(valor)
                aux = valor[len(valor)-1]
                #ultima string contem numero seguido de ';'
                aux = aux[:-1] #removo ';'
                nos = int(aux) #guardo valor na memoria
                #print(nos)
            #procuro o valor 'nosf' na primeira string da lista
            elif (valor[0] == 'nosf'):
                #print(valor)
                #aux recebeu o ultimo valor da string
                aux = valor[len(valor)-1]
                aux = aux[:-1] #removo o ';'
                nosf = int(aux) #guardo valor na memoria
                #print(nosf)
            #procuro valor 'm' na primeira string
            elif (valor[0] == 'm'):
                #print(valor)
                #print(valor[len(valor)-1])
                aux = valor[len(valor)-1]
                aux = aux[:-1]
                #m = int(aux)
                #print(m)
            elif (valor[0] == 'ncp'):
                #print(valor)
                #print(valor[len(valor)-1])
                aux = valor[len(valor)-1]
                aux = aux[:-1]
                ncp = int(aux)
                #print(ncp)
            elif (valor[0] == 'M'):
                #print(valor)
                #print(valor[len(valor)-1])
                aux = valor[len(valor)-1]
                aux = aux[:-1]
                M = int(aux)
                #print(M)
            elif (valor[0] == 'ot'):
                #print(valor)
                #print(valor[len(valor)-1])
                aux = valor[len(valor)-1]
                aux = aux[:-1]
                ot = float(aux)
                #print(ot)
            elif (valor[0] == 'N'):
                #print(valor)
                #print(valor[len(valor)-1])
                aux = valor[len(valor)-1]
                aux = aux[:-1]
                N = int(aux)
                #print(N)
            #procuro a lista de listas 'distancia'
            elif (valor[0] == 'distancia'):
                #enquanto nao chego ao fim da secao 'distancia'
                while valor[len(valor)-1] != '];':
                    #continuo a ler o arquivo
                    linha = fhand.readline()
                    valor = linha.split()
                    #print(valor)
                    listadist = []
                    #loop dentro de cada lista
                    for i in range(1, len(valor)-1):
                        #print (valor[i])
                        try:
                            #tenta transformar em int
                            listadist.append(int(valor[i]))
                        except:
                            try:
                                #se nao tenta em float (caso em que ha ponto)
                                listadist.append(float(valor[i]))
                            except: continue             #continua nos '['
                    #print(listadist)
                    #armazeno a lista em 'distanica'
                    if listadist != []:
                        distancia.append(listadist)
                #imprime_distancia(distancia)
            elif (valor[0] == 't'):
                #leio até a ultima linha das listas
                while valor[len(valor)-1] != '];':
                    #continuo a leitura do arquivo
                    linha = fhand.readline()
                    valor = linha.split()
                    listat = []
                    #percorro a lista de strings 'valor'
                    for i in range(1, len(valor)-1):                                    
                        #print (valor[i])
                        try:
                            listat.append(int(valor[i]))
                        except:
                            try:
                                listat.append(float(valor[i]))
                            except: continue
                    #print(listat)
                    t.append(listat)
                #imprime_distancia(t)
            elif (valor[0] == 'prop'):
                while valor[len(valor)-1] != '];':
                    linha = fhand.readline()
                    valor = linha.split()
                    listaprop = []
                    for i in range(1, len(valor)-1):
                        #print (valor[i])
                        try:
                            listaprop.append(int(valor[i]))
                        except: continue
                    #print(listaprop)
                    prop.append(listaprop)
                #imprime_prop(prop)
            elif (valor[0] == 'vlc'):
                while valor[len(valor)-1] != '];':
                    linha = fhand.readline()
                    valor = linha.split()
                    listavlc = []
                    for i in range(1, len(valor)-1):
                        #print (valor[i])
                        try:
                            listavlc.append(int(valor[i]))
                        except: continue
                    #print(listavlc)
                    vlc.append(listavlc)
                #print(vlc)
            elif (valor[0] == 'wti'):   #procuro pela lista 'wti'
                #percorro a lista de strings
                for i in range(len(valor)):
                    try:
                        wti.append(int(valor[i]))
                    except:
                        try:
                            #removo o '];' do ultimo elemento
                            rem = valor[i]
                            rem = rem[:-2]
                            wti.append(int(rem))
                        except: continue
                #print(wti)
            elif (valor[0] == 'wtf'):
                for i in range(len(valor)):
                    try:
                        wtf.append(int(valor[i]))
                    except:
                        try:
                            rem = valor[i]
                            rem = rem[:-2]
                            wtf.append(int(rem))
                        except: continue
                #imprime_janelas_tempo(wti,wtf)
            elif (valor[0] == 'vlb'):
                for i in range(len(valor)):
                    try:
                        vlb.append(float(valor[i]))
                    except: 
                        try:
                            rem = valor[i]
                            rem = rem[:-2]
                            vlb.append(float(rem))
                        except: continue
                #imprime_qual_bicicleta(prop, vlb, distancia)
            elif (valor[0] == 'ck'):
                for i in range(len(valor)):
                    try:
                        ck.append(int(valor[i]))
                    except: 
                        try:
                            rem = valor[i]
                            rem = rem[:-2]
                            ck.append(int(rem))
                        except:
                            #ultimo caso removo '[' caso nao
                            #tenha espacos no primerio elemto
                            try:
                                rem = valor[i]
                                rem = rem[1:]
                                ck.append(int(rem))
                            except: continue
                #print(ck)
            elif (valor[0] == 'cd'):
                for i in range(len(valor)):
                    try:
                        cd.append(float(valor[i]))
                    except: 
                        try:
                            rem = valor[i]
                            rem = rem[:-2]
                            cd.append(float(rem))
                        except:
                            try:
                                rem = valor[i]
                                rem = rem[1:]
                                cd.append(int(rem))
                            except: continue
                #print(cd)
        #leitura da proxima linha
        linha = fhand.readline()
    fhand.close()
    os.chdir('..')
    dic_instancia = {
        'nome_instancia'          : entrada[:entrada.find('.dat')],   #             # nome do arquivo .dat da instancia
        'clientes'                : nos,       # 'nos'       # quantidade de clientes (int) 
	'facilidades'             : nosf,      # 'nosf'      # quantidade facilidades (int)
	'num_veiculo_frota'       : m,         # 'm'         # numero de veiculos da frota(int) 
	'num_max_compartimentos'  : ncp,       # 'ncp'       # número máximo de compartimentos(int) 
	'M_grande'                : M,         # 'M'         # parâmetro auxiliar, um número "muito grande" (int)
	'distancia'               : distancia, # 'distancia' # distancia em km (ou custo) do arco i,j, onde i e j podem ser clientes e/ou facilidades. (float)
	'tempo'                   : t,         # 't'         # matriz tempo em horas de i para j, onde i e j podem ser clientes e/ou facilidades (lista de lista float - matriz)
	'janela_cliente_inicio'   : wti,       # 'wti'       # inicio da janela de tempo cliente (lista int)
	'janela_cliente_fim'      : wtf,       # 'wtf'       # fim da janela de tempo cliente (lista int)    
	'tempo_operacao_caixa'    : ot,        # 'ot'        # tempo médio de operação de uma caixa (h) (0.02h = 1.2min) (float)
	'num_caixas'              : N,         # 'N'         # Numero de caixas (int)
	'caixas_do_cliente'       : prop,      # 'prop'      # Qual caixa pertence a qual cliente (lista de lista boolean - matriz) "Boolean type can only be one of True or False"
	'volume_caixa'            : vlb,       # 'vlb'       # volumes das caixas (lista float)        
	'num_caixa_maior_cliente' : vlc,       # 'vlc'       # soma dos numeros de caixa do maior cliente (lista de lista float - matriz)
	'custo_fixo_bike'         : ck,        # 'ck'        # custo fixo das bicicletas (lista int)
	'custo_km_rodado'         : cd,        # 'cd'        # custo por km rodado (lista float)
	}            
            
    return dic_instancia
    #return (nos, nosf, m, ncp, M, ot, N, distancia, t, prop, vlc, wti, wtf, vlb, ck, cd)
            
#fim carrega_instancia
###############################################################################


def fazer_copia(entrada):
    """ Funcao que faz a leitura de arquivo '.dat'
        Tem o objetivo de armazenar texto para criar copia identica de saida
    """

    if not os.path.exists('INPUT'):
        print("Diretório de entrada não encontrado.")
        exit()
    os.chdir('INPUT')  #entro no diretorio para leitura do arquivo de input
    try:
        fhand = open(entrada, encoding = "ISO-8859-1")
    except:
        print(f"Arquivo {entrada} nao encontrado!")
        os.chdir('..')
        return -1
    texto = []
    linha = fhand.readline()
    #inicio leitura
    while linha:  
        #armazeno texto para recuperar mais tarde
        texto.append(linha)
        #leitura da proxima linha
        linha = fhand.readline()
    fhand.close()
    os.chdir('..')
            
    return texto       
    #return (texto, nos, nosf, m, ncp, M, ot, N, distancia, t, prop, vlc, wti, wtf, vlb, ck, cd)
            
#fim fazer_copia
###############################################################################
