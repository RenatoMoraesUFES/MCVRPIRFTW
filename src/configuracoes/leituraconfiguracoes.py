import os

###############################################################################

def leitura_input(config):
    """ Funcao de leitura de configuracao
        Le o arquivo 'input.config' com os arquivos '.dat' a serem lidos
        Verifica se eh 1 (True) ou 0 (False)
        Retorna uma lista com os arquivos a serem lidos
    """

    if not os.path.exists('INPUT'):
        print("Diretório de entrada não encontrado.")
        exit()
    os.chdir('INPUT')
    arquivos = []
    try:
        file = open(config)
    except:
        print("Arquivo 'input.config' não encontrado no diretório.")
    linha = file.readline()
    while linha:
        valor = linha.split()
        if valor[1] == '1':
            aux = valor[0]
            aux = aux[:-4]
            arquivos.append(aux)
        linha = file.readline()
    os.chdir('..')
    return arquivos
###############################################################################


###############################################################################

def leitura_config(config):
    """ Funcao de leitura de configuracao
        Le o arquivo 'configuracoes.py' com os parametros a serem executados
        Verifica se eh 1 (True) ou (0) False
        E armazena numa lista os parametros
    """
    
    dic_configuracoes = {
        'imprime_distancia'         : {},
        'imprime_janelas_tempo'     : {},
        'imprime_prop'              : {},
        'imprime_qual_bicicleta'    : {},
        'escrita'                   : {},
        'grafo_distancia'           : {},
        'grafo_caixas_do_cliente'   : {}
        }
    file = open(config)
    linha = file.readline()
    while linha:
        if not linha.startswith("#"):
            valor = linha.split()
            if valor[1] == '1':
                dic_configuracoes[valor[0]] = 1
        linha = file.readline()
    return dic_configuracoes
###############################################################################
