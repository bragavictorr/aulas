class Produto:
    def __init__(self, nome:str, preco:float, quantidade_em_estoque:int):
        self.nome = nome
        self.preco = preco
        self.quantidade_em_estoque = quantidade_em_estoque

    def vender(self, quantidade_vendida):
        print(f"valor total: R$", quantidade_vendida*self.preco)


produto1 = Produto("arroz", 2.50, 500)
produto1.vender(100)