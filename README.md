# Minesweeper Game

## Introduction

This is a classic Minesweeper game implemented using Python and the Pygame library. The game provides a graphical interface where players can click on cells to reveal them and mark cells they suspect to contain mines. The goal of the game is to reveal all cells without mines and correctly mark all cells that contain mines.

## Features

- A grid-based Minesweeper game.
- Left-click to reveal cells.
- Right-click to mark cells as mines.
- A restart button that appears when the game is lost.
- Win and loss detection.

## Installation

To play the Minesweeper game, you need to have Python and Pygame installed on your system. 

### Install Python

If you don't have Python installed, you can download it from the official website: [Python.org](https://www.python.org/)

### Install Pygame

You can install Pygame using pip, the Python package installer. Open a terminal or command prompt and run the following command:

```bash
pip install pygame
How to Run
Clone or download the repository to your local machine.
Navigate to the directory containing the game script.
Run the script using Python:
bash
Copiar código
python minesweeper.py
How to Play
Objective: Reveal all cells that do not contain mines and mark all cells that contain mines.
Controls:
Left-click on a cell to reveal it.
Right-click on a cell to mark it as a mine.
Restart: If you hit a mine and lose the game, a "Restart" button will appear. Click the button to start a new game.
Code Overview
The game is created using the Pygame library, which handles the graphical interface and user interactions. Below is a brief overview of the main parts of the code:

Game Initialization
python
Copiar código
pygame.init()
largura_tela = 600
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Minesweeper')
Field Generation
python
Copiar código
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
Revealing Cells
python
Copiar código
def revelar_campo(campo, revelado, x, y):
    if revelado[x][y]:
        return
    revelado[x][y] = True
    if campo[x][y] == 0:
        for x2 in range(max(0, x - 1), min(numero_celulas, x + 2)):
            for y2 in range(max(0, y - 1), min(numero_celulas, y + 2)):
                if not revelado[x2][y2]:
                    revelar_campo(campo, revelado, x2, y2)
Drawing the Field
python
Copiar código
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
Resetting the Game
python
Copiar código
def reset_jogo():
    global campo, revelado, marcados, perdeu, ganhou
    campo = gerar_campo()
    revelado = [[False for _ in range(numero_celulas)] for _ in range(numero_celulas)]
    marcados = [[False for _ in range(numero_celulas)] for _ in range(numero_celulas)]
    perdeu = False
    ganhou = False
Contributing
If you would like to contribute to the project, feel free to fork the repository and submit pull requests. Any contributions, such as bug fixes, new features, or improvements, are welcome.
