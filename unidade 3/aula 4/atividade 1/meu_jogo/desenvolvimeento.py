class Deselvolvimento:

    def __init__(self, arma, classe, nome):
        self.arma = arma
        self.classe = classe
        self.nome = nome
        self.dano = 10
        self.nivel = 1
        self.experiencia = 0
        self.vida_maxima = 100
        self.vida = 100
        self.estamina_maxima = 100
        self.estamina = 100

    def ganha_xp(self, xp, vilao):
        self.experiencia += xp

        while self.experiencia >= 100:
            self.experiencia -= 100
            self.nivel += 1
            self.dano += 10

            print(f"{self.nome} subiu para o nível {self.nivel}!")

            vilao.evoluir()

    def ganhar_arma(self, arma):
        self.arma = arma

    def receber_dano(self, dano):
        self.vida = max(0, self.vida - dano)

    def falar(self):
        print(f"{self.nome}: ...")

    def esta_vivo(self):
        return self.vida > 0