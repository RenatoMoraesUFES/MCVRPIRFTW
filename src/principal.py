### Caso queira testar diretamente desse .py
if __name__ == "__main__":
    import sys
    import os

    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

    from src.variaveis.definicaovariaveis import *
    from src.configuracoes import leituraconfiguracoes
    from src.esinstancias import entradainstancias
    from src.esinstancias import saidainstancias

### usado apenas como biblioteca 
else:
    from src.variaveis.definicaovariaveis import *
    from src.configuracoes import leituraconfiguracoes
    from src.esinstancias import entradainstancias
    from src.esinstancias import saidainstancias

###############################################################################
# Funcao principal para controle do fluxo do programa

def main():
    """ Essa função chama as principais funções de entrada, processamento e saída
	    As variáveis globais estão definidas em src.variaveis.definicaovariaveis"""
	    
	### VARIAVEIS GLOBAIS DEFINIDAS EM src.variaveis.definicaovariaveis ###
    global dic_instancia # armazena todas as informações básicas de uma instância. Informações lidas dos arquivos de entrada.

    ### Carrega do arquivo ./executar.config os parâmetros que caracterizam a execução do programa 
    parametros_de_execucao = leituraconfiguracoes.Leitura_config('executar.config') 
    #print(parametros_de_execucao, end='\n\n\n')

    ### Carrega do arquivo INPUT/input.config as instâncias a serem processadas
    lista_de_instancias = leituraconfiguracoes.Leitura_input('input.config') 
    #print(lista_de_instancias, end='\n\n\n')
    
    
    ### processa todas as instâncias da lista. Uma de cada vez, carregada em instancia_corrente
    for instancia_corrente in lista_de_instancias: 
        #print(dic_instancia, end='\n\n\n')
        try:
			### Dada a instancia_corrente, abro o arquivo .dat e carrego seus dados na memória (dicionario global dic_instancia)
            dic_instancia = entradainstancias.carrega_instancia(instancia_corrente + '.dat')
            dic_instancia_corrente = dic_instancia
            #print(dic_instancia, end='\n\n\n')
            #print(dic_instancia_corrente, end='\n\n\n')

            ### Gera as saidas texto e figuras de acordo com os parametros_de_execucao
            if 'Escrita' in parametros_de_execucao:
                texto = entradainstancias.fazer_copia(dic_instancia_corrente["nome_instancia"] + '.dat')
                saidainstancias.Escrita(texto, dic_instancia_corrente)
            if 'Grafo_distancia' in parametros_de_execucao:
                saidainstancias.Grafo_distancia(dic_instancia_corrente)
            if 'Grafo_caixas_do_cliente' in parametros_de_execucao:
                saidainstancias.Grafo_caixas_do_cliente(dic_instancia_corrente)

            ##### dic_solucao_corrente = algoritmos.construtivo(dic_instancia_corrente, configuracoes)
            
            ##### saidasolucao.cria_grafos(dic_instancia_corrente,dic_solucao_corrente, configuracoes)
            ##### saidasolucao.cria_tabelas(dic_instancia_corrente,dic_solucao_corrente, configuracoes)
            ##### saidasolucao.cria_graficos(dic_instancia_corrente,dic_solucao_corrente, configuracoes)
            ##### saidasolucao.cria_estatisticas(dic_instancia_corrente,dic_solucao_corrente, configuracoes)

        except: continue
###############################################################################

### Caso queira testar diretamente desse .py
### Roda o programa chamando main()
### os arquivos de configuração e o diretório INPUT devem estar disponíveis no diretório do .py
if __name__ == "__main__":
	main()
