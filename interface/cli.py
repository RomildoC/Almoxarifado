def main_menu():
    print("\n=== SISTEMA DE ALMOXARIFADO ===")
    print("1. Produto")
    print("2. Estoque")
    print("3. Usuários")
    print("4. Sair")
    entrada = input("Escolha uma opção: ")

    match entrada:
        case "1":
            print("\nMenu de Produto:")
            print("1. Cadastrar produto")
            print("2. Editar produto")
            print("3. Excluir produto")
            entrada_produto = input("Escolha uma opção: ")
            return entrada_produto
        case "2":
            print("\nMenu de Estoque:")
            print("1. Entrada de Estoque")
            print("2. Saída de Estoque")
            entrada_estoque = input("Escolha uma opção: ")
            return entrada_estoque
        case "3":
                print("\nMenu de Usuários:")
                print("1. Visualizar Usuários")
                print("2. Adcionar Usuário")
                print("2. Editar Usuário")
                print("3. Excluir Usuário")
                entrada_usuario = input("Escolha uma opção: ")
                return entrada_usuario
        case "4":
            print("Saindo do acesso")
