######################################################## 
# Faculdade: Cesar School                              #
# Período: 2025.1                                      #
# Disciplina: Projeto 1                                #
# Professor: Humberto Caetano                          #
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
# Data: 22/04/2025                                     #
######################################################## 

import dados
import utilidades
import flet as ft
import re
from pathlib import Path
from datetime import datetime

# Constantes
BANCO_DADOS = "bullying.db"
CAMINHO_BANCO_DADOS = Path(BANCO_DADOS)
FORMATO_DATA = "%d/%m/%Y"

# Variáveis Globais
denuncia_id = 0

# Função de Início da Aplicação
def main(page: ft.Page):
    try:
        # Instância do Banco de Dados
        bd = dados.BancoDados(BANCO_DADOS)
        print("[Banco de Dados Instânciado]")

        # Verifica se o Banco de Dados existe, se não cria as tabelas.
        if not (CAMINHO_BANCO_DADOS.exists()):
            print("[Criar Tabelas]")
            bd.criar_tabelas()

        # Título do App
        page.title = "Denúncia de Bullying Anônima - Módulo Denunciante  [V.1.0]"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20

        # Evento de mudança de 
        def route_change(e):
            global denuncia_id
            global denuncia

            page.views.clear()

            # Validar N° Denúncia
            def validar_n_denuncia(e):
                nonlocal n_denuncia_valida
                n_denuncia_valida = False
                lb_erro.value = ""
                # Verifica se é composto apenas por dígitos
                if not re.match(r'^\d+$', tf_n_denuncia.value):  # type: ignore
                    tf_n_denuncia.error_text = "Digite apenas números inteiros positivos"
                else:
                    # Converte para inteiro e verifica se é maior que zero
                    try:
                        num = int(tf_n_denuncia.value)  # type: ignore
                        if num <= 0:
                            tf_n_denuncia.error_text = "O número deve ser maior que zero"
                        else:
                            tf_n_denuncia.error_text = None
                            n_denuncia_valida = True
                    except:
                        tf_n_denuncia.error_text = "Número da denúncia inválido"
                validar_login()   
                page.update()

            # Validar Senha
            def validar_senha(e):
                nonlocal senha_valida
                senha_valida = False
                senha = tf_senha.value
                erros = []
                lb_erro.value = ""
                # Verifica cada requisito individualmente
                if senha:
                    if len(senha) < 8:
                        erros.append("Mínimo 8 caracteres")
                    if not re.search(r'[A-Z]', senha):
                        erros.append("Pelo menos 1 letra maiúscula")
                    if not re.search(r'[a-z]', senha):
                        erros.append("Pelo menos 1 letra minúscula")
                    if not re.search(r'[0-9]', senha):
                        erros.append("Pelo menos 1 número")
                    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
                        erros.append("Pelo menos 1 símbolo especial")
                else:
                    erros.append("Senha requerida")
                if erros:
                   senha_valida = False
                   tf_senha.error_text = "Senha inválida"
                else:
                   senha_valida = True
                   tf_senha.error_text = None
                validar_login()   
                page.update()

            # Validar login
            def validar_login():
                nonlocal n_denuncia_valida
                nonlocal senha_valida
                login_validado = all([
                    n_denuncia_valida,
                    senha_valida
                ])
                bt_login.disabled = not login_validado

            # Acompanhar Denúncia de Bullying (Login)
            def acompanhar_login(e):
                global denuncia_id
                denuncia_id = 0
                denuncia = bd.verificar_login_denuncia(denuncia_id=int(tf_n_denuncia.value)) # type: ignore
                # print(denuncia)
                if denuncia == None:
                    lb_erro.value = "Login inválido"
                    page.update()
                    return None
                else:
                    if utilidades.verificar_hash_bcrypt(tf_senha.value, denuncia["Senha"]): # type: ignore
                        denuncia_id = denuncia["DenunciaId"]
                        return page.go("/acompanhar")
                    else:
                        lb_erro.value = "Login inválido [Autenticação]"
                        page.update()
                        return None

            # Validar Comentário
            def validar_comentario(e):
                nonlocal comentario_valida
                comentario_valida = False
                comentario = tf_comentario.value
                erros = []
                # Verifica cada requisito individualmente
                if comentario:
                    if len(comentario) < 1:
                        erros.append("Mínimo 1 caractere")
                else:
                    erros.append("Comentário requerido")
                if erros:
                   comentario_valida = False
                   tf_comentario.error_text = "Comentario inválido"
                else:
                   comentario_valida = True
                   tf_comentario.error_text = None
                bt_salvar_comentario.disabled = not comentario_valida
                page.update()

            # Acompanhar Denúncia de Bullying (Novo Comentário)
            def novo_comentario(e):
                global denuncia_id
                denuncia = bd.buscar_denuncia_por_id(denuncia_id)
                if denuncia != None:
                    bd.criar_denuncia_comentario(denuncia_id, tf_comentario.value, 0, denuncia["Status"]) # type: ignore
                return page.go("/acompanhar")

            # Página Inicial
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(title=ft.Text("Denúncia de Bullying Anônima"), bgcolor=ft.Colors.RED_300),
                        ft.Row(
                                controls=[ft.Image(src="assets/logo.jpg", width=200,height=200)],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                        ),
                        ft.Row(
                                controls=[ft.ElevatedButton("Fazer Denúncia de Bullying Anônima", on_click=lambda _: page.go("/denuncia"), icon=ft.Icons.APP_REGISTRATION)],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                        ),
                        ft.Row(
                                controls=[ft.ElevatedButton("Acompanhar Denúncia de Bullying", on_click=lambda _: page.go("/acompanharlogin"), icon=ft.Icons.APPS_OUTAGE)],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                        ),
                        ft.Row(
                                controls=[ft.ElevatedButton("Materiais Educativos", on_click=lambda _: page.go("/materiaiseducativos"), icon=ft.Icons.CASES_ROUNDED)],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                        ),
                    ],
                )
            )
            # Página Fazer Denúncia de Bullying Anônima
            if page.route == "/denuncia":
                page.views.append(
                   ft.View(
                        "/denuncia",
                        [
                            # ft.AppBar(title=ft.Text("Fazer Denúncia de Bullying Anônima"), bgcolor=ft.Colors.RED_300),
                            ft.AppBar(
                                title=ft.Text("Fazer Denúncia de Bullying Anônima"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/"),  # Comportamento de voltar padrão
                                ),
                                bgcolor=ft.Colors.RED_300,
                            ),
                            ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/")),
                        ],
                    )
            )
            # Página Acompanhar Denúncia de Bullying Login
            if page.route == "/acompanharlogin":
                n_denuncia_valida = False
                senha_valida = False
                tf_n_denuncia = ft.TextField(label="Número da Denúncia", on_change=validar_n_denuncia, keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter())
                tf_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, on_change=validar_senha)
                lb_erro = ft.Text("", color=ft.Colors.RED)
                bt_login = ft.ElevatedButton("Login", on_click=acompanhar_login, icon=ft.Icons.LOCK, disabled=True)
                page.views.append(
                   ft.View(
                        "/acompanharlogin",
                        [
                            ft.AppBar(
                                title=ft.Text("Acompanhar Denúncia de Bullying (Login)"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/"),  # Comportamento de voltar padrão
                                ),
                                bgcolor=ft.Colors.RED_300,
                            ),
                            ft.Row(
                                controls=[ft.Text("Informar o número da denúncia e a senha para fazer o login e poder ter acesso ao acompanhamento da denúncia.", weight=ft.FontWeight.BOLD)],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                controls=[tf_n_denuncia],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                controls=[tf_senha],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                controls=[lb_erro],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                # controls=[ft.ElevatedButton("Login", on_click=lambda _: page.go("/acompanhar"))],
                                controls=[bt_login],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                        ],
                    )
            )
            # Página Acompanhar Denúncia de Bullying
            if page.route == "/acompanhar":
                # print(denuncia_id)
                denuncia = bd.buscar_denuncia_por_id(denuncia_id)
                # print(denuncia)
                tf_v_n_denuncia = ft.TextField(label="Número da Denúncia", value=str(denuncia_id), read_only=True)
                # tf_v_datahora = ft.TextField(label="Data e Hora", value=denuncia["DataHora"], read_only=True) # type: ignore
                tf_v_datahora = ft.TextField(label="Data e Hora", value=datetime.fromisoformat(denuncia["DataHora"]).strftime('%d/%m/%Y %H:%M:%S'), read_only=True) # type: ignore
                tf_v_descricao_o_que = ft.TextField(label="Descrição - O que?", value=denuncia["DescricaoOque"], read_only=True, multiline=True, width=610) # type: ignore
                tf_v_descricao_como_se_sente = ft.TextField(label="Descrição - Como se sente?", value=denuncia["DescricaoComoSeSente"], read_only=True, multiline=True, width=610) # type: ignore
                tf_v_local = ft.TextField(label="Local", value=denuncia["Local"], read_only=True) # type: ignore
                tf_v_frequencia = ft.TextField(label="Frequência", value=denuncia["Frequencia"], read_only=True) # type: ignore
                tf_v_tipo_bullying = ft.TextField(label="Tipo Bullying", value=denuncia["TipoBullying"], read_only=True) # type: ignore
                cor = ft.Colors.BLACK
                if denuncia["Status"] == "Aberta": # type: ignore
                    cor = ft.Colors.RED
                elif denuncia["Status"] == "Em Atendimento": # type: ignore
                    cor = ft.Colors.BLUE
                elif denuncia["Status"] == "Em Atendimento": # type: ignore
                    cor = ft.Colors.GREEN
                tf_v_status = ft.TextField(label="Status", value=denuncia["Status"], read_only=True, color=cor) # type: ignore
                denuncia_comentarios = bd.listar_denuncias_comentarios_usuario(denuncia_id=denuncia_id)
                bt_novo_comentario = ft.ElevatedButton("Novo Comentário", on_click=lambda _: page.go("/acompanharnovocomentario"), icon=ft.Icons.ADD_COMMENT)
                bt_reuniao = ft.ElevatedButton("Reuniao", on_click=lambda _: page.go("/reuniao"), icon=ft.Icons.INSERT_COMMENT)
                # print(denuncia_comentarios)
                # Criar itens da lista de comentário
                itens_comentarios = []
                for msg in denuncia_comentarios:
                    # Container para cada comentário
                    ct_comentario = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(msg["UsuarioTipo"], weight=ft.FontWeight.BOLD),
                                ft.Text(msg["Comentario"], size=14),
                                ft.Text(datetime.fromisoformat(msg["DataHora"]).strftime('%d/%m/%Y %H:%M:%S'), size=10, color=ft.Colors.GREY),
                            ],
                            spacing=2,
                        ),
                        padding=10,
                        border_radius=10,
                        bgcolor=ft.Colors.BLUE_100 if msg["UsuarioTipo"] == "Denunciante" else ft.Colors.GREEN_100,
                        margin=ft.margin.only(left=50 if msg["UsuarioTipo"] == "Denunciante" else 0, right=0 if msg["UsuarioTipo"] == "Denunciante" else 50),
                        alignment=ft.alignment.center_left if msg["UsuarioTipo"] == "Denunciante" else ft.alignment.center_right,
                        expand=True,
                    )
                    # Adicionar à lista de itens
                    itens_comentarios.append(ct_comentario)
                # Criar ListView com expansão
                lv_comentarios = ft.ListView(
                    controls=itens_comentarios,
                    spacing=10,
                    expand=True,  # Isso faz o ListView ocupar todo o espaço disponível
                    auto_scroll=True,
                )
                page.views.append(
                   ft.View(
                        "/acompanhar",
                        [
                            ft.AppBar(
                                title=ft.Text("Acompanhar Denúncia de Bullying"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/"),  # Comportamento de voltar padrão
                                ),
                                bgcolor=ft.Colors.RED_300,
                            ),
                            # ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_v_n_denuncia, tf_v_datahora],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_descricao_o_que],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_descricao_como_se_sente],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_local, tf_v_frequencia],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_v_tipo_bullying, tf_v_status],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[ft.Text("Comentários", weight=ft.FontWeight.BOLD), bt_novo_comentario, bt_reuniao],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Container(
                                    content=lv_comentarios,
                                    expand=True,
                                    border=ft.border.all(1, ft.Colors.GREY_300),
                                    border_radius=10,
                                    padding=10,
                                ),
                            # ]), expand=True, padding=10),
                        ],
                    )
            )
            # Página Acompanhar Denúncia de Bullying Novo Comentário
            if page.route == "/acompanharnovocomentario":
                comentario_valida = False
                tf_v_n_denuncia = ft.TextField(label="Número da Denúncia", value=str(denuncia_id), read_only=True)
                tf_comentario = ft.TextField(label="Comentário", multiline=True, width=610, on_change=validar_comentario)
                bt_salvar_comentario = ft.ElevatedButton("Salvar Comentário", disabled=True, on_click=novo_comentario, icon=ft.Icons.DATA_SAVER_ON)
                page.views.append(
                   ft.View(
                        "/acompanharnovocomentario",
                        [
                            ft.AppBar(
                                title=ft.Text("Acompanhar Denúncia de Bullying (Novo Comentário)"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/acompanhar"),  # Comportamento de voltar padrão
                                ),
                                bgcolor=ft.Colors.RED_300,
                            ),
                            ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_v_n_denuncia],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_comentario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[bt_salvar_comentario],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            ]), expand=True, padding=10),
                        ],
                   )
            )
            # Página Reunião
            if page.route == "/reuniao":
                page.views.append(
                   ft.View(
                        "/reuniao",
                        [
                            ft.AppBar(
                                title=ft.Text(f"Reunião [Denúncia N° {denuncia_id}]"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/acompanhar"),  # Comportamento de voltar padrão
                                ),
                                bgcolor=ft.Colors.RED_300,
                            ),
                            ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/")),
                        ],
                    )
            )
            # Página Materiais Educativos
            if page.route == "/materiaiseducativos":
                page.views.append(
                   ft.View(
                        "/materiaiseducativos",
                        [
                            ft.AppBar(
                                title=ft.Text("Materiais Educativos"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/"),  # Comportamento de voltar padrão
                                ),
                                bgcolor=ft.Colors.RED_300,
                            ),
                            ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/")),
                        ],
                    )
            )
            page.update()

        # Fechar a view atual e voltar à anterior
        def view_pop(e):
            page.views.pop()
            top_view = page.views[-1]
            if top_view.route:
                page.go(top_view.route)

        # Atribui Eventos
        page.on_route_change = route_change
        page.on_view_pop = view_pop

        page.go(page.route)

    except Exception as e:
        print(f"Erro: {e}")

# Início da Aplicação
if __name__ == '__main__':
    ft.app(target=main)