import pygame
import random

pygame.init()
largura_tela = 600
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Campo Minado')

branco = (255, 255, 255)
preto = (0, 0, 0)
cinza_claro = (192, 192, 192)
cinza_escuro = (128, 128, 128)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
verde = (0, 255, 0)

tamanho_celula = 20
numero_celulas = largura_tela // tamanho_celula
numero_minas = 40

pygame.font.init()
fonte = pygame.font.SysFont('Arial', 20)

def gerar_campo():
    campo = [[0 for _ in range(numero_celulas)] for _ in range(numero_celulas)]
    minas = random.sample(range(numero_celulas * numero_celulas), numero_minas)
    for mina in minas:
        x, y = divmod(mina, numero_celulas)
        campo[x][y] = -1
    for x in range(numero_celulas):
        for y in range(numero_celulas):
            if campo[x][y] == -1:
                continue
            campo[x][y] = sum((campo[x2][y2] == -1)
                              for x2 in range(max(0, x - 1), min(numero_celulas, x + 2))
                              for y2 in range(max(0, y - 1), min(numero_celulas, y + 2)))
    return campo

def revelar_campo(campo, revelado, x, y):
    if revelado[x][y]:
        return
    revelado[x][y] = True
    if campo[x][y] == 0:
        for x2 in range(max(0, x - 1), min(numero_celulas, x + 2)):
            for y2 in range(max(0, y - 1), min(numero_celulas, y + 2)):
                if not revelado[x2][y2]:
                    revelar_campo(campo, revelado, x2, y2)

def desenhar_campo(campo, revelado, marcados):
    for x in range(numero_celulas):
        for y in range(numero_celulas):
            rect = pygame.Rect(x * tamanho_celula, y * tamanho_celula, tamanho_celula, tamanho_celula)
            if revelado[x][y]:
                pygame.draw.rect(tela, cinza_claro, rect)
                if campo[x][y] > 0:
                    text = fonte.render(str(campo[x][y]), True, preto)
                    tela.blit(text, rect.move(6, 3))
                elif campo[x][y] == -1:
                    pygame.draw.circle(tela, vermelho, rect.center, tamanho_celula // 3)
            else:
                pygame.draw.rect(tela, cinza_escuro, rect)
                if marcados[x][y]:
                    pygame.draw.line(tela, vermelho, rect.topleft, rect.bottomright, 2)
                    pygame.draw.line(tela, vermelho, rect.topright, rect.bottomleft, 2)
            pygame.draw.rect(tela, preto, rect, 1)

def desenhar_botao(texto, posicao):
    rect = pygame.Rect(posicao, (120, 50))
    pygame.draw.rect(tela, azul, rect)
    text = fonte.render(texto, True, branco)
    tela.blit(text, (rect.x + 10, rect.y + 10))
    return rect

def reset_jogo():
    global campo, revelado, marcados, perdeu, ganhou
    campo = gerar_campo()
    revelado = [[False for _ in range(numero_celulas)] for _ in range(numero_celulas)]
    marcados = [[False for _ in range(numero_celulas)] for _ in range(numero_celulas)]
    perdeu = False
    ganhou = False

campo = gerar_campo()
revelado = [[False for _ in range(numero_celulas)] for _ in range(numero_celulas)]
marcados = [[False for _ in range(numero_celulas)] for _ in range(numero_celulas)]
executando = True
perdeu = False
ganhou = False

while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and not perdeu and not ganhou:
            x, y = evento.pos
            x //= tamanho_celula
            y //= tamanho_celula
            if evento.button == 1:
                if not marcados[x][y]:
                    if campo[x][y] == -1:
                        perdeu = True
                    else:
                        revelar_campo(campo, revelado, x, y)
            elif evento.button == 3:
                marcados[x][y] = not marcados[x][y]
        elif evento.type == pygame.MOUSEBUTTONDOWN and perdeu:
            x, y = evento.pos
            if reiniciar_btn.collidepoint(evento.pos):
                reset_jogo()

    tela.fill(preto)
    desenhar_campo(campo, revelado, marcados)

    if perdeu:
        reiniciar_btn = desenhar_botao('Reiniciar', (largura_tela // 2 - 60, altura_tela - 60))
        texto = fonte.render('Você perdeu!', True, vermelho)
        tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, altura_tela // 2 - texto.get_height() // 2))

    pygame.display.flip()

    if not perdeu and all((revelado[x][y] or (marcados[x][y] and campo[x][y] == -1)) for x in range(numero_celulas) for y in range(numero_celulas)):
        ganhou = True

    if ganhou:
        texto = fonte.render('Você ganhou!', True, verde)
        tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, altura_tela // 2 - texto.get_height() // 2))

pygame.quit()
