class Jogo:
    def __init__(self, titulo:str, plataforma:str, genero:str, dificuldade:str):
        self.titulo = titulo
        self.plataforma = plataforma
        self.genero = genero
        self.dificuldade = dificuldade
    
   

       


class Heroi:
    def __init__(self, classe, nome, genero, arma):
        self.classe = classe
        self.nome = nome
        self.genero = genero
        self.arma = arma
        self.dano = 10
        self.experiencia = 0
        self.nivel = 1

    def ganha_xp (self,xp):
            self.experiencia += xp

            if self.experiencia >= 100:
                self.nivel += 1
                self.dano += 10
                self.experiencia = 0
                restante = xp - 100
                if self.nivel == 2:
                    self.ganhar_arma("arma incomum ")
                
                elif self.nivel == 3:
                    self.ganhar_arma("arma rara")
                
                elif self.nivel == 4:
                    self.ganhar_arma("arma epica")    

                elif self.nivel == 5:
                    self.ganhar_arma("arma lendario ")

                elif self.nivel == 6:
                    self.ganhar_arma("arma mistica ")

                if restante > 0:
                    self.ganha_xp(restante)


               

    def ganhar_arma(self,arma):
        self.arma = arma


    
class vilao:
    def __init__(self, classe, nome, genero, estilo, arma):
        self.classe = classe
        self.nome = nome
        self.genero = genero
        self.estilo = estilo
        self.arma = arma
        self.nivel = 1
        self.dano = 10

    def ganha_nivel(self,nivel):
         self.nivel += nivel

         if self.nivel > 100:
            self.dano = 10

jogo1 = Jogo ("skyrim" , "pc", "rpg", "hard")
heroi1 = Heroi("guerreiro", "mauricio", "masculino", "espada")


print(jogo1.titulo, jogo1.plataforma, jogo1.genero, jogo1.dificuldade)
heroi1.ganha_xp(200)
heroi1.ganhar_arma

print(heroi1.nivel)
print(heroi1.arma)
print(heroi1.dano)
print(heroi1.experiencia)
