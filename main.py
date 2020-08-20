#
# space to pause the game
# ctrl + s to store the actual situation of the cells in the files folder
# ctrl + l to load a file
#

import pygame
import numpy as np
import time
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import os


width, height = 1920,1080
screen = pygame.display.set_mode((width,height))

background = 30, 30, 30
screen.fill(background)

numberCellsX, numberCellsY = 200,110

dimCellX = width / numberCellsX
dimCellY = height / numberCellsY

carryOn = True
pauseMode = False

#If the pdfFiles directory for that webpage does not exit, then it is created
Path("saved_games").mkdir(parents=True, exist_ok=True)  

#To store all the states we use a matrix. Alive = 1 . Dead = 0

cellsState = np.zeros((numberCellsX,numberCellsY))
#To start with random cells placed:
#cellsState = np.random.choice([0,1], size=(numberCellsX,numberCellsY))
nextCellsState = np.copy(cellsState)

cellsState[21,21] = 1
cellsState[21,23] = 1
cellsState[22,22] = 1
cellsState[22,23] = 1
cellsState[20,23] = 1


def save_file():
    now = datetime.now()
    np.savetxt(now.strftime("saved_games/%d|%m|%Y_%H:%M:%S.txt"), cellsState, fmt='%d')

def load_file():   
    global nextCellsState
    pauseMode = True
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()    
    if file_path:      
        nextCellsState = np.loadtxt(file_path)
        pauseMode = False
                 
            
def n_neighbours(x,y):
    #         *     *     *
    #         *   cell    *
    #         *     *     *
    # The * are the cells that we check
    # The game map is a toroidal structure so we get the module
    
    return (
                    cellsState[(x - 1) % numberCellsX, (y - 1) % numberCellsY]
                    + cellsState[x % numberCellsX, (y - 1) % numberCellsY]
                    + cellsState[(x + 1) % numberCellsX, (y - 1) % numberCellsY]
                    + cellsState[(x - 1) % numberCellsX, y % numberCellsY]
                    + cellsState[(x + 1) % numberCellsX, y % numberCellsY]
                    + cellsState[(x - 1) % numberCellsX, (y + 1) % numberCellsY]
                    + cellsState[x % numberCellsX, (y + 1) % numberCellsY]
                    + cellsState[(x + 1) % numberCellsX, (y + 1) % numberCellsY]
                )   



while carryOn: 
    screen.fill(background)
    #time.sleep(0.08)

    nextCellsState = np.copy(cellsState)

    ev = pygame.event.get()

    for event in ev:
        
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
        
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                pauseMode = not pauseMode
            
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_file()
            
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                load_file()
        

        mouseClick = pygame.mouse.get_pressed() 
        
        posX, posY = pygame.mouse.get_pos()
        celX, celY = int(np.floor(posX / dimCellX)), int(np.floor(posY / dimCellY))

        if mouseClick[0] == 1:            
            nextCellsState[celX,celY] = 1

        if mouseClick[2] == 1:            
            nextCellsState[celX,celY] = 0    
    #Create grid
    for y in range(0, numberCellsY):
        for x in range(0, numberCellsX):

            if not pauseMode:
                n_neigh = n_neighbours(x,y)                

                #Rules:

                #1.-    Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                if cellsState[x, y]==0 and n_neigh == 3: nextCellsState[x, y]= 1

                #2.-    Any live cell with fewer than two live neighbours or more than three live neighbours dies

                elif cellsState[x, y]==1 and (n_neigh < 2 or  n_neigh >3): nextCellsState[x, y]= 0

                #3.-    Any live cell with two or three live neighbours lives on to the next generation.

                #elif cellsState[x, y]==1 and n_neigh >= 2: pass - We do nothing
                



            poly = [   #They are the vertices of the rectangle
                (int(x * dimCellX), int(y * dimCellY)),
                (int((x + 1) * dimCellX), int(y * dimCellY)),
                (int((x + 1) * dimCellX), int((y + 1) * dimCellY)),
                (int(x * dimCellX), int((y + 1) * dimCellY)),
            ]


            #Draw cell
            
            if nextCellsState[x,y]==0:                
                pygame.draw.polygon(screen, (120, 120, 120), poly, 1)
                #On the screen, grey color, vertices, size of the border
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
    
    cellsState = np.copy(nextCellsState)


    pygame.display.flip()       



pygame.quit()