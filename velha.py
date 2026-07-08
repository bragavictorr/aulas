tabuleiro = [" ", " ", " ",
             " ", " ", " ",
             " ", " ", " "]


def mostrar_tabuleiro():
    print()
    print(tabuleiro[0], "|", tabuleiro[1], "|", tabuleiro[2])
    print("---------")
    print(tabuleiro[3], "|", tabuleiro[4], "|", tabuleiro[5])
    print("---------")
    print(tabuleiro[6], "|", tabuleiro[7], "|", tabuleiro[8])
    print()


def verificar_vitoria():
    combinacoes = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], 
        [0, 3, 6], [1, 4, 7], [2, 5, 8], 
        [0, 4, 8], [2, 4, 6]             
    ]

    for c in combinacoes:
        if tabuleiro[c[0]] == tabuleiro[c[1]] == tabuleiro[c[2]] != " ":
            return True

    return False


jogador = "X"
rodando = True


while rodando:

    mostrar_tabuleiro()

    jogada = int(input(f"Jogador {jogador}, escolha uma posição (1-9): "))

    if jogada < 1 or jogada > 9:
        print("Digite um número entre 1 e 9!")
        continue

    if tabuleiro[jogada - 1] == " ":
        tabuleiro[jogada - 1] = jogador
    else:
        print("Essa posição já está ocupada!")
        continue

    if verificar_vitoria():
        mostrar_tabuleiro()
        print(f"🎉 Jogador {jogador} venceu!")
        rodando = False

    elif " " not in tabuleiro:
        mostrar_tabuleiro()
        print("Empate!")
        rodando = False

    else:
        if jogador == "X":
            jogador = "O"
        else:
            jogador = "X"

