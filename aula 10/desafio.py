

estoque = [
    {"produto":"adidas","preço": 130, "quantidade":20},
    {"produto":"nike","preço": 150, "quantidade":10},
    {"produto":"puma","preço": 115, "quantidade":29}
]

escolha ="sim"
while True:
    input("deseja adiciona novo produto?")
    if escolha == "sim":
        novo_produto = input("digite o produto:")
        preço_produto = float(input("digiter o preço do produto:"))
        quantidade_produto = int(input("digiter a quantidade:"))

        estoque.append({"produto": novo_produto, "preço": preço_produto, "quantidade":quantidade_produto})
    else:
        print("ok")

    for dicionario in estoque:
        print(dicionario)

