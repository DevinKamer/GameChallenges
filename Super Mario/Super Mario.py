#Super Mario.py
#Devin Kamer
#5-15-17

"""Super Mario Bros in pygame"""

import pygame
import os
curDir = os.getcwd()

class Mario(pygame.sprite.Sprite):
    def __init__(self):
	
	#Load and Store Images
        self.idleRight = pygame.image.load(curDir + "/Small Mario/Idle.png").convert()
        self.idleRight = pygame.transform.scale(self.idleRight, [64, 64])
        self.idleRight.set_colorkey((192, 192, 192))
        self.idleLeft = pygame.transform.flip(self.idleRight, True, False)
        self.jumpRight = pygame.image.load(curDir + "/Small Mario/Jump.png").convert()
        self.jumpRight = pygame.transform.scale(self.jumpRight, [64, 64])
        self.jumpRight.set_colorkey((192, 192, 192))
        self.jumpLeft = pygame.transform.flip(self.jumpRight, True, False)
        self.walkRight = []
        self.walkLeft = []
        for i in range(0, 3):
            img = pygame.image.load(curDir + "/Small Mario/Walk" + str(i) + ".png").convert()
            img = pygame.transform.scale(img, [64, 64])
            img.set_colorkey((0, 0, 255))
            self.walkRight.append(img)
            img = pygame.transform.flip(img, True, False)
            self.walkLeft.append(img)

        self.clock = 0
        self.clockIndex = 0
        self.curImg = self.idleRight
        self.rect = self.idleRight.get_rect()
        self.rect.x = 64
        self.rect.y = size[1] - 128
        self.isJump = False
        self.faceRight = True


    def setImg(self, state, isRight):
        """state is i for idle, j for jump, or w for walk, isRight is bool"""
        if isRight:
            if state == 'i':
                self.curImg = self.idleRight
            elif state == 'j':
                self.curImg = self.jumpRight
            elif state == 'w':
                self.curImg = self.walkRight[self.clockIndex]
        else:
            if state == 'i':
                self.curImg = self.idleLeft
            elif state == 'j':
                self.curImg = self.jumpLeft
            elif state == 'w':
                self.curImg = self.walkLeft[self.clockIndex]

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        self.clock += 1
        if self.clock % 10 == 0:
            self.clockIndex += 1
            self.clockIndex = self.clockIndex % 3

        #Handles Image Switching
        if not self.isJump:
            if x > 0:
                self.faceRight = True
                self.setImg('w', True)
            elif x < 0:
                self.faceRight = False
                self.setImg('w', False)

            else:
                self.setImg('i', self.faceRight)
        else:
            self.setImg('j', self.faceRight)

    def draw(self, display):
        display.blit(self.curImg, self.rect)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(curDir + "/Blocks/Ground.png").convert()
        self.image = pygame.transform.scale(self.image, [64, 64])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, display):
        display.blit(self.image, self.rect)

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(curDir + "/Blocks/Brick.png").convert()
        self.image = pygame.transform.scale(self.image, [64, 64])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isHit = False

    def draw(self, display):
        if not self.isHit:
            display.blit(self.image, self.rect)
        


pygame.init()

size = (1280, 960)
screen = pygame.display.set_mode(size)

done = False

clock = pygame.time.Clock()

mario = Mario()
curX = 0
curY = 0
jump = False
canJump = True
gravity = 0
music = pygame.mixer.music.load(curDir + "/Super Mario Bros Theme.mp3")

ground = []
for i in range(size[0] / 64):
    ground.append(Platform(64 * i, size[1] - 64))

ground.remove(ground[4])
ground.remove(ground[4])
for i in range(13, 17):
    ground.append(Platform(64 * i, size[1] - 128))

bricks = []
for i in range(3, 8):
    bricks.append(Brick(i * 64, 64 * 10))
    
pygame.mixer.music.play()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            continue
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                curX = -3
            elif event.key == pygame.K_RIGHT:
                curX = 3

            elif event.key == pygame.K_SPACE:
                mario.isJump = True
                jump = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                curX = 0
    
    touching = None
    for i in range(len(ground)):
        if pygame.sprite.collide_rect(mario, ground[i]):
            if ground[i].rect.collidepoint(mario.rect.midbottom):
                touching = ground[i]
            elif ground[i].rect.collidepoint(mario.rect.midleft):
                curX = 0
                mario.rect.x += 3
            elif ground[i].rect.collidepoint(mario.rect.midright):
                curX = 0
                mario.rect.x -= 3

    hitBlock = False
    for i in range(len(bricks) - 1, -1, -1):
        if pygame.sprite.collide_rect(mario, bricks[i]):
            if bricks[i].rect.collidepoint(mario.rect.midtop):
                bricks[i].isHit = True
                hitBlock = True
                bricks.remove(bricks[i])
            elif bricks[i].rect.collidepoint(mario.rect.midbottom):
                touching = bricks[i]
            elif bricks[i].rect.collidepoint(mario.rect.midleft):
                curX = 0
                mario.rect.x += 3
            elif bricks[i].rect.collidepoint(mario.rect.midright):
                curX = 0
                mario.rect.x -= 3

    if jump and canJump:
        gravity += 2.5
        jump = False
        touching = None
        canJump = False

    if touching:
        gravity = 0
        mario.rect.y = touching.rect.y - 63
        canJump = True
        mario.isJump = False
        curY = 0
    else:
        gravity -= .125
        if gravity < -1:
            gravity = -1
        if hitBlock:
            gravity = -3
        curY -= gravity

    if curY < -10:
        curY = -10


    mario.update(curX, curY)
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.rewind()
        pygame.mixer.music.play()

    screen.fill((70, 130, 180))

    mario.draw(screen)
    for i in ground:
        i.draw(screen)

    for i in bricks:
        i.draw(screen)
                  
                  

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

