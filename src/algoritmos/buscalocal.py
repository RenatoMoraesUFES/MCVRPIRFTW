import itertools
def busca(dic_instancia, rota, custo):
    #funcao pra busca local trocando consecutivos
    d = dic_instancia["distancia"]
    N = len(rota)
    rota[-1] = N-1
    # print(N)
    melhor = True
    while melhor:
        melhor = False
        melhor_rota, melhor_custo = rota, custo 
        for i in range(1, N-2):
            cur = rota[i]
            prev = rota[i-1]
            nxt = rota[i+1]
            novo_custo = custo - d[prev][cur] - d[cur][nxt] - d[nxt][rota[i+2]] # remove arestas antigas
            novo_custo += d[prev][nxt] + d[nxt][cur] + d[cur][rota[i+2]]    # acrescenta arestas novas
            # print("novo custo = %.3f\n" %novo_custo)
            if novo_custo < melhor_custo and novo_custo > 0:
                melhor_custo = novo_custo
                rota[i], rota[i+1] = rota[i+1], rota[i]
                melhor_rota = rota.copy()
                # print(rota)
                # print()
                rota[i], rota[i+1] = rota[i+1], rota[i]
                melhor = True
        rota = melhor_rota
        custo = melhor_custo
        # print(custo)
    rota[-1] = 0
    return rota, custo

def two_opt(dic_instancia, rota, custo):
    d = dic_instancia["distancia"]
    N = len(rota)
    print(N)
    rota[-1] = N-1
    melhor = True
    while melhor:
        melhor = False
        melhor_rota, melhor_custo = rota, custo
        for i in range(N-3):
            for j in range(i+2, N-1):
                cur, nxt_cur = rota[i], rota[i+1]
                nxt, nxt_nxt = rota[j], rota[j+1]
                rota[i+1], rota[j] = rota[j], rota[i+1]
                novo_custo = 0
                for k in range(N-1):
                    novo_custo += d[k][k+1]
                if novo_custo < melhor_custo:
                    melhor_custo = novo_custo
                    melhor_rota = rota.copy()
                    melhor = True
                rota[i+1], rota[j] = rota[j], rota[i+1]
        rota = melhor_rota
        custo = melhor_custo
    rota[-1] = 0
    return rota, custo

def brute(dic_instancia):
    d = dic_instancia["distancia"]
    N = len(d)
    p = []
    for i in range(1, N-1):
        p += [i]
    melhor_rota, melhor_custo = [], 999999999
    for perm in itertools.permutations(p):
        temp = [0] + list(perm) + [N-1]
        novo_custo = 0
        for i in range(N-1):
            novo_custo += d[temp[i]][temp[i+1]]
        if novo_custo < melhor_custo:
            melhor_custo = novo_custo
            melhor_rota = temp.copy()
        # print(temp)
        # print(novo_custo)
        # print()
    return melhor_rota, melhor_custo
