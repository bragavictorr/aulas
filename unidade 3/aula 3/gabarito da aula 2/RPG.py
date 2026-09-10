

class Personagem:
    def __init__(self,nome:str):
        self.nome = nome
        self.nivel = 1
        self.experiencia = 0

    def ganha_xp (self,xp):
            self.experiencia += xp

            if self.experiencia > 100:
                self.nivel += 1
                self.experiencia = 0

nome_personagem = input("nome do seu personagem")
xp = int(input("quantos xp vai ser adicionado ao jogador? "))
personagem = Personagem(nome_personagem)
personagem.ganha_xp(xp)

print("Personagem", personagem.nome)
print("Nivel",personagem.nivel)
print("experiencia", personagem.experiencia)

