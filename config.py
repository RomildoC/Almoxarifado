import os
from pathlib import Path

# Caminho absoluto para a pasta Almoxarifado
BASE_DIR = Path(__file__).parent  # Ajuste esta linha
DATA_DIR = BASE_DIR / 'data'  # Caminho corrigido

# Caminhos dos arquivos Excel
DB_ESTOQUE = DATA_DIR / 'database.xlsx'
DB_USUARIOS = DATA_DIR / 'usuarios.xlsx'
HISTORICO = DATA_DIR / 'historico.xlsx'

# Criar diretórios se não existirem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DATA_DIR / 'backups', exist_ok=True)
