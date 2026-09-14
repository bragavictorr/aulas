from heroi import Heroi
from vilao import Vilao
from jogo import Jogo

import random


# =========================
# CRIANDO O JOGO
# =========================

jogo1 = Jogo(
    "Skyrim",
    "PC",
    "RPG",
    "Hard"
)


# =========================
# CRIANDO O HERÓI
# =========================

heroi1 = Heroi(
    "masculino",
    "espada comum",
    "guerreiro",
    "subzero"
)


# =========================
# DADOS DOS VILÕES
# =========================

nomes = [
    "Shang Tsung",
    "Scorpion",
    "Raiden",
    "Noob Saibot",
    "Shao Kahn"
]

armas = [
    "katana",
    "espada",
    "martelo",
    "foice",
    "machado"
]

classes = [
    "guerreiro",
    "mago",
    "assassino",
    "tanque"
]

estilos = [
    "sombra",
    "fogo",
    "gelo",
    "trevas"
]


# =========================
# CRIANDO O PRIMEIRO VILÃO
# =========================

vilao1 = Vilao(
    "masculino",
    random.choice(estilos),
    random.choice(armas),
    random.choice(classes),
    random.choice(nomes)
)


# =========================
# SISTEMA DE BATALHA
# =========================

while heroi1.esta_vivo():

    print()
    print("================================")
    print("          NOVO VILÃO")
    print("================================")

    print("Nome:", vilao1.nome)
    print("Nível:", vilao1.nivel)
    print("Vida:", vilao1.vida)
    print("Dano:", vilao1.dano)
    print("Arma:", vilao1.arma)
    print("Classe:", vilao1.classe)

    print()

    # BATALHA CONTRA O VILÃO

    while heroi1.esta_vivo() and vilao1.esta_vivo():

        # =========================
        # ESCOLHA DO ATAQUE
        # =========================

        while True:

            print()
            print("========== ATAQUES ==========")
            print("1 - Ataque normal")
            print("2 - Ataque forte   [20 estamina]")
            print("3 - Ataque poderoso [40 estamina]")
            print()
            print("Estamina:", heroi1.estamina)
            print("==============================")

            escolha = int(
                input("Escolha seu ataque: ")
            )

            if escolha in [1, 2, 3]:
                break

            print()
            print("❌ Escolha inválida!")
            print("Digite 1, 2 ou 3.")


        # =========================
        # HERÓI ATACA
        # =========================

        dano = heroi1.atacar(escolha)


        # SEM ESTAMINA
        if dano is None:
            continue


        vilao1.receber_dano(dano)


        print()
        print("⚔️ Herói causou:", dano)
        print("❤️ Vida do vilão:", vilao1.vida)
        print("⚡ Estamina:", heroi1.estamina)


        # =========================
        # VERIFICA SE O VILÃO MORREU
        # =========================

        if not vilao1.esta_vivo():

            print()
            print("💀 O vilão foi derrotado!")

            # HERÓI GANHA 50 XP
            heroi1.ganha_xp(50, vilao1)

            print()
            print("⭐ XP do herói:", heroi1.experiencia)
            print("⭐ Nível do herói:", heroi1.nivel)

            break


        # =========================
        # VILÃO ATACA
        # =========================

        dano = vilao1.atacar()

        heroi1.receber_dano(dano)


        print()
        print("👹 Vilão causou:", dano)
        print("❤️ Vida do herói:", heroi1.vida)


        # =========================
        # VERIFICA SE O HERÓI MORREU
        # =========================

        if not heroi1.esta_vivo():

            break


    # =========================
    # HERÓI MORREU
    # =========================

    if not heroi1.esta_vivo():
        break


    # =========================
    # CRIA UM NOVO VILÃO
    # =========================

    print()
    print("🔄 Preparando próximo inimigo...")


    vilao1 = Vilao(
        "masculino",
        random.choice(estilos),
        random.choice(armas),
        random.choice(classes),
        random.choice(nomes)
    )


    # =========================
    # VILÃO ACOMPANHA O NÍVEL
    # DO HERÓI
    # =========================

    while vilao1.nivel < heroi1.nivel:

        vilao1.evoluir()


# =========================
# RESULTADO FINAL
# =========================

print()
print("================================")
print("          FIM DE JOGO")
print("================================")


if heroi1.esta_vivo():

    print("🏆 O HERÓI VENCEU!")

else:

    print("💀 O VILÃO VENCEU!")


# =========================
# STATUS FINAL
# =========================

print()
print("========== STATUS ==========")

print()
print("🧙 HERÓI")
print("Nome:", heroi1.nome)
print("Nível:", heroi1.nivel)
print("XP:", heroi1.experiencia)
print("Dano:", heroi1.dano)
print("Vida:", heroi1.vida)
print("Estamina:", heroi1.estamina)
print("Arma:", heroi1.arma)
print("Classe:", heroi1.classe)

print()
print("👹 ÚLTIMO VILÃO")
print("Nome:", vilao1.nome)
print("Nível:", vilao1.nivel)
print("Dano:", vilao1.dano)
print("Vida:", vilao1.vida)
print("Arma:", vilao1.arma)
print("Classe:", vilao1.classe)