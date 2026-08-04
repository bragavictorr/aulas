import random

mapa_jogador= [
    ["~","~","~","~"],
    ["~","~","~","~"],
    ["~","~","~","~"],
    ["~","~","~","~"]
]

mapa_computador= [
    ["~","~","~","~"],
    ["~","~","~","~"],
    ["~","~","~","~"],
    ["~","~","~","~"]
    
   
]

#jogado escolher a onde bota o barquinho
print("onde colocar o barquinho")
while True: 
    LINHA_INICIAL_JOGADOR = int(input("escolha uma linha:"))
    COLUNA_INICIAL_JOGADOR = int(input("escolha uma coluna:"))

    if escolha_linha_jogador > 3 or escolha_coluna_computador > 3:

        mapa_jogador[LINHA_INICIAL_JOGADOR][COLUNA_INICIAL_JOGADOR] = "o"


    # o computado escolhe a onde deixa o barquinho
    LINHA_INICIAL_COMPUTADOR = random.randint(0,3)
    COLUNA_INICIAL_COMPUTADOR = random.randint(0,3)

    while True:
        print("sua vez de atacar!")
        escolha_linha_jogador = int(input("escolha uma linha:"))
        escolha_coluna_jogador = int(input("escolha uma coluna:"))

        if (escolha_linha_jogador == LINHA_INICIAL_COMPUTADOR) and \
        (escolha_coluna_jogador == COLUNA_INICIAL_COMPUTADOR):
            print("voce ganhou!")
            break
        else:
            print("voce errou!")
            mapa_computador[escolha_linha_jogador][escolha_coluna_jogador] = "x"

            for linha in mapa_computador:
                print("   ".join(linha))
            
        print("vez do computador")

        while True:
            escolha_linha_computador = random.randint(0,3)
            escolha_coluna_computador = random.randint(0,3)

            if mapa_jogador[escolha_coluna_computador][escolha_linha_computador] == "x":
                continue
            else:
                break

        if escolha_linha_computador == LINHA_INICIAL_JOGADOR and \
        escolha_coluna_computador == COLUNA_INICIAL_JOGADOR:
            print("voce perdeu")
            break
        else: 
            mapa_jogador[escolha_linha_computador][escolha_coluna_computador] = "x"
            for linha in mapa_jogador:
                print("   ".join(linha))



    
