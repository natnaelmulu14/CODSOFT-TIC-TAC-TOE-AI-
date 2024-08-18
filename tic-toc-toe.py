import pygame
import sys
import numpy as np
from game_setting import *


pygame.init()

screen = pygame.display.set_mode((screen_width, Screen_height))
pygame.display.set_caption("Tic Tac Toe AI")
screen_rect = screen.get_rect()
screen.fill(white)
game_board = np.zeros((3,3))
x = pygame.image.load('x.png')
o = pygame.image.load('o.png')

x = pygame.transform.scale(x, (int(Cell_size//2), int(Cell_size//2)))
o = pygame.transform.scale(o, (int(Cell_size//2), int(Cell_size//2)))


def game_grids(color=Black):
    for i in range(1, Dimension):
        pygame.draw.line(screen, color, (0,Cell_size*i), (screen_width, Cell_size*i), Line_width)
        pygame.draw.line(screen, color, (Cell_size*i,0), (Cell_size*i, Screen_height), Line_width)

def mark_cell(row_cell, col_cell, player):
    game_board[row_cell][col_cell] = player
    
def sketch_figures():
    for col in range(Dimension):
        for row in range(Dimension):
            if game_board[row][col] == 1:
                screen.blit(x, (0.25*Cell_size+Cell_size*col, 0.25*Cell_size+Cell_size*row))
            elif game_board[row][col] == 2:
                screen.blit(o, (0.25*Cell_size+Cell_size*col, 0.25*Cell_size+Cell_size*row))



def check_cell(row_cell, col_cell):
    if game_board[row_cell, col_cell] == 0:
        return True
    else:
        return False

def check_board(game_board=game_board):
    for row in range(Dimension):
        for col in range(Dimension):
            if game_board[row][col] == 0:
                return False
    return True

def check_winnner(player, game_board=game_board):
    for row in game_board:
        if row[0] == row[1] == row[2] == player:
            return True
    for col in game_board.T:
        if col[0]== col[1] == col[2] == player:
            return True
    if game_board[0][0]==player and game_board[1][1]==player and game_board[2][2]==player:
        return True
    if game_board[0][2]==player and game_board[1][1]==player and game_board[2][0]==player:
        return True
    return False



def best_choice():
    
    def minimax_algorithm(ideal_board, min_or_max):
        if check_winnner(2, ideal_board):
            return 10000
        elif check_winnner(1, ideal_board):
            return -10000
        elif check_board(ideal_board):
            return 0
        
        if min_or_max:
            high_score = -100
            for row in range(Dimension):
                for col in range(Dimension):
                    if ideal_board[row][col] == 0:
                        ideal_board[row][col] = 2
                        score = minimax_algorithm(ideal_board, False)
                        ideal_board[row][col] = 0
                        high_score = max(high_score, score)
            return high_score
        else:
            high_score = 100
            for row in range(Dimension):
                for col in range(Dimension):
                    if ideal_board[row][col] == 0:
                        ideal_board[row][col] = 1
                        score = minimax_algorithm(ideal_board, True)
                        ideal_board[row][col] = 0
                        high_score = min(high_score, score)
            return high_score
    
    
    high_score = -100
    choice = []
    for row in range(Dimension):
        for col in range(Dimension):
            if game_board[row][col] == 0:
                game_board[row][col] = 2
                score = minimax_algorithm(game_board, False)
                game_board[row][col] = 0
                if score > high_score:
                    high_score = score
                    choice = [row, col]
    if choice:
        mark_cell(choice[0], choice[1], 2)
        return True
    return False


def restart_game():
    screen.fill(white)
    game_grids(Black)
    for row in range(Dimension):
        for col in range(Dimension):
            game_board[row][col] = 0

def game_stat(text, color):
    font_size = 48
    font = pygame.font.Font(None, font_size)
    text_sur = font.render(text, True, color)
    text_rect = text_sur.get_rect()
    text_rect.center = (screen_width//2, Screen_height//2)
    screen.blit(text_sur, text_rect)

player = 1
game_grids(Black)
game_on = True


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and game_on:
            mouse_x = int(event.pos[0]/Cell_size)
            mouse_y = int(event.pos[1]/Cell_size)

            if check_cell(mouse_y, mouse_x):
                mark_cell(mouse_y, mouse_x, player)
                if check_winnner(player):
                    game_on = False
                player = 2 if player == 1 else 1

                if game_on:
                    if best_choice():
                        if check_winnner(2):
                            game_on = False
                        player = 2 if player == 1 else 1
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                restart_game()
                game_on = True
                player = 1
    
    sketch_figures()
    if not game_on:
        if check_winnner(1):
            game_stat("Win", Green)
        
        elif check_winnner(2):
            game_stat("Game over", Red)

        else:
            game_stat("Tie", yellow)


  
    pygame.display.update()