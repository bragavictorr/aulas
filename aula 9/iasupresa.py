import random
import time

LARGURA_LINHA = 48


def linha(caractere="-"):
    print(caractere * LARGURA_LINHA)


def pausa(segundos=0.6):
    time.sleep(segundos)


BANNER = r"""
  ____   ____   ____   ___
 |  _ \ / __ \ / ___| / _ \
 | |_) | |  | | |     | | | |
 |  __/| |__| | |___  | |_| |
 |_|    \____/ \____|  \___/
     O   P O Ç O   S E M   F U N D O
"""

EVENTOS = [
    {
        "nome": "Joia da Sorte",
        "descricao": "um brilho azul vai te proteger do próximo tropeço nesta descida.",
        "efeito": "perdao",
    },
    {
        "nome": "Maldição do Ouro Fraco",
        "descricao": "o ouro encontrado aqui embaixo vale só a metade.",
        "efeito": "meio_ouro",
    },
    {
        "nome": "Mapa Antigo",
        "descricao": "você encontra 5 moedas escondidas logo na entrada.",
        "efeito": "bonus_fixo",
    },
    {
        "nome": "Neblina Densa",
        "descricao": "um número já nasce 'gasto' antes mesmo da primeira rolada.",
        "efeito": "risco_extra",
    },
]


def intro():
    print(BANNER)
    linha("=")
    print("Você é um(a) aventureiro(a) descendo em um poço amaldiçoado atrás de ouro.")
    print("A cada descida, você rola um dado (1 a 6) quantas vezes quiser.")
    print(" - Número NOVO nesta descida  -> você ganha ouro.")
    print(" - Número REPETIDO nesta descida -> o poço desaba e você perde")
    print("   TODO o ouro conseguido nesta descida (o resto fica salvo).")
    print("A qualquer momento você pode SUBIR e guardar o que já ganhou,")
    print("ou arriscar descendo mais fundo por mais ouro.")
    print("De vez em quando, algo inesperado acontece lá embaixo...")
    linha("=")
    input("\nPressione ENTER para começar a descer...")


def escolher_evento():
    return random.choice(EVENTOS)


def realizar_descida(numero_descida):
    print(f"\n=== Descida {numero_descida} ===")
    numeros_usados = set()
    ouro_descida = 0
    perdao_disponivel = False
    multiplicador = 1

    if numero_descida % 3 == 0:
        evento = escolher_evento()
        print(f"\n✨ Evento especial: {evento['nome']}")
        print(f"   {evento['descricao']}")
        pausa()

        if evento["efeito"] == "perdao":
            perdao_disponivel = True
        elif evento["efeito"] == "meio_ouro":
            multiplicador = 0.5
        elif evento["efeito"] == "bonus_fixo":
            ouro_descida += 5
        elif evento["efeito"] == "risco_extra":
            numero_bloqueado = random.randint(1, 6)
            numeros_usados.add(numero_bloqueado)
            print(f"   (o número {numero_bloqueado} já está 'gasto' nesta descida)")

    while True:
        input("\nPressione ENTER para rolar o dado...")
        dado = random.randint(1, 6)
        print(f"🎲 Você rolou: {dado}")

        colapsou = dado in numeros_usados and not perdao_disponivel

        if colapsou:
            print("💥 COLAPSO! O teto desaba e todo o ouro desta descida se perde.")
            pausa()
            return 0

        if dado in numeros_usados and perdao_disponivel:
            print("   A joia da sorte brilha e perdoa esse tropeço!")
            perdao_disponivel = False
        else:
            numeros_usados.add(dado)
            ganho = int(dado * 2 * multiplicador)
            ouro_descida += ganho
            print(f"   Você encontra {ganho} moedas de ouro! (nesta descida: {ouro_descida})")

        if len(numeros_usados) >= 6:
            bonus = 15
            print(f"\n🌟 Descida perfeita! Todos os números saíram sem colapso. Bônus de {bonus} moedas!")
            ouro_descida += bonus
            pausa()
            return ouro_descida

        escolha = input("Continuar descendo (d) ou subir com o ouro (s)? [d/s]: ").strip().lower()
        if escolha == "s":
            print(f"Você sobe com {ouro_descida} moedas guardadas em segurança.")
            return ouro_descida


def classificacao(ouro):
    if ouro < 20:
        return "Aprendiz Desastrado"
    if ouro < 50:
        return "Caçador de Moedas"
    if ouro < 90:
        return "Explorador Experiente"
    return "Lenda do Poço Sem Fundo"


def jogar():
    intro()
    ouro_total = 0
    max_descidas = 6

    for numero_descida in range(1, max_descidas + 1):
        ouro_total += realizar_descida(numero_descida)
        print(f"\nOuro total acumulado: {ouro_total}")
        linha()

        if numero_descida < max_descidas:
            continuar = input(
                "Pressione ENTER para a próxima descida, ou digite 'sair' para encerrar agora: "
            ).strip().lower()
            if continuar == "sair":
                break

    linha("=")
    print(f"Fim da jornada! Ouro total: {ouro_total}")
    print(f"Seu título: {classificacao(ouro_total)}")
    linha("=")


def main():
    try:
        while True:
            jogar()
            de_novo = input("\nJogar novamente? (s/n): ").strip().lower()
            if de_novo != "s":
                print("Até a próxima aventura!")
                break
    except (EOFError, KeyboardInterrupt):
        print("\nAté a próxima aventura!")


if __name__ == "__main__":
    main()