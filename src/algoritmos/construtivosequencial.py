def savings(dic_instancia):
      #Função que busca minimizar o custo total de transporte obedecendo as restrições de capacidade e de número de visitas a um cliente
  D= dic_instancia['distancia'][:] #Busca a matriz distancia 
  capacidade= dic_instancia['num_max_compartimentos']    #Busca o valor da capacidade do veiculo
  #print('capacidade',capacidade) 
  volume=dic_instancia['caixas_do_cliente']      #Busca os valores das demandas
  #print('distancia',D)
  #print('Demanda',volume)
  economias=[]
  custo=[]
  rotas=[]
  rotas_unitarias=[]
  custo_max=0
  
  
  #print(len(D))
  for i in range(0, len(D)-1):    #Esse bloco calcula o valor economizado com a junção de duas entregas
    linha=[]
    #print('distancia',D[i])
    for j in range(0,len(D)-1):
      if j!=i and i>0 and j>0:
        linha.append(D[i][0]+D[0][j]-D[i][j])
      else:
        linha.append(9999)    # matriz savings deve ser a subtração da primeira com a segunda
    economias.append(linha)
    #print('matriz economias',economias)
  
  for i in range(0,1):            #Esse bloco monta as rotas unitárias com o custo de cada uma e também com o custo da soma de todas as viagens
    for j in range(1,len(D)-1):
      unitarias=[sum(volume[j]),0,j,0]
      rotas_unitarias.append(unitarias)
      custo_max+=D[0][j]+D[j][0]      #calcula o custo máximo da soma de todas as rotas
  print('Rotas unitarias:', rotas_unitarias)



  for i in range(1,len(D)-1):     #Percorrer a matriz economias e colocar as cidades em ordem decrescente de ganhos
    for j in range(i+1,len(D)-1):
      custo=economias[i][j]
      rotas.append([custo,(i,j)])
  rotas=sorted(rotas,reverse=True)[:] #colocou cada linha em ordem decrescente de valor
  print('Economias:',rotas)
  rota_corrente=[]

  for cidade in rotas:   #percorre cada rota em ordem decrescente de economias
    
    rota_final=rotas_unitarias
    i=cidade[1][0]   #seleciona a cidade de partida da rota mais economica
    j=cidade[1][1]   #seleciona a cidade de chegada da rota mais economica
    
    restricao_liberada=restricao_de_rotas(i,j,rota_corrente,rotas_unitarias)
    if restricao_liberada==True:
      resultado= restricao_de_demanda(i,j,capacidade,volume,rota_corrente)
      if resultado==True:
        rota_corrente,rotas_final=unir_rotas(i,j,rota_corrente,rotas_unitarias,volume)
    #print('rota unitária nova',rotas_unitarias)
    #print("Rota Corrente",rota_corrente)
  
  rota_corrente.insert(1,0) #Coloca o armazém como ponto de partida da rota
  rota_corrente.append(0) #Coloca o armazém como local de retorno do veículo
  rota_final.append(rota_corrente)  #Adiciona a rota formada em rota final
  print('Rota Final:',rota_final)
  
  return rota_final

def restricao_de_rotas(i, j,rota_corrente,rotas_unitarias):
  #print('rotas unitarias dentro:',rotas_unitarias)
#for cidade in rotas_unitarias:
    #if j in cidade or i in cidade:
  
  if i in rota_corrente and j in rota_corrente: #Verifica se i e j já fazem parte da rota que está sendo montada
    return False
  elif i in rota_corrente and j not in rota_corrente:     #Verifica se i faz parte da rota corrente e j não
    if i==rota_corrente[1] or i==rota_corrente[-1]:       #verifica se a posição de i na rota corrente é de inicio ou de fim
      return True
    else:
      return False
  elif j in rota_corrente and i not in rota_corrente:     #Verifica se j faz parte da rota corrente e i não
    if j==rota_corrente[1] or j==rota_corrente[-1]:       #verifica se a posição de j na rota corrente é de inicio ou de fim
      return True
    else:
      return False
  else:                                       #Verifica se i e j não fazem parte da rota que está sendo montada
    if rota_corrente==[]:
      return True
    else:
      return False
     
 


