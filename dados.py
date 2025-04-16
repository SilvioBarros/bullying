######################################################## 
# App Denúncia de Bullying Anônima
# Classe Banco de Dados
# Equipe:
#           Artur Cavalcanti
#           Eduardo Henrique Ferreira Fonseca Barbosa
#           Evandro José Rodrigues Torres Zacarias
#           Gabriel de Medeiros Almeida 
#           Maria Clara Miranda
#           Mauro Sérgio Rezende da Silva
#           Silvio Barros Tenório
# Versão: 1.0
######################################################## 

import sqlite3
# import hashlib
# from typing import Optional, List, Dict

class BancoDados:
    # Construtor
    def __init__(self, db_name: str = 'bullying.db'):
        self.db_name = db_name
        self._criar_tabelas()
    
    # Conexão 
    def _conectar(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name, timeout=10, isolation_level=None)

    # Cria Tabelas
    def _criar_tabelas(self):
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()

            # Tabela de Denúncia
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Denuncias (
                    Denunciaid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Senha TEXT NOT NULL,
                    DataHora DATETIME NOT NULL,
                    DescricaoOque TEXT UNIQUE NOT NULL,
                    DescricaoComoSeSente TEXT UNIQUE NOT NULL,
                    Local TEXT UNIQUE NOT NULL,
                    Frequencia TEXT UNIQUE NOT NULL,
                    TipoBullying TEXT UNIQUE NOT NULL,
                    Status TEXT UNIQUE NOT NULL
                )
            ''')
            conn.commit()

            # Tabela de Denúncia Comentários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Denuncias_Comentarios (
                    DenunciaComentarioid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Denunciaid INTEGER NOT NULL,
                    DataHora DATETIME NOT NULL,
                    Comentario TEXT UNIQUE NOT NULL,
                    Usuarioid INTEGER NOT NULL,
                    Status TEXT UNIQUE NOT NULL
                )
            ''')
            conn.commit()

            # Tabela de Denúncia Reunião
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Denuncias_Reuniao (
                    DenunciaReuniaoid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Denunciaid INTEGER NOT NULL,
                    DataHora DATETIME NOT NULL,
                    Comentario TEXT UNIQUE NOT NULL,
                    Mensagem TEXT UNIQUE NOT NULL,
                    Usuarioid INTEGER NOT NULL
                )
            ''')
            conn.commit()

            # Tabela de Cadastro de Usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Usuario (
                    Usuarioid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Email TEXT UNIQUE NOT NULL,
                    Senha TEXT UNIQUE NOT NULL,
                    Nome TEXT UNIQUE NOT NULL,
                    Tipo TEXT UNIQUE NOT NULL,
                    Status TEXT UNIQUE NOT NULL
                )
            ''')
            conn.commit()

            # Tabela de Cadastro de Materiais Educativos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Materiais_Educativos (
                    Materialid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Descricao TEXT UNIQUE NOT NULL,
                    Link TEXT UNIQUE NOT NULL,
                    UsuarioidCriou INTEGER NOT NULL,
                    UsuarioidAlterou INTEGER NOT NULL,
                    DataHoraUltAlt DATETIME NOT NULL,
                    Status TEXT UNIQUE NOT NULL
                )
            ''')
            conn.commit()

            # Tabela de Log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Log (
                    Loglid INTEGER PRIMARY KEY AUTOINCREMENT,
                    Descricao TEXT UNIQUE NOT NULL,
                    Usuarioid INTEGER NOT NULL,
                    DataHora DATETIME NOT NULL
                )
            ''')
            conn.commit()

            print("Criou Tabelas")


    # def _gerar_md5(self, senha: str) -> str:
    #     return hashlib.md5(senha.encode('utf-8')).hexdigest()

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