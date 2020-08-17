def savings(dic_instancia):
    d = dic_instancia["distancia"]
    n_clientes = dic_instancia["clientes"] #numero de clientes
    cv = 100 #capacidade do veiculo
    #inicialmente vou assumir que cada veiculo é igual para facilitar a implementação e que temos infinitos veiculos
    #sem armazem intermediario por enquanto
    rota_inicial = [d[0][i] + d[i][-1] for i in range(1, n_clientes + 1)] # 0 -> i -> 0
    rota_final = []
    ocupacao_rota = [0]*n_clientes #volume total em cada rota
    savings = []
    for i in range(1, n_clientes + 1):
        for j in range(i + 1, n_clientes + 1):
            if d[i][j] != 9999:
                savings += [(d[i][-1] + d[0][j] - d[i][j], i-1, j-1)] #economia ao mesclar i com j
    savings.sort(reverse=True) #ordena decrescentemente pela economia
    # print(savings)
    # print("nclientes = %d \n" %n_clientes)
    cnt = 0
    tem_rota = [-1]*n_clientes #rota que o cliente pertence, -1 se nao esta em nenhuma
    vol_cliente = [0]*n_clientes
    for i in range(n_clientes):
        for j in range(len(dic_instancia["caixas_do_cliente"][i])):
            vol_cliente[i] += (dic_instancia["caixas_do_cliente"][i][j])*dic_instancia["volume_caixa"][j]
    # print(vol_cliente)
    for par in savings: #falta tratar os veiculos
        i, j = par[1], par[2]
        # i -= 1
        # j -= 1
        if tem_rota[i] != -1 and tem_rota[j] != -1: # se ambos tiverem rota
            continue
        elif tem_rota[i] == -1 and tem_rota[j] == -1 and cv >= vol_cliente[i] + vol_cliente[j]: #criando nova rota com 0->i->j->0
            rota_final += [[i, j]]
            tem_rota[i], tem_rota[j] = cnt, cnt
            ocupacao_rota[cnt] = vol_cliente[i] + vol_cliente[j]
            cnt += 1
        elif tem_rota[i] == -1 and tem_rota[j] != -1 and ocupacao_rota[tem_rota[j]] + vol_cliente[i] <= cv: # se i nao tem rota e j tem
            if j == rota_final[tem_rota[j]][0]: # se j for o primeiro da rota, inserir i antes
                rota_final[tem_rota[j]] = [i] + rota_final[tem_rota[j]]
            elif j == rota_final[tem_rota[j]][-1]: # se j for o ultimo da rota, inserir i no final
                rota_final[tem_rota[j]] = rota_final[tem_rota[j]] + [i]
            else:
                continue
            ocupacao_rota[tem_rota[j]] += vol_cliente[i]
            tem_rota[i] = tem_rota[j]
        elif tem_rota[j] == -1 and tem_rota[i] != -1 and ocupacao_rota[tem_rota[i]] + vol_cliente[j] <= cv: # se j nao tem rota e i tem
            if i == rota_final[tem_rota[i]][0]:
                rota_final[tem_rota[i]] = [j] + rota_final[tem_rota[i]]
            elif i == rota_final[tem_rota[i]][-1]:
                rota_final[tem_rota[i]] = rota_final[tem_rota[i]] + [j]
            else:
                continue
            ocupacao_rota[tem_rota[i]] += vol_cliente[j]
            tem_rota[j] = tem_rota[i]
    for i in range(n_clientes): #quem ficou sem rota vai ficar sozinho
        if tem_rota[i] == -1:
            rota_final += [[i]]
            ocupacao_rota[cnt] += vol_cliente[i]
            tem_rota[i] = cnt
            cnt += 1
    custo = 0
    for v in rota_final:
        for i in range(len(v)-1):
            custo += d[v[i]+1][v[i+1]+1]
        custo += d[0][v[0]+1] + d[v[-1]+1][-1]

    return rota_final, custo