def restricao_de_demanda(i, j,capacidade,volume,rota_corrente):
  demanda_corrente=0
  print('i',i)
  print('j',j)
  print('ROTA CORRENTE',rota_corrente)
  if rota_corrente==[]:           #quando a rota corrente ainda não possui nenhuma cidade utiliza-se esse if
    demanda_corrente=sum(volume[i])+sum(volume[j])    #soma-se a demanda das cidades que estãotentando entrar na rota para verificara  capacidade
    print('DEMANDA CORRENTE',demanda_corrente)
  else:                                  #quando a rota corrente já possui cidades
    demanda_corrente=rota_corrente[0]   #a demanda corrente recebe o valor da demanda da rta corrente
    if i in rota_corrente:
      demanda_corrente+=sum(volume[j])    #soma-se ao valor da rota corrente o volume da nova cidade
    if j in rota_corrente:
      demanda_corrente+=sum(volume[i])    #soma-se ao valor da rota corrente o volume da nova cidade
    print('DEMANDA CORRENTE',demanda_corrente)
  if demanda_corrente<=capacidade:    # ele testa se a demanda existente a a da cidade candidata a rota nao excedem a capacidade maxima
    return True  # se nao exceder, entao SIM. as rotas podem ser unidas
  else:
    return False

def unir_rotas(i, j,rota_corrente,rotas_unitarias,volume):
  print('i',i)
  print('j',j)
  print('!!!!rota corrente:',rota_corrente)
  

  if i in rota_corrente and j in rota_corrente: #Verifica se as cidades já fazem parte da rota que está sendo montada
    return rota_corrente,rotas_unitarias
  elif i in rota_corrente and j not in rota_corrente:   #verifica se uma das cidades dessa rota já pertencee a rota corrente
    if i==rota_corrente[1]:       #verifica se a cidade que já pertence a rota é um extremo
      rota_corrente.insert(1,j)   #adiciona somente a cidade que não faz parte da rota ainda
      rota_corrente[0]=rota_corrente[0]+sum(volume[j])    #Adiciona ao volume da rota a demanda da nova cidade
      for cidade in rotas_unitarias:
        if j in cidade:
          rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
    elif i==rota_corrente[-1]:      #verifica se a cidade que já pertence a rota é um extremo
      rota_corrente.append(j)       #adiciona somente a cidade que não faz parte da rota ainda
      rota_corrente[0]=rota_corrente[0]+sum(volume[j])    #Adiciona ao volume da rota a demanda da nova cidade
      for cidade in rotas_unitarias:
        if j in cidade:
          rotas_unitarias.remove(cidade)      #Remove a cidade inserida das rotas unitárias
    else:
      return rota_corrente,rotas_unitarias
  elif j in rota_corrente and i not in rota_corrente:
    if j==rota_corrente[1]:         #verifica se a cidade que já pertence a rota é um extremo
      rota_corrente.insert(1,i)     #adiciona somente a cidade que não faz parte da rota ainda
      rota_corrente[0]=rota_corrente[0]+sum(volume[i])    #Adiciona ao volume da rota a demanda da nova cidade
      for cidade in rotas_unitarias:
        if i in cidade:
          rotas_unitarias.remove(cidade)      #Remove a cidade inserida das rotas unitárias
    elif  j==rota_corrente[-1]:               #verifica se a cidade que já pertence a rota é um extremo
      rota_corrente.append(i)
      rota_corrente[0]=rota_corrente[0]+sum(volume[i])    #Adiciona ao volume da rota a demanda da nova cidade
      for cidade in rotas_unitarias:
        if i in cidade:
          rotas_unitarias.remove(cidade)      #Remove a cidade inserida das rotas unitárias
  else:                             #adiciona as duas cidades que não fazem parte da rota ainda
    rota_corrente.append(i)
    rota_corrente.append(j)
    rota_corrente.insert(0,sum(volume[i])+sum(volume[j]))   #Adiciona ao volume da rota a demanda das novas cidades
    for cidade in rotas_unitarias:
      if j in cidade or i in cidade:
        rotas_unitarias.remove(cidade)    #Remove as cidades inseridas das rotas unitárias
  #print('????rotas:',rota_corrente)
  return rota_corrente,rotas_unitarias