######################################################## 
# Faculdade: Cesar School                              #
# Curso: Segurança da Informação                       #
# Período: 2025.1                                      #
# Disciplina: Projeto 1                                #
# Professor: Humberto Caetano                          #
# Projeto: App Denúncia de Bullying Anônima            #
# Descrição: Testes                                    #
# Equipe:                                              #
#           Artur Cavalcanti                           #
#           Eduardo Henrique Ferreira Fonseca Barbosa  #
#           Evandro José Rodrigues Torres Zacarias     #
#           Gabriel de Medeiros Almeida                #
#           Maria Clara Miranda                        #
#           Mauro Sérgio Rezende da Silva              #
#           Silvio Barros Tenório                      #
# Versão: 1.0                                          #
# Data: 04/05/2025                                     #
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
        print("[Criar Tabelas]")
        bd.criar_tabelas()

    # Criar Denúncia
    print("[Criar Denúncia]")
    # novo_id = bd.criar_denuncia(senha=utilidades.gerar_md5("senha123"), descricao_o_que="Foi feito Bullying de Gordofobia, me chamaram de baleia", descricao_como_se_sente="Me sinto mal", local="Escola", frequencia="Frequentemente", tipo_bullying="Verbal")
    novo_id = bd.criar_denuncia(senha=utilidades.gerar_hash_bcrypt("Senha#123"), descricao_o_que="Foi feito Bullying de Gordofobia, me chamaram de baleia", descricao_como_se_sente="Me sinto mal", local="Escola", frequencia="Frequentemente", tipo_bullying="Verbal")
    print(f"Novo ID {novo_id}")
    print('-' * 100)

    # Busca Denúncia por Id 
    if novo_id != None:
        print("[Busca Denúncia por Id]")
        denuncia = bd.buscar_denuncia_por_id(novo_id)
        print(denuncia)
        print('-' * 100)

    # Criar Denúncia
    print("[Criar Denúncia]")
    # novo_id = bd.criar_denuncia(senha=utilidades.gerar_md5("senha456"), descricao_o_que="Foi feito Bullying de Gordofobia, me chamaram de baleia", descricao_como_se_sente="Me sinto mal", local="Escola", frequencia="Frequentemente", tipo_bullying="Verbal")
    novo_id = bd.criar_denuncia(senha=utilidades.gerar_hash_bcrypt("Senha#456"), descricao_o_que="Foi feito Bullying de Gordofobia, me chamaram de baleia", descricao_como_se_sente="Me sinto mal", local="Escola", frequencia="Frequentemente", tipo_bullying="Verbal")
    print(f"Novo ID {novo_id}")
    print('-' * 100)

    # Busca Denúncia por Id 
    if novo_id != None:
        print("[Buscar Denúncia por Id]")
        denuncia = bd.buscar_denuncia_por_id(novo_id)
        print(denuncia)
        print('-' * 100)

    # Atualizar Denúncia
    print("[Atualizar Denúncia]")
    if novo_id:
        alterou_id = novo_id
    else:
        alterou_id = 1
    status = "Em Atendimento"
    retorno = bd.atualizar_denuncia(denuncia_id=alterou_id, status=status)
    print(f"Atualizou ID {alterou_id}")
    print(f"Retornou {retorno}")
    print('-' * 100)

    # Busca Denúncia por Id 
    if alterou_id != None:
        print("[Buscar Denúncia por Id]")
        denuncia = bd.buscar_denuncia_por_id(alterou_id)
        print(denuncia)
        print('-' * 100)

    # Listar Denúncias Geral
    print("[Listar Denúncias Geral]")
    denuncias = bd.listar_denuncias()
    print(denuncias)
    print('-' * 100)

    # Listar Denúncias Intervalo de Datas
    print("[Listar Denúncias Intervalo de Datas]")
    data_inicio = datetime.strptime("17/04/2025", FORMATO_DATA)
    data_fim = datetime.strptime("19/04/2025", FORMATO_DATA)
    denuncias = bd.listar_denuncias(data_inicio=data_inicio, data_fim=data_fim)
    print(denuncias)
    print('-' * 100)

    # Listar Denúncias Status
    print("[Listar Denúncias Status]")
    status = ('Aberta', 'Em Atendimento', 'Encerrada')
    denuncias = bd.listar_denuncias(status=status)
    print(denuncias)
    print('-' * 100)

    # Listar Denúncias Intervalo de Datas e Status
    print("[Listar Denúncias intervalo de Datas e Status]")
    data_inicio = datetime.strptime("17/04/2025", FORMATO_DATA)
    data_fim = datetime.strptime("19/04/2025", FORMATO_DATA)
    status = ('Aberta', 'Em Atendimento', 'Encerrada')
    denuncias = bd.listar_denuncias(data_inicio=data_inicio, data_fim=data_fim, status=status)
    print(denuncias)
    print('-' * 100)

    # Verificar Login Denúncia
    print("[Verificar Login Denúncia]")
    # denuncia = bd.verificar_login_denuncia(denuncia_id=alterou_id, senha=utilidades.gerar_md5("senha456"))
    denuncia = bd.verificar_login_denuncia(denuncia_id=alterou_id)
    print(f"{denuncia}")
    print('-' * 100)

    # Criar Denúncia
    print("[Criar Denúncia Comentário]")
    comentario_novo_id = bd.criar_denuncia_comentario(denuncia_id=alterou_id, comentario="Comentário 1", usuario_id=0, status="Em Atendimento")
    print(f"Novo ID {comentario_novo_id}")
    print('-' * 100)

    # Criar Denúncia
    print("[Criar Denúncia Comentário]")
    comentario_novo_id = bd.criar_denuncia_comentario(denuncia_id=alterou_id, comentario="Comentário 2", usuario_id=1, status="Em Atendimento")
    print(f"Novo ID {comentario_novo_id}")
    print('-' * 100)

    # Listar Denúncias Comentários Id Denúncia
    print("[Listar Denúncias Comentários Id Denúncia]")
    denuncias_comentarios = bd.listar_denuncias_comentarios(denuncia_id=alterou_id)
    print(denuncias_comentarios)
    print('-' * 100)

    # Listar Denúncias Comentários Id Denúncia e Id Comentário
    print("[Listar Denúncias Comentários Id Denúncia e Id Comentário]")
    denuncias_comentarios = bd.listar_denuncias_comentarios(denuncia_id=alterou_id, denuncia_comentario_id=alterou_id-1)
    print(denuncias_comentarios)
    print('-' * 100)

    # Criar Denúncias Reunião
    print("[Criar Denúncias Reunião]")
    reuniao_novo_id = bd.criar_denuncia_reuniao(denuncia_id=alterou_id, mensagem="Mensagem Denunciante 1", usuario_id=0)
    print(f"Novo ID {reuniao_novo_id}")
    print('-' * 100)

    # Criar Denúncias Reunião
    print("[Criar Denúncias Reunião]")
    reuniao_novo_id = bd.criar_denuncia_reuniao(denuncia_id=alterou_id, mensagem="Mensagem Psicológo 1", usuario_id=1)
    print(f"Novo ID {reuniao_novo_id}")
    print('-' * 100)

    # Listar Denúncias Renião Id Denúncia
    print("[Listar Denúncias Reunião Id Denúncia]")
    denuncias_reuniao = bd.listar_denuncias_reuniao(denuncia_id=alterou_id)
    print(denuncias_reuniao)
    print('-' * 100)

    # Listar Denúncias Renião Id Denúncia e Id Reunião
    if not reuniao_novo_id:
        reuniao_novo_id = 1
    print(reuniao_novo_id)
    print("[Listar Denúncias Reunião Id Denúncia e Id Reunião]")
    denuncias_reuniao = bd.listar_denuncias_reuniao(denuncia_id=alterou_id, denuncia_reuniao_id=reuniao_novo_id-1)
    print(denuncias_reuniao)
    print('-' * 100)

    # Listar Denúncias Renião Id Denúncia e Id Reunião e Data
    data = datetime.strptime("18/04/2025", FORMATO_DATA)
    print(data)
    print("[Listar Denúncias Reunião Id Denúncia e Id Reunião e Data]")
    denuncias_reuniao = bd.listar_denuncias_reuniao(denuncia_id=alterou_id, denuncia_reuniao_id=reuniao_novo_id-1, data=data)
    print(denuncias_reuniao)
    print('-' * 100)

    # Criar Usuário
    print("[Criar Usuário]")
    # usuario_novo_id = bd.criar_usuario(email="msrs@cesar.school", senha=utilidades.gerar_md5("senhaU444"), nome="Mauro Sérgio Rezende da Silva", tipo="Administrador", status="Ativo")
    usuario_novo_id = bd.criar_usuario(email="msrs@cesar.school", senha=utilidades.gerar_hash_bcrypt("senha#U444"), nome="Mauro Sérgio Rezende da Silva", tipo="Administrador", status="Ativo")
    print(f"Novo ID {usuario_novo_id}")
    print('-' * 100)

    # Criar Usuário
    print("[Criar Usuário]")
    # usuario_novo_id = bd.criar_usuario(email="sbt@cesar.school", senha=utilidades.gerar_md5("senhaUSBT1"), nome="Silvio Barros Tenório", tipo="Diretor", status="Ativo")
    usuario_novo_id = bd.criar_usuario(email="sbt@cesar.school", senha=utilidades.gerar_hash_bcrypt("senha#USBT1"), nome="Silvio Barros Tenório", tipo="Diretor", status="Ativo")
    print(f"Novo ID {usuario_novo_id}")
    print('-' * 100)

    # Criar Usuário
    print("[Criar Usuário]")
    # usuario_novo_id = bd.criar_usuario(email="gma@cesar.school", senha=utilidades.gerar_md5("senhaU567"), nome="Gabriel de Medeiros Almeida", tipo="Psicólogo", status="Ativo")
    usuario_novo_id = bd.criar_usuario(email="gma@cesar.school", senha=utilidades.gerar_hash_bcrypt("senha#U567"), nome="Gabriel de Medeiros Almeida", tipo="Psicólogo", status="Ativo")
    print(f"Novo ID {usuario_novo_id}")
    print('-' * 100)

    # Busca Usuário por Id 
    if usuario_novo_id != None:
        print("[Buscar Usuário por Id]")
        usuario = bd.buscar_usuario_por_id(usuario_novo_id)
        print(usuario)
        print('-' * 100)

    # Busca Usuário por Email 
    print("[Buscar Usuário por Email]")
    usuario = bd.buscar_usuario_por_email("sbt@cesar.school")
    print(usuario)
    print('-' * 100)

    # Listar Usuários Geral
    print("[Listar Usuários Geral]")
    usuarios = bd.listar_usuarios()
    print(usuarios)
    print('-' * 100)

    # Listar Usuários Id
    print("[Listar Usuários Id]")
    usuarios = bd.listar_usuarios(usuario_id=1)
    print(usuarios)
    print('-' * 100)

    # Listar Usuários Email
    print("[Listar Usuários Email]")
    usuarios = bd.listar_usuarios(email="msrs@cesar.school")
    print(usuarios)
    print('-' * 100)

    # Listar Usuários Tipo
    print("[Listar Usuários Tipo]")
    usuarios = bd.listar_usuarios(tipo="Administrador")
    print(usuarios)
    print('-' * 100)

    # Listar Usuários Status
    print("[Listar Usuários Status]")
    usuarios = bd.listar_usuarios(status="Ativo")
    print(usuarios)
    print('-' * 100)

    # Atualizar Usuário
    print("[Atualizar Usuário]")
    retorno = bd.atualizar_usuario(2, status="Bloqueado")
    print(f"Atualizou ID 2")
    print(f"Retornou {retorno}")
    print('-' * 100)

    # Listar Usuários Id
    print("[Listar Usuários Id]")
    usuarios = bd.listar_usuarios(usuario_id=2)
    print(usuarios)
    print('-' * 100)

    # Verificar Login Usuário
    print("[Verificar Login Usuário]")
    # usuario = bd.verificar_login_usuario(email="msrs@cesar.school", senha=utilidades.gerar_md5("senhaU444"))
    usuario = bd.verificar_login_usuario(email="msrs@cesar.school")
    print(f"{usuario}")
    print('-' * 100)

    # Verificar Login Usuário
    print("[Verificar Login Usuário]")
    # usuario = bd.verificar_login_usuario(email="gma@cesar.school", senha=utilidades.gerar_md5("senhaU567"))
    usuario = bd.verificar_login_usuario(email="gma@cesar.school")
    print(f"{usuario}")
    print('-' * 100)

    # Deletar Usuário
    # print("[Deletar Usuário Id 1]")
    # retorno = bd.deletar_usuario(1)
    # print(f"{retorno}")
    # print('-' * 100)

    # # Deletar Usuário
    # print("[Deletar Usuário Id 2]")
    # retorno = bd.deletar_usuario(2)
    # print(f"{retorno}")
    # print('-' * 100)

    # # Deletar Usuário
    # print("[Deletar Usuário Id 3]")
    # retorno = bd.deletar_usuario(3)
    # print(f"{retorno}")
    # print('-' * 100)

    # # Deletar Usuário
    # print("[Deletar Usuário Id 1]")
    # retorno = bd.deletar_usuario(1)
    # print(f"{retorno}")
    # print('-' * 100)

    # Criar Material Educativo
    print("[Criar Material Educativo 1]")
    material_novo_id = bd.criar_material_educativo(descricao="M1", link="m1.pdf", usuario_id_criou=1, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    # Criar Material Educativo
    print("[Criar Material Educativo 2]")
    material_novo_id = bd.criar_material_educativo(descricao="M2", link="m2.mov", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    # Criar Material Educativo
    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="M3", link="m3.avi", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    # Busca Material Educativo por Id 
    print("[Buscar Material Educativo por Id]")
    material = bd.buscar_material_educativo_por_id(1)
    print(material)
    print('-' * 100)

    # Listar Material Educativo Geral
    print("[Listar Material Educativo Geral]")
    material = bd.listar_materiais_educativos()
    print(material)
    print('-' * 100)

    # Listar Material Educativo Id
    print("[Listar Material Educativo Id]")
    material = bd.listar_materiais_educativos(material_id=1)
    print(material)
    print('-' * 100)

    # Listar Material Educativo Status
    print("[Listar Material Educativo Status]")
    material = bd.listar_materiais_educativos(status="Ativo")
    print(material)
    print('-' * 100)

    # Atualizar Material Educativo
    print("[Atualizar Material Educativo]")
    retorno = bd.atualizar_material_educativo(2, status="Não Ativo")
    print(f"Atualizou ID 2")
    print(f"Retornou {retorno}")
    print('-' * 100)

    # Busca Material Educativo por Id 
    print("[Buscar Material Educativo por Id]")
    material = bd.buscar_material_educativo_por_id(2)
    print(material)
    print('-' * 100)

    # Deletar Material Educativo
    print("[Material Educativo Id 3]")
    retorno = bd.deletar_material_educativo(3)
    print(f"{retorno}")
    print('-' * 100)

    # Criar Log
    print("[Criar Log]")
    log_novo_id = bd.criar_log(descricao="Log 1", usuario_id=1)
    print(f"Novo ID {log_novo_id}")
    print('-' * 100)

    # Criar Log
    print("[Criar Log]")
    log_novo_id = bd.criar_log(descricao="Log 2", usuario_id=2)
    print(f"Novo ID {log_novo_id}")
    print('-' * 100)

    # Listar Log Geral
    print("[Listar Log Geral]")
    log = bd.listar_log()
    print(log)
    print('-' * 100)

    # Listar Log Geral
    print("[Listar Log Intervalo de Datas]")
    data_inicio = datetime.strptime("18/04/2025", FORMATO_DATA)
    data_fim = datetime.strptime("18/04/2025", FORMATO_DATA)
    log = bd.listar_log(data_inicio=data_inicio, data_fim=data_fim)
    print(log)
    print('-' * 100)


    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.pdf", link="https://drive.google.com/file/d/12zx4dH49ydysy4i5-DeaZjdZUQefIrXH/view?usp=sharing", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)

    print("[Criar Material Educativo 3]")
    material_novo_id = bd.criar_material_educativo(descricao="Este item tem uma descrição mais longa que deve ocupar múltiplas linhas na tabela. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, quis aliquam nisl nunc eu nisl.video", link="https://www.youtube.com/watch?v=mWQoikd72A4", usuario_id_criou=2, usuario_id_alterou=0, status="Ativo")
    print(f"Novo ID {material_novo_id}")
    print('-' * 100)


except Exception as e:
    print(f"Erro: {e}")
