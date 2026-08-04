import random
import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA_TELA = 720
ALTURA_TELA = 400
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Batalha Naval - Deluxe")

# Cores (Paleta moderna)
BRANCO = (255, 255, 255)
PRETO = (30, 30, 30)
AZUL_AGUA = (52, 152, 219)
AZUL_ESCURO = (41, 128, 185)
AZUL_FUNDO = (240, 244, 248)
VERDE_NAVIO = (39, 174, 96)
VERDE_CLARO = (46, 204, 113)
VERMELHO_EXPLOSAO = (231, 76, 60)
LARANJA = (243, 156, 18)
CINZA_X = (149, 165, 153)
AMARELO_SELECAO = (241, 196, 15)
CINZA_BOTAO = (189, 195, 199)

# Fontes
FONTE_UI = pygame.font.SysFont("Segoe UI", 20, bold=True)
FONTE_MSG = pygame.font.SysFont("Segoe UI", 16, bold=True)
FONTE_CELULA = pygame.font.SysFont("Segoe UI", 28, bold=True)

# Configurações do Grid
TAMANHO_CELULA = 80
MARGEM = 8
TAMANHO_TOTAL_GRID = (3 * TAMANHO_CELULA) + (2 * MARGEM)

# Posição dos tabuleiros
Y_GRIDS = (ALTURA_TELA - TAMANHO_TOTAL_GRID) // 2 - 20
X_JOGADOR = 60
X_COMPUTADOR = LARGURA_TELA - X_JOGADOR - TAMANHO_TOTAL_GRID

