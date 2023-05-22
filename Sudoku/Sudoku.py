import numpy as np
import pygame
import time
from random import sample
pygame.font.init()

### Generate Random Puzzle ###
size = 3
grid = size*size
rSize = range(size)

def pattern(r,c):
    return (size*(r%size) + r // size + c)%grid

def randomize(s):
    return sample(s, len(s))

puzzle_rows = [g*size + r for g in randomize(rSize) for r in randomize(rSize)]
puzzle_cols = [g*size + c for g in randomize(rSize) for c in randomize(rSize)]
nums = randomize(range(1, grid+1))

board = np.full(shape=(9,9), fill_value=[[nums[pattern(r,c)] for r in puzzle_rows] for c in puzzle_cols])
board1 = np.full(shape=(9,9), fill_value=[[nums[pattern(r,c)] for r in puzzle_rows] for c in puzzle_cols])

print(board)
print(board1)

### Variables ###
x = 0
y = 0
width = 630
height = 630
tile = height // 9
fnt = pygame.font.SysFont("alice", 40)
fnt1 = pygame.font.SysFont("alice", 30)
window = pygame.display.set_mode((width, height))

### Play ###
def cord(pos):
    global x
    global y
    if pos[0] < width and pos[1] < height:
        x = pos[0] // tile
        y = pos[1] // tile
        #print(x)
        #print(y)
        print(board[y][x])

### Draw ###
def draw_grid():
    for i in range(10):
        if i%3 == 0 and i != 0:
            thick = 4
        else:
            thick = 1

        pygame.draw.line(window, (0,0,0), (0, i*tile), (width, i*tile), thick)
        pygame.draw.line(window, (0,0,0), (i*tile, 0), (i*tile, height), thick)

def draw_puzzle():
    for i in range(9):
        for j in range(9):
            if board[j][i] != 0:
                #pygame.draw.rect(window, (255,255,255), (i,j,tile,tile))
                pygame.draw.rect(window, (255,255,255), (i*tile, j*tile, tile+1, tile+1))

                txt = fnt.render(str(board[j][i]), 1, (0,0,0))
                window.blit(txt, (i*tile+15, j*tile+15))

def draw_cell():
    for i in range(2):
        #if selected == True:
        pygame.draw.line(window, (255, 0, 0), (x * tile-3, (y + i)*tile), (x * tile + tile + 3, (y + i)*tile), 3)
        pygame.draw.line(window, (255, 0, 0), ( (x + i)* tile, y * tile ), ((x + i) * tile, y * tile + tile), 3)

def draw_val(val):
    if board1[y][x] == val:
        txt = fnt1.render(str(val), 1, (0,0,0))
        window.blit(txt, (x*tile + 15, y*tile + 15))
    else:
        print("Incorrect")

### Solve using backtracking ###
def valid(i, j, val):
    for k in range(9):
        if board[i][k] == val and j != k:
            return False

    for k in range(9):
        if board[k][j] == val and i != k:
            return False

    tx = j // 3
    ty = i // 3

    for k in range(ty*3, ty*3 + 3):
        for l in range(tx*3, tx*3 + 3):
            if board[k][l] == val and (k,l) != (i,j):
                return False

    return True

def solve(i, j):
    while board[i][j] != 0:
        if i < 8:
            i+=1
        elif i == 8 and j < 8:
            i=0
            j+=1
        elif i == 8 and j == 8:
            return True

    pygame.event.pump()

    for k in range(1, 10):
        if valid(i,j,k):
            board[i][j] = k
            window.fill((255,255,255))
            draw_puzzle()
            draw_grid()
            draw_cell()
            pygame.display.update()
            pygame.time.delay(10)

            if solve(i,j) == 1:
                return True
            else:
                board[i][j] = 0

            window.fill((255,255,255))
            draw_puzzle()
            draw_grid()
            draw_cell()
            pygame.display.update()
            pygame.time.delay(10)

    return False

def main():
    print("Press 'Delete' to clear board or 'Space' to solve board'")
    print("Click desired tile, enter value and press 'Enter' to play")
    print("Please enter level\n1. Beginner 2. Intermediate 3. Advanced:")
    level = input()

    if level == str(1):
        filled = grid*grid
        #41 numbers given
        empty = filled*3 // 6
        for p in sample(range(filled), empty):
            board[p//grid][p%grid] = 0
    elif level == str(2):
        filled = grid*grid
        #33 numbers given
        empty = filled*3 // 5
        for p in sample(range(filled), empty):
            board[p//grid][p%grid] = 0
    elif level == str(3):
        filled = grid*grid
        #21 numbers given
        empty = filled*3 // 4
        for p in sample(range(filled), empty):
            board[p//grid][p%grid] = 0
    else:
        print("Invalid choice")

    #print(board)
    print(board1)

    pygame.display.set_caption("Sudoku")
    window = pygame.display.set_mode((width, height + 50))
    window.fill((255,255,255))
    draw_puzzle()
    draw_grid()
    key = 0
    flag1 = 0
    run = True 
    
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:                
                pos = pygame.mouse.get_pos()
                cord(pos)
                draw_cell()
                draw_grid()

            if event.type == pygame.KEYDOWN:                
                                
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_9 or event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9

                #print(key)
                
                if event.key == pygame.K_SPACE:
                    solve(0,0)

        if key != 0:
            draw_val(key)
            key = 0

        draw_puzzle()
        draw_grid()

        pygame.display.update()

main()
pygame.quit()
