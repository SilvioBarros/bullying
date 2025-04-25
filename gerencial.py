######################################################## 
# Faculdade: Cesar School                              #
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
# Data: 22/04/2025                                     #
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