######################################################## 
# Projeto: App Denúncia de Bullying Anônima            #
# Descrição: Módulo Denunciante                        #
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

import dados
import utilidades
from pathlib import Path
from datetime import datetime

# Constantes
BANCO_DADOS = "bullying.db"
CAMINHO_BANCO_DADOS = Path(BANCO_DADOS)
FORMATO_DATA = "%d/%m/%Y"

try:
    # Instância do Banco de Dados
    bd = dados.BancoDados(BANCO_DADOS)

    # Verifica se o Banco de Dados existe, se não cria as tabelas.
    if not (CAMINHO_BANCO_DADOS.exists()):
        bd.criar_tabelas()

    # Criar Denúncia
    novo_id = bd.criar_denuncia(senha=utilidades.gerar_md5("senha123"), descricao_o_que="Foi feito Bullying de Gordofobia, me chamaram de baleia", descricao_como_se_sente="Me sinto mal", local="Escola", frequencia="Frequentemente", tipo_bullying="Verbal")
    print(f"Novo ID {novo_id}")
    print('-' * 100)

    # Busca Denúncia por Id 
    if novo_id != None:
        denuncia = bd.buscar_denuncia_por_id(novo_id)
        print(denuncia)
        print('-' * 100)

    # Criar Denúncia
    novo_id = bd.criar_denuncia(senha=utilidades.gerar_md5("senha456"), descricao_o_que="Foi feito Bullying de Gordofobia, me chamaram de baleia", descricao_como_se_sente="Me sinto mal", local="Escola", frequencia="Frequentemente", tipo_bullying="Verbal")
    print(f"Novo ID {novo_id}")
    print('-' * 100)

    # Busca Denúncia por Id 
    if novo_id != None:
        denuncia = bd.buscar_denuncia_por_id(novo_id)
        print(denuncia)
        print('-' * 100)

    # Listar Denúncias Geral
    denuncias = bd.listar_denuncias()
    print(denuncias)
    print('-' * 100)

    # Listar Denúncias Intervalo de Datas
    data_inicio = datetime.strptime("17/04/2025", FORMATO_DATA)
    data_fim = datetime.strptime("18/04/2025", FORMATO_DATA)
    denuncias = bd.listar_denuncias(data_inicio=data_inicio, data_fim=data_fim)
    print(denuncias)
    print('-' * 100)

    # Listar Denúncias Status
    status = ('Aberta', 'Em Atendimento', 'Encerrada')
    denuncias = bd.listar_denuncias(status=status)
    print(denuncias)
    print('-' * 100)

    # Listar Denúncias Intervalo de Datas e Status
    data_inicio = datetime.strptime("17/04/2025", FORMATO_DATA)
    data_fim = datetime.strptime("18/04/2025", FORMATO_DATA)
    status = ('Aberta', 'Em Atendimento', 'Encerrada')
    denuncias = bd.listar_denuncias(data_inicio=data_inicio, data_fim=data_fim, status=status)
    print(denuncias)
    print('-' * 100)

except Exception as e:
    print(f"Erro: {e}")
