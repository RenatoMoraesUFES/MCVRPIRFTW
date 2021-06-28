def savings(dic_instancia):
      #Função que busca minimizar o custo total de transporte obedecendo as restrições de capacidade e de número de visitas a um cliente
  D= dic_instancia['distancia'][:] #Busca a matriz distancia 
  #capacidade= dic_instancia['num_max_compartimentos']    #Busca o valor da capacidade do veiculo
  #print('capacidade',capacidade) 
  prop=dic_instancia['caixas_do_cliente']
  #print('caixas_cliente',prop)
  volume=dic_instancia['volume_caixa']      #Busca os valores das demandas
  #print('distancia',D)
  #print('Demanda',volume)
  volume_limite=100
  nosf=dic_instancia['facilidades']
  economias=[]
  custo=[]
  rotas=[]
  rotas_unitarias=[]
  volume_por_rota_unitaria=[]
  volume_final=[]
  unitarias=[]
  custo_final=[]
  
  #print(len(D))
  for i in range(0,len(D)-1):    #Esse bloco calcula o valor economizado com a junção de duas entregas
    linha=[]
    for j in range(0,len(D)-1):
      if j!=i and i>0 and j>0:
        linha.append(D[i][0]+D[0][j]-D[i][j])
      else:
        linha.append(9999)    # matriz savings deve ser a subtração da primeira com a segunda
    economias.append(linha)
  
  #print('matriz economias',economias)

  #Cria o vetor de volumes calculados por cliente
  for i in range(0,len(prop)-1-nosf):
    
    volume_cliente=0
    for j in range(0, len(prop[i])):
      if prop[i][j]==1:
        volume_cliente+=volume[j]
    volume_por_rota_unitaria.append(volume_cliente)
  #print('volume por rota unitaria',volume_por_rota_unitaria)
  
  
  for i in range(0,1):            #Esse bloco monta as rotas unitárias com o custo de cada uma e também com o custo da soma de todas as viagens
    for j in range(1,len(D)-2-nosf):
      #print('lend',len(D))
      unitarias=[j]
      rotas_unitarias.append(unitarias)
  #print('Rotas unitarias:', rotas_unitarias)



  for i in range(1,len(D)-2-nosf):     #Percorrer a matriz economias e colocar as cidades em ordem decrescente de ganhos
    for j in range(i+1,len(D)-2-nosf):
      custo=economias[i][j]
      rotas.append([custo,(i,j)])
  rotas=sorted(rotas,reverse=True)[:] #colocou cada linha em ordem decrescente de valor
  #print('Economias:',rotas)

  for cidade in rotas:   #percorre cada rota em ordem decrescente de economias
    
    #rota_corrente=[]
    i=cidade[1][0]   #seleciona a cidade de partida da rota mais economica
    j=cidade[1][1]   #seleciona a cidade de chegada da rota mais economica
    
    
    rota_final=rotas_unitarias
    i=cidade[1][0]   #seleciona a cidade de partida da rota mais economica
    j=cidade[1][1]   #seleciona a cidade de chegada da rota mais economica

    verificacao_rota=restricao_de_rotas(i,j,rotas_unitarias)
    if verificacao_rota==True:
      #verificacao_janela=janela_tempo(wti,wtf,oti,rotas_unitarias,i,j,t)
      #if verificacao_janela==True:
      verificacao_demanda=restricao_de_demanda(i,j,volume_limite,volume_por_rota_unitaria,rotas_unitarias)
      if verificacao_demanda==True:
        rotas_unitarias=unir_rotas(i,j,rotas_unitarias)

  for rota in rotas:
    rota.insert(0, 0)
    rota.append(0)
  for rota in rotas_unitarias:
    demanda_rota=0
    custo_rota=0
    for cidade in rota:
      demanda_rota+=volume_por_rota_unitaria[cidade-1]
      custo_rota+=D[cidade][cidade+1]
      #print('custo rota',custo_rota)
    volume_final.append(demanda_rota)
    custo_final.append(custo_rota)

  rotas_formadas=rotas_unitarias
  
  custo_final = []
  for rota in rotas_formadas:
    custo_corrente = 0
    rota.insert(0,0)
    rota.append(0)
    for i in range(len(rota)-2):
      custo_corrente += D[rota[i]][rota[i+1]]
    custo_corrente += D[rota[-2]][-1]
    custo_final.append(custo_corrente)
  #a diferença de valor encontrada na rota que inicia com a cidade 6 é devido a ordem de visita da rota

  #print('Rotas formadas:',rotas_formadas)
  #print('custos finais',custo_final)
  #print('Volumes finais',volume_final)
  dic_solucao = {
    'caminho'   : rotas_formadas,
    'volume'    : volume_final,
    'custo'     : custo_final
          }
  return dic_solucao
  


   
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
