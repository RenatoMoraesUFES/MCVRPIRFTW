import os


###############################################################################
# Funcao de escrita em um novo arquivo dos dados obtidos na funcao leitura
# Abro um arquivo de saida e percorro todo o arquivo texto
# Escrevo como copia identica do arquivo original
# Inicio escrita

def Escrita(texto, dic_instancia):
	
			
    entrada    = dic_instancia["nome_instancia"]          #             # nome do arquivo .dat da instancia			
    nos        = dic_instancia["clientes"]                # quantidade de clientes (int) 
    nosf       = dic_instancia["facilidades"]             # quantidade facilidades (int)
    m          = dic_instancia["num_veiculo_frota"]       # numero de veiculos da frota(int) 
    ncp        = dic_instancia["num_max_compartimentos"]  # número máximo de compartimentos(int) 
    M          = dic_instancia["M_grande"]                # parâmetro auxiliar  um número "muito grande" (int)
    distancia  = dic_instancia["distancia"]               # distancia em km (ou custo) do arco i j  onde i e j podem ser clientes e/ou facilidades. (float)
    t          = dic_instancia["tempo"]                   # matriz tempo em horas de i para j  onde i e j podem ser clientes e/ou facilidades (lista de lista float - matriz)
    wti        = dic_instancia["janela_cliente_inicio"]   # inicio da janela de tempo cliente (lista int)
    wtf        = dic_instancia["janela_cliente_fim"]      # fim da janela de tempo cliente (lista int)    
    ot         = dic_instancia["tempo_operacao_caixa"]    # tempo médio de operação de uma caixa (h) (0.02h = 1.2min) (float)
    N          = dic_instancia["num_caixas"]              # Numero de caixas (int)
    prop       = dic_instancia["caixas_do_cliente"]       # Qual caixa pertence a qual cliente (lista de lista boolean - matriz) "Boolean type can only be one of True or False"
    vlb        = dic_instancia["volume_caixa"]            # volumes das caixas (lista float)        
    vlc        = dic_instancia["num_caixa_maior_cliente"] # soma dos numeros de caixa do maior cliente (lista de lista float - matriz)
    ck         = dic_instancia["custo_fixo_bike"]         # custo fixo das bicicletas (lista int)
    cd         = dic_instancia["custo_km_rodado"]         # custo por km rodado (lista float)				
				
				
				
    if not os.path.exists('OUTPUT'):    #se o caminho não existe
        os.makedirs('OUTPUT')           #crio um diretorio
    os.chdir('OUTPUT')      #entro para escrita do arquivo de saida
    saida = entrada + '.out' # define nome do arquivo de saida
    fout = open(saida, 'w')
    #percorrer todo o texto inutil
    for linha in texto: # linha eh uma lista de strings
        #reconstruo linha com strings da lista e separadas por espaco
        #print(' '.join(linha))
        #se encontro 'nos' recupero dados na memoria
        if (linha[0] == 'nos'):
            #crio linha igual arquivo original
            fout.write(linha[0]+ " = " + str(nos) +';\n\n')
        elif (linha == 'nosf'):
            fout.write(linha+ " = " + str(nosf) +';\n\n')   
        elif (linha[0] == 'm'):
            fout.write(linha[0]+ " = " + str(m) +';\n\n')
        elif (linha == 'ncp'):
            fout.write(linha+ " = " + str(ncp) +';\n\n')
        elif (linha[0] == 'M'):
            fout.write(linha[0]+ " = " + str(M) +';\n\n')
        elif (linha == 'ot'):
            fout.write(linha+ " = " + str(ot) +';\n\n')
        elif (linha[0] == 'N'):
            fout.write(linha[0]+ " = " + str(N) +';\n\n')
        elif (linha == 'distancia'):  #recuperando a lista de listas na memoria
            #print(linha)
            fout.write(linha+ " = [\n")  #crio linha igual a de entrada
            for i in distancia:  #percorro cada lista da lista distancia
                if i != []:
                    fout.write('[	')         
                    for j in i:             #percorro cada item da lista
                        if type(j) == int:
                            fout.write(str(j)+'	')
                        else:
                            fout.write("%.3f	" %j)
                    fout.write(']\n')  
            fout.write("            ];\n\n")  #crio linha igual arqvo origem
        elif (linha == 't'):
            #print(linha)
            fout.write(linha+ " = [\n")
            for i in t:
                if i != []:
                    fout.write('[	')
                    for j in i:
                        if type(j) == int:
                            fout.write(str(j)+'  ')
                        else:
                            fout.write("%.3f   " %j)
                    fout.write(']\n')
            fout.write("            ];\n\n")
        elif (linha == 'prop'):
            #print(linha)
            fout.write(linha+ " = [\n")
            for i in prop:
                if i != []:
                    fout.write('[	')
                    for j in i:
                        fout.write(str(j) + '	')
                    fout.write(']\n')
            fout.write("];\n\n")
        elif (linha == 'vlc'):
            #crio linha igual arqvo original
            fout.write(linha+ " = [ " + texto[texto.index('vlc')+1] + "\n")
            for i in vlc:
                if i != []:
                    fout.write('[ ')
                    for j in i:
                        fout.write(str(j) + '  ')
                    fout.write(']\n')
            fout.write("];\n\n")
        elif (linha == 'wti'):  #acho lista no texto
            fout.write(linha+" = "+'[ ')
            for i in wti:     #percorro lista 'wti'
                fout.write(str(i)+'	')  #escrevo cada item na forma de str
            fout.write('];\n\n')            #fecho a lista
        elif (linha == 'wtf'):
            fout.write(linha+" = "+'[ ')
            for i in wtf:
                fout.write(str(i)+'	')
            fout.write('];\n\n')
        elif (linha == 'vlb'):
            fout.write(linha+" = "+'[ ')
            for i in vlb:
                fout.write(str(i)+' ')
            fout.write('];\n\n')
        elif (linha == 'ck'):
            fout.write(linha+" = "+'[')
            for i in ck:
                fout.write(str(i)+' ')
            fout.write('];\n')
        elif (linha == 'cd'):
            fout.write(linha+" = "+'[')
            for i in cd:
                fout.write(str(i)+' ')
            fout.write('];\n\n')
        #caso particular de texto inutil que surge dentro da variavel 'vlc'
        elif not(' '.join(linha).startswith('/ / ( s')):
            fout.write(' '.join(linha)+'\n')
    fout.close()
    os.chdir('..')
    print("\n\nFIM - verificar arquivo de saida.\n")
