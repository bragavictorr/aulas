import random

from  desenvolvimeento   import Deselvolvimento


class Vilao(Deselvolvimento):

    def __init__(self, genero, estilo, arma, classe, nome):
        super().__init__(arma, classe, nome)
        self.genero = genero
        self.estilo = estilo

    def falar(self):
        print(f"{self.nome}: Sua alma é minha!")

    def atacar(self):
        escolha = random.randint(1, 3)

        if escolha == 1:
            dano = self.dano

        elif escolha == 2:
            dano = self.dano + 10

        elif escolha == 3:
            dano = self.dano + 20

        return dano

    def evoluir(self):
        self.nivel += 1
        self.dano += 10

        print(f"{self.nome} evoluiu para o nível {self.nivel}!")