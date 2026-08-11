estoque = [
    {"produto": "adidas", "preço": 130, "quantidade": 20},
    {"produto": "nike", "preço": 150, "quantidade": 10},
    {"produto": "puma", "preço": 115, "quantidade": 29}
]

def new_sistema():
    while True:
        try:
            escolha_usuario = int(input("Menu\n1- Ver estoque\n2- Adicionar novo produto\n3- Soma dos preços\n4- Soma das quantidades\n5- Sair\nEscolha uma opção: "))
        except ValueError:
            print("Por favor, digite um número válido.")
            continue

        if escolha_usuario == 1:
            print("Estoque atual:")
            for produto in estoque:
                print(produto)

        elif escolha_usuario == 2:
            try:
                novo_produto = {
                    "produto": input("Digite o nome do novo produto: "),
                    "preço": float(input("Digite o preço: ")),
                    "quantidade": int(input("Digite a quantidade: "))
                }
                estoque.append(novo_produto)
                print("Produto adicionado com sucesso!")
            except ValueError:
                print("Erro: Certifique-se de digitar valores válidos para preço e quantidade.")

        elif escolha_usuario == 3:
            total_geral = 0
            for produto in estoque:
                total_geral += produto["preço"] * produto["quantidade"]
            print(f"Total geral da soma dos preços: {total_geral}")

        elif escolha_usuario == 4:
            total_quantidade = 0
            for produto in estoque:
                total_quantidade += produto["quantidade"]
            print(f"Total da quantidade: {total_quantidade}")

        elif escolha_usuario == 5:
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

# Inicia o sistema
new_sistema()


         

      

          
         

         
      