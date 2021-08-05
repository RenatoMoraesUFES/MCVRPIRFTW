def savings(dic_instancia):
  #Função que busca minimizar o custo total de transporte obedecendo as restrições de capacidade e de número de visitas a um cliente
  D= dic_instancia['distancia'][:] #Busca a matriz distancia 
  #capacidade= dic_instancia['num_max_compartimentos']    #Busca o valor da capacidade do veiculo
  prop=dic_instancia['caixas_do_cliente']
  volume=dic_instancia['volume_caixa']      #Busca os valores das demandas
  volume_limite=50
  nosf=dic_instancia['facilidades']
  cd=dic_instancia['custo_km_rodado']
  ck=dic_instancia['custo_fixo_bike']
  economias=[]
  import numpy as np
  
  for i in range(0,len(D)-1):    #Esse bloco calcula o valor economizado com a junção de duas entregas
    linha=[]
    for j in range(0,len(D)-1):
      if j!=i and i>0 and j>0:
        linha.append(D[i][0]+D[0][j]-D[i][j])
      else:
        linha.append(9999)    # matriz savings deve ser a subtração da primeira com a segunda
    economias.append(linha)
  

  #Cria o vetor de volumes calculados por cliente
  volume_por_rota_unitaria=[]
  for i in range(0,len(prop)-1-nosf):
    
    volume_cliente=0
    for j in range(0, len(prop[i])):
      if prop[i][j]==1:
        volume_cliente+=volume[j]
    volume_por_rota_unitaria.append(volume_cliente)

  #Esse bloco monta as rotas unitárias com o custo de cada uma e também com o custo da soma de todas as viagens
  unitarias=[]
  rotas_unitarias=[]
  for i in range(0,1):            
    for j in range(1,len(D)-2-nosf):
      unitarias=[j]
      rotas_unitarias.append(unitarias)


  #Percorrer a matriz economias e colocar as cidades em ordem decrescente de ganhos
  rotas=[]
  custo=[]
  for i in range(1,len(D)-2-nosf):     
    for j in range(i+1,len(D)-2-nosf):
      custo=economias[i][j]
      rotas.append([custo,(i,j)])
  rotas=sorted(rotas,reverse=True)[:] #colocou cada linha em ordem decrescente de valor


  for cidade in rotas:   #percorre cada rota em ordem decrescente de economias
    
    #rota_corrente=[]
    i=cidade[1][0]   #seleciona a cidade de partida da rota mais economica
    j=cidade[1][1]   #seleciona a cidade de chegada da rota mais economica
    
    rota_final=rotas_unitarias
    i=cidade[1][0]   #seleciona a cidade de partida da rota mais economica
    j=cidade[1][1]   #seleciona a cidade de chegada da rota mais economica

    verificacao_rota=restricao_de_rotas(i,j,rotas_unitarias)
    if verificacao_rota==True:
      verificacao_demanda=restricao_de_demanda(i,j,volume_limite,volume_por_rota_unitaria,rotas_unitarias)
      if verificacao_demanda==True:
        rotas_unitarias=unir_rotas(i,j,rotas_unitarias)

  rotas_formadas, volume_final, caixas_por_rota, custo_km,custo_total,custo_utilizacao,dmp,vmpr,cau=saidas(rotas_unitarias,cd,ck,D,volume_por_rota_unitaria,prop,volume,volume_limite)
  
  #cpr_T=[]
  #cpr_T= np.array(caixas_por_rota).T  #Resultado da entrega de caixas por rota transposta
  dic_solucao = {
    'Caminho'               : rotas_formadas,
    'Volume'                : volume_final,
    'Caixas por rota'   : caixas_por_rota,
    #'Entrega de caixas por rota'  : cpr_T,
    'Distancia Percorrida'  : custo_total,
    'Custo Utilização'       : custo_utilizacao,
    'Custo KM'              : custo_km,
    'Quantidade de Veiculos': len(rotas_formadas),
    'Distancia média percorrida'  : dmp,
    'Volume médio por rota' : vmpr,
    'Capacidades utilizadas'  : cau,
    'Capacidade média utilizada' : sum(cau)/len(rotas_formadas),
    'Volume limite'  : volume_limite

    }

  return dic_solucao
  

'''def entrega(rotas_formadas,volume_final,caixas_por_rota): #Função que retira os clientes e suas caixas das rotas após a entrega
  import copy
  entrega_caixas_por_rota=copy.deepcopy(caixas_por_rota)
  for rota in rotas_formadas:
    for cliente in range(1,len(rota)-1):
      for j in range(0,len(entrega_caixas_por_rota)):
        if entrega_caixas_por_rota[j] != "-":
          for k in range(0,len(entrega_caixas_por_rota[j])):
            if rota[cliente] == entrega_caixas_por_rota[j][k][0]:
              entrega_caixas_por_rota[j][k]="-"

  return entrega_caixas_por_rota'''

