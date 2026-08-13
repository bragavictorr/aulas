import pygame
import random
import sys

pygame.init()

# Configurações da tela
LARGURA, ALTURA = 400, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Bird")

# Cores
AZUL_CEU = (135, 206, 235)
VERDE = (34, 139, 34)
AMARELO = (255, 215, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Relógio
clock = pygame.time.Clock()
FPS = 60

# Fonte
fonte = pygame.font.SysFont("Arial", 32)
fonte_pequena = pygame.font.SysFont("Arial", 20)

# Física
GRAVIDADE = 0.5
FORCA_PULO = -8


class Passaro:
    def __init__(self):
        self.x = 80
        self.y = ALTURA // 2
        self.raio = 15
        self.velocidade = 0

    def pular(self):
        self.velocidade = FORCA_PULO

    def atualizar(self):
        self.velocidade += GRAVIDADE
        self.y += self.velocidade

    def desenhar(self):
        pygame.draw.circle(tela, AMARELO, (self.x, int(self.y)), self.raio)
        pygame.draw.circle(tela, PRETO, (self.x, int(self.y)), self.raio, 2)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.raio, self.y - self.raio, self.raio * 2, self.raio * 2
        )


class Cano:
    LARGURA = 60
    GAP = 150

    def __init__(self, x):
        self.x = x
        self.altura_topo = random.randint(50, ALTURA - self.GAP - 50)
        self.passou = False

    def atualizar(self, velocidade):
        self.x -= velocidade

    def desenhar(self):
        pygame.draw.rect(tela, VERDE, (self.x, 0, self.LARGURA, self.altura_topo))
        pygame.draw.rect(
            tela, VERDE, (self.x, self.altura_topo + self.GAP, self.LARGURA, ALTURA)
        )

    def colidiu(self, passaro):
        rect_passaro = passaro.get_rect()
        rect_topo = pygame.Rect(self.x, 0, self.LARGURA, self.altura_topo)
        rect_base = pygame.Rect(
            self.x, self.altura_topo + self.GAP, self.LARGURA, ALTURA
        )
        return rect_passaro.colliderect(rect_topo) or rect_passaro.colliderect(rect_base)

    def fora_da_tela(self):
        return self.x + self.LARGURA < 0


def tela_inicial():
    tela.fill(AZUL_CEU)
    titulo = fonte.render("Flappy Bird", True, PRETO)
    instrucao = fonte_pequena.render("Pressione ESPAÇO para começar", True, PRETO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 - 60))
    tela.blit(instrucao, (LARGURA // 2 - instrucao.get_width() // 2, ALTURA // 2))
    pygame.display.update()


def tela_fim(pontuacao, recorde):
    tela.fill(AZUL_CEU)
    fim = fonte.render("Fim de Jogo", True, PRETO)
    pont = fonte_pequena.render(f"Pontuação: {pontuacao}", True, PRETO)
    rec = fonte_pequena.render(f"Recorde: {recorde}", True, PRETO)
    reiniciar = fonte_pequena.render("Pressione ESPAÇO para reiniciar", True, PRETO)
    tela.blit(fim, (LARGURA // 2 - fim.get_width() // 2, ALTURA // 2 - 80))
    tela.blit(pont, (LARGURA // 2 - pont.get_width() // 2, ALTURA // 2 - 30))
    tela.blit(rec, (LARGURA // 2 - rec.get_width() // 2, ALTURA // 2))
    tela.blit(
        reiniciar, (LARGURA // 2 - reiniciar.get_width() // 2, ALTURA // 2 + 40)
    )
    pygame.display.update()


def main():
    recorde = 0
    rodando = True

    while rodando:
        # --- Tela inicial ---
        esperando = True
        while esperando:
            tela_inicial()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    esperando = False
            clock.tick(FPS)

        # --- Início do jogo ---
        passaro = Passaro()
        canos = [Cano(LARGURA + 100)]
        velocidade_canos = 3
        pontuacao = 0
        jogo_ativo = True

        while jogo_ativo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    passaro.pular()

            passaro.atualizar()

            # Gerar novos canos
            if canos[-1].x < LARGURA - 200:
                canos.append(Cano(LARGURA + 20))

            for cano in canos:
                cano.atualizar(velocidade_canos)
                if cano.colidiu(passaro):
                    jogo_ativo = False
                if not cano.passou and cano.x + Cano.LARGURA < passaro.x:
                    cano.passou = True
                    pontuacao += 1

            canos = [c for c in canos if not c.fora_da_tela()]

            if passaro.y - passaro.raio <= 0 or passaro.y + passaro.raio >= ALTURA:
                jogo_ativo = False

            # --- Desenho ---
            tela.fill(AZUL_CEU)
            for cano in canos:
                cano.desenhar()
            passaro.desenhar()

            texto_pontos = fonte.render(str(pontuacao), True, BRANCO)
            tela.blit(
                texto_pontos, (LARGURA // 2 - texto_pontos.get_width() // 2, 30)
            )

            pygame.display.update()
            clock.tick(FPS)

        recorde = max(recorde, pontuacao)

        # --- Tela final ---
        esperando_reinicio = True
        while esperando_reinicio:
            tela_fim(pontuacao, recorde)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    esperando_reinicio = False
            clock.tick(FPS)


if __name__ == "__main__":
    main()