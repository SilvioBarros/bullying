######################################################## 
# Faculdade: Cesar School                              #
# Curso: Segurança da Informação                       #
# Período: 2025.1                                      #
# Disciplina: Projeto 1                                #
# Professor: Humberto Caetano                          #
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
# Data: 05/05/2025                                     #
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
                    DenunciaId INTEGER PRIMARY KEY AUTOINCREMENT,
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

            # Tabela de Denúncia Comentários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Denuncias_Comentarios (
                    DenunciaComentarioId INTEGER PRIMARY KEY AUTOINCREMENT,
                    DenunciaId INTEGER NOT NULL,
                    DataHora DATETIME NOT NULL,
                    Comentario TEXT NOT NULL,
                    UsuarioId INTEGER NOT NULL,
                    Status TEXT NOT NULL,
                    FOREIGN KEY (DenunciaId) REFERENCES TB_Denuncias(DenunciaId)
                )
            ''')

            # Tabela de Denúncia Reunião
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Denuncias_Reuniao (
                    DenunciaReuniaoId INTEGER PRIMARY KEY AUTOINCREMENT,
                    DenunciaId INTEGER NOT NULL,
                    DataHora DATETIME NOT NULL,
                    Mensagem TEXT NOT NULL,
                    UsuarioId INTEGER NOT NULL,
                    FOREIGN KEY (DenunciaId) REFERENCES TB_Denuncias(DenunciaId)
                )
            ''')

            # Tabela de Cadastro de Usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Usuarios (
                    UsuarioId INTEGER PRIMARY KEY AUTOINCREMENT,
                    Email TEXT UNIQUE NOT NULL,
                    Senha TEXT NOT NULL,
                    Nome TEXT NOT NULL,
                    Tipo TEXT NOT NULL,
                    Status TEXT NOT NULL
                )
            ''')

            # Tabela de Cadastro de Materiais Educativos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Materiais_Educativos (
                    MaterialId INTEGER PRIMARY KEY AUTOINCREMENT,
                    Descricao TEXT NOT NULL,
                    Link TEXT NOT NULL,
                    UsuarioIdCriou INTEGER NOT NULL,
                    UsuarioIdAlterou INTEGER NOT NULL,
                    DataHoraUltAlt DATETIME NOT NULL,
                    Status TEXT NOT NULL
                )
            ''')

            # Tabela de Log
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TB_Log (
                    LoglId INTEGER PRIMARY KEY AUTOINCREMENT,
                    Descricao TEXT NOT NULL,
                    Usuarioid INTEGER NOT NULL,
                    DataHora DATETIME NOT NULL
                )
            ''')
            conn.commit()

            # print("Criou as Tabelas")

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

    # Verificar Login Denúncia
    def verificar_login_denuncia(self, denuncia_id: int) -> Optional[Dict]:
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM TB_Denuncias 
                WHERE DenunciaID = ?
            ''', (denuncia_id,))
            denuncia = cursor.fetchone()
            return dict(denuncia) if denuncia else None
        
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
                   filtro = f'(date(DataHora)>=date(\'{valor}\'))'
                elif campo == 'data_fim':
                   filtro = f'(date(DataHora)<=date(\'{valor}\'))'
                elif campo == 'status':
                   filtro = f'(status in {valor})'
                if flg:
                   query += ' WHERE ' + filtro
                   flg = False
                else:   
                   query += ' AND ' + filtro
        # print(query)
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    # Atualizar Denúncia
    def atualizar_denuncia(self, denuncia_id: int, **kwargs):
        campos_permitidos = {'status'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}
        
        if not campos:
            raise ValueError("Nenhum campo válido para atualização")

        query = []
        params = []
        
        for campo, valor in campos.items():
            if campo == 'status':
                query.append(f"Status = ?")
            params.append(valor)
        
        params.append(denuncia_id)

        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE TB_Denuncias
                SET {', '.join(query)}
                WHERE DenunciaId = ?
            ''', params)
            conn.commit()

    # Criar Denúncia Comentário
    def criar_denuncia_comentario(self, denuncia_id: int, comentario: str, usuario_id: int, status: str) -> int | None:
        data_hora = datetime.now()
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO TB_Denuncias_Comentarios (DenunciaId, DataHora, Comentario, UsuarioId, Status)
                VALUES (?, ?, ?, ?, ?)
            ''', (denuncia_id, data_hora, comentario, usuario_id, status))
            conn.commit()
            return cursor.lastrowid

    # Listar Denúncias Comentários
    def listar_denuncias_comentarios(self, **kwargs) -> List[Dict]:
        campos_permitidos = {'denuncia_id', 'denuncia_comentario_id'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}

        query = 'SELECT * FROM TB_Denuncias_Comentarios'

        if campos:
            flg = True
            for campo, valor in campos.items():
                if campo == 'denuncia_id':
                   filtro = f'(DenunciaId={valor})'
                elif campo == 'denuncia_comentario_id':
                   filtro = f'(DenunciaComentarioId>{valor})'
                if flg:
                   query += ' WHERE ' + filtro
                   flg = False
                else:   
                   query += ' AND ' + filtro
        # print(query)
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    # Listar Denúncias Comentários Usuário
    def listar_denuncias_comentarios_usuario(self, **kwargs) -> List[Dict]:
        campos_permitidos = {'denuncia_id', 'denuncia_comentario_id'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}

        query = '''SELECT
                   A.DenunciaComentarioId,
                   A.DenunciaId,
                   A.DataHora,
                   A.Comentario,
                   A.UsuarioId,
                   A.Status,
                   IFNULL(B.Nome, 'Denunciante') AS UsuarioNome,
                   IFNULL(B.Tipo, 'Denunciante') AS UsuarioTipo
                   FROM TB_Denuncias_Comentarios A
                   LEFT JOIN TB_Usuarios B ON B.UsuarioId = A.UsuarioId'''
        if campos:
            flg = True
            for campo, valor in campos.items():
                if campo == 'denuncia_id':
                   filtro = f'(DenunciaId={valor})'
                elif campo == 'denuncia_comentario_id':
                   filtro = f'(DenunciaComentarioId>{valor})'
                if flg:
                   query += ' WHERE ' + filtro
                   flg = False
                else:   
                   query += ' AND ' + filtro
        # print(query)
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    # Criar Denúncia Reunião
    def criar_denuncia_reuniao(self, denuncia_id: int, mensagem: str, usuario_id: int) -> int | None:
        data_hora = datetime.now()
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO TB_Denuncias_Reuniao (DenunciaId, DataHora, Mensagem, UsuarioId)
                VALUES (?, ?, ?, ?)
            ''', (denuncia_id, data_hora, mensagem, usuario_id))
            conn.commit()
            return cursor.lastrowid

    # Listar Denúncias Reunião
    def listar_denuncias_reuniao(self, **kwargs) -> List[Dict]:
        campos_permitidos = {'denuncia_id', 'denuncia_reuniao_id', 'data'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}

        query = 'SELECT * FROM TB_Denuncias_Reuniao'

        if campos:
            flg = True
            for campo, valor in campos.items():
                if campo == 'denuncia_id':
                   filtro = f'(DenunciaId={valor})'
                elif campo == 'denuncia_reuniao_id':
                   filtro = f'(DenunciaReuniaoId>{valor})'
                elif campo == 'data':
                   filtro = f'(date(DataHora)=date(\'{valor}\'))'
                if flg:
                   query += ' WHERE ' + filtro
                   flg = False
                else:   
                   query += ' AND ' + filtro
        # print(query)
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    # Listar Denúncias Reunião Usuário
    def listar_denuncias_reuniao_usuario(self, **kwargs) -> List[Dict]:
        campos_permitidos = {'denuncia_id', 'denuncia_reuniao_id', 'data'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}

        query = '''SELECT
                   A.DenunciaReuniaoId,
                   A.DenunciaId,
                   A.DataHora,
                   A.Mensagem,
                   A.UsuarioId,
                   IFNULL(B.Nome, 'Denunciante') AS UsuarioNome,
                   IFNULL(B.Tipo, 'Denunciante') AS UsuarioTipo
                   FROM TB_Denuncias_Reuniao A
                   LEFT JOIN TB_Usuarios B ON B.UsuarioId = A.UsuarioId'''

        if campos:
            flg = True
            for campo, valor in campos.items():
                if campo == 'denuncia_id':
                   filtro = f'(DenunciaId={valor})'
                elif campo == 'denuncia_reuniao_id':
                   filtro = f'(DenunciaReuniaoId>{valor})'
                elif campo == 'data':
                   filtro = f'(date(DataHora)=date(\'{valor}\'))'
                if flg:
                   query += ' WHERE ' + filtro
                   flg = False
                else:   
                   query += ' AND ' + filtro
        # print(query)
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    # Criar Usuário
    def criar_usuario(self, email: str, senha: str, nome: str, tipo: str, status: str) -> int | None:
        data_hora = datetime.now()
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO TB_Usuarios (Email, Senha, Nome, Tipo, Status)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, senha, nome, tipo, status))
            conn.commit()
            return cursor.lastrowid

    # Buscar Usuário por Id
    def buscar_usuario_por_id(self, usuario_id: int) -> Optional[Dict]:
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM TB_Usuarios WHERE UsuarioId = ?', (usuario_id,))
            usuario = cursor.fetchone()
            return dict(usuario) if usuario else None

    # Buscar Usuário por Email
    def buscar_usuario_por_email(self, email: str) -> Optional[Dict]:
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM TB_Usuarios WHERE Email = ?', (email,))
            usuario = cursor.fetchone()
            return dict(usuario) if usuario else None

    # Listar Usuários
    def listar_usuarios(self, **kwargs) -> List[Dict]:
        campos_permitidos = {'usuario_id', 'email', 'tipo', 'status'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}

        query = 'SELECT * FROM TB_Usuarios'

        if campos:
            flg = True
            for campo, valor in campos.items():
                if campo == 'usuario_id':
                   filtro = f'(UsuarioId={valor})'
                elif campo == 'email':
                   filtro = f'(Email=\'{valor}\')'
                elif campo == 'tipo':
                   filtro = f'(Tipo=\'{valor}\')'
                elif campo == 'status':
                   filtro = f'(Status=\'{valor}\')'
                if flg:
                   query += ' WHERE ' + filtro
                   flg = False
                else:   
                   query += ' AND ' + filtro
        # print(query)
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    # Atualizar Usuário
    def atualizar_usuario(self, usuario_id: int, **kwargs):
        campos_permitidos = {'senha', 'nome', 'tipo', 'status'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}
        
        if not campos:
            raise ValueError("Nenhum campo válido para atualização")

        query = []
        params = []
        
        for campo, valor in campos.items():
            if campo == 'senha':
                query.append(f"Senha = ?")
            elif campo == 'nome':
                query.append(f"Nome = ?")
            elif campo == 'tipo':
                query.append(f"Tipo = ?")
            elif campo == 'status':
                query.append(f"Status = ?")
            params.append(valor)
        
        params.append(usuario_id)
        
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE TB_Usuarios
                SET {', '.join(query)}
                WHERE UsuarioId = ?
            ''', params)
            conn.commit()
      
    # Deletar Usuário
    def deletar_usuario(self, usuario_id: int) -> bool:
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute('DELETE FROM TB_Usuarios WHERE UsuarioId = ?', (usuario_id,))
            conn.commit()
            return cursor.rowcount > 0

    # Verificar Login Usuário
    def verificar_login_usuario(self, email: str) -> Optional[Dict]:
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM TB_Usuarios 
                WHERE Email = ? AND Status = 'Ativo'
            ''', (email,))
            usuario = cursor.fetchone()
            return dict(usuario) if usuario else None
        
    # Criar Material Educativo
    def criar_material_educativo(self, descricao: str, link: str, usuario_id_criou: int, usuario_id_alterou: int, status: str) -> int | None:
        data_hora = datetime.now()
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO TB_Materiais_Educativos (Descricao, Link, UsuarioIdCriou, UsuarioIdAlterou, DataHoraUltAlt, Status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (descricao, link, usuario_id_criou, usuario_id_alterou, data_hora, status))
            conn.commit()
            return cursor.lastrowid

    # Buscar Material Educativo por Id
    def buscar_material_educativo_por_id(self, material_id: int) -> Optional[Dict]:
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM TB_Materiais_Educativos WHERE MaterialId = ?', (material_id,))
            material_educativo = cursor.fetchone()
            return dict(material_educativo) if material_educativo else None

    # Listar Materiais Educativos
    def listar_materiais_educativos(self, **kwargs) -> List[Dict]:
        campos_permitidos = {'material_id', 'status'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}

        query = 'SELECT * FROM TB_Materiais_Educativos'

        if campos:
            flg = True
            for campo, valor in campos.items():
                if campo == 'material_id':
                   filtro = f'(MaterialId={valor})'
                elif campo == 'status':
                   filtro = f'(Status=\'{valor}\')'
                if flg:
                   query += ' WHERE ' + filtro
                   flg = False
                else:   
                   query += ' AND ' + filtro
        # print(query)
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    # Atualizar Material Educativo
    def atualizar_material_educativo(self, material_id: int, **kwargs):
        campos_permitidos = {'descricao', 'link', 'usuario_id_criou', 'usuario_id_alterou', 'status'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}
       
        if not campos:
            raise ValueError("Nenhum campo válido para atualização")

        query = []
        params = []
        data_hora = datetime.now()
        
        for campo, valor in campos.items():
            if campo == 'descricao':
                query.append(f"Descricao = ?")
            elif campo == 'link':
                query.append(f"Link = ?")
            elif campo == 'usuario_id_criou':
                query.append(f"UsuarioIdCriou = ?")
            elif campo == 'usuario_id_alterou':
                query.append(f"UsuarioIdAlterou = ?")
            elif campo == 'status':
                query.append(f"Status = ?")
            params.append(valor)
        
        query.append(f"DataHoraUltAlt = ?")
        params.append(data_hora)
        params.append(material_id)
        
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE TB_Materiais_Educativos
                SET {', '.join(query)}
                WHERE MaterialId = ?
            ''', params)
            conn.commit()
      
    # Deletar Material Educativo
    def deletar_material_educativo(self, material_id: int) -> bool:
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute('DELETE FROM TB_Materiais_Educativos WHERE MaterialId = ?', (material_id,))
            conn.commit()
            return cursor.rowcount > 0

    # Criar Log
    def criar_log(self, descricao: str, usuario_id: int) -> int | None:
        data_hora = datetime.now()
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO TB_Log (Descricao, UsuarioId, DataHora)
                VALUES (?, ?, ?)
            ''', (descricao, usuario_id, data_hora))
            conn.commit()
            return cursor.lastrowid
        
    # Listar Log
    def listar_log(self, **kwargs) -> List[Dict]:
        campos_permitidos = {'log_id', 'usuario_id', 'data_inicio', 'data_fim'}
        campos = {k: v for k, v in kwargs.items() if k in campos_permitidos}

        query = 'SELECT * FROM TB_Log'

        if campos:
            flg = True
            for campo, valor in campos.items():
                if campo == 'log_id':
                   filtro = f'(LogId={valor})'
                if campo == 'usuario_id':
                   filtro = f'(UsuarioId={valor})'
                elif campo == 'data_inicio':
                   filtro = f'(date(DataHora)>=date(\'{valor}\'))'
                elif campo == 'data_fim':
                   filtro = f'(date(DataHora)<=date(\'{valor}\'))'
                if flg:
                   query += ' WHERE ' + filtro
                   flg = False
                else:   
                   query += ' AND ' + filtro
        # print(query)
        with self._conectar() as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Melhora concorrência
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]