estoque = [
    {"produto":"adidas","preço": 130, "quantidade":20},
    {"produto":"nike","preço": 150, "quantidade":10},
    {"produto":"puma","preço": 115, "quantidade":29}
]


while True:
        escolha_usuario = int(input("Menu\n1-estoque\n2-adiciona novo produto \n3-Dsoma dos preços\n4-soma das quantidades\n5-sair\n:"))
        
        if escolha_usuario == 1:
         for chave in estoque:
            print(chave)
        
        elif escolha_usuario == 2:
           produto = {
           "produto":input("digite novo produto"),
           "valor":int(input("digite o valor")),
           "quantidade":int(input("digiter a quantidade"))
        }
           estoque.append(produto)

        elif escolha_usuario == 3:

         