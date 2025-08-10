import pandas as pd
from pathlib import Path
from datetime import datetime
from config import DB_ESTOQUE, DATA_DIR


def mostrar_informacoes_arquivo():
    """Mostra informações detalhadas sobre o arquivo de estoque"""
    print("\n=== INFORMAÇÕES DO ARQUIVO ===")
    print(f"Local do arquivo: {DB_ESTOQUE}")
    print(f"Caminho absoluto: {DB_ESTOQUE.absolute()}")
    print(f"Arquivo existe? {'Sim' if DB_ESTOQUE.exists() else 'Não'}")

    if DB_ESTOQUE.exists():
        print(f"Tamanho do arquivo: {DB_ESTOQUE.stat().st_size} bytes")
        print(f"Última modificação: {datetime.fromtimestamp(DB_ESTOQUE.stat().st_mtime)}")

        try:
            df = pd.read_excel(DB_ESTOQUE)
            print("\nConteúdo do arquivo:")
            print(df)
        except Exception as e:
            print(f"\nErro ao ler arquivo: {e}")


def cadastrar_produto_de_teste():
    """Cadastra um produto de teste com valores padrão"""
    print("\n=== CADASTRANDO PRODUTO DE TESTE ===")

    produto = {
        'codigo': 20,
        'nome': "Parafuso 6mm",
        'quantidade': 100,
        'unidade_medida': "un",
        'local_armazenamento': "Prateleira B3",
        'estoque_minimo': 20,
        'fornecedor': "Fornecedora ABC"
    }

    print("\nDados do produto que será cadastrado:")
    for chave, valor in produto.items():
        print(f"{chave}: {valor}")

    # Carrega ou cria o DataFrame
    try:
        df = pd.read_excel(DB_ESTOQUE)
        print("\nArquivo carregado com sucesso. Conteúdo atual:")
        print(df)
    except FileNotFoundError:
        print("\nArquivo não encontrado. Criando novo DataFrame...")
        colunas = [
            'codigo', 'nome', 'quantidade', 'unidade_medida',
            'local_armazenamento', 'estoque_minimo', 'fornecedor',
            'data_ultima_entrada'
        ]
        df = pd.DataFrame(columns=colunas)

    # Verifica se produto já existe
    if str(produto['codigo']) in df['codigo'].astype(str).values:
        print("\nAVISO: Produto já existe! Atualizando quantidade...")
        idx = df.index[df['codigo'].astype(str) == str(produto['codigo'])][0]
        df.at[idx, 'quantidade'] += produto['quantidade']
    else:
        print("\nProduto não existe. Adicionando novo...")
        novo_produto = {
            **produto,
            'data_ultima_entrada': datetime.now().strftime('%Y-%m-%d')
        }
        df = pd.concat([df, pd.DataFrame([novo_produto])], ignore_index=True)

    # Tenta salvar o arquivo
    try:
        with pd.ExcelWriter(DB_ESTOQUE, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        print("\nArquivo salvo com sucesso!")
        return True
    except Exception as e:
        print(f"\nERRO ao salvar arquivo: {e}")
        print("\nTentando salvar com método alternativo...")
        try:
            df.to_excel(DB_ESTOQUE, index=False)
            print("Salvo com método alternativo!")
            return True
        except Exception as e2:
            print(f"Falha ao salvar: {e2}")
            return False


def verificar_arquivo_depois():
    """Verifica o arquivo após a operação"""
    print("\n=== VERIFICAÇÃO PÓS-CADASTRO ===")
    try:
        df = pd.read_excel(DB_ESTOQUE)
        print("Conteúdo atual do arquivo:")
        print(df)

        print("\nProduto cadastrado:")
        produto = df[df['codigo'].astype(str) == '3']
        if not produto.empty:
            print(produto.iloc[0].to_dict())
        else:
            print("Produto não encontrado no arquivo!")
    except Exception as e:
        print(f"Erro ao verificar arquivo: {e}")


if __name__ == "__main__":
    print("=== TESTE DE CADASTRO DE PRODUTO ===")

    # 1. Mostra informações iniciais
    mostrar_informacoes_arquivo()

    # 2. Tenta cadastrar o produto
    sucesso = cadastrar_produto_de_teste()

    # 3. Verifica o resultado
    if sucesso:
        verificar_arquivo_depois()
    else:
        print("\nFalha no cadastro. Verifique as mensagens acima.")

    print("\n=== TESTE CONCLUÍDO ===")