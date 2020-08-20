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
from random import randint


width, height = 1000,1000
screen = pygame.display.set_mode((width,height))

background = 30, 30, 30
screen.fill(background)

numberCellsX, numberCellsY = 76,76

dimCellX = width / numberCellsX
dimCellY = height / numberCellsY

carryOn = True
pauseMode = False



#If the pdfFiles directory for that webpage does not exit, then it is created
Path("saved_games").mkdir(parents=True, exist_ok=True)  

#To store all the states we use a matrix. Alive = 1 . Dead = 0



cellsState = np.zeros((3,numberCellsX,numberCellsY)) 
# age, male 0/female 1, number of row, number of column

#To start with random cells placed:
#cellsState = np.random.choice([0,1], size=(3,numberCellsX,numberCellsY))
nextCellsState = np.copy(cellsState)

cellsState[0,37,38] = 1
cellsState[0,38,38] = 1
cellsState[0,39,38] = 1
cellsState[2,37,38] = 0
cellsState[2,38,38] = 1
cellsState[2,39,38] = 0



def save_file():
    now = datetime.now()
    np.save(now.strftime("saved_games/mod_%d|%m|%Y_%H:%M:%S"), cellsState)

def load_file():
     
    global nextCellsState
    pauseMode = True
    try:  
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()    
        if file_path:      
            nextCellsState = np.load(file_path)
            
    except: print("Error loading the file")
    pauseMode = False

def getColor(colorNum):
    if colorNum == 0: return (135,206,235)
    elif colorNum == 1: return (255,192,203) 
    else: return (255,255,255)                
            
def n_neighbours(x,y):
    #         *     *     *
    #         *   cell    *
    #         *     *     *
    # The * are the cells that we check
    # The game map is a toroidal structure so we get the module
    #return (#males, #females)
    return [(
                    cellsState[0, (x - 1) % numberCellsX, (y - 1) % numberCellsY]*(1-cellsState[2, (x - 1) % numberCellsX, (y - 1) % numberCellsY])
                    + cellsState[0, x % numberCellsX, (y - 1) % numberCellsY] * (1-cellsState[2, x % numberCellsX, (y - 1) % numberCellsY])
                    + cellsState[0,(x + 1) % numberCellsX, (y - 1) % numberCellsY]* (1-cellsState[2,(x + 1) % numberCellsX, (y - 1) % numberCellsY])
                    + cellsState[0,(x - 1) % numberCellsX, y % numberCellsY]* (1-cellsState[2,(x - 1) % numberCellsX, y % numberCellsY])
                    + cellsState[0,(x + 1) % numberCellsX, y % numberCellsY]* (1-cellsState[2,(x + 1) % numberCellsX, y % numberCellsY])
                    + cellsState[0,(x - 1) % numberCellsX, (y + 1) % numberCellsY]* (1-cellsState[2,(x - 1) % numberCellsX, (y + 1) % numberCellsY])
                    + cellsState[0,x % numberCellsX, (y + 1) % numberCellsY]* (1-cellsState[2,x % numberCellsX, (y + 1) % numberCellsY])
                    + cellsState[0,(x + 1) % numberCellsX, (y + 1) % numberCellsY]* (1-cellsState[2,(x + 1) % numberCellsX, (y + 1) % numberCellsY])
                ), 
                (
                    cellsState[0, (x - 1) % numberCellsX, (y - 1) % numberCellsY]*(cellsState[2, (x - 1) % numberCellsX, (y - 1) % numberCellsY])
                    + cellsState[0, x % numberCellsX, (y - 1) % numberCellsY] * (cellsState[2, x % numberCellsX, (y - 1) % numberCellsY])
                    + cellsState[0,(x + 1) % numberCellsX, (y - 1) % numberCellsY]* (cellsState[2,(x + 1) % numberCellsX, (y - 1) % numberCellsY])
                    + cellsState[0,(x - 1) % numberCellsX, y % numberCellsY]* (cellsState[2,(x - 1) % numberCellsX, y % numberCellsY])
                    + cellsState[0,(x + 1) % numberCellsX, y % numberCellsY]* (cellsState[2,(x + 1) % numberCellsX, y % numberCellsY])
                    + cellsState[0,(x - 1) % numberCellsX, (y + 1) % numberCellsY]* (cellsState[2,(x - 1) % numberCellsX, (y + 1) % numberCellsY])
                    + cellsState[0,x % numberCellsX, (y + 1) % numberCellsY]* (cellsState[2,x % numberCellsX, (y + 1) % numberCellsY])
                    + cellsState[0,(x + 1) % numberCellsX, (y + 1) % numberCellsY]* (cellsState[2,(x + 1) % numberCellsX, (y + 1) % numberCellsY])
                )]



while carryOn:     
    screen.fill(background)
    time.sleep(0.08)

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
            nextCellsState[0,celX,celY] = 1
            nextCellsState[2,celX,celY] = randint(0,1)
            

        if mouseClick[2] == 1:            
            nextCellsState[0,celX,celY] = 0    
    #Create grid
    for y in range(0, numberCellsY):
        for x in range(0, numberCellsX):

            if not pauseMode:
                n_neigh = n_neighbours(x,y)              
                
                #Rules:

                #1.-    Any dead cell with at least 2 live neighbours (1 male and 1 female) becomes a live cell, as if by reproduction.
                if cellsState[0, x, y]==0 and n_neigh[0]>0 and n_neigh[1]>0 and sum(n_neigh)==3:
                     nextCellsState[0, x, y]= 1
                     nextCellsState[1, x, y]= 0; 
                     #biological sex
                     cellsState[2,x,y] = randint(0,1)                   
                
                   

                #2.-    Any live cell with fewer than two live neighbours or more than 3 live neighbours dies

                elif cellsState[0,x, y]==1 and (sum(n_neigh) < 2 or  sum(n_neigh) >3):
                     nextCellsState[0, x, y]= 0
                     nextCellsState[1, x, y]= 0
                     

                #3.-    All lives cell age and die after 6s 

                
                if cellsState[1,x,y] >50:
                    nextCellsState[0,x, y]= 0
                    nextCellsState[1, x, y]= 0; 

                if cellsState[0,x, y] == 1:
                    nextCellsState[1,x, y] += 1

                
                

            poly = [   #They are the vertices of the rectangle
                (int(x * dimCellX), int(y * dimCellY)),
                (int((x + 1) * dimCellX), int(y * dimCellY)),
                (int((x + 1) * dimCellX), int((y + 1) * dimCellY)),
                (int(x * dimCellX), int((y + 1) * dimCellY)),
            ]


            #Draw cell
            
            if nextCellsState[0,x,y]==0:                
                pygame.draw.polygon(screen, (120, 120, 120), poly, 1)
                #On the screen, grey color, vertices, size of the border
            else:
                pygame.draw.polygon(screen, getColor(nextCellsState[2,x,y]), poly, 0)
                

                    
    
    cellsState = np.copy(nextCellsState)


    pygame.display.flip()       



pygame.quit()