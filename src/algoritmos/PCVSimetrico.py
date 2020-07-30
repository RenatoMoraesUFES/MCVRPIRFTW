
def buscalocalcaxeiro(dic_instancia,visitadas,custo):
    
  #Função para encontrar solucoes viáveis trocando a posição de uma cidade da solução viável já obtida
  
  distancias= dic_instancia['distancia'] #Busca a matriz de distancias
  #print("distancias: ", distancias)
  solucaoviavel=visitadas[:] #Busca a solução viável encontrada no código do pcv
  #print('solucaoviavel:',solucaoviavel,"\n")
  custos= custo #Busca o custo da solução viável obtida
  #print("custos:",custos)

  melhoria=True
  minlocal=[]
  novocusto=0
  melhorvalor=9999
  #print('novocusto:',novocusto)
  n=len(solucaoviavel) #guarda o valor do tamanho da lista analisada
  #print('n:',n)
  j=0
  i=0


  while melhoria:
    solucao=[]
    melhoria=False
    #for i in range (0,n):
    while i<=n-2:
      solucao=solucaoviavel[:]
      reserva=solucao[i]      #Recebe o valor da primeira cidade encontrada na lista
      #print("Reserva:", reserva)
      solucao[i]=solucao[i+1]   #Faz a troca de posição entre duas cidades
      solucao[i+1]=reserva
      #print("Solução", i+1, ": ", solucao)
      #print('i:',i)

      for k in range(0,n):  #Esse bloco recalcula o custo da viagem
        j=k+1
        if j== n:
          chegada=solucao[k-n]
          novocusto+=distancias[k][chegada]
          #print('Novo custo: R$', novocusto)
        else:
          partida=solucao[k]
         #print('partida:',partida)
          chegada=solucao[j]
          #print('chegada:',chegada)
          novocusto+=distancias[partida][chegada]  #encontra o valor da viagem utilizando a posicao da cidade de partida e de chegada na matriz
          #print('Novo custo: R$', novocusto)
      #print('Novo custo: R$', novocusto,"\n")


      if novocusto<melhorvalor and novocusto>0: #Compara o custo minimo que já havia sido encontrado coom o novo valor obtido com a troca das cidades
        minlocal=solucao
        #print('minlocal:',minlocal,"\n")
        melhorvalor=novocusto
        #print('melhor valor: ',melhorvalor,"\n")
      novocusto=0
      i+=1

    if custos>melhorvalor:
      solucaoviavel=minlocal
      custos=melhorvalor
      melhoria=True
  #print('melhor solucao:', solucaoviavel)

  return solucaoviavel,custos
