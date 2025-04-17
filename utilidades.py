######################################################## 
# Projeto: App Denúncia de Bullying Anônima            #
# Descrição: Utilidades                                #
# Equipe:                                              #
#           Artur Cavalcanti                           #
#           Eduardo Henrique Ferreira Fonseca Barbosa  #
#           Evandro José Rodrigues Torres Zacarias     #
#           Gabriel de Medeiros Almeida                #
#           Maria Clara Miranda                        #
#           Mauro Sérgio Rezende da Silva              #
#           Silvio Barros Tenório                      #
# Versão: 1.0                                          #
# Data: 17/04/2025                                     #
######################################################## 

import hashlib

# Gerar MD5
def gerar_md5(senha: str) -> str:
    return hashlib.md5(senha.encode('utf-8')).hexdigest()
