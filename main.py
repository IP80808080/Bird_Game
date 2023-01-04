import pygame
from pygame.locals import *
import sys
import random

pygame.init()
clock = pygame.time.Clock()
fps = 100

# Screen
screen = pygame.display.set_mode((412, 470))
pygame.display.set_caption('Flappy Bird')

#Define Font
font = pygame.font.SysFont('Bauhaus 83', 60)

#Define Color
white = (255, 255, 255)

# Game Variable
ground_scroll = 0
sroll_speed = 3
flying = False
game_over = False
pipe_gap = 110
pipe_frequency =1000
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# Images
bg = pygame.image.load("Assests/sprites/background.png")
base = pygame.image.load("Assests/sprites/base1.png")
button_img = pygame.image.load("Assests/sprites/gameover.png")

########## Score ###########

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = 470//2
    score = 0
    return score

########## BIRD ############

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'Assests/sprites/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velo = 0
        self.clicked = False

    def update(self):

        #Physics
        if flying == True:
            self.velo += 0.5
            if self.velo > 4:
                self.velo = 2
            if self.rect.bottom < 370:
                self.rect.y += int(self.velo)

        if game_over == False:
            #Jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velo = -7
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #handle the animation (All 3 Images Combine)
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # handle the animation (Rotate)
            self.image = pygame.transform.rotate(self.images[self.index], self.velo * -2)

        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

########## PIPE ############

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assests/sprites/pipe-green.png")
        self.rect = self.image.get_rect()
        # 1 is for top, -1 is for bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]

    def update(self):
        self.rect.x -= (sroll_speed)
        if self.rect.right < 0:
            self.kill()

########### Restart Game #########

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action =False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #Draw Button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(470/2))
bird_group.add(flappy)

#create restart button instance
button = Button(452//4, 500//3, button_img)

run = True
while run:

    clock.tick(fps)

    # background
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)


    #Base
    screen.blit(base, (ground_scroll, 370))

    #Check the Score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(30), 20)


    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top <0:
        game_over = True

    #Gameover
    if flappy.rect.bottom >= 370:
        game_over = True
        flying = False

    # Base Scrolling
    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(412, int(472 / 2) + pipe_height, -1)
            pipe_group.add(bottom_pipe)
            top_pipe = Pipe(412, int(472 / 2) + pipe_height, 1)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        #Ground Scroll
        ground_scroll -= sroll_speed
        if abs(ground_scroll) > 70:
            ground_scroll = 0
        pipe_group.update()

    #Check  for game Restart
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score =reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True


    pygame.display.update()

pygame.quit()