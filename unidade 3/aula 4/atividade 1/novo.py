class Jogo:

    def __init__(self, titulo: str, plataforma: str, genero: str, dificuldade: str):
        self.titulo = titulo
        self.plataforma = plataforma
        self.genero = genero
        self.dificuldade = dificuldade

        # Classe agregadora
        self.heroi = None
        self.vilao = None

    def adicionar_heroi(self, heroi):
        self.heroi = heroi

    def adicionar_vilao(self, vilao):
        self.vilao = vilao

    def iniciar_batalha(self):

        while True:

            print("\n========================")
            print("        BATALHA")
            print("========================")

            print("\n--- HERÓI ---")
            print("Nome:", self.heroi.nome)
            print("Classe:", self.heroi.classe)
            print("Nível:", self.heroi.nivel)
            print("XP:", self.heroi.experiencia)
            print("Dano:", self.heroi.dano)
            print("Arma:", self.heroi.arma)

            print("\n--- VILÃO ---")
            print("Nome:", self.vilao.nome)
            print("Classe:", self.vilao.classe)
            print("Nível:", self.vilao.nivel)
            print("Vida:", self.vilao.vida)
            print("Dano:", self.vilao.dano)
            print("Arma:", self.vilao.arma)

            print("\n1 - Atacar")
            print("2 - Sair")

            escolha = input("\nEscolha: ")

            if escolha == "1":

                derrotou = self.heroi.atacar(self.vilao)

                if derrotou:

                    print("\n💀 VILÃO DERROTADO!")
                    print("Você ganhou 50 XP!")

                    # Herói ganha XP
                    self.heroi.ganha_xp(50)

                    # Vilão evolui junto com o herói
                    self.vilao.ganha_nivel(1)

                    # Recupera a vida do próximo vilão
                    self.vilao.restaura_vida()

                    print("\n🔥 Um novo vilão apareceu!")
                    print("Nível do vilão:", self.vilao.nivel)
                    print("Vida do vilão:", self.vilao.vida)

            elif escolha == "2":

                print("\nVocê saiu do jogo.")
                break

            else:

                print("\n❌ Opção inválida!")


class Heroi:

    def __init__(self, classe, nome, genero, arma):

        self.classe = classe
        self.nome = nome
        self.genero = genero
        self.arma = arma

        self.dano = 10
        self.experiencia = 0
        self.nivel = 1

    def ganha_xp(self, xp):

        self.experiencia += xp

        while self.experiencia >= 100:

            self.experiencia -= 100
            self.nivel += 1
            self.dano += 10

            print("\n🎉 VOCÊ SUBIU DE NÍVEL!")
            print("Seu nível agora é:", self.nivel)
            print("Seu dano agora é:", self.dano)

            if self.nivel == 2:

                self.ganhar_arma("Arma incomum")

            elif self.nivel == 3:

                self.ganhar_arma("Arma rara")

            elif self.nivel == 4:

                self.ganhar_arma("Arma épica")

            elif self.nivel == 5:

                self.ganhar_arma("Arma lendária")

            elif self.nivel == 6:

                self.ganhar_arma("Arma mística")

    def atacar(self, vilao):

        vilao.vida -= self.dano

        print("\n⚔️ Você atacou o vilão!")
        print("Você causou", self.dano, "de dano.")
        print("Vida restante do vilão:", vilao.vida)

        if vilao.vida <= 0:

            return True

        return False

    def ganhar_arma(self, arma):

        self.arma = arma

        print("🎁 Você recebeu:", arma)


class Vilao:

    def __init__(self, classe, nome, genero, estilo, arma):

        self.classe = classe
        self.nome = nome
        self.genero = genero
        self.estilo = estilo
        self.arma = arma

        self.nivel = 1
        self.dano = 10

        self.vida_maxima = 50
        self.vida = self.vida_maxima

    def ganha_nivel(self, nivel):

        self.nivel += nivel
        self.dano += 10
        self.vida_maxima += 20

        print("\n👹 O VILÃO EVOLUIU!")
        print("Nível do vilão:", self.nivel)
        print("Dano do vilão:", self.dano)
        print("Vida máxima:", self.vida_maxima)

    def restaura_vida(self):

        self.vida = self.vida_maxima


# ==========================================
# CRIANDO O JOGO
# ==========================================

jogo1 = Jogo(
    "Skyrim",
    "PC",
    "RPG",
    "Hard"
)


# ==========================================
# CRIANDO O HERÓI
# ==========================================

heroi1 = Heroi(
    "Guerreiro",
    "Mauricio",
    "Masculino",
    "Espada"
)


# ==========================================
# CRIANDO O VILÃO
# ==========================================

vilao1 = Vilao(
    "Guerreiro",
    "Dragão",
    "Masculino",
    "Agressivo",
    "Espada"
)


# ==========================================
# ADICIONANDO AO JOGO
# ==========================================

jogo1.adicionar_heroi(heroi1)
jogo1.adicionar_vilao(vilao1)


# ==========================================
# INFORMAÇÕES DO JOGO
# ==========================================

print("\n========================")
print("        JOGO")
print("========================")

print("Título:", jogo1.titulo)
print("Plataforma:", jogo1.plataforma)
print("Gênero:", jogo1.genero)
print("Dificuldade:", jogo1.dificuldade)


# ==========================================
# INICIANDO O JOGO
# ==========================================

jogo1.iniciar_batalha()