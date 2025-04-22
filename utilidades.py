######################################################## 
# Faculdade: Cesar School                              #
# Período: 2025.1                                      #
# Disciplina: Projeto 1                                #
# Professor: Humberto Caetano                          #
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
# Data: 22/04/2025                                     #
######################################################## 

import hashlib
import bcrypt

# Gerar MD5
def gerar_md5(senha: str) -> str:
    return hashlib.md5(senha.encode('utf-8')).hexdigest()

# Gerar BCrypt
def gerar_hash_bcrypt(senha: str) -> str:
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_hash_bcrypt(senha: str, hashed: str) -> bool:
    return bcrypt.checkpw(senha.encode('utf-8'), hashed.encode('utf-8'))
