### Caso queira testar diretamente desse .py
if __name__ == "__main__":
    import sys
    import os

    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
    os.chdir('../bin')

    from src.variaveis.definicaovariaveis import *
    from src.configuracoes import leituraconfiguracoes
    from src.esinstancias import entradainstancias
    from src.esinstancias import saidainstancias
    from src.algoritmos import construtivopcv
    from src.algoritmos import construtivo_sam
    from src.algoritmos import buscalocalpcv
    from src.algoritmos import saving

### usado apenas como biblioteca 
else:
    from src.variaveis.definicaovariaveis import *
    from src.configuracoes import leituraconfiguracoes
    from src.esinstancias import entradainstancias
    from src.esinstancias import saidainstancias
    from src.algoritmos import construtivopcv
    from src.algoritmos import construtivo_sam
    from src.algoritmos import buscalocalpcv
    from src.algoritmos import saving

###############################################################################
# Funcao principal para controle do fluxo do programa

def main():
    """ Esta função chama as principais funções de entrada, processamento e saída
	    As variáveis globais estão definidas em src.variaveis.definicaovariaveis
    """
	    
	### VARIAVEIS GLOBAIS DEFINIDAS EM src.variaveis.definicaovariaveis ###
    global dic_instancia # armazena todas as informações básicas de uma instância. Informações lidas dos arquivos de entrada.
    
    ### Carrega do arquivo ./executar.config os parâmetros que caracterizam a execução do programa 
    parametros_de_execucao = leituraconfiguracoes.leitura_config('executar.config')
    #print(parametros_de_execucao, end='\n\n\n')

    ### Carrega do arquivo INPUT/input.config as instâncias a serem processadas
    lista_de_instancias = leituraconfiguracoes.leitura_input('input.config') 
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
            if parametros_de_execucao['escrita'] == 1:
                texto = entradainstancias.fazer_copia(dic_instancia_corrente["nome_instancia"] + '.dat')
                saidainstancias.escrita(texto, dic_instancia_corrente)
            if parametros_de_execucao['grafo_distancia'] == 1:
                saidainstancias.grafo_distancia(dic_instancia_corrente)
            if parametros_de_execucao['grafo_caixas_do_cliente'] == 1:
                saidainstancias.grafo_caixas_do_cliente(dic_instancia_corrente)

            solucao_pcv, custo_pcv = construtivopcv.pcv(dic_instancia_corrente)
            #print(f"Solucao {instancia_corrente} = {solucao_pcv} com custo = %.3f\n" %custo_pcv)
            saidainstancias.grafo_solucao_pcv(dic_instancia_corrente, solucao_pcv)

            sol_bl_pcv, cust_bl_pcv = buscalocalpcv.bl_perm(dic_instancia_corrente, solucao_pcv, custo_pcv)
            #print(f"Solucao BL {instancia_corrente} = {sol_bl_pcv} com custo = %.3f\n" %cust_bl_pcv)
            saidainstancias.grafo_solucao_pcv(dic_instancia_corrente, sol_bl_pcv)

            sol_bl2_pcv, cust_bl2_pcv = buscalocalpcv.bl_2otp(dic_instancia_corrente, solucao_pcv, custo_pcv)
            #print(f"Solucao BL2 {instancia_corrente} = {sol_bl2_pcv} com custo = %.3f\n" %cust_bl2_pcv)

            dic_solucao = saving.construtivo(dic_instancia_corrente)
            #saidainstancias.grafo_savings(dic_instancia_corrente, dic_solucao)
            print(f"Solucao Savings {instancia_corrente} = {dic_solucao}\n")
            
            ##### dic_solucao_corrente = algoritmos.construtivo(dic_instancia_corrente, configuracoes)
            
            ##### saidasolucao.cria_grafos(dic_instancia_corrente,dic_solucao_corrente, configuracoes)
            ##### saidasolucao.cria_tabelas(dic_instancia_corrente,dic_solucao_corrente, configuracoes)
            ##### saidasolucao.cria_graficos(dic_instancia_corrente,dic_solucao_corrente, configuracoes)
            ##### saidasolucao.cria_estatisticas(dic_instancia_corrente,dic_solucao_corrente, configuracoes)

        except Exception as e:
            print(f"\nErro em {instancia_corrente}.")
            print(e, "\n")
            continue
    print("\nFim.\n")
###############################################################################

### Caso queira testar diretamente desse .py
### Roda o programa chamando main()
### os arquivos de configuração e o diretório INPUT devem estar disponíveis no diretório do .py
if __name__ == "__main__":
	main()

