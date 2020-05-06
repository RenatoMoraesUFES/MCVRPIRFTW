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
# Funcao de leitura arquivo 'input.config'.
# Funcao le arquivo de entrada com nomes dos arq '.dat' a serem lidos,
# armazena nomes de entrada seguidos de 1 e ignora os  seguidos de 0
# retorna uma lista com os nomes de arquivos a serem lidos.

def leitura_config(config):
    """ Funcao de leitura de configuracao
        Le o arquivo 'executar.config' com os parametros a serem executados
        Verifica se eh 1 (True) ou (0) False
        E armazena numa lista os parametros
    """

    funcoes = []
    file = open(config)
    linha = file.readline()
    while linha:
        if not linha.startswith("###"):
            valor = linha.split()
            if valor[1] == '1':
                funcoes.append(valor[0])
        linha = file.readline()
    return funcoes
###############################################################################
