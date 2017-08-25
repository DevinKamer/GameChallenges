#Minesweeper.py
#Devin Kamer
#8/25/17

"""A Recreation of Minesweeper in pygame"""

import pygame
import random

class Tile(pygame.sprite.Sprite):
    """Clickable tiles that indicate how many bombs are near by"""
    def __init__(self, col, row):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = None
        self.isBomb = False
        self.neighbors = 0
        self.isClicked = False

    def setBomb(self):
        self.isBomb = True
        self.image = bombImage

    def checkNeighbors(self):
        if not self.isBomb:    
            self.neighbors = 0
            for y in range(self.col - 1, self.col + 2):
                for x in range(self.row - 1 , self.row + 2):
                    if x >= 0 and y >= 0:
                        try:
                            if tiles[y][x].isBomb:
                                self.neighbors += 1
                        except:
                            pass
            self.image = text.render(str(self.neighbors), True, [0, 0, 255])

    def click(self):
        if self.isBomb:
            pygame.quit()
        if self.isClicked:
            pass
        self.isClicked = True
        if self.neighbors == 0:
            for y in range(self.col - 1, self.col + 2):
                for x in range(self.row - 1 , self.row + 2):
                    if x >= 0 and y >= 0:
                        try:
                            if not tiles[y][x].isClicked:
                                tiles[y][x].click()
                        except:
                            pass
            
    

    def draw(self):
        if self.isClicked:
            pygame.draw.rect(screen, [64,64,64], [self.row * scl + scl // 8, self.col * scl + scl // 8, scl * 7 // 8, scl * 7 // 8])
            if self.image != None:
                if self.isBomb:
                    screen.blit(self.image, [self.row * scl + scl // 8, self.col * scl + scl // 8])
                else:
                    screen.blit(self.image, [self.row * scl + scl // 4, self.col * scl + scl // 4])
        else:
            pygame.draw.rect(screen, [100, 100, 100], [self.row * scl + scl // 8, self.col * scl + scl // 8, scl * 7 // 8, scl * 7 // 8])
                



pygame.init()
pygame.font.init()

size = (640, 640)
scl = 64

screen = pygame.display.set_mode(size)
text = pygame.font.Font(None, scl)
bombImage = pygame.image.load("bomb.png").convert()
bombImage = pygame.transform.scale(bombImage, [scl * 7 // 8, scl * 7 // 8])


#2d array [y][x]
tiles = []

for y in range(size[1] // scl):
    newRow = []
    for x in range(size[0] // scl):
        newRow.append(Tile(y, x))
    tiles.append(newRow)


bombs = 10
while bombs != 0:
    randy = random.randrange(0, len(tiles))
    randx = random.randrange(0, len(tiles[randy]))
    if not tiles[randy][randx].isBomb:
        tiles[randy][randx].setBomb()
        bombs -= 1

for y in tiles:
    for x in y:
        x.checkNeighbors()

clock = pygame.time.Clock()
done = False
mouse = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            continue
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = True

    mosX = pygame.mouse.get_pos()[0] // scl
    mosY = pygame.mouse.get_pos()[1] // scl
    if mouse:
        tiles[mosY][mosX].click()
        mouse = False

    screen.fill([128, 128, 128])
    for y in tiles:
        for x in y:
            x.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
