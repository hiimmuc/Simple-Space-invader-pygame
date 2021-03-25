import math
import random

import pygame
from pygame import mixer

# initialize
pygame.init()
height = 600
width = 500
screen = pygame.display.set_mode(size=(width, height))
score = 0
clock = pygame.time.Clock()
life = 3
# icon
pygame.display.set_caption("Space invaders_ my first game")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
# Score_value
font = pygame.font.Font('freesansbold.ttf', 32)

# game over
game_over_text = pygame.font.Font('freesansbold.ttf', 64)


class Ship:

    def __init__(self):
        self.image = pygame.image.load('space-invaders2_.png')
        self.x = (width - 50) // 2
        self.y = height - 150
        self.move_horizontal = 0
        self.move_vertical = 0
        self.die = False

    def display(self):
        self.x += self.move_horizontal
        self.y += self.move_vertical
        if self.x <= 0:
            self.x = 0
        elif self.x >= width - 50:
            self.x = width - 50
        if self.y <= 0:
            self.y = 0
        elif self.y >= height - 125:
            self.y = height - 125

        screen.blit(self.image, (self.x, self.y))

    def respawn(self):
        global life
        self.x = (width - 50) // 2
        self.y = height - 150
        self.move_horizontal = 0
        self.move_vertical = 0
        self.die = False
        life -= 1

    def shoot(self):
        pass


class Bullet:

    def __init__(self):
        self.image = pygame.image.load('bullet_no_bg.png').convert()
        self.x = 0
        self.y = 0
        self.move_vertical = 0.5
        self.move_horizontal = 0
        self.ready = True

    def display(self):
        self.ready = False
        screen.blit(self.image, (self.x + 12.5, self.y - 35))

    def reload(self):
        self.ready = True


class Enemy:
    def __init__(self):
        self.image = pygame.image.load('ghost.png').convert()
        self.x = random.randrange(0, width - 25, 25)
        self.y = random.randrange(50, 125, 25)

        self.move_horizontal = 0.27
        self.move_vertical = 50
        self.die = False
        self.acceleration = 0.3

    def display(self):
        if self.x <= 0:
            self.x = 0
            self.y += self.move_vertical
            self.move_horizontal = self.acceleration
        elif self.x >= width - 50:
            self.x = width - 50
            self.y += self.move_vertical
            self.move_horizontal = -self.acceleration

        self.x += self.move_horizontal
        screen.blit(self.image, (self.x, self.y))

    def respawn(self):
        self.x = random.randrange(0, width - 25, 25)
        self.y = random.randrange(50, 125, 25)
        self.die = False


class Background:
    def __init__(self):
        # space back ground
        self.back_ground = pygame.image.load('background.jpg')
        # bottom city
        self.city = [pygame.image.load('cityscape.png'),
                     pygame.image.load('cityscape 2.png'),
                     pygame.image.load('cityscape3.png')]
        self.cloud = [pygame.image.load('cloud_1.png'),
                      pygame.image.load('cloud_2.png')]
        self.health = pygame.image.load('heart.png')

    def display(self):
        for i in range(life):
            screen.blit(self.health, (width - 50 - i * 50, 0))
        for place in range(0, width, 50):
            if place % 15 == 0:
                screen.blit(self.city[0], (place, height - 50))
            elif place % 10 == 0:
                screen.blit(self.city[1], (place, height - 50))
            else:
                screen.blit(self.city[2], (place, height - 50))

        for place in range(0, width, 50):
            if place % 100 == 0:
                screen.blit(self.cloud[0], (place, height - 100))
            else:
                screen.blit(self.cloud[1], (place, height - 100))


def main():
    global score
    bg = Background()
    bullet = Bullet()
    player = Ship()
    enemy = Enemy()
    running = True
    while running:
        clock.tick(-1)
        screen.fill((250, 250, 250))
        bg.display()
        # key pressed:
        for event in pygame.event.get():
            # if quit
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.move_horizontal = 0.3
                    print("-> right")
                if event.key == pygame.K_LEFT:
                    player.move_horizontal = -0.3
                    print("->left")
                if event.key == pygame.K_UP:
                    player.move_vertical = -0.3
                    print("->up")
                if event.key == pygame.K_DOWN:
                    player.move_vertical = 0.3
                    print("->down")
                if event.key == pygame.K_SPACE:
                    if bullet.ready:
                        bullet_sound = mixer.Sound('Gun+Shot2.wav')
                        bullet_sound.play()
                        bullet.x = player.x
                        bullet.y = player.y
                        bullet.display()
                    print("--> FIRE!!")
            if event.type == pygame.KEYUP:
                # keyup mean release
                if event.key == pygame.K_RIGHT or \
                        event.key == pygame.K_LEFT or \
                        event.key == pygame.K_UP or \
                        event.key == pygame.K_DOWN or \
                        event.key == pygame.K_SPACE:
                    player.move_horizontal = 0
                    player.move_vertical = 0
                    print("stop!!")
    # bullet movements:
        if bullet.y <= 0:
            bullet.y = player.y
            bullet.reload()
        if not bullet.ready:
            bullet.display()
            bullet.y -= bullet.move_vertical
    # game conditions:
        if is_collision([enemy.x, enemy.y], [bullet.x, bullet.y]) and bullet.ready is False:
            score += 10
            bullet.reload()
            bullet.x = player.x
            bullet.y = player.y
            # respawn enemy
            enemy.die = True
            enemy.acceleration += 0.01
            enemy.respawn()
        if is_ate([enemy.x, enemy.y], [player.x, player.y]):
            player.respawn()

        if is_lose([enemy.x, enemy.y]):
            running = False

        score_display = font.render("Score :" + str(score), True, (0, 0, 0))
        screen.blit(score_display, (0, 0))
        player.display()
        enemy.display()
        pygame.display.update()


def is_lose(enemy):
    if enemy[1] >= (height - 100) or life == 0:
        print('lose')
        text_display = game_over_text.render("GAME OVER", True, (250, 0, 0))
        screen.blit(text_display, (70, 180))
        pygame.display.update()
        pygame.time.delay(50)
        clock.tick(10)
        pygame.event.wait()
        return True
    else:
        return False


def is_collision(enemy, bullet):
    distance = math.sqrt(
        math.pow(enemy[0] - bullet[0], 2) + math.pow(enemy[1] - bullet[1], 2))
    if distance < 56:
        return True
    else:
        return False


def is_ate(enemy, ship):
    distance = math.sqrt(
        math.pow((enemy[0] - ship[0]), 2) + math.pow((enemy[1] - ship[1]), 2))
    if distance < 55:
        return True
    else:
        return False

# to replay: demo


def message_box():
    pass


# play music
# setup mixer to avoid sound lag
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.mixer.music.load('Anh Thanh Nien - HuyR.mp3')
pygame.mixer.music.play(-1)

main()
