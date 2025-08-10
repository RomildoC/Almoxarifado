import pandas as pd
from datetime import datetime
from config import DB_ESTOQUE, HISTORICO  # Agora importando HISTORICO do config
from modules.produtos import carregar_estoque, salvar_estoque


def entrada_estoque(codigo, quantidade, motivo="", responsavel=""):
    """Registra entrada de itens no estoque"""
    try:

        df = carregar_estoque()

        # Converter código para string se necessário (dependendo de como está armazenado)
        codigo = str(codigo)
        idx = df.index[df['codigo'].astype(str) == codigo].tolist()

        if not idx:
            return False, "Produto não encontrado"

        idx = idx[0]

        df.at[idx, 'quantidade'] += quantidade
        df.at[idx, 'data_ultima_entrada'] = datetime.now().strftime('%Y-%m-%d')


        salvar_estoque(df)

        # Registrar movimentação (histórico)
        registrar_movimentacao(
            codigo,
            'entrada',
            quantidade,
            df.at[idx, 'quantidade'],
            responsavel,
            motivo
        )

        return True, "Entrada registrada com sucesso"
    except Exception as e:
        return False, f"Erro ao registrar entrada: {str(e)}"




def saida_estoque(codigo, quantidade, motivo="", responsavel=""):
    """Registra saída de itens do estoque"""
    try:
        df = carregar_estoque()
        idx = df.index[df['codigo'] == codigo].tolist()

        if not idx:
            return False, "Produto não encontrado"

        idx = idx[0]

        if df.at[idx, 'quantidade'] < quantidade:
            return False, "Quantidade insuficiente em estoque"

        df.at[idx, 'quantidade'] -= quantidade
        salvar_estoque(df)

        # Registrar movimentação (histórico)
        registrar_movimentacao(
            codigo,
            'saida',
            quantidade,
            df.at[idx, 'quantidade'],
            responsavel,
            motivo
        )

        return True, "Saída registrada com sucesso"
    except Exception as e:
        return False, f"Erro ao registrar saída: {str(e)}"


def registrar_movimentacao(codigo, tipo, quantidade, saldo_atual, responsavel="", motivo=""):
    """Registra movimentação no histórico"""
    try:
        nova_movimentacao = {
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'codigo_produto': codigo,
            'tipo': tipo,
            'quantidade': quantidade,
            'saldo_atual': saldo_atual,
            'responsavel': responsavel,
            'motivo': motivo
        }

        try:
            df_historico = pd.read_excel(HISTORICO)
        except FileNotFoundError:
            df_historico = pd.DataFrame(columns=nova_movimentacao.keys())

        df_historico = pd.concat(
            [df_historico, pd.DataFrame([nova_movimentacao])],
            ignore_index=True
        )
        df_historico.to_excel(HISTORICO, index=False)

    except Exception as e:
        print(f"Erro ao registrar movimentação: {str(e)}")