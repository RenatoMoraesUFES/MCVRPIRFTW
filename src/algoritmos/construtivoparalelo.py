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
  
  
  #print(len(D))
  for i in range(0, len(D)):    #Esse bloco calcula o valor economizado com a junção de duas entregas
    linha=[]
    #print('distancia',D[i])
    for j in range(0,len(D)):
      if j!=i and i>0 and j>0:
        linha.append(D[i][0]+D[0][j]-D[i][j])
      else:
        linha.append(9999)    # matriz savings deve ser a subtração da primeira com a segunda
    economias.append(linha)
    #print('matriz economias',economias)
  
  for i in range(0,1):            #Esse bloco monta as rotas unitárias com o custo de cada uma e também com o custo da soma de todas as viagens
    for j in range(1,len(D)):
      unitarias=[sum(volume[j]),0,j,0]
      rotas_unitarias.append(unitarias)
  print('Rotas unitarias:', rotas_unitarias)



  for i in range(1,len(D)):     #Percorrer a matriz economias e colocar as cidades em ordem decrescente de ganhos
    for j in range(i+1,len(D)):
      custo=economias[i][j]
      rotas.append([custo,(i,j)])
  rotas=sorted(rotas,reverse=True)[:] #colocou cada linha em ordem decrescente de valor
  print('Economias:',rotas)

  for cidade in rotas:   #percorre cada rota em ordem decrescente de economias
    
    #rota_corrente=[]
    i=cidade[1][0]   #seleciona a cidade de partida da rota mais economica
    j=cidade[1][1]   #seleciona a cidade de chegada da rota mais economica
    
    
    verificacao_demanda= restricao_de_demanda(i,j,capacidade,volume,rotas_unitarias)
    print('RESTRIÇÃO DE DEMANDA',verificacao_demanda)
    if verificacao_demanda==True:
      verificacao_rota=restricao_de_rotas(i,j,rotas_unitarias)
      print('restrição de rota',verificacao_rota)
      if verificacao_rota==True:
        rotas_unitarias=unir_rotas(i,j,rotas_unitarias,volume)

  custo_final=[]
  for rota in rotas_unitarias: #calcula o custo final de cada rota
    custo_rota=0
    for i in range(1,len(rota)-1):
      custo_rota+=D[rota[i]][rota[i+1]]   #lista parcial de custos
    custo_final.append(custo_rota)    #adiciona o custo da rota completa na lista final de custos

  
  
  print('Rotas unitárias:',rotas_unitarias)
  print('custos finais',custo_final)
  
  return rotas_unitarias


  
  
def unir_rotas(i, j,rotas_unitarias,volume):
  print('i',i)
  print('j',j)
  print('!!!!rotas unitárias:',rotas_unitarias)


  for rota in rotas_unitarias: 
    

    if i in rota and j not in rota:   #verifica se uma das cidades dessa rota já pertencee a rota corrente
      if i==rota[2]:       #verifica se a cidade que já pertence a rota é um extremo
        rota.insert(2,j)   #adiciona somente a cidade que não faz parte da rota ainda
        rota[0]=rota[0]+sum(volume[j])    #Adiciona ao volume da rota a demanda da nova cidade
        for cidade in rotas_unitarias:
          if j in cidade and j==cidade[2] and j==cidade[-2]:
            rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias

      elif i==rota[-2]:      #verifica se a cidade que já pertence a rota é um extremo
        rota.insert(-1,j)       #adiciona somente a cidade que não faz parte da rota ainda
        rota[0]=rota[0]+sum(volume[j])    #Adiciona ao volume da rota a demanda da nova cidade
        for cidade in rotas_unitarias:
          if j in cidade and j==cidade[2] and j==cidade[-2]:
            rotas_unitarias.remove(cidade)      #Remove a cidade inserida das rotas unitárias
      else:
        return rotas_unitarias
 
    elif j in rota and i not in rota:
      if j==rota[2]:         #verifica se a cidade que já pertence a rota é um extremo
        rota.insert(2,i)     #adiciona somente a cidade que não faz parte da rota ainda
        rota[0]=rota[0]+sum(volume[i])    #Adiciona ao volume da rota a demanda da nova cidade
        for cidade in rotas_unitarias:
          if i in cidade and i==cidade[2] and i==cidade[-2]:
            rotas_unitarias.remove(cidade)      #Remove a cidade inserida das rotas unitárias
        
      elif  j==rota[-2]:               #verifica se a cidade que já pertence a rota é um extremo
        rota.insert(-1,i)
        rota[0]=rota[0]+sum(volume[i])    #Adiciona ao volume da rota a demanda da nova cidade
        for cidade in rotas_unitarias:
          if i in cidade and i==cidade[2] and i==cidade[-2]:
            rotas_unitarias.remove(cidade)      #Remove a cidade inserida das rotas unitárias
      else:
        return rotas_unitarias

  print(" ROTAS UNITARIAS", rotas_unitarias)
  return rotas_unitarias

def restricao_de_rotas(i, j,rotas_unitarias):
  #print('rotas unitarias dentro:',rotas_unitarias)
  #for cidade in rotas_unitarias:
  #if j in cidade or i in cidade:
  for rota in rotas_unitarias:  
    
    if i in rota and j not in rota:   #verifica se uma das cidades dessa rota já pertencee a rota corrente
      if i==rota[2] or i==rota[-2]:       #verifica se a cidade que já pertence a rota é um extremo
        return True
      else:
        return False
    if i in rota and j not in rota:   #verifica se uma das cidades dessa rota já pertencee a rota corrente
      if j==rota[2] or i==rota[-2]:       #verifica se a cidade que já pertence a rota é um extremo
        return True
      else:
        return False







def restricao_de_demanda(i, j,capacidade,volume,rotas_unitarias):
  demanda_corrente=0
  print('i',i)
  print('j',j)
  print('ROTA UNITARIA******',rotas_unitarias)

  for rota in rotas_unitarias:  #Calcula a demanda das cidades candidatas e da possivel rota que já estão inseridas
    
    if i in rota and j not in rota:
      demanda_corrente+=rota[0]
    elif j in rota and i not in rota:
      demanda_corrente+=rota[0]
      
  print('DEMANDA CORRENTE',demanda_corrente)
  if demanda_corrente<=capacidade:  #verifica se a demanda atende a restrição de capacidade
    return True
  else:
    return False
    