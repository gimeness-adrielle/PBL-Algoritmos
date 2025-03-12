import numpy as np
import random
import time
import curses

# Autor: Adrielle Gimenes
# Componente Curricular: MI Algoritmos
# Concluído em: 26/10/2024
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.

# Função principal do jogo
def main (stdscr):
    global tabuleiro, linhas, colunas, pos_y, pos_x, pontuaçao, score, display_peça, prox_peça, peça
    curses.curs_set(0)
    tela_inicial (stdscr)
    stdscr.nodelay(1)
    stdscr.timeout(10)
    pontuaçao = 0

    # Criação do tabuleiro
    tabuleiro = np.zeros((20,10))

    # Display Score
    score = curses.newwin(5, 15, 1, 22)
    display_score()

    # Display da próxima peça
    display_peça = curses.newwin(6, 10, 6, 24) 
    display_peça.box()

    # Definição de cores para cada peça
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)

    # Coloca a primeira peça
    prox_peça = np.rot90 (random.choice(peças),random.randint(0,3))
    gerar_peça ()
    tempo_inicial = time.time()
    delay = 0.5

    # Loop do jogo para descer as peças
    while (1):  
        tempo_atual = time.time()
        if tempo_atual - tempo_inicial >= delay:
            limpar_desenhar_peça (0) # Limpa a peça para mover
            if colisao(linhas, colunas, pos_y + 1, pos_x):
                pos_y += 1
                limpar_desenhar_peça (peça) # Desenha a peça
            else:
                limpar_desenhar_peça (peça)
                if peça[0,0] == 8: # Se for a peça bomba
                    bomba(tabuleiro, pos_y, pos_x)
                limpar_linhas ()
                gerar_peça ()
                if not colisao(linhas, colunas, pos_y, pos_x):
                    game_over (stdscr)
                    break
            tempo_inicial = tempo_atual

        # Captura de teclas
        tecla = stdscr.getch ()
        if tecla != -1:
            limpar_desenhar_peça (0)
            # Mover para esquerda
            if tecla == curses.KEY_LEFT and colisao (linhas, colunas, pos_y, pos_x - 1):
                pos_x -= 1

            # Mover para direita
            elif tecla == curses.KEY_RIGHT and colisao (linhas, colunas, pos_y, pos_x + 1):
                pos_x += 1

            # Mover para baixo
            elif tecla == curses.KEY_DOWN and colisao (linhas, colunas, pos_y + 1, pos_x):
                pos_y += 1

            # Rotacionar peça
            elif tecla == curses.KEY_UP:
                peça_rot = np.rot90(peça) # Cria uma nova peça rotacionada
                linhas_rot, colunas_rot = peça_rot.shape
                if colisao(linhas_rot, colunas_rot, pos_y, pos_x): # Verifica se a peça rotacionada cabe no tabuleiro
                    peça = peça_rot
                    linhas, colunas = linhas_rot, colunas_rot
            limpar_desenhar_peça (peça)

        print_tabuleiro (stdscr)
        display_score()
        proxima_peça (prox_peça)

# Definir situações de colisão com tabuleiro e com peças
def colisao(linhas, colunas, pos_y, pos_x):
    if pos_y < 0 or pos_x < 0 or pos_y + linhas > tabuleiro.shape[0] or pos_x + colunas > tabuleiro.shape[1]:
        return False
    # Colisão com outras peças
    limite = tabuleiro[pos_y:pos_y + linhas, pos_x:pos_x + colunas]
    if peça.shape == limite.shape:
        if np.any(np.logical_and(peça != 0, limite != 0)):
            return False
        else:
            return True
    return True

# Função de colocar uma nova peça ao tabuleiro
def gerar_peça():
    global prox_peça, linhas, colunas, pos_y, pos_x, peça
    peça = prox_peça
    linhas, colunas = peça.shape
    pos_y, pos_x = 0, random.randint(0, tabuleiro.shape[1] - colunas)
    # Armazenar a próxima peça para display
    prox_peça = np.rot90(random.choice(peças), random.randint(0, 3))

# Função para limpar as peças ou desenhar e fixar a peça, dependendo do parâmetro
def limpar_desenhar_peça (valor):
    tabuleiro[pos_y:pos_y + linhas, pos_x:pos_x + colunas] = np.where(peça != 0, valor, tabuleiro[pos_y:pos_y + linhas, pos_x:pos_x + colunas])

