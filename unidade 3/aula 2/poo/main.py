class Carro:
    def __init__(self, cor, ano, modelo):
        self.cor = cor
        self.ano = ano
        self.modelo = modelo
        self.cambio = "automatico"

    def buzinar(self):
        print("biiiii biiii")

carro = Carro("prata", 2025, "hilux")
carro

carro2 = Carro("blue", 2020, "yaris")
