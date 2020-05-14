
##### Insere os caminhos de diretório (ou pastas) das bibliotecas do nosso programa no caminhos do sistema ####
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
#####

from src import principal

# Roda o programa chamando main()
if __name__ == "__main__":
	principal.main() # a função main() da biblioteca principal, organiza o fluxo de execução do programa.

	
