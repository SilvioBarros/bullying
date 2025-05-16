######################################################## 
# Faculdade: Cesar School                              #
# Curso: Segurança da Informação                       #
# Período: 2025.1                                      #
# Disciplina: Projeto 1                                #
# Professor: Humberto Caetano                          #
# Projeto: App Denúncia de Bullying Anônima            #
# Descrição: Módulo Gerencial                          #
# Equipe:                                              #
#           Artur Cavalcanti                           #
#           Eduardo Henrique Ferreira Fonseca Barbosa  #
#           Evandro José Rodrigues Torres Zacarias     #
#           Gabriel de Medeiros Almeida                #
#           Maria Clara Miranda                        #
#           Mauro Sérgio Rezende da Silva              #
#           Silvio Barros Tenório                      #
# Versão: 1.0                                          #
# Data: 06/05/2025                                     #
######################################################## 

import dados
import utilidades
import flet as ft
from datetime import datetime
from pathlib import Path

# Constantes
BANCO_DADOS = "bullying.db"
CAMINHO_BANCO_DADOS = Path(BANCO_DADOS)

class Gerencial:
    def __init__(self, page: ft.Page):
        self.page = page
        self.bd = dados.BancoDados(BANCO_DADOS)
        self.usuario_logado = None
        self.configurar_pagina()
        self.definir_rotas()

    def configurar_pagina(self):
        self.page.title = "Sistema Gerencial - App Denúncia de Bullying"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def definir_rotas(self):
        self.page.on_route_change = self.rota_change
        self.page.on_view_pop = self.view_pop
        self.page.go("/gerencial/login")

    # Navegação entre páginas
    def rota_change(self, e):
        self.page.views.clear()
        
        # Página de Login
        if self.page.route == "/gerencial/login":
            self.criar_pagina_login()
        
        # Dashboard Principal
        elif self.page.route == "/gerencial/dashboard":
            self.criar_pagina_dashboard()
        
        # Gerenciamento de Denúncias
        elif self.page.route == "/gerencial/denuncias":
            self.criar_pagina_denuncias()
        
        # Detalhes da Denúncia
        elif self.page.route.startswith("/gerencial/denuncia/"):
            denuncia_id = int(self.page.route.split("/")[-1])
            self.criar_pagina_detalhes_denuncia(denuncia_id)
        
        # Gerenciamento de Usuários
        elif self.page.route == "/gerencial/usuarios":
            self.criar_pagina_usuarios()
        
        # Gerenciamento de Materiais
        elif self.page.route == "/gerencial/materiais":
            self.criar_pagina_materiais()
        
        # Visualização de Logs
        elif self.page.route == "/gerencial/logs":
            self.criar_pagina_logs()

        self.page.update()

    def view_pop(self, e):
        self.page.views.pop()
        top_view = self.page.views[-1]
        if top_view.route:
            self.page.go(top_view.route)

    # Componentes Comuns
    def criar_appbar(self, titulo):
        return ft.AppBar(
            title=ft.Text(titulo),
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: self.page.go("/gerencial/dashboard"),
            ),
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE
        )

    # Páginas
    def criar_pagina_login(self):
        self.tf_email = ft.TextField(label="E-mail", width=300)
        self.tf_senha = ft.TextField(label="Senha", password=True, width=300)
        self.lb_erro = ft.Text("", color=ft.colors.RED)

        view = ft.View(
            "/gerencial/login",
            [
                ft.Column(
                    [
                        ft.Row([ft.Image(src="assets/logo_gerencial.jpg", width=200)], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([self.tf_email], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([self.tf_senha], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([self.lb_erro], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row(
                            [ft.ElevatedButton("Entrar", on_click=self.fazer_login)],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    height=self.page.height
                )
            ]
        )
        self.page.views.append(view)

    def criar_pagina_dashboard(self):
        view = ft.View(
            "/gerencial/dashboard",
            [
                self.criar_appbar("Dashboard Gerencial"),
                ft.Row([
                    ft.ElevatedButton("Denúncias", icon=ft.icons.REPORT, on_click=lambda _: self.page.go("/gerencial/denuncias")),
                    ft.ElevatedButton("Usuários", icon=ft.icons.PEOPLE, on_click=lambda _: self.page.go("/gerencial/usuarios")),
                    ft.ElevatedButton("Materiais", icon=ft.icons.LIBRARY_BOOKS, on_click=lambda _: self.page.go("/gerencial/materiais")),
                    ft.ElevatedButton("Logs", icon=ft.icons.ASSIGNMENT, on_click=lambda _: self.page.go("/gerencial/logs")),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ]
        )
        self.page.views.append(view)

    def criar_pagina_denuncias(self):
        denuncias = self.bd.listar_denuncias()
        linhas = []
        
        for d in denuncias:
            linhas.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(d["DenunciaId"])),
                    ft.DataCell(ft.Text(datetime.fromisoformat(d["DataHora"]).strftime('%d/%m/%Y'))),
                    ft.DataCell(ft.Text(d["TipoBullying"])),
                    ft.DataCell(ft.Text(d["Status"], color=self.obter_cor_status(d["Status"]))),
                    ft.DataCell(ft.ElevatedButton("Ver", on_click=lambda e, id=d["DenunciaId"]: self.page.go(f"/gerencial/denuncia/{id}"))),
                ]
            ))

        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Data")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=linhas,
        )

        view = ft.View(
            "/gerencial/denuncias",
            [
                self.criar_appbar("Gerenciamento de Denúncias"),
                ft.Container(
                    content=tabela,
                    padding=20,
                    expand=True
                )
            ]
        )
        self.page.views.append(view)

    def criar_pagina_detalhes_denuncia(self, denuncia_id):
        denuncia = self.bd.buscar_denuncia_por_id(denuncia_id)
        comentarios = self.bd.listar_denuncias_comentarios_usuario(denuncia_id=denuncia_id)

        detalhes = ft.Column([
            ft.Text(f"Denúncia #{denuncia_id}", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(f"Data: {datetime.fromisoformat(denuncia['DataHora']).strftime('%d/%m/%Y %H:%M')}" if denuncia else "Data: Informação indisponível"),
            ft.Text(f"Local: {denuncia['Local']}" if denuncia else "Local: Informação indisponível"),
            ft.Text(f"Status: {denuncia['Status']}" if denuncia else "Status: Informação indisponível", color=self.obter_cor_status(denuncia['Status']) if denuncia else ft.colors.BLACK),
            ft.Divider()
        ])

        comentarios_ui = ft.ListView(expand=True)
        for c in comentarios:
            comentarios_ui.controls.append(
                ft.ListTile(
                    title=ft.Text(c["Comentario"]),
                    subtitle=ft.Text(f"{c['UsuarioTipo']} - {datetime.fromisoformat(c['DataHora']).strftime('%d/%m/%Y %H:%M')}"),
                )
            )

        view = ft.View(
            f"/gerencial/denuncia/{denuncia_id}",
            [
                self.criar_appbar(f"Denúncia #{denuncia_id}"),
                ft.Row([detalhes]),
                ft.Row([ft.Text("Comentários", size=18)]),
                ft.Row([comentarios_ui]),
                ft.Row([
                    ft.ElevatedButton("Alterar Status", on_click=self.mostrar_dialogo_status),
                    ft.ElevatedButton("Adicionar Comentário", on_click=self.mostrar_dialogo_comentario)
                ])
            ]
        )
        self.page.views.append(view)

    # ... (Implementar métodos similares para outras páginas)

    def criar_pagina_logs(self):
        view = ft.View(
            "/gerencial/logs",
            [
                self.criar_appbar("Visualização de Logs"),
                ft.Container(
                    content=ft.Text("Página de Visualização de Logs em construção."),
                    padding=20,
                    expand=True
                )
            ]
        )
        self.page.views.append(view)

    def criar_pagina_materiais(self):
        view = ft.View(
            "/gerencial/materiais",
            [
                self.criar_appbar("Gerenciamento de Materiais"),
                ft.Container(
                    content=ft.Text("Página de Gerenciamento de Materiais em construção."),
                    padding=20,
                    expand=True
                )
            ]
        )
        self.page.views.append(view)

    def criar_pagina_usuarios(self):
        usuarios = self.bd.listar_usuarios()
        linhas = []

        for u in usuarios:
            linhas.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(u["UsuarioId"])),
                    ft.DataCell(ft.Text(u["Nome"])),
                    ft.DataCell(ft.Text(u["Email"])),
                    ft.DataCell(ft.Text(u["Tipo"])),
                    ft.DataCell(ft.ElevatedButton("Editar", on_click=lambda e, id=u["UsuarioId"]: self.editar_usuario(id))),
                ]
            ))

        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("E-mail")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=linhas,
        )

        view = ft.View(
            "/gerencial/usuarios",
            [
                self.criar_appbar("Gerenciamento de Usuários"),
                ft.Container(
                    content=tabela,
                    padding=20,
                    expand=True
                )
            ]
        )
        self.page.views.append(view)

    def editar_usuario(self, usuario_id):
        # Implementar lógica para editar usuário
        pass

    # Métodos de Ação
    def fazer_login(self, e):
        usuario = self.bd.buscar_usuario_por_email(self.tf_email.value or "")
        if usuario and utilidades.verificar_hash_bcrypt(self.tf_senha.value or "", usuario["Senha"]):
            if usuario["Tipo"] in ["Administrador", "Diretor"]:
                self.usuario_logado = usuario
                self.page.go("/gerencial/dashboard")
                return
        self.lb_erro.value = "Credenciais inválidas ou sem permissão"
        self.page.update()

    def obter_cor_status(self, status):
        cores = {
            "Aberta": ft.colors.RED,
            "Em Atendimento": ft.colors.ORANGE,
            "Encerrada": ft.colors.GREEN
        }
        return cores.get(status, ft.colors.BLACK)

    def mostrar_dialogo_status(self, e):
        # Implementar diálogo para alterar status
        pass

    def mostrar_dialogo_comentario(self, e):
        # Implementar diálogo para adicionar comentário
        pass