#fim escrita
###############################################################################

    
###############################################################################
# Funcao para criar um arquivo de saida '.dot'
# Gera um grafo para a lista de listas 'distancia' pelo graphviz

def Grafo_distancia(dic_instancia):
    caminho = 'OUTPUT'
    name = dic_instancia["nome_instancia"]
    distancia = dic_instancia["distancia"]
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    file = caminho + '/' + name + '_DIST.dot'
    #abro um arquivo '.dot' para linguagem graphviz
    arq = open(file, 'w')
    #primeira linha como padrao da linguagem
    arq.write('strict graph {\nsplines="compound"\n')
    for i in range(len(distancia)-1):
        for j in range(len(distancia[i])-1):
            #ignoro as distancias entre si mesmos e as 'infinitas' ditas '9999'
            if not i == j and distancia[i][j] != 9999:
                if distancia[i][j] > 1.655:
                    arq.write(str(i) + '--' + str(j) + ' [color=grey];\n')
                else:
                    #aresta como vertice os indices da matriz distancia
                    arq.write(str(i)
                              + '--'
                              + str(j)
                              + ' [label =  "'
                              + "%.3f" %distancia[i][j]
                              + 'km"];\n')
    arq.write('}')
    arq.close()
    print("\nVerificar arquivo '.dot' de saída.\n")
    
    os.chdir('OUTPUT')
    os.system('dot ' + name + '_DIST.dot -Tpng -o' + name + '_DIST.png')
    #os.system('dot -Kfdp -n -Tpng -o'
     #         + name + '_DIST.png'
      #        + name + '_DIST.dot')
    os.chdir('..')
    print("\nVerificar arquivo '.png' de saída.\n")

    # codigo acima equivale a execucao no terminal:
    # -> dot nomedoarquivo.dot -Tpng -o nomedografo.png
###############################################################################

###############################################################################
# Funcao para criar um arquvivo de saida '.dot'
# Gera um grafo para a lista de listas 'prop'
# Quais caixas (colunas j) pertencem a quais clientes (linhas i) da matriz prop

def Grafo_caixas_do_cliente(dic_instancia):
    caminho = 'OUTPUT'
    name = dic_instancia["nome_instancia"]
    prop = dic_instancia["caixas_do_cliente"]
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    file = caminho + '/' + name + '_caixas_do_cliente.dot'

    arq = open(file, 'w')
    arq.write('strict graph {\n')
    arq.write('rankdir = LR;\n')
    for i in range(len(prop)-1):
        cliente = str(i) + ' [label = "Cliente ' + str(i) + '"];\n'
        arq.write(cliente)
        for j in range(len(prop[i])):
            if prop[i][j] == 1:
                caixa = str(str(i)
                            + str(j)
                            + ' [label = "Caixa '
                            + str(j)
                            + '", shape=box];\n')
                arq.write(caixa)
                arq.write(str(i) + '--' + str(i) + str(j) + ' ;\n')
    arq.write('}')
    arq.close()
    print("\nVerificar '.dot' arquivo de saída.\n")
    
    os.chdir('OUTPUT')
    os.system('dot ' + name + '_caixas_do_cliente.dot -Tpng -o' + name + '_caixas_do_cliente.png')
    os.chdir('..')
    print("\nVerificar arquivo '.png' de saída.\n")