# Configuração do Botão
btn_rect = pygame.Rect(LARGURA_TELA // 2 - 60, ALTURA_TELA - 65, 120, 35)

# --- VARIÁVEIS GLOBAIS DO JOGO ---
estado_jogo = ""
mensagem = ""
turno = ""
mapa_jogador = []
mapa_computador = []
LINHA_INICIAL_JOGADOR = COLUNA_INICIAL_JOGADOR = None
LINHA_INICIAL_COMPUTADOR = COLUNA_INICIAL_COMPUTADOR = None

def inicializar_jogo():
    global estado_jogo, mensagem, turno, mapa_jogador, mapa_computador, \
           LINHA_INICIAL_JOGADOR, COLUNA_INICIAL_JOGADOR, LINHA_INICIAL_COMPUTADOR, COLUNA_INICIAL_COMPUTADOR
    
    mapa_jogador = [["~" for _ in range(3)] for _ in range(3)]
    mapa_computador = [["~" for _ in range(3)] for _ in range(3)]

    LINHA_INICIAL_JOGADOR = COLUNA_INICIAL_JOGADOR = None
    
    # Computador escolhe posição secreta
    LINHA_INICIAL_COMPUTADOR = random.randint(0, 2)
    COLUNA_INICIAL_COMPUTADOR = random.randint(0, 2)

    estado_jogo = "COLOCAR_BARCO"
    mensagem = "Clique no seu tabuleiro para posicionar o navio."
    turno = "jogador"

# Inicializa o jogo pela primeira vez
inicializar_jogo()

def desenhar_celula_personalizada(surface, x, y, tipo, eh_jogador):
    # Desenha o fundo da célula (Água com efeito visual)
    rect = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
    pygame.draw.rect(surface, AZUL_AGUA, rect, border_radius=6)
    pygame.draw.rect(surface, AZUL_ESCURO, rect, 2, border_radius=6)
    
    # Detalhe de ondas sutis na água
    pygame.draw.arc(surface, AZUL_ESCURO, (x + 15, y + 20, 50, 20), 0, 3.14, 2)

    if tipo == "o":  # Navio
        if eh_jogador:
            # Desenha um navio estilizado verde
            navio_rect = pygame.Rect(x + 15, y + 25, 50, 30)
            pygame.draw.rect(surface, VERDE_NAVIO, navio_rect, border_radius=8)
            # Cabine do navio
            cabine_rect = pygame.Rect(x + 30, y + 12, 20, 15)
            pygame.draw.rect(surface, VERDE_CLARO, cabine_rect, border_radius=4)
        else:
            # Navio inimigo destruído (Explosão)
            pygame.draw.circle(surface, LARANJA, (x + 40, y + 40), 25)
            pygame.draw.circle(surface, VERMELHO_EXPLOSAO, (x + 40, y + 40), 15)

    elif tipo == "x":  # Tiro na água / Erro
        if eh_jogador:
            # Tiro certeiro do PC no seu navio (Explosão no seu navio)
            navio_rect = pygame.Rect(x + 15, y + 25, 50, 30)
            pygame.draw.rect(surface, VERMELHO_EXPLOSAO, navio_rect, border_radius=8)
            pygame.draw.circle(surface, LARANJA, (x + 40, y + 40), 12)
        else:
            # Erro do jogador (Um 'X' elegante)
            pygame.draw.line(surface, CINZA_X, (x + 25, y + 25), (x + 55, y + 55), 5)
            pygame.draw.line(surface, CINZA_X, (x + 55, y + 25), (x + 25, y + 55), 5)

def desenhar_grid(x_inicial, y_inicial, matriz, titulo, eh_tabuleiro_jogador):
    # Título do Tabuleiro
    texto_titulo = FONTE_UI.render(titulo, True, PRETO)
    TELA.blit(texto_titulo, (x_inicial + (TAMANHO_TOTAL_GRID - texto_titulo.get_width())//2, y_inicial - 30))

    # Destaque de seleção (borda amarela no tabuleiro ativo)
    destaque = False
    if eh_tabuleiro_jogador and estado_jogo == "COLOCAR_BARCO":
        destaque = True
    elif not eh_tabuleiro_jogador and estado_jogo == "JOGO" and turno == "jogador":
        destaque = True

    if destaque:
        rect_destaque = pygame.Rect(x_inicial - 6, y_inicial - 6, TAMANHO_TOTAL_GRID + 12, TAMANHO_TOTAL_GRID + 12)
        pygame.draw.rect(TELA, AMARELO_SELECAO, rect_destaque, 4, border_radius=8)

    # Desenhar células
    for linha in range(3):
        for coluna in range(3):
            rx = x_inicial + coluna * (TAMANHO_CELULA + MARGEM)
            ry = y_inicial + linha * (TAMANHO_CELULA + MARGEM)
            
            conteudo = matriz[linha][coluna]

            if eh_tabuleiro_jogador:
                desenhar_celula_personalizada(TELA, rx, ry, conteudo, eh_jogador=True)
            else:
                # Tabuleiro do computador esconde o navio dele até ser descoberto
                if conteudo == "o":
                    desenhar_celula_personalizada(TELA, rx, ry, "o", eh_jogador=False)
                elif conteudo == "x":
                    desenhar_celula_personalizada(TELA, rx, ry, "x", eh_jogador=False)
                else:
                    desenhar_celula_personalizada(TELA, rx, ry, "~", eh_jogador=False)

def processar_clique(pos_x, pos_y):
    global estado_jogo, mensagem, turno, LINHA_INICIAL_JOGADOR, COLUNA_INICIAL_JOGADOR

    # Etapa 1: Jogador posiciona o barco
    if estado_jogo == "COLOCAR_BARCO":
        rect_jogador = pygame.Rect(X_JOGADOR, Y_GRIDS, TAMANHO_TOTAL_GRID, TAMANHO_TOTAL_GRID)
        if rect_jogador.collidepoint(pos_x, pos_y):
            coluna = (pos_x - X_JOGADOR) // (TAMANHO_CELULA + MARGEM)
            linha = (pos_y - Y_GRIDS) // (TAMANHO_CELULA + MARGEM)
            
            LINHA_INICIAL_JOGADOR = linha
            COLUNA_INICIAL_JOGADOR = coluna
            mapa_jogador[linha][coluna] = "o"
            
            estado_jogo = "JOGO"
            mensagem = "Navio posicionado! Sua vez de atacar o inimigo."
            turno = "jogador"

    # Etapa 2: Jogador ataca
    elif estado_jogo == "JOGO" and turno == "jogador":
        rect_computador = pygame.Rect(X_COMPUTADOR, Y_GRIDS, TAMANHO_TOTAL_GRID, TAMANHO_TOTAL_GRID)
        if rect_computador.collidepoint(pos_x, pos_y):
            coluna = (pos_x - X_COMPUTADOR) // (TAMANHO_CELULA + MARGEM)
            linha = (pos_y - Y_GRIDS) // (TAMANHO_CELULA + MARGEM)

            # Se for célula limpa, ataca
            if mapa_computador[linha][coluna] == "~":
                if linha == LINHA_INICIAL_COMPUTADOR and coluna == COLUNA_INICIAL_COMPUTADOR:
                    mapa_computador[linha][coluna] = "o"
                    mensagem = "BOOM! Você acertou o navio inimigo! VITÓRIA!"
                    estado_jogo = "FIM"
                else:
                    mapa_computador[linha][coluna] = "x"
                    mensagem = "Água! Você errou. Vez do computador..."
                    turno = "computador"

# --- LOOP PRINCIPAL ---
relogio = pygame.time.Clock()
rodando = True

while rodando:
    TELA.fill(AZUL_FUNDO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mx, my = evento.pos
            
            # Clique no botão de reiniciar
            if btn_rect.collidepoint(mx, my):
                inicializar_jogo()
            
            # Cliques no tabuleiro
            elif estado_jogo != "FIM":
                processar_clique(mx, my)

    # Lógica da IA do Computador
    if estado_jogo == "JOGO" and turno == "computador":
        pygame.display.flip() 
        pygame.time.delay(900) # Pausa dramática para parecer que o pc está "pensando"

        # Computador escolhe uma jogada válida aleatória
        while True:
            lr = random.randint(0, 2)
            cr = random.randint(0, 2)
            if mapa_jogador[lr][cr] != "x":
                break
        
        if lr == LINHA_INICIAL_JOGADOR and cr == COLUNA_INICIAL_JOGADOR:
            mapa_jogador[lr][cr] = "x"
            mensagem = "O computador destruiu seu navio! DERROTA."
            estado_jogo = "FIM"
        else:
            mapa_jogador[lr][cr] = "x"
            mensagem = "O computador errou! Sua vez de atacar."
            turno = "jogador"

    # Desenhar Elementos na Tela
    desenhar_grid(X_JOGADOR, Y_GRIDS, mapa_jogador, "SEU ESPAÇO", True)
    desenhar_grid(X_COMPUTADOR, Y_GRIDS, mapa_computador, "INIMIGO", False)

    # Caixa de Mensagem Centralizada
    texto_renderizado = FONTE_MSG.render(mensagem, True, PRETO)
    TELA.blit(texto_renderizado, (LARGURA_TELA // 2 - texto_renderizado.get_width() // 2, ALTURA_TELA - 35))

    # Botão Reiniciar Estilizado
    cor_botao = CINZA_BOTAO if not btn_rect.collidepoint(pygame.mouse.get_pos()) else (210, 215, 220)
    pygame.draw.rect(TELA, cor_botao, btn_rect, border_radius=6)
    pygame.draw.rect(TELA, PRETO, btn_rect, 2, border_radius=6)
    
    texto_btn = FONTE_UI.render("Reiniciar", True, PRETO)
    TELA.blit(texto_btn, (btn_rect.x + (120 - texto_btn.get_width()) // 2, btn_rect.y + 6))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
sys.exit()