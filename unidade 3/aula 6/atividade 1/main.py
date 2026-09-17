class Cadastra:
    def __init__(self):
        self.km = 0 
        self.cor = "" 
        self.ano = 0
        self.marca = "" 
        self.modelo = ""
        self.preço = 0

    def __add__(self, other):
        return self.preço + other.preço
     


    def adicionar(self):
        self.marca = input("Digite o marca do carro: ")
        self.modelo = input("Digite a modelo do carro: ")
        self.ano = input("Digite o ano do carro: ")
        self.cor = input("Digite a cor do carro: ")
        self.km = input("Digite a quilometragem do carro: ")
        self.preço = int(input("Digite a preço do carro: "))
       
    def mostrar(self): 
        print(f"Marca: {self.marca}")
        print(f"Modelo: {self.modelo}")
        print(f"Ano: {self.ano}")
        print(f"Cor: {self.cor}")
        print(f"Quilometragem: {self.km} km")
        print(f"Preço: {self.preço} preço")

    def auteraçao_km(self):
        self.km + 10
        


class Teste_drive(Cadastra):    
    def __init__(self):
        pass


class venda(Cadastra):
    def __init__(self):
        pass

carro1 = Cadastra()
carro1.adicionar()
carro1.mostrar()

carro2 = Cadastra()
carro2.adicionar()
carro2.mostrar()

print(carro1 + carro2)

