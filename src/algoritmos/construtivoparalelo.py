def savings(dic_instancia):
  #Função que busca minimizar o custo total de transporte obedecendo as restrições de capacidade e de número de visitas a um cliente
  D= dic_instancia['distancia'][:] #Busca a matriz distancia 
  #capacidade= dic_instancia['num_max_compartimentos']    #Busca o valor da capacidade do veiculo
  #print('capacidade',capacidade) 
  prop=dic_instancia['caixas_do_cliente']
  #print('caixas_cliente',prop)
  volume=dic_instancia['volume_cliente']      #Busca os valores das demandas
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


  #Cria o vetor de volumes calculados por cliente
  for i in range(0,len(prop)-1-nosf):
    volume_cliente=0
    for j in range(0, len(prop[i])):
      if prop[i][j]==1:
        volume_cliente+=volume[j]
    volume_por_rota_unitaria.append(volume_cliente)
  #print('volume por rota unitaria',volume_por_rota_unitaria)
  
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
    
    
    verificacao_demanda= restricao_de_demanda(i,j,volume_limite,volume_por_rota_unitaria,rotas_unitarias)
    #print('RESTRIÇÃO DE DEMANDA',verificacao_demanda)
    if verificacao_demanda==True:
      verificacao_rota=restricao_de_rotas(i,j,rotas_unitarias)
      #print('restrição de rota',verificacao_rota)
      if verificacao_rota==True:
        rotas_unitarias=unir_rotas(i,j,rotas_unitarias)

  for rota in rotas_unitarias:
    demanda_rota=0
    for cidade in rota:
      demanda_rota+=volume_por_rota_unitaria[cidade-1]
    volume_final.append(demanda_rota)

  rotas_formadas=rotas_unitarias
  
  
  print('Rotas unitárias:',rotas_unitarias)
  print('Rotas formadas:',rotas_formadas)
  #print('custos finais',custo_final)
  print('Volumes finais',volume_final)
  
  return rotas_unitarias


  
  
