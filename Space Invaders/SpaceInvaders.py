#SpaceInvaders.py
#Devin Kamer
#5/11/17

"""A simple clone of Space Invaders"""

import pygame
import random

class Alien(pygame.sprite.Sprite):
    """A enemy meant to be in an array"""
    def __init__(self, row, col):
        pygame.sprite.Sprite.__init__(self)
        self.path = ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'd',
                     'l', 'l', 'l', 'l', 'l', 'l', 'l', 'l', 'd']
        self.curPath = 0
        self.coolDown = 60
        self.image = pygame.image.load("Enemy.png").convert()
        self.image.set_colorkey([0, 0, 0])
        self.image = pygame.transform.scale(self.image, [80, 80])
        self.rect = self.image.get_rect()
        #20 Rows & Cols
        self.rect.x = row * 64
        self.rect.y = col * 64
        self.bullets = []

    def update(self):
        if self.coolDown == 0:
            self.curPath += 1
            self.curPath = self.curPath % len(self.path)
            cur = self.path[self.curPath]
            if cur == 'r':
                self.rect.x += 32
            elif cur == 'l':
                self.rect.x -= 32
            elif cur == 'd':
                self.rect.y += 32
            self.coolDown = 60
        else:
            self.coolDown -= 1
        self.makeBullet()
        for i in self.bullets:
            if i.isDead:
                self.bullets.remove(i)
            else:
                i.update()

    def draw(self, display):
        display.blit(self.image, [self.rect.x, self.rect.y])
        for i in self.bullets:
            i.draw(display)

    def makeBullet(self):
        if random.randint(1, 750) == 1:
            self.bullets.append(Bullet(self.rect.x + 16, self.rect.y + 32, False))

class Player(pygame.sprite.Sprite):
    """Ship that player controls"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Ship.png").convert()
        self.image.set_colorkey([255, 255, 255])
        self.image = pygame.transform.scale(self.image, [64, 32])
        self.rect = self.image.get_rect()
        self.rect.x = 298
        self.rect.y = 640 - 32
        self.bullets = []
        self.health = 5

    def update(self, x):
        self.rect.x += x
        for i in self.bullets:
            if i.isDead:
                self.bullets.remove(i)
            else:
                i.update()

    def draw(self, display):
        display.blit(self.image, [self.rect.x, self.rect.y])
        for i in self.bullets:
            i.draw(display)

    def makeBullet(self):
        if len(self.bullets) < 3:
            self.bullets.append(Bullet(self.rect.x + 32, self.rect.y, True))

class Bullet(pygame.sprite.Sprite):
    """Bullet fired from ships or enemy"""
    def __init__(self, x, y, isUp):
        """x = x position, isUp is true if from ship, false if from alien"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([8, 32])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isUp = isUp
        self.isDead = False
        if isUp:
            self.image.fill([0, 255, 0])
        else:
            self.image.fill([255, 255, 255])

    def update(self):
        if self.isUp:
            self.rect.y -= 4
            if self.rect.y < 0:
                self.isDead = True
            for i in aliens:
                if pygame.sprite.collide_rect(i, self):
                    aliens.remove(i)
                    self.isDead = True
        else:
            self.rect.y += 4
            if self.rect.y > 640:
                self.isDead = True
            if pygame.sprite.collide_rect(self, player):
                player.health -= 1
                self.isDead = True
                
        

    def draw(self, display):
        display.blit(self.image, [self.rect.x, self.rect.y])
            
        
        


pygame.init()
size = (640, 640)
screen = pygame.display.set_mode(size)

done = False

clock = pygame.time.Clock()

aliens = []
for y in range(3):
    for x in range(1, 6):
        aliens.append(Alien(x, y))

player = Player()
direction = 0

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = -4
            elif event.key == pygame.K_RIGHT:
                direction = 4
            elif event.key == pygame.K_SPACE:
                player.makeBullet()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                direction = 0

    player.update(direction)
    if player.health == 0:
        done = True
    if len(aliens) == 0:
        done = True

    screen.fill([100, 100, 100])

    for i in range(len(aliens)):
        aliens[i].update()
        aliens[i].draw(screen)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

    

                

        
