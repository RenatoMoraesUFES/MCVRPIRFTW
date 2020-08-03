def menordistancia (dic_instancia, configuracoes):

    #Função para calcular um solução viável para o problema do caxeiro viajante utilizando como base o exemplo do vizinho mais proximo

    D= dic_instancia["distancia"]
    #print("\n","D: ", D, "\n")
    visitadas=[0] #cidades que o caxeiro já passou
    custo=0       #Custo da viagem
    N=list(range(0,len(D)-1)) #lista as cidades que faltam ser visitadas
    N.remove(0)                      #Remove a primeira cidade pois é de onde o caxeiro está partindo
    i=0
    #print("Cidades visitadas: ", visitadas)
    #print("Custo da viagem: R$", custo)
    #print("Cidades que ainda precisam ser visitadas: ",N)
    #print("Localização atual: Cidade ", i, "\n")
    
    while(N!=[]):
        distancia_corrente=D[i][:]             #recebe todo os valores referentes as cidades que podem ser visitadas da cidade em que ooo caxeiro esta
       # print("distancias corrente: ", distancia_corrente)
        valorminimo=min(distancia_corrente) #identifica dentro da lista criada na linha acima qual cidade tem o menor custo de deslocamento
        posi_min=distancia_corrente.index(valorminimo)  #recebe o numero da cidade que tem o custo minimo
        #print("posição do valor minimo: ", posi_min, "\n")
 

        while(posi_min in visitadas):  #esse comando foi criado para que nenhuma cidade já visitada possa ter seu percurso analisado
            distancia_corrente[posi_min]=valorminimo+9999    #torna o valor minimo encontrado um valor alto fazendo com que seja eliminado da visita
            #print("Novas distancias corrente: ", distancia_corrente)
            valorminimo=min(distancia_corrente)
            #print("valorm: ",valorminimo)
            posi_min=distancia_corrente.index(valorminimo)  #recebe a posicao do valor minimo encontrado que foi acrescido com o valor 999
            #print("posi_min: ", posi_min)
    
        #ultimo=[j for j, valor in enumerate(distancia_corrente) if valor==valorminimo] #essa linha faz a comparação entre os valores repetidos e guarda o ultimo analisado
        #posi_min=distancia_corrente.index(ultimo)
        #print("Ultima ocorrencia: ",ultimo)

        #posi_min=ultimo[len(ultimo)-1]
        visitadas.append(posi_min)      #está acrescentando o número da cidade na lista de cidades visitadas 
        custo+=valorminimo              #soma o valor gasto até o momento com a viagem com o novo valor encontrado
        N.remove(posi_min)              #remove o numero da cidade da lista das que faltam ser visitadas
        i=posi_min                      #recebe o valor da localização atual do caxeiro

        #print("Cidades visitadas: ", visitadas)
        #print("Custo da viagem: R$", custo)
        #print("Cidades que ainda precisam ser visitadas: ",N)
        #print("Localização atual: Cidade ", i, "\n")
    distancia_corrente=D[i] [:]    #recebe os valores da ultima coluna(cidade) para que seja identificado o valor de retorno para a cidade de partida
    custo+=distancia_corrente[0]   #recebe o valor referente a viagem do ultimo ponto ate o ponto de partida
    #print("Cidades visitadas: ", visitadas)
    #print("Custo total da viagem R$",custo)

    return visitadas, custo #envia a função para o local que for chamada  