def unir_rotas(i, j,rotas_unitarias):
  print('i',i)
  print('j',j)
  print('!!!!rotas unitárias:',rotas_unitarias)


  for rota in rotas_unitarias: 
    

    if i in rota and j not in rota:   #verifica se uma das cidades dessa rota já pertencee a rota corrente
      if i==rota[0] and i==rota[-1]:       #verifica se a cidade que já pertence a rota é um extremo
        cidade_candidata=search(rotas_unitarias,j) #procura onde está a outra cidade
        if j==rotas_unitarias[cidade_candidata[0]][0] and j==rotas_unitarias[cidade_candidata[0]][-1]:
          rota.insert(0,j)   #adiciona somente a cidade que não faz parte da rota ainda
          for cidade in rotas_unitarias:
            if j in cidade and j==cidade[0] and j==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
        elif j==rotas_unitarias[cidade_candidata[0]][0] and j!=rotas_unitarias[cidade_candidata[0]][-1]:
          rotas_unitarias[cidade_candidata[0]].insert(0,i)
          for cidade in rotas_unitarias:
            if i in cidade and i==cidade[0] and i==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
          
        elif j==rotas_unitarias[cidade_candidata[0]][-1] and j!=rotas_unitarias[cidade_candidata[0]][0]:
          rotas_unitarias[cidade_candidata[0]].append(i)
          for cidade in rotas_unitarias:
            if i in cidade and i==cidade[0] and i==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
      
      elif i==rota[0] and i!=rota[-1]:       #verifica se a cidade que já pertence a rota é um extremo
        cidade_candidata=search(rotas_unitarias,j) #procura onde está a outra cidade
        if j==rotas_unitarias[cidade_candidata[0]][0] and j==rotas_unitarias[cidade_candidata[0]][-1]:
          rota.insert(0,j)   #adiciona somente a cidade que não faz parte da rota ainda
          for cidade in rotas_unitarias:
            if j in cidade and j==cidade[0] and j==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
        elif j==rotas_unitarias[cidade_candidata[0]][0] and j!=rotas_unitarias[cidade_candidata[0]][-1]:
          return rotas_unitarias
          
        elif j==rotas_unitarias[cidade_candidata[0]][-1] and j!=rotas_unitarias[cidade_candidata[0]][0]:
          rotas_unitarias[cidade_candidata[0]].extend(rota) #uni as duas rotas existentes
          rotas_unitarias.remove(rota)
          
        
      elif i==rota[-1] and i!=rota[0]:      #verifica se a cidade que já pertence a rota é um extremo
        cidade_candidata=search(rotas_unitarias,j) #procura onde está a outra cidade
        if j==rotas_unitarias[cidade_candidata[0]][0] and j==rotas_unitarias[cidade_candidata[0]][-1]:
          rota.append(j)       #adiciona somente a cidade que não faz parte da rota ainda
          for cidade in rotas_unitarias:
            if j in cidade and j==cidade[0] and j==cidade[-1]:
              rotas_unitarias.remove(cidade)      #Remove a cidade inserida das rotas unitárias
        elif j==rotas_unitarias[cidade_candidata[0]][0] and j!=rotas_unitarias[cidade_candidata[0]][-1]:
          rotas_unitarias[cidade_candidata[0]].insert(0,i)
          for cidade in rotas_unitarias:
            if i in cidade and i==cidade[0] and i==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
          
        elif j==rotas_unitarias[cidade_candidata[0]][-1] and j!=rotas_unitarias[cidade_candidata[0]][0]:
          rotas_unitarias[cidade_candidata[0]].append(i)
          for cidade in rotas_unitarias:
            if j in cidade and j==cidade[0] and j==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
      else:
        return rotas_unitarias
    elif j in rota and i not in rota:
      if j==rota[0] and j==rota[-1]:         #verifica se a cidade que já pertence a rota é um extremo
        cidade_candidata=search(rotas_unitarias,i) #procura onde está a outra cidade
        if i==rotas_unitarias[cidade_candidata[0]][0] and i==rotas_unitarias[cidade_candidata[0]][-1]:
          rota.insert(0,i)   #adiciona somente a cidade que não faz parte da rota ainda
          for cidade in rotas_unitarias:
            if i in cidade and i==cidade[0] and i==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
        elif i==rotas_unitarias[cidade_candidata[0]][0] and i!=rotas_unitarias[cidade_candidata[0]][-1]:
          rotas_unitarias[cidade_candidata[0]].insert(0,j)
          for cidade in rotas_unitarias:
            if j in cidade and j==cidade[0] and j==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
          
        elif i==rotas_unitarias[cidade_candidata[0]][-1] and i!=rotas_unitarias[cidade_candidata[0]][0]:
          rotas_unitarias[cidade_candidata[0]].append(j)
          for cidade in rotas_unitarias:
            if i in cidade and i==cidade[0] and i==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
        
      elif j==rota[0] and j!=rota[-1]:       #verifica se a cidade que já pertence a rota é um extremo
        cidade_candidata=search(rotas_unitarias,i) #procura onde está a outra cidade
        if i==rotas_unitarias[cidade_candidata[0]][0] and i==rotas_unitarias[cidade_candidata[0]][-1]:
          rota.insert(0,i)   #adiciona somente a cidade que não faz parte da rota ainda
          for cidade in rotas_unitarias:
            if i in cidade and i==cidade[0] and i==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
        elif i==rotas_unitarias[cidade_candidata[0]][0] and i!=rotas_unitarias[cidade_candidata[0]][-1]:
          rotas_unitarias[cidade_candidata[0]].extend(rota)
          rotas_unitarias.remove(rota)  
        elif i==rotas_unitarias[cidade_candidata[0]][-1] and i!=rotas_unitarias[cidade_candidata[0]][0]:
          return rotas_unitarias
      elif  j==rota[-1] and j!=rota[0]:               #verifica se a cidade que já pertence a rota é um extremo
        cidade_candidata=search(rotas_unitarias,j) #procura onde está a outra cidade
        if i==rotas_unitarias[cidade_candidata[0]][0] and i==rotas_unitarias[cidade_candidata[0]][-1]:
          rota.append(i)       #adiciona somente a cidade que não faz parte da rota ainda
          for cidade in rotas_unitarias:
            if i in cidade and i==cidade[0] and i==cidade[-1]:
              rotas_unitarias.remove(cidade)      #Remove a cidade inserida das rotas unitárias
        elif i==rotas_unitarias[cidade_candidata[0]][0] and i!=rotas_unitarias[cidade_candidata[0]][-1]:
          rotas_unitarias[cidade_candidata[0]].insert(0,j)
          for cidade in rotas_unitarias:
            if i in cidade and i==cidade[0] and i==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
          
        elif j==rotas_unitarias[cidade_candidata[0]][-1] and j!=rotas_unitarias[cidade_candidata[0]][0]:
          rotas_unitarias[cidade_candidata[0]].append(i)
          for cidade in rotas_unitarias:
            if j in cidade and j==cidade[0] and j==cidade[-1]:
              rotas_unitarias.remove(cidade)    #Remove a cidade inserida das rotas unitárias
      else:
        return rotas_unitarias  
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
      cidade_candidata=search(rotas_unitarias,j) #procura onde está a outra cidade canditada para verificar se ela já está associada a uma rota
      for cidade in rotas_unitarias[cidade_candidata[0]]:
        demanda_corrente+=volume[cidade-1] #demanda da segunda cidade verificada
      if demanda_corrente<=volume_limite:  #verifica se a demanda atende a restrição de capacidade
        return True
      else:
        return False


def restricao_de_rotas(i, j,rotas_unitarias):
      
  for rota in rotas_unitarias:  
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
