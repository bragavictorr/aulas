from desenvolvimeento import Deselvolvimento


class Heroi(Deselvolvimento):

    def __init__(self, genero, arma, classe, nome):
        super().__init__(arma, classe, nome)
        self.genero = genero

    def falar(self):
        print(f"{self.nome}: Sinta o frio do desespero.")

   

    def atacar(self, escolha):

        if escolha == 1:
            custo = 0
            dano = self.dano

        elif escolha == 2:
            custo = 20
            dano = self.dano + 10

        elif escolha == 3:
            custo = 40
            dano = self.dano + 20

        if self.estamina >= custo:
            self.estamina -= custo
            return dano

        else:
            print("❌ Estamina insuficiente!")
            return None