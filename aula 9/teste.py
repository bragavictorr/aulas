import random
import time

# Códigos de Cores ANSI para o Terminal
AZUL = "\033[94m"
AZUL_CLARO = "\033[96m"
VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
ROXO = "\033[95m"
CINZA = "\033[90m"
RESET = "\033[0m"
NEGRITO = "\033[1m"

TAMANHO = 8  # Tabuleiro maior (8x8) para mais estratégia
VIDAS_INICIAIS = 5

mapa_jogador = [["~" for _ in range(TAMANHO)] for _ in range(TAMANHO)]
mapa_computador = [["~" for _ in range(TAMANHO)] for _ in range(TAMANHO)]

def imprimir_tabuleiro(matriz, mostrar_navios=False):
    print(AZUL_CLARO + "    " + " ".join([str(i) for i in range(TAMANHO)]) + RESET)
    print(AZUL_CLARO + "  + " + "--- " * TAMANHO + "+" + RESET)
    for idx, linha in enumerate(matriz):
        linha_formatada = []
        for celula in linha:
            if celula == "~":
                linha_formatada.append(AZUL + "~" + RESET)
            elif celula == "O":
                if mostrar_navios:
                    linha_formatada.append(VERDE + "O" + RESET)
                else:
                    linha_formatada.append(AZUL + "~" + RESET)
            elif celula == "X":
                linha_formatada.append(VERMELHO + NEGRITO + "X" + RESET)
            elif celula == "x":
                linha_formatada.append(AMARELO + "x" + RESET)
        print(AZUL_CLARO + f"{idx} |" + RESET + "   ".join(linha_formatada) + AZUL_CLARO + "|" + RESET)
    print(AZUL_CLARO + "  + " + "--- " * TAMANHO + "+" + RESET)

print(NEGRITO + AMARELO + "╔════════════════════════════════════════╗" + RESET)
print(NEGRITO + AMARELO + "║   BATALHA NAVAL: GUERRA DOS OCEANOS    ║" + RESET)
print(NEGRITO + AMARELO + "╚════════════════════════════════════════╝" + RESET)
print(f"Tabuleiro épico de {TAMANHO}x{TAMANHO}. Prepare sua frota de 3 navios!")

# Definição dos tamanhos dos barcos da frota
tamanhos_frota = [3, 2, 1]  # Porta-aviões (3), Cruzador (2), Lancha (1) = Total 6 partes

# --- POSICIONAMENTO DOS BARCOS DO JOGADOR ---
barcos_jogador = []

for i, tamanho in enumerate(tamanhos_frota, 1):
    print(f"\n{AMARELO}--- Posicionar Navio {i} (Tamanho: {tamanho} blocos na horizontal) ---{RESET}")
    imprimir_tabuleiro(mapa_jogador, mostrar_navios=True)
    
    while True:
        try:
            linha = int(input(f"Escolha a linha (0-{TAMANHO-1}): "))
            coluna = int(input(f"Escolha a coluna inicial (0-{TAMANHO-tamanho}): "))
            
            if 0 <= linha < TAMANHO and 0 <= coluna <= TAMANHO - tamanho:
                # Verifica se o espaço está livre
                livre = all(mapa_jogador[linha][coluna + c] == "~" for c in range(tamanho))
                if livre:
                    for c in range(tamanho):
                        mapa_jogador[linha][coluna + c] = "O"
                        barcos_jogador.append((linha, coluna + c))
                    break
                else:
                    print(VERMELHO + "Já existe um navio ocupando esse espaço!" + RESET)
            else:
                print(VERMELHO + f"Posição inválida! A coluna deve ir até {TAMANHO-tamanho} para caber o barco." + RESET)
        except ValueError:
            print(VERMELHO + "Digite apenas números inteiros válidos." + RESET)

# --- POSICIONAMENTO DOS BARCOS DO COMPUTADOR ---
barcos_computador = []
for tamanho in tamanhos_frota:
    while True:
        l_pc = random.randint(0, TAMANHO - 1)
        c_pc = random.randint(0, TAMANHO - tamanho)
        
        # Garante que não haja sobreposição
        espaco_livre = all((l_pc, c_pc + c) not in barcos_computador for c in range(tamanho))
        if espaco_livre:
            for c in range(tamanho):
                barcos_computador.append((l_pc, c_pc + c))
            break

