def menordistancia (dic_instancia, configuracoes):

    #Função para calcular um solução viável para o problema do caxeiro viajante utilizando como base o exemplo do vizinho mais proximo

    D= dic_instancia["distancia"]
    visitadas=[1] #cidades que o caxeiro já passou
    custo=0       #Custo da viagem
    N=list(range(1,len(D)-1)) #lista as cidades que faltam ser visitadas
    N.remove(1)                      #Remove a primeira cidade pois é de onde o caxeiro está partindo
    i=1
    print("Cidades visitadas: ", visitadas)
    print("Custo da viagem: R$", custo)
    print("Cidades que ainda precisam ser visitadas: ",N)
    print("Localização atual: Cidade ", i)

    while(N!=[]):
        distancia_corrente=D[i]             #recebe todo os valores referentes as cidades que podem ser visitadas da cidade em que ooo caxeiro esta
        valorminimo=min(distancia_corrente) #identifica dentro da lista criada na linha acima qual cidade tem o menor custo de deslocamento
        posi_min=distancia_corrente.index(valorminimo)  #recebe o numero da cidade que tem o custo minimo
        while(posi_min in visitadas):                   #esse comando foi criado para que nenhuma cidade já visitada possa ter seu percurso analisado
            distancia_corrente=D[i]
            valorminimo=min(distancia_corrente)
            distancia_corrente[posi_min]=valorminimo+999    #torna o valor minimo encontrado um valor alto fazendo com que seja eliminado da visita
            posi_min=distancia_corrente.index(valorminimo)  #recebe a posicao do valor minimo encontrado que foi acrescido com o valor 999
    
    
        ultimo=[j for j, valor in enumerate(distancia_corrente) if valor==valorminimo] #essa linha faz a comparação entre os valores repetidos e guarda o ultimo analisado
        posi_min=distancia_corrente.index(ultimo)
        print("Ultima ocorrencia: ",ultimo)
    
        visitadas.append(posi_min)      #está acrescentando o número da cidade na lista de cidades visitadas 
        custo+=valorminimo              #soma o valor gasto até o momento com a viagem com o novo valor encontrado
        N.remove(posi_min)              #remove o numero da cidade da lista das que faltam ser visitadas
        i=posi_min                      #recebe o valor da localização atual do caxeiro
        print("Cidades visitadas: ", visitadas)
        print("Custo da viagem: R$", custo)
        print("Cidades que ainda precisam ser visitadas: ",N)
        print("Localização atual: Cidade ", i)
        distancia_corrente=D[i]     #recebe os valores da ultima coluna(cidade) para que seja identificado o valor de retorno para a cidade de partida
        custo+=distancia_corrente[1]   #recebe o valor referente a viagem do ultimo ponto ate o ponto de partida
        return dic_instancia #envia a função para o local que for chamada  

