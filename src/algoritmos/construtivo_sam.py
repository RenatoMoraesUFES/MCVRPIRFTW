def construtivo(dic_instancia):
    """ Esta função lê o dicionário da instância de entrada e
        retorna a solução final do problema MCVRPIRFTW que
        pretende encontrar uma rota com o menor custo possível
        em que uma bicicleta com multiplos compartimentos,
        convencional ou elétrica, saia do armazém central,
        vá até os clientes e reabasteça em armazéns intermediários
        respeitando uma janela de tempo.
    """

    #busco a matriz distancia no dicionario de entrada para facilitar o nome da variável
    distancia = dic_instancia["distancia"]
    #crio uma matriz para salvar as economias feitas ao colocar
    #os arcos i e j na mesma rota
    economia = []
    #crio um laço para percorrer todas distancias entre os arcos i e j
    for i in range(1, len(distancia)-1):
        economias_i = []
        for j in range(i, len(distancia)-1):
            if i != j and distancia[i][j] != 9999:
                saving = (distancia[0][i]
                          +distancia[0][j]
                          -distancia[i][j])
                economias_i.append(saving)
        economia.append(economias_i)



    
    #print(dic_instancia["nome_instancia"])
    #for linha in economia:
    #    for item in linha:
    #        print(" %.2f " %item, end='')
    #    print("\n")
            
            