total_partes = len(barcos_jogador) # Total de blocos para destruir
acertos_no_computador = 0
acertos_no_jogador = 0
vidas_jogador = VIDAS_INICIAIS
vidas_computador = VIDAS_INICIAIS
radares_disponiveis = 3

print("\n" + VERDE + "="*45 + RESET)
print(VERDE + NEGRITO + "  FROTA PRONTA! QUE A GUERRA COMEÇE NO MAR!  " + RESET)
print(VERDE + "="*45 + RESET)
time.sleep(1)

# --- LOOP PRINCIPAL DO JOGO ---
while True:
    # Painel de Status
    print("\n" + "—"*45)
    cor_v_j = VERDE if vidas_jogador > 1 else VERMELHO
    cor_v_c = VERDE if vidas_computador > 1 else VERMELHO
    print(f"❤️ Suas Vidas: {cor_v_j}{'♥ ' * vidas_jogador}{RESET} | 📡 Radares: {AZUL_CLARO}{radares_disponiveis}{RESET}")
    print(f"🤖 Vidas do PC: {cor_v_c}{'♥ ' * vidas_computador}{RESET}")
    print("—"*45)

    # Eventos Aleatórios (Desafios do Mar)
    evento_atual = random.choice(["normal", "normal", "normal", "tempestade", "nevoa"])
    if evento_atual == "tempestade":
        print(AMARELO + "⚡ ALERTA DE TEMPESTADE! Um raio revelou aleatoriamente uma coordenada inimiga!" + RESET)
        bloco_secreto = random.choice(barcos_computador)
        print(CINZA + f"   (Dica da tempestade: Há partes do inimigo na linha perto de {bloco_secreto[0]}...)" + RESET)
    elif evento_atual == "nevoa":
        print(CINZA + "🌫️ Uma névoa espessa cobre o oceano! Os radares ficam imprecisos neste turno." + RESET)

    print(f"\n{AMARELO}--- SEU MAPA DE ATAQUE (Inimigo) ---{RESET}")
    imprimir_tabuleiro(mapa_computador, mostrar_navios=False)
    
    print(f"\n{NEGRITO}Sua vez!{RESET} Digite as coordenadas, {ROXO}R{RESET} para usar o Radar, ou {ROXO}99{RESET} para Trapaças:")
    entrada_usuario = input("Comando ou Linha: ").strip().upper()

    # Sistema de Radar
    if entrada_usuario == "R":
        if radares_disponiveis > 0:
            radares_disponiveis -= 1
            print(AZUL_CLARO + "\n📡 [Radar Ativado] Escolha uma área 2x2 para escanear:" + RESET)
            try:
                rx = int(input("Linha inicial do radar (0-6): "))
                ry = int(input("Coluna inicial do radar (0-6): "))
                encontrou_algo = False
                for dr in range(2):
                    for dc in range(2):
                        if (rx + dr, ry + dc) in barcos_computador:
                            encontrou_algo = True
                if encontrou_algo:
                    print(VERDE + "📡 O Radar detectou assinaturas de navios inimigos nessa região!" + RESET)
                else:
                    print(CINZA + "📡 O Radar não detectou nada por lá. Setor limpo." + RESET)
            except ValueError:
                print(VERMELHO + "Coordenadas inválidas para o radar. Turno perdido!" + RESET)
        else:
            print(VERMELHO + "Você não tem mais radares disponíveis!" + RESET)
        input("Pressione Enter para continuar...")
        continue

    # Sistema de Trapaças (Cheats)
    if entrada_usuario == "99":
        print(ROXO + "\n╔════════════════ MENU DE TRAPAÇAS ════════════════╗" + RESET)
        print(ROXO + "║ [1] Revelar o mapa completo do Computador       ║" + RESET)
        print(ROXO + "║ [2] Ganhar +3 Vidas Extras                      ║" + RESET)
        print(ROXO + "║ [3] Ataque de Míssil Teleguiado (Destriui Bloco)║" + RESET)
        print(ROXO + "║ [4] Voltar ao Jogo                              ║" + RESET)
        print(ROXO + "╚═════════════════════════════════════════════════╝" + RESET)
        
        escolha_cheat = input("Escolha a trapaça: ")
        if escolha_cheat == "1":
            print(AMARELO + f"👀 POSIÇÕES DOS BARCOS DO PC: {barcos_computador}" + RESET)
            input("Pressione Enter...")
            continue
        elif escolha_cheat == "2":
            vidas_jogador += 3
            print(VERDE + "✨ Trapaça ativada! +3 Vidas ganhas." + RESET)
            continue
        elif escolha_cheat == "3":
            alvo_cheat = next((b for b in barcos_computador if mapa_computador[b[0]][b[1]] != "X"), None)
            if alvo_cheat:
                mapa_computador[alvo_cheat[0]][alvo_cheat[1]] = "X"
                acertos_no_computador += 1
                print(VERDE + f"🚀 Míssil teleguiado destruiu o bloco {alvo_cheat} do inimigo!" + RESET)
                if acertos_no_computador == total_partes:
                    print(VERDE + NEGRITO + "\n🏆 VOCÊ VENCEU USANDO TRAPAÇAS! 🏆" + RESET)
                    break
            else:
                print("Todos os barcos já foram destruídos!")
            continue
        else:
            continue

    try:
        tiro_l = int(entrada_usuario)
        tiro_c = int(input("Escolha a coluna: "))
    except ValueError:
        print(VERMELHO + "Digite números válidos!" + RESET)
        continue

    if not (0 <= tiro_l < TAMANHO and 0 <= tiro_c < TAMANHO):
        print(VERMELHO + "Coordenadas fora do tabuleiro!" + RESET)
        continue
    
    if mapa_computador[tiro_l][tiro_c] in ["X", "x"]:
        print(VERMELHO + "Você já atacou essa coordenada! Perdeu a vez." + RESET)
        continue

    # Processando o ataque do Jogador
    if evento_atual == "nevoa" and random.random() < 0.3:
        print(CINZA + "💨 A névoa atrapalhou seu tiro e fez ele desviar para a água!" + RESET)
        mapa_computador[tiro_l][tiro_c] = "x"
    elif (tiro_l, tiro_c) in barcos_computador:
        print(VERDE + NEGRITO + "\n🔥 EM CHEIO! Você acertou um navio inimigo! 🔥" + RESET)
        mapa_computador[tiro_l][tiro_c] = "X"
        acertos_no_computador += 1
        if vidas_computador > 0:
            vidas_computador -= 1

        if acertos_no_computador == total_partes or vidas_computador <= 0:
            print(VERDE + NEGRITO + "\n" + "!"*45 + RESET)
            print(VERDE + NEGRITO + " 🏆 GLÓRIA! Você destruiu toda a frota inimiga e VENCEU! 🏆" + RESET)
            print(VERDE + NEGRITO + "!"*45 + RESET)
            break
    else:
        print(AMARELO + "\n🌊 Água! Tiro perdido no oceano. 🌊" + RESET)
        mapa_computador[tiro_l][tiro_c] = "x"

    # Turno do Computador
    print(f"\n{VERMELHO}--- VEZ DO COMPUTADOR ATACAR ---{RESET}")
    time.sleep(0.8)
    
    while True:
        tiro_pc_l = random.randint(0, TAMANHO - 1)
        tiro_pc_c = random.randint(0, TAMANHO - 1)
        if mapa_jogador[tiro_pc_l][tiro_pc_c] not in ["X", "x"]:
            break

    if (tiro_pc_l, tiro_pc_c) in barcos_jogador:
        print(VERMELHO + f"⚠️ O computador disparou em ({tiro_pc_l}, {tiro_pc_c}) e ACERTOU seu navio! ⚠️" + RESET)
        mapa_jogador[tiro_pc_l][tiro_pc_c] = "X"
        acertos_no_jogador += 1
        vidas_jogador -= 1
        
        if acertos_no_jogador == total_partes or vidas_jogador <= 0:
            print(VERMELHO + NEGRITO + "\n" + "!"*45 + RESET)
            print(VERMELHO + NEGRITO + " 💀 Sua frota afundou completamente! VOCÊ PERDEU. 💀" + RESET)
            print(VERMELHO + NEGRITO + "!"*45 + RESET)
            break
    else:
        print(AZUL + f"💨 O computador errou o tiro na coordenada ({tiro_pc_l}, {tiro_pc_c})." + RESET)
        mapa_jogador[tiro_pc_l][tiro_pc_c] = "x"

    print(f"\n{AMARELO}--- SEU MAPA ATUALIZADO ---{RESET}")
    imprimir_tabuleiro(mapa_jogador, mostrar_navios=True)