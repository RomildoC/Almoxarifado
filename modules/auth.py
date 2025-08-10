import pandas as pd
from getpass import getpass
from hashlib import sha256
from datetime import datetime
from config import DB_USUARIOS, DATA_DIR
import os

# Estrutura do arquivo de usuários (usuarios.xlsx)
"""
| username | nome_completo | hash_senha | nivel_acesso | data_criacao       | ultimo_login      | ativo |
|----------|---------------|------------|--------------|--------------------|-------------------|-------|
| admin    | Administrador| abc123...  | admin        | 2023-01-01 10:00:00| 2023-10-20 15:30:00| True  |
| joao     | João Silva    | def456...  | usuario      | 2023-02-15 09:15:00| 2023-10-19 11:20:00| True  |
"""


def carregar_usuarios():
    """Carrega o DataFrame de usuários ou cria um novo se não existir"""
    try:
        return pd.read_excel(DB_USUARIOS)
    except FileNotFoundError:
        colunas = [
            'username', 'nome_completo', 'hash_senha',
            'nivel_acesso', 'data_criacao', 'ultimo_login', 'ativo'
        ]
        df = pd.DataFrame(columns=colunas)
        # Cria usuário admin padrão se o arquivo não existir
        criar_usuario(
            username="admin",
            nome_completo="Administrador do Sistema",
            senha="admin",
            nivel_acesso="admin",
            ativo=True
        )
        return df


def salvar_usuarios(df):
    """Salva o DataFrame de usuários no arquivo Excel"""
    df.to_excel(DB_USUARIOS, index=False)


def hash_senha(senha):
    """Gera o hash SHA-256 de uma senha"""
    return sha256(senha.encode('utf-8')).hexdigest()


def criar_usuario(username, nome_completo, senha, nivel_acesso="usuario", ativo=True):
    """Cria um novo usuário no sistema"""
    try:
        df = carregar_usuarios()

        if username in df['username'].values:
            return False, "Nome de usuário já existe"

        if nivel_acesso not in ['admin', 'usuario', 'consulta']:
            return False, "Nível de acesso inválido"

        novo_usuario = {
            'username': username,
            'nome_completo': nome_completo,
            'hash_senha': hash_senha(senha),
            'nivel_acesso': nivel_acesso,
            'data_criacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ultimo_login': None,
            'ativo': ativo
        }

        df = pd.concat([df, pd.DataFrame([novo_usuario])], ignore_index=True)
        salvar_usuarios(df)
        return True, "Usuário criado com sucesso"

    except Exception as e:
        return False, f"Erro ao criar usuário: {str(e)}"


def autenticar_usuario(username, senha):
    """Autentica um usuário com nome e senha"""
    try:
        df = carregar_usuarios()
        usuario = df[(df['username'] == username) & (df['ativo'] == True)]

        if usuario.empty:
            return False, "Usuário não encontrado ou inativo", None

        usuario = usuario.iloc[0]

        if usuario['hash_senha'] != hash_senha(senha):
            return False, "Senha incorreta", None

        # Atualiza último login
        df.loc[df['username'] == username, 'ultimo_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        salvar_usuarios(df)

        return True, "Autenticação bem-sucedida", {
            'username': usuario['username'],
            'nome_completo': usuario['nome_completo'],
            'nivel_acesso': usuario['nivel_acesso']
        }

    except Exception as e:
        return False, f"Erro na autenticação: {str(e)}", None


def alterar_senha(username, senha_atual, nova_senha):
    """Altera a senha de um usuário"""
    try:
        df = carregar_usuarios()
        usuario = df[df['username'] == username]

        if usuario.empty:
            return False, "Usuário não encontrado"

        if usuario.iloc[0]['hash_senha'] != hash_senha(senha_atual):
            return False, "Senha atual incorreta"

        df.loc[df['username'] == username, 'hash_senha'] = hash_senha(nova_senha)
        salvar_usuarios(df)
        return True, "Senha alterada com sucesso"

    except Exception as e:
        return False, f"Erro ao alterar senha: {str(e)}"


def listar_usuarios():
    """Lista todos os usuários do sistema (apenas para admin)"""
    try:
        df = carregar_usuarios()
        return True, df.to_dict('records')
    except Exception as e:
        return False, f"Erro ao listar usuários: {str(e)}"


def desativar_usuario(username, admin_username):
    """Desativa um usuário (apenas para admin)"""
    try:
        # Verifica se quem está desativando é admin
        df = carregar_usuarios()
        admin = df[df['username'] == admin_username]

        if admin.empty or admin.iloc[0]['nivel_acesso'] != 'admin':
            return False, "Apenas administradores podem desativar usuários"

        if username == admin_username:
            return False, "Você não pode desativar a si mesmo"

        if username not in df['username'].values:
            return False, "Usuário não encontrado"

        df.loc[df['username'] == username, 'ativo'] = False
        salvar_usuarios(df)
        return True, f"Usuário {username} desativado com sucesso"

    except Exception as e:
        return False, f"Erro ao desativar usuário: {str(e)}"