import pandas as pd
import os
from datetime import datetime
from config import DB_ESTOQUE

UNIDADES_VALIDAS = ['un', 'kg', 'g', 'lt', 'ml', 'm', 'cm', 'mm', 'cx', 'pc', 'dz', 'ton', 'l', 'kg']

def validar_unidade_medida(unidade):
    """Verifica se a unidade de medida é válida"""
    return unidade.lower() in UNIDADES_VALIDAS


def cadastrar_produto(codigo, nome, quantidade, unidade_medida, local, estoque_minimo=0, fornecedor=""):
    """Cadastra um novo produto no sistema"""
    try:
        # Validações (mantidas as anteriores)
        if not validar_unidade_medida(unidade_medida):
            unidades_str = ", ".join(UNIDADES_VALIDAS)
            return False, f"Unidade de medida inválida. Unidades válidas: {unidades_str}"

        df = carregar_estoque()

        # Verifica se o código já existe (convertendo para string para comparação)
        if not df.empty and str(codigo) in df['codigo'].astype(str).values:
            return False, "Código de produto já existe"

        # Cria o novo produto como um DataFrame
        novo_produto_df = pd.DataFrame([{
            'codigo': str(codigo),
            'nome': nome,
            'quantidade': float(quantidade),
            'unidade_medida': unidade_medida.lower(),
            'local_armazenamento': local,
            'estoque_minimo': float(estoque_minimo),
            'fornecedor': fornecedor,
            'data_ultima_entrada': datetime.now().strftime('%Y-%m-%d')
        }])

        # Concatenação correta - garante que vai adicionar nova linha
        df = pd.concat([df, novo_produto_df], ignore_index=True)

        # Remove possíveis duplicatas (por segurança)
        df = df.drop_duplicates(subset=['codigo'], keep='last')

        salvar_estoque(df)
        return True, "Produto cadastrado com sucesso"

    except ValueError as ve:
        return False, f"Erro de valor: {str(ve)}"
    except Exception as e:
        return False, f"Erro ao cadastrar produto: {str(e)}"


def listar_produtos():
    """Retorna todos os produtos em estoque"""
    try:
        df = carregar_estoque()
        return True, df.to_dict('records')
    except Exception as e:
        return False, f"Erro ao listar produtos: {str(e)}"


def buscar_produto(codigo):
    """Busca um produto pelo código"""
    try:
        df = carregar_estoque()
        produto = df[df['codigo'] == codigo]

        if produto.empty:
            return False, "Produto não encontrado"

        return True, produto.iloc[0].to_dict()
    except Exception as e:
        return False, f"Erro ao buscar produto: {str(e)}"


def carregar_estoque():
    """Carrega o arquivo de estoque, criando se não existir"""
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(DB_ESTOQUE):
            # Cria um DataFrame vazio com as colunas corretas
            colunas = [
                'codigo', 'nome', 'quantidade', 'unidade_medida',
                'local_armazenamento', 'estoque_minimo', 'fornecedor',
                'data_ultima_entrada'
            ]
            return pd.DataFrame(columns=colunas)

        # Se o arquivo existe, carrega normalmente
        df = pd.read_excel(DB_ESTOQUE)

        # Garante que temos todas as colunas necessárias
        colunas_necessarias = [
            'codigo', 'nome', 'quantidade', 'unidade_medida',
            'local_armazenamento', 'estoque_minimo', 'fornecedor',
            'data_ultima_entrada'
        ]

        for col in colunas_necessarias:
            if col not in df.columns:
                df[col] = None if col != 'quantidade' else 0.0

        return df

    except Exception as e:
        print(f"Erro ao carregar estoque: {str(e)}")
        return pd.DataFrame()


def salvar_estoque(df):
    """Salva o dataframe no arquivo Excel"""
    try:
        # Garante o diretório existe
        os.makedirs(os.path.dirname(DB_ESTOQUE), exist_ok=True)

        # Salva com engine openpyxl (mais robusta)
        df.to_excel(
            DB_ESTOQUE,
            index=False,
            engine='openpyxl'
        )
    except Exception as e:
        print(f"Erro ao salvar estoque: {str(e)}")
        raise