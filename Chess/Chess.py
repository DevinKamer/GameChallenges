#Chess.py
#Devin Kamer
#5/9/16

"""A Chess Game built in Pygame"""

import pygame
import os

curDir = os.getcwd() + "/Pieces/"

class Piece(pygame.sprite.Sprite):
    def __init__(self, row, col, img, color):
        """img is a converted pygame image, color is either 'b' or 'w'"""
        self.image = img
        self.image = pygame.transform.scale(self.image, [64, 64])
        self.rect = img.get_rect()
        self.rect.x = row * 80
        self.rect.y = col * 80
        self.color = color

    def getPos(self):
        """Returns the Row and Column the piece occupies"""
        return self.rect.x / 80, self.rect.y / 80
    
    def setPos(self, row, column):
        """sets the row and col of the piece"""
        self.rect.x = row * 80
        self.rect.y = col * 80

    def draw(self, display):
        """Display is the pygame screen"""
        display.blit(self.image, [self.rect.x + 7, self.rect.y + 7])

    def getColor(self):
        return self.color

pygame.init()
size = (640, 640)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess")

done = False

clock = pygame.time.Clock()

background = pygame.image.load("Chess.png").convert()
background = pygame.transform.scale(background, size)
pieces = []

#White Row
curPieces = ["WhiteRook.png", "WhiteKnight.png", "WhiteBishop.png", "WhiteQueen.png",
          "WhiteKing.png", "WhiteBishop.png", "WhiteKnight.png", "WhiteRook.png"]
for i in range(len(curPieces)):
    piece = Piece(i, 7, pygame.image.load(curDir + curPieces[i]), 'w')
    pieces.append(piece)

#White Pawns
for i in range(8):
    pieces.append(Piece(i, 6, pygame.image.load(curDir + "WhitePawn.png"), 'w'))

#Black Row
curPieces = ["BlackRook.png", "BlackKnight.png", "BlackBishop.png", "BlackQueen.png",
          "BlackKing.png", "BlackBishop.png", "BlackKnight.png", "BlackRook.png"]
for i in range(len(curPieces)):
    piece = Piece(i, 0, pygame.image.load(curDir + curPieces[i]), 'b')
    pieces.append(piece)
    
#Black Pawns
for i in range(8):
    pieces.append(Piece(i, 1, pygame.image.load(curDir + "BlackPawn.png"), 'b'))

clickedPiece = None

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if clickedPiece == None:
                row, col = pygame.mouse.get_pos()
                row = row / 80
                col = col / 80
                for i in range(len(pieces)):
                    if pieces[i].getPos() == (row, col):
                        clickedPiece = pieces[i]
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if clickedPiece != None:
                inSpot = None
                row, col = pygame.mouse.get_pos()
                row = row / 80
                col = col / 80
                isOccupied = False
                for i in range(len(pieces)):
                    if pieces[i].getPos() == (row, col):
                        isOccupied = True
                        inSpot = pieces[i]
                        break

                if not isOccupied:
                    clickedPiece.setPos(row, col)
                    clickedPiece = None
                elif inSpot.getColor() != clickedPiece.getColor():
                    pieces.remove(inSpot)
                    clickedPiece.setPos(row, col)
                    clickedPiece = None
            
                
            

    screen.blit(background, [0, 0])

    for piece in pieces:
        piece.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