def saidas(rotas_unitarias,cd,ck,D,volume_por_rota_unitaria,prop,volume,volume_limite):


  #CALCULA O VOLUME QUE CADA ROTA CARREGA
  volume_final=[]
  capacidades_utilizadas=[]
  for rota in rotas_unitarias:
    demanda_rota=0
    capacidade_utilizada_rota=0
    for cidade in rota:
      demanda_rota+=volume_por_rota_unitaria[cidade-1]
    volume_final.append(demanda_rota)
    capacidade_utilizada_rota=(demanda_rota*100)/volume_limite
    capacidades_utilizadas.append(capacidade_utilizada_rota)
  volume_medio_por_rota=sum(volume_final)/len(rotas_unitarias)
  
  #Busca as caixas de cada cliente e seus respectivos volumes quue estarão em cada rota
  caixas_por_rota=[]
  r=[]
  caixa=()
  for rota in rotas_unitarias:
    for cidade in rota:
      for j in range(0, len(prop[cidade])):
        if prop[cidade-1][j]==1:
          caixa=(cidade,j,volume[j])
          r.append(caixa)
        caixa=()
    caixas_por_rota.append(r)
    r=[]

  #print('caixas por rota',caixas_por_rota)

  #Insere o armazem no inicio e final das rotas formadas, para padronização, e calcula o custo de cada uma delas(custo de utilização, por km e distancia)
  custo_rota = [] 
  custo_km_rota=[]           
  for rota in rotas_unitarias:
    custo_corrente = 0
    rota.insert(0,0)    #insere o armazem no inicio de cada rota
    rota.append(0)      #insere o armazem no fim de cada rota
    cdr=0
    for i in range(len(rota)-2):
      custo_corrente += D[rota[i]][rota[i+1]]
    custo_corrente += D[rota[-2]][-1]
    cdr=custo_corrente*cd[2]            #calcula o custo do km para bicicleta convencional
    custo_km_rota.append(cdr)
    custo_rota.append(custo_corrente)
  custo_km=sum(custo_km_rota)
  custo_total=sum(custo_rota)    #Calcula o custo final de todas as rotas
  custo_utilizacao=len(rotas_unitarias)*ck[2] #custo de utilização da instancia
  #print('custo utilização',custo_utilizacao)
  distancia_media_percorrida=custo_total/len(rotas_unitarias)

  return rotas_unitarias, volume_final, caixas_por_rota, custo_km,custo_total,custo_utilizacao,distancia_media_percorrida,volume_medio_por_rota,capacidades_utilizadas


#FUNÇÃO PARA UNIR AS ROTAS VIÁVEIS
def unir_rotas(i, j, rotas_unitarias):
  '''p1, p2 = [], []
  for rota in rotas:
    if rota[0] == j:
      p1 = rota
    elif rota[-1] == i:
      p2 = rota
   '''

  p1=[]
  p2=[]
  for rota in rotas_unitarias:
    if j in rota:
      p1 = rota
    elif i in rota:
      p2 = rota
      
  pos_p1 = rotas_unitarias.index(p1)
  pos_p2 = rotas_unitarias.index(p2)
 
  if p1[0] == j and p2[0] == i:
    rotas_unitarias.remove(p1)
    rotas_unitarias.remove(p2)
    p1.reverse()
    rotas_unitarias.append(p1+p2)
  elif p1[-1] == j and p2[-1] == i:
    rotas_unitarias.remove(p1)
    rotas_unitarias.remove(p2)
    p2.reverse()
    rotas_unitarias.append(p1+p2)
  elif p1[0] == j and p2[-1] == i:
    rotas_unitarias.remove(p1)
    rotas_unitarias.remove(p2)
    rotas_unitarias.append(p2+p1)
  elif p1[-1] == j and p2[0] == i:
    rotas_unitarias.remove(p1)
    rotas_unitarias.remove(p2)
    rotas_unitarias.append(p1+p2)
          
  return rotas_unitarias
  


#FUNÇÃO QUE VERIFICA SE CONSEGUE COLOCAR DOIS CLIENTES EM UMA ROTA ANALISANDO O VOLUME DEMANDADO POR CADA UM E A CAPACIDADE DO VEÍCULO
def restricao_de_demanda(i, j, volume_limite,volume,rotas_unitarias):
  for rota in rotas_unitarias:  #Calcula a demanda das cidades candidatas e da possivel rota que já estão inseridas
    if i in rota and j not in rota:
      demanda_corrente=0
      for cidade in rota:
        demanda_corrente+=volume[cidade-1]
      cidade_candidata=search(rotas_unitarias,j) #procura onde está a outra cidade canditada para verificar se ela já está associada a uma rota
      for cidade in rotas_unitarias[cidade_candidata[0]]:
        demanda_corrente+=volume[cidade-1]  
      if demanda_corrente<=volume_limite:  #verifica se a demanda atende a restrição de capacidade
        return True
      else:
        return False
    elif j in rota and i not in rota:
      demanda_corrente=0
      for cidade in rota:
        demanda_corrente+=volume[cidade-1]
      cidade_candidata=search(rotas_unitarias,i) #procura onde está a outra cidade canditada para verificar se ela já está associada a uma rota
      for cidade in rotas_unitarias[cidade_candidata[0]]:
        demanda_corrente+=volume[cidade-1] #demanda da segunda cidade verificada
      if demanda_corrente<=volume_limite:  #verifica se a demanda atende a restrição de capacidade
        return True
      else:
        return False

#FUNÇÃO QUE VERIFICA SE CONSEGUE COLOCAR DOIS CLIENTES EM UMA ROTA ANALISANDO A SEQUENCIA DE ENTREGA 
def restricao_de_rotas(i, j,rotas_unitarias):
  #print('i',i)
  #print('j',j)
  #print('ROTA unitaria:',rotas_unitarias)    
  for rota in rotas_unitarias:  
    #print('ROTA:',rota)
    if i in rota and j not in rota:   #verifica se uma das cidades dessa rota já pertencee a rota corrente
      if i==rota[0] or i==rota[-1]:       #verifica se a cidade que já pertence a rota é um extremo
        return True
      else:
        return False
    if j in rota and i not in rota:   #verifica se uma das cidades dessa rota já pertencee a rota corrente
      if j==rota[0] or j==rota[-1]:       #verifica se a cidade que já pertence a rota é um extremo
        return True
      else:
        return False

def search (lista, valor):
  localizacao=[[lista.index(x), x.index(valor)] for x in lista if valor in x]
  return localizacao[0]