# Inicialização do Módulo
def main(page: ft.Page):
    Gerencial(page)

if __name__ == "__main__":
    ft.app(target=main)
import dados
import utilidades
import flet as ft
import re
import webbrowser
from pathlib import Path
from datetime import datetime
import asyncio

# Constantes
BANCO_DADOS = "bullying.db"
CAMINHO_BANCO_DADOS = Path(BANCO_DADOS)
FORMATO_DATA = "%d/%m/%Y"

# Variáveis Globais
denuncia_id = 0
denuncia_id_gerado = 0
data_reuniao = datetime.now().date()
flag_thread = False
flag_atualiza = False
reniao_id = 0

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
        page.title = "Denúncia de Bullying Anônima - Módulo Gerencial  [V.1.0]"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20

        # Evento de mudança de 
        def route_change(e):
            global denuncia_id
            global denuncia
            global denuncia_id_gerado
            global data_reuniao
            global flag_thread
            global flag_atualiza
            global reuniao_id
            global lv_reuniao

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

            # Validar Senha Nova
            def validar_senha_nova(e):
                nonlocal senha_nova_valida
                senha_nova_valida = False
                senha_nova = tf_senha_nova.value
                erros = []
                # Verifica cada requisito individualmente
                if len(senha_nova) < 8: # type: ignore 
                    erros.append("Mínimo 8 caracteres")
                if not re.search(r'[A-Z]', senha_nova): # type: ignore
                    erros.append("Pelo menos 1 letra maiúscula")
                if not re.search(r'[a-z]', senha_nova): # type: ignore
                    erros.append("Pelo menos 1 letra minúscula")
                if not re.search(r'[0-9]', senha_nova): # type: ignore
                    erros.append("Pelo menos 1 número")
                if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova): # type: ignore
                    erros.append("Pelo menos 1 símbolo especial")

                if erros:
                    tf_senha_nova.error_text = "\n".join(erros)
                    # Exibe quais requisitos foram atendidos
                    cl_validacao_indicadores.controls = [
                        ft.Row([
                            ft.Text("A senha deve conter", color="grey")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if len(senha_nova) >= 8 else ft.Icons.CLOSE, # type: ignore
                            color="green" if len(senha_nova) >= 8 else "red"), # type: ignore
                            ft.Text("8+ caracteres")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[A-Z]', senha_nova) else ft.Icons.CLOSE, # type: ignore
                            color="green" if re.search(r'[A-Z]', senha_nova) else "red"), # type: ignore
                            ft.Text("Letra maiúscula")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[a-z]', senha_nova) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[a-z]', senha_nova) else "red"), # type: ignore
                            ft.Text("Letra minúscula")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[0-9]', senha_nova) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[0-9]', senha_nova) else "red"), # type: ignore
                            ft.Text("Número")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova) else "red"), # type: ignore
                            ft.Text("Símbolo especial")
                        ])
                    ]
                else:
                    tf_senha_nova.error_text = None
                    senha_nova_valida = True
                    cl_validacao_indicadores.controls = [
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color="green"),
                            ft.Text("Senha forte!", weight=ft.FontWeight.BOLD)
                        ]),
                    ]
        
                cl_validacao_indicadores.update()
                validar_fazer_denuncia()
                page.update()
                validar_senha_nova_confirmar(e)

            # Validar Senha Nova Confirmar
            def validar_senha_nova_confirmar(e):
                nonlocal senha_nova_confirmar_valida
                senha_nova_confirmar_valida = False
                senha_nova = tf_senha_nova.value
                senha_nova_confirmar = tf_senha_nova_confirmar.value
                errosc = []
                # Verifica cada requisito individualmente
                if len(senha_nova_confirmar) < 8: # type: ignore 
                    errosc.append("Mínimo 8 caracteres")
                if not re.search(r'[A-Z]', senha_nova_confirmar): # type: ignore
                    errosc.append("Pelo menos 1 letra maiúscula")
                if not re.search(r'[a-z]', senha_nova_confirmar): # type: ignore
                    errosc.append("Pelo menos 1 letra minúscula")
                if not re.search(r'[0-9]', senha_nova_confirmar): # type: ignore
                    errosc.append("Pelo menos 1 número")
                if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova_confirmar): # type: ignore
                    errosc.append("Pelo menos 1 símbolo especial")
                if not senha_nova == senha_nova_confirmar:
                    errosc.append("Confirma Senha")

                if errosc:
                    tf_senha_nova_confirmar.error_text = "\n".join(errosc)
                    # Exibe quais requisitos foram atendidos
                    cl_validacao_indicadores_confirmar.controls = [
                        ft.Row([
                            ft.Text("A senha deve conter", color="grey")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if len(senha_nova_confirmar) >= 8 else ft.Icons.CLOSE, # type: ignore
                            color="green" if len(senha_nova_confirmar) >= 8 else "red"), # type: ignore
                            ft.Text("8+ caracteres")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[A-Z]', senha_nova_confirmar) else ft.Icons.CLOSE, # type: ignore
                            color="green" if re.search(r'[A-Z]', senha_nova_confirmar) else "red"), # type: ignore
                            ft.Text("Letra maiúscula")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[a-z]', senha_nova_confirmar) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[a-z]', senha_nova_confirmar) else "red"), # type: ignore
                            ft.Text("Letra minúscula")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[0-9]', senha_nova_confirmar) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[0-9]', senha_nova_confirmar) else "red"), # type: ignore
                            ft.Text("Número")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova_confirmar) else ft.Icons.CLOSE, # type: ignore
                                color="green" if re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_nova_confirmar) else "red"), # type: ignore
                            ft.Text("Símbolo especial")
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK if senha_nova_confirmar == senha_nova else ft.Icons.CLOSE,
                                color="green" if senha_nova_confirmar == senha_nova else "red"),
                            ft.Text("Confirma Senha")
                        ])
                    ]
                else:
                    tf_senha_nova_confirmar.error_text = None
                    senha_nova_confirmar_valida = True
                    cl_validacao_indicadores_confirmar.controls = [
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color="green"),
                            ft.Text("Senha Confirmada!", weight=ft.FontWeight.BOLD)
                        ]),
                    ]
        
                cl_validacao_indicadores_confirmar.update()
                validar_fazer_denuncia()
                page.update()

            # Validar Descrição O que
            def validar_descricao_o_que(e):
                nonlocal descricao_o_que_valida
                descricao_o_que_valida = False
                if not tf_descricao_o_que.value.strip():  # type: ignore
                    tf_descricao_o_que.error_text = "Requer preenchimento"
                else:
                    tf_descricao_o_que.error_text = None
                    descricao_o_que_valida = True

                validar_fazer_denuncia()   
                page.update()

            # Validar Descrição Como se sente
            def validar_descricao_como_se_sente(e):
                nonlocal descricao_como_se_sente_valida
                descricao_como_se_sente_valida = False
                if not tf_descricao_como_se_sente.value.strip():  # type: ignore
                    tf_descricao_como_se_sente.error_text = "Requer preenchimento"
                else:
                    tf_descricao_como_se_sente.error_text = None
                    descricao_como_se_sente_valida = True

                validar_fazer_denuncia()   
                page.update()

            # Validar Local
            def validar_local(e):
                nonlocal local_valida
                local_valida = False
                if not dd_local.value.strip():  # type: ignore
                    dd_local.error_text = "Requer preenchimento"
                else:
                    dd_local.error_text = None
                    local_valida = True

                validar_fazer_denuncia()   
                page.update()

            # Validar Frequência
            def validar_frequencia(e):
                nonlocal frequencia_valida
                frequencia_valida = False
                if not dd_frequencia.value.strip():  # type: ignore
                    dd_frequencia.error_text = "Requer preenchimento"
                else:
                    dd_frequencia.error_text = None
                    frequencia_valida = True

                validar_fazer_denuncia()   
                page.update()

            # Validar Tipo de Bullying
            def validar_tipo_bullying(e):
                nonlocal tipo_bullying_valida
                tipo_bullying_valida = False
                if not dd_tipo_bullying.value.strip():  # type: ignore
                    dd_tipo_bullying.error_text = "Requer preenchimento"
                else:
                    dd_tipo_bullying.error_text = None
                    tipo_bullying_valida = True

                validar_fazer_denuncia()   
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

            # Validar fazer Denúncia
            def validar_fazer_denuncia():
                nonlocal descricao_o_que_valida
                nonlocal descricao_como_se_sente_valida
                nonlocal local_valida
                nonlocal frequencia_valida
                nonlocal tipo_bullying_valida
                nonlocal senha_nova_valida
                nonlocal senha_nova_confirmar_valida
                fazer_denuncia_validado = all([
                    descricao_o_que_valida,
                    descricao_como_se_sente_valida,
                    local_valida,
                    frequencia_valida,
                    tipo_bullying_valida,
                    senha_nova_valida,
                    senha_nova_confirmar_valida
                ])
                bt_fazer_decuncia.disabled = not fazer_denuncia_validado

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

            # Fazer Denúncia de Bullying
            def fazer_denuncia(e):
                global denuncia_id_gerado
                denuncia_id_gerado = bd.criar_denuncia(utilidades.gerar_hash_bcrypt(tf_senha_nova.value), tf_descricao_o_que.value, tf_descricao_como_se_sente.value, dd_local.value, dd_frequencia.value, dd_tipo_bullying.value) # type: ignore
                # print(denuncia_id_gerado)
                return page.go("/denunciaaviso")

            # Validar Mensagem
            def validar_mensagem(e):
                nonlocal mensagem_valida
                mensagem_valida = False
                mensagem = tf_mensagem.value
                erros = []
                # Verifica cada requisito individualmente
                if mensagem:
                    if len(mensagem) < 1:
                        erros.append("Mínimo 1 caractere")
                else:
                    erros.append("Mensagem requerida")
                if erros:
                   mensagem_valida = False
                   tf_mensagem.error_text = "Mensagem inválida"
                else:
                   mensagem_valida = True
                   tf_mensagem.error_text = None
                bt_enviar_reuniao.disabled = not mensagem_valida
                page.update()

            # Enivar mensagem Reunião
            def envia_reuniao(e):
                global denuncia_id
                global data_reuniao
                global flag_thread
                bd.criar_denuncia_reuniao(denuncia_id, tf_mensagem.value, 0) # type: ignore
                tf_mensagem.value = ""
                bt_enviar_reuniao.disabled = True
                page.update()

            # Autorefresh Reunião
            async def auto_reuniao(ct_reuniao, page):
                global lv_reuniao
                global flag_atualiza
                while flag_thread:
                    # print(f"Auto {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} {flag_atualiza}")
                    atualizar_reuniao(True)
                    if flag_atualiza:
                        flag_atualiza = False
                        ct_reuniao.content.controls = [lv_reuniao]
                        page.update()
                    await asyncio.sleep(1)  # Espera 2 segundos antes de atualizar novamente

            # Sair Reunião
            def sair_reuniao(e):
                global flag_thread
                flag_thread = False
                return page.go("/acompanhar")

            # Atualizar Reunião
            def atualizar_reuniao(fazer):
                global denuncia_id
                global reuniao_id
                global data_reuniao
                global lv_reuniao
                global flag_atualiza
                
                aux_reuniao_id = 0
                
                reuniao = bd.listar_denuncias_reuniao_usuario(denuncia_id=denuncia_id, denuncia_reuniao_id=reuniao_id, data=data_reuniao)

                for msg in reuniao:
                    # Container para cada mensagem
                    ct_reuniao = ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(msg["UsuarioTipo"], weight=ft.FontWeight.BOLD),
                                ft.Text(msg["Mensagem"], size=14),
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
                    itens_reuniao.append(ct_reuniao)
                    aux_reuniao_id = msg["DenunciaReuniaoId"]
                # Criar ListView com expansão
                lv_reuniao = ft.ListView(
                    controls=itens_reuniao,
                    spacing=10,
                    expand=True,  # Isso faz o ListView ocupar todo o espaço disponível
                    auto_scroll=True,
                )
                # print(reuniao_id, aux_reuniao_id)    
                if fazer:
                    if aux_reuniao_id > reuniao_id:
                       reuniao_id = aux_reuniao_id
                       flag_atualiza = True

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
                descricao_o_que_valida = False
                descricao_como_se_sente_valida = False
                local_valida = False
                frequencia_valida = False
                tipo_bullying_valida = False
                senha_nova_valida = False
                senha_nova_confirmar_valida = False
                tf_descricao_o_que = ft.TextField(label="Descrição - O que?", multiline=True, width=610, on_change=validar_descricao_o_que) # type: ignore
                tf_descricao_como_se_sente = ft.TextField(label="Descrição - Como se sente?", multiline=True, width=610, on_change=validar_descricao_como_se_sente) # type: ignore
                dd_local = ft.Dropdown(label="Local", 
                                            options=[
                                                ft.dropdown.Option("Escola"),
                                                ft.dropdown.Option("Internet"),
                                                ft.dropdown.Option("Trabalho"),
                                                ft.dropdown.Option("Outro"),
                                                ], on_change=validar_local)
                dd_frequencia = ft.Dropdown(label="Frequência", 
                                                options=[
                                                    ft.dropdown.Option("Única vez"),
                                                    ft.dropdown.Option("Algumas vezes"),
                                                    ft.dropdown.Option("Frequentemente"),
                                            ], on_change=validar_frequencia)
                dd_tipo_bullying = ft.Dropdown(label="Tipo Bullying",
                                                options=[
                                                    ft.dropdown.Option("Físico"),
                                                    ft.dropdown.Option("Verbal"),
                                                    ft.dropdown.Option("Psicológico"),
                                                    ft.dropdown.Option("Ciberbullying"),
                                                    ft.dropdown.Option("Outro"),
                                            ], on_change=validar_tipo_bullying)
                tf_senha_nova = ft.TextField(label="Nova Senha", password=True, can_reveal_password=True, on_change=validar_senha_nova)
                
                cl_validacao_indicadores = ft.Column(spacing=5)

                tf_senha_nova_confirmar = ft.TextField(label="Confirmar a Senha", password=True, can_reveal_password=True, on_change=validar_senha_nova_confirmar)

                cl_validacao_indicadores_confirmar = ft.Column(spacing=5)

                bt_fazer_decuncia = ft.ElevatedButton("Fazer Denúncia", on_click=fazer_denuncia, disabled=True, icon=ft.Icons.ANNOUNCEMENT)

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
                            ft.Container(content=ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, controls=[
                                ft.Row(
                                    controls=[tf_descricao_o_que],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_descricao_como_se_sente],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[dd_local, dd_frequencia, dd_tipo_bullying],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[ft.Text("Criar a Senha forte para ter acesso ao acompanhamento da denúncia.", weight=ft.FontWeight.BOLD)],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_senha_nova, cl_validacao_indicadores],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[tf_senha_nova_confirmar, cl_validacao_indicadores_confirmar],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                                ft.Row(
                                    controls=[bt_fazer_decuncia],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                                ),
                            ]), expand=True, padding=10),
                        ],
                    )
                )
            
            # Página Fazer Denúncia de Bullying Anônima (Aviso)
            if page.route == "/denunciaaviso":
                tf_v_aviso = ft.TextField(label="N° Denúncia", value=str(denuncia_id_gerado), read_only=True,  text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.BLUE))

                page.views.append(
                   ft.View(
                        "/denunciaaviso",
                        [
                            ft.AppBar(
                                title=ft.Text("Fazer Denúncia de Bullying Anônima (Aviso)"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    on_click=lambda _: page.go("/"),  # Comportamento de voltar padrão
                                ),
                                bgcolor=ft.Colors.RED_300,
                            ),
                            ft.Row(
                                controls=[ft.Text("Atenção utilizar esse N° de Denúncia para Acompanhar a Denúncia, junto com a senha que você cadastrou.", color=ft.Colors.RED, weight=ft.FontWeight.BOLD)],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ft.Row(
                                controls=[tf_v_aviso],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
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
                tf_v_descricao_o_que = ft.TextField(label="Descrição - O que?", value=denuncia["DescricaoOque"], read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
                tf_v_descricao_como_se_sente = ft.TextField(label="Descrição - Como se sente?", value=denuncia["DescricaoComoSeSente"], read_only=True, multiline=True, width=610, max_lines=3) # type: ignore
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
                reuniao_id = 0
                itens_reuniao = []
                data_reuniao = datetime.now().date()
                mensagem_valida = False
                tf_mensagem = ft.TextField(label="Mensagem", multiline=True, expand=True, on_change=validar_mensagem, max_lines=1)
                bt_enviar_reuniao = ft.ElevatedButton("Enviar mensagem", disabled=True, on_click=envia_reuniao, icon=ft.Icons.SEND)
                
                atualizar_reuniao(False)

                ct_reuniao = ft.Container(
                    content=lv_reuniao,
                    expand=True,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=10,
                    padding=10,
                )
                
                page.views.append(
                   ft.View(
                        "/reuniao",
                        [
                            ft.AppBar(
                                title=ft.Text(f"Reunião [{data_reuniao.strftime('%d/%m/%Y')}] [Denúncia N° {denuncia_id}]"),
                                leading=ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    tooltip="Voltar",  # Tooltip modificado
                                    # on_click=lambda _: page.go("/acompanhar"),  # Comportamento de voltar padrão
                                    on_click=sair_reuniao,  # Comportamento de voltar padrão
                                ),
                                bgcolor=ft.Colors.RED_300,
                            ),

                            ft.Row(
                                controls=[tf_mensagem, bt_enviar_reuniao],
                                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza horizontalmente
                            ),
                            ct_reuniao
                        ],
                    )
                )
                # Iniciar atualização automática
                flag_thread = True
                asyncio.run(auto_reuniao(ct_reuniao, page))

            # Página Materiais Educativos
            if page.route == "/materiaiseducativos":
                # link_url1 ="https://drive.google.com/file/d/12zx4dH49ydysy4i5-DeaZjdZUQefIrXH/view?usp=sharing"
                # link_url2 ="https://drive.google.com/file/d/1wB3Hcfw4FFT_wPOPd3ZK1kR6EDJVtrJS/view?usp=sharing"
                # link_url3 ="https://www.youtube.com/watch?v=mWQoikd72A4"

                rows = []

                header = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Descrição do Material Educativo", weight=ft.FontWeight.BOLD, expand=True),
                            ft.Text("Link", weight=ft.FontWeight.BOLD),
                        ],
                        spacing=20
                    ),
                    padding=10,
                    bgcolor=ft.Colors.GREY_200,
                )
                rows.append(header)

                materiais = bd.listar_materiais_educativos(status="Ativo")

                for item in materiais:
                    descricao = ft.Text(
                        item["Descricao"],
                        size=14,
                        color=ft.Colors.BLACK87,
                        selectable=True,
                    )

                    link_btn = ft.ElevatedButton(
                        text="Link",
                        icon=ft.Icons.LINK,
                        on_click=lambda e, url=item["Link"]: webbrowser.open(url),
                        style=ft.ButtonStyle(
                            padding=10,
                            bgcolor=ft.Colors.BLUE_50,
                            color=ft.Colors.BLUE_700
                        )
                    )

                    row = ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(descricao, expand=True, padding=10),
                                ft.Container(link_btn, padding=10),
                            ],
                            spacing=20,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                        border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_300)),
                        padding=ft.padding.symmetric(vertical=5),
                    )
        
                    rows.append(row)




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
                            ft.Container(
                                content=ft.Column(
                                    controls=rows,
                                    spacing=0,
                                    expand=True,
                                    scroll=ft.ScrollMode.AUTO,
                                ),
                                border=ft.border.all(1, ft.Colors.GREY_400),
                                border_radius=5,
                                expand=True,
                            ),
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