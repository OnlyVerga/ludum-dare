import pygame
import data.engine as e
import sys
import random

pygame.init()
pygame.font.init()
pygame.mixer.set_num_channels(64)

font = pygame.font.Font("data/fonts/Silver.ttf", 20)
big_font = pygame.font.Font("data/fonts/Silver.ttf", 50)
clock = pygame.time.Clock()
main_theme = pygame.mixer.Sound('data/audio/main_theme.wav')
main_theme.play(-1)

thunder_sound = pygame.mixer.Sound('data/audio/lightning.wav')
#exit_level = pygame.mixer.Sound('data/audio/change_scene.wav')

WIN_DIM = (608, 416)
DISP_DIM = (WIN_DIM[0] / 2, WIN_DIM[1] / 2)

#       setup basic stuff
window = pygame.display.set_mode(WIN_DIM)
display = pygame.Surface(DISP_DIM)
pygame.display.set_caption("Magic Rush")
life = pygame.image.load("data/graphics/life.png")

e.load_animations("data/graphics/")
e.load_levels("data/levels/")

total_levels = 10

#active_color = e.blue

class Platform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collider = pygame.Rect((self.x, self.y, 16, 16))
        self.type = "platform"
        self.img = pygame.image.load(e.animation_folder + self.type +".png")

    def blit(self, display):
        display.blit(self.img, (self.x, self.y))

class Half_Platform(Platform):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.collider = pygame.Rect((self.x, self.y, 16, 8))
        self.type = "half_platform"
        self.img = pygame.image.load(e.animation_folder + self.type +".png")

class Spike(Half_Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "spike"
        self.img = e.entity(x,y, 16, 8, "spike")

    def collide(self, player):
        if player.obj.rect.colliderect(self.collider):
            return True

    def blit(self, display):
        self.img.display(display, [0, 0])
        self.img.change_frame(1)

class Key:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collider = pygame.Rect((self.x, self.y, 16, 16))
        self.type = "key"
        self.img = e.entity(x, y, 16, 16, self.type)

    def collide(self, player):
        if player.obj.rect.colliderect(self.collider):
            return True

    def blit(self, display):
        self.img.display(display, [0, 0])
        self.img.change_frame(1)

class Colored(Platform):
    def __init__(self, x, y, color, type):
        super().__init__(x, y)
        self.color = color
        self.type = type
        self.active=True
        self.img = pygame.image.load(e.animation_folder + self.type + ".png")
        self.transparent = pygame.image.load(e.animation_folder + self.type + "_transparent.png")

    def blit(self, display, active_color):
        if active_color == self.color:
            display.blit(self.img, (self.x, self.y))
            self.active = True
        else:
            display.blit(self.transparent, (self.x, self.y))
            self.active = False

class Button(Half_Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color=e.grey
        self.collider = pygame.Rect((self.x, self.y+8, 16, 8))
        self.type = "button"
        self.img = pygame.image.load(e.animation_folder + self.type + ".png")
        self.checker = False

    def blit(self, display):
        display.blit(self.img, (self.x, self.y+8))

class onButton():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collider = pygame.Rect((self.x, self.y, 16, 8))
        self.type = "onbutton"
        self.checker = False

    def collide(self, player):
        if player.obj.rect.colliderect(self.collider) and not self.checker:
            self.checker = True
            return True
        else:
            if not player.obj.rect.colliderect(self.collider):
                self.checker = False
            return False

class Movable(Half_Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.start = (x, y)
        self.end = (0, 0)
        self.dir = "to_end"
        self.type = "movable"
        self.dire = "r"

    def move(self):
        self.collider = pygame.Rect((self.x, self.y, 16, 8))
        if self.dir == "to_end":
            if self.end[0] > self.x:
                self.x += 1
                self.dire="r"
            if self.end[0] < self.x:
                self.x -= 1
                self.dire = "l"
            if self.end[0] == self.x:
                self.dir = "to_start"

        if self.dir == "to_start":
            if self.start[0] > self.x:
                self.x += 1
                self.dire = "r"
            if self.start[0] < self.x:
                self.x -= 1
                self.dire = "l"
            if self.start[0] == self.x:
                self.dir = "to_end"

    def collide(self, player):
        if player.obj.rect.colliderect(self.collider):
            return True