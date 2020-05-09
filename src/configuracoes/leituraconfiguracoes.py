import os
from bin.configuracoes import *

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

def leitura_config():
    """ Funcao de leitura de configuracao
        Le o arquivo 'configuracoes.py' com os parametros a serem executados
        Verifica se eh 1 (True) ou (0) False
        E armazena numa lista os parametros
    """
    
    global dic_configuracoes
    
    funcoes = []
    for parametro in dic_configuracoes:
        if dic_configuracoes[parametro] == 1:
            funcoes.append(parametro)
    return funcoes
###############################################################################