# Função para limpar as linhas completas e adicionar pontuação
def limpar_linhas():
    global tabuleiro, pontuaçao
    linhas_removidas = 0  # Contador
    linhas_tab = tabuleiro.shape[0] - 1
    while linhas_tab >= 0: # Percorre as linhas do tabuleiro de baixo para cima
        if np.all(tabuleiro[linhas_tab, :] != 0):
            tabuleiro = np.delete(tabuleiro, linhas_tab, axis=0) # Deleta uma linha totalmente preenchida
            tabuleiro = np.vstack((np.zeros((1,10)), tabuleiro)) # Adiciona uma nova linha ao topo do tabuleiro
            linhas_removidas += 1
        else: # Caso a linha atual não esteja totalmente preenchida, verifica a proxima
            linhas_tab -= 1
    # Adicionar pontuação
    if linhas_removidas > 0:
        base_pontuacao = 100
        bonus = 1 if linhas_removidas == 1 else 2 if linhas_removidas <= 4 else 3
        pontuaçao += base_pontuacao * linhas_removidas * bonus

# Função para a peça bomba
def bomba (tabuleiro, pos_y, pos_x): 
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= pos_y + i < tabuleiro.shape[0] and 0 <= pos_x + j < tabuleiro.shape[1]:
                tabuleiro[pos_y + i, pos_x + j] = 0

# Função de imprimir o tabuleiro e as peças de acordo com sua devida cor
def print_tabuleiro(stdscr):
    stdscr.clear()
    # Definir os limites
    lin, col = tabuleiro.shape[0], tabuleiro.shape[1]
    for y in range(lin): # Percorre as linhas do tabuleiro
        for x in range(col): # Percorre as colunas do tabuleiro
            elemento = tabuleiro[y, x] # Percorre cada coordenada do tabuleiro, para desenhar em cada uma
            # Definir o símbolo e a cor com base no elemento
            if elemento == 0: celula, cor = '▢', curses.A_NORMAL
            elif elemento == 8: celula, cor = '💣', curses.A_NORMAL
            else: celula, cor = '■', curses.color_pair(int(elemento))
            # Desenhar a peça (*2 é apenas para ter um espaçamento entre as células)
            stdscr.addstr(y, x * 2, celula, cor)
    stdscr.refresh()

# Display score
def display_score():
    global score, pontuaçao
    score.clear()
    score.attrset(curses.color_pair(6))
    score.box()
    score.attrset(curses.color_pair(0))
    score.addstr(1, 5, "SCORE", curses.A_BOLD)
    score.addstr(2, 6, str(pontuaçao))
    score.refresh()

# Display próxima peça
def proxima_peça(prox_peça):
    display_peça.clear()
    display_peça.attrset(curses.color_pair(6))
    display_peça.box()
    display_peça.attrset(curses.color_pair(0))

    lin, col = prox_peça.shape[0], prox_peça.shape[1]
    for y in range(lin):
        for x in range(col):
            elemento = prox_peça[y, x]
            if elemento == 0: continue
            elif elemento == 8: celula, cor = '💣', curses.A_NORMAL
            else: celula, cor = '■', curses.color_pair(int(elemento))
            display_peça.addstr(y + 1, x + 4, celula, cor)
    display_peça.refresh()

# Display da tela inicial
def tela_inicial (stdscr):
    stdscr.addstr (10,20,"████████╗ ███████╗ ████████╗ ██████╗  ██╗  ██████╗")
    stdscr.addstr (11,20,"╚══██╔══╝ ██╔════╝ ╚══██╔══╝ ██╔══██╗ ██║ ██╔════╝")
    stdscr.addstr (12,20,"   ██║    █████╗      ██║    ██████╔╝ ██║ ╚█████╗ ")
    stdscr.addstr (13,20,"   ██║    ██╔══╝      ██║    ██╔══██╗ ██║  ╚═══██╗")
    stdscr.addstr (14,20,"   ██║    ███████╗    ██║    ██║  ██║ ██║ ██████╔╝")
    stdscr.addstr (15,20,"   ╚═╝    ╚══════╝    ╚═╝    ╚═╝  ╚═╝ ╚═╝ ╚═════╝ ")
    stdscr.refresh ()
    time.sleep (3)
    stdscr.addstr (17,38,"PRESS 'ANY KEY'")
    stdscr.refresh ()
    stdscr.getch ()
    stdscr.clear()

# Mostrar GAME OVER
def game_over (stdscr):
    stdscr.clear ()
    stdscr.addstr (12,20,"█▀▀ ▄▀█ █▀▄▀█ █▀▀   █▀█ █░█ █▀▀ █▀█ ", curses.color_pair(7))
    stdscr.addstr (13,20,"█▄█ █▀█ █░▀░█ ██▄   █▄█ ▀▄▀ ██▄ █▀▄ ", curses.color_pair(7))
    stdscr.refresh ()
    time.sleep (3)
    
# Definindo cada peça
peças = [np.array([[1, 1, 1, 1]]), np.array([[2, 2], [2, 2]]),  np.array([[3, 3, 3], [0, 3, 0]]), 
         np.array([[0, 4, 4], [4, 4, 0]]), np.array([[5, 5, 0], [0, 5, 5]]), np.array([[6, 0, 0], [6, 6, 6]]),
        np.array([[0, 0, 7], [7, 7, 7]]), np.array([[8]])]

stdscr = curses.initscr()
curses.wrapper(main)