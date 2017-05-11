#Snake.py
#Devin Kamer
#5/10/17

"""A Simple Pygame Snake game"""

import pygame
import random

class Segment(pygame.sprite.Sprite):
    """A individual piece of a snake"""
    def __init__(self, coords):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([16, 16])
        self.image.fill([255, 255, 255])
        self.rect = self.image.get_rect()
        row, col = coords
        self.rect.x = row * 16
        self.rect.y = col * 16
        self.isDead = False

    def update(self, coords):
        row, col = coords
        self.rect.x = row * 16
        self.rect.y = col * 16

    def getPos(self):
        return self.rect.x / 16, self.rect.y / 16

    def draw(self, display):
        display.blit(self.image, [self.rect.x, self.rect.y])


class Food(pygame.sprite.Sprite):
    """A piece of food"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([16, 16])
        self.image.fill([255, 255, 0])
        self.rect = self.image.get_rect()
        self.eat()

    def eat(self):
        self.rect.x = random.randint(0, 39) * 16
        self.rect.y = random.randint(0, 39) * 16

    def getPos(self):
        return self.rect.x / 16, self.rect.y / 16

    def draw(self, display):
        display.blit(self.image, [self.rect.x, self.rect.y])


#Main Program
#40 rows & col
pygame.init()
size = (640, 640)
screen = pygame.display.set_mode(size)
traveled = [[10, 20]]
snake = [Segment(traveled[0])]
food = Food()
direction = 'r'
frameRate = 5

done = False

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        #Testing for Arrow Keys
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = 'l'
            elif event.key == pygame.K_RIGHT:
                direction = 'r'
            elif event.key == pygame.K_UP:
                direction = 'u'
            elif event.key == pygame.K_DOWN:
                direction = 'd'



    #Finding which direction to go
    if direction == 'l':
        traveled.append([traveled[-1][0] - 1, traveled[-1][1]])
    elif direction == 'r':
        traveled.append([traveled[-1][0] + 1, traveled[-1][1]])
    elif direction == 'u':
        traveled.append([traveled[-1][0], traveled[-1][1] - 1])
    elif direction == 'd':
        traveled.append([traveled[-1][0], traveled[-1][1] + 1])

    collision = []
    for i in range(len(snake)):
        snake[i].update(traveled[len(traveled) - 1 - i])
        collision.append(snake[i].getPos())

    for i in collision:
        if collision.count(i) > 1:
            done = True
        elif i == food.getPos():
            food.eat()
            snake.append(Segment(traveled[len(traveled) - 1 - len(snake)]))
            frameRate += 1

        if traveled[-1][0] < 0 or traveled[-1][0] > 39:
            done = True
        elif traveled[-1][1] < 0 or traveled[-1][1] > 39:
            done = True
    screen.fill((100, 100, 100))

    for piece in snake:
        piece.draw(screen)
    food.draw(screen)

        
    pygame.display.flip()
    clock.tick(frameRate)

pygame.quit()

