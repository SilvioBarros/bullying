######################################################## 
# Projeto: App Denúncia de Bullying Anônima            #
# Descrição: Classe Banco de Dados                     #
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

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict

class BancoDados:
    # Construtor
    def __init__(self, db_name: str = 'dbsqlite3.db'):
        self.db_name = db_name
    
    # Conexão 
    def _conectar(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name, timeout=10, isolation_level=None)

    # Cria Tabelas
    def criar_tabelas(self):
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()

            # Tabela de Denúncia
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Denuncias (
                    Denunciaid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Senha TEXT NOT NULL,
                    DataHora DATETIME NOT NULL,
                    DescricaoOque TEXT NOT NULL,
                    DescricaoComoSeSente TEXT NOT NULL,
                    Local TEXT NOT NULL,
                    Frequencia TEXT NOT NULL,
                    TipoBullying TEXT NOT NULL,
                    Status TEXT NOT NULL
                )
            ''')
            conn.commit()

            # Tabela de Denúncia Comentários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Denuncias_Comentarios (
                    DenunciaComentarioid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Denunciaid INTEGER NOT NULL,
                    DataHora DATETIME NOT NULL,
                    Comentario TEXT NOT NULL,
                    Usuarioid INTEGER NOT NULL,
                    Status TEXT NOT NULL
                )
            ''')
            conn.commit()

            # Tabela de Denúncia Reunião
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Denuncias_Reuniao (
                    DenunciaReuniaoid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Denunciaid INTEGER NOT NULL,
                    DataHora DATETIME NOT NULL,
                    Comentario TEXT NOT NULL,
                    Mensagem TEXT NOT NULL,
                    Usuarioid INTEGER NOT NULL
                )
            ''')
            conn.commit()

            # Tabela de Cadastro de Usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Usuario (
                    Usuarioid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Email TEXT UNIQUE NOT NULL,
                    Senha TEXT NOT NULL,
                    Nome TEXT NOT NULL,
                    Tipo TEXT NOT NULL,
                    Status TEXT NOT NULL
                )
            ''')
            conn.commit()

            # Tabela de Cadastro de Materiais Educativos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Materiais_Educativos (
                    Materialid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Descricao TEXT NOT NULL,
                    Link TEXT NOT NULL,
                    UsuarioidCriou INTEGER NOT NULL,
                    UsuarioidAlterou INTEGER NOT NULL,
                    DataHoraUltAlt DATETIME NOT NULL,
                    Status TEXT NOT NULL
                )
            ''')
            conn.commit()

            # Tabela de Log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Log (
                    Loglid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Descricao TEXT NOT NULL,
                    Usuarioid INTEGER NOT NULL,
                    DataHora DATETIME NOT NULL
                )
            ''')
            conn.commit()

            print("Criou Tabelas")

    # Criar Denúncia
    def criar_denuncia(self, senha: str, descricao_o_que: str, descricao_como_se_sente: str, local: str, frequencia: str, tipo_bullying: str) -> int | None:
        data_hora = datetime.now()
        status = "Aberta"
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO TB_Denuncias (Senha, DataHora, DescricaoOque, DescricaoComoSeSente, Local, Frequencia, TipoBullying, Status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (senha, data_hora, descricao_o_que, descricao_como_se_sente, local, frequencia, tipo_bullying, status))
            conn.commit()
            return cursor.lastrowid

    # Buscar Denúncia por Id
    def buscar_denuncia_por_id(self, denuncia_id: int) -> Optional[Dict]:
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM TB_Denuncias WHERE DenunciaId = ?', (denuncia_id,))
            denuncia = cursor.fetchone()
            return dict(denuncia) if denuncia else None

    # Listar Denúncias
    def listar_denuncias(self, **kwargs) -> List[Dict]:
        campos_permitidos = {'data_inicio', 'data_fim', 'status'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}

        query = 'SELECT * FROM TB_Denuncias'

        if campos:
            flg = True
            for campo, valor in campos.items():
                if campo == 'data_inicio':
                   filtro = f'(DataHora>=\'{valor}\')'
                elif campo == 'data_fim':
                   filtro = f'(DataHora<=\'{valor}\')'
                elif campo == 'status':
                   filtro = f'(status in {valor})'
                if flg:
                   query += ' WHERE ' + filtro
                   flg = False
                else:   
                   query += ' AND ' + filtro
        print(query)
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    # def criar_usuario(self, email: str, senha: str, nome: str, status: str, permissao: str) -> int:
    #     senha_md5 = self._gerar_md5(senha)
    #     with self._conectar() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute('''
    #             INSERT INTO usuarios (email, senha_md5, nome, status, permissao)
    #             VALUES (?, ?, ?, ?, ?)
    #         ''', (email, senha_md5, nome, status, permissao))
    #         conn.commit()
    #         return cursor.lastrowid

    # def buscar_usuario_por_id(self, usuario_id: int) -> Optional[Dict]:
    #     with self._conectar() as conn:
    #         conn.row_factory = sqlite3.Row
    #         cursor = conn.cursor()
    #         cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
    #         usuario = cursor.fetchone()
    #         return dict(usuario) if usuario else None

    # def buscar_usuario_por_email(self, email: str) -> Optional[Dict]:
    #     with self._conectar() as conn:
    #         conn.row_factory = sqlite3.Row
    #         cursor = conn.cursor()
    #         cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    #         usuario = cursor.fetchone()
    #         return dict(usuario) if usuario else None

    # def listar_usuarios(self) -> List[Dict]:
    #     with self._conectar() as conn:
    #         conn.row_factory = sqlite3.Row
    #         cursor = conn.cursor()
    #         cursor.execute('SELECT * FROM usuarios')
    #         return [dict(row) for row in cursor.fetchall()]

    # def atualizar_usuario(self, usuario_id: int, **kwargs):
    #     campos_permitidos = {'email', 'senha', 'nome', 'status', 'permissao'}
    #     campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}
        
    #     if not campos:
    #         raise ValueError("Nenhum campo válido para atualização")

    #     query = []
    #     params = []
        
    #     for campo, valor in campos.items():
    #         if campo == 'senha':
    #             valor = self._gerar_md5(valor)
    #             query.append(f"senha_md5 = ?")
    #         else:
    #             query.append(f"{campo} = ?")
    #         params.append(valor)
        
    #     params.append(usuario_id)
        
    #     with self._conectar() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(f'''
    #             UPDATE usuarios
    #             SET {', '.join(query)}
    #             WHERE id = ?
    #         ''', params)
    #         conn.commit()
    #         return cursor.rowcount

    # def deletar_usuario(self, usuario_id: int) -> bool:
    #     with self._conectar() as conn:
    #         cursor = conn.cursor()
    #         cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
    #         conn.commit()
    #         return cursor.rowcount > 0

    # def verificar_login(self, email: str, senha: str) -> Optional[Dict]:
    #     senha_md5 = self._gerar_md5(senha)
    #     with self._conectar() as conn:
    #         conn.row_factory = sqlite3.Row
    #         cursor = conn.cursor()
    #         cursor.execute('''
    #             SELECT * FROM usuarios 
    #             WHERE email = ? AND senha_md5 = ? AND status = 'ativo'
    #         ''', (email, senha_md5))
    #         usuario = cursor.fetchone()
    #         return dict(usuario) if usuario else None