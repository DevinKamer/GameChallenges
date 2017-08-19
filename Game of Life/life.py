#life.py
#Devin Kamer
#8/18/17

"""A Recreation of Conway's Game of Life in pygame"""

import pygame
import random

#constants
SCL = 16 #How big each square is
SIZE = (512, 512)

#Global variables
cells = []
space = False
mouse = False

class Cell(pygame.sprite.Sprite):

    def __init__(self, row, col):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([SCL, SCL])
        self.row = row
        self.col = col
        self.isDead = random.choice([True, False])
        self.image.fill([51, 51, 51])
        self.neighbors = 0

    def update(self):
        if self.isDead:
            if self.neighbors == 3:
                self.isDead = False
        else:
            self.neighbors -= 1 #It counts itself
            if self.neighbors < 2:
                self.isDead = True
            elif self.neighbors > 3:
                self.isDead = True

    def checkNeighbors(self):
        self.neighbors = 0
        for y in range(self.col - 1, self.col + 2):
            for x in range(self.row - 1 , self.row + 2):
                if x >= 0 and y >= 0:
                    try:
                        if cells[y][x].isDead == False:
                            self.neighbors += 1
                    except:
                        pass
        

    def draw(self):
        if self.isDead:
            self.image.fill([51, 51, 51])
        else:
            self.image.fill([150, 150, 150])

        screen.blit(self.image, [self.row * SCL, self.col * SCL])
            

pygame.init()
screen = pygame.display.set_mode(SIZE)
for col in range(SIZE[1] // SCL):
    colCel = []
    for row in range(SIZE[0] // SCL):
        colCel.append(Cell(row, col))

    cells.append(colCel)

done = False
pause = True

clock = pygame.time.Clock()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space = True

    mosX = pygame.mouse.get_pos()[0] // SCL
    mosY = pygame.mouse.get_pos()[1] // SCL
    if mouse:
        cells[mosY][mosX].isDead = not cells[mosY][mosX].isDead
        mouse = False
    
    if space:
        pause = not pause
        space = False
    
    if not pause:    
        for i in cells:
            for j in i:
                j.checkNeighbors()
        for i in cells:
            for j in i:
                j.update()

    


    screen.fill([0, 0, 0])
    for i in cells:
        for j in i:
            j.draw()

    pygame.display.flip()
    clock.tick(10)


pygame.quit()

    
    
                    
